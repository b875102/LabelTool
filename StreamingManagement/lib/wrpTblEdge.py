# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 21:04:54 2022

@author: HUANG Chun-Huang
"""

import pandas as pd
from PyQt5 import QtCore, QtWidgets

from lib.tblib import Tblib
from wdg.EdgeDevice import EdgeDevice

class WrpTblEdge(QtCore.QObject, Tblib):
    
    __COL_EDGE = 0
    __COL_TASK = 1
    __COL_STATUS = 2    
    __COL_REFIDX = 3
    
    __task_list = ['offline', 'inline']
    __status_list = ['stop', 'start']
    
    def __init__(self, widget, config):
        super(WrpTblEdge, self).__init__(widget)
        
        self.__widget = widget
        self.__config = config
        
        self.__initHeader(self.__widget)
        
        self.__load(self.__config.getEdgeDevice())
        
        self.__sortReverse = True
        self.__loading = False
        
    def __initHeader(self, tbl):
        header = ['Edge Device', 'mode', 'status', 'refIdx']
        tbl.setColumnCount(len(header))
        tbl.setHorizontalHeaderLabels(header)
        tbl.hideColumn(self.__COL_REFIDX)
        tbl.setRowCount(0)
        
        header = tbl.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        
 
    def __load(self, edgeDeviceList):
        
        self.__loading = True
        self.__widget.setRowCount(0)
        contents = []
        
        for idx, edgeDevice in enumerate(edgeDeviceList):
            contents.append([edgeDevice['name'], edgeDevice['task'], edgeDevice['status'], str(idx)])
            
        addedRowIdxList = self.addRows(self.__widget, contents)
        self.addCombobox(self.__widget, self.__COL_TASK, self.__task_list, addedRowIdxList, self.TaskStatus_IndexChanged)
        self.addCombobox(self.__widget, self.__COL_STATUS, self.__status_list, addedRowIdxList, self.TaskStatus_IndexChanged)
        
        self.__loading = False
    
    def AddEdge(self):
        edgeDevice = EdgeDevice(self.__config.getStreamingNameList())
        execResult = edgeDevice.exec()
        if execResult == QtWidgets.QDialog.Accepted:
            edgeSetting = edgeDevice.GetResult(execResult)
            self.__config.addEdgeDevice(edgeSetting)
            self.__load(self.__config.getEdgeDevice())
            #self.__config.printConfig()
        else:
            pass      
    
    def UpdateEdge(self):
        selectedIndex = self.selectedIndex()
        if selectedIndex > -1:
            idx = int(self.getValue(self.__widget, selectedIndex, self.__COL_REFIDX))
            edgeDeviceList = self.__config.getEdgeDevice()
            edgeSetting = edgeDeviceList[idx]
            
            edgeDevice = EdgeDevice(self.__config.getStreamingNameList(), edgeSetting)
            execResult = edgeDevice.exec()
            if execResult == QtWidgets.QDialog.Accepted:
                edgeSetting = edgeDevice.GetResult(execResult)

                edgeDeviceList[idx] = edgeSetting
                self.__config.setEdgeDevice(edgeDeviceList)
                self.__load(self.__config.getEdgeDevice())
                #self.__config.printConfig()
            else:
                pass
    
    
    def DeleteEdge(self):
        selectedIndex = self.selectedIndex()
        if selectedIndex > -1:
            idx = int(self.getValue(self.__widget, selectedIndex, self.__COL_REFIDX))
            edgeDeviceList = self.__config.getEdgeDevice()
            edgeDeviceList.pop(idx)
            self.__config.setEdgeDevice(edgeDeviceList)
            self.__load(self.__config.getEdgeDevice())
            #self.__config.printConfig()
    
    def TaskStatus_IndexChanged(self, tbl, row, col, txt):
        #print(tbl, row, col, txt)
        task = self.getValue(self.__widget, row, self.__COL_TASK)
        status = self.getValue(self.__widget, row, self.__COL_STATUS)
        idx = int(self.getValue(self.__widget, row, self.__COL_REFIDX))
        edgeDeviceList = self.__config.getEdgeDevice()
        edgeSetting = edgeDeviceList[idx]
        edgeSetting['task'] = task
        edgeSetting['status'] = status
        return
    
    def SortEdge(self):
        self.__sortReverse = not self.__sortReverse
        rowCount = self.__widget.rowCount()
        contentList = []
        for idx in range(rowCount):
            edge = self.__widget.item(idx, self.__COL_EDGE).text()
            refIdx = int(self.__widget.item(idx, self.__COL_REFIDX).text())
            contentList.append([edge, refIdx])
            
        cdf = pd.DataFrame(contentList, columns = ['edge', 'refidx'])
        cdf = cdf.sort_values(by = ['edge'], ascending = self.__sortReverse).reset_index(drop = True)
        
        edgeDeviceList = self.__config.getEdgeDevice()
        sortedEdgeDeviceList= []
        
        for idx, row in cdf.iterrows():
            sortedEdgeDeviceList.append(edgeDeviceList[row['refidx']])
        
        self.__config.setEdgeDevice(sortedEdgeDeviceList)
        self.__load(self.__config.getEdgeDevice())
        #self.__config.printConfig()
        
    def ApplyEdge(self):
        self.__config.printConfig()
    
    def PreviewEdge(self):
        selectedIndex = self.selectedIndex()
        if selectedIndex > -1:
            idx = int(self.getValue(self.__widget, selectedIndex, self.__COL_REFIDX))
            edgeDeviceList = self.__config.getEdgeDevice()
            edgeSetting = edgeDeviceList[idx]
            print('Preview Edge', edgeSetting)

    def selectedIndex(self):
        return super().selectedIndex(self.__widget)
        
    def deleteRow(self):
        return super().deleteRow(self.__widget)

    def selectedRow(self, rowIdx):
        self.__loading = True
        super().selectedRow(self.__widget, rowIdx)
        self.__loading = False    