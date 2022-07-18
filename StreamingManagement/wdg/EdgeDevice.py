# -*- coding: utf-8 -*-
"""
Created on Sun Jul  3 15:23:05 2022

@author: HUANG Chun-Huang
"""

from PyQt5 import QtWidgets, uic
from wdg.ItemEditor import ItemEditor

class EdgeDevice(QtWidgets.QDialog):
    
    __task_list = ['offline', 'inline']
    __status_list = ['stop', 'start']
    
    def __init__(self, streamingList, edgeSetting = None):
        super(EdgeDevice, self).__init__()
        uic.loadUi('wdg/EdgeDevice.ui', self)
        
        self.__initUi()
        
        self.__streamingList = streamingList
        
        if edgeSetting != None:
            self.__setting = edgeSetting
        else:
            self.__setting = self.__getEmptySetting()
            
        self.__setUi(self.__setting)
        
        self.btnStreaming.clicked.connect(self.__Streaming_Clicked)
        
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)  
    
    def __initUi(self):
        self.resize(400, 200)
        self.cboTask.addItems(self.__task_list)
        self.cboStatus.addItems(self.__status_list)
        self.cboTask.setCurrentIndex(0)
        self.cboStatus.setCurrentIndex(0)
        
        self.label_8.hide()
        self.label_9.hide()
        self.cboTask.hide()
        self.cboStatus.hide()
        
    def __getEmptySetting(self):
        setting = {'name':'',
                   'ip': '',
                   'acc': '',
                   'pw': '',
                   'streaming': '',
                   'task': 'offline',
                   'status': 'stop'}
        return setting
        
    def __setUi(self, setting):
        
        self.txtName.setText(setting['name'])
        self.txtIP.setText(setting['ip'])
        self.txtAccount.setText(setting['acc'])
        self.txtPassword.setText(setting['pw'])
        self.txtStreaming.setText(setting['streaming'])
        
        if setting['task'] in self.__task_list:
            taskidx = self.__task_list.index(setting['task'])
            self.cboTask.setCurrentIndex(taskidx)
        else:
            self.cboTask.setCurrentIndex(0)
            
        if setting['status'] in self.__status_list:
            statusIdx = self.__status_list.index(setting['status'])
            self.cboStatus.setCurrentIndex(statusIdx)
        else:       
            self.cboStatus.setCurrentIndex(0)        
        
    def __getEdgeSetting(self):

        setting = self.__getEmptySetting()
        
        setting['name'] = self.txtName.text()
        setting['ip'] = self.txtIP.text()
        setting['acc'] = self.txtAccount.text()
        setting['pw'] =  self.txtPassword.text()
        setting['streaming'] = self.txtStreaming.text()
        setting['task'] = self.cboTask.currentText()
        setting['status'] = self.cboStatus.currentText()
        
        return setting
    
    def __Streaming_Clicked(self):
        itemEditor = ItemEditor('Streaming', self.__streamingList, editable = False)
        execResult = itemEditor.exec()
        
        if execResult == QtWidgets.QDialog.Accepted:
            selectedText, self.__streamingList = itemEditor.GetResult(execResult)
            self.txtStreaming.setText(selectedText)
        else:
            pass
        
    def GetResult(self, execResult):
        
        if execResult == QtWidgets.QDialog.Accepted:
            config = self.__getEdgeSetting()
        else:
            config = self.__setting
        
        return config

if __name__ == "__main__":
    
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    setting = {'name':'gpu1',
               'ip': '192.168.50.42',
               'acc': 'dan',
               'pw': 'dan',
               'streaming': 'http://127.0.0.1/streaming1',
               'task': 'inline',
               'status': 'stop'}
        
    edgeDevice = EdgeDevice([], setting)

    execResult = edgeDevice.exec()
    setting = edgeDevice.GetResult(execResult)
    
    if execResult == QtWidgets.QDialog.Accepted:
        print('Accepted')
    else:
        print('Rejected')
        
    print(setting)

