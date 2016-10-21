'''
Created on 15 wrz 2016

@author: Konrad Rutkowski
'''

import sys
import PyQt5.QtWidgets
import qtapp.page
import qtapp.util_sql
import qtapp.util_svn

class PageWgtHome(qtapp.page.AppPage):    
    
    def __init__(self):
        super(PageWgtHome,self).__init__('Page');
        
    def init(self):
        self.message('Hallo World!');
        self.progress(20);

def main():
    app = PyQt5.QtWidgets.QApplication(sys.argv)
    
    win = qtapp.AppWindow()
    
    win.add_page(PageWgtHome())
    
    win.add_utility(qtapp.util_sql.AppUtilSql())
    win.add_utility(qtapp.util_svn.AppUtilSvn())    
    
    win.show()
    
    sys.exit(app.exec_())
    
main()