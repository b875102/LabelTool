from collections import UserList
from Label import Label

from PyQt5.QtGui import QPixmap, QPainter, QPen, QBrush, QPainterPath

class LabelList(UserList):
    def __init__(self, initlist = None):
        super(LabelList, self).__init__(initlist)
        
    def add(self, p1, p2):
        if Label.isDifferent(p1, p2):
            label = Label(p1, p2)
            self.append(label)
        
    def size(self):
        return len(self.data)

    def scoop(self, pos):
        for label in self.data:
            label.isSelected(pos)
        return

    def toString(self):
        lst = []
        for label in self.data:
            lst.append(label.toString())
        return lst
        
    def getPainterPath(self):
        pass
        
if __name__ == "__main__":
    
    from PyQt5.QtCore import QPoint
    import numpy as np
    
    ll = LabelList()
    
    rarr = np.random.rand(8, 4)
    
    for r in rarr:
        n1 = int (r[0] * 100)
        n2 = int (r[1] * 100)
        n3 = int (r[2] * 100)
        n4 = int (r[3] * 100)
        
        p1 = QPoint(n1, n2)
        p2 = QPoint(n3, n4)
  
        ll.add(p1, p2)
    
    print(ll.size())
    #print(ll.data)
    
    ll2 = ll.copy()
    ll.Add(QPoint(34, 5), QPoint(38, 5))

    
    print(ll.toString())
    print(ll2.toString())
    
    