# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 14:09:43 2022

@author: HUANG Chun-Huang
"""

import sys

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QDialogButtonBox

from lib.Image import Image
from conf.IntersectionConfiguration import IntersectionConfiguration

class Demo(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Demo, self).__init__()
        uic.loadUi('demo.ui', self)
        
        self.imageSketch = Image(self.scrollArea_2, self.lblSketchImage, self.hsldSScaling, self.spbSScaling, self.btnSDock)
        self.showSketch()
        
        
    def show(self):
        super().show()

    def showSketch(self):
        
        #path = 'D:/_Course/Project/iTraffic/GUI/000北港大橋/IF-065/Intersection_configuration_IF-065.xml'
        path = 'D:/_Course/Project/iTraffic/GUI/000北港大橋/IF-065/Intersection_configuration_IF-065_debug.xml'
        
        intersectionConfiguration = IntersectionConfiguration()
        intersectionConfiguration.loadFile(path)
        
        # or
        #xml = ElementTree.parse(path)
        #intersectionConfiguration.loadXml(xml)
        
        sketch = intersectionConfiguration.toSketch(inTrack = '3001900107078Q', outTrack = '4016400001675Q')
        
        self.imageSketch.setImage(sketch)
        
    
if __name__ == "__main__":
    
    app = QtWidgets.QApplication(sys.argv)
    demo = Demo()
    demo.show()

    sys.exit(app.exec_())