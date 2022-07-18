# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 14:46:36 2022

@author: HUANG Chun-Huang
"""

from PyQt5 import QtCore
from ConfigTool.lib.Tblib import Tblib
from ConfigTool.conf.Road import Road

class WrpTblRoad(QtCore.QObject, Tblib):
    
    __COL_LINK_ID = 0
    __COL_NAME = 1
    __COL_LANE_NUM = 2
    __COL_SECTION = 3
    __COL_DIRECTION = 4
    __COL_REFIDX = 5
    RoadSelectionChangedEvent = QtCore.pyqtSignal(int, str, str)
    RoadItemChangedEvent = QtCore.pyqtSignal(int, list)
    
    def __init__(self, widget):
        super(WrpTblRoad, self).__init__(widget)   
        
        self.__widget = widget
        self.__initHeader(self.__widget)        
        
        self.__widget.itemChanged.connect(self.__itemChanged)
        self.__widget.itemSelectionChanged.connect(self.__itemSelectionChanged)
        
        self.__loading = False
        self.hidx = -1
        
    def __initHeader(self, tbl):
        header = ['link_id', 'name', 'lane_num', 'section', 'direction', 'refIdx']
        tbl.setColumnCount(len(header))
        tbl.setHorizontalHeaderLabels(header)
        tbl.hideColumn(self.__COL_REFIDX)
        tbl.setRowCount(0)    
        
    def load(self, hidx, roadList):
        
        self.__loading = True
        self.__widget.setRowCount(0)
        self.hidx = hidx
        
        contents = []
        
        for idx, road in enumerate(roadList):
            roads = road.toList()
            roads.append(str(idx))
            contents.append(roads)
            
        self.addRows(self.__widget, contents)
        self.__loading = False
        
    def __itemChanged(self, item):
        self.resizeToContents(self.__widget)
        if not self.__loading:
            
            rowCount = self.__widget.rowCount()
            roadList = []
            
            for idx in range(rowCount):
                
                link_id = self.getValue(self.__widget, idx, self.__COL_LINK_ID)
                name = self.getValue(self.__widget, idx, self.__COL_NAME)
                lane_num = self.getValue(self.__widget, idx, self.__COL_LANE_NUM)
                section = self.getValue(self.__widget, idx, self.__COL_SECTION)
                direction = self.getValue(self.__widget, idx, self.__COL_DIRECTION)
                
                road = Road(link_id, name, lane_num, section, direction)
                roadList.append(road)

            self.RoadItemChangedEvent.emit(self.hidx, roadList)

    def __itemSelectionChanged(self):
        selectedIndexes = self.selectedIndexes(self.__widget)
        if len(selectedIndexes) > 0:
            def match(selectedIndexes, direction):
                result = ''
                for selectedIndex in selectedIndexes:
                    if self.getValue(self.__widget, selectedIndex, self.__COL_DIRECTION) == direction:
                        result = self.getValue(self.__widget, selectedIndex, self.__COL_LINK_ID)
                        break
                return result
            
            inTrack = match(selectedIndexes, 'In')
            outTrack = match(selectedIndexes, 'Out')
            
            self.RoadSelectionChangedEvent.emit(self.hidx, inTrack, outTrack)
            
    def selectedIndex(self):
        return super().selectedIndex(self.__widget)
        
    def deleteRow(self):
        return super().deleteRow(self.__widget)

    def selectedRow(self, rowIdx):
        self.__loading = True
        super().selectedRow(self.__widget, rowIdx)
        self.__loading = False