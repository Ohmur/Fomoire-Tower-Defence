'''
Created on 16.4.2016

@author: Rohmu
'''

from math import sqrt

class Projectile(object):
    
    def __init__(self, origin, destination):
        self._origin = origin
        self._destination = destination
        self._posX = origin.posX
        self._posY = origin.posY
        self._isFinished = False
        
    
    def move(self):
        
        fullDistance = sqrt(pow((self._posX - self._destination.posX), 2) + pow((self._posY - self._destination.posY), 2))
        
        if self._speed < fullDistance:
            x = self._speed/fullDistance*sqrt(pow(self._posX - self._destination.posX))
            y = self._speed/fullDistance*sqrt(pow(self._posY - self._destination.posY))
        else:
            x = sqrt(pow(self._posX - self._destination.posX))
            y = sqrt(pow(self._posY - self._destination.posY))
            
        self._posX += x
        self._posY += y
        
        
    def checkIfHit(self):
        
        if self._posX == self._destination.posX and self._posY == self._destination.posY:
            self._destination.takeHit(self._damage)
            self._Finished = True
            
    
    def getIsFinished(self):
        return self._isFinished
    

    def getDestination(self):
        return self._destination

    
    isFinished = property(getIsFinished)
    destination = property(getDestination)


class Bullet(Projectile):
    
    def __init__(self, origin, destination):
        super().__init__(origin, destination)
        self._speed = 10
        self._damage = origin.power
    
    
class Cannonball(Projectile):
    
    def __init__(self, origin, destination):
        super().__init__(origin, destination)
        self._speed = 5
        self._damage = origin.power