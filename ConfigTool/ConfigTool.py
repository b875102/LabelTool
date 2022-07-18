# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 15:00:06 2022

@author: HUANG Chun-Huang
"""

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QDialogButtonBox

from ConfigTool.conf.IntersectionConfigurationHelper import IntersectionConfigurationHelper
from ConfigTool.conf.Road import Road

from ConfigTool.lib.IntersectionImageHelper import IntersectionImageHelper
from ConfigTool.lib.WrpTblIntersection import WrpTblIntersection
from ConfigTool.lib.WrpTblRoad import WrpTblRoad
from ConfigTool.lib.Image import Image

class ConfigTool(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(ConfigTool, self).__init__()
        uic.loadUi('ConfigTool/ConfigTool.ui', self)

        self.__intersectionConfigurationHelper = IntersectionConfigurationHelper()
        self.__intersectionImageHelper = IntersectionImageHelper()
        
        self.wrpTblIntersection = WrpTblIntersection(self.tblIntersection)
        self.wrpTblRoad = WrpTblRoad(self.tblRoad)
        
        self.__intersectionConfigList = self.__intersectionConfigurationHelper.getIntersectionConfigList()
                
        self.wrpTblIntersection.load(self.__intersectionConfigList)
        self.wrpTblIntersection.IntersectionSelectionChangedEvent.connect(self.IntersectionSelectionChanged)
        self.wrpTblIntersection.IntersectionItemChangedEvent.connect(self.IntersectionItemChangedEvent)
        self.wrpTblRoad.RoadSelectionChangedEvent.connect(self.RoadSelectionChanged)
        self.wrpTblRoad.RoadItemChangedEvent.connect(self.RoadItemChanged)
        
        self.btnIntersectionAdd.clicked.connect(self.__AddIntersection)
        self.btnIntersectionDelete.clicked.connect(self.__DeleteIntersection)
        
        self.btnRoadAdd.clicked.connect(self.__AddRoad)
        self.btnRoadDelete.clicked.connect(self.__DeleteRoad)
             
        btnApply = self.buttonBox.button(QDialogButtonBox.Ok)
        btnCancel = self.buttonBox.button(QDialogButtonBox.Cancel)
        btnApply.clicked.connect(self.__applyChanges)
        btnCancel.clicked.connect(self.__cancelChanges)         
        
        self.imageIntersection = Image(self.scrollArea, self.lblIntersectionImage, self.hsldIScaling, self.spbIScaling, self.btnIDock)
        self.imageSketch = Image(self.scrollArea_2, self.lblSketchImage, self.hsldSScaling, self.spbSScaling, self.btnSDock)
        
    def show(self):
        super().show()
        
    @QtCore.pyqtSlot(int)
    def IntersectionSelectionChanged(self, idx):
        self.wrpTblRoad.load(idx, self.__intersectionConfigList[idx].roadInfo.roadList)
        self.showIntersection(self.__intersectionConfigList[idx])
        self.showSketch(self.__intersectionConfigList[idx])

    @QtCore.pyqtSlot(int, list)
    def IntersectionItemChangedEvent(self, idx, contentList):
        self.__intersectionConfigList[idx].header.update(contentList)
        
    @QtCore.pyqtSlot(int, str, str)
    def RoadSelectionChanged(self, idx, inTrack, outTrack):
        self.showSketch(self.__intersectionConfigList[idx], inTrack, outTrack)
        
    @QtCore.pyqtSlot(int, list)
    def RoadItemChanged(self, idx, roadList):
        self.__intersectionConfigList[idx].roadInfo.roadList = roadList
        self.showSketch(self.__intersectionConfigList[idx])
        
    def showIntersection(self, intersectionConfig):
        header = intersectionConfig.header
        path = self.__intersectionImageHelper.getPath(header.intersection_id)
        self.imageIntersection.setImage(QPixmap(path))
        
    def showSketch(self, intersectionConfig, inTrack = '', outTrack = ''):
        self.imageSketch.setImage(intersectionConfig.toSketch('', False, inTrack, outTrack))
                              
    def __AddIntersection(self):
        rowCount = len(self.__intersectionConfigList)
        intersectionConfiguration = IntersectionConfigurationHelper.getEmptyInstance()
        self.__intersectionConfigList.append(intersectionConfiguration)
        self.wrpTblIntersection.load(self.__intersectionConfigList)
        self.IntersectionSelectionChanged(rowCount)
        self.wrpTblIntersection.selectedRow(rowCount)
        
        
    def __DeleteIntersection(self):
        deletedRow = self.wrpTblIntersection.deleteRow()
        self.__intersectionConfigList.pop(deletedRow)
        self.wrpTblIntersection.load(self.__intersectionConfigList)
        
    def __AddRoad(self):
        selectedIndex = self.wrpTblIntersection.selectedIndex()
        if selectedIndex > -1:
            road = Road('', '', '', '', '')
            self.__intersectionConfigList[selectedIndex].roadInfo.addRoad(road)
            self.IntersectionSelectionChanged(selectedIndex)

    def __DeleteRoad(self):
        selectedIndex = self.wrpTblIntersection.selectedIndex()
        if selectedIndex > -1:        
            deletedRowIdx = self.wrpTblRoad.deleteRow()
            self.__intersectionConfigList[selectedIndex].roadInfo.deleteRoad(deletedRowIdx)
            
    def __applyChanges(self):
        self.__intersectionConfigurationHelper.saveIntersectionConfigList(self.__intersectionConfigList)
    
    def __cancelChanges(self):
        self.__intersectionConfigList = IntersectionConfigurationHelper().getIntersectionConfigList()
        self.wrpTblIntersection.load(self.__intersectionConfigList)