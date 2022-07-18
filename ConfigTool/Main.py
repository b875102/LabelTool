# -*- coding: utf-8 -*-
"""
Created on Sat Feb 12 15:00:16 2022

@author: HUANG Chun-Huang
"""

import sys
from PyQt5 import QtWidgets

from ConfigTool.ConfigTool import ConfigTool

def loadConfigTool():

    app = QtWidgets.QApplication(sys.argv)
    configTool = ConfigTool()
    configTool.show()

    sys.exit(app.exec_())
    
if __name__ == "__main__":
    
    loadConfigTool()
