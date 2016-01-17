"""Line numbers and bookmarks areas
"""

from PyQt4.QtCore import QPoint, Qt, pyqtSignal
from PyQt4.QtGui import QPainter, QPalette, \
                        QPixmap, QMenu,\
                        QTextBlock, QToolTip, QWidget

import qutepart
from qutepart.bookmarks import Bookmarks


class LineNumberArea(QWidget):
    """Line number area widget
    """
    _LEFT_MARGIN = 5
    _RIGHT_MARGIN = 3

    def __init__(self, qpart):
        QWidget.__init__(self, qpart)
        self._qpart = qpart

    def paintEvent(self, event):
        """QWidget.paintEvent() implementation
        """
        painter = QPainter(self)
        painter.fillRect(event.rect(), self.palette().color(QPalette.Window))
        painter.setPen(Qt.black)

        block = self._qpart.firstVisibleBlock()
        blockNumber = block.blockNumber()
        top = int(self._qpart.blockBoundingGeometry(block).translated(self._qpart.contentOffset()).top())
        bottom = top + int(self._qpart.blockBoundingRect(block).height())
        singleBlockHeight = self._qpart.cursorRect().height()

        width = None

        boundingRect = self._qpart.blockBoundingRect(block)
        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(blockNumber + 1)
                painter.drawText(0, top, self.width() - self._RIGHT_MARGIN, self._qpart.fontMetrics().height(),
                                 Qt.AlignRight, number)
                if boundingRect.height() >= singleBlockHeight * 2:  # wrapped block
                    if width is None:
                        width = self.width()  # laizy calculation
                    painter.fillRect(1, top + singleBlockHeight,
                                     width - 2, boundingRect.height() - singleBlockHeight - 2,
                                     Qt.darkGreen)

            block = block.next()
            boundingRect = self._qpart.blockBoundingRect(block)
            top = bottom
            bottom = top + int(boundingRect.height())
            blockNumber += 1

    def width(self):
        """Desired width. Includes text and margins
        """
        digits = len(str(max(1, self._qpart.blockCount())))
        return self._LEFT_MARGIN + self._qpart.fontMetrics().width('9') * digits + self._RIGHT_MARGIN


class MarkArea(QWidget):

    blockClicked = pyqtSignal(QTextBlock)
    blockDoubleClicked = pyqtSignal(int)

    _MARGIN = 1

    def __init__(self, qpart):
        QWidget.__init__(self, qpart)
        self._qpart = qpart

        qpart.blockCountChanged.connect(self.update)

        self.setMouseTracking(True)

        self._bookmarkPixmap = self._loadIcon('bookmark.png')
        self._lintPixmaps = {qpart.LINT_ERROR: self._loadIcon('lint-error.png'),
                             qpart.LINT_WARNING: self._loadIcon('lint-warning.png'),
                             qpart.LINT_NOTE: self._loadIcon('lint-note.png')}
        self._bpPixmap = self._loadIcon('bp.png')
        self._bpcPixmap = self._loadIcon('bpcond.png')
        self._bpdPixmap = self._loadIcon('bpdis.png')
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)        
        
    def showContextMenu(self,pos):
        if self._qpart.mainWindow:
            menu=QMenu()
            cursor = self._qpart.cursorForPosition(QPoint(0, pos.y()))
            block = cursor.block()
            self._qpart.contextMenuLine=block.firstLineNumber()
            self._qpart.mainWindow.insertContextMenuItems(self._qpart,menu)
            menu.exec_(self._qpart.viewport().mapToGlobal(pos))

    def _loadIcon(self, fileName):
        defaultSizePixmap = QPixmap(qutepart.getIconPath(fileName))
        iconSize = self._qpart.cursorRect().height()
        return defaultSizePixmap.scaled(iconSize, iconSize, transformMode=Qt.SmoothTransformation)


    def sizeHint(self, ):
        """QWidget.sizeHint() implementation
        """
        return QSize(self.width(), 0)

    def paintEvent(self, event):
        """QWidget.paintEvent() implementation
        Draw markers
        """
        painter = QPainter(self)
        painter.fillRect(event.rect(), self.palette().color(QPalette.Window))

        block = self._qpart.firstVisibleBlock()
        blockBoundingGeometry = self._qpart.blockBoundingGeometry(block).translated(self._qpart.contentOffset())
        top = blockBoundingGeometry.top()
        bottom = top + blockBoundingGeometry.height()

        for block in qutepart.iterateBlocksFrom(block):
            height = self._qpart.blockBoundingGeometry(block).height()
            if top > event.rect().bottom():
                break
            if block.isVisible() and \
               bottom >= event.rect().top():
                if block.blockNumber() in self._qpart.lintMarks:
                    msgType, msgText = self._qpart.lintMarks[block.blockNumber()]
                    pixMap = self._lintPixmaps[msgType]
                    yPos = top + ((height - pixMap.height()) / 2)  # centered
                    painter.drawPixmap(0, yPos, pixMap)
                    
                bp=self._qpart.bpMarks.get(block.blockNumber())
                if bp:
                    pix=self._bpdPixmap
                    if bp.isEnabled():
                        pix=self._bpcPixmap if bp.condition() else self._bpPixmap
                    yPos = top + ((height - self._bpPixmap.height()) / 2)  # centered
                    painter.drawPixmap(0, yPos, pix)

                if Bookmarks.isBlockMarked(block):
                    yPos = top + ((height - self._bookmarkPixmap.height()) / 2)  # centered
                    painter.drawPixmap(0, yPos, self._bookmarkPixmap)

            top += height

    def width(self):
        """Desired width. Includes text and margins
        """
        return self._MARGIN + self._bookmarkPixmap.width() + self._MARGIN

    def mouseDoubleClickEvent(self,mouseEvent):
        cursor = self._qpart.cursorForPosition(QPoint(0, mouseEvent.y()))
        block = cursor.block()
        blockRect = self._qpart.blockBoundingGeometry(block).translated(self._qpart.contentOffset())
        if blockRect.bottom() >= mouseEvent.y():  # clicked not lower, then end of text
            self.blockDoubleClicked.emit(block.firstLineNumber())

    def mousePressEvent_Old(self, mouseEvent):
        cursor = self._qpart.cursorForPosition(QPoint(0, mouseEvent.y()))
        block = cursor.block()
        blockRect = self._qpart.blockBoundingGeometry(block).translated(self._qpart.contentOffset())
        if blockRect.bottom() >= mouseEvent.y():  # clicked not lower, then end of text
            self.blockClicked.emit(block)

    def mouseMoveEvent(self, event):
        blockNumber = self._qpart.cursorForPosition(event.pos()).blockNumber()
        if blockNumber in self._qpart._lintMarks:
            msgType, msgText = self._qpart._lintMarks[blockNumber]
            QToolTip.showText(event.globalPos(), msgText)
        else:
            QToolTip.hideText()

        return QWidget.mouseMoveEvent(self, event)
