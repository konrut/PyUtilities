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

class AppAttribStore(PyQt5.QtWidgets.QWidget):
    '''
    classdocs
    '''
    def __init__(self, parent = None):
        super(AppAttribStore,self).__init__(parent)
        self._attribs = {}
        self._widgets = {}
        
        self.setLayout(PyQt5.QtWidgets.QFormLayout())         
        
        buttonOK = PyQt5.QtWidgets.QPushButton('OK')
        buttonOK.setDefault(True)
        buttonCancel = PyQt5.QtWidgets.QPushButton('Cancel')
        buttonApply = PyQt5.QtWidgets.QPushButton('Apply')
        
        buttons = PyQt5.QtWidgets.QWidget()
        buttons.setLayout(PyQt5.QtWidgets.QHBoxLayout())
        buttons.layout().addStretch()
        buttons.layout().addWidget(buttonOK)                
        buttons.layout().addWidget(buttonCancel)
        buttons.layout().addWidget(buttonApply)
        
        self._widgetdialog = PyQt5.QtWidgets.QWidget()
        self._widgetdialog.setWindowTitle('Settings')   
        self._widgetdialog.setLayout(PyQt5.QtWidgets.QVBoxLayout())
        self._widgetdialog.layout().addWidget(self)
        self._widgetdialog.layout().addWidget(buttons)
        self._widgetdialog.layout().addStretch()
        
        self._dialogSettings = PyQt5.QtWidgets.QDialog()
        self._dialogSettings.setLayout(PyQt5.QtWidgets.QVBoxLayout())
        self._dialogSettings.layout().addWidget(self._widgetdialog)    
            
        buttonOK.clicked.connect(self._dialogSettings.accept)
        buttonOK.clicked.connect(self.apply_settings)
        buttonCancel.clicked.connect(self._dialogSettings.reject)
        buttonApply.clicked.connect(self.apply_settings)

    def save(self, element, xml_tag = ''):
        if element == None:
            return        
        elif type(element) == str:
            if xml_tag == '':
                tag = element
            else:
                tag = xml_tag
            out_element = xml.etree.ElementTree.Element(tag)
            elementTree = xml.etree.ElementTree.ElementTree(out_element)
        else:
            out_element = element
        
        for attrib_name in self._attribs.keys():
            subelement = xml.etree.ElementTree.Element(attrib_name)
            if self._attribs[attrib_name].attribtype == AttribType.text:
                subelement. text = self._attribs[attrib_name].value
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
            out_element.append(subelement)
        if type(element) == str:
            elementTree.write(element)
        return out_element
    
    def load(self, element, xml_tag = ''):
        if type(element) == str:
            if xml_tag == '':
                tag = element
            else:
                tag = xml_tag
            elementTree = xml.etree.ElementTree.ElementTree()
            elementTree.parse(element)
            if elementTree.getroot().tag == tag:
                element = elementTree.getroot()
            else:
                element = elementTree.getroot().find(tag)
            
        if element == None:
            return

        for attrib_name in self._attribs.keys():
            str_value = element.findtext(attrib_name)
            if str_value == None:
                continue
            if self._attribs[attrib_name].attribtype == AttribType.text:
                self.set(attrib_name,str_value)
            elif self._attribs[attrib_name].attribtype == AttribType.number:
                self.set(attrib_name,float(str_value))              
            elif self._attribs[attrib_name].attribtype == AttribType.number_int:
                self.set(attrib_name,int(str_value))
            elif self._attribs[attrib_name].attribtype == AttribType.options:
                self.set(attrib_name,str_value)
            elif self._attribs[attrib_name].attribtype == AttribType.check:
                self.set(attrib_name,bool(str_value))
        return element
    
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
            self.layout().addRow(app_attrib.description,self._widgets[name])
        elif app_attrib.attribtype == AttribType.number:
            self._widgets[name] = PyQt5.QtWidgets.QLineEdit(str(value))
            self._widgets[name].setValidator(PyQt5.QtGui.QDoubleValidator())
            self.layout().addRow(app_attrib.description,self._widgets[name])              
        elif app_attrib.attribtype == AttribType.number_int:
            self._widgets[name] = PyQt5.QtWidgets.QLineEdit(str(value))
            self._widgets[name].setValidator(PyQt5.QtGui.QIntValidator())
            self.layout().addRow(app_attrib.description,self._widgets[name])
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
        return self
    
    def exec_settings(self, title = None):
        self.get_settingsform()
        if title != None:
            self._dialogSettings.setWindowTitle(title)
        return self._dialogSettings.exec_()    
        
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
        