from PyQt6 import QtCore
from PyQt6 import QtWidgets
import errno
import fcntl
import os
import subprocess
import termios
import time
import globals


class VarNode:
    def __init__(self, name='', value=''):
        self.name = name
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def _bool_setting(value):
    if isinstance(value, str):
        return value.lower() not in ('0', 'false', 'no', '')
    return bool(value)


def _mi_quote(text):
    if isinstance(text, list):
        if len(text) == 1:
            text = text[0]
        else:
            text = ''.join(str(part) for part in text)
    elif text is None:
        text = ''
    elif not isinstance(text, str):
        text = str(text)
    res = ['"']
    for ch in text:
        if ch == '\\':
            res.append('\\\\')
        elif ch == '"':
            res.append('\\"')
        elif ch == '\n':
            res.append('\\n')
        elif ch == '\r':
            res.append('\\r')
        elif ch == '\t':
            res.append('\\t')
        else:
            code = ord(ch)
            if 32 <= code < 127:
                res.append(ch)
            else:
                res.append('\\{:03o}'.format(code))
    res.append('"')
    return ''.join(res)


def _decode_mi_string(text):
    res = []
    index = 0
    while index < len(text):
        ch = text[index]
        if ch != '\\':
            res.append(ch)
            index += 1
            continue
        index += 1
        if index >= len(text):
            break
        esc = text[index]
        if esc == 'n':
            res.append('\n')
            index += 1
        elif esc == 'r':
            res.append('\r')
            index += 1
        elif esc == 't':
            res.append('\t')
            index += 1
        elif esc == 'a':
            res.append('\a')
            index += 1
        elif esc == 'b':
            res.append('\b')
            index += 1
        elif esc == 'f':
            res.append('\f')
            index += 1
        elif esc == 'v':
            res.append('\v')
            index += 1
        elif esc in ('\\', '"', "'"):
            res.append(esc)
            index += 1
        elif esc == 'x':
            index += 1
            digits = []
            while index < len(text) and text[index] in '0123456789abcdefABCDEF':
                digits.append(text[index])
                index += 1
            if digits:
                res.append(chr(int(''.join(digits), 16)))
        elif esc in '01234567':
            digits = [esc]
            index += 1
            for _ in range(2):
                if index < len(text) and text[index] in '01234567':
                    digits.append(text[index])
                    index += 1
                else:
                    break
            res.append(chr(int(''.join(digits), 8)))
        else:
            res.append(esc)
            index += 1
    return ''.join(res)


def _store_result(mapping, key, value):
    if key in mapping:
        cur = mapping[key]
        if isinstance(cur, list):
            cur.append(value)
        else:
            mapping[key] = [cur, value]
    else:
        mapping[key] = value


def _as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def _named_items(value, key):
    if isinstance(value, dict):
        items = value.get(key, [])
        if isinstance(items, list):
            return items
        if items is None:
            return []
        return [items]
    return []


def _as_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def _record_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if not isinstance(value, dict):
        return [value]
    if not value:
        return []

    max_len = 1
    for item in value.values():
        if isinstance(item, list):
            max_len = max(max_len, len(item))

    if max_len == 1:
        return [value]

    res = []
    for index in range(max_len):
        row = {}
        for key, item in value.items():
            if isinstance(item, list):
                if index < len(item):
                    row[key] = item[index]
            elif index == 0:
                row[key] = item
        if row:
            res.append(row)
    return res


class MIParser:
    def __init__(self, text):
        self.text = text
        self.index = 0

    def parse_record(self):
        token = ''
        while self.index < len(self.text) and self.text[self.index].isdigit():
            token += self.text[self.index]
            self.index += 1
        if self.index >= len(self.text):
            return None
        kind = self.text[self.index]
        self.index += 1
        if kind in ('~', '@', '&'):
            payload = self.parse_value()
            return {
                'type': 'stream',
                'channel': kind,
                'token': token,
                'payload': payload,
            }
        record_class = self.read_until(',').strip()
        results = {}
        if self.index < len(self.text) and self.text[self.index] == ',':
            self.index += 1
            results = self.parse_results(())
        record_type = 'result'
        if kind in ('*', '+', '='):
            record_type = 'async'
        return {
            'type': record_type,
            'kind': kind,
            'token': token,
            'class': record_class,
            'results': results,
        }

    def read_until(self, *terminators):
        start = self.index
        while self.index < len(self.text) and self.text[self.index] not in terminators:
            self.index += 1
        return self.text[start:self.index]

    def parse_results(self, terminators):
        res = {}
        while self.index < len(self.text):
            if self.text[self.index] in terminators:
                break
            name = self.read_until('=')
            if self.index >= len(self.text) or self.text[self.index] != '=':
                break
            self.index += 1
            value = self.parse_value()
            _store_result(res, name, value)
            if self.index < len(self.text) and self.text[self.index] == ',':
                self.index += 1
        return res

    def parse_value(self):
        if self.index >= len(self.text):
            return ''
        ch = self.text[self.index]
        if ch == '"':
            return self.parse_c_string()
        if ch == '{':
            return self.parse_tuple()
        if ch == '[':
            return self.parse_list()
        return self.parse_atom()

    def parse_c_string(self):
        self.index += 1
        raw = []
        while self.index < len(self.text):
            ch = self.text[self.index]
            if ch == '"':
                self.index += 1
                break
            if ch == '\\' and self.index + 1 < len(self.text):
                raw.append(ch)
                self.index += 1
                raw.append(self.text[self.index])
                self.index += 1
                continue
            raw.append(ch)
            self.index += 1
        return _decode_mi_string(''.join(raw))

    def parse_tuple(self):
        self.index += 1
        if self.index < len(self.text) and self.text[self.index] == '}':
            self.index += 1
            return {}
        res = self.parse_results(('}',))
        if self.index < len(self.text) and self.text[self.index] == '}':
            self.index += 1
        return res

    def parse_list(self):
        self.index += 1
        if self.index < len(self.text) and self.text[self.index] == ']':
            self.index += 1
            return []
        if self.is_result_list():
            res = self.parse_results((']',))
            if self.index < len(self.text) and self.text[self.index] == ']':
                self.index += 1
            return res
        res = []
        while self.index < len(self.text):
            if self.text[self.index] == ']':
                self.index += 1
                break
            res.append(self.parse_value())
            if self.index < len(self.text) and self.text[self.index] == ',':
                self.index += 1
        return res

    def is_result_list(self):
        probe = self.index
        while probe < len(self.text) and self.text[probe] not in ',]':
            if self.text[probe] == '=':
                return True
            if self.text[probe] in '"{[':
                return False
            probe += 1
        return False

    def parse_atom(self):
        start = self.index
        while self.index < len(self.text) and self.text[self.index] not in ',}]':
            self.index += 1
        return self.text[start:self.index]


class GDBWrapper:
    """Wrapper above the GDB process using the MI interface."""

    MAX_VAR_DEPTH = 3
    MAX_VAR_CHILDREN = 64

    def __init__(self, bps, args, dir):
        settings = QtCore.QSettings()
        self.breakpoints = bps
        self.breakpoints.breakpointsChanged.connect(self.setBreakpoints)
        dataRoot = os.path.dirname(os.path.abspath(__file__))

        self.args = ['gdb', '--quiet', '--interpreter=mi2', '--args'] + args
        self.debugged = os.path.abspath(args[0])

        self.dumpLog = None
        if len(os.getenv('COIDE', '')) > 0:
            self.dumpLog = open('dump.log', 'w')

        self.gdb = None
        self.stdoutBuffer = ''
        self.stderrBuffer = ''
        self.pendingResults = {}
        self.nextToken = 1
        self.outputText = []

        self.running = False
        self.active = False
        self.changed = True
        self.allFiles = set()
        self.pid = ''
        self.expectingInterrupt = False

        self.inferiorMaster = None
        self.inferiorSlave = None
        self.inferiorTTY = ''
        self.initInferiorTTY()

        self.gdb = subprocess.Popen(
            self.args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=dir,
        )
        self.setNonBlocking(self.gdb.stdout.fileno())
        self.setNonBlocking(self.gdb.stderr.fileno())

        self.poll(0.2)
        self.sendCommand('-gdb-set confirm off', allow_error=True)
        self.sendCommand('-gdb-set pagination off', allow_error=True)
        self.sendCommand('-gdb-set mi-async on', allow_error=True)
        self.sendCommand('-inferior-tty-set {}'.format(_mi_quote(self.inferiorTTY)), allow_error=True)
        self.sendCommand('-enable-pretty-printing', allow_error=True)

        if _bool_setting(settings.value('customPrinters', True)):
            self.initializePrettyPrints(dataRoot)

        self.setBreakpoints()
        self.startInferior()

    def initInferiorTTY(self):
        master, slave = os.openpty()
        attrs = termios.tcgetattr(slave)
        attrs[3] &= ~termios.ECHO
        if hasattr(termios, 'ECHONL'):
            attrs[3] &= ~termios.ECHONL
        termios.tcsetattr(slave, termios.TCSANOW, attrs)
        self.setNonBlocking(master)
        self.inferiorMaster = master
        self.inferiorTTY = os.ttyname(slave)
        os.close(slave)
        self.inferiorSlave = None

    def setNonBlocking(self, fd):
        flags = fcntl.fcntl(fd, fcntl.F_GETFL)
        fcntl.fcntl(fd, fcntl.F_SETFL, flags | os.O_NONBLOCK)

    def startInferior(self):
        self.sendCommand('-break-insert -t {}'.format(_mi_quote('main')), allow_error=True, timeout=5.0)
        self.sendCommand('-exec-run', allow_error=True, timeout=5.0)
        self.waitForStop(30.0)

    def initializePrettyPrints(self, dataRoot):
        path = os.path.join(dataRoot, 'gdb_printers', 'python')
        cmd = (
            'python import sys;'
            'sys.path.insert(0,{!r});'
            'from eigen.printers import register_eigen_printers;'
            'register_eigen_printers(None)'
        ).format(path)
        res = self.runConsoleCommand(cmd, allow_error=True)
        if res and res.get('class') == 'error':
            print('Failed to install pretty prints')

    def quitDebugger(self):
        if not self.gdb:
            return
        if self.running:
            self.actStop()
        try:
            self.sendCommand('-gdb-exit', allow_error=True, timeout=2.0)
        except (BrokenPipeError, OSError, TimeoutError):
            pass
        try:
            self.gdb.wait(timeout=2.0)
        except subprocess.TimeoutExpired:
            self.gdb.kill()
            self.gdb.wait()
        self.closeResources()

    def closeResources(self):
        if self.inferiorMaster is not None:
            os.close(self.inferiorMaster)
            self.inferiorMaster = None
        if self.inferiorSlave is not None:
            os.close(self.inferiorSlave)
            self.inferiorSlave = None
        if self.dumpLog is not None:
            self.dumpLog.close()
            self.dumpLog = None
        self.gdb = None

    def closingApp(self):
        self.quitDebugger()

    def update(self):
        self.poll(0.0)
        return ''

    def sendInput(self, s):
        if self.inferiorMaster is None or not s:
            return
        try:
            os.write(self.inferiorMaster, s.encode('utf-8', errors='replace'))
        except OSError:
            pass

    def hasOutput(self):
        return len(self.outputText) > 0

    def getOutput(self):
        s = ''.join(self.outputText)
        self.outputText = []
        return s

    def getBackTrace(self):
        if self.active or not self.running:
            return []
        frames = self.getFrames()
        return [self.formatFrame(frame) for frame in frames]

    def isValidSource(self, cand):
        if cand.startswith('/usr'):
            return False
        if cand.find('built-in') > 0:
            return False
        validExts = {'.c', '.cpp', '.cxx', '.C', '.cc'}
        for ext in validExts:
            if cand.endswith(ext):
                return True
        return False

    def getAllFiles(self):
        res = self.sendCommand('-file-list-exec-source-files', allow_error=True)
        if not res or res.get('class') != 'done':
            return []
        files = set()
        for item in _as_list(res.get('results', {}).get('files')):
            if not isinstance(item, dict):
                continue
            cand = item.get('fullname') or item.get('file') or ''
            if cand and self.isValidSource(cand):
                files.add(cand)
        self.allFiles = files
        return sorted(list(files))

    def updatePath(self, name):
        if not name:
            return name
        if name[0] == '/':
            return name
        for path in self.allFiles:
            if path.endswith(name):
                return path
        return name

    def getCurrentPos(self):
        res = [('', 1)]
        if not self.running or self.active:
            return res
        frames = self.getFrames()
        if frames:
            res = []
            for frame in frames:
                path = self.framePath(frame)
                line = _as_int(frame.get('line'), 0)
                if path and line > 0:
                    res.append((path, line))
            if res:
                self.changed = False
        return res

    def log(self, s):
        if self.dumpLog is not None:
            self.dumpLog.write(s)
            self.dumpLog.write('\n')
            self.dumpLog.flush()

    def sendCommand(self, command, timeout=5.0, allow_error=False):
        if not self.gdb or not self.gdb.stdin:
            raise RuntimeError('Debugger is not running')
        token = str(self.nextToken)
        self.nextToken += 1
        line = '{}{}\n'.format(token, command)
        if globals.dev:
            print('>{}'.format(line.rstrip()))
        self.log('>{}'.format(line.rstrip()))
        self.gdb.stdin.write(line.encode('utf-8'))
        self.gdb.stdin.flush()
        return self.waitForResult(token, timeout, allow_error)

    def waitForResult(self, token, timeout=5.0, allow_error=False):
        deadline = time.time() + timeout
        while time.time() < deadline:
            rec = self.pendingResults.pop(token, None)
            if rec is not None:
                if globals.dev:
                    print(rec)
                self.log('<<{}'.format(rec))
                if rec.get('class') == 'error' and not allow_error:
                    raise RuntimeError(self.resultMessage(rec))
                return rec
            self.poll(0.05)
        raise TimeoutError('Timeout waiting for gdb command {}'.format(token))

    def waitForStop(self, timeout=5.0):
        deadline = time.time() + timeout
        while time.time() < deadline:
            self.poll(0.05)
            if not self.active:
                return True
        return False

    def runConsoleCommand(self, command, allow_error=False, timeout=5.0):
        return self.sendCommand(
            '-interpreter-exec console {}'.format(_mi_quote(command)),
            allow_error=allow_error,
            timeout=timeout,
        )

    def resultMessage(self, rec):
        msg = rec.get('results', {}).get('msg', '')
        if msg:
            return msg
        return rec.get('class', 'error')

    def poll(self, timeout=0.0):
        deadline = time.time() + timeout
        while True:
            progressed = False
            progressed |= self.readGDBOutput()
            progressed |= self.readGDBErrors()
            progressed |= self.readInferiorOutput()
            if not progressed:
                if timeout <= 0.0 or time.time() >= deadline:
                    break
                time.sleep(0.01)
        if self.gdb and self.gdb.poll() is not None:
            self.running = False
            self.active = False

    def readChunk(self, fd):
        try:
            return os.read(fd, 4096)
        except BlockingIOError:
            return b''
        except OSError as e:
            if e.errno in (errno.EAGAIN, errno.EWOULDBLOCK, errno.EIO):
                return b''
            raise

    def readGDBOutput(self):
        if not self.gdb or not self.gdb.stdout:
            return False
        chunk = self.readChunk(self.gdb.stdout.fileno())
        if not chunk:
            return False
        self.stdoutBuffer += chunk.decode('utf-8', errors='replace')
        progressed = True
        while True:
            if self.stdoutBuffer.startswith('(gdb) '):
                self.stdoutBuffer = self.stdoutBuffer[6:]
                continue
            pos = self.stdoutBuffer.find('\n')
            if pos < 0:
                break
            line = self.stdoutBuffer[:pos].rstrip('\r')
            self.stdoutBuffer = self.stdoutBuffer[(pos + 1):]
            if line and line != '(gdb)':
                self.handleRecord(line)
        if self.stdoutBuffer in ('(gdb)', '(gdb) '):
            self.stdoutBuffer = ''
        return progressed

    def readGDBErrors(self):
        if not self.gdb or not self.gdb.stderr:
            return False
        chunk = self.readChunk(self.gdb.stderr.fileno())
        if not chunk:
            return False
        text = chunk.decode('utf-8', errors='replace')
        self.stderrBuffer += text
        self.outputText.append(text)
        return True

    def readInferiorOutput(self):
        if self.inferiorMaster is None:
            return False
        try:
            chunk = os.read(self.inferiorMaster, 4096)
        except BlockingIOError:
            return False
        except OSError as e:
            if e.errno in (errno.EAGAIN, errno.EWOULDBLOCK, errno.EIO):
                return False
            raise
        if not chunk:
            return False
        self.outputText.append(chunk.decode('utf-8', errors='replace'))
        return True

    def handleRecord(self, line):
        if globals.dev:
            print(line)
        self.log('<<{}'.format(line))
        rec = MIParser(line).parse_record()
        if rec is None:
            return
        if rec.get('type') == 'stream':
            if rec.get('channel') == '@':
                self.outputText.append(rec.get('payload', ''))
            return
        if rec.get('type') == 'result':
            self.pendingResults[rec.get('token', '')] = rec
            return
        self.handleAsyncRecord(rec)

    def handleAsyncRecord(self, rec):
        results = rec.get('results', {})
        kind = rec.get('kind')
        rec_class = rec.get('class')
        if kind == '*' and rec_class == 'running':
            self.active = True
            self.running = True
            return
        if kind == '*' and rec_class == 'stopped':
            reason = results.get('reason', '')
            self.active = False
            self.changed = True
            if reason.startswith('exited') or reason == 'exited':
                self.running = False
            else:
                self.running = True
            if reason == 'signal-received':
                sig = results.get('signal-name', '')
                if sig and not (sig == 'SIGINT' and self.expectingInterrupt):
                    QtWidgets.QMessageBox.critical(None, 'Unhandled Signal', sig)
            return
        if kind == '=' and rec_class == 'thread-group-started':
            self.pid = results.get('pid', '')
            return
        if kind == '=' and rec_class == 'thread-group-exited':
            self.running = False
            self.active = False
            self.changed = True

    def clearBreakpoints(self):
        self.sendCommand('-break-delete', allow_error=True)

    def setBreakpoint(self, path, line, cond):
        cmd = '-break-insert'
        if cond:
            cmd += ' -c {}'.format(_mi_quote(cond))
        cmd += ' {}'.format(_mi_quote('{}:{}'.format(path, line)))
        self.sendCommand(cmd, allow_error=True)
        self.changed = True

    def setBreakpoints(self):
        if not self.gdb:
            return
        self.clearBreakpoints()
        for path in self.breakpoints.paths():
            bps = self.breakpoints.pathBreakpoints(path)
            for bp in bps:
                if bp.isEnabled():
                    self.setBreakpoint(path, bp.line() + 1, bp.condition())

    def runExecCommand(self, command):
        if self.active or (not self.running and command != '-exec-run'):
            return
        self.sendCommand(command, allow_error=True, timeout=5.0)

    def actStep(self):
        if self.running and not self.active:
            self.runExecCommand('-exec-step')

    def actNext(self):
        if self.running and not self.active:
            self.runExecCommand('-exec-next')

    def actOut(self):
        if self.running and not self.active:
            self.runExecCommand('-exec-finish')

    def actCont(self):
        if not self.running:
            self.runExecCommand('-exec-run')
        elif not self.active:
            self.runExecCommand('-exec-continue')

    def actBreak(self):
        if not self.active:
            return
        self.expectingInterrupt = True
        try:
            self.sendCommand('-exec-interrupt --all', allow_error=True, timeout=2.0)
            if self.waitForStop(5.0):
                self.active = False
            else:
                self.log('Break Failed')
                print('Failed to break gdb')
        finally:
            self.expectingInterrupt = False
        self.changed = True

    def actStop(self):
        if not self.running:
            return
        self.runConsoleCommand('kill', allow_error=True, timeout=5.0)
        deadline = time.time() + 5.0
        while time.time() < deadline:
            self.poll(0.05)
            if not self.running:
                break

    def printVar(self, var):
        if self.active or not self.running:
            return ''
        res = self.sendCommand(
            '-data-evaluate-expression {}'.format(_mi_quote(var)),
            allow_error=True,
        )
        if not res or res.get('class') != 'done':
            return ''
        return res.get('results', {}).get('value', '')

    def evaluate(self, var):
        if self.active or not self.running:
            return None
        obj = self.createVarObject(var)
        if not obj:
            value = self.printVar(var)
            if not value:
                return None
            return VarNode(var, value)
        try:
            return self.varObjectToNode(var, obj)
        finally:
            name = obj.get('name', '')
            if name:
                self.sendCommand('-var-delete {}'.format(_mi_quote(name)), allow_error=True)

    def createVarObject(self, expr):
        res = self.sendCommand(
            '-var-create - * {}'.format(_mi_quote(expr)),
            allow_error=True,
        )
        if not res or res.get('class') != 'done':
            return None
        return res.get('results', {})

    def varObjectToNode(self, displayName, varObj):
        value = varObj.get('value', '')
        if not value and _as_int(varObj.get('numchild'), 0) > 0:
            value = varObj.get('type', '')
        node = VarNode(displayName, value)
        self.populateVarChildren(node, varObj, 0)
        return node

    def populateVarChildren(self, node, varObj, depth):
        if _as_int(varObj.get('numchild'), 0) <= 0 and varObj.get('dynamic') != '1':
            return
        if depth >= self.MAX_VAR_DEPTH:
            node.add_child(VarNode('...', 'depth limit'))
            return
        name = varObj.get('name', '')
        if not name:
            return
        res = self.sendCommand(
            '-var-list-children --all-values {}'.format(_mi_quote(name)),
            allow_error=True,
        )
        if not res or res.get('class') != 'done':
            return
        children = _named_items(res.get('results', {}).get('children'), 'child')
        totalChildren = len(children)
        if totalChildren > self.MAX_VAR_CHILDREN:
            children = children[:self.MAX_VAR_CHILDREN]
        for child in children:
            if not isinstance(child, dict):
                continue
            childName = child.get('exp') or child.get('name', '').rsplit('.', 1)[-1]
            childValue = child.get('value', '')
            if not childValue and _as_int(child.get('numchild'), 0) > 0:
                childValue = child.get('type', '')
            childNode = VarNode(childName, childValue)
            node.add_child(childNode)
            self.populateVarChildren(childNode, child, depth + 1)
        if totalChildren > self.MAX_VAR_CHILDREN or res.get('results', {}).get('has_more') == '1':
            node.add_child(VarNode('...', 'truncated'))

    def flatten(self, root):
        if not root:
            return ''
        res = root.value
        if len(root.children) > 0:
            res += ' { '
            for index, child in enumerate(root.children):
                if index > 0:
                    res += ', '
                res += self.flatten(child)
            res += ' } '
        return res

    def evaluateAsText(self, var):
        root = self.evaluate(var)
        return self.flatten(root)

    def nodeFromSimpleItem(self, item):
        name = item.get('name', '')
        if not name:
            return None
        value = item.get('value')
        if value is not None:
            return VarNode(name, value)
        return self.evaluate(name)

    def localsInfo(self):
        if self.active or not self.running:
            return {}
        res = {}
        args = self.sendCommand('-stack-list-arguments --simple-values 0 0', allow_error=True)
        if args and args.get('class') == 'done':
            frames = _named_items(args.get('results', {}).get('stack-args'), 'frame')
            if frames:
                for arg in _record_list(frames[0].get('args')):
                    if isinstance(arg, dict) and 'name' in arg:
                        node = self.nodeFromSimpleItem(arg)
                        if node:
                            res[arg['name']] = node
        locals_res = self.sendCommand('-stack-list-locals --simple-values', allow_error=True)
        if locals_res and locals_res.get('class') == 'done':
            for item in _record_list(locals_res.get('results', {}).get('locals')):
                if isinstance(item, dict) and 'name' in item and item['name'] not in res:
                    node = self.nodeFromSimpleItem(item)
                    if node:
                        res[item['name']] = node
        return res

    def getLocals(self):
        return self.localsInfo()

    def getFrames(self):
        res = self.sendCommand('-stack-list-frames', allow_error=True)
        if not res or res.get('class') != 'done':
            return []
        return _named_items(res.get('results', {}).get('stack'), 'frame')

    def framePath(self, frame):
        path = frame.get('fullname') or frame.get('file') or ''
        return self.updatePath(path)

    def formatFrame(self, frame):
        level = frame.get('level', '?')
        func = frame.get('func', '??')
        path = self.framePath(frame)
        line = frame.get('line', '')
        if path and line:
            return '#{} {} at {}:{}'.format(level, func, path, line)
        source = frame.get('from') or frame.get('addr', '')
        if source:
            return '#{} {} from {}'.format(level, func, source)
        return '#{} {}'.format(level, func)
