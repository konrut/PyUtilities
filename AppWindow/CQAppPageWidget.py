'''
Created on 13 lip 2016

@author: Konrad Rutkowski
'''

from PyQt4 import QtGui, QtCore

class CQAppPageWidget(QtGui.QWidget):

    sigAppMessage = QtCore.pyqtSignal('QString')
    sigAppProgress = QtCore.pyqtSignal('int')

    def __init__(self, mainWindow):
        super(CQAppPageWidget,self).__init__()
        self.Name = 'WIN';
        
        self.sigAppMessage.connect(mainWindow.message)        
        self.sigAppProgress.connect(mainWindow.progress) 

    def appMessage(self, msg):
        msg = self.Name + ': ' + msg;
        self.sigAppMessage.emit(msg);
        
    def appProgress(self, progress):
        self.sigAppProgress.emit(progress);
        
    def setName(self, name):
        self.Name = name;

    '''
        
        vLayout = QtGui.QVBoxLayout()
        
        btnClose = QtGui.QPushButton("Quit")   
            
        vLayout.addWidget(btnClose)
        vLayout.addStretch()
        
        self.setLayout(vLayout)
    '''
        