'''
Created on 13 oct 2016

@author: Drakon
'''

import qtapp.utility
import PyQt5.QtWidgets
import xml.etree.ElementTree

import subprocess


class AppUtilSvn(qtapp.utility.AppUtility):
    '''
    classdocs
    '''

    def __init__(self, name = 'SVN'):
        '''
        Constructor
        '''
        super(AppUtilSvn,self).__init__(name)
        
        self._add_attrib('SVN_bin', '', description = 'SVN bin folder')        
        self._add_attrib('SVN_dir', '', description = 'SVN directory')
        self._add_attrib('SVN_access', '', description = 'Direct access directory')        
        
        #Actions:
        action_settings = PyQt5.QtWidgets.QAction('Settings', self)
        action_settings.setStatusTip('SQL connection settings')
        action_settings.triggered.connect(self.exec_settings)  
        self._add_menuaction(action_settings.text(), action_settings)
        
        action_test = PyQt5.QtWidgets.QAction('debug', self)
        action_test.setStatusTip('Test action')
        action_test.triggered.connect(self._test)  
        self._add_menuaction(action_test.text(), action_test)
                
    def put(self, file_dir, svn_dir, comment = ''):
        subprocess.call([self.get_attrib('SVN_bin') + 'svnmucc', '--non-interactive',  '-m', comment,'put', file_dir, svn_dir])         
        
    def copy(self, svn_dir, dest_dir, rev = ''):
        subprocess.call([self.get_attrib('SVN_bin') + 'svnmucc', '--non-interactive',  'cp', rev, svn_dir, dest_dir])        
        
    def _test(self):
        element = xml.etree.ElementTree.Element(self.name)
        elementTree = xml.etree.ElementTree.ElementTree(element = self._attribs.save(element))
        elementTree.write('tmp.xml')
        #self.put(PyQt5.QtWidgets.QFileDialog.getOpenFileName()[0],'svn://diskstation/library/footprints/tmp','test')
    
