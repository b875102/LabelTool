# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 14:29:35 2022

@author: HUANG Chun-Huang
"""

from PyQt5 import QtCore, QtWidgets

class Tblib():
    
    def addRows(self, tbl, contents):
        addedRowIdx = []
        rowNum = len(contents)
        if rowNum > 0:
            columnNum = len(contents[0])
            for rIdx in range(rowNum):
                row_count = tbl.rowCount()
                tbl.insertRow(row_count)
                row = contents[rIdx]
                for cIdx in range(columnNum):
                    item = QtWidgets.QTableWidgetItem(row[cIdx])
                    #item.setTextAlignment(QtCore.Qt.AlignRight)
                    tbl.setItem(row_count, cIdx, item)
                addedRowIdx.append(row_count)
        return addedRowIdx
    
    def resizeToContents(self, tbl):
        tbl.resizeRowsToContents()
        tbl.resizeColumnsToContents()    
        
    def selectedIndex(self, tbl):
        return tbl.currentRow()
    
    def selectedIndexes(self, tbl):
        rows = []
        selected = tbl.selectedItems()
        if selected:
            for item in selected:
                rows.append(item.row())

        return rows
    
    def getValue(self, tbl, rowIdx, colIdx):
        return tbl.item(rowIdx, colIdx).text()
    
    def deleteRow(self, tbl):
        selectedRow = tbl.currentRow()
        tbl.removeRow(selectedRow)
        return selectedRow
    
    def selectedRow(self, tbl, rowIdx):
        item = tbl.item(rowIdx, 0)
        tbl.setCurrentItem(item)
        
    def addCombobox(self, tbl, col, itemList, rowList, cbf = None):
        for row in rowList:
            item = tbl.item(row, col)
            cbo = QtWidgets.QComboBox()
            cbo.addItems(itemList)
            
            idx = cbo.findText(item.text(), QtCore.Qt.MatchFixedString)
            idx = 0 if idx < 0 else idx
                
            cbo.setCurrentIndex(idx)
            cbo.setProperty('row', row)
            cbo.setProperty('col', col)
            cbo.setProperty('tbl', tbl)
            cbo.setProperty('cbf', cbf)
            cbo.currentIndexChanged.connect(self.__cbo_IndexChanged)
            tbl.setCellWidget(row, col, cbo)
            
    def __cbo_IndexChanged(self):
        cbo = self.sender()
        if type(cbo).__name__ == 'QComboBox':
            row = cbo.property('row')
            col = cbo.property('col')
            tbl = cbo.property('tbl')
            cbf = cbo.property('cbf')
            txt = cbo.currentText()
            item = tbl.item(row , col)
            item.setText(txt)
            if cbf != None:
                cbf(tbl, row, col, txt)