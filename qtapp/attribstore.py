'''
Created on 14 oct 2016

@author: Konrad Rutkowski
'''

import enum
import PyQt5.QtWidgets

class AttribType(enum.Enum):
    text = 0
    number = 1
    number_int = 2
    options = 3
    check = 4
    

class AppAttribStore(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self._attribs = {}
        
        self._Form = PyQt5.QtWidgets.QWidget()
        self._Form.setLayout(PyQt5.QtWidgets.QFormLayout())         
        
        buttonOK = PyQt5.QtWidgets.QPushButton('OK')
        buttonOK.setDefault(True)
        buttonCancel = PyQt5.QtWidgets.QPushButton('Cancel')
        buttonApply = PyQt5.QtWidgets.QPushButton('Apply')
        
        Buttons = PyQt5.QtWidgets.QWidget()
        Buttons.setLayout(PyQt5.QtWidgets.QHBoxLayout())
        Buttons.layout().addStretch()
        Buttons.layout().addWidget(buttonOK)                
        Buttons.layout().addWidget(buttonCancel)
        Buttons.layout().addWidget(buttonApply)
        
        self._wgtSettings = PyQt5.QtWidgets.QWidget()
        self._wgtSettings.setWindowTitle('Settings')   
        self._wgtSettings.setLayout(PyQt5.QtWidgets.QVBoxLayout())
        self._wgtSettings.layout().addWidget(self._Form)
        self._wgtSettings.layout().addWidget(Buttons)
        self._wgtSettings.layout().addStretch()
        
        self._dialogSettings = PyQt5.QtWidgets.QDialog()
        self._dialogSettings.setLayout(PyQt5.QtWidgets.QVBoxLayout())
        self._dialogSettings.layout().addWidget(self._wgtSettings)        
        buttonOK.clicked.connect(self._dialogSettings.accept)
        buttonOK.clicked.connect(self.apply_settings)
        buttonCancel.clicked.connect(self._dialogSettings.reject)
        buttonApply.clicked.connect(self.apply_settings)

    def save(self):
        pass
    
    def load(self):
        pass
    
    def add(self, name, value, attribtype = AttribType.text, description = '',is_setting = True, option_list = []):
        if name in self._attribs.keys():
            print('attribute with given name already exist!')
            raise IOError
            return
        
        app_attrib = AppAttribute()
        app_attrib.attribtype = attribtype
        app_attrib.is_setting = is_setting
        app_attrib.option_list = option_list
        app_attrib.description = description
        
        self._set(app_attrib, value)  
        self._attribs[name] = app_attrib        
    
    def set(self, name, value):
        if not (name in self._attribs.keys()):
            print('no attribute with given name!')
            raise IOError
            return
        self._set(self._attribs[name], value)
    
    def _set(self, app_attrib, value):        
        if app_attrib.attribtype == AttribType.text:
            app_attrib.value = str(value)
        elif app_attrib.attribtype == AttribType.number:
            app_attrib.value = float(value)
        elif app_attrib.attribtype == AttribType.number_int:
            app_attrib.value = int(value)     
        elif app_attrib.attribtype == AttribType.options:
            if not (value in app_attrib.option_list):
                print('empty option list given!')
                raise IOError
                return     
            app_attrib.value = value
        elif app_attrib.attribtype == AttribType.check:
            app_attrib.value = bool(value)  
        else:
            return            
    
    def get(self, name):
        if not (name in self._attribs.keys()):
            print('wrong type given!')
            raise IOError
            return None
        return self._attribs[name].value
    
    def get_settingsform(self):
        
        while self._Form.layout().count() > 0:
            item = self._Form.layout().takeAt(0)
            if not item:
                continue
            w = item.widget()
            if w:
                w.deleteLater()

        self._Form.setLayout(PyQt5.QtWidgets.QFormLayout())   
        for attrib in self._attribs.values():
            if attrib.attribtype == AttribType.text:
                edit_text = PyQt5.QtWidgets.QLineEdit(attrib.value)
                self._Form.layout().addRow(attrib.description,edit_text)
            elif attrib.attribtype == AttribType.number:
                edit_text = PyQt5.QtWidgets.QLineEdit(str(attrib.value))
                edit_text.setValidator(PyQt5.QtGui.QDoubleValidator())
                self._Form.layout().addRow(attrib.description,edit_text)                
            elif attrib.attribtype == AttribType.number_int:
                edit_text = PyQt5.QtWidgets.QLineEdit(str(attrib.value))
                edit_text.setValidator(PyQt5.QtGui.QIntValidator())
                self._Form.layout().addRow(attrib.description,edit_text)   
            elif attrib.attribtype == AttribType.options:
                raise NotImplementedError 
            elif attrib.attribtype == AttribType.check:
                raise NotImplementedError 
        
        return self._Form
    
    def exec_settings(self, title = None):
        self.get_settingsform()
        if title != None:
            self._dialogSettings.setWindowTitle(title)
        self._dialogSettings.exec_()    
        
    def apply_settings(self):
        raise NotImplementedError
        
        
class AppAttribute(object):
    '''
    classdocs
    '''
    attribtype = AttribType.text
    value = None
    is_setting = True    
    description = ''
    option_list = []
        