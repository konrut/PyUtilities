'''
Created on 15 wrz 2016

@author: Konrad Rutkowski
'''

import sys
from PyQt4 import QtGui
from AppWindow.CQAppWindow import CQAppWindow

def main():
    app = QtGui.QApplication(sys.argv)
    
    win = CQAppWindow();
    win.show();
    
    sys.exit(app.exec_())
    
main()