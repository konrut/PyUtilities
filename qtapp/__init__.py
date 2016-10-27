'''
Created on 27 lut 2016

@file: CQAppWindow.py
@author: Konrad Rutkowski

'''

import sys
import datetime
import xml.etree.ElementTree
import enum

from PyQt5 import QtWidgets, QtCore, QtGui
import PyQt5

class AppWidgetGroup(enum.Enum):
    pages = 'page'
    utilities = 'utility'

class AppWindow(QtWidgets.QMainWindow):
    '''
    classdocs
    '''
    def __init__(self):
        super(AppWindow,self).__init__()
        #params:
        self.name = 'Qt application'        
        
        self.resize(600,600)
        self.setWindowIcon(QtGui.QIcon("resources/pyIcon.png"))
        self.setWindowTitle(self.name)    
                
        self.statusBar = QtWidgets.QStatusBar()
        self.progressBar = QtWidgets.QProgressBar()
        self.statusBar.addPermanentWidget(self.progressBar)
        self.setStatusBar(self.statusBar)
        self.progressBar.setValue(0)
        self.progressBar.setFixedSize(self.progressBar.width()/2, self.progressBar.height())
        self.progressBar.setVisible(False)      

        #central widget:        
        self.mainWidget = QtWidgets.QWidget(self)
        self.mainWidget.setLayout(PyQt5.QtWidgets.QHBoxLayout())        
        
        self.msgLog = QtWidgets.QTextEdit(self)
        self.msgLog.setFixedHeight(100)
        self.msgLog.setReadOnly(True)
        
        self.setCentralWidget(QtWidgets.QWidget())
        self.centralWidget().setLayout(QtWidgets.QVBoxLayout())
        self.centralWidget().layout().addWidget(self.mainWidget)
        self.centralWidget().layout().addWidget(self.msgLog)        
                
        #Main menu bar:
        extractAction = QtWidgets.QAction("Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Exit the application')
        extractAction.triggered.connect(self.close)  
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu. addAction(extractAction) 
        
        self.menu_utilities = None
        
        #Content
        self.utilities = {}
        self.pages = {}
        
        self._settings_rootname = 'qtapp'                
        self._settings_file = 'settings.xml'                
        
    def home(self):
        self.setWidget(self.homeWgt)
        
    def message(self, msg):
        time = datetime.datetime.now()
        self.msgLog.append(time.strftime("[%H:%m:%S] - " + msg)) 

    def progress(self, progress):
        if progress >= 100:
            self.progressBar.setValue(100);
            self.progressBar.setVisible(False);
        else:
            self.progressBar.setValue(progress);
            self.progressBar.setVisible(True);  
        
    def set_currentpage(self, page_name):
        if not (page_name in self.pages.keys()):
            self.message('No page with specified name.')
            return
        
        self.mainWidget.layout().addWidget(self.pages[page_name])
         
    def add_page(self, page):
        if page.name in self.pages.keys():
            self.message('Adding page error. Page with given name already exists.')
            return
        
        self.pages[page.name] = page
        self.settings_load(page, AppWidgetGroup.pages)
        
        #Signals:
        page.sig_message.connect(self.message)        
        page.sig_progress.connect(self.progress) 
        
        self.set_currentpage(page.name)
        
    def add_utility(self, utility):
        if utility.name in self.utilities.keys():
            self.message('Adding utility error. Utility with given name already exists.')
            return
                
        utility_menu = utility.get_menu()
        if utility_menu != None:                    
            if self.menu_utilities == None:
                self.menu_utilities = self.menuBar().addMenu('&Utilities')            
            self.menu_utilities.addMenu(utility_menu)
        
        self.utilities[utility.name] = utility
        self.settings_load(utility, AppWidgetGroup.utilities)
        
        #Signals:
        utility.sig_message.connect(self.message)        
        utility.sig_progress.connect(self.progress) 
        
    def settings_save(self, widget = None, widget_group = None, file_name = ''):
        if file_name == '':
            file_name = self._settings_file
        
        if widget != None:
            elementTree = xml.etree.ElementTree.ElementTree()
            try:
                elementTree.parse(file_name)
            except FileNotFoundError:
                return
            
            root = elementTree.getroot()

            for element in elementTree.getroot().findall(widget_group.value):
                if element.get('name',None) == widget.name:
                    break
                else:                    
                    element = None
            if element == None:
                element = xml.etree.ElementTree.Element(widget_group.value, {'name':widget.name})
                root.append(element)
            else:             
                element.clear()     
                element.set('name',widget.name)       
            widget._settings_save(element)
            elementTree.write(file_name)
            return
            
        root = xml.etree.ElementTree.Element(self._settings_rootname,{'name':self.name})
        elementTree = xml.etree.ElementTree.ElementTree(root)

        for widget_group in [AppWidgetGroup.utilities, AppWidgetGroup.pages]: 
            if widget_group == AppWidgetGroup.utilities:
                for utility in self.utilities.values():
                    element = xml.etree.ElementTree.Element(widget_group.value, {'name':utility.name})
                    utility._settings_save(element)
                    root.append(element)
            elif widget_group == AppWidgetGroup.pages:
                for page in self.pages.values():
                    element = xml.etree.ElementTree.Element(widget_group.value, {'name':page.name})
                    page._settings_save(element)
                    root.append(element)
        
        elementTree.write(file_name)
        
    def settings_load(self, widget = None, widget_group = None, file_name = ''):
        if file_name == '':
            file_name = self._settings_file
        
        elementTree = xml.etree.ElementTree.ElementTree()
        try:
            elementTree.parse(file_name)
        except FileNotFoundError:
            return
        
        root = elementTree.getroot()   
             
        if widget != None:
            element = None
            for element in root.findall(widget_group.value):
                if element.get('name',None) == widget.name:
                    break
                else:                    
                    element = None
            if element == None:
                return
            widget._settings_load(element)
            return
        
        for element in root.findall("."):
            print(element.tag)
            if element.tag == AppWidgetGroup.utilities.value:
                self.utilities[element.get('name')]._settings_load(element)
            elif element.tag == AppWidgetGroup.pages.value:
                self.pages[element.get('name')]._settings_load(element)
                        
    def closeEvent(self, event):
        self.settings_save()
        event.accept()
        sys.exit()
        
        return
        choice = QtWidgets.QMessageBox.question(self, "Closing", "Do you realy want to quit?", QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        if choice == QtWidgets.QMessageBox.Yes:
            event.accept()
            sys.exit()
        else:
            event.ignore()
        
