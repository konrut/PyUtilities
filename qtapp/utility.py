'''
Created on 13 oct 2016

@author: Konrad Rutkowski
'''

import qtapp.widget

class AppUtility(qtapp.widget.AppWidget):
    '''
    classdocs
    '''


    def __init__(self, name):
        '''
        Constructor
        '''
        super(AppUtility,self).__init__()
        self.set_name(name)        
        
