'''
Created on 6.3.2016

@author: Rohmu
'''

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap
from math import sqrt

class Tower(object):
    
    def __init__(self):
        self.position_x = 0
        self.position_y = 0
        self.level = 1

    
    def getCenter(self):
        return QPoint(self.position_x + (self.size*20/2), self.position_y + self.size*20/2)
    
    
    def getRange(self):
        return self.range
    
    
    def inRange(self, enemy):
        return int(sqrt(pow((self.getCenter().x() - enemy.getCenter().x()), 2) + pow((self.getCenter().y() - enemy.getCenter().y()), 2) )) <= self.shotrange
    
    
    def getPrice(self):
        return self.cost
    
    
    def getPicture(self):
        return self.picture
        

class Musketeer(Tower):
    
    def __init__(self):
        self.name = "Musketeer"
        self.range = 50
        self.fireRate = 10
        self.cost = 100
        self.damage = 40
        self.size = 2
        self.picture = QPixmap("musketeer.png")
        

class Cannon(Tower):
    
    def __init__(self):    
        self.name = "Cannon"
        self.range = 100
        self.fireRate = 30
        self.cost = 150
        self.damage = 80
        self.size = 2
        self.picture = QPixmap("cannon.png")