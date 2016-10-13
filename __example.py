'''
Created on 15 wrz 2016

@author: Konrad Rutkowski
'''

import sys
from PyQt5 import QtWidgets
import qtapp.widget
import qtapp.util_sql
import qtapp.util_svn


class PageWgtHome(qtapp.widget.AppWidget):    
    
    def __init__(self, appWindow):
        super(PageWgtHome,self).__init__(appWindow);
        self.Name = 'Page'
        self.message('Hallo World!');
        self.progress(20);

def main():
    app = QtWidgets.QApplication(sys.argv)
    
    win = qtapp.AppWindow();
    win.show();
    
    pageHome = PageWgtHome(win);
    utilSql = qtapp.util_sql.AppUtilSql(win)
    utilSvn = qtapp.util_svn.AppUtilSvn(win)
    
    win.set_currentpage(pageHome);
    win.add_utility(utilSql)
    win.add_utility(utilSvn)
    
    sys.exit(app.exec_())
    
main()