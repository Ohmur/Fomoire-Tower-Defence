'''
Created on 16.4.2016

@author: Rohmu
'''

from math import sqrt

class Projectile(object):
    
    def __init__(self, origin, destination):
        self._origin = origin
        self._damage = origin.power
        self._destination = destination
        self._posX = origin.posX
        self._posY = origin.posY
        self._isFinished = False
        
    
    def move(self):
        
        fullDistance = sqrt(pow(self._posX - self._destination.posX, 2) + pow(self._posY - self._destination.posY, 2))
        
        if self._speed < fullDistance:
            x = self._speed/fullDistance*sqrt(pow(self._posX - self._destination.posX, 2))
            y = self._speed/fullDistance*sqrt(pow(self._posY - self._destination.posY, 2))
        else:
            x = sqrt(pow(self._posX - self._destination.posX, 2))
            y = sqrt(pow(self._posY - self._destination.posY, 2))
            
        if self._posX < self._destination.posX:
            self._posX += x
        else:
            self._posX -= x  
        
        if self._posY < self._destination.posY:
            self._posY += y
        else:
            self._posY -= y  
        
        
    def checkIfHit(self):
        
        if self._posX == self._destination.posX and self._posY == self._destination.posY:
            self._destination.getHit(self._damage)
            self._isFinished = True
            return True
        else:
            return False
            
    
    def getIsFinished(self):
        return self._isFinished
    

    def getDestination(self):
        return self._destination
    
    
    def getName(self):
        return self._name
    
    
    def getPosX(self):
        return self._posX
    
    
    def getPosY(self):
        return self._posY
    
    
    def getDamage(self):
        return self._damage
        
    
    isFinished = property(getIsFinished)
    destination = property(getDestination)
    name = property(getName)
    posX = property(getPosX)
    posY = property(getPosY)
    damage = property(getDamage)


class Bullet(Projectile):
    
    def __init__(self, origin, destination):
        super().__init__(origin, destination)
        self._speed = 8
        self._name = "Bullet"
    
    
class Cannonball(Projectile):
    
    def __init__(self, origin, destination):
        super().__init__(origin, destination)
        self._speed = 6
        self._name = "Cannonball"
        