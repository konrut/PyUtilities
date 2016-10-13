'''
Created on 13 oct 2016

@author: Drakon
'''

import qtapp.utility
import PyQt5.QtWidgets

import subprocess


class AppUtilSvn(qtapp.utility.AppUtility):
    '''
    classdocs
    '''

    def __init__(self, mainWindow):
        '''
        Constructor
        '''
        super(AppUtilSvn,self).__init__(mainWindow,'SVN')
        
        #window: settings
        self.wgtSettings = PyQt5.QtWidgets.QWidget()
        self.wgtSettings.setWindowTitle(self.name + ': settings')
        self.wgtSettings.setWindowModality(PyQt5.QtCore.Qt.WindowModal)
        
        self.wgtSettings.setLayout(PyQt5.QtWidgets.QVBoxLayout())
        
        Form = PyQt5.QtWidgets.QWidget(self)
        Form.setLayout(PyQt5.QtWidgets.QFormLayout())
        self.wgtSettings.layout().addWidget(Form)        

        
        self.edit_path = PyQt5.QtWidgets.QLineEdit()
        Form.layout().addRow('SVN bin folder:',self.edit_path)
        
        
        self.edit_svn_dir = PyQt5.QtWidgets.QLineEdit()
        Form.layout().addRow('SVN directory:',self.edit_svn_dir)
        
        self.edit_direct_dir = PyQt5.QtWidgets.QLineEdit()
        Form.layout().addRow('Direct access directory:',self.edit_direct_dir)
        
        
        #self.wgtSettings.
        
        
        #Actions:
        action_settings = PyQt5.QtWidgets.QAction('Settings', self)
        action_settings.setStatusTip('SQL connection settings')
        action_settings.triggered.connect(self.settings)  
        self._add_menuaction(action_settings.text(), action_settings)
        
        action_test = PyQt5.QtWidgets.QAction('debug', self)
        action_test.setStatusTip('Test action')
        action_test.triggered.connect(self._test)  
        self._add_menuaction(action_test.text(), action_test)
                
    def put(self, file_dir, svn_dir, comment = ''):
        subprocess.call(['svnmucc', '--non-interactive',  '-m', comment,'put', file_dir, svn_dir])            
    
    def settings(self):
        self.wgtSettings.show()
        
    def _test(self):
        self.put(PyQt5.QtWidgets.QFileDialog.getOpenFileName()[0],'svn://diskstation/library/footprints/tmp','test')
    
