from PyQt5 import QtCore, QtWidgets, uic, QtGui
import copy

from CCTVConfiguration import CCTVConfiguration
from CCTVConfiguration import Header as CCTVHeader
from CCTVConfiguration import RoadInfo as CCTVRoadInfo
from CCTVConfiguration import VirtualGate as CCTVVirtualGate
from CCTVConfiguration import Road as CCTVRoad
from CCTVConfiguration import Lane as CCTVLane
from CCTVConfiguration import ReferencePoint as CCTVReferencePoint

#from FileHelper import FileHelper
#from TextEdit import TextEdit

class CCTVConfigurationDialog(QtWidgets.QDialog):

    _TABLE_COLUMNS_REFERENCE_POINTS = 4 + 1
    _TABLE_COLUMNS_ROAD = 9 + 1
    _TABLE_COLUMNS_LANE = 5 + 2
    
    _DEFAULT_VALUE_CELL = '0'
    
    def __init__(self, parent = None):
        super(CCTVConfigurationDialog, self).__init__(None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi('CCTVConfigurationDialog.ui', self)
        
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
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)  
        
        self.config = None
        self.tempConfig = None
        
        self.keepRoadIdxOfLanes = -1
        
    def show(self):
        super().show()

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
        
    def __tblReferencePoints_ItemChanged(self, item):
        self.__tblItemChanged(self.tblReferencePoints, item)

    def __tblRoad_ItemChanged(self, item):
        #self.tblRoad.sortItems(0, QtCore.Qt.AscendingOrder)
        self.__tblItemChanged(self.tblRoad, item)
        
    def __tblLane_ItemChanged(self, item):
        #self.tblLane.sortItems(0, QtCore.Qt.AscendingOrder)
        self.__tblItemChanged(self.tblLane, item)
        
        '''
        if self.keepRoadIdxOfLanes > -1:
            self.__RefreshLanes(self.keepRoadIdxOfLanes)
        '''
        
    def __tblItemChanged(self, tbl, item):
        '''  
        row = item.row()
        col = item.column()
        print('tblReferencePoints_ItemChanged ', row, col)
        '''
        
        tbl.resizeRowsToContents()
        tbl.resizeColumnsToContents()
    
    '''
    def __tblRoad_CurrentItemChanged(self, current, previous):
        self.__tblCurrentItemChanged(self.tblRoad, current, previous)
        
    def __tblCurrentItemChanged(self, tbl, current, previous):
        #print('tblCurrentItemChanged')
        pass
    '''
    
    def __tblRoad_ItemSelectionChanged(self):
        
        currentRow = self.tblRoad.currentRow()
        
        if currentRow >= 0:
            
            if self.keepRoadIdxOfLanes > -1:
                self.__RefreshLanes(self.keepRoadIdxOfLanes)
    
            self.tblLane.setRowCount(0)

            self.keepRoadIdxOfLanes = int(self.tblRoad.item(currentRow, self._TABLE_COLUMNS_ROAD - 1).text())
            
            lanes = self.tempConfig.virtualGate.roads[self.keepRoadIdxOfLanes].lanes
            
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
        self.tempConfig.roadInfo.reference_points.append(cctvRefPoint)

    def __DeletePoint(self):
        self.__DeleteTableRow(self.tblReferencePoints)
        self.__RefreshReferencePoints()
        self.__ShowConfig(self.tempConfig)
        
    def __AddRoad(self):
        
        rowCount = str(self.tblRoad.rowCount())
        
        cctvRoad = CCTVRoad(None)
        #cctvRoad.road_id = rowCount
        values = cctvRoad.getValues()
        #values[0] = rowCount
        values.append(rowCount)
        
        self.__AddTableRow(self.tblRoad, [values])
        self.tempConfig.virtualGate.roads.append(cctvRoad)
        
    def __DeleteRoad(self):
        self.__DeleteTableRow(self.tblRoad)
        self.__RefreshRoads()
        self.__ShowConfig(self.tempConfig)
        
    def __AddLane(self):
        
        rowCount = str(self.tblLane.rowCount())
        
        cctvLane = CCTVLane(None)
        #cctvLane.lane_id = rowCount
        values = cctvLane.getValues()
        #values[0] = rowCount
        values.append(str(self.keepRoadIdxOfLanes))
        values.append(rowCount)
        
        self.__AddTableRow(self.tblLane, [values])
        self.tempConfig.virtualGate.roads[self.keepRoadIdxOfLanes].lanes.append(cctvLane)
        
    def __DeleteLane(self):
        self.__DeleteTableRow(self.tblLane)
    
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
        
        self.tempConfig.header.cctv = self.txtCCTV.text()
        #self.tempConfig.header.name = safeNodeText(header.find('name'))
        self.tempConfig.header.version = self.txtVersion.text()
        self.tempConfig.header.date = self.txtDate.text()
        self.tempConfig.header.intersection_id = self.txtIntersectionId.text()
        self.tempConfig.header.device_ip = self.txtDeviceIp.text()
        self.tempConfig.header.camera_position.latitude = self.txtCameraPositionLat.text()
        self.tempConfig.header.camera_position.longitude = self.txtCameraPositionLng.text()
        
    def __RefreshReferencePoints(self):
        
        self.tempConfig.roadInfo.reference_points.clear()
        
        rowCount = self.tblReferencePoints.rowCount()
        
        for idx in range(rowCount):
            
            ref_point = CCTVReferencePoint(None)
            ref_point.img_position.x = self.tblReferencePoints.item(idx, 0).text()
            ref_point.img_position.y = self.tblReferencePoints.item(idx, 1).text()
            ref_point.geograph_position.latitude = self.tblReferencePoints.item(idx, 2).text()
            ref_point.geograph_position.longitude = self.tblReferencePoints.item(idx, 3).text()
            
            self.tempConfig.roadInfo.reference_points.append(ref_point)
        
    def __RefreshRoads(self):
        
        keepRoads = copy.deepcopy(self.tempConfig.virtualGate.roads)
        
        self.tempConfig.virtualGate.roads.clear()
        
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
            
            self.tempConfig.virtualGate.roads.append(cctvRoad)
        
    def __RefreshLanes(self, roadIdx):
        
        if roadIdx >= 0:
            self.tempConfig.virtualGate.roads[roadIdx].lanes.clear()
            
            rowCount = self.tblLane.rowCount()
            
            for idx in range(rowCount):
                
                cctvLane = CCTVLane(None)
                cctvLane.lane_id = self.tblLane.item(idx, 0).text()
                cctvLane.position1.x = self.tblLane.item(idx, 1).text()
                cctvLane.position1.y = self.tblLane.item(idx, 2).text()
                cctvLane.position2.x = self.tblLane.item(idx, 3).text()
                cctvLane.position2.y = self.tblLane.item(idx, 4).text()
                
                self.tempConfig.virtualGate.roads[roadIdx].lanes.append(cctvLane)
    
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
        
    def LoadCCTVConfig(self, cctvConfig):
        
        self.config = cctvConfig
        self.tempConfig = copy.deepcopy(self.config)
        self.__ShowConfig(self.config)

    def LoadIntersectionConfig(self, intersectionConfig):
        
        cctvHeader = CCTVHeader(None)
        cctvRoadInfo = CCTVRoadInfo(None)
        cctvVirtualGate = CCTVVirtualGate(None)
        
        intersectionHeader = intersectionConfig.getHeader()
        
        cctvHeader.name = intersectionHeader.name
        cctvHeader.version = intersectionHeader.version
        cctvHeader.date = intersectionHeader.date
        cctvHeader.intersection_id = intersectionHeader.intersection_id
        
        intersectionRoad = intersectionConfig.getRoadInfo()
        
        
        for idxRoad, isRoad in enumerate(intersectionRoad.roads):
            
            cctvRoad = CCTVRoad(None)
            
            cctvRoad.road_id = str(idxRoad)
            cctvRoad.link_id = isRoad.link_id
            cctvRoad.name = isRoad.name
            cctvRoad.direction = isRoad.direction
            cctvRoad.section = isRoad.section
            
            #cctvRoad.position1 = PointPosition()
            #cctvRoad.position2 = PointPosition()
        
            for idxLane in range(int(isRoad.lane_num)):
                
                lane = CCTVLane(None)
                lane.lane_id = str(idxLane)
                cctvRoad.lanes.append(lane)
            
            cctvVirtualGate.roads.append(cctvRoad)

        cctvConfig = CCTVConfiguration()
        cctvConfig.header = cctvHeader
        cctvConfig.roadInfo = cctvRoadInfo
        cctvConfig.virtualGate = cctvVirtualGate
        self.LoadCCTVConfig(cctvConfig)

    def GetResult(self, execResult):
        
        if execResult == QtWidgets.QDialog.Accepted:
            
            if self.keepRoadIdxOfLanes > -1:
                self.__RefreshLanes(self.keepRoadIdxOfLanes)
            
            self.__RefreshHeader()
            self.__RefreshReferencePoints()
            self.__RefreshRoads()
            
            return self.tempConfig
        else:
            return self.config
        
if __name__ == "__main__":
    
    import sys
    from CCTVConfiguration import CCTVConfiguration
    from IntersectionConfiguration import IntersectionConfiguration

    app = QtWidgets.QApplication(sys.argv)
    dialog = CCTVConfigurationDialog()
    
    
    cctvConfig = CCTVConfiguration('D:/_Course/Project/LabelTool/data/cctv_configuration.xml')
    dialog.LoadCCTVConfig(cctvConfig)
    
    '''
    intersectionConfig = IntersectionConfiguration('D:/_Course/Project/LabelTool/data/Intersection_configuration.xml')
    dialog.LoadIntersectionConfig(intersectionConfig)
    '''
    
    execResult= dialog.exec()
    if execResult == QtWidgets.QDialog.Accepted:
        print('Accepted')
    else:
        print('Rejected')
    
    ''' '''
    config = dialog.GetResult(execResult)
    print(config.header.toXmlString())
    print(config.roadInfo.toXmlString())
    print(config.virtualGate.toXmlString())
    print(config.toXmlString())
    
