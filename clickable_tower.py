'''
Created on 10.4.2016

@author: Rohmu
'''

from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtGui import QPainter

class ClickableTower(QAbstractButton):
    # This is the physical version of a tower. With little tweaking I could probably make just one tower class.
    
    def __init__(self, tower, parent):
        super(ClickableTower, self).__init__(parent)
        self.pixmap = tower.picture
        self.upgraded = tower.upgradedPicture
        self.parent = parent
        self.tower = tower
    
        self.pressed.connect(self.click)
    
    
    def paintEvent(self, event):
        
        if self.tower.level == 2:
            pix = self.upgraded
        else:
            pix = self.pixmap
            
        painter = QPainter()
        painter.begin(self)
        painter.drawPixmap(event.rect(), pix)
        
    
    def enterEvent(self, event):
        self.parent.getParent().setIsTowerBeingHovered(True, self.tower)
        self.parent.getParent().update()


    def leaveEvent(self, event):
        self.parent.getParent().setIsTowerBeingHovered(False, None)
        self.parent.getParent().update()
    
    
    def sizeHint(self):
        return self.pixmap.size()

    
    def click(self):
        self.parent.towerClick(self.tower)