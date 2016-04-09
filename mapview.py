'''
Created on 9.4.2016

@author: Rohmu
'''

from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton, QAbstractButton
from globals import *
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QPoint
from PyQt5.Qt import QVBoxLayout


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
        
        if not self.parent.isTowerSelected and self.parent.isTowerHovered:
            self.drawTowerRange(self.parent.towerBeingHovered.getPositionX(), self.parent.towerBeingHovered.getPositionY(), self.parent.towerBeingHovered.getRange(), qp)
        
        if self.underMouse() and self.parent.isTowerSelected:
            self.drawTowerRange(self.mouse_x, self.mouse_y, self.parent.selectedTower.getRange(), qp)
            self.drawTowerOutline(self.mouse_x, self.mouse_y, qp)
        
        qp.end()
        
        
    def drawMap(self, qp):
        
        self.drawMapBlocks(qp, self.parent.gameboard.getRiver(), riverColor)
        self.drawMapBlocks(qp, self.parent.gameboard.getRoad(), roadColor)
        self.drawMapBlocks(qp, self.parent.gameboard.getUnoccupied(), grassColor)
        self.drawGrid(qp, gridColor)
            
            
    def drawMapBlocks(self, qp, coordinateList, color):
        qp.setPen(color) #Qt.NoPen not working...
        qp.setBrush(color)
        for i in coordinateList:
            qp.drawRect(i[0]*blockSize, i[1]*blockSize, blockSize, blockSize)
    
    
    def drawGrid(self, qp, color):
        qp.setPen(color)
        for i in range(0, self.parent.gameboard.getWidth()*blockSize, blockSize):
            qp.drawLine(i, 0, i, self.parent.gameboard.getHeight()*blockSize)
            qp.drawLine(0, i, self.parent.gameboard.getWidth()*blockSize, i)
    
    
    def mousePressEvent(self, e):
        
        if e.button() == Qt.LeftButton:
            if self.parent.isTowerSelected == True:
                #check mouse location, build a tower
                
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
                    occupied = self.parent.gameboard.getOccupied()
                    canPlaceTower = True
                        
                    for block in blocks:
                        if block in occupied:
                            canPlaceTower = False
                                
                    if canPlaceTower == True:
                        #places the tower on the map
                        tower = self.parent.selectedTower
                        tower.setPosition(closest_corner_x, closest_corner_y)
                            
                        #tower_pic = self.parent.getSelectedTower().getPicture()
                        placedTower = ClickableTower(tower, self)
                        #placedTower.setPixmap(tower_pic)
                        placedTower.move(block3[0] * 20, block3[1] * 20)
                        placedTower.show()
                            
                        for block in blocks:
                            self.parent.gameboard.addToOccupied(block)
                            
                        self.parent.gameboard.addBuildTower(tower)    
                        self.parent.gameboard.buy(tower.getPrice())
                        self.parent.gamestats.update()
                            
                        self.parent.statusBar().showMessage('Tower build') 
                        self.parent.selectedTower = None
                        self.parent.isTowerSelected = False
                            
                        
                    else:
                        self.parent.statusBar().showMessage("Can't place it there")
                            
                else:
                        self.parent.statusBar().showMessage("Can't place it there")          

        
        else:
            self.parent.selectedTower = None
            self.parent.isTowerSelected = False
            self.parent.statusBar().showMessage('')
            self.update()
    
    
    def mouseMoveEvent(self, event):
        
        if self.underMouse() and self.parent.isTowerSelected == True:
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
        
        if self.parent.isTowerSelected == False:
            self.clickedTower = tower
            self.parent.statusBar().showMessage("Tower clicked")
            self.popUp = QFrame()
            self.popUp.setGeometry(500, 500, 100, 100)
        
            grid = QGridLayout()
            self.popUp.setLayout(grid)
        
            #I need to set fxed decimals here.
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
        
            vbox2 = QVBoxLayout()
        
            if self.clickedTower.getMaxLevel() > self.clickedTower.getLevel():
                upgradeButton = QPushButton("Upgrade for " + str(tower.getUpgradePrice()))
                vbox2.addWidget(upgradeButton)
                upgradeButton.clicked.connect(self.upgrade)
            else:
                maxLevel = QLabel("Tower at maximum level.")
                vbox2.addWidget(maxLevel)
            
            doneButton = QPushButton("Done")
            vbox2.addWidget(doneButton)
            grid.addLayout(vbox2, 0, 1)
        
            self.popUp.show()
            doneButton.clicked.connect(self.popUp.deleteLater)
    
    
    def upgrade(self):
        
        if self.clickedTower.getMaxLevel() > self.clickedTower.getLevel():
            
            if self.parent.gameboard.getMoney() >= self.clickedTower.getUpgradePrice():
                self.clickedTower.upgrade()
                self.parent.gameboard.buy(self.clickedTower.getUpgradePrice())
                self.statusBarMessage("Tower upgraded.")
                self.popUp.deleteLater()
        
            else:
                self.statusBarMessage("Not enough money to upgrade.")
        
        else:
            self.statusBarMessage("Tower already at maximum level.")
            
               

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