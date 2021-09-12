from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QPen
import copy
from Label import Label

class Image(QtCore.QObject):
    
    _SCALING_BASE = 100
    _RND_NO = 2
    
    _mouseMoveEvent = QtCore.pyqtSignal(QtCore.QPoint)
    _labelChangedEvent = QtCore.pyqtSignal(list)

    def __init__(self, widget, imagePath):
        super().__init__(widget)
        
        #print('Image__init__')
        
        self._widget = widget

        self.widget.setMouseTracking(True)
        self.widget.installEventFilter(self)
        
        self.imagePath = imagePath
        self.pixmap = QPixmap(self.imagePath)
        self.scaledPixmap = self.pixmap.copy()
        self.cloneImage = self.scaledPixmap.copy()
        
        self.scalingRatio = 1
        self.labels = []
        self.ScaleImage()

        self.drawing = False
        self.lastPoint = QtCore.QPoint()
        
    def __del__(self):
        pass
    
    @property
    def widget(self):
        return self._widget


    def eventFilter(self, source, event):
        #print('MouseTracker: eventFilter_{0}'.format(event.type()))
        if source is self.widget:
            if event.type() == QtCore.QEvent.MouseMove:
                self._mouseMoveEvent.emit(self.cursorPosition(event.pos()))
                self.mouseMoveEvent(event)
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                self.mousePressEvent(event)
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                self.mouseReleaseEvent(event)
            elif event.type() == QtCore.QEvent.Paint:
                self.paintEvent(event)
                
        return super().eventFilter(source, event)
  

    def paintEvent(self, event):
        '''
        print('paintEvent', self.cloneImage.rect())
        painter = QPainter(self.cloneImage)
        painter.drawPixmap(self.cloneImage.rect(), self.cloneImage)
        '''
    
    def mousePressEvent(self, event):
        #print('mousePressEvent')
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = self.cursorPosition(event.pos())
            #self.lastPoint = event.pos()# + QPoint(-9, -9)

    def mouseMoveEvent(self, event):
        #print('mouseMoveEvent')
        if event.buttons() and Qt.LeftButton and self.drawing:
            if self.lastPoint:
                currentPosition = self.cursorPosition(event.pos())
                #currentPosition = event.pos()# + QPoint(-9, -9)
                tmpLabels = copy.deepcopy(self.labels)
                tmpLabels.append(Label(self.lastPoint, currentPosition))
                self.drawLine(tmpLabels)
        else:
            for label in self.labels:
                label.isSelected(event.pos())
            self.drawLine(self.labels)

    def mouseReleaseEvent(self, event):
        #print('mouseReleaseEvent')
        if event.button() == Qt.LeftButton:
            currentPosition = self.cursorPosition(event.pos())
            #currentPosition = event.pos()# + QPoint(-9, -9)
            if Label.isDifferent(self.lastPoint, currentPosition):
                self.labels.append(Label(self.lastPoint, currentPosition))
                self.drawLine(self.labels)
                self.drawing = False
                self._labelChangedEvent.emit(self.labels)

    #implement
    '''
    def SetImage(self, imagePath, labels):
        self.imagePath = imagePath
        self.pixmap = QPixmap(self.imagePath)
        self.scaledPixmap = self.pixmap.copy()
        self.cloneImage = self.scaledPixmap.copy()
    '''
    
    def ScaleImage(self, scaling = _SCALING_BASE):
        self.scalingRatio = round((scaling / self._SCALING_BASE), self._RND_NO)
        scaledWidth, scaledHeight = self.pixmap.width() * self.scalingRatio, self.pixmap.height() * self.scalingRatio
        self.scaledPixmap = self.pixmap.scaled(scaledWidth, scaledHeight, QtCore.Qt.KeepAspectRatio)
        self.cloneImage = self.scaledPixmap.copy()
        
        self.widget.resize(scaledWidth, scaledHeight)
        self.widget.setPixmap(self.cloneImage)

        self.drawLine(self.labels)
        
    def cursorPosition(self, pos):
        origSize = self.pixmap.size()
        scaledSize = self.widget.pixmap().size()
        #print('original size: ', origSize.width(), origSize.height())
        #print('scaled size:   ', scaledSize.width(), scaledSize.height())
        ratioWidth, ratioHeight = origSize.width() / scaledSize.width(), origSize.height() / scaledSize.height()
        p = QPoint(int(pos.x() * ratioWidth), int(pos.y() * ratioHeight))
        return p
        
    def size(self):
        return self.pixmap.size()
    
    def scaledSize(self):
        self.lblImage.pixmap().size()
        
    def drawLine(self, labels):
        #print('drawLine')
        
        self.cloneImage = self.scaledPixmap.copy()
        painter = QPainter(self.cloneImage)
        
        redPen = QPen(Qt.red, 3, Qt.SolidLine)
        greenPen = QPen(Qt.green, 3, Qt.SolidLine)
        
        
        for label in labels:
            lastPos, currentPos = label.shape.p1, label.shape.p2
            p1 = lastPos * self.scalingRatio
            p2 = currentPos * self.scalingRatio
            
            if label.selected:
                painter.setPen(greenPen)
            else:
                painter.setPen(redPen)
                
            painter.drawLine(p1, p2)
            
            #print('drawLine', lastPos, currentPos)
            
        painter.end()
        
        #self.widget.update()
        
        self.widget.setPixmap(self.cloneImage)
        
        #print('drawLine', self.imagePath)

