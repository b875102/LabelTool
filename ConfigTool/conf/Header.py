# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 15:21:54 2022

@author: HUANG Chun-Huang
"""

class Header():
    
    def __init__(self, name = '', version = '', date = '', intersection_id = ''):

        self.name = name
        self.version = version
        self.date = date
        self.intersection_id = intersection_id
        
    def loadXml(self, header):
        
        if header:
            self.name = header.find('name').text
            self.version = header.find('version').text
            self.date = header.find('date').text
            self.intersection_id = header.find('intersection_id').text        
        
    def toList(self):
        return [self.name, str(self.version), self.date, self.intersection_id]
    
    def update(self, contentList):
        self.name = contentList[0]
        self.version = contentList[1]
        self.date = contentList[2]
        self.intersection_id = contentList[3]
        
    def toXml(self):
        xml = \
            "\t<header>\n" + \
            "\t\t<name>" + self.name + "</name>\n" + \
            "\t\t<version>" + str(self.version) + "</version>\n" + \
            "\t\t<date>" + self.date + "</date>\n" + \
            "\t\t<intersection_id>" + self.intersection_id + "</intersection_id>\n" + \
            "\t</header>\n"
        return xml        