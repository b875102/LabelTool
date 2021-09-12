

class Shape():
    
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        
    def inRange(self, v1, v2, t):
        result = False
        if v1 < v2:
            result = (v1 <= t and t <= v2)
        else:
            result = (v1 >= t and t >= v2)
        return result
        
    def isSelected(self, pos):
        return self.inRange(self.p1.x(), self.p2.x(), pos.x()) and self.inRange(self.p1.y(), self.p2.y(), pos.y())

