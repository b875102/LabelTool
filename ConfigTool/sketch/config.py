# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 21:55:30 2022

@author: Danny
"""

import pandas as pd
from ConfigTool.lib.intersection import Intersection

class Config():
    
    def __init__(self, path):
        self.__cpd = pd.read_excel(path, 'Intersection', skiprows = [0])
        self.intersections = []
        self.__getConfigs()
        return
    
    def __getConfigs(self):
        intersectionpd = self.__cpd.drop_duplicates(['intersection_id'])[['intersection_id']]
        
        for index, row in intersectionpd.iterrows():
            
            subpd = self.__cpd[self.__cpd['intersection_id'] == row['intersection_id']]
            subpd.reset_index(drop = True, inplace = True)
            
            intersection = Intersection()
            intersection.name = subpd.loc[0]['name']
            intersection.version = subpd.loc[0]['version']
            intersection.date = subpd.loc[0]['date']
            intersection.intersection_id = subpd.loc[0]['intersection_id']
            intersection.road_type = subpd.loc[0]['road_type']
            intersection.road_num = subpd.loc[0]['road_num']
            intersection.pd = subpd
            
            self.intersections.append(intersection)
            
        return
    
