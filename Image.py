from PyQt5 import QtCore
#from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QColor
import copy
#from LabelList import LabelList
from Label import Label
from Label import LabelType
from Label import RoadType
from Label import RoadFlag

class Image(QtCore.QObject):
    
    _SCALING_BASE = 100
    _RND_NO = 2
    
    _mouseMoveEvent = QtCore.pyqtSignal(QtCore.QPoint)
    _labelChangedEvent = QtCore.pyqtSignal(list)
    _labelSelectedEvent = QtCore.pyqtSignal(Label)

    def __init__(self, widget, imagePath, enableLabel = False):
        super().__init__(widget)
        
        #print('Image__init__')
        
        self._widget = widget

        if enableLabel:
            self.widget.setMouseTracking(True)
            self.widget.installEventFilter(self)
        
        self.imagePath = imagePath
        self.pixmap = QPixmap(self.imagePath)
        self.scaledPixmap = self.pixmap.copy()
        self.cloneImage = self.scaledPixmap.copy()
        
        self.centerPos = self.centerPosition()
        
        self.scalingRatio = 1
        self.labels = []
        #self.labelList = LabelList()
        self.roadFlagByte = RoadFlag.Road | RoadFlag.Link | RoadFlag.Lane
        
        self.cctvConfig = None
        self.ScaleImage()

        #add label
        self.drawing = False
        self.lastPoint = None #QtCore.QPoint()
        
        #modify label
        self.moving = False
        self.selectedLabel = None
        self.selectedIndex = -1
        self.pivotPoint = None
        self.movingBasePoint = None
        
        #lock label
        self.locked = False
        self.lockedLabel = None
        self.lockedLabelIndex = -1
        
        
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
            elif event.type() == QtCore.QEvent.KeyPress:
                self.keyPressEvent(event)
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
            
            currentPosition = self.cursorPosition(event.pos())
            #self.lastPoint = event.pos()# + QPoint(-9, -9)
            
            if not self.locked:

                idx = -1
                self.selectedLabel = None
                for label in self.labels:
                    idx += 1
                    if label.selected:
                        self.selectedLabel = label
                        self.selectedIndex = idx
                        self.pivotPoint = self.selectedLabel.pivotPoint
                        
                        if not self.pivotPoint:
                            self.movingBasePoint = currentPosition
                        break
                
                if self.selectedLabel:
                    #print('press moving')
                    self.moving = True
                else:
                    #print('press drawing')
                    self.drawing = True
                    self.lastPoint = currentPosition
            else:
                self.drawing = True
                self.lastPoint = currentPosition
                    
    def mouseMoveEvent(self, event):
        #print('mouseMoveEvent')
        #print('drawing: ', self.drawing, ', moving: ', self.moving)
        
        currentPosition = self.cursorPosition(event.pos())
        #currentPosition = event.pos()# + QPoint(-9, -9)
                    
        if event.buttons() and Qt.LeftButton:
            if self.drawing:
                if self.lastPoint:
                    #print('mouse move drawing')
                    
                    tmpLabels = copy.deepcopy(self.labels)
                    
                    if self.locked:
                        popLabel = tmpLabels.pop(self.lockedLabelIndex)
                        tmpLabels.append(self.newLabel(self.lastPoint, currentPosition, popLabel.roadType, popLabel.roadIdx, popLabel.roadId))
                    else:
                        tmpLabels.append(self.newLabel(self.lastPoint, currentPosition))
                        
                    self.drawLine(tmpLabels)
            elif self.moving:
                if self.selectedLabel:
                    #print('mouse move moving')
                    tmpLabels = copy.deepcopy(self.labels)
                    popLabel = tmpLabels.pop(self.selectedIndex)
                    
                    label = None
                    if self.pivotPoint:
                        p1, p2 = popLabel.getPoints()
                        if self.pivotPoint == p1:
                            p1, p2 = self.pivotPoint, currentPosition
                        elif self.pivotPoint == p2:
                            p1, p2 = currentPosition, self.pivotPoint
                        label = self.newLabel(p1, p2, popLabel.roadType, popLabel.roadIdx, popLabel.roadId)
                        label.selectedEndpoint = currentPosition
                    elif self.movingBasePoint:
                        shiftX, shiftY = currentPosition.x() - self.movingBasePoint.x(), currentPosition.y() - self.movingBasePoint.y()
                        p1, p2 = popLabel.getPoints()
                        p1 = QPoint(p1.x() + shiftX, p1.y() + shiftY)
                        p2 = QPoint(p2.x() + shiftX, p2.y() + shiftY)
                        label = self.newLabel(p1, p2, popLabel.roadType, popLabel.roadIdx, popLabel.roadId)
                        
                    if label:
                        label.selected = True
                        tmpLabels.append(label)
                    self.drawLine(tmpLabels)
        else:
            
            if not self.locked:
            
                for label in self.labels:
                    label.selected = False
                    
                #print('just mouse move')
                for label in self.labels:
                    #label.isSelected(event.pos())
                    if label.isSelected(currentPosition):
                        self._labelSelectedEvent.emit(label)
                        break
                    
                self.drawLine(self.labels)

    def mouseReleaseEvent(self, event):
        #print('mouseReleaseEvent')
        if event.button() == Qt.LeftButton:
            
            currentPosition = self.cursorPosition(event.pos())
            #currentPosition = event.pos()# + QPoint(-9, -9)
                
            if self.drawing:
                #print('release drawing')
                
                if self.locked:
                    if Label.isDifferent(self.lastPoint, currentPosition):
                        popLabel = self.labels.pop(self.lockedLabelIndex)
                        label = self.newLabel(self.lastPoint, currentPosition, popLabel.roadType, popLabel.roadIdx, popLabel.roadId)
                        self.labels.append(label)
                        #self.labels.append(self.newLabel(self.lastPoint, currentPosition))
                    else:
                        return
                else:
                    pass
                
                    '''
                    if Label.isDifferent(self.lastPoint, currentPosition):
                        self.labels.append(self.newLabel(self.lastPoint, currentPosition))
                    '''
                    
            elif self.moving:
                #print('release moving')
                popLabel = self.labels.pop(self.selectedIndex)
                
                label = None
                if self.pivotPoint:
                    p1, p2 = popLabel.getPoints()
                    if self.pivotPoint == p1:
                        p1, p2 = self.pivotPoint, currentPosition
                    elif self.pivotPoint == p2:
                        p1, p2 = currentPosition, self.pivotPoint
                    label = self.newLabel(p1, p2, popLabel.roadType, popLabel.roadIdx, popLabel.roadId)
                elif self.movingBasePoint:
                    shiftX, shiftY = currentPosition.x() - self.movingBasePoint.x(), currentPosition.y() - self.movingBasePoint.y()
                    p1, p2 = popLabel.getPoints()
                    p1 = QPoint(p1.x() + shiftX, p1.y() + shiftY)
                    p2 = QPoint(p2.x() + shiftX, p2.y() + shiftY)
                    label = self.newLabel(p1, p2, popLabel.roadType, popLabel.roadIdx, popLabel.roadId)
                    
                if label:
                    self.labels.append(label)
                    
            self.drawLine(self.labels)
            self._labelChangedEvent.emit(self.labels)
                
                
                
        self.drawing = False
        self.lastPoint = None
        
        self.moving = False
        self.selectedLabel = None
        self.selectedIndex = -1
        self.pivotPoint = None
        self.movingBasePoint = None
        
        self.locked = False
        self.lockedLabel = None
        self.lockedLabelIndex = -1
        
        return 
    
    def keyPressEvent(self, event):
        #print('keyPressEvent ', event.key())
        
        idx = -1
        for label in self.labels:
            idx += 1
            if label.selected:
                self.labels.pop(idx)
            
        self.drawLine(self.labels)
        self._labelChangedEvent.emit(self.labels)
        
    def newLabel(self, p1, p2, roadType = RoadType.Road, roadIdx = None, roadId = '', labelType = LabelType.Line):
        return Label(p1, p2, roadType, roadIdx, roadId, labelType)
        
    #implement
    '''
    def SetImage(self, imagePath, labels):
        self.imagePath = imagePath
        self.pixmap = QPixmap(self.imagePath)
        self.scaledPixmap = self.pixmap.copy()
        self.cloneImage = self.scaledPixmap.copy()
    '''
    def findLabel(self, roadType, roadIdx):
        fidx = -1
        flbl = None
        for index, label in enumerate(self.labels):
            if label.roadType == roadType:
                if label.roadIdx == roadIdx:
                    fidx = index
                    flbl = label
                    break
                
        return fidx, flbl         
        
    def lockForNewLabel(self, roadType, roadIdx):
        self.locked = True
        self.lockedLabelIndex, self.lockedLabel = self.findLabel(roadType, roadIdx)
        return self.lockedLabel
    
    def updateLabel(self, roadType, roadIdx, roadId, p1, p2):
        updateLabelIndex, updateLabel = self.findLabel(roadType, roadIdx)
        if updateLabelIndex > -1:
            self.labels[updateLabelIndex].roadId = roadId
            self.labels[updateLabelIndex].setPoints(p1, p2)
            self.drawLine(self.labels)
        
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
    
    def centerPosition(self):
        origSize = self.size()
        p = QPoint(int(origSize.width() / 2), int(origSize.height() / 2))
        return p
        
    def size(self):
        return self.pixmap.size()
    
    def scaledSize(self):
        self.lblImage.pixmap().size()
        
    def drawLine(self, labels):
        #print('drawLine')
        
        self.cloneImage = self.scaledPixmap.copy()
        painter = QPainter(self.cloneImage)
        #painter.setRenderHint(QPainter.Antialiasing)
                              
        brush = painter.brush()
        
        pen = painter.pen()
        pen.setWidth(2)
        pen.setStyle(Qt.SolidLine)
        pen.setJoinStyle(Qt.MiterJoin)
        brush.setStyle(Qt.SolidPattern)
        
        '''
        redPen = QPen(Qt.red, 2, Qt.SolidLine)
        greenPen = QPen(Qt.green, 2, Qt.SolidLine)
        
        redBrush = QBrush(Qt.red, Qt.SolidPattern)
        greenBrush = QBrush(Qt.green, Qt.SolidPattern)
        '''
        
        for label in labels:

            
            if label.selected:
                #painter.setPen(redPen)
                #painter.setBrush(redBrush)
                pen.setColor(Qt.red)
                brush.setColor(Qt.red)
            else:
                #painter.setPen(greenPen)
                #painter.setBrush(greenBrush)                
                pen.setColor(label.getPainterColor())
                brush.setColor(label.getPainterColor())
                
            painter.setPen(pen)
            painter.setBrush(brush)
            
            painter.drawPath(label.getPainterPath(self.scalingRatio, self.roadFlagByte))
            
            '''
            lastPos, currentPos = label.shape.p1, label.shape.p2
            p1 = lastPos * self.scalingRatio
            p2 = currentPos * self.scalingRatio
            
            painter.drawLine(p1, p2)
            painter.drawEllipse(p1, 3, 3)
            painter.drawEllipse(p2, 3, 3)
            '''
            
            #print('drawLine', lastPos, currentPos)
            
        painter.end()
        
        #self.widget.update()
        
        self.widget.setPixmap(self.cloneImage)
        
        #print('drawLine', self.imagePath)

