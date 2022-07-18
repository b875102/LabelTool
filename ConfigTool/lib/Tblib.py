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