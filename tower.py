'''
Created on 6.3.2016

@author: Rohmu
'''

import os.path
from PyQt5.QtGui import QPixmap
from math import sqrt
from projectile import *

class Tower(object):
    
    def __init__(self):
        self._position_x = 0
        self._position_y = 0
        self._lastShot = 0
    
    
    def getRange(self):
        return self._range
    
    
    def inRange(self, enemy):
        return int(sqrt(pow((self._position_x - enemy.posX), 2) + pow((self._position_y - enemy.posY), 2) )) <= self._range
    
    
    def getPrice(self):
        return self._price
    
    
    def getPicture(self):
        return self._picture
    
    
    def setPosition(self, x, y):
        self._position_x = x
        self._position_y = y
        
        
    def getPositionX(self):
        return self._position_x
    
    
    def getPositionY(self):
        return self._position_y
    
    
    def getPower(self):
        return self._power
    
    
    def getFireRate(self):
        return self._fireRate
    
    
    def getName(self):
        return self._name
    
    
    def getUpgradePrice(self):
        return self._upgradePrice
    
    
    def getLevel(self):
        return self._level

    
    def getMaxLevel(self):
        return self._maxLevel
    
    
    def getUpgradedPicture(self):
        return self._upgradedPicture
    
    
    def getLastShot(self):
        return self._lastShot
    
    
    def setLastShot(self, time):
        self._lastShot = time
    
    
    name = property(getName)
    range = property(getRange)
    fireRate = property(getFireRate)
    price = property(getPrice)
    upgradePrice = property(getUpgradePrice)
    power = property(getPower)
    level = property(getLevel)
    maxLevel = property(getMaxLevel)
    picture = property(getPicture)
    upgradedPicture = property(getUpgradedPicture)
    posX = property(getPositionX)
    posY = property(getPositionY)
    lastShot = property(getLastShot, setLastShot)
    

class Musketeer(Tower):
    
    def __init__(self):
        super().__init__()
        self._name = "Musketeer"
        self._range = 70
        self._fireRate = 15
        self._price = 100
        self._upgradePrice = 120
        self._power = 10
        self._size = 2
        self._level = 1
        self._maxLevel = 2
        self._picture = QPixmap(os.path.join('./Pictures/', "musketeer.png"))
        self._upgradedPicture = QPixmap(os.path.join('./Pictures/', "musketeer_upgraded.png"))
    
    
    def upgrade(self):
        self._power += self._power / 4
        self._range += self._range / 3
        self._fireRate -= 5
        self._level += 1
        
    
    def shoot(self, enemy):
        return Bullet(self, enemy)
        

class Cannon(Tower):
    
    def __init__(self):
        super().__init__()
        self._name = "Cannon"
        self._range = 100
        self._fireRate = 40
        self._price = 150
        self._upgradePrice = 180
        self._power = 35
        self._size = 2
        self._level = 1
        self._maxLevel = 2
        self._picture = QPixmap(os.path.join('./Pictures/', "cannon.png"))
        self._upgradedPicture = QPixmap(os.path.join('./Pictures/', "cannon_upgraded.png"))
        
        
    def upgrade(self):
        self._power += self._power / 2
        self._range += self._range / 4
        self._fireRate -= 3
        self._level += 1
        
        
    def shoot(self, enemy):
        return Cannonball(self, enemy)