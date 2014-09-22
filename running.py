from PyQt4 import QtCore
from PyQt4 import QtGui

class RunningWidget(QtGui.QWidget):
    def __init__(self,parent=None):
        super(RunningWidget,self).__init__(parent)
        self.timer=QtCore.QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start(100)
        self.angle=0.0
        self.setMinimumSize(QtCore.QSize(64,64))
        self.setMaximumSize(QtCore.QSize(64,64))

    def update(self):
        self.angle+=0.2
        self.repaint()
        
    def paintEvent(self,event):
        qp=QtGui.QPainter()
        qp.begin(self)
        self.drawRunning(qp,event.rect())
        qp.end()

    def drawRunning(self,qp,r):
        qp.setBrush(QtGui.QBrush(QtGui.QColor(0,0,0)))
        c=r.center()
        rad=24
        steps=8
        import math
        for i in xrange(0,steps):
            angle=self.angle+i*(2*3.14159265*(1.0/steps))
            cs=math.cos(angle)
            sn=math.sin(angle)
            x=c.x()+cs*rad
            y=c.y()+sn*rad
            p=QtCore.QPointF(x,y)
            curRad=(i+1.0)
            qp.drawEllipse(p,curRad,curRad)


