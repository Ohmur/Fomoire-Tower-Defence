'''
Created on 10.4.2016

@author: Rohmu
'''

from PyQt5.QtWidgets import QAbstractButton
from PyQt5.QtGui import QPainter


class BuyButton(QAbstractButton):
    # This is a picture button that changes appearance when howered and clicked.
    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, parent):
        super(BuyButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)


    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)


    def enterEvent(self, event):
        self.update()


    def leaveEvent(self, event):
        self.update()


    def sizeHint(self):
        return self.pixmap.size()