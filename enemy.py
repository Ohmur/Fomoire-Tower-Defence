'''
Created on 24.3.2016

@author: Rohmu
'''
import os.path
from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtGui import QPainter, QPixmap
from PyQt5.QtCore import QPoint
from globals import blockSize
from math import floor 


class Enemy(QAbstractButton):
    
    def __init__(self, path, parent):
        super(Enemy, self).__init__(parent)
        self._parent = parent
        self._path = path
        self._isFinished = False
        self._isDead = False
        
        self._blocksMoved = 0
        self._currentBlock = self._path[0]
        self._nextBlock = self._path[1]
        
        # We want the enemy to be in the middle of the current block
        self._position_x = self._path[0][0] * blockSize + blockSize / 2
        self._position_y = self._path[0][1] * blockSize + blockSize / 2
        
        # We need to know which way the enemy is moving in order to keep them in the middle of the path at all times
        self._direction = None
        
        if self._currentBlock[0] < self._nextBlock[0]:
            self._direction = "R"
        elif self._currentBlock[0] > self._nextBlock[0]:
            self._direction = "L"
        elif self._currentBlock[1] < self._nextBlock[1]:
            self._direction = "D"
        elif self._currentBlock[1] > self._nextBlock[1]:
            self._direction = "U"    
            
        self.pressed.connect(self.click)
    
    
    def moveEnemy(self):
        # First we check which way the enemy needs to move and how much and move them
        if self._currentBlock[0] < self._nextBlock[0]:
            if self._direction == "R":
                self._position_x += self._speed
            elif self._direction == "D":
                if (self._position_y + self._speed) < (self._currentBlock[1] * blockSize + blockSize / 2):
                    self._position_y += self._speed
                else:
                    x = (self._position_y + self._speed) % (self._currentBlock[1] * blockSize + blockSize / 2)    
                    y = self._speed - x
                    self._position_y += y
                    self._position_x += x
                    self._direction = "R"
            elif self._direction == "U":
                if (self._position_y - self._speed) > (self._currentBlock[1] * blockSize + blockSize / 2):
                    self._position_y -= self._speed
                else:
                    x = (self._currentBlock[1] * blockSize + blockSize / 2) % (self._position_y - self._speed)
                    y = self._speed - x
                    self._position_y -= y
                    self._position_x += x
                    self._direction = "R"
                
        elif self._currentBlock[0] > self._nextBlock[0]:
            if self._direction == "L":
                self._position_x -= self._speed
            elif self._direction == "D":
                if (self._position_y + self._speed) < (self._currentBlock[1] * blockSize + blockSize / 2):
                    self._position_y += self._speed
                else:
                    x = (self._position_y + self._speed) % (self._currentBlock[1] * blockSize + blockSize / 2)    
                    y = self._speed - x
                    self._position_y += y
                    self._position_x -= x
                    self._direction = "L"
            elif self._direction == "U":
                if (self._position_y - self._speed) > (self._currentBlock[1] * blockSize + blockSize / 2):
                    self._position_y -= self._speed
                else:
                    x = (self._currentBlock[1] * blockSize + blockSize / 2) % (self._position_y - self._speed)
                    y = self._speed - x
                    self._position_y -= y
                    self._position_x -= x
                    self._direction = "L"    
                
        elif self._currentBlock[1] < self._nextBlock[1]:
            if self._direction == "D":
                self._position_y += self._speed
            elif self._direction == "R":
                if (self._position_x + self._speed) < (self._currentBlock[0] * blockSize + blockSize / 2):
                    self._position_x += self._speed
                else:
                    y = (self._position_x + self._speed) % (self._currentBlock[0] * blockSize + blockSize / 2)    
                    x = self._speed - y
                    self._position_y += y
                    self._position_x += x
                    self._direction = "D" 
            elif self._direction == "L":
                if (self._position_x - self._speed) > (self._currentBlock[0] * blockSize + blockSize / 2):
                    self._position_x -= self._speed
                else:
                    y = (self._currentBlock[0] * blockSize + blockSize / 2) % (self._position_x - self._speed) 
                    x = self._speed - y
                    self._position_y += y
                    self._position_x -= x
                    self._direction = "D" 
                          
        elif self._currentBlock[1] > self._nextBlock[1]:
            if self._direction == "U":
                self._position_y -= self._speed
            elif self._direction == "R":
                if (self._position_x + self._speed) < (self._currentBlock[0] * blockSize + blockSize / 2):
                    self._position_x += self._speed
                else:
                    y = (self._position_x + self._speed) % (self._currentBlock[0] * blockSize + blockSize / 2)    
                    x = self._speed - y
                    self._position_y -= y
                    self._position_x += x
                    self._direction = "U" 
            elif self._direction == "L":
                if (self._position_x - self._speed) > (self._currentBlock[0] * blockSize + blockSize / 2):
                    self._position_x -= self._speed
                else:
                    y = (self._currentBlock[0] * blockSize + blockSize / 2) % (self._position_x - self._speed)
                    x = self._speed - y
                    self._position_y -= y
                    self._position_x -= x
                    self._direction = "U" 
        
        # Then we check if they've moved to another block
        if floor(self._position_x / blockSize) != self._currentBlock[0]:
            self._blocksMoved += 1
            self._currentBlock = self._path[self._blocksMoved]
            if self._blocksMoved < len(self._path) - 1:
                self._nextBlock = self._path[self._blocksMoved + 1]    
                
        elif floor(self._position_y / blockSize) != self._currentBlock[1]:
            self._blocksMoved += 1
            self._currentBlock = self._path[self._blocksMoved]
            if self._blocksMoved < len(self._path) - 1:
                self._nextBlock = self._path[self._blocksMoved + 1]
    
    
    def checkIfFinished(self):
        if self._blocksMoved == len(self._path) - 1:
            self.setIsFinished(True)
            self.hide()
            return True
        else:
            return False
    
    
    def paintEvent(self, event):
        
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(event.rect(), self._picture)
            
    
    def sizeHint(self):
        return self.picture.size()

    
    def click(self):
        self._parent.enemyClick(self)
    
        
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
    
    
    def getCenter(self):
        return QPoint(self._position_x, self._position_y)
    
    
    def getDirection(self):
        return self._direction
    
    
    def getPicture(self):
        return self._picture
    
    
    def getName(self):
        return self._name
    

    def getCurrentBlock(self):
        return self._currentBlock
    
    
    def setCurrentBlock(self, coordinates):
        self._currentBlock = coordinates
        
    
    def getBlocksMoved(self):
        return self._blocksMoved


    def getSpeed(self):
        return self._speed
    
    
    def getHealth(self):
        return self._health
    
    
    def getHit(self, damage):
        self._health -= damage
        
    
    def checkIfDead(self):
        if self._health <= 0:
            self._isDead = True
            self._picture = self._deadPicture
            return True
        else:
            return False
        
        
    def getReward(self):
        return self._reward


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
    name = property(getName)
    blocksMoved = property(getBlocksMoved)
    getCenter = property(getCenter)
    reward = property(getReward)


class Barbarian(Enemy):
    
    def __init__(self, path, parent):
        super().__init__(path, parent)
        self._name = "Barbarian"
        self._health = 100
        self._speed = 3
        self._picture = QPixmap(os.path.join('./Pictures/', "barbarian.png"))
        self._reward = 20
        self._deadPicture = QPixmap(os.path.join('./Pictures/', "blood.png"))
           
        
class Berserker(Enemy):
    
    def __init__(self, path, parent):
        super().__init__(path, parent)
        self._name = "Berserker"
        self._health = 80
        self._speed = 4
        self._picture = QPixmap(os.path.join('./Pictures/', "berserker.png"))
        self._deadPicture = QPixmap(os.path.join('./Pictures/', "blood2.png"))
        self._reward = 30
        
        