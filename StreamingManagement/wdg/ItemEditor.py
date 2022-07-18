# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 17:21:04 2022

@author: HUANG Chun-Huang
"""

from PyQt5 import QtWidgets, uic

from lib.tblib import Tblib

class ItemEditor(QtWidgets.QDialog, Tblib):
    
    __COL_CONTENT = 0
    __COL_REFIDX = 1
    
    def __init__(self, itemName, contentList, editable = False):
        super(ItemEditor, self).__init__()
        uic.loadUi('wdg/ItemEditor.ui', self)
        
        self.__itemName = itemName
        self.__contentList = contentList
        
        self.setWindowTitle(f'{self.__itemName} Editor')
        
        self.__initHeader(self.__itemName, self.tblContent)
        self.__load(self.__contentList)
        
        self.btnAdd.clicked.connect(self.__Add_Clicked)
        self.btnDelete.clicked.connect(self.__Delete_Clicked)
        self.btnAscent.clicked.connect(self.__Ascent_Clicked)
        self.btnDescent.clicked.connect(self.__Descent_Clicked)
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
         
        self.btnAdd.setVisible(editable)
        self.btnDelete.setVisible(editable)
        self.btnAscent.setVisible(editable)
        self.btnDescent.setVisible(editable)
        
        if not editable:
            self.tblContent.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
    def __initHeader(self, itemName, tbl):
        header = [itemName, 'refIdx']
        tbl.setColumnCount(len(header))
        tbl.setHorizontalHeaderLabels(header)
        tbl.hideColumn(self.__COL_REFIDX)
        tbl.setRowCount(0)
        
        header = tbl.horizontalHeader()       
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        
        
    def __load(self, contentList):
        
        self.__loading = True
        self.tblContent.setRowCount(0)
        contents = []
        
        for idx, content in enumerate(contentList):
            contents.append([content, str(idx)])
            
        self.addRows(self.tblContent, contents)
        self.selectedRow(self.tblContent, 0)
        self.__loading = False        
        
    def __Add_Clicked(self):
        rowCount = str(self.tblContent.rowCount())
        self.addRows(self.tblContent, [['', rowCount]])
        
    def __Delete_Clicked(self):
        self.deleteRow(self.tblContent)
    
    def __Ascent_Clicked(self):
        self.__sortItems(reverse = False)
    
    def __Descent_Clicked(self):
        self.__sortItems(reverse = True)
        
    def __sortItems(self, reverse):
        contentList = self.__getContentList()
        contentList = sorted(contentList, reverse = reverse)
        self.__load(contentList)
        
    def __getContentList(self):
        rowCount = self.tblContent.rowCount()
        contentList = []
        for idx in range(rowCount):
            contentList.append(self.tblContent.item(idx, 0).text())
        return contentList
    
    def __selectedText(self):
        selectedIndex = self.selectedIndex(self.tblContent)
        return self.tblContent.item(selectedIndex, 0).text()
        
    def GetResult(self, execResult):
        result = None
        if execResult == QtWidgets.QDialog.Accepted:
            result = self.__selectedText(), self.__getContentList()
        else:
            pass
        return result
    
if __name__ == "__main__":

    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    contentList = ['streaming1', 'streaming2']

    itemEditor = ItemEditor(contentList)

    execResult = itemEditor.exec()
    name, setting = itemEditor.GetResult(execResult)
    
    if execResult == QtWidgets.QDialog.Accepted:
        print('Accepted')
    else:
        print('Rejected')
        
    print(name, setting)        