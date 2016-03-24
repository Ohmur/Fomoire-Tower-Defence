'''
Created on 6.3.2016

@author: Rohmu
'''

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QFrame, QPushButton, QAbstractButton, QLabel, QMainWindow, QLCDNumber
from PyQt5.QtGui import QPainter, QColor, QPixmap
from globals import *
from PyQt5.QtCore import Qt, QBasicTimer
from gameboard import Gameboard
from tower import *
from PyQt5.Qt import QHBoxLayout, QVBoxLayout, QBasicTimer, QGridLayout
        

class UserInterface(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.gameboard = Gameboard()
        
        self.isTowerSelected = False
        self.isTowerHovered = False
        self.towerBeingHovered = None
        self.selectedTower = None
        self.timepassed = 0
        self.timer = QBasicTimer()
        
        self.gameboard.readMapData("Map1.txt")
        self.initUI()
        self.timer.start(gameSpeed, self)
        

    def initUI(self):
        
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.setWindowTitle(self.gameboard.getName())
        self.statusBar().showMessage('Ready')
        vbox = QVBoxLayout()
        centralWidget.setLayout(vbox)
        self.gameStats = GameStats(self)
        self.mapView = MapView(self)
        self.bottomButtons = BottomButtons(self)
        vbox.addWidget(self.gameStats)
        vbox.addWidget(self.mapView)
        vbox.addWidget(self.bottomButtons)
        self.show()
        
        
    def getGameboard(self):
        return self.gameboard
    
    
    def getIsTowerSelected(self):
        return self.isTowerSelected
    
    
    def setIsTowerSelected(self, boolean):
        self.isTowerSelected = boolean
        
    
    def getSelectedTower(self):
        return self.selectedTower
    
    
    def setSelectedTower(self, towerType):
        self.selectedTower = towerType
    
    
    def getIsTowerBeingHovered(self):
        return self.isTowerHovered
    
    
    def getTowerBeingHovered(self):
        return self.towerBeingHovered
    
    
    def setIsTowerBeingHovered(self, boolean, tower):
        self.isTowerHovered = boolean
        self.towerBeingHovered = tower
    

    def getGameStats(self):
        return self.gameStats
    

class MapView(QFrame):
    
    def __init__(self, parent):
        super(MapView, self).__init__(parent)
        self.parent = parent
        self.initUI(self.parent.getGameboard())
        self.mouse_x = 0
        self.mouse_y = 0
        self.clickedTower = None
    
        
    def initUI(self, gameboard): 

        #self.setStyleSheet("QWidget { background: #5ea352    }")
        self.setFixedSize(gameboard.getWidth()*blockSize, gameboard.getHeight()*blockSize)
        self.setMouseTracking(True)
        self.show()
    
    
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawMap(qp)
        
        if not self.parent.getIsTowerSelected() and self.parent.getIsTowerBeingHovered():
            self.drawTowerRange(self.parent.getTowerBeingHovered().getPositionX(), self.parent.getTowerBeingHovered().getPositionY(), self.parent.getTowerBeingHovered().getRange(), qp)
        
        if self.underMouse() and self.parent.getIsTowerSelected():
            self.drawTowerRange(self.mouse_x, self.mouse_y, self.parent.getSelectedTower().getRange(), qp)
            self.drawTowerOutline(self.mouse_x, self.mouse_y, qp)
        
        qp.end()
        
        
    def drawMap(self, qp):
        
        self.drawMapBlocks(qp, self.parent.getGameboard().getRiver(), riverColor)
        self.drawMapBlocks(qp, self.parent.getGameboard().getRoad(), roadColor)
        self.drawMapBlocks(qp, self.parent.getGameboard().getUnoccupied(), grassColor)
        self.drawGrid(qp, gridColor)
            
            
    def drawMapBlocks(self, qp, coordinateList, color):
        qp.setPen(color) #Qt.NoPen not working...
        qp.setBrush(color)
        for i in coordinateList:
            qp.drawRect(i[0]*blockSize, i[1]*blockSize, blockSize, blockSize)
    
    
    def drawGrid(self, qp, color):
        qp.setPen(color)
        for i in range(0, self.parent.getGameboard().getWidth()*blockSize, blockSize):
            qp.drawLine(i, 0, i, self.parent.getGameboard().getHeight()*blockSize)
            qp.drawLine(0, i, self.parent.getGameboard().getWidth()*blockSize, i)
    
    
    def mousePressEvent(self, e):
        
        if e.button() == Qt.LeftButton:
            if self.parent.getIsTowerSelected() == True:
                #check mouse location, check money, build a tower
                if self.parent.getSelectedTower().getPrice() <= self.parent.getGameboard().getMoney():
                
                    self.mouse_x = e.pos().x()
                    self.mouse_y = e.pos().y()
                    
                    closest_corner_x, closest_corner_y = self.calculateClosestCorner(self.mouse_x, self.mouse_y)
                    
                    #then we calculate the grid blocks for the tower
                    block1 = [int(closest_corner_x / 20), int(closest_corner_y / 20)]
                    
                    if block1[0] > 0 and block1[1] > 0:
                        block2 = [block1[0] - 1, block1[1]]
                        block3 = [block1[0] - 1, block1[1] - 1]
                        block4 = [block1[0], block1[1] - 1]
                        
                        blocks = [block1, block2, block3, block4]
                        occupied = self.parent.getGameboard().getOccupied()
                        canPlaceTower = True
                        
                        for block in blocks:
                            if block in occupied:
                                canPlaceTower = False
                                
                        if canPlaceTower == True:
                            #places the tower on the map
                            tower = self.parent.getSelectedTower()
                            tower.setPosition(closest_corner_x, closest_corner_y)
                            
                            #tower_pic = self.parent.getSelectedTower().getPicture()
                            placedTower = ClickableTower(tower, self)
                            #placedTower.setPixmap(tower_pic)
                            placedTower.move(block3[0] * 20, block3[1] * 20)
                            placedTower.show()
                            
                            for block in blocks:
                                self.parent.getGameboard().addToOccupied(block)
                            
                            self.parent.getGameboard().addBuildTower(tower)    
                            self.parent.getGameboard().buy(tower.getPrice())
                            self.parent.getGameStats().update()
                            
                            self.parent.statusBar().showMessage('Tower build') 
                            self.parent.setSelectedTower(None)
                            self.parent.setIsTowerSelected(False)
                            
                        
                        else:
                            self.parent.statusBar().showMessage("Can't place it there")
                            
                    else:
                            self.parent.statusBar().showMessage("Can't place it there")          
                    
                else:
                    self.parent.setSelectedTower(None)
                    self.parent.setIsTowerSelected(False)
                    self.parent.statusBar().showMessage("Not enough money")   
        
        else:
            self.parent.setSelectedTower(None)
            self.parent.setIsTowerSelected(False)
            self.parent.statusBar().showMessage('')
    
    
    def mouseMoveEvent(self, event):
        
        if self.underMouse():
            self.mouse_x, self.mouse_y = self.calculateClosestCorner(event.pos().x(), event.pos().y())
            self.update()
            
    
    def calculateClosestCorner(self, mouse_x, mouse_y):
                    
        closest_corner_x = 0
        closest_corner_y = 0
                    
        #we calculate the closest grid corner from where the mouse was clicked
        if mouse_x % 20 < 10:
            closest_corner_x = mouse_x - (mouse_x % 20)
        else:
            closest_corner_x = mouse_x + (20 - mouse_x % 20)
                        
        if mouse_y % 20 < 10:
            closest_corner_y = mouse_y - (mouse_y % 20)
        else:
            closest_corner_y = mouse_y + (20 - mouse_y % 20)
            
        return closest_corner_x, closest_corner_y
        
        
    def drawTowerRange(self, x, y, towerRange, painter):
        
        painter.setPen(rangePenColor)
        painter.setBrush(rangeBrushColor)
        painter.drawEllipse(QPoint(x, y), towerRange, towerRange)
    
    
    def drawTowerOutline(self, x, y, painter):
        painter.setPen(rangePenColor)
        painter.setBrush(rangeBrushColor)
        painter.drawRect(x - 20, y - 20, 40, 40)
    
    
    def getParent(self):
        return self.parent
    
        
    def statusBarMessage(self, message):
        self.parent.statusBar().showMessage(message)
    
    
    def towerClick(self, tower):
        #Should open a menu to upgrade tower, and to see it's stats somewhere.
        self.clickedTower = tower
        self.parent.statusBar().showMessage("Tower clicked")
        self.popUp = QFrame()
        self.popUp.setGeometry(500, 500, 100, 100)
        
        grid = QGridLayout()
        self.popUp.setLayout(grid)
        
        towerStats = QLabel(tower.getName() + " Tower Stats", self)
        power = QLabel("Power: " + str(tower.getPower()), self)
        towerRange = QLabel("Range: " + str(tower.getRange()), self)
        fireRate = QLabel("Rate of Fire: " + str(tower.getFireRate()), self)
        level = QLabel("Level: " + str(tower.getLevel()), self)
        
        vbox = QVBoxLayout()
        vbox.addWidget(towerStats)
        vbox.addWidget(power)
        vbox.addWidget(towerRange)
        vbox.addWidget(fireRate)
        vbox.addWidget(level)
        
        grid.addLayout(vbox, 0, 0)
        
        upgradeButton = QPushButton("Upgrade for " + str(tower.getUpgradePrice()))
        doneButton = QPushButton("Done")
        
        vbox2 = QVBoxLayout()
        
        vbox2.addWidget(upgradeButton)
        vbox2.addWidget(doneButton)
        
        grid.addLayout(vbox2, 0, 1)
        
        self.popUp.show()
        
        upgradeButton.clicked.connect(self.upgrade)
        doneButton.clicked.connect(self.popUp.deleteLater)
    
    
    def upgrade(self):
        
        if self.clickedTower.getMaxLevel() > self.clickedTower.getLevel():
            
            if self.parent.getGameboard().getMoney() >= self.clickedTower.getUpgradePrice():
                self.clickedTower.upgrade()
                self.parent.getGameboard().buy(self.clickedTower.getUpgradePrice())
                self.statusBarMessage("Tower upgraded.")
        
            else:
                self.statusBarMessage("Not enough money to upgrade.")
        
        else:
            self.statusBarMessage("Tower already at maximum level.")
            
            
class BottomButtons(QFrame):
    
    def __init__(self, parent):
        super(BottomButtons, self).__init__(parent)
        self.parent = parent
        self.isPaused = False
        self.seconds = 0
        
        self.initUI(self.parent.getGameboard())
        
        self.clockTimer = QBasicTimer()
        self.clockTimer.start(1000, self)
        
        
    def initUI(self, gameboard): 
        
        
        self.setStyleSheet("QWidget { background: #D1D1D1}")
        self.setFixedSize(gameboard.getWidth()*blockSize, 100)
        grid = QGridLayout()
        self.setLayout(grid)
        
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        
        buildLabel = QLabel('Build', self)
        buildLabel.move(10, 0)
        vbox.addWidget(buildLabel)
        
        vbox.addStretch()
        vbox.addLayout(hbox)
        grid.addLayout(vbox, 0, 0)
        

        towers = gameboard.getTowers()
        i = 0
        buttons = 0
        while i < len(towers):
            if towers[i] == "t1":
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
        
        grid.addLayout(vbox2, 0, 1)
        
        self.show()
        
        
    def musketeerButtonClick(self):
        if self.isPaused == False:
            self.parent.isTowerSelected = True
            self.parent.setSelectedTower(Musketeer())
            self.parent.statusBar().showMessage('Musketeer tower selected')
        else:
            self.parent.statusBar().showMessage("The game is paused. You can't build towers.")
        
        
    def cannonButtonClick(self):
        if self.isPaused == False:
            self.parent.isTowerSelected = True
            self.parent.setSelectedTower(Cannon())
            self.parent.statusBar().showMessage('Cannon tower selected')
        else:
            self.parent.statusBar().showMessage("The game is paused. You can't build towers.")
        

    def pauseGame(self, pressed):
        #not yet implemented
        if self.isPaused == False:
            self.parent.statusBar().showMessage('Game paused')
            self.pauseButton.setText('Play') 
            self.isPaused = True 
            self.parent.timer.stop()  
            self.clockTimer.stop()
        else:
            self.parent.statusBar().showMessage('')
            self.pauseButton.setText('Pause')
            self.isPaused = False 
            self.parent.timer.start(gameSpeed, self.parent)
            self.clockTimer.start(1000, self)
    
    
    def timerEvent(self, event):
        self.seconds += 1
        self.lcd.display("%.2d:%.2d" % (self.seconds // 60, self.seconds % 60))
      
      
class GameStats(QFrame):
    
    def __init__(self, parent):
        super(GameStats, self).__init__(parent)
        self.parent = parent
        self.initUI(self.parent.getGameboard())    
    
    
    def initUI(self, gameboard): 

        self.setStyleSheet("QFrame { background: #D1D1D1}") 
        self.setFixedSize(gameboard.getWidth()*blockSize, 20)
        self.show()
    
    
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawGameStats(event, qp)
        qp.end()


    def drawGameStats(self, event, qp):
        
        qp.setPen(QColor(0, 0, 0, 255))
        qp.drawText(event.rect(), Qt.AlignLeft, "Money: " + str(self.parent.getGameboard().getMoney()))
        qp.drawText(event.rect(), Qt.AlignCenter, "Wave: " + str(self.parent.getGameboard().getCurrentWave()) + "/" + str(self.parent.getGameboard().getNoOfWaves()))
        qp.drawText(event.rect(), Qt.AlignRight, "Lives " + str(self.parent.getGameboard().getCurrentLives()) + "/" + str(self.parent.getGameboard().getStartingLives()))

     
class BuyButton(QAbstractButton):

    
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


class ClickableTower(QAbstractButton):
    
    def __init__(self, tower, parent):
        super(ClickableTower, self).__init__(parent)
        self.pixmap = tower.getPicture()
        self.parent = parent
        self.tower = tower
    
        self.pressed.connect(self.click)
    
    
    def paintEvent(self, event):
        
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
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())