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

    
    def getCenter(self):
        return QPoint(self.position_x, self.position_y)
    
    
    def getRange(self):
        return self.range
    
    
    def inRange(self, enemy):
        return int(sqrt(pow((self.getCenter().x() - enemy.getCenter().x()), 2) + pow((self.getCenter().y() - enemy.getCenter().y()), 2) )) <= self.shotrange
    
    
    def getPrice(self):
        return self.cost
    
    
    def getPicture(self):
        return self.picture
    
    
    def setPosition(self, x, y):
        self.position_x = x
        self.position_y = y
        
        
    def getPositionX(self):
        return self.position_x
    
    
    def getPositionY(self):
        return self.position_y
    
    
    def getPower(self):
        return self.power
    
    
    def getFireRate(self):
        return self.fireRate
    
    
    def getName(self):
        return self.name
    
    
    def getUpgradePrice(self):
        return self.upgradeCost
    
    
    def getLevel(self):
        return self.level

    
    def getMaxLevel(self):
        return self.maxLevel


class Musketeer(Tower):
    
    def __init__(self):
        self.name = "Musketeer"
        self.range = 65
        self.fireRate = 2
        self.cost = 100
        self.upgradeCost = 120
        self.power = 40
        self.size = 2
        self.level = 1
        self.maxLevel = 2
        self.picture = QPixmap("musketeer.png")
    
    
    def upgrade(self):
        self.power += self.power / 4
        self.range += self.range / 3
        self.fireRate -= 1
        self.level += 1
        

class Cannon(Tower):
    
    def __init__(self):    
        self.name = "Cannon"
        self.range = 100
        self.fireRate = 3
        self.cost = 150
        self.upgradeCost = 120
        self.power = 80
        self.size = 2
        self.level = 1
        self.maxLevel = 2
        self.picture = QPixmap("cannon.png")
        
    def upgrade(self):
        self.power += self.power / 2
        self.range += self.range / 4
        self.fireRate -= 1
        self.level += 1