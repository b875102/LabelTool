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
        
    def isSelected(self, pos):
        self.selected = self.shape.isSelected(pos)
        return self.selected
    
    def toString(self):
        p1 = self.shape.p1
        p2 = self.shape.p2
        return 'p1: ({0}, {1}), p2: ({2}, {3})'.format(p1.x(), p1.y(), p2.x(), p2.y())
    
    @staticmethod
    def isDifferent(p1, p2):
        return (pow(pow(p1.x() - p2.x(), 2) + pow(p1.y() - p2.y(), 2), 0.5) > 0)
        
        
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