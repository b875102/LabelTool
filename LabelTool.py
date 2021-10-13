import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from Label import Label
from Image import Image
from FileHelper import FileHelper
from OpenFileDialog import OpenFileDialog
from CCTVConfiguration import CCTVConfiguration
from IntersectionConfiguration import IntersectionConfiguration
from CCTVConfigurationDialog import CCTVConfigurationDialog

class LabelTool(QtWidgets.QMainWindow):
    
    _SCALING_BASE = 100
    _SCALING_MIN = 10
    
    def __init__(self):
        super(LabelTool, self).__init__()
        uic.loadUi('LabelTool.ui', self)
        
        self.init = True
        
        #initial components
        
        self.setWindowTitle(self.GetTitle())        
        self.lblCoordinate = QtWidgets.QLabel('')
        self.statusBar().addPermanentWidget(self.lblCoordinate)
        self.openFileDialog = OpenFileDialog(self)
        self.cctvConfigurationDialog = CCTVConfigurationDialog(self)
        
        self.image = None
        self.illustrationImage = None
        
        #event connect
        #Tool Bar
        self.actionOpen_Video.triggered.connect(self.OpenVideo_Click)
        self.actionOpen_Images.triggered.connect(self.OpenImages_Click)
        #self.actionOpen_Images_Patty_Label.triggered.connect(self.OpenImages_Patty_Label_Click)
        
        #Widget
        self.hsldScaling.valueChanged.connect(self.SetSilder)
        self.btnDock.clicked.connect(self.DockImage)
        self.lstFile.itemClicked.connect(self.FileList_Clicked)
        self.treeCCTVConfig.itemClicked.connect(self.TreeCCTVConfig_ItemClicked)
        self.treeIntersectionConfig.itemClicked.connect(self.TreeIntersectionConfig_ItemClicked)
        

        #set attribute
        self.actionOpen_Video.setVisible(False)
        self.actionOpen_Images_Patty_Label.setVisible(False)
        self.spbScaling.setSuffix('%')
        self.hsldScaling.setValue(100)
        self.dwgFileList.close()
        self.dwgLabelList.close()
        
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
        print('OpenImages_Click')
        
        '''
        self.OpenImage('D:/_Course/Project/LabelTool/data/192.168.111.26_園區二路與研發二路球機(12)_道路淨空.png')
        self.OpenIllustrationImage('D:/_Course/Project/LabelTool/data/illustration.png')
        
        self.intersectionConfig.loadXml('D:/_Course/Project/LabelTool/data/Intersection_configuration.xml')
        self.intersectionConfig.showInTree(self.treeIntersectionConfig)
        
        self.cctvConfig.loadXml('D:/_Course/Project/LabelTool/data/cctv_configuration.xml')
        self.cctvConfig.showInTree(self.treeCCTVConfig)
        
        
        self.openFileDialog.txtIllustration.setText('D:/_Course/Project/LabelTool/data/illustration.png')
        self.openFileDialog.txtCCTVImage.setText('D:/_Course/Project/LabelTool/data/192.168.111.26_園區二路與研發二路球機(12)_道路淨空.png')
        self.openFileDialog.txtIntersectionConfiguration.setText('D:/_Course/Project/LabelTool/data/Intersection_configuration.xml')
        self.openFileDialog.txtCCTVConfiguration.setText('D:/_Course/Project/LabelTool/data/cctv_configuration.xml')
        '''
        
        if self.openFileDialog.exec() == QtWidgets.QDialog.Accepted:
            if self.openFileDialog.checkResult():
                
                self.treeCCTVConfig.clear()
                
                print('QDialog.Accepted', self.openFileDialog.getResult())
                dialogResult = self.openFileDialog.getResult()
                
                self.OpenImage(dialogResult['CCTVImage'])
                self.OpenIllustrationImage(dialogResult['Illustration'])
                
                self.intersectionConfig.loadXml(dialogResult['IntersectionConfiguration'])
                self.intersectionConfig.showInTree(self.treeIntersectionConfig)
                
                if dialogResult['CCTVConfiguration'] != '':
                    self.cctvConfig.loadXmlFile(dialogResult['CCTVConfiguration'])
                    self.cctvConfigurationDialog.LoadCCTVConfig(self.cctvConfig)
                else:
                    self.cctvConfigurationDialog.LoadIntersectionConfig(self.intersectionConfig)
                    
                execResult = self.cctvConfigurationDialog.exec()
                
                self.cctvConfig = self.cctvConfigurationDialog.GetResult(execResult)
                self.cctvConfig.showInTree(self.treeCCTVConfig)
                
                labels = []
                for roadIdx, road in enumerate(self.cctvConfig.virtualGate.roads):
                    p1, p2 = road.position1, road.position2
                    
                    if p1.hasValue() and p2.hasValue:
                        labels.append(Label(p1.toQPoint(), p2.toQPoint(), roadIdx))
                        
                    for laneIdx, lane in enumerate(road.lanes):
                        p1, p2 = lane.position1, lane.position2
                        
                        if p1.hasValue() and p2.hasValue:
                            labels.append(Label(p1.toQPoint(), p2.toQPoint(), roadIdx, laneIdx))
                    
                self.image.labels = labels
                self.Label_Changed(self.image.labels)
                self.SetSilder()                    
                
            else:
                print('QDialog.Invalid')
        else:
            print('QDialog.Rejected')
        

    
    def OpenImages_Patty_Label_Click(self):
        self.pngfiles = self.fileHelper.GetFilesP(self, 'Open Images (Patty Label)')
        self.LoadImages(self.pngfiles)
    
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
            print(label.toString())
        
    @QtCore.pyqtSlot(Label)
    def Label_Selected(self, label):
        #print('Label_Selected', label.toString())
        #print('Label_Selected', label.roadIdx, label.laneIdx)
        
        roadIdx = label.roadIdx
        laneIdx = label.laneIdx
        
        itemKey = ''
        try:
            if roadIdx > -1 and laneIdx > -1:
                itemKey = 'Road_{0}_itemLanes_lane_{1}_position'.format(roadIdx, laneIdx)
        except:
            try:
                if roadIdx > -1:
                    itemKey = 'Road_{0}_position'.format(roadIdx)
            except:
                pass
        
        print('itemKey', roadIdx, laneIdx, itemKey)
        
        if itemKey != '':
            item = self.cctvConfig.virtualGate.treeItems[itemKey]
            #item.setSelected(True)
            #self.treeCCTVConfig.itemClicked(item, 0)
            #self.treeCCTVConfig.scrollToItem(item)
            self.treeCCTVConfig.setCurrentItem(item, 0)

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
        
