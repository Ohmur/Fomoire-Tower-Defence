'''
Created on 9.4.2016

@author: Rohmu
'''

import os.path
from PyQt5.QtWidgets import QGridLayout, QFrame, QPushButton, QLabel, QLCDNumber
from globals import *
from tower import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.Qt import QHBoxLayout, QVBoxLayout, QBasicTimer
from buy_button import BuyButton


class BottomButtons(QFrame):
    
    def __init__(self, parent):
        super(BottomButtons, self).__init__(parent)
        self.parent = parent
        self.isPaused = False
        self.seconds = 0
        self.clockTimer = QBasicTimer()
        self.clockTimer.start(1000, self)
        self.initUI(self.parent.gameboard)
        
        
    def initUI(self, gameboard): 
        
        self.setStyleSheet("QWidget { background: #BCBCBC}")
        self.setFrameStyle(QFrame.Sunken | QFrame.StyledPanel)
        self.setFixedSize((gameboard.width - 1)*blockSize, 120)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        
        towerLabel = QLabel()
        towerLabel.setPixmap(QPixmap(os.path.join('./Pictures/', "tower.png")))
        
        vbox.addWidget(towerLabel)
        
        vbox.addLayout(hbox)
        self.grid.addLayout(vbox, 0, 0)
        
        towers = gameboard.getTowers()
        i = 0
        buttons = 0
        
        # We go through the list of different towers in the map and add buttons for them to the bottom left corner of the screen.
        while i < len(towers):
            if towers[i] == "t1":
                self.musketeerButton = BuyButton(QPixmap(os.path.join('./Pictures/', "musketeer_buybutton.png")), QPixmap(os.path.join('./Pictures/', "musketeer_buybutton_hover.png")), QPixmap(os.path.join('./Pictures/', "musketeer_buybutton_pressed.png")), self)
                self.musketeerButton.move(buttons*towerButtonSize + 10, 50)
                self.musketeerButton.clicked.connect(self.musketeerButtonClick)
                hbox.addWidget(self.musketeerButton)
                buttons += 1
            elif towers[i] == "t2":
                self.cannonButton = BuyButton(QPixmap(os.path.join('./Pictures/', "cannon_buybutton.png")), QPixmap(os.path.join('./Pictures/', "cannon_buybutton_hovered.png")), QPixmap(os.path.join('./Pictures/', "cannon_buybutton_pressed.png")), self)
                self.cannonButton.move(buttons*towerButtonSize + 10, 50)
                self.cannonButton.clicked.connect(self.cannonButtonClick)
                hbox.addWidget(self.cannonButton)
                buttons += 1
            i += 1
        
        hbox.addStretch()
        
        hbox2 = QHBoxLayout()
        vbox2 = QVBoxLayout()
        hbox2.addStretch()
        
        self.lcd = QLCDNumber(self)
        
        vbox2.addStretch()
        vbox2.addWidget(self.lcd)
        vbox2.addStretch()
        
        self.pauseButton = QPushButton('Pause')
        self.pauseButton.clicked.connect(self.pauseGame)
    
        # I could add a restart button
        
        vbox2.addWidget(self.pauseButton)
        
        self.grid.addLayout(vbox2, 0, 2)
        
        self.show()
    
        
    def musketeerButtonClick(self):
        
        if self.isPaused == False:
            if self.parent.gameboard.money > Musketeer().price:
                self.parent.isTowerSelected = True
                self.parent.selectedTower = Musketeer()
                self.statusBarMessage('Musketeer tower selected')
            else:
                self.statusBarMessage("You don't have enough money.")
        else:
            self.statusBarMessage("The game is paused. You can't build towers.")
        
        
    def cannonButtonClick(self):
        
        if self.parent.gameover == False:
            if self.isPaused == False:
                if self.parent.gameboard.money > Cannon().price:
                    self.parent.isTowerSelected = True
                    self.parent.selectedTower = Cannon()
                    self.statusBarMessage('Cannon tower selected')
                else:    
                    self.statusBarMessage("You don't have enough money.")
            else:
                self.statusBarMessage("The game is paused. You can't build towers.")
        else: self.statusBarMessage("The game has ended can't build towers.")
        

    def pauseGame(self, pressed):
        
        if self.parent.gameover == False:
        
            if self.isPaused == False:
                self.statusBarMessage('Game paused')
                self.pauseButton.setText('Play')
                self.isPaused = True 
                self.parent.timer.stop()  
                self.clockTimer.stop()
                
            else:
                self.statusBarMessage('')
                self.pauseButton.setText('Pause')
                self.isPaused = False 
                self.parent.timer.start(gameSpeed, self.parent)
                self.clockTimer.start(1000, self)
        
        else:
            self.statusBarMessage('The game has ended.')
    
    
    def timerEvent(self, event):
        self.seconds += 1
        self.lcd.display("%.2d:%.2d" % (self.seconds // 60, self.seconds % 60))
        
    
    def statusBarMessage(self, message):
        self.parent.statusBar().showMessage(message)
        
        
