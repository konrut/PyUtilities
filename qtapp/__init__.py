'''
Created on 27 lut 2016

@file: CQAppWindow.py
@author: Konrad Rutkowski

'''

import sys
import datetime
from PyQt5 import QtWidgets, QtCore, QtGui

class AppWindow(QtWidgets.QMainWindow):
    '''
    classdocs
    '''
    def __init__(self):
        super(AppWindow,self).__init__()
        
        self.setGeometry(50,50,600,600)
        self.setWindowIcon(QtGui.QIcon("resources/pyIcon.png"))
        self.setWindowTitle("My application")    
                
        self.statusBar = QtWidgets.QStatusBar()
        self.progressBar = QtWidgets.QProgressBar()
        self.statusBar.addPermanentWidget(self.progressBar)
        self.setStatusBar(self.statusBar)
        self.progressBar.setValue(0)
        self.progressBar.setFixedSize(self.progressBar.width()/2, self.progressBar.height())
        self.progressBar.setVisible(False)
        
        
        #self.destroyed.connect(self.app_close)
        #central widget:
        centralWidget = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget)
        
        vLayout = QtWidgets.QVBoxLayout()
        self.mainWidget = QtWidgets.QWidget(self)
        vLayout.addWidget(self.mainWidget)
        
        self.msgLog = QtWidgets.QTextEdit(self)
        self.msgLog.setFixedHeight(100)
        self.msgLog.setReadOnly(True)
        vLayout.addWidget(self.msgLog)
        
        self.centralWidget().setLayout(vLayout)
                
        #Main menu bar:
        extractAction = QtWidgets.QAction("Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Exit the application')
        extractAction.triggered.connect(self.close)  
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu. addAction(extractAction) 
        
        self.menuUtilities = None
        
        #Utilities
        self.utilities = {}
                
        
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
        
    def set_currentpage(self, widget):
        vLayout = QtWidgets.QVBoxLayout()  
        vLayout.addWidget(widget)
        self.mainWidget.setLayout(vLayout);   
        
    def add_utility(self, utility):
        if utility.name in self.utilities:
            self.message('Adding utility error. Utility with given name already exists.')
            return
                
        utility_menu = utility.get_menu()
        if utility_menu == None:
            return
        
        if self.menuUtilities == None:
            self.menuUtilities = self.menuBar().addMenu('&Utilities')
            
        self.menuUtilities.addMenu(utility_menu)
        self.utilities[utility.name] = utility
                
    def closeEvent(self, event):
        event.accept()
        return
        choice = QtWidgets.QMessageBox.question(self, "Closing", "Do you realy want to quit?", QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
        if choice == QtWidgets.QMessageBox.Yes:
            event.accept()
            sys.exit()
        else:
            event.ignore()
        
