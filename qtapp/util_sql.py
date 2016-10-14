'''
Created on 13 oct 2016

@author: Konrad Rutkowski
'''

import qtapp.utility

import PyQt5.QtWidgets
import PyQt5.QtSql



import time

class AppUtilSql(qtapp.utility.AppUtility):
    '''
    classdocs
    '''

    def __init__(self, name = 'SQL'):
        '''
        Constructor
        '''
        super(AppUtilSql,self).__init__(name)
        
        self._add_attrib('ODBC', '', description = 'ODBC Name')  
        
        #Actions:
        action_settings = PyQt5.QtWidgets.QAction('Settings', self)
        action_settings.setStatusTip('SQL connection settings')
        action_settings.triggered.connect(self.settings)  
        self._add_menuaction(action_settings.text(), action_settings)
        
        action_test = PyQt5.QtWidgets.QAction('debug', self)
        action_test.setShortcut('Ctrl+D')
        action_test.setStatusTip('Test action')
        action_test.triggered.connect(self._test)  
        self._add_menuaction(action_test.text(), action_test)
        
    
    def _test(self):
        
        db = PyQt5.QtSql.QSqlDatabase.addDatabase('QODBC3')
        db.setDatabaseName(self.edit_odbc.text())
        
        for i in range(1,5):
            time.sleep(1)
            if db.open():
                continue
            print(db.lastError().text())
        
        
        q = db.exec("SELECT * FROM components.components")
        print(q.record().fieldName(1))
        
        
        
        