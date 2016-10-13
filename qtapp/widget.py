'''
Created on 13 lip 2016

@author: Konrad Rutkowski
'''

import PyQt5.QtWidgets
import PyQt5.QtCore

class AppWidget(PyQt5.QtWidgets.QWidget):

    sig_message = PyQt5.QtCore.pyqtSignal('QString')
    sig_progress = PyQt5.QtCore.pyqtSignal('int')

    def __init__(self, mainWindow):
        super(AppWidget,self).__init__()
        
        self.name = 'Wgt'
        self._menuactions = {}
        self._menu = None
        self.attrib = {}
                
        self.sig_message.connect(mainWindow.message)        
        self.sig_progress.connect(mainWindow.progress) 

    def message(self, msg):
        msg = self.name + ': ' + msg
        self.sig_message.emit(msg)
        
    def progress(self, progress):
        self.sig_progress.emit(progress)
        
    def set_name(self, name):
        self.name = name
        
    def get_menu(self):
        if not self._menuactions:
            return None
        if self._menu == None:
            self._menu = PyQt5.QtWidgets.QMenu(self.name,self)
        else:
            self._menu.clear()
                        
        for action in self._menuactions.values():            
            self._menu.addAction(action) 
            
        return self._menu

    def _add_menuaction(self, name, action):
        if name in self._menuactions.keys():
            self.message('Adding action error. Action with given name already exists.')
            return
        self._menuactions[name] = action
        
    def _add_attrib(self, name, attrib):
        if name in self._attrib.keys():
            self.message('Adding attrib error. Action with given name already exists.')
            return
        self.attrib[name] = attrib
        

    '''
        
        vLayout = QtGui.QVBoxLayout()
        
        btnClose = QtGui.QPushButton("Quit")   
            
        vLayout.addWidget(btnClose)
        vLayout.addStretch()
        
        self.setLayout(vLayout)
    '''
        