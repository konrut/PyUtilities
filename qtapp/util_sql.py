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

    def __init__(self, mainWindow):
        '''
        Constructor
        '''
        super(AppUtilSql,self).__init__(mainWindow,'SQL')
        
        #window: settings
        self.wgtSettings = PyQt5.QtWidgets.QWidget()
        self.wgtSettings.setWindowTitle(self.name + ': settings')
        self.wgtSettings.setWindowModality(PyQt5.QtCore.Qt.WindowModal)
        
        self.wgtSettings.setLayout(PyQt5.QtWidgets.QVBoxLayout())
        
        Form = PyQt5.QtWidgets.QWidget(self)
        Form.setLayout(PyQt5.QtWidgets.QFormLayout())
        self.wgtSettings.layout().addWidget(Form)        

        
        self.edit_odbc = PyQt5.QtWidgets.QLineEdit()
        Form.layout().addRow('ODBC Name:',self.edit_odbc)
        
        #self.wgtSettings.
        
        
        #Actions:
        action_settings = PyQt5.QtWidgets.QAction('Settings', self)
        action_settings.setStatusTip('SQL connection settings')
        action_settings.triggered.connect(self.settings)  
        self._add_menuaction(action_settings, action_settings.text())
        
        action_test = PyQt5.QtWidgets.QAction('debug', self)
        action_test.setShortcut('Ctrl+D')
        action_test.setStatusTip('Test action')
        action_test.triggered.connect(self._test)  
        self._add_menuaction(action_test.text(), action_test)
        
    def settings(self):
        self.wgtSettings.show()
    
    def _test(self):
        
        db = PyQt5.QtSql.QSqlDatabase.addDatabase('QODBC3')
        db.setDatabaseName(self.edit_odbc.text())
        
        for i in range(1,5):
            time.sleep(1)
            if db.open():
                continue
            print(db.lastError().text())
        
        
        q = db.exec("SELECT * FROM components")
        print(q.record().fieldName(1))
        
        
        
        