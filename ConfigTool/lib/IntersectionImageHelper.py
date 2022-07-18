# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 21:05:37 2022

@author: HUANG Chun-Huang
"""

import os
import glob

class IntersectionImageHelper():
    
    __DEFAULT_DATASET_PATH = '/nol/iTraffic/GUI'
    #__DEFAULT_DATASET_PATH = 'D:/_Course/Project/iTraffic/GUI'
    
    #__PNG_PATH = '/**/**/**/*.png'
    __PNG_PATH = '/**/**/*.png'
    
    def __init__(self):
        
        self.__imageDict = self.__loadImage()
        
    def __loadImage(self):
        
        imageDict = {}
        
        imgList = glob.glob(self.__DEFAULT_DATASET_PATH + self.__PNG_PATH, recursive = True)
        
        for img in imgList:
            basename = os.path.basename(img).split('.')[0]
            imageDict[basename] = img
        
        return imageDict
    
    def getPath(self, intersectionId):
        
        path = ''
        
        if intersectionId in self.__imageDict:
            path = self.__imageDict[intersectionId]
            
        return path
    
if __name__ == "__main__":
    
    helper = IntersectionImageHelper()
    print(helper.getPath('IP-034'))