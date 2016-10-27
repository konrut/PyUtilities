'''
Created on 13 oct 2016

@author: Konrad Rutkowski
'''

import qtapp.utility

import PyQt5.QtWidgets
import PyQt5.QtSql

class AppUtilSql(qtapp.utility.AppUtility):
    '''
    classdocs
    '''

    def __init__(self, name = 'SQL'):
        '''
        Constructor
        '''
        super(AppUtilSql,self).__init__(name)
        
        #Attributes:
        self._add_attrib('ODBC', '', description = 'ODBC Name')  
        self._add_attrib('quotemark', '`', description = 'Quotation mark')  
        
        #Variables:
        self._db = PyQt5.QtSql.QSqlDatabase(PyQt5.QtSql.QSqlDatabase.addDatabase('QODBC3'))
        
        #Actions:
        action_settings = PyQt5.QtWidgets.QAction('Settings', self)
        action_settings.setStatusTip('SQL connection settings')
        action_settings.triggered.connect(self.settings_exec)  
        self._add_menuaction(action_settings.text(), action_settings)
        
        self.action_toggleopen = PyQt5.QtWidgets.QAction('Open', self)
        self.action_toggleopen.setStatusTip('Open/Close database')
        self.action_toggleopen.triggered.connect(self.toggleopen)  
        self._add_menuaction(self.action_toggleopen.text(), self.action_toggleopen)
        
        action_test = PyQt5.QtWidgets.QAction('debug', self)
        action_test.setShortcut('Ctrl+D')
        action_test.setStatusTip('Test action')
        action_test.triggered.connect(self._test)  
        self._add_menuaction(action_test.text(), action_test)
        
        
    def db_open(self):
        if self._db.isOpen():
            return
        self._db.setDatabaseName(self.get_attrib('ODBC'))
        
        try:
            if self._db.open():
                self.message(self.get_attrib('ODBC') + ' - opened.')
                self.action_toggleopen.setText('Close')
            else:
                self.message('Error: ' + self._db.lastError().text())
        except Exception:
            self.message('Error: ' + self._db.lastError().text())
            
    def db_close(self):
        if not self._db.isOpen():
            return        
        try:
            self._db.close()
            self.message(self.get_attrib('ODBC') + ' - closed.')
            self.action_toggleopen.setText('Open')
        except Exception:
            self.message('Error: ' + self._db.lastError().text())
    
    def toggleopen(self):
        if not self._db.isOpen():
            self.db_open()
        else:
            self.db_close()
            
    def query(self, query):
        return self._db.exec_(query)
    
    def get_table(self, table, collist = [], scheme = ''):
        quote = self.get_attrib('quotemark')
        query = 'SELECT '
        if len(collist) > 0:
            for col in collist[0:len(collist)-1]:
                query += quote + col + quote + ','
            query += quote + collist[len(collist)-1] + quote + ' '
        else:
            query += '* '
            
        query += 'FROM '
        if scheme != '':
            query += quote + scheme + quote + '.'
        query += quote + table + quote      
        return self.query(query)        
    
    def get_values(self, column, table, column_key = '', scheme = ''):
        if column_key == '':
            collist = [column]
            res = []
        else:
            collist = [column_key, column]
            res = {}
        q = self.get_table(table,collist,scheme)
        q.first()
        while q.isValid():           
            if column_key == '':
                res. append(q.record().value(column))
            else:
                res[q.record().value(column_key)] = q.record().value(column)
            q.next()
                
        return res
    
    def _test(self):
        print(self.get_values('name','components', 'id'))
        print(self.get_values('name','components'))

        
#         PyQt5.QtSql.QSqlQuery.ne
#         print(q.record())
        
        
        
        