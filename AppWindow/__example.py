'''
Created on 15 wrz 2016

@author: Konrad Rutkowski
'''

import sys
from PyQt4 import QtGui
from AppWindow.CQAppWindow import CQAppWindow
from AppWindow.CQAppPageWidget import CQAppPageWidget


class PageWgtHome(CQAppPageWidget):    
    
    def __init__(self, appWindow):
        super(PageWgtHome,self).__init__(appWindow);
        self.appMessage('Hallo World!');

def main():
    app = QtGui.QApplication(sys.argv)
    
    win = CQAppWindow();
    win.show();
    
    pageHome = PageWgtHome(win);
    
    sys.exit(app.exec_())
    
main()