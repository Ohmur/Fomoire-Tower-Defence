'''
Created on 9.4.2016

@author: Rohmu
'''

from globals import blockSize
from PyQt5.QtWidgets import QFrame
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtCore import Qt


class GameStats(QFrame):
    
    def __init__(self, parent):
        super(GameStats, self).__init__(parent)
        self.parent = parent
        self.initUI(self.parent.gameboard)    
    
    
    def initUI(self, gameboard): 

        #self.setStyleSheet("QFrame { background: #BCBCBC }") 
        self.setFixedSize((gameboard.width - 1)*blockSize, 20)
        self.show()
    
    
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawGameStats(event, qp)
        qp.end()


    def drawGameStats(self, event, qp):
        
        qp.setPen(QColor(0, 0, 0, 255))
        qp.drawText(event.rect(), Qt.AlignLeft, "Money: " + str(self.parent.gameboard.money))
        if self.parent.gameboard.currentWave < len(self.parent.gameboard.waves):
            qp.drawText(event.rect(), Qt.AlignCenter, "Wave: " + str(self.parent.gameboard.currentWave) + "/" + str(self.parent.gameboard.noOfWaves))
        else:
            qp.drawText(event.rect(), Qt.AlignCenter, "Wave: " + str(len(self.parent.gameboard.waves)) + "/" + str(self.parent.gameboard.noOfWaves))
        qp.drawText(event.rect(), Qt.AlignRight, "Lives " + str(self.parent.gameboard.currentLives) + "/" + str(self.parent.gameboard.startingLives))
