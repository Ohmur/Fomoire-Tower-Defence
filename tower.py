'''
Created on 6.3.2016

@author: Rohmu
'''

from PyQt5.QtCore import QPoint

class Tower(object):

    ARCHER = 0
    CANNON = 1
    
    def __init__(self):
        self.position_x = 0
        self.position_y = 0
        self.level = 1
    
    def getCenter(self):
        #print self.size
        return QPoint(self.position_x + (self.size*20/2), self.position_y + self.size*20/2)