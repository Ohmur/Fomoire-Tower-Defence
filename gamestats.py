'''
Created on 9.4.2016

@author: Rohmu
'''

import os.path
from globals import blockSize
from PyQt5.QtWidgets import QFrame, QLabel
from PyQt5.QtGui import QPainter, QColor, QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.Qt import QHBoxLayout, QGridLayout


class GameStats(QFrame):
    
    def __init__(self, parent):
        super(GameStats, self).__init__(parent)
        self.parent = parent
        self.initUI(self.parent.gameboard)
        
    
    def initUI(self, gameboard): 

        self.setFixedSize((gameboard.width - 1)*blockSize, 40)
        
        moneypix = QPixmap(os.path.join('./Pictures/', "money.png"))
        moneyLabel = QLabel(self)
        moneyLabel.setPixmap(moneypix)
        moneyLabel.setFixedSize(moneypix.size())
        moneyLabel.move(5, 10)
        moneyLabel.show()
        
        
        wavepix = QPixmap(os.path.join('./Pictures/', "waves.png"))
        waveLabel = QLabel(self)
        waveLabel.setPixmap(wavepix)
        waveLabel.setFixedSize(wavepix.size())
        waveLabel.move((gameboard.width - 1)*blockSize / 2 - 82, 8)
        waveLabel.show()
        
        self.hearts = []
        heart = QPixmap(os.path.join('./Pictures/', 'heart.png'))
        self.heart_lost = QPixmap(os.path.join('./Pictures/', 'heart_lost.png'))
        i = 1
        
        while i <= self.parent.gameboard.startingLives:
            heartLabel = QLabel(self)
            heartLabel.setPixmap(heart)
            self.hearts.append([True, heartLabel])
            heartLabel.move((gameboard.width - 1)*blockSize - (2 + i * 12), 18)
            heartLabel.show()
            i += 1
        
        self.show()
    
    
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawGameStats(event, qp)
        qp.end()


    def drawGameStats(self, event, qp):
        
        qp.setPen(QColor(0, 0, 0, 255))
        qp.drawText(60, 28 ,str(self.parent.gameboard.money))
        
        if self.parent.gameboard.currentWave < len(self.parent.gameboard.waves):
            qp.drawText((self.parent.gameboard.width - 1)*blockSize / 2 + 15, 28, str(self.parent.gameboard.currentWave) + " / " + str(self.parent.gameboard.noOfWaves))
        else:
            qp.drawText((self.parent.gameboard.width - 1)*blockSize / 2 + 15, 28, str(len(self.parent.gameboard.waves)) + " / " + str(self.parent.gameboard.noOfWaves))
        
        if self.parent.gameboard.startingLives > self.parent.gameboard.currentLives and self.hearts[self.parent.gameboard.currentLives][0] == True:
            self.hearts[self.parent.gameboard.currentLives][1].setPixmap(self.heart_lost)
            self.hearts[self.parent.gameboard.currentLives][0] = False
        