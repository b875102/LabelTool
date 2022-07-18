# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 21:19:41 2022

@author: HUANG Chun-Huang
"""

from PyQt5 import QtWidgets, uic

from lib.config import Config
from lib.wrpTblStreaming import WrpTblStreaming
from lib.wrpTblEdge import WrpTblEdge

class StreamingManagement(QtWidgets.QDialog):
    
    def __init__(self):
        super(StreamingManagement, self).__init__()
        uic.loadUi('StreamingManagement.ui', self)
        
        self.__config = Config()
        
        self.wrpTblStreaming = WrpTblStreaming(self.tblStreaming, self.__config)
        self.wrpTblEdge = WrpTblEdge(self.tblEdge, self.__config)
        
        self.tabWidget.setCurrentIndex(0)
        
        self.btnStreamingAdd.clicked.connect(self.wrpTblStreaming.AddStreaming)
        self.btnStreamingUpdate.clicked.connect(self.wrpTblStreaming.UpdateStreaming)
        self.btnStreamingDelete.clicked.connect(self.wrpTblStreaming.DeleteStreaming)
        self.btnStreamingSort.clicked.connect(self.wrpTblStreaming.SortStreaming)
        self.btnStreamingApply.clicked.connect(self.wrpTblStreaming.ApplyStreaming)
        self.btnStreamingPreview.clicked.connect(self.wrpTblStreaming.PreviewStreaming)
        self.bbxStreaming.rejected.connect(self.close)
        
        self.btnEdgeAdd.clicked.connect(self.wrpTblEdge.AddEdge)
        self.btnEdgeUpdate.clicked.connect(self.wrpTblEdge.UpdateEdge)
        self.btnEdgeDelete.clicked.connect(self.wrpTblEdge.DeleteEdge)
        self.btnEdgeSort.clicked.connect(self.wrpTblEdge.SortEdge)
        self.btnEdgeApply.clicked.connect(self.wrpTblEdge.ApplyEdge)
        self.btnEdgePreview.clicked.connect(self.wrpTblEdge.PreviewEdge)
        self.bbxEdge.rejected.connect(self.close)
        
    def show(self):
        super().show()

    def close(self):
        self.__config.printConfig()
        #self.__config.save()
        super().close()
        
if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    streamingManagement = StreamingManagement()
    execResult = streamingManagement.exec()
    



    
