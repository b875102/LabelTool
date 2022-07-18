from PyQt5 import QtCore, QtWidgets, uic, QtGui
from VirtualGateTool.lib.FileHelper import FileHelper
from VirtualGateTool.lib.FileHelper import OptionType
from VirtualGateTool.lib.TextEdit import TextEdit

class OpenFileDialog(QtWidgets.QDialog):
    
    _SCALING_BASE = 100
    _SCALING_MIN = 10
    
    def __init__(self, parent = None):
        super(OpenFileDialog, self).__init__(None, QtCore.Qt.WindowStaysOnTopHint)
        uic.loadUi('VirtualGateTool/lib/OpenFileDialog.ui', self)
        
        self.fileHelper = FileHelper()
        
        #event connect
        self.btnIllustration.clicked.connect(self.btnIllustration_Click)
        self.btnCCTVImage.clicked.connect(self.btnCCTVImage_Click)
        self.btnIntersectionConfiguration.clicked.connect(self.btnIntersectionConfiguration_Click)
        self.btnCCTVConfiguration.clicked.connect(self.btnCCTVConfiguration_Click)
        
        self._txtIllustration = TextEdit(self.txtIllustration)
        self._txtCCTVImage = TextEdit(self.txtCCTVImage)
        self._txtIntersectionConfiguration = TextEdit(self.txtIntersectionConfiguration)
        self._txtCCTVConfiguration = TextEdit(self.txtCCTVConfiguration)
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)        
        

    def show(self):
        super().show()
        
    def btnIllustration_Click(self):
        fileName = self.fileHelper.GetFile(self, 'Open Illustration Image', OptionType.Open)
        self.txtIllustration.setText(fileName)

    def btnCCTVImage_Click(self):
        fileName = self.fileHelper.GetFile(self, 'Open CCTV Image', OptionType.Open)
        self.txtCCTVImage.setText(fileName)
    
    def btnIntersectionConfiguration_Click(self):
        fileName = self.fileHelper.GetFile(self, 'Open Intersection Configuration', OptionType.Open)
        self.txtIntersectionConfiguration.setText(fileName)
        
    def btnCCTVConfiguration_Click(self):
        fileName = self.fileHelper.GetFile(self, 'Open CCTV Configuration', OptionType.Open)
        self.txtCCTVConfiguration.setText(fileName)
        
    def checkResult(self):
        return (self.txtIllustration.text() != '') and (self.txtIntersectionConfiguration.text() != '') and (self.txtCCTVImage.text() != '')
        
        
    def getResult(self):
        result = {'Illustration': self.txtIllustration.text(), 
                  'CCTVImage': self.txtCCTVImage.text(),
                  'IntersectionConfiguration': self.txtIntersectionConfiguration.text(),
                  'CCTVConfiguration': self.txtCCTVConfiguration.text()}
        
        return result
