# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 15:22:14 2022

@author: HUANG Chun-Huang
"""

from ConfigTool.conf.Road import Road

class RoadInfo():
    
    def __init__(self, ripd):
        
        self.roadType = 'Intersection' 
        self.roadList = self.__load(ripd)
        self.roadNum = len(self.roadList)
        
    def __load(self, ripd):
        
        roadList = []
        
        if not (ripd is None):
            for idx, row in ripd.iterrows():
                link_id = row['link_id']
                name = row['name.1']
                lane_num = row['lane_num']
                section = row['section']
                direction = row['direction']
                
                road = Road(link_id, name, lane_num, section, direction)
                roadList.append(road)
            
        return roadList
    
    def loadXml(self, roadInfo):

        if roadInfo:
            
            self.road_type = roadInfo.find('road_type').text
            self.road_num = roadInfo.find('road_num').text
            
            self.roadList = []
            for road in roadInfo.findall('roads/road'):
                
                link_id = road.find('link_id').text
                name = road.find('name').text
                lane_num = road.find('lane_num').text
                section = road.find('section').text
                direction = road.find('direction').text
                
                self.roadList.append(Road(link_id, name, lane_num, section, direction))    
            
            self.roadNum = len(self.roadList)
            
    def toList(self):
        roadInfoList = []
        for road in self.roadList:
            roadInfo = [self.roadType, str(self.roadNum)]
            roadInfo.extend(road.toList())
            roadInfoList.append(roadInfo)
        
        return roadInfoList
    
    def addRoad(self, road):
        self.roadList.append(road)
        self.roadNum = len(self.roadList)
        
    def deleteRoad(self, idx):
        self.roadList.pop(idx)
        self.roadNum = len(self.roadList)
        
    def toXml(self):
        xml = \
            "\t<road_information>\n" + \
            "\t\t<road_type>" + self.roadType + "</road_type>\n" + \
            "\t\t<road_num>" + str(self.roadNum) + "</road_num>\n" + \
            "\t\t<roads>\n"

        for road in self.roadList:
            xml += road.toXml()

        xml += "\t\t</roads>\n"
        xml += "\t</road_information>\n"

        return xml       