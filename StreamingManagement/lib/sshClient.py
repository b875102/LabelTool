# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 22:00:55 2022

@author: HUANG Chun-Huang
"""

import paramiko
import re

class SSHClient():
    
    def __init__(self, ip, userid, pw, timeout = 5):
        
        self.__encoding = 'utf-8'
        self.__ip = ip
        self.__userid = userid
        self.__pw = pw
        
        print(f'connect to {self.__userid}@{self.__ip}')
        
        self.__client = paramiko.SSHClient()
        self.__client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__client.connect(hostname = self.__ip, username = self.__userid, password = self.__pw, timeout = timeout)
        self.__sftp = self.__client.open_sftp()
        
    def chdir(self, path):
        return self.sftp.chdir(path)
    
    def listdir(self, path = '.'):
        return self.__sftp.listdir(path)
    
    def remove(self, path):
        self.__sftp.remove(path)
        
    def execcmd(self, cmd, timeout = 5):
        print(f'execute command: {cmd}')
        stdin, stdout, stderr = self.__client.exec_command(cmd, timeout = timeout)
        print('executed command successfully')
        outlines = ''.join(stdout.readlines())
        errlines = ''.join(stderr.readlines())
        return stdin, outlines, errlines
        
    def toServerPath(self, dir):
        return f'{self.__userid}@{self.__ip}:{dir}'
    
    def cp(self, source, destination):
        cmd = f'sshpass -p {self.__pw} scp -o StrictHostKeyChecking=no {source} {destination}'
        stdin, outlines, errlines = self.execcmd(cmd)
        print('stdout: ', outlines)
        print('stderr: ', errlines)
        return (errlines == '')
        
    def close(self):
        self.__sftp.close()
        self.__client.close()
        print(f'disconnect {self.__userid}@{self.__ip}')
        
if __name__ == "__main__":
    
    sshClient = SSHClient('192.168.0.222', 'dan', 'dan')

    #echo <password> | sudo -S <command>
    stdin, outlines, errlines = sshClient.execcmd('echo dan | sudo -S docker ps -a')
    print('stdout: ', outlines)
    print('stderr: ', errlines)
    
    sshClient.close()