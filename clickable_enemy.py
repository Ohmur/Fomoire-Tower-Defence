'''
Created on 12.4.2016

@author: Rohmu
'''

from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtGui import QPainter


class ClickableEnemy(QAbstractButton):
    
    def __init__(self, enemy, parent):
        super(ClickableEnemy, self).__init__(parent)
        self.pixmap = enemy.picture
        self.parent = parent
        self.tower = enemy
    
        self.pressed.connect(self.click)
    
    
    def paintEvent(self, event):
        
        pix = self.pixmap
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(event.rect(), pix)
            
    
    def sizeHint(self):
        return self.pixmap.size()

    
    def click(self):
        self.parent.towerClick(self.tower)