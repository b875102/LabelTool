# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 14:31:36 2022

@author: HUANG Chun-Huang
"""

from PyQt5 import QtCore
from ConfigTool.lib.Tblib import Tblib

class WrpTblIntersection(QtCore.QObject, Tblib):
    
    
    
    __COL_NAME = 0
    __COL_VERSION = 1
    __COL_DATE = 2
    __COL_INTERSECTION_ID = 3
    __COL_REFIDX = 4
    IntersectionSelectionChangedEvent = QtCore.pyqtSignal(int)
    IntersectionItemChangedEvent = QtCore.pyqtSignal(int, list)
    
    
    def __init__(self, widget):
        super(WrpTblIntersection, self).__init__(widget)
        
        self.__widget = widget
        self.__initHeader(self.__widget)
        
        self.__widget.itemChanged.connect(self.__itemChanged)
        self.__widget.itemSelectionChanged.connect(self.__itemSelectionChanged)
        
        self.__loading = False
        
    def __initHeader(self, tbl):
        header = ['name', 'version', 'date', 'intersection_id', 'refIdx']
        tbl.setColumnCount(len(header))
        tbl.setHorizontalHeaderLabels(header)
        tbl.hideColumn(self.__COL_REFIDX)
        tbl.setRowCount(0)
        
    def load(self, intersectionConfigList):
        
        self.__loading = True
        self.__widget.setRowCount(0)
        contents = []
        
        for idx, intersectionConfig in enumerate(intersectionConfigList):
            headers = intersectionConfig.header.toList()
            headers.append(str(idx))
            contents.append(headers)
            
        self.addRows(self.__widget, contents)
        self.__loading = False
        
    def __itemChanged(self, item):
        self.resizeToContents(self.__widget)
        if not self.__loading:
            selectedIndex = self.selectedIndex()
            if selectedIndex > -1:
                idx = int(self.getValue(self.__widget, selectedIndex, self.__COL_REFIDX))
                
                name = self.getValue(self.__widget, selectedIndex, self.__COL_NAME)
                version = self.getValue(self.__widget, selectedIndex, self.__COL_VERSION)
                modify_date = self.getValue(self.__widget, selectedIndex, self.__COL_DATE)
                intersection_id = self.getValue(self.__widget, selectedIndex, self.__COL_INTERSECTION_ID)
                
                contentList = [name, version, modify_date, intersection_id]
                self.IntersectionItemChangedEvent.emit(idx, contentList)
                
            
    def __itemSelectionChanged(self):
        selectedIndex = self.selectedIndex()
        if selectedIndex > -1:
            idx = int(self.getValue(self.__widget, selectedIndex, self.__COL_REFIDX))
            self.IntersectionSelectionChangedEvent.emit(idx)
        
    def selectedIndex(self):
        return super().selectedIndex(self.__widget)
        
    def deleteRow(self):
        return super().deleteRow(self.__widget)

    def selectedRow(self, rowIdx):
        self.__loading = True
        super().selectedRow(self.__widget, rowIdx)
        self.__loading = False
        
    
