import sys
import copy
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from Label import Label
from Label import RoadType

from Image import Image
from FileHelper import FileHelper
from OpenFileDialog import OpenFileDialog
from CCTVConfiguration import CCTVConfiguration
from IntersectionConfiguration import IntersectionConfiguration
#from CCTVConfigurationDialog import CCTVConfigurationDialog

#from CCTVConfiguration import CCTVConfiguration
#from CCTVConfiguration import Header as CCTVHeader
#from CCTVConfiguration import RoadInfo as CCTVRoadInfo
#from CCTVConfiguration import VirtualGate as CCTVVirtualGate
from CCTVConfiguration import Road as CCTVRoad
from CCTVConfiguration import Lane as CCTVLane
from CCTVConfiguration import ReferencePoint as CCTVReferencePoint

class LabelTool(QtWidgets.QMainWindow):
    
    _SCALING_BASE = 100
    _SCALING_MIN = 10
    
    _TABLE_COLUMNS_REFERENCE_POINTS = 4 + 1
    _TABLE_COLUMNS_ROAD = 9 + 1
    _TABLE_COLUMNS_LANE = 5 + 2
    
    _DEFAULT_VALUE_CELL = '0'
    
    def __init__(self):
        super(LabelTool, self).__init__()
        uic.loadUi('LabelTool2.ui', self)
        
        self.init = True
        
        #initial components
        
        self.setWindowTitle(self.GetTitle())        
        self.lblCoordinate = QtWidgets.QLabel('')
        self.statusBar().addPermanentWidget(self.lblCoordinate)
        self.openFileDialog = OpenFileDialog(self)
        #self.cctvConfigurationDialog = CCTVConfigurationDialog(self)
        
        self.image = None
        self.illustrationImage = None
        
        #event connect
        #Tool Bar
        self.actionOpen_Video.triggered.connect(self.OpenVideo_Click)
        self.actionOpen_Images.triggered.connect(self.OpenImages_Click)
        #self.actionOpen_Images_Patty_Label.triggered.connect(self.OpenImages_Patty_Label_Click)
        self.actionIllustration_Image.triggered.connect(self.Illustration_Image_Click)
        self.actionIntersection_Configuration.triggered.connect(self.Intersection_Configuration_Click)
        self.actionCCTV_Configuration.triggered.connect(self.CCTV_Configuration_Click)
        
        #Widget
        self.hsldScaling.valueChanged.connect(self.SetSilder)
        self.btnDock.clicked.connect(self.DockImage)
        self.lstFile.itemClicked.connect(self.FileList_Clicked)
        self.treeCCTVConfig.itemClicked.connect(self.TreeCCTVConfig_ItemClicked)
        self.treeIntersectionConfig.itemClicked.connect(self.TreeIntersectionConfig_ItemClicked)

        #CCTV Config Widget
        self.__initialTableHeader()
        
        self.tblReferencePoints.itemChanged.connect(self.__tblReferencePoints_ItemChanged)
        
        self.btnAddPoint.clicked.connect(self.__AddPoint)
        self.btnDeletePoint.clicked.connect(self.__DeletePoint)
        
        self.tblRoad.itemChanged.connect(self.__tblRoad_ItemChanged)
        #self.tblRoad.currentItemChanged.connect(self.__tblRoad_CurrentItemChanged)
        self.tblRoad.itemSelectionChanged.connect(self.__tblRoad_ItemSelectionChanged)
        
        self.btnAddRoad.clicked.connect(self.__AddRoad)
        self.btnDeleteRoad.clicked.connect(self.__DeleteRoad)
        
        self.tblLane.itemChanged.connect(self.__tblLane_ItemChanged)
        
        self.btnAddLane.clicked.connect(self.__AddLane)
        self.btnDeleteLane.clicked.connect(self.__DeleteLane)
        
        self.keepRoadIdxOfLanes = -1

        #set attribute
        self.actionOpen_Video.setVisible(False)
        self.actionOpen_Images_Patty_Label.setVisible(False)
        self.spbScaling.setSuffix('%')
        self.hsldScaling.setValue(100)
        self.dwgFileList.close()
        self.dwgLabelList.close()
        self.dwgCCTVConfig.close()
        
        print('sizeHint', self.sizeHint())
        
        self.imagePath = ''
        #self.imagePath = 'data/counting_example_cam_5_1min.mp4_000000001.png'        
        self.pngfiles = {}
        
        #default action
        #self.OpenImage(self.imagePath)
        #self.DockImage()
        
        #libs
        self.fileHelper = FileHelper()
        self.intersectionConfig = IntersectionConfiguration()
        self.cctvConfig = CCTVConfiguration()
        
        #slot
        #self.txtCCTV.setText(self.cctvConfig..textChanged
        
        self.init = False
    def show(self):
        super().show()
        
    
    '''
    def eventFilter(self, source, event):
        print(event.type())
        return super().eventFilter(source, event)
        
    def closeEvent(self, event):
        print('closeEvent')
        
    def mouseDoubleClickEvent(self, event):
        print('mouseDoubleClickEvent')
        
    def mousePressEvent(self, event):
        print('mousePressEvent')
    
    def resizeEvent(self, event):
        #print('resizeEvent')
        self.SetSilder()    
    '''
    def keyPressEvent(self, event):
        #print('mainform keyPressEvent ', event.key())
        if self.image:
            self.image.keyPressEvent(event)
        
    def GetTitle(self, prefix = ''):
        appname = 'LabelTool {0}'
        return appname.format(prefix)
       
    def OpenVideo_Click(self):
        print('OpenVideo_Click')
        pass
    
    def OpenImages_Click(self):
        #print('OpenImages_Click')
        
        ''''''
        self.openFileDialog.txtIllustration.setText('D:/_Course/Project/LabelTool/data/illustration.png')
        self.openFileDialog.txtCCTVImage.setText('D:/_Course/Project/LabelTool/data/192.168.111.26_園區二路與研發二路球機(12)_道路淨空.png')
        self.openFileDialog.txtIntersectionConfiguration.setText('D:/_Course/Project/LabelTool/data/Intersection_configuration.xml')
        self.openFileDialog.txtCCTVConfiguration.setText('D:/_Course/Project/LabelTool/data/cctv_configuration.xml')
        
        
        if self.openFileDialog.exec() == QtWidgets.QDialog.Accepted:
            if self.openFileDialog.checkResult():
                
                self.treeIntersectionConfig.clear()
                self.treeCCTVConfig.clear()
                
                print('QDialog.Accepted', self.openFileDialog.getResult())
                dialogResult = self.openFileDialog.getResult()
                
                self.OpenImages(dialogResult)
            else:
                print('QDialog.Invalid')
        else:
            print('QDialog.Rejected')
        

    
    def OpenImages_Patty_Label_Click(self):
        self.pngfiles = self.fileHelper.GetFilesP(self, 'Open Images (Patty Label)')
        self.LoadImages(self.pngfiles)
    
    def Illustration_Image_Click(self):
        #print('Illustration_Image_Click')
        self.dwgIllustrationImage.show()
    
    def Intersection_Configuration_Click(self):
        #print('Intersection_Configuration_Click')
        self.dwgIntersectionConfiguration.show()
    
    def CCTV_Configuration_Click(self):
        #print('CCTV_Configuration_Click')
        self.dwgCCTVConfiguration.show()
        
    def FileList_Clicked(self, item):
        fileName = item.text()
        if fileName != '':
            if self.imagePath != fileName:
                self.OpenImage(fileName)
                
                if fileName in self.pngfiles:
                    labels = self.pngfiles[fileName][1]
                    self.image.labels = labels
                    self.Label_Changed(self.image.labels)
                    self.SetSilder()
    
    def TreeCCTVConfig_ItemClicked(self, item, column):
        print('TreeCCTVConfig', column, item.text(column))
        
    def TreeIntersectionConfig_ItemClicked(self, item, column):
        print('TreeIntersectionConfig', column, item.text(column))
    
    def LoadImages(self, pngfiles):
        self.lstLabel.clear()
        self.lstFile.clear()
        
        if len(pngfiles) > 0:
            for pngfile in pngfiles:
                self.lstFile.addItem(pngfile)
                print(pngfile)
            
            #self.OpenImage(pngfile)
            item = self.lstFile.item(0)
            self.FileList_Clicked(item)

    def OpenImages(self, fileDict):
        
        self.OpenImage(fileDict['CCTVImage'])
        self.OpenIllustrationImage(fileDict['Illustration'])
        
        self.intersectionConfig.loadXml(fileDict['IntersectionConfiguration'])
        self.intersectionConfig.showInTree(self.treeIntersectionConfig)
        
        if fileDict['CCTVConfiguration'] != '':
            self.cctvConfig.loadXmlFile(fileDict['CCTVConfiguration'])
        else:
            self.cctvConfig = self.intersectionConfig.toCCTVConfiguration()
        
        self.__refreshCCTVConfigAndLabel(self.cctvConfig)
     
    
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
        self.lstLabel.clear()
        for label in labels:
            self.lstLabel.addItem(label.toString())
            #print(label.toString())
            

            if label.roadType == RoadType.Road:

                roadIdx = label.roadIdx
            
                self.cctvConfig.virtualGate.roads[roadIdx].position1.x = str(label.shape.p1.x())
                self.cctvConfig.virtualGate.roads[roadIdx].position1.y = str(label.shape.p1.y())
                self.cctvConfig.virtualGate.roads[roadIdx].position2.x = str(label.shape.p2.x())
                self.cctvConfig.virtualGate.roads[roadIdx].position2.y = str(label.shape.p2.y())
                
                self.tblRoad.item(roadIdx, 5).setText(str(label.shape.p1.x()))
                self.tblRoad.item(roadIdx, 6).setText(str(label.shape.p1.y()))
                self.tblRoad.item(roadIdx, 7).setText(str(label.shape.p2.x()))
                self.tblRoad.item(roadIdx, 8).setText(str(label.shape.p2.y()))
                
            elif label.roadType == RoadType.Lane:
                
                (roadIdx, laneIdx) = label.roadIdx
                
                self.cctvConfig.virtualGate.roads[roadIdx].lanes[laneIdx].position1.x = str(label.shape.p1.x())
                self.cctvConfig.virtualGate.roads[roadIdx].lanes[laneIdx].position1.y = str(label.shape.p1.y())
                self.cctvConfig.virtualGate.roads[roadIdx].lanes[laneIdx].position2.x = str(label.shape.p2.x())
                self.cctvConfig.virtualGate.roads[roadIdx].lanes[laneIdx].position2.y = str(label.shape.p2.y())   
                
                if self.keepRoadIdxOfLanes == roadIdx:

                    self.tblLane.item(laneIdx, 1).setText(str(label.shape.p1.x()))
                    self.tblLane.item(laneIdx, 2).setText(str(label.shape.p1.y()))
                    self.tblLane.item(laneIdx, 3).setText(str(label.shape.p2.x()))
                    self.tblLane.item(laneIdx, 4).setText(str(label.shape.p2.y()))
                
        #self.__refreshCCTVConfigAndLabel(self.cctvConfig)
        
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
            
            #if p1.hasValue() and p2.hasValue:
            labels.append(Label(p1.toQPoint(), p2.toQPoint(), RoadType.Road, roadIdx))
                
            for laneIdx, lane in enumerate(road.lanes):
                p1, p2 = lane.position1, lane.position2
                
                #if p1.hasValue() and p2.hasValue:
                labels.append(Label(p1.toQPoint(), p2.toQPoint(), RoadType.Lane, (roadIdx, laneIdx)))
        return labels
    
    def __initialTableHeader(self):
        
        header = ['img_x', 'img_y', 'lat', 'lng', 'refIdx']
        self.tblReferencePoints.setColumnCount(self._TABLE_COLUMNS_REFERENCE_POINTS)
        self.tblReferencePoints.setHorizontalHeaderLabels(header)
        self.tblReferencePoints.hideColumn(4)
        
        header = ['road_id', 'link_id', 'name', 'direction', 'section', 'x1', 'y1', 'x2', 'y2', 'roadIdx']
        self.tblRoad.setColumnCount(self._TABLE_COLUMNS_ROAD)
        self.tblRoad.setHorizontalHeaderLabels(header)
        self.tblRoad.hideColumn(9)
        
        header = ['lane_id', 'x1', 'y1', 'x2', 'y2', 'roadIdx', 'laneIdx']
        self.tblLane.setColumnCount(self._TABLE_COLUMNS_LANE)
        self.tblLane.setHorizontalHeaderLabels(header)
        self.tblLane.hideColumn(5)
        self.tblLane.hideColumn(6)
        
    def __ShowConfig(self, cctvConfig):
        
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
        self.__AddTableRow(self.tblReferencePoints, refPointList)
        
        virtualGate = cctvConfig.virtualGate
        roadList = []
        for idx, road in enumerate(virtualGate.roads):
            values = road.getValues()
            values.append(str(idx))
            roadList.append(values)
        self.__AddTableRow(self.tblRoad, roadList)
        
    def __AddTableRow(self, tbl, contents):
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

    def __tblReferencePoints_ItemChanged(self, item):
        self.__tblItemChanged(self.tblReferencePoints, item)

    def __tblRoad_ItemChanged(self, item):
        self.__tblItemChanged(self.tblRoad, item)
        
    def __tblLane_ItemChanged(self, item):
        self.__tblItemChanged(self.tblLane, item)
        
    def __tblItemChanged(self, tbl, item):
        tbl.resizeRowsToContents()
        tbl.resizeColumnsToContents()
    
    def __tblRoad_ItemSelectionChanged(self):
        #print('__tblRoad_ItemSelectionChanged')
        
        currentRow = self.tblRoad.currentRow()
        
        if currentRow >= 0:
            
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
                
            self.__AddTableRow(self.tblLane, laneList)
        else:
            self.keepRoadIdxOfLanes = -1
            
    def __AddPoint(self):
        
        rowCount = str(self.tblReferencePoints.rowCount())
        cctvRefPoint = CCTVReferencePoint(None)
        values = cctvRefPoint.getValues()
        values.append(rowCount)
        
        self.__AddTableRow(self.tblReferencePoints, [values])
        self.cctvConfig.roadInfo.reference_points.append(cctvRefPoint)

    def __DeletePoint(self):
        self.__DeleteTableRow(self.tblReferencePoints)
        self.__RefreshReferencePoints()
        self.__ShowConfig(self.cctvConfig)
        
    def __AddRoad(self):
        
        rowCount = str(self.tblRoad.rowCount())
        
        cctvRoad = CCTVRoad(None)
        #cctvRoad.road_id = rowCount
        values = cctvRoad.getValues()
        #values[0] = rowCount
        values.append(rowCount)
        
        self.__AddTableRow(self.tblRoad, [values])
        self.cctvConfig.virtualGate.roads.append(cctvRoad)
        
        self.__refreshCCTVConfigAndLabel(self.cctvConfig)
        
        self.image.lockForNewLabel(RoadType.Road, int(rowCount))
        
    def __DeleteRoad(self):
        self.__DeleteTableRow(self.tblRoad)
        self.__RefreshRoads()
        
        self.__refreshCCTVConfigAndLabel(self.cctvConfig)
        
    def __AddLane(self):
        
        rowCount = str(self.tblLane.rowCount())
        
        cctvLane = CCTVLane(None)
        #cctvLane.lane_id = rowCount
        values = cctvLane.getValues()
        #values[0] = rowCount
        values.append(str(self.keepRoadIdxOfLanes))
        values.append(rowCount)
        
        self.__AddTableRow(self.tblLane, [values])
        self.cctvConfig.virtualGate.roads[self.keepRoadIdxOfLanes].lanes.append(cctvLane)
        
        #self.__refreshCCTVConfigAndLabel(self.cctvConfig)
        self.image.labels = self.__cctvConfig2Label(self.cctvConfig)
        self.SetSilder() 
        
        self.image.lockForNewLabel(RoadType.Lane, (self.keepRoadIdxOfLanes, int(rowCount)))
        
    def __DeleteLane(self):
        self.__DeleteTableRow(self.tblLane)
        
        self.__refreshCCTVConfigAndLabel(self.cctvConfig)
    
    def __AddTableRow(self, tbl, contents):
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
                    
    def __DeleteTableRow(self, tbl):
        selectedRow = tbl.currentRow()
        tbl.removeRow(selectedRow)
        
    def __RefreshHeader(self):
        
        self.cctvConfig.header.cctv = self.txtCCTV.text()
        #self.cctvConfig.header.name = safeNodeText(header.find('name'))
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
            cctvRoad.name = self.tblRoad.item(idx, 2).text()
            cctvRoad.direction = self.tblRoad.item(idx, 3).text()
            cctvRoad.section = self.tblRoad.item(idx, 4).text()
            
            cctvRoad.position1.x = self.tblRoad.item(idx, 5).text()
            cctvRoad.position1.y = self.tblRoad.item(idx, 6).text()
            cctvRoad.position2.x = self.tblRoad.item(idx, 7).text()
            cctvRoad.position2.y = self.tblRoad.item(idx, 8).text()
            
            cctvRoad.lanes = copy.deepcopy(keepRoads[int(self.tblRoad.item(idx, 9).text())].lanes)
            
            self.cctvConfig.virtualGate.roads.append(cctvRoad)
        
    def __RefreshLanes(self, roadIdx):
        
        if roadIdx >= 0:
            self.cctvConfig.virtualGate.roads[roadIdx].lanes.clear()
            
            rowCount = self.tblLane.rowCount()
            
            for idx in range(rowCount):
                
                cctvLane = CCTVLane(None)
                cctvLane.lane_id = self.tblLane.item(idx, 0).text()
                cctvLane.position1.x = self.tblLane.item(idx, 1).text()
                cctvLane.position1.y = self.tblLane.item(idx, 2).text()
                cctvLane.position2.x = self.tblLane.item(idx, 3).text()
                cctvLane.position2.y = self.tblLane.item(idx, 4).text()
                
                self.cctvConfig.virtualGate.roads[roadIdx].lanes.append(cctvLane)      
                
    def GetResult(self):

        if self.keepRoadIdxOfLanes > -1:
            self.__RefreshLanes(self.keepRoadIdxOfLanes)
        
        self.__RefreshHeader()
        self.__RefreshReferencePoints()
        self.__RefreshRoads()
        
        return self.cctvConfig
              