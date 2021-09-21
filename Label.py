from PyQt5.QtGui import QPainterPath

from enum import Enum
from Line import Line

class LabelType(Enum):
    Line = 0
    #Rectangle = 1

class Label():

    def __init__(self, p1, p2, labelType = LabelType.Line):
        
        self.labelType = labelType
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
        
    def getPainterPath(self, scalingRatio):
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
    