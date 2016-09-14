'''
Created on 27 lut 2016

@file: CQMainWindow.py
@author: Konrad Rutkowski
'''
import sys
import datetime
from PyQt4 import QtGui #QtCore

class CQMainWindow(QtGui.QMainWindow):
    '''
    classdocs
    '''
    def __init__(self):
        super(CQMainWindow,self).__init__()
        
        self.setGeometry(50,50,600,600)
        self.setWindowIcon(QtGui.QIcon("pyIcon.png"))
        self.setWindowTitle("My application")    
                
        self.statusBar = QtGui.QStatusBar()
        self.progressBar = QtGui.QProgressBar()
        self.statusBar.addPermanentWidget(self.progressBar)
        self.setStatusBar(self.statusBar)
        self.progressBar.setValue(0)
        self.progressBar.setFixedSize(self.progressBar.width()/2, self.progressBar.height())
        self.progressBar.setVisible(False);
        
        #central widget:
        centralWidget = QtGui.QWidget()
        self.setCentralWidget(centralWidget)
        
        vLayout = QtGui.QVBoxLayout()
        self.mainWidget = QtGui.QWidget(self)
        vLayout.addWidget(self.mainWidget)
        
        self.msgLog = QtGui.QTextEdit(self)
        self.msgLog.setFixedHeight(100)
        self.msgLog.setReadOnly(True)
        vLayout.addWidget(self.msgLog)
        
        self.centralWidget().setLayout(vLayout)
                
        #Main menu bar:
        extractAction = QtGui.QAction("Exit", self)
        extractAction.setShortcut("Ctrl+Q")
        extractAction.setStatusTip('Exit the application')
        extractAction.triggered.connect(self.close_app)  
        
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu('&File')
        fileMenu.addAction(extractAction) 
                
        
    def home(self):
        self.setWidget(self.homeWgt)
        
    def msgPrint(self, msg):
        time = datetime.datetime.now()
        self.msgLog.append(time.strftime("[%H:%m:%S] - " + msg))  
        
    def setWidget(self, widget):
        vLayout = QtGui.QVBoxLayout()  
        vLayout.addWidget(widget)
        self.mainWidget.setLayout(vLayout);        
                
    def close_app(self):
        choice = QtGui.QMessageBox.question(self, "Closing", "Do you realy want to quit?", QtGui.QMessageBox.No, QtGui.QMessageBox.Yes)
        if choice == QtGui.QMessageBox.Yes:
            sys.exit()
        else:
            pass
        
