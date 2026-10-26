"""Minimal Language Server Protocol client, used to get code completions from clangd

One clangd process is run per workspace root.  It is started on demand, and
restarted if it exits unexpectedly.
"""

import glob
import json
import os
import pathlib
import re
import shutil
import time

from PyQt6.QtCore import QObject, QProcess, QTimer


CPP_EXTENSIONS = {
    '.c': 'c',
    '.cpp': 'cpp', '.cc': 'cpp', '.cxx': 'cpp', '.c++': 'cpp',
    '.h': 'cpp', '.hpp': 'cpp', '.hh': 'cpp', '.hxx': 'cpp', '.inl': 'cpp',
}

# Give up restarting clangd if it crashes this many times within RESTART_WINDOW_SEC
MAX_RESTARTS = 3
RESTART_WINDOW_SEC = 60

_clangdPath = None
_clangdSearched = False
_client = None


def languageId(path):
    """Return the LSP language id for a file, or None if clangd does not handle it"""
    return CPP_EXTENSIONS.get(os.path.splitext(path)[1].lower())


def pathToUri(path):
    return pathlib.Path(os.path.abspath(path)).as_uri()


def findClangd():
    """Locate a clangd executable.  Prefers plain 'clangd', then the newest clangd-NN"""
    global _clangdPath, _clangdSearched
    if _clangdSearched:
        return _clangdPath
    _clangdSearched = True
    _clangdPath = shutil.which('clangd')
    if not _clangdPath:
        candidates = []
        for d in os.environ.get('PATH', '').split(os.pathsep):
            for p in glob.glob(os.path.join(d, 'clangd-*')):
                m = re.match(r'clangd-(\d+)$', os.path.basename(p))
                if m and os.access(p, os.X_OK):
                    candidates.append((int(m.group(1)), p))
        if candidates:
            _clangdPath = max(candidates)[1]
    if not _clangdPath:
        print('clangd not found.  Using simple word completion')
    return _clangdPath


def getClient(root):
    """Return a running client for the workspace root, or None if clangd is not available"""
    global _client
    if not root or not os.path.isdir(root):
        return None
    root = os.path.abspath(root)
    if _client is not None and _client.root != root:
        _client.shutdown()
        _client = None
    if _client is None:
        exe = findClangd()
        if not exe:
            return None
        _client = LanguageClient(root, exe)
    if not _client.isAlive():
        return None
    return _client


def shutdown():
    global _client
    if _client is not None:
        _client.shutdown()
        _client = None


class LanguageClient(QObject):
    def __init__(self, root, executable):
        QObject.__init__(self)
        self.root = root
        self.executable = executable
        self._process = None
        self._buffer = b''
        self._nextId = 1
        self._callbacks = {}
        self._initialized = False
        self._pending = []        # messages queued until the initialize handshake completes
        self._documents = {}      # path -> [languageId, version, textGetter, dirty]
        self._restarts = []
        self._stopping = False
        self._failed = False
        self._start()

    def isAlive(self):
        return not self._failed

    def _start(self):
        self._buffer = b''
        self._callbacks = {}
        self._initialized = False
        self._pending = []
        self._process = QProcess(self)
        self._process.setWorkingDirectory(self.root)
        self._process.setStandardErrorFile(QProcess.nullDevice())
        self._process.readyReadStandardOutput.connect(self._onReadyRead)
        self._process.finished.connect(self._onFinished)
        args = [
            '--compile-commands-dir={}'.format(self.root),
            '--background-index',
            '--header-insertion=never',
            '--header-insertion-decorators=0',
            '--query-driver=/usr/bin/*g++*,/usr/bin/*gcc*,/usr/bin/c++,/usr/bin/cc',
            '--log=error',
        ]
        self._process.start(self.executable, args)
        if not self._process.waitForStarted(5000):
            print('Failed to start {}'.format(self.executable))
            self._failed = True
            return
        params = {
            'processId': os.getpid(),
            'rootUri': pathToUri(self.root),
            'capabilities': {
                'textDocument': {
                    'synchronization': {'didSave': True},
                    'completion': {
                        'completionItem': {'snippetSupport': False},
                        'contextSupport': True,
                    },
                },
            },
        }
        self._send({'jsonrpc': '2.0', 'id': self._newId(self._onInitialized),
                    'method': 'initialize', 'params': params}, force=True)

    def _onInitialized(self, result, error):
        if error:
            print('clangd initialization failed: {}'.format(error.get('message')))
            return
        self._initialized = True
        self._send({'jsonrpc': '2.0', 'method': 'initialized', 'params': {}})
        pending = self._pending
        self._pending = []
        for msg in pending:
            self._send(msg)
        # Reopen documents after a restart
        for path, doc in self._documents.items():
            self._sendDidOpen(path, doc)

    def _onFinished(self, exitCode, exitStatus):
        if self._stopping:
            return
        now = time.time()
        self._restarts = [t for t in self._restarts if now - t < RESTART_WINDOW_SEC]
        if len(self._restarts) >= MAX_RESTARTS:
            print('clangd keeps exiting.  Language server disabled')
            self._failed = True
            return
        self._restarts.append(now)
        print('clangd exited (code {}).  Restarting'.format(exitCode))
        for cb in self._callbacks.values():
            cb(None, {'message': 'clangd exited'})
        self._process.deleteLater()
        QTimer.singleShot(500, self._start)

    def shutdown(self):
        if self._process is None or self._stopping:
            return
        self._stopping = True
        if self._process.state() == QProcess.ProcessState.Running:
            if self._initialized:
                self._send({'jsonrpc': '2.0', 'id': self._newId(None), 'method': 'shutdown'})
                self._send({'jsonrpc': '2.0', 'method': 'exit'})
            self._process.closeWriteChannel()
            if not self._process.waitForFinished(1000):
                self._process.kill()
                self._process.waitForFinished(1000)

    # ---- transport ----

    def _newId(self, callback):
        id = self._nextId
        self._nextId += 1
        if callback is not None:
            self._callbacks[id] = callback
        return id

    def _send(self, msg, force=False):
        if self._failed or self._process is None:
            return
        if not self._initialized and not force:
            self._pending.append(msg)
            return
        body = json.dumps(msg).encode('utf-8')
        self._process.write(b'Content-Length: %d\r\n\r\n' % len(body) + body)

    def _onReadyRead(self):
        self._buffer += bytes(self._process.readAllStandardOutput())
        while True:
            sep = self._buffer.find(b'\r\n\r\n')
            if sep < 0:
                return
            length = None
            for line in self._buffer[:sep].split(b'\r\n'):
                name, _, value = line.partition(b':')
                if name.strip().lower() == b'content-length':
                    length = int(value.strip())
            if length is None:
                # Malformed header; drop it
                self._buffer = self._buffer[sep + 4:]
                continue
            if len(self._buffer) < sep + 4 + length:
                return
            body = self._buffer[sep + 4:sep + 4 + length]
            self._buffer = self._buffer[sep + 4 + length:]
            try:
                msg = json.loads(body.decode('utf-8'))
            except ValueError:
                continue
            self._handleMessage(msg)

    def _handleMessage(self, msg):
        if 'id' in msg and 'method' in msg:
            # Server to client request (e.g. workDoneProgress/create).  Acknowledge it
            self._send({'jsonrpc': '2.0', 'id': msg['id'], 'result': None}, force=True)
        elif 'id' in msg:
            cb = self._callbacks.pop(msg['id'], None)
            if cb:
                cb(msg.get('result'), msg.get('error'))
        # Notifications (diagnostics, progress) are currently ignored

    # ---- documents ----

    def openDocument(self, path, textGetter):
        """Register an open editor.  textGetter returns the current document text"""
        lang = languageId(path)
        if lang is None:
            return
        doc = [lang, 1, textGetter, False]
        self._documents[path] = doc
        self._sendDidOpen(path, doc)

    def _sendDidOpen(self, path, doc):
        doc[3] = False
        self._send({'jsonrpc': '2.0', 'method': 'textDocument/didOpen', 'params': {
            'textDocument': {'uri': pathToUri(path), 'languageId': doc[0],
                             'version': doc[1], 'text': doc[2]()}}})

    def closeDocument(self, path):
        if self._documents.pop(path, None) is not None:
            self._send({'jsonrpc': '2.0', 'method': 'textDocument/didClose', 'params': {
                'textDocument': {'uri': pathToUri(path)}}})

    def isOpen(self, path):
        return path in self._documents

    def documentChanged(self, path):
        """Mark document as modified.  Text is sent lazily, before the next request"""
        doc = self._documents.get(path)
        if doc:
            doc[3] = True

    def documentSaved(self, path):
        self._flush(path)
        if path in self._documents:
            self._send({'jsonrpc': '2.0', 'method': 'textDocument/didSave', 'params': {
                'textDocument': {'uri': pathToUri(path)}}})

    def _flush(self, path):
        doc = self._documents.get(path)
        if doc and doc[3]:
            doc[1] += 1
            doc[3] = False
            self._send({'jsonrpc': '2.0', 'method': 'textDocument/didChange', 'params': {
                'textDocument': {'uri': pathToUri(path), 'version': doc[1]},
                'contentChanges': [{'text': doc[2]()}]}})

    # ---- requests ----

    def completion(self, path, line, character, callback):
        """Request completions at a position (0 based line, UTF-16 column).
        callback(items, isIncomplete) is called with items=None on failure.
        Each item is a dict with 'label', 'detail', 'insertText' and 'filterText'
        """
        if path not in self._documents:
            callback(None, False)
            return
        self._flush(path)

        def onResult(result, error):
            if error or result is None:
                callback(None, False)
                return
            if isinstance(result, list):
                items, incomplete = result, False
            else:
                items, incomplete = result.get('items', []), result.get('isIncomplete', False)
            callback([self._convertItem(i) for i in items], incomplete)

        self._send({'jsonrpc': '2.0', 'id': self._newId(onResult),
                    'method': 'textDocument/completion', 'params': {
                        'textDocument': {'uri': pathToUri(path)},
                        'position': {'line': line, 'character': character}}})

    @staticmethod
    def _convertItem(item):
        label = item.get('label', '').strip()
        textEdit = item.get('textEdit')
        if textEdit and 'newText' in textEdit:
            insertText = textEdit['newText']
        else:
            insertText = item.get('insertText') or label
        return {
            'label': label,
            'detail': item.get('detail', ''),
            'insertText': insertText,
            'filterText': item.get('filterText') or insertText,
        }
