import numpy as np
from enum import Enum
from Shape import Shape

class LineType(Enum):
    Horizontal = 0
    Vertical = 1
    Slash = 3
    
class Line(Shape):
    
    def __init__(self, p1, p2):
        super().__init__(p1, p2)
        
        self.lineType = self.getLineType(self.p1, self.p2)
        self.ab = self.getAB(self.p1, self.p2)

    def setPoints(self, p1, p2):
        self.p1, self.p2 = p1, p2

        self.lineType = self.getLineType(self.p1, self.p2)
        self.ab = self.getAB(self.p1, self.p2)
        
    def isSelected(self, pos):
        result = False
        
        if self.lineType == LineType.Slash:
            if super().isSelected(pos):
                a = self.ab[0, 0]
                b = self.ab[1, 0]
                result = (abs(a * pos.x() + b - pos.y()) < self._Tolerance)
        elif self.lineType == LineType.Horizontal:
            if self.inRange(self.p1.x(), self.p2.x(), pos.x()):
                result = (abs(pos.y() - self.p1.y()) < self._Tolerance)  
        elif self.lineType == LineType.Vertical:
            if self.inRange(self.p1.y(), self.p2.y(), pos.y()):
                result = (abs(pos.x() - self.p1.x()) < self._Tolerance)

        return result
    
    def getLineType(self, p1, p2):
        lineType = LineType.Slash
        
        if abs(p1.y() - p2.y()) < self._Tolerance:
            lineType = LineType.Horizontal
        elif abs(p1.x() - p2.x()) < self._Tolerance:
            lineType = LineType.Vertical
            
        '''
        if p1.y() == p2.y():
            lineType = LineType.Horizontal
        elif p1.x() == p2.x():
            lineType = LineType.Vertical
        '''
        return lineType
    
    def getAB(self, p1, p2):
        ab = [[0]
              [0]]
        if self.lineType == LineType.Slash:
            x = np.array([[p1.x(), 1],
                          [p2.x(), 1]])
            
            y = np.array([[p1.y()],
                          [p2.y()]])
            
            ab = np.linalg.pinv(x) @ y
        return ab
    
    def getCentralXY(self):
        
        maxX = max(self.p1.x(), self.p2.x())
        minX = min(self.p1.x(), self.p2.x())
        maxY = max(self.p1.y(), self.p2.y())
        minY = min(self.p1.y(), self.p2.y())
        
        x = int(minX + ((maxX - minX) / 2))
        y = int(minY + ((maxY - minY) / 2))
        return x, y

if __name__ == '__main__':
    
    from PyQt5.QtCore import QPoint
    #ans
    #[[ 1.66666667]
    # [-0.33333333]]
    
    p1 = QPoint(2, 3)
    p2 = QPoint(5, 8)
    line = Line(p1, p2)
    print(line.ab)
    
    for y in range(12):
        cp = QPoint(5, y)
        print(line.isSelected(cp))
    
  