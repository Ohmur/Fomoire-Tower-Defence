'''
Created on 24.3.2016

@author: Rohmu
'''
from PyQt5.QtGui import QPixmap


class Enemy(object):
    def __init__(self, path):
        self.path = path
        self.size = 2
        self.isFinished = False
        self.isDead = False

        self.position_x = self.path[0][0]*20
        self.position_y = self.path[0][1]*20
        
        self.current_block = self.path[0]
        self.direction = "RIGHT"
        



class Barbarian(Enemy):
    def __init__(self, path):
        self.name = "Barbarian"
        self.health = 100
        self.speed = 3
        self.picture = QPixmap("barbaari.png")