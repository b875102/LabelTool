import sys
import os
import copy
#from functools import partial
import glob

from PyQt5 import QtCore, QtGui, QtWidgets, uic

from VirtualGateTool.label.Label import Label
from VirtualGateTool.label.Label import RoadType
from VirtualGateTool.label.Label import RoadFlag

from VirtualGateTool.lib.Image import Image
from VirtualGateTool.lib.FileHelper import FileHelper
from VirtualGateTool.lib.ImageHelper import ImageHelper
from VirtualGateTool.lib.OpenFileDialog import OpenFileDialog

from VirtualGateTool.conf.CCTVConfiguration import CCTVConfiguration
from VirtualGateTool.conf.IntersectionConfiguration import IntersectionConfiguration
from VirtualGateTool.conf.CCTVConfiguration import Road as CCTVRoad
from VirtualGateTool.conf.CCTVConfiguration import Lane as CCTVLane
from VirtualGateTool.conf.CCTVConfiguration import ReferencePoint as CCTVReferencePoint

class LabelTool(QtWidgets.QMainWindow):
    
    _SCALING_BASE = 100
    _SCALING_MIN = 10
    
    _TABLE_COLUMNS_REFERENCE_POINTS = 4 + 1
    _TABLE_COLUMNS_ROAD = 7 + 1
    _TABLE_COLUMNS_LANE = 9 + 2
    
    _DEFAULT_VALUE_CELL = '0'
    
    def __init__(self):
        super(LabelTool, self).__init__()
        uic.loadUi('VirtualGateTool/LabelTool.ui', self)
        
        self.init = True
        
        #initial components
        
        self.setWindowTitle(self.GetTitle())        
        self.lblCoordinate = QtWidgets.QLabel('')
        self.statusBar().addPermanentWidget(self.lblCoordinate)
        self.openFileDialog = OpenFileDialog(self)
        
        self.image = None
        self.illustrationImage = None
        
        #event connect
        #Tool Bar
        self.actionOpen_Images.triggered.connect(self.OpenImages_Click)
        self.actionIllustration_Image.triggered.connect(self.Illustration_Image_Click)
        self.actionIntersection_Configuration.triggered.connect(self.Intersection_Configuration_Click)
        self.actionCCTV_Configuration.triggered.connect(self.CCTV_Configuration_Click)
        
        #Widget
        self.hsldScaling.valueChanged.connect(self.SetSilder)
        self.btnDock.clicked.connect(self.DockImage)
        self.treeIntersectionConfig.itemClicked.connect(self.TreeIntersectionConfig_ItemClicked)
        self.chkShowRoadId.stateChanged.connect(self.ChkShowRoadId_StateChanged)
        self.chkShowLinkId.stateChanged.connect(self.ChkShowRoadId_StateChanged)
        self.chkShowLaneId.stateChanged.connect(self.ChkShowRoadId_StateChanged)
        
        self.btnSave1.clicked.connect(self.__saveCCTVConfig)
        self.btnSave2.clicked.connect(self.__saveCCTVConfig)
        
        self.hsldNr.valueChanged.connect(self.ChangeImage)
        self.btnReset.clicked.connect(self.__ResetImage)
        
        #CCTV Config Widget
        self.__initialTableHeader()
        
        self.tblReferencePoints.itemChanged.connect(self.__tblReferencePoints_ItemChanged)
        
        self.btnAddPoint.clicked.connect(self.__AddPoint)
        self.btnDeletePoint.clicked.connect(self.__DeletePoint)
        
        self.tblRoad.itemChanged.connect(self.__tblRoad_ItemChanged)
        self.tblRoad.itemSelectionChanged.connect(self.__tblRoad_ItemSelectionChanged)
        
        self.btnAddRoad.clicked.connect(self.__AddRoad)
        self.btnDeleteRoad.clicked.connect(self.__DeleteRoad)
        
        self.tblLane.itemChanged.connect(self.__tblLane_ItemChanged)
        self.tblLane.itemSelectionChanged.connect(self.__tblLane_ItemSelectionChanged)
        
        self.btnAddLane.clicked.connect(self.__AddLane)
        self.btnDeleteLane.clicked.connect(self.__DeleteLane)
        
        self.keepRoadIdxOfLanes = -1
        
        self.roadFlagByte = RoadFlag.Road | RoadFlag.Link | RoadFlag.Lane

        #libs
        self.fileHelper = FileHelper()
        self.intersectionConfig = IntersectionConfiguration()
        self.cctvConfig = CCTVConfiguration()
        
        #set attribute
        self.spbScaling.setSuffix('%')
        self.hsldScaling.setValue(100)
        
        
        self.imagePath = ''
        self.imagePathList = []
        self.cctvImagePath = ''
        
        self.init = False
        self.refreshRoadTable = False
        self.refreshLaneTable = False
        



        
    def __del__(self):
        print('called destructor')
        
    def show(self):
        super().show()
        
    def keyPressEvent(self, event):
        #print('mainform keyPressEvent ', event.key())
        if event.key() == QtCore.Qt.Key_Delete:
            pass
            #if self.image:
            #    self.image.keyPressEvent(event)
        
    def GetTitle(self, prefix = ''):
        appname = 'Virtual Gate Label Tool {0}'
        return appname.format(prefix)
       
    def OpenVideo_Click(self):
        print('OpenVideo_Click')
        pass
    
    def OpenImages_Click(self):
        #print('OpenImages_Click')
        
        if self.openFileDialog.exec() == QtWidgets.QDialog.Accepted:
            if self.openFileDialog.checkResult():
                
                self.treeIntersectionConfig.clear()
                
                print('QDialog.Accepted', self.openFileDialog.getResult())
                dialogResult = self.openFileDialog.getResult()
                
                self.OpenImages(dialogResult)
            else:
                print('QDialog.Invalid')
        else:
            print('QDialog.Rejected')
    
    def Illustration_Image_Click(self):
        #print('Illustration_Image_Click')
        self.dwgIllustrationImage.show()
    
    def Intersection_Configuration_Click(self):
        #print('Intersection_Configuration_Click')
        self.dwgIntersectionConfiguration.show()
    
    def CCTV_Configuration_Click(self):
        self.dwgCCTVConfiguration.show()
        
    def TreeCCTVConfig_ItemClicked(self, item, column):
        print('TreeCCTVConfig', column, item.text(column))
        
    def TreeIntersectionConfig_ItemClicked(self, item, column):
        print('TreeIntersectionConfig', column, item.text(column))
    
    def ChkShowRoadId_StateChanged(self):
        
        self.roadFlagByte = RoadFlag.NoFlag

        if self.chkShowRoadId.isChecked():
            self.roadFlagByte = self.roadFlagByte | RoadFlag.Road
          
        if self.chkShowLinkId.isChecked():
            self.roadFlagByte = self.roadFlagByte | RoadFlag.Link
            
        if self.chkShowLaneId.isChecked():
            self.roadFlagByte = self.roadFlagByte | RoadFlag.Lane
        
        if self.image:
            self.image.roadFlagByte = self.roadFlagByte
            self.SetSilder()
    
    def __ResetImage(self):
        if self.cctvImagePath != '':
            if len(self.imagePathList) > 1:
                for p in self.imagePathList:
                    if p != self.cctvImagePath:
                        if os.path.exists(p):
                          os.remove(p)
                          
                self.imagePathList = self.GetImagePathList(self.cctvImagePath)
                self.SetImageNr(self.imagePathList)
        
                self.OpenImage(self.imagePathList[0])
                
    def GetImagePathList(self, cctvImagePath):

        self.cctvImagePath = cctvImagePath
        
        cctvImageDir = ''
        
        if os.path.isfile(cctvImagePath):
            cctvImageDir = os.path.dirname(cctvImagePath)
        else:
            cctvImageDir = cctvImagePath
        
        #cctvImageDir = os.path.join(cctvImageDir, '*.png')
        #matchedPng = glob.glob(cctvImageDir)
        

        cctvImageDir = os.path.join(cctvImageDir, 'screenshot')

        imageHelper = ImageHelper(cctvImagePath, cctvImageDir)
        imgList = imageHelper.getImgList()
        
        if len(imgList) == 0:
            imgList = [cctvImagePath]
            
        return imgList
    
    def SetImageNr(self, imagePathList):
        imageNr = len(imagePathList)
        self.hsldNr.setMaximum(imageNr)
        self.hsldNr.setValue(1)
        self.spbNr.setMaximum(imageNr)
        self.spbNr.setValue(1)
        
    def OpenImages(self, fileDict):
        
        self.imagePathList = self.GetImagePathList(fileDict['CCTVImage'])
        self.SetImageNr(self.imagePathList)
        
        self.OpenImage(self.imagePathList[0])
        self.OpenIllustrationImage(fileDict['Illustration'])
        
        self.intersectionConfig.loadXml(fileDict['IntersectionConfiguration'])
        self.intersectionConfig.showInTree(self.treeIntersectionConfig)
        
        if fileDict['CCTVConfiguration'] != '':
            if os.path.exists(fileDict['CCTVConfiguration']):
                self.cctvConfig.loadXmlFile(fileDict['CCTVConfiguration'])
            else:
                print('The specified CCTV configuration file is not existent: {0}'.format(fileDict['CCTVConfiguration']))
                print('Create empty one through the intersection configuration file.')
                self.cctvConfig = self.intersectionConfig.toCCTVConfiguration()
                self.cctvConfig.xmlPath = fileDict['CCTVConfiguration']
        else:
            print('No specified CCTV configuration file.')
            print('Create empty one through the intersection configuration file.')
            self.cctvConfig = self.intersectionConfig.toCCTVConfiguration()
            self.cctvConfig.xmlPath = ''
        
        self.__refreshCCTVConfigAndLabel(self.cctvConfig)
     
    def ChangeImage(self):
        imageNr = self.hsldNr.value() - 1
        if imageNr in range(len(self.imagePathList)):
            imagePath = self.imagePathList[imageNr]
            self.imagePath = imagePath
            self.image.setImage(imagePath)
            self.SetSilder()
        
    def OpenImage(self, imagePath):
        
        if self.image:
            self.image._widget = None
            self.image._mouseMoveEvent.disconnect(self.Image_MouseMove)
            self.image._labelChangedEvent.disconnect(self.Label_Changed)
            self.image._labelSelectedEvent.disconnect(self.Label_Selected)   
            del self.image

        self.imagePath = imagePath
        self.image = Image(self.lblImage, imagePath, True)
        self.image._mouseMoveEvent.connect(self.Image_MouseMove)
        self.image._labelChangedEvent.connect(self.Label_Changed)
        self.image._labelSelectedEvent.connect(self.Label_Selected)
        self.image.roadFlagByte = self.roadFlagByte
        self.SetSilder()
    
    def OpenIllustrationImage(self, imagePath):
        
        if self.illustrationImage:
            self.illustrationImage._widget = None           
            del self.illustrationImage
            
        self.illustrationImage = Image(self.lblIllustrationImage, imagePath, False)
        self.illustrationImage.ScaleImage()
            
    @QtCore.pyqtSlot(QtCore.QPoint)
    def Image_MouseMove(self, pos):
        #print('X: {0}; Y {1}'.format(pos.x(), pos.y()))
        self.lblCoordinate.setText('X: {0}; Y {1}'.format(pos.x(), pos.y()))
        
    @QtCore.pyqtSlot(list)
    def Label_Changed(self, labels):
        
        self.refreshRoadTable = True
        self.refreshLaneTable = True        
        
        for label in labels:

            if label.roadType == RoadType.Road:

                roadIdx = label.roadIdx
                
                p1, p2 = label.getPoints()
                road = self.cctvConfig.virtualGate.roads[roadIdx]
                
                road.position1.x = str(p1.x())
                road.position1.y = str(p1.y())
                road.position2.x = str(p2.x())
                road.position2.y = str(p2.y())
                
                self.tblRoad.item(roadIdx, 3).setText(road.position1.x)
                self.tblRoad.item(roadIdx, 4).setText(road.position1.y)
                self.tblRoad.item(roadIdx, 5).setText(road.position2.x)
                self.tblRoad.item(roadIdx, 6).setText(road.position2.y)	

            elif label.roadType == RoadType.Lane:
                
                (roadIdx, laneIdx) = label.roadIdx
                
                p1, p2 = label.getPoints()
                lane = self.cctvConfig.virtualGate.roads[roadIdx].lanes[laneIdx]
                
                lane.position1.x = str(p1.x())
                lane.position1.y = str(p1.y())
                lane.position2.x = str(p2.x())
                lane.position2.y = str(p2.y()) 
                
                if self.keepRoadIdxOfLanes == roadIdx:
                    
                    self.tblLane.item(laneIdx, 5).setText(lane.position1.x)
                    self.tblLane.item(laneIdx, 6).setText(lane.position1.y)
                    self.tblLane.item(laneIdx, 7).setText(lane.position2.x)
                    self.tblLane.item(laneIdx, 8).setText(lane.position2.y) 

        #self.__refreshCCTVConfigAndLabel(self.cctvConfig)
        
        self.refreshRoadTable = False
        self.refreshLaneTable = False        
        
    @QtCore.pyqtSlot(Label)
    def Label_Selected(self, label):
        
        self.tabCCTVConfiguration.setCurrentIndex(1)
        
        roadIdx = -1
        laneIdx = -1
        
        if label.roadType == RoadType.Road:
            roadIdx = label.roadIdx
        elif label.roadType == RoadType.Lane:
            (roadIdx, laneIdx) = label.roadIdx
            
        if roadIdx > -1:
            item = self.tblRoad.item(roadIdx, 0)
            self.tblRoad.setCurrentItem(item)
            
        if laneIdx > -1:
            item = self.tblLane.item(laneIdx, 0)
            self.tblLane.setCurrentItem(item)
        
        #print('itemKey', roadIdx, laneIdx)

        
    def DockImage(self):
        #print('DockImage', self.init)
        if self.image:
            
            if self.init:
                rectWidth, rectHeight = self.lblImage.width(), self.lblImage.height()
            else:
                rectWidth, rectHeight = self.scrollArea.width() - 9, self.scrollArea.height() - 18
               
            imageSize = self.image.size()
            imgWidth, imgHeight = imageSize.width(), imageSize.height()
            ratioWidth, ratioHeight = rectWidth / imgWidth, rectHeight / imgHeight

            scaling = max(int(min(ratioWidth, ratioHeight) * self._SCALING_BASE), self._SCALING_MIN)
            self.hsldScaling.setValue(scaling)
            
    def SetSilder(self):
        #print('SetSilder')
        if self.image:
            scaling = self.hsldScaling.value()
            self.image.ScaleImage(scaling)
        
    def __refreshCCTVConfigAndLabel(self, cctvConfig):
        self.__ShowConfig(cctvConfig)
        self.image.labels = self.__cctvConfig2Label(cctvConfig)
        #self.Label_Changed(self.image.labels)
        self.SetSilder() 
        
        
    def __cctvConfig2Label(self, cctvConfig):
        
        labels = []
        for roadIdx, road in enumerate(cctvConfig.virtualGate.roads):
            p1, p2 = road.position1, road.position2
            labels.append(self.image.newLabel(p1.toQPoint(), p2.toQPoint(), RoadType.Road, roadIdx, (road.road_id, road.link_id)))
            
            
            for laneIdx, lane in enumerate(road.lanes):
                p1, p2 = lane.position1, lane.position2
                labels.append(self.image.newLabel(p1.toQPoint(), p2.toQPoint(), RoadType.Lane, (roadIdx, laneIdx), lane.lane_id))
                
        return labels
    
    def __initialTableHeader(self):
        
        header = ['img_x', 'img_y', 'lat', 'lng', 'refIdx']
        self.tblReferencePoints.setColumnCount(self._TABLE_COLUMNS_REFERENCE_POINTS)
        self.tblReferencePoints.setHorizontalHeaderLabels(header)
        self.tblReferencePoints.hideColumn(4)
        
        header = ['road_id', 'link_id', 'direction', 'x1', 'y1', 'x2', 'y2', 'roadIdx']
        self.tblRoad.setColumnCount(self._TABLE_COLUMNS_ROAD)
        self.tblRoad.setHorizontalHeaderLabels(header)
        
        self.tblRoad.hideColumn(7)
        header = ['lane_id', 'Left Turn', 'U Turn', 'Right Turn', 'Straight', 'x1', 'y1', 'x2', 'y2', 'roadIdx', 'laneIdx']
        
        self.tblLane.setColumnCount(self._TABLE_COLUMNS_LANE)
        self.tblLane.setHorizontalHeaderLabels(header)
        
        self.tblLane.hideColumn(9)
        self.tblLane.hideColumn(10)        
        
    def __ShowConfig(self, cctvConfig):
        
        self.refreshRoadTable = True
        self.refreshLaneTable = True
        
        self.tblReferencePoints.setRowCount(0)
        self.tblRoad.setRowCount(0)
        self.tblLane.setRowCount(0)
        
        header = cctvConfig.header
        
        self.txtCCTV.setText(header.cctv)
        self.txtVersion.setText(header.version)
        self.txtDate.setText(header.date)
        self.txtIntersectionId.setText(header.intersection_id)
        self.txtDeviceIp.setText(header.device_ip)
        self.txtCameraPositionLat.setText(header.camera_position.latitude)
        self.txtCameraPositionLng.setText(header.camera_position.longitude)
        
        roadInfo = cctvConfig.roadInfo
        refPointList = []
        for idx, ref_point in enumerate(roadInfo.reference_points):
            values = ref_point.getValues()
            values.append(str(idx))
            refPointList.append(values)
        self.__AddTblReferencePointsRow(refPointList)
        
        
        virtualGate = cctvConfig.virtualGate
        roadList = []
        for idx, road in enumerate(virtualGate.roads):
            values = road.getValues()
            values.append(str(idx))
            roadList.append(values)
        self.__AddTblRoadRow(roadList)
        
        
        self.refreshRoadTable = False
        self.refreshLaneTable = False        
        
    def __AddTableRow(self, tbl, contents):
        addedRowIdx = []
        rowNum = len(contents)
        if rowNum > 0:
            columnNum = len(contents[0])
            for rIdx in range(rowNum):
                row_count = tbl.rowCount()
                tbl.insertRow(row_count)
                row = contents[rIdx]
                for cIdx in range(columnNum):
                    item = QtWidgets.QTableWidgetItem(row[cIdx])
                    item.setTextAlignment(QtCore.Qt.AlignRight)
                    tbl.setItem(row_count, cIdx, item)
                addedRowIdx.append(row_count)
        return addedRowIdx
                    
    def __AddTblReferencePointsRow(self, contents):
        self.__AddTableRow(self.tblReferencePoints, contents)
    
    def __AddTblRoadRow(self, contents):
        addedRowIdx = self.__AddTableRow(self.tblRoad, contents)
        
        cboList = ['In', 'Out']
        
        for rowIdx in addedRowIdx:
            item = self.tblRoad.item(rowIdx, 2)
            cbobox = QtWidgets.QComboBox()
            cbobox.addItems(cboList)
            
            idx = cbobox.findText(item.text(), QtCore.Qt.MatchFixedString)
            if idx < 0:
                idx = 0
                
            cbobox.setCurrentIndex(idx)
            cbobox.setProperty('row', rowIdx)
            cbobox.setProperty('col', 2)
            cbobox.currentIndexChanged.connect(self.__tblRoadDirectionIndexChanged)
            self.tblRoad.setCellWidget(rowIdx, 2, cbobox)
    
    #def __tblRoadDirectionIndexChanged(self, index):
    def __tblRoadDirectionIndexChanged(self):
        
        cbo = self.sender()
        
        if type(cbo).__name__ == 'QComboBox':
            
            row = cbo.property('row')
            col = cbo.property('col')
            txt = cbo.currentText()
            
            item = self.tblRoad.item(row , col)
            item.setText(txt)

    def __AddTblLaneRow(self, contents):
        addedRowIdx = self.__AddTableRow(self.tblLane, contents)
        
        for rowIdx in addedRowIdx:
            
            for colIdx in [1, 2, 3, 4]:

                cellWidget = QtWidgets.QWidget()
                hBoxLayout = QtWidgets.QHBoxLayout(cellWidget)
                
                chkbox = QtWidgets.QCheckBox()
                
                chkbox.setProperty('row', rowIdx)
                chkbox.setProperty('col', colIdx)
                chkbox.stateChanged.connect(self.__tblLaneForwordDirectionStatusChanged)
                
                hBoxLayout.addWidget(chkbox)
                hBoxLayout.setAlignment(QtCore.Qt.AlignCenter)            
                hBoxLayout.setContentsMargins(0, 0, 0, 0)
                cellWidget.setLayout(hBoxLayout)
    
                self.tblLane.setCellWidget(rowIdx, colIdx, cellWidget)
                
                item = self.tblLane.item(rowIdx, colIdx)
                item.setTextAlignment(QtCore.Qt.AlignCenter)
                
                if item.text() == '1':
                    chkbox.setCheckState(QtCore.Qt.Checked)  
                else:
                    chkbox.setCheckState(QtCore.Qt.Unchecked)  

    def __tblLaneForwordDirectionStatusChanged(self):
        
        chk = self.sender()
        
        if type(chk).__name__ == 'QCheckBox':
        
            row = chk.property('row')
            col = chk.property('col')
            
            #print('tblLaneForwordDirectionStatusChanged: ', row, col)
            
            txt = '0'
            if chk.isChecked():
                txt = '1'
                
            item = self.tblLane.item(row , col)
            item.setText(txt)
                
    def __tblReferencePoints_ItemChanged(self, item):
        self.__tblItemChanged(self.tblReferencePoints, item)

    def __tblRoad_ItemChanged(self, item):
        #print('__tblRoad_ItemChanged')
        self.__tblItemChanged(self.tblRoad, item)
        
        if not self.refreshRoadTable:
            
            row = item.row()
            column = item.column()
                
            self.__RefreshRoads()
            
            if column in [0, 1, 3, 4, 5, 6]:
                roadType = RoadType.Road
                roadIdx = row
                roadId = (self.cctvConfig.virtualGate.roads[roadIdx].road_id, self.cctvConfig.virtualGate.roads[roadIdx].link_id)
                p1 = self.cctvConfig.virtualGate.roads[roadIdx].position1.toQPoint()
                p2 = self.cctvConfig.virtualGate.roads[roadIdx].position2.toQPoint()
                
                self.image.updateLabel(roadType, roadIdx, roadId, p1, p2)

    def __tblLane_ItemChanged(self, item):
        #print('__tblLane_ItemChanged')
        self.__tblItemChanged(self.tblLane, item)
        
        if not self.refreshLaneTable:
            
            row = item.row()
            column = item.column()

            if self.keepRoadIdxOfLanes > -1:
                self.__RefreshLanes(self.keepRoadIdxOfLanes)
                
                if column in [0, 5, 6, 7, 8]:
                    roadType = RoadType.Lane
                    roadIdx = self.keepRoadIdxOfLanes
                    roadId = self.cctvConfig.virtualGate.roads[roadIdx].lanes[row].lane_id
                    p1 = self.cctvConfig.virtualGate.roads[roadIdx].lanes[row].position1.toQPoint()
                    p2 = self.cctvConfig.virtualGate.roads[roadIdx].lanes[row].position2.toQPoint()
                    
                    self.image.updateLabel(roadType, (roadIdx, row), roadId, p1, p2)
        
    def __tblItemChanged(self, tbl, item):
        tbl.resizeRowsToContents()
        tbl.resizeColumnsToContents()
    
    def __tblRoad_ItemSelectionChanged(self):
        #print('__tblRoad_ItemSelectionChanged')
        
        currentRow = self.tblRoad.currentRow()
        
        if currentRow >= 0:
            
            self.refreshLaneTable = True
            
            if self.keepRoadIdxOfLanes > -1:
                self.__RefreshLanes(self.keepRoadIdxOfLanes)
    
            self.tblLane.setRowCount(0)

            self.keepRoadIdxOfLanes = int(self.tblRoad.item(currentRow, self._TABLE_COLUMNS_ROAD - 1).text())
            
            lanes = self.cctvConfig.virtualGate.roads[self.keepRoadIdxOfLanes].lanes
            
            laneList = []
            
            for idx, lane in enumerate(lanes):
                values = lane.getValues()
                values.append(str(self.keepRoadIdxOfLanes))
                values.append(str(idx))
                laneList.append(values)
                
            self.__AddTblLaneRow(laneList)
            
            self.refreshLaneTable = False
            
            if self.__IsNoLabeledRoad(self.keepRoadIdxOfLanes):
                self.image.lockForNewLabel(RoadType.Road, self.keepRoadIdxOfLanes)
        else:
            self.keepRoadIdxOfLanes = -1
            
    def __AddPoint(self):
        
        rowCount = str(self.tblReferencePoints.rowCount())
        cctvRefPoint = CCTVReferencePoint(None)
        values = cctvRefPoint.getValues()
        values.append(rowCount)
        
        self.__AddTblReferencePointsRow([values])
        self.cctvConfig.roadInfo.reference_points.append(cctvRefPoint)

    def __DeletePoint(self):
        self.__DeleteTableRow(self.tblReferencePoints)
        self.__RefreshReferencePoints()
        self.__ShowConfig(self.cctvConfig)
        
    def __AddRoad(self):

        self.refreshRoadTable = True
        self.refreshLaneTable = True
        
        rowCount = str(self.tblRoad.rowCount())
        
        cctvRoad = CCTVRoad(None)
        values = cctvRoad.getValues()
        values.append(rowCount)
        
        self.__AddTblRoadRow([values])
        self.cctvConfig.virtualGate.roads.append(cctvRoad)
        
        self.__refreshCCTVConfigAndLabel(self.cctvConfig)
        
        self.image.lockForNewLabel(RoadType.Road, int(rowCount))

        self.refreshRoadTable = False
        self.refreshLaneTable = False
        
    def __DeleteRoad(self):
        
        self.refreshRoadTable = True
        self.refreshLaneTable = True
        
        self.__DeleteTableRow(self.tblRoad)
        self.__RefreshRoads()
        
        self.__refreshCCTVConfigAndLabel(self.cctvConfig)

        self.refreshRoadTable = False
        self.refreshLaneTable = False
        
    def __IsNoLabeledRoad(self, roadIdx):
        road = self.cctvConfig.virtualGate.roads[roadIdx]
        result = road.position1.hasValue() and road.position2.hasValue()
        return not result
    
    def __IsNoLabeledLane(self, roadIdx, laneIdx):
        lane = self.cctvConfig.virtualGate.roads[roadIdx].lanes[laneIdx]
        result = lane.position1.hasValue() and lane.position2.hasValue()
        return not result
    
    def __tblLane_ItemSelectionChanged(self):
        
        currentRow = self.tblLane.currentRow()
        
        if currentRow >= 0:
            laneIdx = int(self.tblLane.item(currentRow, 10).text())
            if self.__IsNoLabeledLane(self.keepRoadIdxOfLanes, laneIdx):
                self.image.lockForNewLabel(RoadType.Lane, (self.keepRoadIdxOfLanes, laneIdx))
                
    def __AddLane(self):
        
        self.refreshLaneTable = True
        
        rowCount = str(self.tblLane.rowCount())
        
        cctvLane = CCTVLane(None)
        values = cctvLane.getValues()
        values.append(str(self.keepRoadIdxOfLanes))
        values.append(rowCount)
        
        self.__AddTblLaneRow([values])
        self.cctvConfig.virtualGate.roads[self.keepRoadIdxOfLanes].lanes.append(cctvLane)
        
        self.image.labels = self.__cctvConfig2Label(self.cctvConfig)
        self.SetSilder() 
        
        self.image.lockForNewLabel(RoadType.Lane, (self.keepRoadIdxOfLanes, int(rowCount)))
        
        self.refreshLaneTable = False
    def __DeleteLane(self):
        
        self.refreshLaneTable = True
        
        keepRoadIdxOfLanes = self.keepRoadIdxOfLanes
        
        self.__DeleteTableRow(self.tblLane)
        self.__RefreshLanes(keepRoadIdxOfLanes)
        
        self.__refreshCCTVConfigAndLabel(self.cctvConfig)
        
        item = self.tblRoad.item(keepRoadIdxOfLanes, 0)
        self.tblRoad.setCurrentItem(item)
        
        self.refreshLaneTable = False
        
    def __DeleteTableRow(self, tbl):
        selectedRow = tbl.currentRow()
        tbl.removeRow(selectedRow)
        
    def __RefreshHeader(self):
        
        self.cctvConfig.header.cctv = self.txtCCTV.text()
        self.cctvConfig.header.version = self.txtVersion.text()
        self.cctvConfig.header.date = self.txtDate.text()
        self.cctvConfig.header.intersection_id = self.txtIntersectionId.text()
        self.cctvConfig.header.device_ip = self.txtDeviceIp.text()
        self.cctvConfig.header.camera_position.latitude = self.txtCameraPositionLat.text()
        self.cctvConfig.header.camera_position.longitude = self.txtCameraPositionLng.text()
        
    def __RefreshReferencePoints(self):
        
        self.cctvConfig.roadInfo.reference_points.clear()
        
        rowCount = self.tblReferencePoints.rowCount()
        
        for idx in range(rowCount):
            
            ref_point = CCTVReferencePoint(None)
            ref_point.img_position.x = self.tblReferencePoints.item(idx, 0).text()
            ref_point.img_position.y = self.tblReferencePoints.item(idx, 1).text()
            ref_point.geograph_position.latitude = self.tblReferencePoints.item(idx, 2).text()
            ref_point.geograph_position.longitude = self.tblReferencePoints.item(idx, 3).text()
            
            self.cctvConfig.roadInfo.reference_points.append(ref_point)
        
    def __RefreshRoads(self):
        
        keepRoads = copy.deepcopy(self.cctvConfig.virtualGate.roads)
        
        self.cctvConfig.virtualGate.roads.clear()
        
        rowCount = self.tblRoad.rowCount()
        
        for idx in range(rowCount):
            
            cctvRoad = CCTVRoad(None)
            
            cctvRoad.road_id = self.tblRoad.item(idx, 0).text()
            cctvRoad.link_id = self.tblRoad.item(idx, 1).text()
            cctvRoad.direction = self.tblRoad.item(idx, 2).text()
            
            cctvRoad.position1.x = self.tblRoad.item(idx, 3).text()
            cctvRoad.position1.y = self.tblRoad.item(idx, 4).text()
            cctvRoad.position2.x = self.tblRoad.item(idx, 5).text()
            cctvRoad.position2.y = self.tblRoad.item(idx, 6).text()
            
            cctvRoad.lanes = copy.deepcopy(keepRoads[int(self.tblRoad.item(idx, 7).text())].lanes)            
            
            self.cctvConfig.virtualGate.roads.append(cctvRoad)
        
    def __RefreshLanes(self, roadIdx):
        
        if roadIdx >= 0:
            self.cctvConfig.virtualGate.roads[roadIdx].lanes.clear()
            
            rowCount = self.tblLane.rowCount()
            
            for idx in range(rowCount):
                
                cctvLane = CCTVLane(None)
                
                cctvLane.lane_id = self.tblLane.item(idx, 0).text()
                
                cctvLane.leftTurn = self.tblLane.item(idx, 1).text()
                cctvLane.uTurn = self.tblLane.item(idx, 2).text()
                cctvLane.rightTurn = self.tblLane.item(idx, 3).text()
                cctvLane.straight = self.tblLane.item(idx, 4).text()
                
                cctvLane.position1.x = self.tblLane.item(idx, 5).text()
                cctvLane.position1.y = self.tblLane.item(idx, 6).text()
                cctvLane.position2.x = self.tblLane.item(idx, 7).text()
                cctvLane.position2.y = self.tblLane.item(idx, 8).text()
                
                self.cctvConfig.virtualGate.roads[roadIdx].lanes.append(cctvLane)      
                
    def __getResult(self):

        if self.keepRoadIdxOfLanes > -1:
            self.__RefreshLanes(self.keepRoadIdxOfLanes)
        
        self.__RefreshHeader()
        self.__RefreshReferencePoints()
        self.__RefreshRoads()
        
        return self.cctvConfig
              
    def __saveCCTVConfig(self):
        self.cctvConfig.save()