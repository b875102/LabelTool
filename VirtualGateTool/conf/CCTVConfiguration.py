import os
import xml.etree.ElementTree as ElementTree
from xml.dom import minidom

from PyQt5.QtWidgets import QTreeWidgetItem
from PyQt5.QtCore import QPoint

from VirtualGateTool.lib.FileHelper import FileHelper
from VirtualGateTool.lib.FileHelper import OptionType

def safeNodeText(node):
    txt = ''
    try:
        if node.text != None:
            txt = node.text
    except:
        txt = ''
    return txt
    
class PointPosition():
    def __init__(self, x = '', y = ''):
        self.x = x
        self.y = y
        
    def hasValue(self):
        result = self.x != '' and self.y != ''
        if result:
            result = float(self.x) != 0 and float(self.y) != 0
        return result
    
    def toQPoint(self):
        if self.hasValue():
            p = QPoint(int(self.x), int(self.y))
        else:
            p = QPoint()
        return p
    
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
        #self.name = ''
        self.version = ''
        self.date = ''
        self.intersection_id = ''
        self.device_ip = ''
        self.camera_position = GeographicCoordinate()
        
        self.extract(header)
        self.treeItems = {}
        
    def extract(self, header):
        
        if header:
            self.cctv = safeNodeText(header.find('cctv'))
            self.version = safeNodeText(header.find('version'))
            self.date = safeNodeText(header.find('date'))
            self.intersection_id = safeNodeText(header.find('intersection_id'))
            self.device_ip = safeNodeText(header.find('device_ip'))
            self.camera_position.latitude = safeNodeText(header.find('camera_position/lat'))
            self.camera_position.longitude = safeNodeText(header.find('camera_position/lng'))
            
    def showInTree(self, root):

        self.treeItems['cctv'] = QTreeWidgetItem(root, ['cctv', self.cctv])
        self.treeItems['version'] = QTreeWidgetItem(root, ['version', self.version])
        self.treeItems['date'] = QTreeWidgetItem(root, ['date', self.date])
        self.treeItems['intersection_id'] = QTreeWidgetItem(root, ['intersection_id', self.intersection_id])
        self.treeItems['device_ip'] = QTreeWidgetItem(root, ['device_ip', self.device_ip])
        
        pos = QTreeWidgetItem(root, ['camera_position'])
        self.treeItems['camera_position'] = pos
        self.treeItems['camera_position_lat'] = QTreeWidgetItem(pos, ['lat', self.camera_position.latitude])
        self.treeItems['camera_position_lng'] = QTreeWidgetItem(pos, ['lng', self.camera_position.longitude])
        
        
    def toXmlString(self):
        
        #'<name>' + self.name + '</name>' + \
            
        xmlStr = '<header>' + \
                    '<cctv>' + self.cctv + '</cctv>' + \
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
        self.treeItems = {}
        
    def extract(self, roadInfo):

        if roadInfo:
            for reference_point in roadInfo.findall('Reference_points/point'):
                self.reference_points.append(ReferencePoint(reference_point))
                
    def showInTree(self, root):
        
        road_Info = QTreeWidgetItem(root, ['road_information'])
        ref_point = QTreeWidgetItem(road_Info, ['Reference_points'])
        
        self.treeItems['road_information'] = road_Info
        self.treeItems['Reference_points'] = ref_point
        
        for idx, reference_point in enumerate(self.reference_points):
            
            point = QTreeWidgetItem(ref_point, ['point'])
            
            self.treeItems['reference_point_{0}'.format(idx)] = point
            self.treeItems['reference_point_{0}_img_x'.format(idx)] = QTreeWidgetItem(point, ['img_x', reference_point.img_position.x])
            self.treeItems['reference_point_{0}_img_y'.format(idx)] = QTreeWidgetItem(point, ['img_y', reference_point.img_position.y])
            self.treeItems['reference_point_{0}_lat'.format(idx)] = QTreeWidgetItem(point, ['lat', reference_point.geograph_position.latitude])
            self.treeItems['reference_point_{0}_lng'.format(idx)] = QTreeWidgetItem(point, ['lng', reference_point.geograph_position.longitude])
            
    def toXmlString(self):
        
        xmlStr = ''
        
        if len(self.reference_points) > 0:
            
            xmlStr = '<road_information>' + \
                        '<Reference_points>'
                        
            for ref_point in self.reference_points:
                
                xmlStr += '<point>' + \
                                '<img_x>' + ref_point.img_position.x + '</img_x>' + \
                                '<img_y>' + ref_point.img_position.y + '</img_y>' + \
                                '<lat>' + ref_point.geograph_position.latitude + '</lat>' + \
                                '<lng>' + ref_point.geograph_position.longitude + '</lng>' + \
                            '</point>'
                        
            xmlStr += '</Reference_points>' + \
                    '</road_information>'

        return xmlStr   
        
class VirtualGate():

    def __init__(self, virtualGate):
        self.roads = []
        self.extract(virtualGate)
        self.treeItems = {}
        
    def extract(self, virtualGate):

        if virtualGate:
            for road in virtualGate.findall('road'):
                self.roads.append(Road(road))
                
            if len(self.roads) == 0:
                for road in virtualGate.findall('Road'):
                    self.roads.append(Road(road))
                
    def showInTree(self, root):
        
        virtual_gate = QTreeWidgetItem(root, ['virtual_gate'])
        
        for roadIdx, road in enumerate(self.roads):
            itemRoad = QTreeWidgetItem(virtual_gate, ['road'])
            
            self.treeItems['Road_{0}'.format(roadIdx)] = itemRoad
            self.treeItems['Road_{0}_road_id'.format(roadIdx)] = QTreeWidgetItem(itemRoad, ['road_id', road.road_id])
            self.treeItems['Road_{0}_link_id'.format(roadIdx)] = QTreeWidgetItem(itemRoad, ['link_id', road.link_id])
            self.treeItems['Road_{0}_direction'.format(roadIdx)] = QTreeWidgetItem(itemRoad, ['direction', road.direction])
            
            itemPosition = QTreeWidgetItem(itemRoad, ['position'])
            
            self.treeItems['Road_{0}_position'.format(roadIdx)] = itemPosition
            self.treeItems['Road_{0}_position_x1'.format(roadIdx)] = QTreeWidgetItem(itemPosition, ['x1', road.position1.x])
            self.treeItems['Road_{0}_position_y1'.format(roadIdx)] = QTreeWidgetItem(itemPosition, ['y1', road.position1.y])
            self.treeItems['Road_{0}_position_x2'.format(roadIdx)] = QTreeWidgetItem(itemPosition, ['x2', road.position2.x])
            self.treeItems['Road_{0}_position_y2'.format(roadIdx)] = QTreeWidgetItem(itemPosition, ['y2', road.position2.y])
            
            itemLanes = QTreeWidgetItem(itemRoad, ['lanes'])
            self.treeItems['Road_{0}_itemLanes'.format(roadIdx)] = itemLanes
            
            for laneIdx, lane in enumerate(road.lanes):
                itemLane = QTreeWidgetItem(itemLanes, ['lane'])
                
                self.treeItems['Road_{0}_itemLanes_lane_{1}'.format(roadIdx, laneIdx)] = itemLane
                self.treeItems['Road_{0}_itemLanes_lane_{1}_lane_id'.format(roadIdx, laneIdx)] = QTreeWidgetItem(itemLane, ['lane_id', lane.lane_id])
                self.treeItems['Road_{0}_itemLanes_lane_{1}_forward_direction'.format(roadIdx, laneIdx)] = QTreeWidgetItem(itemLane, ['forward_direction', lane.forward_direction])
                
                itemPosition = QTreeWidgetItem(itemLane, ['position'])
                
                self.treeItems['Road_{0}_itemLanes_lane_{1}_position'.format(roadIdx, laneIdx)] = itemPosition
                self.treeItems['Road_{0}_itemLanes_lane_{1}_position_x1'.format(roadIdx, laneIdx)] = QTreeWidgetItem(itemPosition, ['x1', lane.position1.x])
                self.treeItems['Road_{0}_itemLanes_lane_{1}_position_y1'.format(roadIdx, laneIdx)] = QTreeWidgetItem(itemPosition, ['y1', lane.position1.y])
                self.treeItems['Road_{0}_itemLanes_lane_{1}_position_x2'.format(roadIdx, laneIdx)] = QTreeWidgetItem(itemPosition, ['x2', lane.position2.x])
                self.treeItems['Road_{0}_itemLanes_lane_{1}_position_y2'.format(roadIdx, laneIdx)] = QTreeWidgetItem(itemPosition, ['y2', lane.position2.y])
                
    def toXmlString(self):
        
        xmlStr = '<virtual_gate>'
        
        for road in self.roads:
            
            xmlStr += '<road>' + \
                        '<road_id>' + road.road_id + '</road_id>' + \
                        '<link_id>' + road.link_id + '</link_id>' + \
                        '<direction>' + road.direction + '</direction>' + \
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
                                '<forward_direction>' + lane.leftTurn + lane.uTurn + lane.rightTurn + lane.straight + '</forward_direction>' + \
                                '<position>' + \
                                    '<x1>' + lane.position1.x + '</x1>' + \
                                    '<y1>' + lane.position1.y + '</y1>' + \
                                    '<x2>' + lane.position2.x + '</x2>' + \
                                    '<y2>' + lane.position2.y + '</y2>' + \
                                '</position>' + \
                                '</lane>'
                    
                    
                xmlStr += '</lanes>'
                    
            xmlStr += '</road>'
        
        xmlStr += '</virtual_gate>'
        
        return xmlStr
        
class Road():
    
    def __init__(self, road):
        
        self.road_id = ''
        self.link_id = ''
        self.direction = 'In'
        self.position1 = PointPosition()
        self.position2 = PointPosition()
        
        self.lanes = []
        self.extract(road)
  
    def extract(self, road):
        
        if road:
            self.road_id = safeNodeText(road.find('road_id'))
            self.link_id = safeNodeText(road.find('link_id'))
            self.direction = safeNodeText(road.find('direction'))
            
            self.position1.x = safeNodeText(road.find('position/x1'))
            self.position1.y = safeNodeText(road.find('position/y1'))
            self.position2.x = safeNodeText(road.find('position/x2'))
            self.position2.y = safeNodeText(road.find('position/y2'))
            
            for lane in road.findall('lanes/lane'):
                self.lanes.append(Lane(lane))
                
    def getValues(self):
        #return [self.road_id, self.link_id, self.name, self.direction, self.section, self.position1.x, self.position1.y, self.position2.x, self.position2.y]
        return [self.road_id, self.link_id, self.direction, self.position1.x, self.position1.y, self.position2.x, self.position2.y]
        
class Lane():
    
    def __init__(self, lane):
        self.lane_id = ''
        self.forward_direction = '0000'
        self.straight = '0'
        self.rightTurn = '0'
        self.leftTurn = '0'
        self.uTurn = '0'
        self.position1 = PointPosition()
        self.position2 = PointPosition()
        
        self.extract(lane)
  
    def extract(self, lane):
        
        if lane:
            self.lane_id = safeNodeText(lane.find('lane_id'))
            self.forward_direction = safeNodeText(lane.find('forward_direction'))
            self.extractForwardDirection()
            
            self.position1.x = safeNodeText(lane.find('position/x1'))
            self.position1.y = safeNodeText(lane.find('position/y1'))
            self.position2.x = safeNodeText(lane.find('position/x2'))
            self.position2.y = safeNodeText(lane.find('position/y2'))
    
    def extractForwardDirection(self):
        
        straight = '0'
        rightTurn = '0'
        uTurn = '0'
        leftTurn = '0'
        
                
        if len(self.forward_direction) == 4:
            try:
                straight = self.forward_direction[3]
                rightTurn = self.forward_direction[2]
                uTurn = self.forward_direction[1]
                leftTurn = self.forward_direction[0] 
                            
            except:
                straight = '0'
                rightTurn = '0'
                uTurn = '0'
                leftTurn = '0'

        self.straight = straight
        self.rightTurn = rightTurn
        self.uTurn = uTurn
        self.leftTurn = leftTurn

    
    def getValues(self):
        return [self.lane_id, self.leftTurn, self.uTurn, self.rightTurn, self.straight, self.position1.x, self.position1.y, self.position2.x, self.position2.y]
    
class CCTVConfiguration():
    
    
    def __init__(self, xmlPath = ''):
        
        self.xmlPath = xmlPath
        self.fileHelper = FileHelper()
        
        self.root = None
        self.header = None
        self.roadInfo = None
        self.virtualGate = None
        
        if self.xmlPath != '':
            self.loadXmlFile(self.xmlPath)
    
    def loadXmlFile(self, xmlPath):
        self.xmlPath = xmlPath
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
        roadInfo = RoadInfo(self.root.find('road_information'))
        if len(roadInfo.reference_points) == 0:
            roadInfo = RoadInfo(self.root.find('RoadInformation'))
        return roadInfo
        
    def getVirtualGate(self):
        virtualGate = VirtualGate(self.root.find('virtual_gate'))
        if len(virtualGate.roads) == 0:
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
        
        tree.expandAll()
        tree.resizeColumnToContents(0)
        tree.resizeColumnToContents(1)
        
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
        xmlStr = '<configuration type="cctv">' + xmlStr + '</configuration>'
        return xmlStr
    
    def save(self, path = ''):
        
        #tree = ElementTree.fromstring(self.toXmlString())
        #xmlStr = etree.tostring(tree, pretty_print = True)
        
        reparsed = minidom.parseString(self.toXmlString())
        xmlStr = reparsed.toprettyxml(indent = '    ')
        print(xmlStr)
        
        if self.xmlPath == '':
            self.xmlPath = self.fileHelper.GetFile(None, 'Save CCTV Configuration', OptionType.Save)
        
        if self.xmlPath != '':

            if os.path.exists(self.xmlPath):
                print('overwrite file: ', self.xmlPath)
            else:
                print('create file: ', self.xmlPath)
                dirname = os.path.dirname(self.xmlPath)
                os.makedirs(dirname, exist_ok = True)
                
            self.fileHelper.WriteFile(xmlStr, self.xmlPath)
            
            
            
            
if __name__ == "__main__":
    
    #xmlPath = 'D:/_Course/Project/LabelTool/data/cctv_configuration.xml'
    xmlPath = 'D:/_Course/Project/LabelTool/data/cctv_configuration_IF-065-1.xml'
    config = CCTVConfiguration(xmlPath)
    
    #print(config.getHeader())
    #print(config.getRoadInfo())
    #print(config.getVirtualGate())
    
    print(config.toXmlString())
    config.save()

    