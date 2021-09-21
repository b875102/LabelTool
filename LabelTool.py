import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

from Image import Image
from FileHelper import FileHelper

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
        self.image = None
        
        #event connect
        #Tool Bar
        self.actionOpen_Video.triggered.connect(self.OpenVideo_Click)
        self.actionOpen_Images.triggered.connect(self.OpenImages_Click)
        self.actionOpen_Images_Patty_Label.triggered.connect(self.OpenImages_Patty_Label_Click)
        
        #Widget
        self.hsldScaling.valueChanged.connect(self.SetSilder)
        self.btnDock.clicked.connect(self.DockImage)
        self.lstFile.itemClicked.connect(self.FileList_Clicked)
        

        #set attribute
        self.spbScaling.setSuffix('%')
        self.hsldScaling.setValue(100)
        
        self.imagePath = ''
        #self.imagePath = 'data/counting_example_cam_5_1min.mp4_000000001.png'        
        self.pngfiles = {}
        
        #default action
        #self.OpenImage(self.imagePath)
        #self.DockImage()
        
        #libs
        self.fileHelper = FileHelper()
        
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
        pass
    
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
            del self.image

        self.imagePath = imagePath
        self.image = Image(self.lblImage, imagePath)
        self.image._mouseMoveEvent.connect(self.Image_MouseMove)
        self.image._labelChangedEvent.connect(self.Label_Changed)
        self.SetSilder()
        
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
        
