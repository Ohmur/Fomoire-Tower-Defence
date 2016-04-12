'''
Created on 9.4.2016

@author: Rohmu
'''

from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton
from globals import *
from PyQt5.QtGui import QPainter
from PyQt5.QtCore import Qt, QPoint
from PyQt5.Qt import QVBoxLayout
from clickable_tower import ClickableTower
from clickable_enemy import ClickableEnemy
from enemies import *


class MapView(QFrame):
    
    def __init__(self, parent):
        super(MapView, self).__init__(parent)
        self.parent = parent
        self.initUI(self.parent.gameboard)
        self.mouse_x = 0
        self.mouse_y = 0
        self.clickedTower = None
    
        
    def initUI(self, gameboard): 

        self.setFixedSize((gameboard.width - 1)*blockSize, gameboard.height*blockSize)
        self.setMouseTracking(True)
        self.show()
    
    
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawMap(qp)
        
        if not self.parent.isTowerSelected and self.parent.isTowerHovered:
            # Draws tower range when a tower is being hovered
            self.drawTowerRange(self.parent.towerBeingHovered.posX, self.parent.towerBeingHovered.posY, self.parent.towerBeingHovered.range, qp)
        
        if self.underMouse() and self.parent.isTowerSelected:
            # Draws tower outline and range when a tower is being bought
            self.drawTowerRange(self.mouse_x, self.mouse_y, self.parent.selectedTower.range, qp)
            self.drawTowerOutline(self.mouse_x, self.mouse_y, qp)
        
        '''
        if len(self.parent.gameboard.enemiesSummoned) > 0:
            
            for enemy in self.parent.gameboard.enemiesSummoned:
                pic = enemy.picture
                label = QLabel()
                label.setPixmap(pic)
                label.move(enemy.posX, enemy.posY)
                label.show()
        '''
        qp.end()
        
        
    def drawMap(self, qp):
        
        self.drawMapBlocks(qp, self.parent.gameboard.river, riverColor)
        self.drawMapBlocks(qp, self.parent.gameboard.road, roadColor)
        self.drawMapBlocks(qp, self.parent.gameboard.unoccupied, grassColor)
         
            
    def drawMapBlocks(self, qp, coordinateList, color):
        # Draws map block according to the coordinate list
        qp.setPen(gridColor)
        qp.setBrush(color)
        
        for i in coordinateList:
            qp.drawRect(i[0]*blockSize, i[1]*blockSize, blockSize, blockSize)
    
 
    def mousePressEvent(self, e):
        # Method for building towers and checking that their location is ok
        if e.button() == Qt.LeftButton:
            
            if self.parent.isTowerSelected == True:
                # First we check the mouse location
                self.mouse_x = e.pos().x()
                self.mouse_y = e.pos().y()
                
                # We calculate the closest grid corner to find the center of the tower
                closest_corner_x, closest_corner_y = self.calculateClosestCorner(self.mouse_x, self.mouse_y)
                    
                # We calculate the bottom right block for the tower
                block1 = [int(closest_corner_x / 20), int(closest_corner_y / 20)]
                
                # We need to make sure that the tower doesn't go over the borders of the gameboard
                if block1[0] > 0 and block1[1] > 0 and block1[0] < self.parent.gameboard.width and block1[1] < self.parent.gameboard.height:
                    #Then we calculate the other blocks
                    block2 = [block1[0] - 1, block1[1]]
                    block3 = [block1[0] - 1, block1[1] - 1]
                    block4 = [block1[0], block1[1] - 1]
                        
                    blocks = [block1, block2, block3, block4]
                    occupied = self.parent.gameboard.occupied
                    canPlaceTower = True
                    
                    # We check that none of the tower blocks are occupied
                    for block in blocks:
                        if block in occupied:
                            canPlaceTower = False
                                
                    if canPlaceTower == True:
                        # We places the tower on the map
                        tower = self.parent.selectedTower
                        tower.setPosition(closest_corner_x, closest_corner_y)
                            
                        placedTower = ClickableTower(tower, self)
                        placedTower.move(block3[0] * 20, block3[1] * 20)
                        placedTower.show()
                        
                        # Then we add the tower blocks to the list of occupied tiles   
                        for block in blocks:
                            self.parent.gameboard.addToOccupied(block)
                            
                        self.parent.gameboard.addBuildTower(tower)    
                        self.parent.gameboard.buy(tower.price)
                        self.parent.gamestats.update()
                            
                        self.statusBarMessage('Tower build') 
                        self.parent.selectedTower = None
                        self.parent.isTowerSelected = False
                            
                    else:
                        self.statusBarMessage("Can't place it there")
                            
                else:
                        self.statusBarMessage("Can't place it there")          

        else:
            # If we click the right mouse button we cancel the tower selection
            self.parent.selectedTower = None
            self.parent.isTowerSelected = False
            self.statusBarMessage('')
            self.update()
    
    
    def mouseMoveEvent(self, event):
        # This method makes sure that the tower outline and range follow the mouse
        if self.underMouse() and self.parent.isTowerSelected == True:
            self.mouse_x, self.mouse_y = self.calculateClosestCorner(event.pos().x(), event.pos().y())
            self.update()
            
    
    def calculateClosestCorner(self, mouse_x, mouse_y):
        # Calculates the closest grid corner from mouse location      
        closest_corner_x = 0
        closest_corner_y = 0      
        
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
            self.statusBarMessage("Tower clicked")
            self.popUp = QFrame()
            self.popUp.setGeometry(500, 500, 100, 100)
        
            grid = QGridLayout()
            self.popUp.setLayout(grid)
        
            #I need to set fxed decimals here.
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
        
            grid.addLayout(vbox, 0, 0)
        
            vbox2 = QVBoxLayout()
        
            if self.clickedTower.maxLevel > self.clickedTower.level:
                upgradeButton = QPushButton("Upgrade for " + str(tower.upgradePrice))
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
        
        if self.clickedTower.maxLevel > self.clickedTower.level:
            
            if self.parent.gameboard.money >= self.clickedTower.upgradePrice:
                self.clickedTower.upgrade()
                self.parent.gameboard.buy(self.clickedTower.upgradePrice)
                self.statusBarMessage("Tower upgraded")
                self.popUp.deleteLater()
        
            else:
                self.statusBarMessage("Not enough money to upgrade.")
        
        else:
            self.statusBarMessage("Tower already at maximum level.")   
    
    
    def summonEnemy(self):
        
        waveIndex = self.parent.gameboard.currentWave - 1
        
        if self.parent.gameboard.currentWave <= len(self.parent.gameboard.waves):
        
            if (self.parent.timePassed % self.parent.gameboard.waves[waveIndex][0]) == 0:
                
                if self.parent.gameboard.currentWave <= len(self.parent.gameboard.waves):
                    
                    if self.checkNextEnemy("e1", Barbarian(self.parent.gameboard.enemyPath)):
                        self.parent.checkIsWaveDone()
    
                    elif self.checkNextEnemy("e2", Berserker(self.parent.gameboard.enemyPath)):
                        self.parent.checkIsWaveDone()
    
    
    def checkNextEnemy(self, name, enemyType):
        
        enemyIndex = self.parent.gameboard.currentEnemy - 1
        waveIndex = self.parent.gameboard.currentWave - 1
        
        if self.parent.gameboard.waves[waveIndex][1][enemyIndex] == name:
            clickableEnemy = ClickableEnemy(enemyType, self)
            clickableEnemy.move(enemyType.posX, enemyType.posY)
            clickableEnemy.show()
            self.parent.gameboard.addSummonedEnemy(enemyType, clickableEnemy)
            self.parent.gameboard.currentEnemy += 1
            return True
        
        else:
            return False
    
    
    def moveEnemies(self):
        
        noOfSummonedEnemies = len(self.parent.gameboard.enemiesSummoned)
        
        if noOfSummonedEnemies > 0:
            i = 0
            while i < noOfSummonedEnemies:
                enemy = self.parent.gameboard.enemiesSummoned[i][0]
                clickableEnemy = self.parent.gameboard.enemiesSummoned[i][1]
                if not enemy.isFinished:
                    enemy.move()
                    clickableEnemy.move(enemy.posX, enemy.posY)
                    if enemy.checkIfFinished():
                        self.parent.gameboard.currentLives -= 1
                        if self.parent.gameboard.currentLives <= 0:
                            self.parent.loseGame()      
                i += 1         
        self.update()       
    