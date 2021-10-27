from PyQt5.QtGui import QPainterPath, QColor, QFont, QFontMetrics

from enum import Enum
from enum import IntEnum
from Line import Line

class LabelType(Enum):
    Line = 0
    #Rectangle = 1
    
class RoadType(IntEnum):
    Road = 2 ** 0
    Lane = 2 ** 1
    
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
            color = QColor(0, 204, 255)
        else:
            color = QColor(255, 0, 255)
        return color
        
    def getPainterPath(self, scalingRatio, roadHintByte):
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
        
        
        
        if roadHintByte & int(self.roadType):
            
            t = self.roadId
            f = QFont("SansSerif", 14, QFont.Normal)
            
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
    