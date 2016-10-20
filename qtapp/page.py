'''
Created on 20 oct 2016

@author: Konrad
'''

import qtapp.widget

class AppPage(qtapp.widget.AppWidget):

    def __init__(self, name):
        '''
        Constructor
        '''
        super(AppPage,self).__init__()
        self.set_name(name)
        