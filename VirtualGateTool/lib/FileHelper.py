import os
import glob

from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import QPoint

import xml.etree.ElementTree as ET
import xmltodict

from enum import Enum
#from enum import IntEnum
#from enum import IntFlag

from VirtualGateTool.label.Label import Label

class OptionType(Enum):
    Open = 0
    Save = 1
    
class FileHelper(QFileDialog):
    
    _DEFAULT_PATH = './'
    
    _DEFAULT_ALL_FILES = '*.*'
    
    _DEFAULT_IMAGE_EXTENSION = ['.png']
    _DEFAULT_LABEL_EXTENSION = ['.xml']
    
    def __init__(self):
        super(FileHelper, self).__init__()
        
        #self.setFileMode(QFileDialog.DirectoryOnly)
        #self.setOption(QFileDialog.DontUseNativeDialog)
        
        self.lastDir = self._DEFAULT_PATH
        return        
    
    def GetFile(self, parent, caption, optionType):
        
        if optionType == OptionType.Open:
            selectedPath = QFileDialog.getOpenFileName(parent, caption, self.lastDir)
        else:
            selectedPath = QFileDialog.getSaveFileName(parent, caption, self.lastDir)
        
        selectedPath = selectedPath[0]
        
        if selectedPath != '':
            self.lastDir = os.path.dirname(selectedPath)
            
        return selectedPath
       
    def WriteFile(self, content, path):
        f = None
        try:
            f = open(path, 'w')
            f.write(content)
        except Exception as ex:
            print('error occured: ', ex)
        finally:
            if f != None:
                f.close()

    
if __name__ == "__main__":
    
    from PyQt5 import QtCore
    from PyQt5.QtWidgets import QWidget
    from PyQt5.QtCore import Qt, QPoint
    from PyQt5.QtGui import QPixmap, QPainter, QPen
    
    xmlFile = 'D:/_Course/Project/LabelTool/data/000000.xml'
    
    fh = FileHelper()
    print(fh.Pxml2Line(xmlFile))
    
    