from PyQt4 import QtCore
from PyQt4 import QtGui


class WatchesTree(QtGui.QTreeWidget):
    def __init__(self,parent=None):
        super(WatchesTree,self).__init__(parent)
        
        
    def keyPressEvent(self,event):
        if event.key() == QtCore.Qt.Key_Delete:
            for item in self.selectedItems():
                index=self.indexOfTopLevelItem(item)
                # Do not remove last row
                if index>=0 and index!=(self.topLevelItemCount()-1):
                    self.takeTopLevelItem(index)
        return super(WatchesTree,self).keyPressEvent(event)


