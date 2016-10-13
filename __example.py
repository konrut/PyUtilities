'''
Created on 15 wrz 2016

@author: Konrad Rutkowski
'''

import sys
from PyQt4 import QtGui
import qtapp
import qtapp.wgt_page


class PageWgtHome(qtapp.wgt_page.CQAppPageWidget):    
    
    def __init__(self, appWindow):
        super(PageWgtHome,self).__init__(appWindow);
        self.appMessage('Hallo World!');
        self.appProgress(20);

def main():
    app = QtGui.QApplication(sys.argv)
    
    win = qtapp.CQAppWindow();
    win.show();
    
    pageHome = PageWgtHome(win);
    
    sys.exit(app.exec_())
    
main()