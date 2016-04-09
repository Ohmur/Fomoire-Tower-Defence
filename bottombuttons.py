'''
Created on 9.4.2016

@author: Rohmu
'''

from PyQt5.QtWidgets import QGridLayout, QFrame, QPushButton, QLabel, QLCDNumber, QAbstractButton
from PyQt5.QtGui import QPainter
from globals import *
from tower import *
from PyQt5.Qt import QHBoxLayout, QVBoxLayout, QBasicTimer


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
        
        self.setStyleSheet("QWidget { background: #D1D1D1}")
        self.setFixedSize(gameboard.width*blockSize, 120)
        self.grid = QGridLayout()
        self.setLayout(self.grid)
        
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        
        buildLabel = QLabel('Build', self)
        buildLabel.move(10, 0)
        vbox.addWidget(buildLabel)
        vbox.addStretch()
        vbox.addLayout(hbox)
        self.grid.addLayout(vbox, 0, 0)
        

        towers = gameboard.getTowers()
        i = 0
        buttons = 0
        
        # We go through the list of different towers in the map and add buttons for them to the bottom left corner of the screen.
        while i < len(towers):
            if towers[i] == "t1":
                # I should add the price to the picture
                self.musketeerButton = BuyButton(QPixmap("musketeer.png"), QPixmap("musketeer_hover.png"), QPixmap("musketeer_pressed.png"), self)
                self.musketeerButton.move(buttons*towerButtonSize + 10, 50)
                self.musketeerButton.clicked.connect(self.musketeerButtonClick)
                hbox.addWidget(self.musketeerButton)
                buttons += 1
            elif towers[i] == "t2":
                self.cannonButton = BuyButton(QPixmap("cannon.png"), QPixmap("cannon_hover.png"), QPixmap("cannon_pressed.png"), self)
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
        
        vbox2.addWidget(self.lcd)
        vbox2.addStretch()
        
        self.pauseButton = QPushButton("Pause", self)
        self.pauseButton.clicked.connect(self.pauseGame)
    
        vbox2.addWidget(self.pauseButton)
        
        self.grid.addLayout(vbox2, 0, 2)
        
        self.show()
    
    
    '''
    # These methods draw the tower stats into the bottom of the screen when a tower is being bought.
    # For some reason these methods make the timer not work and the game starts to lag.
    
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        if self.parent._isTowerSelected == True:
            self.drawTowerInfo(self.parent.selectedTower, qp)
        else:
            noTowerLabel = QLabel("")
            self.grid.addWidget(noTowerLabel, 0, 1)   
        
        qp.end()
    
    
    def drawTowerInfo(self, tower, qp):
        
        towerStats = QLabel(tower.name + " Tower Stats", self)
        power = QLabel("Power: " + str(tower.power), self)
        towerRange = QLabel("Range: " + str(tower.range), self)
        fireRate = QLabel("Rate of Fire: " + str(tower.fireRate), self)
        level = QLabel("Level: " + str(tower.level), self)
        
        vbox = QVBoxLayout()
        
        vbox.addWidget(towerStats)
        vbox.addWidget(power)
        vbox.addWidget(towerRange)
        vbox.addWidget(fireRate)
        vbox.addWidget(level)
    
        hbox = QHBoxLayout()
        vbox.addLayout(hbox)
        hbox.addStretch()
        
        self.grid.addLayout(vbox, 0, 1)
    '''
        
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
        
        if self.isPaused == False:
            if self.parent.gameboard.money > Cannon().price:
                self.parent.isTowerSelected = True
                self.parent.selectedTower = Cannon()
                self.statusBarMessage('Cannon tower selected')
            else:    
                self.statusBarMessage("You don't have enough money.")
        else:
            self.statusBarMessage("The game is paused. You can't build towers.")
        

    def pauseGame(self, pressed):

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
    
    
    def timerEvent(self, event):
        self.seconds += 1
        self.lcd.display("%.2d:%.2d" % (self.seconds // 60, self.seconds % 60))
        
    
    def statusBarMessage(self, message):
        self.parent.statusBar().showMessage(message)
        
        
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