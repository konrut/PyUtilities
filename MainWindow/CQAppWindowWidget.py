'''
Created on 13 lip 2016

@author: Konrad Rutkowski
'''

from PyQt4 import QtGui, QtCore

class CQAppWindowWidget(QtGui.QWidget):    
    
    sigMsgPrint = QtCore.pyqtSignal('QString')

    def __init__(self, mainWindow):
        super(CQAppWindowWidget,self).__init__()
        
        self.sigMsgPrint.connect(mainWindow.msgPrint)


    def msgPrint(self, msg):
        self.sigMsgPrint.emit(msg);

    '''
        
        vLayout = QtGui.QVBoxLayout()
        
        btnClose = QtGui.QPushButton("Quit")   
            
        vLayout.addWidget(btnClose)
        vLayout.addStretch()
        
        self.setLayout(vLayout)
    '''
        