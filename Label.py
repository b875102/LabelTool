from PyQt5.QtGui import QPainterPath, QColor, QFont, QFontMetrics, QPolygonF
from PyQt5.QtCore import QLineF, QPointF

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
        
        self.__shape = Line(p1, p2)
        
        self.selected = False
        self.selectedEndpoint = None
        self.pivotPoint = None
        
    def setPoints(self, p1, p2):
        self.__shape.setPoints(p1, p2)
        
    def getPoints(self):
        return self.__shape.getPoints()
        
    def isSelected(self, pos):
        self.selected = self.__shape.isSelected(pos)
        if self.selected:
            self.selectedEndpoint, self.pivotPoint = self.__shape.getSelectedEndpoint(pos)
        else:
            self.selectedEndpoint = None
            self.pivotPoint = None
        return self.selected
    
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
        
    def getArrow(self, p1, p2):
        
        line = QLineF(p1, p2)
        line.setLength(line.length() - 10)
        
        v = line.unitVector()
        v.setLength(10)
        v.translate(QPointF(line.dx(), line.dy()))

        n = v.normalVector()
        n.setLength(n.length() * 0.4)
        n2 = n.normalVector().normalVector()

        p1 = v.p2()
        p2 = n.p2()
        p3 = n2.p2()

        arrow = QPolygonF([p1, p2, p3, p1])        
        return arrow
        
    def getPainterPath(self, scalingRatio, roadFlagByte):
        diameter = 6
        radius = diameter / 2
        p1_o, p2_o = self.__shape.getPoints()
        p1_s = p1_o * scalingRatio
        p2_s = p2_o * scalingRatio
        painterPath = QPainterPath()
        painterPath.moveTo(p1_s)
        painterPath.lineTo(p2_s)
        
        p1selected = False
        p2selected = False
        
        if self.selectedEndpoint:
            if self.selectedEndpoint == p1_o:
                p1selected = True
            elif self.selectedEndpoint == p2_o:
                p2selected = True

        if p1selected:
            p1Fp = painterPath.addRect
        else:
            p1Fp = painterPath.addEllipse
        
        p1Fp(p1_s.x() - radius, p1_s.y() - radius, diameter, diameter)
        
        if p2selected:
            p2Fp = painterPath.addRect
            p2Fp(p2_s.x() - radius, p2_s.y() - radius, diameter, diameter)
        else:
            painterPath.addPolygon(self.getArrow(p1_s, p2_s))
            
        
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
            
            x, y = self.__shape.getCentralXY()
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
    