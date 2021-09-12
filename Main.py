import sys
from PyQt5 import QtWidgets

from LabelTool import LabelTool

if __name__ == "__main__":


    app = QtWidgets.QApplication(sys.argv)
    labelTool = LabelTool()
    #app.installEventFilter(myshow)
    labelTool.show()

    sys.exit(app.exec_())