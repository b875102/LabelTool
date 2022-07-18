# -*- coding: utf-8 -*-
"""
Created on Sun Feb 20 14:29:32 2022

@author: HUANG Chun-Huang
"""

import os
from datetime import datetime


class FileHelper():
    
    def __init__(self):
        pass
    
    def writeTxt(self, fname, contents):
        
        result = False
        f = None
        tname = str(hex(int(datetime.now().timestamp())))
        
        try:
            f = open(tname, mode = 'w+', encoding = 'utf-8')
            for content in contents:
                f.write(content + '\n')
            result = True
        except Exception as ex:
            result = False
            print('error occured: ', ex)
        finally:
            if f:
                f.close()
                
            if result:
                if os.path.exists(fname):
                    os.remove(fname)
                os.rename(tname, fname)
            else:
                if os.path.exists(tname):
                    os.remove(tname)

        return result
    
    def writeFiles(self, fdict):
        for fname in fdict:
            result = False
            f = None
            try:
                f = open(fname, mode = 'w+', encoding = 'utf-8')
                f.write(fdict[fname])
                result = True
            except Exception as ex:
                print('error occured: ', ex)
                result = False
            finally:
                if f:
                    f.close()
                    
                if result:
                    print('write file {0} successfully'.format(fname))
                else:
                    print('write file {0} fail'.format(fname))
    
    def writePngs(self, fdict):
        for fname in fdict:
            result = False
            f = None
            try:
                f = open(fname, mode = 'w+', encoding = 'utf-8')
                f.write(fdict[fname])
                result = True
            except Exception as ex:
                print('error occured: ', ex)
                result = False
            finally:
                if f:
                    f.close()
                    
                if result:
                    print('write file {0} successfully'.format(fname))
                else:
                    print('write file {0} fail'.format(fname))
                    
if __name__ == "__main__":
    
    fileHelper = FileHelper()
    fileHelper.writeTxt('12345', [])