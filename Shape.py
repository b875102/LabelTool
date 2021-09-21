

class Shape():
    
    _Tolerance = 4
        
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
    
    def distance(self, p1, p2):
        return pow(pow(p1.x() - p2.x(), 2) + pow(p1.y() - p2.y(), 2), 0.5)
        
        
    def isSelected(self, pos):
        return self.inRange(self.p1.x(), self.p2.x(), pos.x()) and self.inRange(self.p1.y(), self.p2.y(), pos.y())

    def getSelectedEndpoint(self, pos):
        selectedEndpoint = None
        pivotPoint = None
        if self.distance(self.p1, pos) < self._Tolerance:
            selectedEndpoint = self.p1
            pivotPoint = self.p2
        elif self.distance(self.p2, pos) < self._Tolerance:
            selectedEndpoint = self.p2
            pivotPoint = self.p1
        return selectedEndpoint, pivotPoint