import os
import glob

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QPoint

import xml.etree.ElementTree as ET
import xmltodict

from Label import Label


class FileHelper(QFileDialog):
    
    _DEFAULT_PATH = './'
    
    _DEFAULT_ALL_FILES = '*.*'
    
    _DEFAULT_IMAGE_EXTENSION = ['.png']
    _DEFAULT_LABEL_EXTENSION = ['.xml']
    
    #DEFAULT_FILE_TYPE = 'Image Files (*.png *.jpg *.bmp)'
    #_DEFAULT_FILE_TYPE = 'Image Files (*.*)'
    
    def __init__(self):
        super(FileHelper, self).__init__()
        
        #self.setFileMode(QFileDialog.DirectoryOnly)
        #self.setOption(QFileDialog.DontUseNativeDialog)
        
        self.lastDir = self._DEFAULT_PATH
        return        
        
    def _GetFiles(self, parent, caption, fp):
        selectedPath = QFileDialog.getExistingDirectory(parent, caption, self.lastDir)
        #selectedPath = self.getOpenFileName(parent, caption, self.lastDir, self._DEFAULT_FILE_TYPE);
        
        pngfiles = {}
        
        if selectedPath:
            self.lastDir = selectedPath
            
            selectedPath = os.path.join(selectedPath, self._DEFAULT_ALL_FILES)
            for path in glob.glob(selectedPath):
                filename, file_extension = os.path.splitext(path)
                if file_extension.lower() in self._DEFAULT_IMAGE_EXTENSION:
                    xmlFileName = filename + '.xml'
                    labels = []
                    if os.path.exists(xmlFileName):
                        labels = fp(xmlFileName)
                    
                    pngfiles[path] = [xmlFileName, labels]
                    
        return pngfiles
        
    def GetFiles(self, parent, caption):
        pngfiles = self._GetFiles(parent, caption, self.Xml2Line)
        return pngfiles
    
    def GetFilesP(self, parent, caption):
        pngfiles = self._GetFiles(parent, caption, self.Pxml2Line)
        return pngfiles
    
    def Xml2Line(self, xmlFile):
        pass
    
    def Pxml2Line(self, xmlFile):
        xmlContent = open(xmlFile).read()
        xmlDict = xmltodict.parse(xmlContent)
        
        lineDictList = xmlDict['annotation']['object']
        
        labels = []
        
        for lineDict in lineDictList:
            if lineDict['state'] == 'static':
                if (lineDict['type'] == 'Parallel line set (horizontal)') or (lineDict['type'] == 'Vertical line'):
                    coordinate = lineDict['coordinate']
                    
                    p1 = QPoint(self.C2Int(coordinate['x1']), self.C2Int(coordinate['y1']))
                    p2 = QPoint(self.C2Int(coordinate['x2']), self.C2Int(coordinate['y2']))
                    
                    labels.append(Label(p1, p2))
        return labels
        
    def C2Int(self, c):
        return int(float(c))
    
if __name__ == "__main__":
    
    from PyQt5 import QtCore
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtCore import Qt, QPoint
    from PyQt5.QtGui import QPixmap, QPainter, QPen
    
    xmlFile = 'D:/_Course/Project/LabelTool/data/000000.xml'
    
    fh = FileHelper()
    print(fh.Pxml2Line(xmlFile))
    
    