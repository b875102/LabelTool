# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 19:09:31 2022

@author: HUANG Chun-Huang
"""

import os
import pandas as pd
import json 

from ConfigTool.lib.FileHelper import FileHelper
from ConfigTool.conf.IntersectionConfiguration import IntersectionConfiguration
from ConfigTool.conf.Road import Road

class IntersectionConfigurationHelper():
    
    __CSV_INTERSECTION_CONFIG = 'ConfigTool/Intersection_configuration.csv'
    __XLSM_INTERSECTION_CONFIG = 'ConfigTool/Intersection_configuration.xlsm'
    
    # {0}: cwd
    # {1}: project key
    # {2}: intersection id
    # {3}: intersection id
    
    __XML_INTERSECTION_CONFIG = "{0}/{1}/{2}/Intersection_configuration_{3}.xml"
    __PNG_INTERSECTION_CONFIG = "{0}/{1}/{2}/{3}.png"
    
    def __init__(self):
        self.cwd = os.getcwd()
        self.projects = self.__getProjects()
    
    @classmethod
    def columns(cls):
        return IntersectionConfiguration.columns()
    
    @classmethod
    def getEmptyInstance(cls):
        name = ''
        version = ''
        date = ''
        intersection_id = ''
        ripd = pd.DataFrame(columns = Road.columns())
        intersectionConfiguration = IntersectionConfiguration(name, version, date, intersection_id, ripd)
        return intersectionConfiguration
        
    def getIntersectionConfigList(self):
        
        if os.path.exists(self.__CSV_INTERSECTION_CONFIG):
            #confpd = pd.read_csv(self.__CSV_INTERSECTION_CONFIG, sep = ',', engine = 'python')
            confpd = pd.read_csv(self.__CSV_INTERSECTION_CONFIG, sep = ',', encoding = 'utf-8')
        else:
            confpd = pd.read_excel(self.__XLSM_INTERSECTION_CONFIG, 'Intersection', header = 1)
            confpd['date'] = confpd['date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        
        confpd.fillna('', inplace=True)
        
        headerpd = confpd.drop_duplicates(['intersection_id'])[['intersection_id']].sort_values(by = ['intersection_id'])
        headerpd.reset_index()
        
        intersectionConfigList = []
        
        for idx, row in headerpd.iterrows():
            
            intersection_id = row['intersection_id']
            
            ripd = confpd[(confpd['intersection_id'] == intersection_id)]
            ripd.reset_index(drop = True, inplace = True)
            
            if ripd.shape[0] > 0:
                name = ripd.loc[0]['name']
                version = ripd.loc[0]['version']
                date = ripd.loc[0]['date']
                
                intersectionConfiguration = IntersectionConfiguration(name, version, date, intersection_id, ripd)
                intersectionConfigList.append(intersectionConfiguration)
        
        return intersectionConfigList
    
    def saveIntersectionConfigList(self, intersectionConfigurationList):
        if len(intersectionConfigurationList) > 0:
            self.__saveIntersectionConfigCsv(intersectionConfigurationList)
            self.__saveIntersectionConfigXml(intersectionConfigurationList)
            self.__saveIntersectionConfigPng(intersectionConfigurationList)
    
    def __saveIntersectionConfigCsv(self, intersectionConfigurationList):
        contentList = []
        contentList.append(','.join(IntersectionConfigurationHelper.columns()))
        
        for intersectionConfiguration in intersectionConfigurationList:
            contents = intersectionConfiguration.toList()
            for content in contents:
                contentList.append(','.join(content))
            
        fileHelper = FileHelper()
        
        if fileHelper.writeTxt(self.__CSV_INTERSECTION_CONFIG, contentList):            
            print('save intersection configuration successfully')
        else:
            print('no intersection configuration')
            
        return len(contents)
    
    def __saveIntersectionConfigXml(self, intersectionConfigurationList):
        xmldict = {}
        for intersectionConfiguration in intersectionConfigurationList:
            
            intersection_id = intersectionConfiguration.header.intersection_id
            project = self.projects[intersection_id]
            
            xname = self.__XML_INTERSECTION_CONFIG.format(self.cwd, project, intersection_id, intersection_id)
            xml = intersectionConfiguration.toXml()
            xmldict[xname] = xml
        
        fileHelper = FileHelper()
        fileHelper.writeFiles(xmldict)
        print('done')
        
    def __saveIntersectionConfigPng(self, intersectionConfigurationList):
        #pngdict = {}
        for intersectionConfiguration in intersectionConfigurationList:
            
            intersection_id = intersectionConfiguration.header.intersection_id
            project = self.projects[intersection_id]
            
            pname = self.__PNG_INTERSECTION_CONFIG.format(self.cwd, project, intersection_id, intersection_id)
            intersectionConfiguration.toSketch(pname, True)

        print('done')

    def __getProjects(self):
        projects = {}
        with open('projects.json', mode = 'r', encoding ="utf-8") as f:
            data = json.load(f)
            for project in data:
                intersectionIds = data[project]['IntersectionID']
                for intersectionId in intersectionIds:
                    projects[intersectionId] = project
        return projects
            
            