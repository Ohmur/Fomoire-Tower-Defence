'''
Created on 16.4.2016

@author: Rohmu
'''

class Projectile(object):
    
    def __init__(self, origin, destination):
        self._origin = origin
        self._destination = destination
        self._posX = origin.posX
        self._posY = origin.posY
        
    
    def move(self):
        return -1


class Bullet(Projectile):
    
    def __init__(self, origin, destination):
        self._speed = 10
    
    
class Cannonball(Projectile):
    
    def __init__(self, origin, destination):
        self._speed = 5