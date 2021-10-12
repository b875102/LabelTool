import xml.etree.ElementTree as ElementTree
#from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QTreeWidgetItem

def safeNodeText(node):
    txt = ''
    try:
        txt = node.text
    except:
        pass
    return txt
    
class PointPosition():
    def __init__(self, x = '', y = ''):
        self.x = x
        self.y = y
    
class GeographicCoordinate():
    def __init__(self, latitude = '', longitude = ''):
        self.latitude = latitude
        self.longitude = longitude

class ReferencePoint():
    def __init__(self, reference_point):
        
        self.img_position = PointPosition()
        self.geograph_position = GeographicCoordinate()
        
        if reference_point:
            self.img_position.x = safeNodeText(reference_point.find('img_x'))
            self.img_position.y = safeNodeText(reference_point.find('img_y'))
            self.geograph_position.latitude = safeNodeText(reference_point.find('lat'))
            self.geograph_position.longitude = safeNodeText(reference_point.find('lng'))
        
    def getValues(self):
        return [self.img_position.x, self.img_position.y, self.geograph_position.latitude, self.geograph_position.longitude]
        
class Header():
    
    def __init__(self, header):
        
        self.cctv = ''
        self.name = ''
        self.version = ''
        self.date = ''
        self.intersection_id = ''
        self.device_ip = ''
        self.camera_position = GeographicCoordinate()
        
        self.extract(header)

    def extract(self, header):
        
        if header:
            self.cctv = safeNodeText(header.find('cctv'))
            self.name = safeNodeText(header.find('name'))
            self.version = safeNodeText(header.find('version'))
            self.date = safeNodeText(header.find('date'))
            self.intersection_id = safeNodeText(header.find('intersection_id'))
            self.device_ip = safeNodeText(header.find('device_ip'))
            self.camera_position.latitude = safeNodeText(header.find('camera_position/lat'))
            self.camera_position.longitude = safeNodeText(header.find('camera_position/lng'))
            
    def showInTree(self, root):

        QTreeWidgetItem(root, ['cctv', self.cctv])
        QTreeWidgetItem(root, ['version', self.version])
        QTreeWidgetItem(root, ['date', self.date])
        QTreeWidgetItem(root, ['intersection_id', self.intersection_id])
        QTreeWidgetItem(root, ['device_ip', self.device_ip])
        
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
        
    def toXmlString(self):
        
        xmlStr = '<header>' + \
                    '<cctv>' + self.cctv + '</cctv>' + \
                    '<name>' + self.name + '</name>' + \
                    '<version>' + self.version + '</version>' + \
                    '<date>' + self.date + '</date>' + \
                    '<intersection_id>' + self.intersection_id + '</intersection_id>' + \
                    '<device_ip>' + self.device_ip + '</device_ip>' + \
                    '<camera_position>' + \
                        '<lat>' + self.camera_position.latitude + '</lat>' + \
                        '<lng>' + self.camera_position.longitude + '</lng>' + \
                    '</camera_position>' + \
                 '</header>'
        return xmlStr       
        
class RoadInfo():
    
    def __init__(self, roadInfo):
        
        self.reference_points = []
        self.extract(roadInfo)
  
    def extract(self, roadInfo):

        if roadInfo:
            for reference_point in roadInfo.findall('Reference_points/point'):
                self.reference_points.append(ReferencePoint(reference_point))
                
    def showInTree(self, root):
        
        road_Info = QTreeWidgetItem(root, ['RoadInformation'])
        ref_point = QTreeWidgetItem(road_Info, ['Reference_points'])
        
        for reference_point in self.reference_points:
            point = QTreeWidgetItem(ref_point, ['point'])
            QTreeWidgetItem(point, ['img_x', reference_point.img_position.x])
            QTreeWidgetItem(point, ['img_y', reference_point.img_position.y])
            QTreeWidgetItem(point, ['lat', reference_point.geograph_position.latitude])
            QTreeWidgetItem(point, ['lng', reference_point.geograph_position.longitude])
            
    def toXmlString(self):
        
        xmlStr = ''
        
        if len(self.reference_points) > 0:
            
            xmlStr = '<RoadInformation>' + \
                        '<Reference_points>'
                        
            for ref_point in self.reference_points:
                
                xmlStr += '<point>' + \
                                '<img_x>' + ref_point.img_position.x + '</img_x>' + \
                                '<img_y>' + ref_point.img_position.y + '</img_y>' + \
                                '<lat>' + ref_point.geograph_position.latitude + '</lat>' + \
                                '<lng>' + ref_point.geograph_position.longitude + '</lng>' + \
                            '</point>'
                        
            xmlStr += '</Reference_points>' + \
                    '</RoadInformation>'

        return xmlStr   
        
class VirtualGate():

    def __init__(self, virtualGate):
        self.roads = []
        self.extract(virtualGate)
  
    def extract(self, virtualGate):

        if virtualGate:
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
            QTreeWidgetItem(itemPosition, ['x1', road.position1.x])
            QTreeWidgetItem(itemPosition, ['y1', road.position1.y])
            QTreeWidgetItem(itemPosition, ['x2', road.position2.x])
            QTreeWidgetItem(itemPosition, ['y2', road.position2.y])
            
            itemLanes = QTreeWidgetItem(itemRoad, ['lanes'])
            
            for lane in road.lanes:
                itemLane = QTreeWidgetItem(itemLanes, ['lane'])
                QTreeWidgetItem(itemLane, ['lane_id', lane.lane_id])
                
                itemPosition = QTreeWidgetItem(itemLane, ['position'])
                QTreeWidgetItem(itemPosition, ['x1', lane.position1.x])
                QTreeWidgetItem(itemPosition, ['y1', lane.position1.y])
                QTreeWidgetItem(itemPosition, ['x2', lane.position2.x])
                QTreeWidgetItem(itemPosition, ['y2', lane.position2.y])
                
    def toXmlString(self):
        
        xmlStr = '<Virtual_gate>'
        
        for road in self.roads:
            
            xmlStr += '<Road>' + \
                        '<road_id>' + road.road_id + '</road_id>' + \
                        '<link_id>' + road.link_id + '</link_id>' + \
                        '<name>' + road.name + '</name>' + \
                        '<direction>' + road.direction + '</direction>' + \
                        '<section>' + road.section + '</section>' + \
                        '<position>' + \
                            '<x1>' + road.position1.x + '</x1>' + \
                            '<y1>' + road.position1.y + '</y1>' + \
                            '<x2>' + road.position2.x + '</x2>' + \
                            '<y2>' + road.position2.y + '</y2>' + \
                        '</position>'
            
            if len(road.lanes) > 0:
                xmlStr += '<lanes>'
                
                for lane in road.lanes:
                    
                    xmlStr += '<lane>' + \
                                '<lane_id>' + lane.lane_id + '</lane_id>' + \
                                '<position>' + \
                                    '<x1>' + lane.position1.x + '</x1>' + \
                                    '<y1>' + lane.position1.y + '</y1>' + \
                                    '<x2>' + lane.position2.x + '</x2>' + \
                                    '<y2>' + lane.position2.y + '</y2>' + \
                                '</position>' + \
                                '</lane>'
                    
                    
                xmlStr += '</lanes>'
                    
            xmlStr += '</Road>'
        
        xmlStr += '</Virtual_gate>'
        
        return xmlStr
        
class Road():
    
    def __init__(self, road):
        
        self.road_id = ''
        self.link_id = ''
        self.name = ''
        self.direction = ''
        self.section = ''
        self.position1 = PointPosition()
        self.position2 = PointPosition()
        
        self.lanes = []
        self.extract(road)
  
    def extract(self, road):
        
        if road:
            self.road_id = road.find('road_id').text
            self.link_id = road.find('link_id').text
            self.name = road.find('name').text
            self.direction = road.find('direction').text
            self.section = road.find('section').text
            
            self.position1.x = safeNodeText(road.find('position/x1'))
            self.position1.y = safeNodeText(road.find('position/y1'))
            self.position2.x = safeNodeText(road.find('position/x2'))
            self.position2.y = safeNodeText(road.find('position/y2'))
            
            for lane in road.findall('lanes/lane'):
                self.lanes.append(Lane(lane))
                
    def getValues(self):
        return [self.road_id, self.link_id, self.name, self.direction, self.section, self.position1.x, self.position1.y, self.position2.x, self.position2.y]
        
class Lane():
    
    def __init__(self, lane):
        self.lane_id = ''
        self.position1 = PointPosition()
        self.position2 = PointPosition()
        
        self.extract(lane)
  
    def extract(self, lane):
        
        if lane:
            self.lane_id = safeNodeText(lane.find('lane_id'))
            self.position1.x = safeNodeText(lane.find('position/x1'))
            self.position1.y = safeNodeText(lane.find('position/y1'))
            self.position2.x = safeNodeText(lane.find('position/x2'))
            self.position2.y = safeNodeText(lane.find('position/y2'))
    
    def getValues(self):
        return [self.lane_id, self.position1.x, self.position1.y, self.position2.x, self.position2.y]
    
class CCTVConfiguration():
    
    
    def __init__(self, xmlPath = ''):
        
        self.root = None
        self.header = None
        self.roadInfo = None
        self.virtualGate = None
        
        if xmlPath != '':
            self.loadXmlFile(xmlPath)
    
    def loadXmlFile(self, xmlPath):
        self.xml = ElementTree.parse(xmlPath)
        self.loadXml(self.xml)
    
    def loadXmlStr(self, xmlStr):
        self.xml = ElementTree.ElementTree(ElementTree.fromstring(xmlStr))
        self.loadXml(self.xml)

    def loadXml(self, xml):
        self.root = self.xml.getroot()
        self.header = self.getHeader()
        self.roadInfo = self.getRoadInfo()
        self.virtualGate = self.getVirtualGate()
        
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
        
        self.header.showInTree(root)
        self.roadInfo.showInTree(root)
        self.virtualGate.showInTree(root)
        
    def findLanesOfRoad(self, roadId, linkId):
        lanes = []
        for road in self.getVirtualGate().roads:
            if (road.road_id == roadId) and (road.link_id == linkId):
                lanes = road.lanes
                break
        return lanes
    
    def findRoadIndex(self, roadId, linkId):
        roadIdx = -1
        for idx, road in enumerate(self.getVirtualGate().roads):
            if (road.road_id == roadId) and (road.link_id == linkId):
                roadIdx = idx
                break
        return roadIdx
    
    def toXmlString(self):
        xmlStr = self.header.toXmlString() + self.roadInfo.toXmlString() + self.virtualGate.toXmlString()
        xmlStr = '<Configuration type="cctv">' + xmlStr + '</Configuration>'
        return xmlStr
        
if __name__ == "__main__":
    
    xmlPath = 'D:/_Course/Project/LabelTool/data/cctv_configuration.xml'
    config = CCTVConfiguration(xmlPath)
    
    print(config.getHeader())
    print(config.getRoadInfo())
    print(config.getVirtualGate())
    