# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 15:21:41 2022

@author: HUANG Chun-Huang
"""

import numpy as np
import pandas as pd
from PyQt5.QtGui import QPixmap, QImage

import xml.etree.ElementTree as ElementTree

from ConfigTool.conf.Header import Header
from ConfigTool.conf.RoadInfo import RoadInfo

from ConfigTool.sketch.intersection import Intersection as Sketch_Intersection

class IntersectionConfiguration():
    
    def __init__(self, name = '', version = '', date = '', intersection_id = '', ripd = None):

        self.header = Header(name, version, date, intersection_id)
        self.roadInfo = RoadInfo(ripd)
        
    @classmethod
    def columns(cls):
        return ['name', 'version', 'date', 'intersection_id', 'road_type', 'road_num', 'link_id', 'name.1', 'lane_num', 'section', 'direction']
        
    def loadFile(self, path):
        xml = ElementTree.parse(path)
        self.loadXml(xml)
        
    def loadXml(self, xml):
        root = xml.getroot()
        self.header.loadXml(root.find('header'))
        self.roadInfo.loadXml(root.find('road_information'))
    
    def toList(self):
        intersectionConfigurationList = []
        roadInfoList = self.roadInfo.toList()
        for roadInfo in roadInfoList:
            headerList = self.header.toList()
            headerList.extend(roadInfo)
            intersectionConfigurationList.append(headerList)
        
        return intersectionConfigurationList
        
    def toXml(self):
        xml = "<configuration type='intersection'>\n" + \
                self.header.toXml() + \
                self.roadInfo.toXml() + \
                "</configuration>"
        return xml
    
    def toSketch(self, path = '', save = False, inTrack = '', outTrack = ''):
        
        columns = self.columns()

        icpf = pd.DataFrame(self.toList(), columns = columns)
        sketch_intersection = Sketch_Intersection()
        
        sketch_intersection.name = self.header.name
        sketch_intersection.version = self.header.version
        sketch_intersection.date = self.header.date
        sketch_intersection.intersection_id = self.header.intersection_id
        sketch_intersection.road_type = self.roadInfo.roadType
        sketch_intersection.road_num = self.roadInfo.roadNum 
        sketch_intersection.pd = icpf
        
        try:
            img = sketch_intersection.generate(path, save, inTrack, outTrack)
            
            imgArr = np.asarray(img)
            height, width, channel = imgArr.shape
            bytesPerLine = 3 * width
            qimg = QImage(imgArr, width, height, bytesPerLine, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
        except Exception as ex:
            #print('error occured: ', ex)
            pixmap = QPixmap()
        finally:
            pass
        
        return pixmap

if __name__ == "__main__":
    
    intersectionConfiguration = IntersectionConfiguration()
    #print(intersectionConfiguration.toXml())
    
    intersectionConfiguration.loadFile('D:/_Course/Project/iTraffic/GUI/000北港大橋/IF-065/Intersection_configuration_IF-065.xml')
    
    sketch = intersectionConfiguration.toSketch()
