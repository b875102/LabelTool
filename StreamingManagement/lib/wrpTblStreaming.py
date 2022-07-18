# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 22:04:10 2022

@author: HUANG Chun-Huang
"""

import pandas as pd
from PyQt5 import QtCore, QtWidgets

from lib.streamingHelper import StreamingHelper
from lib.tblib import Tblib
from wdg.StreamingInfo import StreamingInfo

class WrpTblStreaming(QtCore.QObject, Tblib):
    
    __COL_STREAMING = 0
    __COL_TASK = 1
    __COL_STATUS = 2
    __COL_REFIDX = 3
    
    __task_list = ['demo', 'live']
    __status_list = ['stop', 'start']    
    
    def __init__(self, widget, config):
        super(WrpTblStreaming, self).__init__(widget)
        
        self.__widget = widget
        self.__config = config
        
        self.__initHeader(self.__widget)
        
        self.__load(self.__config.getStreamingServer())
        
        self.__sortReverse = True
        self.__loading = False
        
    def __headers(self):
        return ['name', 'mode', 'status', 'refidx']
        
    def __initHeader(self, tbl):
        headers = self.__headers()
        tbl.setColumnCount(len(headers))
        tbl.setHorizontalHeaderLabels(headers)
        tbl.hideColumn(self.__COL_REFIDX)
        tbl.setRowCount(0)
        
        header = tbl.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        
 
    def __load(self, streamingServerList):
        
        self.__loading = True
        self.__widget.setRowCount(0)
        contents = []
        
        for idx, streamingServer in enumerate(streamingServerList):
            contents.append([streamingServer['name'], streamingServer['task'], streamingServer['status'], str(idx)])
            
        addedRowIdxList = self.addRows(self.__widget, contents)
        self.addCombobox(self.__widget, self.__COL_TASK, self.__task_list, addedRowIdxList, self.TaskStatus_IndexChanged)
        self.addCombobox(self.__widget, self.__COL_STATUS, self.__status_list, addedRowIdxList, self.TaskStatus_IndexChanged)
        
        self.__loading = False
        
    def AddStreaming(self):
        streamingInfo = StreamingInfo(self.__config.getCCTVList(), self.__config.getDemoVideoList())
        execResult = streamingInfo.exec()
        if execResult == QtWidgets.QDialog.Accepted:
            cctvList, demoVideoList, streamingSetting = streamingInfo.GetResult(execResult)
            self.__config.setCCTVList(cctvList)
            self.__config.setDemoVideoList(demoVideoList)
            self.__config.addStreamingServer(streamingSetting)
            self.__load(self.__config.getStreamingServer())
            #self.__config.printConfig()
        else:
            pass      
        
    def UpdateStreaming(self):
        selectedIndex = self.selectedIndex()
        if selectedIndex > -1:
            idx = int(self.getValue(self.__widget, selectedIndex, self.__COL_REFIDX))
            streamingServerList = self.__config.getStreamingServer()
            streamingSetting = streamingServerList[idx]
            
            streamingInfo = StreamingInfo(self.__config.getCCTVList(), self.__config.getDemoVideoList(), streamingSetting)
            execResult = streamingInfo.exec()
            if execResult == QtWidgets.QDialog.Accepted:
                cctvList, demoVideoList, streamingSetting = streamingInfo.GetResult(execResult)
                self.__config.setCCTVList(cctvList)
                self.__config.setDemoVideoList(demoVideoList)
                streamingServerList[idx] = streamingSetting
                self.__config.setStreamingServer(streamingServerList)
                self.__load(self.__config.getStreamingServer())
                #self.__config.printConfig()
            else:
                pass
        
    def DeleteStreaming(self):
        selectedIndex = self.selectedIndex()
        if selectedIndex > -1:
            idx = int(self.getValue(self.__widget, selectedIndex, self.__COL_REFIDX))
            streamingServerList = self.__config.getStreamingServer()
            streamingServerList.pop(idx)
            self.__config.setStreamingServer(streamingServerList)
            self.__load(self.__config.getStreamingServer())
            #self.__config.printConfig()
    
    def TaskStatus_IndexChanged(self, tbl, row, col, txt):
        #print(tbl, row, col, txt)
        task = self.getValue(self.__widget, row, self.__COL_TASK)
        status = self.getValue(self.__widget, row, self.__COL_STATUS)
        idx = int(self.getValue(self.__widget, row, self.__COL_REFIDX))
        streamingServerList = self.__config.getStreamingServer()
        streamingSetting = streamingServerList[idx]
        streamingSetting['task'] = task
        streamingSetting['status'] = status
        return
        
    def SortStreaming(self):
        self.__sortReverse = not self.__sortReverse
        rowCount = self.__widget.rowCount()
        contentList = []
        for idx in range(rowCount):
            streaming = self.__widget.item(idx, self.__COL_STREAMING).text()
            task = self.__widget.item(idx, self.__COL_TASK).text()
            status = self.__widget.item(idx, self.__COL_STATUS).text()
            refIdx = int(self.__widget.item(idx, self.__COL_REFIDX).text())
            contentList.append([streaming, task, status, refIdx])
            
        cdf = pd.DataFrame(contentList, columns = self.__headers())
        cdf = cdf.sort_values(by = ['name'], ascending = self.__sortReverse).reset_index(drop = True)
        
        streamingServerList = self.__config.getStreamingServer()
        sortedStreamingServerList = []
        
        for idx, row in cdf.iterrows():
            sortedStreamingServerList.append(streamingServerList[row['refidx']])
        
        self.__config.setStreamingServer(sortedStreamingServerList)
        self.__load(self.__config.getStreamingServer())
        #self.__config.printConfig()
        
    def ApplyStreaming(self):
        streamingHelper = StreamingHelper()
        for setting in self.__config.getStreamingServer():
            streamingHelper.post(setting)
        
    def PreviewStreaming(self):
        selectedIndex = self.selectedIndex()
        if selectedIndex > -1:
            idx = int(self.getValue(self.__widget, selectedIndex, self.__COL_REFIDX))
            streamingServerList = self.__config.getStreamingServer()
            streamingSetting = streamingServerList[idx]
            print('Preview Streaming', streamingSetting)
            
            streamingHelper = StreamingHelper()
            streamingHelper.preview(streamingSetting)
            
            
    
    def selectedIndex(self):
        return super().selectedIndex(self.__widget)
        
    def deleteRow(self):
        return super().deleteRow(self.__widget)

    def selectedRow(self, rowIdx):
        self.__loading = True
        super().selectedRow(self.__widget, rowIdx)
        self.__loading = False    