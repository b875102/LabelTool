import sys
import os
from PyQt5 import QtWidgets

from LabelTool import LabelTool




def loadLabelTool(fileDict = None):
    '''
    Parameters
    ----------
    fileDict : TYPE dictionary
        DESCRIPTION.
    {
        'Illustration': Illustration image path, 
        'CCTVImage': CCTV image path,
        'IntersectionConfiguration': Intersection Configuration XML path,
        'CCTVConfiguration': CCTV Configuration XML path
     }  
    
    Returns
    -------
    None.
    '''

    app = QtWidgets.QApplication(sys.argv)
    labelTool = LabelTool()
    #app.installEventFilter(myshow)
    labelTool.show()

    if fileDict:
        labelTool.OpenImages(fileDict)

    sys.exit(app.exec_())

def loadForDev():
    
    folder = os.path.dirname(__file__)
    folder = os.path.join(folder, 'data')
    #folder = 'D:/_Course/Project/LabelTool/data'
    
    fileDict = {}

    fileDict['Illustration'] = os.path.join(folder, 'illustration.png')
    fileDict['CCTVImage'] = os.path.join(folder, '192.168.111.26_園區二路與研發二路球機(12)_道路淨空.png')
    fileDict['IntersectionConfiguration'] = os.path.join(folder, 'Intersection_configuration.xml')
    fileDict['CCTVConfiguration'] = os.path.join(folder, 'cctv_configuration.xml')

    loadLabelTool(fileDict)

if __name__ == "__main__":

    loadForDev()
    #loadLabelTool(None)

