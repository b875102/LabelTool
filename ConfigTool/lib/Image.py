# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 19:03:15 2022

@author: HUANG Chun-Huang
"""

from PyQt5 import QtCore

class Image(QtCore.QObject):
    
    _SCALING_BASE = 100
    _SCALING_MIN = 10
    _RND_NO = 2

    def __init__(self, scrWidget, lblWidget, hsldWidget, spbWidget, btnWidget):
        super().__init__(lblWidget)
        
        self.__scrWidget = scrWidget
        self.__lblWidget = lblWidget
        self.__hsldWidget = hsldWidget
        self.__spbWidget = spbWidget
        self.__btnWidget = btnWidget
        
        self.__scalingRatio = 1
        
        self.__hsldWidget.setValue(100)
        self.__spbWidget.setSuffix('%')

        self.__hsldWidget.valueChanged.connect(self.__setSilder)
        self.__btnWidget.clicked.connect(self.__dockImage)
        
        self.pixmap = None
        self.scaledPixmap = None
        self.cloneImage = None
        
    def setImage(self, pixmap):
        
        self.pixmap = pixmap
        self.scaledPixmap = self.pixmap.copy()
        self.cloneImage = self.scaledPixmap.copy()
        self.__setSilder()
        
    def __del__(self):
        pass
    
    @property
    def widget(self):
        return self.__lblWidget
        
    def __scaleImage(self, scaling = _SCALING_BASE):
        
        self.__scalingRatio = round((scaling / self._SCALING_BASE), self._RND_NO)
        
        if self.pixmap:
            
            scaledWidth, scaledHeight = self.pixmap.width() * self.__scalingRatio, self.pixmap.height() * self.__scalingRatio
            self.scaledPixmap = self.pixmap.scaled(scaledWidth, scaledHeight, QtCore.Qt.KeepAspectRatio)
            self.cloneImage = self.scaledPixmap.copy()
            
            self.widget.resize(scaledWidth, scaledHeight)
            self.widget.setPixmap(self.cloneImage)
        
    def size(self):
        return self.pixmap.size()
    
    def __setSilder(self):
        scaling = self.__hsldWidget.value()
        self.__scaleImage(scaling)
        
    def __dockImage(self):

        if self.pixmap:

            rectWidth, rectHeight = self.__scrWidget.width() - 9, self.__scrWidget.height() - 18
            
            imageSize = self.size()
            imgWidth, imgHeight = imageSize.width(), imageSize.height()
            ratioWidth, ratioHeight = rectWidth / imgWidth, rectHeight / imgHeight

            scaling = max(int(min(ratioWidth, ratioHeight) * self._SCALING_BASE), self._SCALING_MIN)
            self.__hsldWidget.setValue(scaling)        