from PyQt5.QtGui import QPainterPath, QColor, QFont, QFontMetrics

from enum import Enum
from enum import IntEnum
from enum import IntFlag
from Line import Line

class LabelType(Enum):
    Line = 0
    #Rectangle = 1
    
class RoadType(Enum):
    Road = 0
    Lane = 1

class RoadFlag(IntFlag):
    NoFlag = 0
    Road = 1
    Link = 2
    Lane = 4
    
class Label():
    
    def __init__(self, p1, p2, roadType = RoadType.Road, roadIdx = None, roadId = '', labelType = LabelType.Line):
        
        self.labelType = labelType
        
        self.roadType = roadType
        self.roadIdx = roadIdx
        self.roadId = roadId
        
        self.shape = Line(p1, p2)
        
        self.selected = False
        self.selectedEndpoint = None
        self.pivotPoint = None
        
    def isSelected(self, pos):
        self.selected = self.shape.isSelected(pos)
        if self.selected:
            self.selectedEndpoint, self.pivotPoint = self.shape.getSelectedEndpoint(pos)
        else:
            self.selectedEndpoint = None
            self.pivotPoint = None
        return self.selected
    
    def getPoints(self):
        return self.shape.p1, self.shape.p2
    
    def toString(self):
        p1, p2 = self.getPoints()
        return 'p1: ({0}, {1}), p2: ({2}, {3})'.format(p1.x(), p1.y(), p2.x(), p2.y())
    
    @staticmethod
    def isDifferent(p1, p2):
        return (pow(pow(p1.x() - p2.x(), 2) + pow(p1.y() - p2.y(), 2), 0.5) > 0)
        
    def getPainterColor(self):
        if self.roadType == RoadType.Road:
            #color = QColor(0, 204, 255)
            #color = QColor(0, 112, 192)
            #color = QColor(47, 85, 151)
            #color = QColor(0, 176, 80)
            #color = QColor(112, 48, 160)
            color = QColor(0, 0, 255)
        else:
            #color = QColor(255, 0, 255)
            color = QColor(237, 125, 49)
        return color
        
    def getPainterPath(self, scalingRatio, roadFlagByte):
        diameter = 10
        radius = diameter / 2
        p1_o, p2_o = self.getPoints()
        p1_s = p1_o * scalingRatio
        p2_s = p2_o * scalingRatio
        painterPath = QPainterPath()
        painterPath.moveTo(p1_s)
        painterPath.lineTo(p2_s)
        
        p1Fp = painterPath.addEllipse
        p2Fp = painterPath.addEllipse
        
        if self.selectedEndpoint:
            if self.selectedEndpoint == self.shape.p1:
                p1Fp = painterPath.addRect
            elif self.selectedEndpoint == self.shape.p2:
                p2Fp = painterPath.addRect
  
        p1Fp(p1_s.x() - radius, p1_s.y() - radius, diameter, diameter)
        p2Fp(p2_s.x() - radius, p2_s.y() - radius, diameter, diameter)
        
        
        
        txtList = []
        
        if self.roadType == RoadType.Road:
            if len(self.roadId) == 2:
                (roadId, linkId) = self.roadId
                if roadFlagByte & RoadFlag.Road:
                    txtList.append(roadId)
                if roadFlagByte & RoadFlag.Link:
                    txtList.append(linkId)                
        elif self.roadType == RoadType.Lane:
            if roadFlagByte & RoadFlag.Lane:
                txtList.append(self.roadId)

        
        
        #if roadHintByte & int(self.roadType):
        if len(txtList) > 0:
            
            t = '_'.join(txtList)
            f = QFont("SansSerif", 12, QFont.Normal)
            
            metrics = QFontMetrics(f)
            fontwidth, fontheight = metrics.width(t) / 2, metrics.height() / 2            
            
            x, y = self.shape.getCentralXY()
            x = (x - fontwidth) * scalingRatio
            y = (y - fontheight) * scalingRatio

            painterPath.addText(x, y, f, t)
        
        return painterPath
        
    
if __name__ == '__main__':
    
    from PyQt5.QtCore import QPoint
    #ans
    #[[ 1.66666667]
    # [-0.33333333]]
    
    p1 = QPoint(2, 3)
    p2 = QPoint(5, 8)
    label = Label(p1, p2)

    
    for y in range(12):
        cp = QPoint(5, y)
        print(label.isSelected(cp))
        
    painterPath = label.getPainterPath()
    