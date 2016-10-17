'''
Created on 14 oct 2016

@author: Konrad Rutkowski
'''

import enum
import PyQt5.QtWidgets
import xml.etree

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
        self._widgets = {}
        
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

    def save(self, element):
        for attrib_name in self._attribs.keys():
            subelement = xml.etree.ElementTree.Element(attrib_name)
            if self._attribs[attrib_name].attribtype == AttribType.text:
                subelement.text = self._attribs[attrib_name].value
            elif self._attribs[attrib_name].attribtype == AttribType.number:
                subelement.text = str(self._attribs[attrib_name].value)              
            elif self._attribs[attrib_name].attribtype == AttribType.number_int:
                subelement.text = str(self._attribs[attrib_name].value) 
            elif self._attribs[attrib_name].attribtype == AttribType.options:
                subelement.text = self._attribs[attrib_name].value
            elif self._attribs[attrib_name].attribtype == AttribType.check:
                if self._attribs[attrib_name].value:
                    subelement.text = 'True'
                else:
                    subelement.text = 'False'
            element.append(subelement)
        return element
    
    def load(self):
        pass
    
    def add(self, name, value, attribtype = AttribType.text, description = '',is_setting = True, option_list = []):
        if name in self._attribs.keys():
            print('attribute with given name already exist!')
            raise IOError
        
        app_attrib = AppAttribute()
        app_attrib.attribtype = attribtype
        app_attrib.is_setting = is_setting
        app_attrib.option_list = option_list
        app_attrib.description = description
        
        self._set(app_attrib, value)  
        self._attribs[name] = app_attrib       
        
        if app_attrib.attribtype == AttribType.text:
            self._widgets[name] = PyQt5.QtWidgets.QLineEdit(str(value))
            self._Form.layout().addRow(app_attrib.description,self._widgets[name])
        elif app_attrib.attribtype == AttribType.number:
            self._widgets[name] = PyQt5.QtWidgets.QLineEdit(str(value))
            self._widgets[name].setValidator(PyQt5.QtGui.QDoubleValidator())
            self._Form.layout().addRow(app_attrib.description,self._widgets[name])              
        elif app_attrib.attribtype == AttribType.number_int:
            self._widgets[name] = PyQt5.QtWidgets.QLineEdit(str(value))
            self._widgets[name].setValidator(PyQt5.QtGui.QIntValidator())
            self._Form.layout().addRow(app_attrib.description,self._widgets[name])
        elif app_attrib.attribtype == AttribType.options:
            raise NotImplementedError 
        elif app_attrib.attribtype == AttribType.check:
            raise NotImplementedError  
    
    def set(self, name, value):
        if not (name in self._attribs.keys()):
            print('no attribute with given name!')
            raise IOError
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
            app_attrib.value = value
        elif app_attrib.attribtype == AttribType.check:
            app_attrib.value = bool(value)  
        else:
            return            
    
    def get(self, name):
        if not (name in self._attribs.keys()):
            print('wrong type given!')
            raise IOError
        return self._attribs[name].value
    
    def get_settingsform(self):        
        for name in self._attribs.keys():
            if self._attribs[name].attribtype == AttribType.text:
                self._widgets[name].setText(str(self._attribs[name].value))
            elif self._attribs[name].attribtype == AttribType.number:
                self._widgets[name].setText(str(self._attribs[name].value))               
            elif self._attribs[name].attribtype == AttribType.number_int:
                self._widgets[name].setText(str(self._attribs[name].value))   
            elif self._attribs[name].attribtype == AttribType.options:
                raise NotImplementedError 
            elif self._attribs[name].attribtype == AttribType.check:
                raise NotImplementedError         
        return self._Form
    
    def exec_settings(self, title = None):
        self.get_settingsform()
        if title != None:
            self._dialogSettings.setWindowTitle(title)
        self._dialogSettings.exec_()    
        
    def apply_settings(self):
        for name in self._attribs.keys():
            if self._attribs[name].attribtype == AttribType.text:
                self._attribs[name].value = self._widgets[name].text()
            elif self._attribs[name].attribtype == AttribType.number:
                self._attribs[name].value = float(self._widgets[name].text())        
            elif self._attribs[name].attribtype == AttribType.number_int:
                self._attribs[name].value = int(self._widgets[name].text()) 
            elif self._attribs[name].attribtype == AttribType.options:
                raise NotImplementedError 
            elif self._attribs[name].attribtype == AttribType.check:
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
        