'''
Created on 13 lip 2016

@author: Konrad Rutkowski
'''
import qtapp.attribstore

import PyQt5.QtWidgets
import PyQt5.QtCore

class AppWidget(PyQt5.QtWidgets.QWidget):

    sig_message = PyQt5.QtCore.pyqtSignal('QString')
    sig_progress = PyQt5.QtCore.pyqtSignal('int')

    def __init__(self):
        super(AppWidget,self).__init__()
        
        self.name = 'Wgt'
        self._menuactions = {}
        self._menu = None
        self._attribs = qtapp.attribstore.AppAttribStore()

    def message(self, msg):
        msg = self.name + ': ' + msg
        print(msg)
        self.sig_message.emit(msg)
        
    def progress(self, progress):
        self.sig_progress.emit(progress)
        
    def exec_settings(self):
        self._attribs.exec_settings(self.name + ': settings')
        
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
    
    def get_attrib(self, name):
        return self._attribs.get(name)
    
    def set_attrib(self, name, value):
        return self._attribs.set(name, value)

    def _add_menuaction(self, name, action):
        if name in self._menuactions.keys():
            self.message('Adding action error. Action with given name already exists.')
            return
        self._menuactions[name] = action
        
    def _add_attrib(self, name, value, attribtype = qtapp.attribstore.AttribType.text, description = '',is_setting = True, option_list = []):
        return self._attribs.add(name, value, attribtype, description, is_setting, option_list)
        

        