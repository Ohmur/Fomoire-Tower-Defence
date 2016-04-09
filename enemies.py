'''
Created on 24.3.2016

@author: Rohmu
'''
from PyQt5.QtGui import QPixmap


class Enemy(object):
    def __init__(self, path):
        self._path = path
        self._size = 2
        self._isFinished = False
        self._isDead = False

        self._position_x = self.path[0][0]*20
        self._position_y = self.path[0][1]*20
        
        self._current_block = self.path[0]
        self._direction = "RIGHT"
        

    def getPath(self):
        return self._path
    
    
    def getIsFinished(self):
        return self._isFinished
    
    
    def setIsFinished(self, boolean):
        self._isFinished = boolean

    
    def getIsDead(self):
        return self._isDead
    
    
    def setIsDead(self, boolean):
        self._isDead = boolean
        
    
    def getPositionX(self):
        return self._position_x
    
    
    def getPositionY(self):
        return self._position_y
    
    
    def getDirection(self):
        return self._direction
    
    
    def getPicture(self):
        return self._picture


    path = property(getPath)
    isFinished = property(getIsFinished, setIsFinished)
    isDead = property(getIsDead, setIsDead)
    posX = property(getPositionX)
    posY = property(getPositionY)
    direction = property(getDirection)   
    picture = property(getPicture)


class Barbarian(Enemy):
    def __init__(self, path):
        self._name = "Barbarian"
        self._health = 100
        self._speed = 3
        self._picture = QPixmap("barbaari.png")