# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 21:55:55 2022

@author: HUANG Chun-Huang
"""

import yaml

class Config():
        
    __CONFIG_FILE = 'conf/config.yaml'
    
    def __init__(self):
        self.__config = self.__getConfig()
        
    def __getConfig(self):
        with open(self.__CONFIG_FILE, mode = 'r') as f:
            config = yaml.safe_load(f)
        return config
    
    def save(self):
        with open(self.__CONFIG_FILE, 'w') as f:
            yaml.dump(self.__config, f)
        
    def getContainerInfo(self):
        return self.__config['container_info']
    
    def getCCTVList(self):
        return self.__config['cctvs']
    
    def setCCTVList(self, cctvList):
        self.__config['cctvs'] = cctvList
    
    def getDemoVideoList(self):
        return self.__config['demos']
    
    def setDemoVideoList(self, demoVideoList):
        self.__config['demos'] = demoVideoList
    
    def getStreamingServer(self):
        return self.__config['streaming_server']
    
    def getStreamingNameList(self):
        nameList = [setting['name'] for setting in self.getStreamingServer()]
        return nameList
    
    def setStreamingServer(self, streamingServerList):
        self.__config['streaming_server'] = streamingServerList
        
    def addStreamingServer(self, streamingSetting):
        self.__config['streaming_server'].append(streamingSetting)
    
    def getEdgeDevice(self):
        return self.__config['edge_device']

    def setEdgeDevice(self, edgeDeviceList):
        self.__config['edge_device'] = edgeDeviceList
        
    def addEdgeDevice(self, edgeSetting):
        self.__config['edge_device'].append(edgeSetting)
        
    def printConfig(self):
        print(self.__config)