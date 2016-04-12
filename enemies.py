'''
Created on 24.3.2016

@author: Rohmu
'''

from PyQt5.QtGui import QPixmap
from math import floor 


class Enemy(object):
    
    def __init__(self, path):
        self._path = path
        self._size = 2
        self._isFinished = False
        self._isDead = False

        self._position_x = self._path[0][0]*20
        self._position_y = self._path[0][1]*20
        
        
        self._blocksMoved = 0
        self._currentBlock = self._path[0]
        self._nextBlock = self._path[1]
    
    
    def move(self):
        # First we check which way the enemy needs to move and move them
        if self._currentBlock[0] < self._nextBlock[0]:
            self._position_x += self._speed
        elif self._currentBlock[0] > self._nextBlock[0]:
            self._position_x -= self._speed
        elif self._currentBlock[1] < self._nextBlock[1]:
            self._position_y += self._speed
        elif self._currentBlock[1] > self._nextBlock[1]:
            self._position_y -= self._speed
        
        # Then we check if they've moved to another block
        if floor(self._position_x / 20) != self._currentBlock[0]:
            self._blocksMoved += 1
            self._currentBlock = self._path[self._blocksMoved]
            if self._blocksMoved < len(self._path):
                self._nextBlock = self._path[self._blocksMoved + 1]    
                
        elif floor(self._position_y / 20) != self._currentBlock[1]:
            self._blocksMoved += 1
            self._currentBlock = self._path[self._blocksMoved]
            if self._blocksMoved < len(self._path):
                self._nextBlock = self._path[self._blocksMoved + 1]
    
    
    def checkIfFinished(self):
        if self._blocksMoved == len(self._path):
            self.setIsFinished(True)
            return True
        else:
            return False
    
        
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


    def getCurrentBlock(self):
        return self._currentBlock
    
    
    def setCurrentBlock(self, coordinates):
        self._currentBlock = coordinates


    def getSpeed(self):
        return self._speed
    
    
    def getHealth(self):
        return self._health


    path = property(getPath)
    isFinished = property(getIsFinished, setIsFinished)
    isDead = property(getIsDead, setIsDead)
    posX = property(getPositionX)
    posY = property(getPositionY)
    direction = property(getDirection)   
    picture = property(getPicture)
    currentBlock = property(getCurrentBlock, setCurrentBlock)
    speed = property(getSpeed)
    health = property(getHealth)


class Barbarian(Enemy):
    
    def __init__(self, path):
        super().__init__(path)
        self._name = "Barbarian"
        self._health = 100
        self._speed = 3
        self._isFinished = False
        self._picture = QPixmap("barbaari.png")
        
        
class Berserker(Enemy):
    
    def __init__(self, path):
        super().__init__(path)
        self._name = "Berserker"
        self._health = 80
        self._speed = 4
        self._isFinished = False
        self._picture = QPixmap("berserker.png")