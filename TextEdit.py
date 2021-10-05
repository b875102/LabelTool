from PyQt5 import QtCore
from PyQt5 import QtWidgets

class TextEdit(QtCore.QObject):
    
    _FILE_URL = 'file:///'
    
    def __init__(self, widget):
        super().__init__(widget)
        
        self.widget = widget
        
        self.widget.installEventFilter(self)
        self.widget.setAcceptDrops(True)
        
    def eventFilter(self, source, event):
        #print('eventFilter')
        
        if event.type() == QtCore.QEvent.DragEnter:
            # we need to accept this event explicitly to be able to receive QDropEvents!
            event.accept()
        if event.type() == QtCore.QEvent.Drop:
            md = event.mimeData()
            if md.hasUrls():
                mdtext = md.text()
                if self._FILE_URL in mdtext:
                    mdtext = mdtext.replace(self._FILE_URL, '')
                    self.widget.setText(mdtext)
                    return True
        return super().eventFilter(source, event)        