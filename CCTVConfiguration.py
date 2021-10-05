import xml.etree.ElementTree as ElementTree
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import QPoint

class GeographicCoordinate():
    def __init__(self, latitude = '', longitude = ''):
        self.latitude = latitude
        self.longitude = longitude

class ReferencePoint():
    def __init__(self, reference_point):       
        self.img_position = QPoint(int(reference_point.find('img_x').text), int(reference_point.find('img_y').text))
        self.geograph_position = GeographicCoordinate(reference_point.find('lat').text, reference_point.find('lng').text)
        
        
class Header():
    
    def __init__(self, header):
        self.extract(header)
  
    def extract(self, header):
        
        if header:
            self.cctv = header.find('cctv').text
            self.version = header.find('version').text
            self.date = header.find('date').text
            self.intersection_id = header.find('intersection_id').text
            self.device_ip = header.find('device_ip').text
            self.camera_position = GeographicCoordinate(header.find('camera_position/lat').text, header.find('camera_position/lng').text)
            
    def showInTree(self, root):

        QTreeWidgetItem(root, ['cctv', self.cctv])
        QTreeWidgetItem(root, ['version', self.version])
        QTreeWidgetItem(root, ['date', self.version])
        QTreeWidgetItem(root, ['intersection_id', self.version])
        QTreeWidgetItem(root, ['device_ip', self.version])
        
        pos = QTreeWidgetItem(root, ['camera_position'])
        QTreeWidgetItem(pos, ['lat', self.camera_position.latitude])
        QTreeWidgetItem(pos, ['lng', self.camera_position.longitude])
        
        
        '''
        item1.setText(0, 'cctv')
        item1.setText(1, self.cctv)
        
        root.addChild(item)
        
        item2 = QTreeWidgetItem(root)
        item2.setText(0, 'version')
        item2.setText(1, self.version)
        
        root.addChild(item)
        
        tree.addTopLevelItems(root)
        '''
class RoadInfo():
    
    def __init__(self, roadInfo):
        self.extract(roadInfo)
  
    def extract(self, roadInfo):

        if roadInfo:
            self.reference_points = []
            for reference_point in roadInfo.findall('Reference_points/point'):
                self.reference_points.append(ReferencePoint(reference_point))
                
    def showInTree(self, root):
        
        road_Info = QTreeWidgetItem(root, ['RoadInformation'])
        ref_point = QTreeWidgetItem(road_Info, ['Reference_points'])
        
        for reference_point in self.reference_points:
            point = QTreeWidgetItem(ref_point, ['point'])
            QTreeWidgetItem(point, ['img_x', str(reference_point.img_position.x())])
            QTreeWidgetItem(point, ['img_y', str(reference_point.img_position.y())])
            QTreeWidgetItem(point, ['lat', reference_point.geograph_position.latitude])
            QTreeWidgetItem(point, ['lng', reference_point.geograph_position.longitude])
            
            
        
class VirtualGate():

    def __init__(self, virtualGate):
        self.extract(virtualGate)
  
    def extract(self, virtualGate):

        if virtualGate:
            self.roads = []
            for road in virtualGate.findall('Road'):
                self.roads.append(Road(road))
                
    def showInTree(self, root):
        
        virtual_gate = QTreeWidgetItem(root, ['Virtual_gate'])
        
        for road in self.roads:
            itemRoad = QTreeWidgetItem(virtual_gate, ['Road'])
            
            QTreeWidgetItem(itemRoad, ['road_id', road.road_id])
            QTreeWidgetItem(itemRoad, ['link_id', road.link_id])
            QTreeWidgetItem(itemRoad, ['name', road.name])
            QTreeWidgetItem(itemRoad, ['direction', road.direction])
            QTreeWidgetItem(itemRoad, ['section', road.section])
            
            itemPosition = QTreeWidgetItem(itemRoad, ['position'])
            QTreeWidgetItem(itemPosition, ['x1', str(road.position1.x())])
            QTreeWidgetItem(itemPosition, ['y1', str(road.position1.y())])
            QTreeWidgetItem(itemPosition, ['x2', str(road.position2.x())])
            QTreeWidgetItem(itemPosition, ['y2', str(road.position2.y())])
            
            itemLanes = QTreeWidgetItem(itemRoad, ['lanes'])
            
            for lane in road.lanes:
                itemLane = QTreeWidgetItem(itemLanes, ['lane'])
                QTreeWidgetItem(itemLane, ['lane_id', lane.lane_id])
                
                itemPosition = QTreeWidgetItem(itemLane, ['position'])
                QTreeWidgetItem(itemPosition, ['x1', str(lane.position1.x())])
                QTreeWidgetItem(itemPosition, ['y1', str(lane.position1.y())])
                QTreeWidgetItem(itemPosition, ['x2', str(lane.position2.x())])
                QTreeWidgetItem(itemPosition, ['y2', str(lane.position2.y())])
        
class Road():
    
    def __init__(self, road):
        self.extract(road)
  
    def extract(self, road):
        self.road_id = road.find('road_id').text
        self.link_id = road.find('link_id').text
        self.name = road.find('name').text
        self.direction = road.find('direction').text
        self.section = road.find('section').text
        self.position1 = QPoint(int(road.find('position/x1').text), int(road.find('position/y1').text))
        self.position2 = QPoint(int(road.find('position/x2').text), int(road.find('position/y2').text))
        
        self.lanes = []
        for lane in road.findall('lanes/lane'):
            self.lanes.append(Lane(lane))
        
class Lane():
    
    def __init__(self, lane):
        self.extract(lane)
  
    def extract(self, lane):
        self.lane_id = lane.find('lane_id').text
        self.position1 = QPoint(int(lane.find('position/x1').text), int(lane.find('position/y1').text))
        self.position2 = QPoint(int(lane.find('position/x2').text), int(lane.find('position/y2').text))

class CCTVConfiguration():
    
    
    def __init__(self, xmlPath = ''):
        if xmlPath != '':
            self.loadXml(xmlPath)
    
    def loadXml(self, xmlPath):
        self.tree = ElementTree.parse(xmlPath)
        self.root = self.tree.getroot()
        
    def getHeader(self):
        header = Header(self.root.find('header'))
        return header
        
    def getRoadInfo(self):
        roadInfo = RoadInfo(self.root.find('RoadInformation'))
        return roadInfo
        
    def getVirtualGate(self):
        virtualGate = VirtualGate(self.root.find('Virtual_gate'))
        return virtualGate
    
    def showInTree(self, tree):
        
        tree.setColumnCount(2)
        tree.setHeaderLabels(['Property', 'Value'])

        root = QTreeWidgetItem(tree)
        root.setText(0, 'cctv config')
        
        header = self.getHeader()
        header.showInTree(root)
        
        roadInfo = self.getRoadInfo()
        roadInfo.showInTree(root)
        
        virtualGate = self.getVirtualGate()
        virtualGate.showInTree(root)
        
        '''
        tree.header().setResizeMode(QtGui.QHeaderView.ResizeToContents)
        tree.header().setStretchLastSection(False)
        
        header = tree.header()
        header.setSectionResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        header.setStretchLastSection(False)
        header.setSectionResizeMode(5, QtWidgets.QHeaderView.Stretch)
        '''
        
if __name__ == "__main__":
    
    xmlPath = 'D:/_Course/Project/LabelTool/data/cctv_configuration.xml'
    config = CCTVConfiguration(xmlPath)
    
    print(config.getHeader())
    print(config.getRoadInfo())
    print(config.getVirtualGate())
    