#import os
import xml.etree.ElementTree as ElementTree
#from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QTreeWidgetItem
#from PyQt5.QtCore import QPoint

from VirtualGateTool.conf.CCTVConfiguration import CCTVConfiguration
from VirtualGateTool.conf.CCTVConfiguration import Header as CCTVHeader
from VirtualGateTool.conf.CCTVConfiguration import RoadInfo as CCTVRoadInfo
from VirtualGateTool.conf.CCTVConfiguration import VirtualGate as CCTVVirtualGate
from VirtualGateTool.conf.CCTVConfiguration import Road as CCTVRoad
from VirtualGateTool.conf.CCTVConfiguration import Lane as CCTVLane
from VirtualGateTool.conf.CCTVConfiguration import ReferencePoint as CCTVReferencePoint

class Header():
    
    def __init__(self, header):
        self.extract(header)
  
    def extract(self, header):
        
        if header:
            self.name = header.find('name').text
            self.version = header.find('version').text
            self.date = header.find('date').text
            self.intersection_id = header.find('intersection_id').text
            
    def showInTree(self, root):

        QTreeWidgetItem(root, ['name', self.name])
        QTreeWidgetItem(root, ['version', self.version])
        QTreeWidgetItem(root, ['date', self.date])
        QTreeWidgetItem(root, ['intersection_id', self.intersection_id])

class RoadInfo():
    
    def __init__(self, roadInfo):
        self.extract(roadInfo)
  
    def extract(self, roadInfo):

        if roadInfo:
            
            self.road_type = roadInfo.find('road_type').text
            self.road_num = roadInfo.find('road_num').text
            
            self.roads = []
            for road in roadInfo.findall('roads/road'):
                self.roads.append(Road(road))
                
    def showInTree(self, root):
        
        road_Info = QTreeWidgetItem(root, ['road_information'])
        QTreeWidgetItem(road_Info, ['road_type', self.road_type])
        QTreeWidgetItem(road_Info, ['road_num', self.road_num])
        
        roads_node = QTreeWidgetItem(road_Info, ['roads'])
        
        for road in self.roads:
            road.showInTree(roads_node)
            
class Road():
    
    def __init__(self, road):
        self.extract(road)
  
    def extract(self, road):

        if road:
            self.link_id = road.find('link_id').text
            self.lane_num = road.find('lane_num').text
            self.name = road.find('name').text
            self.section = road.find('section').text
            self.direction = road.find('direction').text

                
    def showInTree(self, root):
        
        road_node = QTreeWidgetItem(root, ['road'])

        QTreeWidgetItem(road_node, ['link_id', self.link_id])
        QTreeWidgetItem(road_node, ['lane_num', self.lane_num])
        QTreeWidgetItem(road_node, ['name', self.name])
        QTreeWidgetItem(road_node, ['section', self.section])
        QTreeWidgetItem(road_node, ['direction', self.direction])    
            
class IntersectionConfiguration():
    
    def __init__(self, xmlPath = ''):

        self.xmlPath = xmlPath
        
        self.root = None
        self.header = None
        self.roadInfo = None
        
        if self.xmlPath != '':
            self.loadXml(self.xmlPath)
    
    def loadXml(self, xmlPath):
        self.tree = ElementTree.parse(xmlPath)
        self.root = self.tree.getroot()
        self.header = self.getHeader()
        self.roadInfo = self.getRoadInfo()
        
    def getHeader(self):
        header = Header(self.root.find('header'))
        return header
        
    def getRoadInfo(self):
        roadInfo = RoadInfo(self.root.find('road_information'))
        return roadInfo
    
    def showInTree(self, tree):
        
        tree.setColumnCount(2)
        tree.setHeaderLabels(['Property', 'Value'])

        root = QTreeWidgetItem(tree)
        root.setText(0, 'intersection config')
        
        header = self.getHeader()
        header.showInTree(root)
        
        roadInfo = self.getRoadInfo()
        roadInfo.showInTree(root)
        
        tree.expandAll()
        tree.resizeColumnToContents(0)
        tree.resizeColumnToContents(1)
        
    def toCCTVConfiguration(self):
        
        cctvHeader = CCTVHeader(None)
        cctvRoadInfo = CCTVRoadInfo(None)
        cctvVirtualGate = CCTVVirtualGate(None)
        
        intersectionHeader = self.header
        
        cctvHeader.name = intersectionHeader.name
        cctvHeader.version = intersectionHeader.version
        cctvHeader.date = intersectionHeader.date
        cctvHeader.intersection_id = intersectionHeader.intersection_id
        
        intersectionRoad = self.roadInfo
        
        for idxRoad, isRoad in enumerate(intersectionRoad.roads):
            
            cctvRoad = CCTVRoad(None)
            
            cctvRoad.road_id = str(idxRoad)
            cctvRoad.link_id = isRoad.link_id
            cctvRoad.direction = isRoad.direction
        
            for idxLane in range(int(isRoad.lane_num)):
                
                lane = CCTVLane(None)
                lane.lane_id = str(idxLane)
                lane.forward_direction = ''
                cctvRoad.lanes.append(lane)
            
            cctvVirtualGate.roads.append(cctvRoad)
        
        
        cctvConfig = CCTVConfiguration()
        cctvConfig.header = cctvHeader
        cctvConfig.roadInfo = cctvRoadInfo
        cctvConfig.virtualGate = cctvVirtualGate
        
        return cctvConfig
        
if __name__ == "__main__":
    
    xmlPath = 'D:/_Course/Project/LabelTool/data/Intersection_configuration.xml'
    config = IntersectionConfiguration(xmlPath)
    
    print(config.getHeader())
    print(config.getRoadInfo())
    
    cctvConfig = config.toCCTVConfiguration()
    cctvConfig.save()
