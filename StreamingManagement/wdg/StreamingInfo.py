# -*- coding: utf-8 -*-
"""
Created on Sat Jul  2 17:07:19 2022

@author: HUANG Chun-Huang
"""

from PyQt5 import QtWidgets, uic

from wdg.ItemEditor import ItemEditor

class StreamingInfo(QtWidgets.QDialog):
    
    __task_list = ['demo', 'live']
    __status_list = ['stop', 'start']
    
    def __init__(self, cctvList, demoVideoList, streamingSetting = None):
        super(StreamingInfo, self).__init__()
        uic.loadUi('wdg/StreamingInfo.ui', self)
        
        self.__initUi()
        
        self.__cctvList = cctvList
        self.__demoVideoList = demoVideoList
        
        if streamingSetting != None:
            self.__setting = streamingSetting
        else:
            self.__setting = self.__getEmptySetting()
            
        self.__setUi(self.__setting)
        
        self.btnCCTV.clicked.connect(self.__CCTV_Clicked)
        self.btnDemoVideo.clicked.connect(self.__DemoVideo_Clicked)
        
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
                   'streaming_port': -1,
                   'nginx_port': -1,
                   'acc': '',
                   'pw': '',
                   'cctv': '',
                   'demo': '',
                   'task': 'demo',
                   'status': 'stop'}
        return setting
        
    def __setUi(self, setting):
        
        self.txtName.setText(setting['name'])
        self.txtIP.setText(setting['ip'])
        self.txtStreamingPort.setText(str(setting['streaming_port']))
        self.txtNginxPort.setText(str(setting['nginx_port']))
        self.txtAccount.setText(setting['acc'])
        self.txtPassword.setText(setting['pw'])
        self.txtCCTV.setText(setting['cctv'])
        self.txtDemoVideo.setText(setting['demo'])
        
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
        
    def __getStreamingSetting(self):

        setting = self.__getEmptySetting()
        
        setting['name'] = self.txtName.text()
        setting['ip'] = self.txtIP.text()
        setting['streaming_port'] = int(self.txtStreamingPort.text())
        setting['nginx_port'] = int(self.txtNginxPort.text())
        setting['acc'] = self.txtAccount.text()
        setting['pw'] =  self.txtPassword.text()
        setting['cctv'] = self.txtCCTV.text()
        setting['demo'] = self.txtDemoVideo.text()
        setting['task'] = self.cboTask.currentText()
        setting['status'] = self.cboStatus.currentText()
        
        return setting
    
    def __CCTV_Clicked(self):
        itemEditor = ItemEditor('CCTV', self.__cctvList, editable = True)
        execResult = itemEditor.exec()
        
        if execResult == QtWidgets.QDialog.Accepted:
            selectedText, self.__cctvList = itemEditor.GetResult(execResult)
            self.txtCCTV.setText(selectedText)
        else:
            pass

    def __DemoVideo_Clicked(self):
        itemEditor = ItemEditor('Demo Video', self.__demoVideoList, editable = True)
        execResult = itemEditor.exec()
        
        if execResult == QtWidgets.QDialog.Accepted:
            selectedText, self.__demoVideoList = itemEditor.GetResult(execResult)
            self.txtDemoVideo.setText(selectedText)
        else:
            pass

    def GetResult(self, execResult):
        result = None
        if execResult == QtWidgets.QDialog.Accepted:
            result = self.__cctvList, self.__demoVideoList, self.__getStreamingSetting()
        else:
            pass
        
        return result

if __name__ == "__main__":
    
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
    setting = {'name': 'streaming1' ,
               'ip': '192.168.50.42',
               'streaming_port': 19350,
               'nginx_port': 8080,               
               'acc': 'dan',
               'pw': 'dan',
               'cctv': 'http://127.0.0.1/cam1',
               'demo': '/usr/local/nginx/html/video/NorthGate_Modify.api',
               'task': 'demo',
               'status': 'stop'}
        
    streamingInfo = StreamingInfo([], [], setting)

    execResult = streamingInfo.exec()
    name, setting = streamingInfo.GetResult(execResult)
    
    if execResult == QtWidgets.QDialog.Accepted:
        print('Accepted')
    else:
        print('Rejected')
        
    print(name, setting)

    