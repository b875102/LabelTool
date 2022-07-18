# -*- coding: utf-8 -*-
"""
Created on Wed Jul  6 21:55:08 2022

@author: HUANG Chun-Huang
"""

import os
import cv2
import threading
from socket import timeout as socket_timeout

from lib.config import Config
from lib.sshClient import SSHClient

class StreamingHelper():
    
    __debug = True
    
    def __init__(self):
        self.__config = Config()
        
    def __getSSHClient(self, setting):
        ip = setting['ip']
        acc = setting['acc']
        pw = setting['pw']
        sshClient = SSHClient(ip, acc, pw)
        return sshClient
    
    def __print(self, outlines, errlines):
        if self.__debug:
            print(outlines)
            print(errlines)
        
    # docker related
    def __checkImage(self, sshClient, setting):
        containerInfo = self.__config.getContainerInfo()
        imageName = containerInfo['docker_image']
        pw = setting['pw']
        if ':' in imageName:
            imageName = imageName.split(':')[0]
        cmd = f'echo {pw} | sudo -S docker images'
        stdin, outlines, errlines = sshClient.execcmd(cmd)
        self.__print(outlines, errlines)
        return (imageName in outlines)
    
    def __pullImage(self, sshClient, setting):
        containerInfo = self.__config.getContainerInfo()
        imageName = containerInfo['docker_image']
        pw = setting['pw']
        cmd = f'echo {pw} | sudo -S docker pull {imageName}'
        stdin, outlines, errlines = sshClient.execcmd(cmd)
        self.__print(outlines, errlines)
        return (imageName in outlines)
    
    def __checkContainer(self, sshClient, setting):
        containerInfo = self.__config.getContainerInfo()
        imageName = containerInfo['docker_image']
        containerName = setting['name']
        containerName = f'{imageName}|{containerName}|'
        pw = setting['pw']
        cmd = 'echo ' + pw + ' | sudo -S docker ps -a --format \"table {{.Image}}|{{.Names}}|{{.Status}}\"'
        stdin, outlines, errlines = sshClient.execcmd(cmd)
        self.__print(outlines, errlines)
        result = (containerName in outlines)
        status = None
        if result:
            outlines = outlines.split('\n')
            for outline in outlines:
                if (containerName in outline):
                    status = outline.split('|')[2].split(' ')[0]
                    break
        return result, status
    
    def __runContainer(self, sshClient, setting):
        containerInfo = self.__config.getContainerInfo()
        imageName = containerInfo['docker_image']
        host_folder = containerInfo['host_folder']
        container_folder = containerInfo['container_folder']
        container_streaming_port = containerInfo['streaming_port']
        container_nginx_port = containerInfo['nginx_port']
        
        host_streaming_port = setting['streaming_port']
        host_nginx_port = setting['nginx_port']

        containerName = setting['name']
        pw = setting['pw']

        cmd = f'echo {pw} | sudo -S docker run -it -d --privileged --cap-add NET_ADMIN --cap-add NET_BROADCAST --cap-add SYS_MODULE -p {host_nginx_port}:{container_nginx_port} -p {host_streaming_port}:{container_streaming_port} -v {host_folder}:{container_folder} --name {containerName} {imageName}'
        stdin, outlines, errlines = sshClient.execcmd(cmd)
        self.__print(outlines, errlines)
        return self.__checkContainer(sshClient, setting)
    
    def __startContainer(self, sshClient, setting):
        containerName = setting['name']
        pw = setting['pw']
        cmd = f'echo {pw} | sudo -S docker start {containerName}'
        stdin, outlines, errlines = sshClient.execcmd(cmd)
        self.__print(outlines, errlines)
        return (f'{containerName}\n' == outlines)
    
    def __stopContainer(self, sshClient, setting):
        containerName = setting['name']
        pw = setting['pw']
        cmd = f'echo {pw} | sudo -S docker stop {containerName}'
        stdin, outlines, errlines = sshClient.execcmd(cmd)
        self.__print(outlines, errlines)
        return (f'{containerName}\n' == outlines)
    
    def __execContainer(self, sshClient, setting):
        containerName = setting['name']
        pw = setting['pw']
        #cmd = f'echo {pw} | sudo -S docker exec -it {containerName} bash'
        cmd = f'echo {pw} | sudo -S docker exec -i {containerName} bash'
        stdin, outlines, errlines = sshClient.execcmd(cmd)
        self.__print(outlines, errlines)
        return (f'{containerName}\n' == outlines)
    
    # demo video related
    def __checkDemoVideo(self, sshClient, setting):     
        containerInfo = self.__config.getContainerInfo()
        host_folder = containerInfo['host_folder']          
        demoVideo = os.path.basename(setting['demo'])
        files = sshClient.listdir(host_folder)
        return (demoVideo in files)
    
    def __cpDemoVideo(self, sshClient, setting):
        containerInfo = self.__config.getContainerInfo()
        host_folder = containerInfo['host_folder']          
        demoVideo = setting['demo']
        demoBaseName = os.path.basename(demoVideo)
        demoVideoPath = f'{host_folder}/{demoBaseName}'
        serverPath = sshClient.toServerPath(demoVideoPath)
        result = sshClient.cp(demoVideo, serverPath)
        return result
    
    def __changeMode(self, sshClient, setting):
        containerInfo = self.__config.getContainerInfo()
        host_folder = containerInfo['host_folder']
        cmd = f'echo dan | sudo -S chmod 755 {host_folder}/*'
        stdin, outlines, errlines = sshClient.execcmd(cmd)
        self.__print(outlines, errlines)
        return (outlines == '')
        
    
    # streaming server related
    def __checkNginX(self, sshClient, setting):
        host_nginx_port = setting['nginx_port']
        ip = setting['ip']
        cmd = f'curl http://{ip}:{host_nginx_port}'
        stdin, outlines, errlines = sshClient.execcmd(cmd)
        self.__print(outlines, errlines)
        return ('Welcome to nginx' in outlines)
    
    def __startNginX(self, sshClient, setting):
        pw = setting['pw']
        name = setting['name']
        cmd = f'echo {pw} | sudo -S docker exec {name} /usr/local/nginx/sbin/nginx'
        stdin, outlines, errlines = sshClient.execcmd(cmd)
        self.__print(outlines, errlines)
        return (outlines == '')
    
    def __stopNginX(self, sshClient, setting):
        pw = setting['pw']
        name = setting['name']
        cmd = f'echo {pw} | sudo -S docker exec {name} /usr/local/nginx/sbin/nginx -s stop'
        stdin, outlines, errlines = sshClient.execcmd(cmd)
        self.__print(outlines, errlines)
        return (outlines == '')
    
    def __checkStreaming(self):
        pass
    
    def __stopStreaming(self, sshClient, setting):
        pass
    
    def __startStreaming(self, sshClient, setting):
        containerInfo = self.__config.getContainerInfo()
        streaming_port = containerInfo['streaming_port']
        pw = setting['pw']
        cctvUrl = setting['cctv']
        name = setting['name']
        demoVideo = setting['demo']
        
        streamingUrl = f'rtmp://localhost:{streaming_port}/live/{name}'
        
        task = setting['task']
        if task == 'live':
            cmd = f'echo {pw} | sudo -S docker exec {name} ffmpeg -re -i {cctvUrl} -c copy -f flv {streamingUrl}'
        else:
            demoBaseName = os.path.basename(demoVideo)
            rtmpName, rtmpNameExt = os.path.splitext(demoBaseName)
            cmd = f'echo {pw} | sudo -S docker exec {name} ffmpeg -re -stream_loop -1 -i /usr/local/nginx/html/video/{demoBaseName} -acodec copy -vcodec copy -f flv -an {streamingUrl}'
        
        result = True
        try:
            stdin, outlines, errlines = sshClient.execcmd(cmd, timeout = 1)
        except socket_timeout:
            print("launch streaming successfully")
        else:
            print("launch streaming failed")
            result = False
        finally:
            pass
        
        #self.__print(outlines, errlines)
        return result       
    
    def __getStreamingUrl(self, setting):
        ip = setting['ip']
        streaming_port = setting['streaming_port']
        name = setting['name']
        rtmp = f'rtmp://{ip}:{streaming_port}/live/{name}'
        return rtmp

    def post(self, setting):
        sshClient = self.__getSSHClient(setting)
        if not self.__checkImage(sshClient, setting):
            self.__pullImage(sshClient, setting)

        result, status = self.__checkContainer(sshClient, setting)
        if not result:
            result = self.__runContainer(sshClient, setting)
            status = 'Up'
            
        if result:
            statusDict = {'stop': 'Exited', 'start':'Up'}
            settingStatus = statusDict[setting['status']]
            if settingStatus != status:
                if settingStatus == 'Up':
                    result = self.__startContainer(sshClient, setting) 
                else:
                    self.__stopContainer(sshClient, setting)
                    result = False
            else:
                result = (settingStatus == 'Up')
                    
        if result:
            if not self.__checkDemoVideo(sshClient, setting):
                self.__cpDemoVideo(sshClient, setting)
                self.__changeMode(sshClient, setting)
                
            if self.__checkNginX(sshClient,setting):
                self.__stopNginX(sshClient, setting)
            
            self.__startNginX(sshClient, setting)
            self.__stopStreaming(sshClient,setting)
            self.__startStreaming(sshClient,setting)
        sshClient.close()
        
    def preview(self, setting):
        streamingUrl = self.__getStreamingUrl(setting)
        
        t = threading.Thread(target = self.__preview_asyc, args=(setting['name'], streamingUrl))
        t.start()
        #self.__preview_asyc(setting['name'], streamingUrl)
        
    def __preview_asyc(self, name, streamingUrl):
        cap = cv2.VideoCapture(streamingUrl)
        helf_size = (960, 540)
        while(True):
            ret, frame = cap.read()
            #helf_size = (int(frame.shape[1] / 2), int(frame.shape[0] / 2))
            imh = cv2.resize(frame, helf_size)  
            cv2.imshow(name, imh)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()        
        
        
        
if __name__ == "__main__":
    import sys
    sys.path.append('D:/_Course/Project/iTraffic/GUI/StreamingManagement')
    setting = {'name': 'streaming1' ,
               'ip': '192.168.50.152',
               'port': 19350,
               'acc': 'dan',
               'pw': 'dan',
               'cctv': 'http://127.0.0.1/cam1',
               'demo': '/usr/local/nginx/html/video/NorthGate_Modify.api',
               'task': 'demo',
               'status': 'stop'}
    
    streamingHelper = StreamingHelper()
    streamingHelper.post(setting)