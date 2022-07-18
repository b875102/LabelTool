# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 15:22:04 2022

@author: HUANG Chun-Huang
"""

class Road():
    
    def __init__(self, link_id, name, lane_num, section, direction):
        
        self.link_id = link_id
        self.name = name
        self.lane_num = lane_num
        self.section = section
        self.direction = direction
        
    @classmethod
    def columns(cls):
        return ['link_id', 'name.1', 'lane_num', 'section', 'direction']
        
    def toList(self):
        return [self.link_id, self.name, str(self.lane_num), self.section, self.direction]
    
    def toXml(self):
        xml = \
            "\t\t\t<road>\n" + \
            "\t\t\t\t<link_id>" + self.link_id + "</link_id>\n" + \
            "\t\t\t\t<name>" + self.name + "</name>\n" + \
            "\t\t\t\t<lane_num>" + str(self.lane_num) + "</lane_num>\n" + \
            "\t\t\t\t<section>" + self.section + "</section>\n" + \
            "\t\t\t\t<direction>" + self.direction + "</direction>\n" + \
            "\t\t\t</road>\n"

        return xml  