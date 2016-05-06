'''
Created on 9.4.2016

@author: Rohmu
'''

import os.path
from PyQt5.QtWidgets import QFrame, QGridLayout, QLabel, QPushButton
from globals import *
from PyQt5.QtGui import QPainter, QCursor
from PyQt5.QtCore import Qt, QPoint
from PyQt5.Qt import QVBoxLayout
from clickable_tower import ClickableTower
from enemy import *


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
        
        if self.underMouse() and self.parent.isTowerSelected:
            # Draws the tower outline and range of the tower being build
            self.drawTowerRange(self.mouse_x, self.mouse_y, self.parent.selectedTower.range, qp)
            self.drawTowerOutline(self.mouse_x, self.mouse_y, qp)
        
        if not self.parent.isTowerSelected and self.parent.isTowerHovered:
            # Draws tower range when a tower is being hovered
            self.drawTowerRange(self.parent.towerBeingHovered.posX, self.parent.towerBeingHovered.posY, self.parent.towerBeingHovered.range, qp)    
        
        self.drawPorjectiles(qp)
        
        qp.end()
        
        
    def drawMap(self, qp):
        
        self.drawMapBlocks(qp, self.parent.gameboard.river, riverColor)
        self.drawMapBlocks(qp, self.parent.gameboard.road, roadColor)
        self.drawMapBlocks(qp, self.parent.gameboard.unoccupied, grassColor)
        self.drawMapBlocks(qp, self.parent.gameboard.cave, caveColor)
        self.drawMapBlocks(qp, self.parent.gameboard.mountain, mountainColor)
        self.drawMapBlocks(qp, self.parent.gameboard.bridge, woodColor)
        
            
    def drawMapBlocks(self, qp, coordinateList, color):
        # Draws map blocks according to the coordinate list
        qp.setPen(gridColor)
        qp.setBrush(color)
        
        for i in coordinateList:
            qp.drawRect(i[0]*blockSize, i[1]*blockSize, blockSize, blockSize)
    
    
    def drawTowerRange(self, x, y, towerRange, painter):
        
        painter.setPen(rangePenColor)
        painter.setBrush(rangeBrushColor)
        painter.drawEllipse(QPoint(x, y), towerRange, towerRange)
    
    
    def drawTowerOutline(self, x, y, painter):
        painter.setPen(rangePenColor)
        painter.setBrush(rangeBrushColor)
        painter.drawRect(x - 20, y - 20, 40, 40)
    
    
    def drawPorjectiles(self, qp):
        
        qp.setPen(projectileColor)
        qp.setBrush(projectileColor)
        
        for projectile in self.parent.gameboard.projectiles:
            
            if not projectile.isFinished:
                if projectile.name == "Bullet":
                    qp.drawEllipse(projectile.posX, projectile.posY, 3, 3)
                elif projectile.name == "Cannonball":
                    qp.drawEllipse(projectile.posX, projectile.posY, 8, 8)
    
    
    def mouseMoveEvent(self, event):
        # This method makes sure that towers are build according to the grid and that the tower outline and range are displayed properly
        if self.underMouse() and self.parent.isTowerSelected == True:
            self.mouse_x, self.mouse_y = self.calculateClosestCorner(event.pos().x(), event.pos().y())  
        
        
    def calculateClosestCorner(self, mouse_x, mouse_y):
        # Calculates the closest grid corner from mouse location      
        closest_corner_x = 0
        closest_corner_y = 0      
        
        if mouse_x % blockSize < blockSize / 2:
            closest_corner_x = mouse_x - (mouse_x % blockSize)
        else:
            closest_corner_x = mouse_x + (blockSize - mouse_x % blockSize)
                        
        if mouse_y % blockSize < blockSize / 2:
            closest_corner_y = mouse_y - (mouse_y % blockSize)
        else:
            closest_corner_y = mouse_y + (blockSize - mouse_y % blockSize)
            
        return closest_corner_x, closest_corner_y

 
    def mousePressEvent(self, e):
        # Method for building towers and checking that their location is ok
        if e.button() == Qt.LeftButton:
            
            if self.parent.gameover == False:
                
                if self.parent.isTowerSelected == True:
                    # We calculate the bottom right block for the tower
                    block1 = [int(self.mouse_x / blockSize), int(self.mouse_y / blockSize)]
                    
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
                            tower.setPosition(self.mouse_x, self.mouse_y)
                                
                            placedTower = ClickableTower(tower, self)
                            placedTower.move(block3[0] * blockSize, block3[1] * blockSize)
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
                            self.statusBarMessage("Can't place it there!")
                                
                    else:
                            self.statusBarMessage("Can't place it there!")    
                                              
            else:
                self.statusBarMessage("The game has ended. You can't build towers.")    
                
        else:
            # If we click the right mouse button we cancel the tower selection
            self.parent.selectedTower = None
            self.parent.isTowerSelected = False
            self.statusBarMessage('')
            self.update()
    
    
    def getParent(self):
        # Not sure if I'm using this anywhere
        return self.parent
    
        
    def statusBarMessage(self, message):
        # Just a shorter way to write statusbar messages
        self.parent.statusBar().showMessage(message)
    
    
    def towerClick(self, tower):
        # Opens a popup to see tower stats and to upgrade tower
        if self.parent.gameover == False:
            
            if self.parent.isTowerSelected == False:
                self.clickedTower = tower
                # self.statusBarMessage("Tower clicked")
                self.towerPopUp = QFrame()
                self.towerPopUp.setGeometry(500, 500, 100, 100)
            
                grid = QGridLayout()
                self.towerPopUp.setLayout(grid)
                
                vbox = QVBoxLayout()
                pixmap = QLabel()
                vbox.addStretch()
                if tower.level == 2:
                    pixmap.setPixmap(tower.upgradedPicture)
                else:
                    pixmap.setPixmap(tower.picture)
                vbox.addWidget(pixmap)
                vbox.addStretch()
                
                grid.addLayout(vbox, 0, 0)
                
                towerStats = QLabel(tower.name + " Tower Stats", self)
                power = QLabel("Power: {:.0f}".format(tower.power), self)
                towerRange = QLabel("Range: {:.0f}".format(tower.range), self)
                fireRate = QLabel("Rate of Fire: " + str(tower.fireRate), self)
                level = QLabel("Level: " + str(tower.level), self)
            
                vbox2 = QVBoxLayout()
                vbox2.addWidget(towerStats)
                vbox2.addWidget(power)
                vbox2.addWidget(towerRange)
                vbox2.addWidget(fireRate)
                vbox2.addWidget(level)
            
                grid.addLayout(vbox2, 0, 1)
        
                vbox3 = QVBoxLayout()
                
                if self.clickedTower.maxLevel > self.clickedTower.level:
                    upgradeButton = QPushButton("Upgrade for " + str(tower.upgradePrice))
                    vbox3.addWidget(upgradeButton)
                    upgradeButton.clicked.connect(self.upgrade)
                else:
                    maxLevel = QLabel("Tower at maximum level.")
                    vbox3.addWidget(maxLevel)
                
                doneButton = QPushButton("Done")
                vbox3.addWidget(doneButton)
                grid.addLayout(vbox3, 0, 2)
            
                location = QPoint(QCursor.pos())
                self.towerPopUp.move(location.x() - 180, location.y())
                self.towerPopUp.show()
                doneButton.clicked.connect(self.towerPopUp.hide)
        
        else:
            self.statusBarMessage("The game has ended. Stop doing stuff.")
            
    
    def upgrade(self):
        
        if self.clickedTower.level < self.clickedTower.maxLevel:
            
            if self.parent.gameboard.money >= self.clickedTower.upgradePrice:
                self.clickedTower.upgrade()
                self.parent.gameboard.buy(self.clickedTower.upgradePrice)
                self.statusBarMessage("Tower upgraded")
                self.parent.gamestats.update()
                self.towerPopUp.hide()
        
            else:
                self.statusBarMessage("Not enough money to upgrade.")
        
        else:
            self.statusBarMessage("Tower already at maximum level.")   
    
    
    def summonEnemy(self):
        # Summons an enemy at given intervals
        waveIndex = self.parent.gameboard.currentWave - 1
        
        if self.parent.gameboard.currentWave <= len(self.parent.gameboard.waves):
            # self.parent.gameboard.waves[waveIndex][0] gives the enemy interval for that wave
            if self.parent.gameboard.currentEnemy == 1:
                # This makes sure that there's a break between enemy waves, the length of the break can be defined in globals
                if self.parent.timePassed - self.parent.waveFinishTime >= breakBetweenWaves:
                    if self.checkNextEnemy("e1", Barbarian(self.parent.gameboard.enemyPath, self)):
                        self.checkIsWaveDone()
    
                    elif self.checkNextEnemy("e2", Berserker(self.parent.gameboard.enemyPath, self)):
                        self.checkIsWaveDone()
            
            elif self.parent.timePassed % self.parent.gameboard.waves[waveIndex][0] == 0:
                    
                if self.checkNextEnemy("e1", Barbarian(self.parent.gameboard.enemyPath, self)):
                    self.checkIsWaveDone()
    
                elif self.checkNextEnemy("e2", Berserker(self.parent.gameboard.enemyPath, self)):
                    self.checkIsWaveDone()
    
    
    def checkIsWaveDone(self):

        waveIndex = self.parent.gameboard.currentWave - 1

        if self.parent.gameboard.currentEnemy > len(self.parent.gameboard.waves[waveIndex][1]):
            self.parent.gameboard.currentEnemy = 1
            self.parent.gameboard.currentWave += 1
            self.parent.waveFinishTime = self.parent.timePassed
            self.parent.gamestats.update()
            return True
        else:
            return False
    
    
    def checkNextEnemy(self, name, enemyType):
        # This method could probably be changed a bit, but it does it's job. I'll update it if I have time.
        enemyIndex = self.parent.gameboard.currentEnemy - 1
        waveIndex = self.parent.gameboard.currentWave - 1
        
        if self.parent.gameboard.waves[waveIndex][1][enemyIndex] == name:
            enemy = enemyType
            enemy.move(enemy.posX, enemy.posY)
            enemy.show()
            self.parent.gameboard.addSummonedEnemy(enemy)
            self.parent.gameboard.currentEnemy += 1
            return True
        
        else:
            return False
    
    
    def moveEnemies(self):
        
        noOfSummonedEnemies = len(self.parent.gameboard.enemiesSummoned)
        
        if noOfSummonedEnemies > 0:
            i = 0
            
            while i < noOfSummonedEnemies:
                enemy = self.parent.gameboard.enemiesSummoned[i]
                
                if not enemy.isFinished and not enemy.isDead:
                    enemy.moveEnemy()
                    
                    if enemy.checkIfFinished():
                        self.parent.gameboard.currentLives -= 1
                        self.parent.update()
                        
                        if self.parent.gameboard.currentLives <= 0:
                            self.parent.loseGame()
                        else:
                            self.checkIfGameEnded()
                              
                i += 1        
                
    
    def enemyClick(self, enemy):
        # Opens an info screen on the enemy
        if self.parent.gameover == False and enemy.isDead == False:
        
            if self.parent.isTowerSelected == False:
                # self.statusBarMessage("Enemy clicked")
                self.enemyPopUp = QFrame()
                self.enemyPopUp.setGeometry(500, 500, 100, 100)
            
                grid = QGridLayout()
                self.enemyPopUp.setLayout(grid)
            
                enemyStats = QLabel("Enemy Stats")
                name = QLabel("Name: " + str(enemy.name))
                speed = QLabel("Speed: " + str(enemy.speed))
                health = QLabel("Health: {:.0f}".format(enemy.health))
                pixmap = QLabel()
                pixmap.setPixmap(enemy.picture)
            
                vbox = QVBoxLayout()
                vbox.addWidget(enemyStats)
                vbox.addWidget(name)
                vbox.addWidget(speed)
                vbox.addWidget(health)
    
                grid.addLayout(vbox, 0, 0)
            
                vbox2 = QVBoxLayout()
                vbox2.addWidget(pixmap)
                vbox2.addStretch()
                
                doneButton = QPushButton("Done")
                vbox2.addWidget(doneButton)
                grid.addLayout(vbox2, 0, 1)
                
                location = QPoint(QCursor.pos())
                self.enemyPopUp.move(location.x() - 100, location.y())
                self.enemyPopUp.show()
                doneButton.clicked.connect(self.enemyPopUp.hide)
        
        else:
            self.statusBarMessage("The game has ended. Stop doing stuff.")

        
    def checkShooting(self):
        # We go trough the towers we have build and check if they have enemies in range
        for tower in self.parent.gameboard.towersBuild:
            
            # This is kind of a simple method of checking the firerate
            # We firs check when the tower has fired it's last shot to see if it's time to shoot again
            if tower.lastShot == 0 or self.parent.timePassed - tower.lastShot >= tower.fireRate: 
                # We always shoot the enemy that has moved to the furthest block. If there's more than one enemy in the same block we select the one that's first in the list.
                # Again, this method could be improved. We could check which enemy is actually furthest down the path in actual pixels.
                i = 0
                maxBlocks = -1
                targetEnemy = None
                
                while i < len(self.parent.gameboard.enemiesSummoned):
                    
                    enemy = self.parent.gameboard.enemiesSummoned[i]
                    # We shouldn't shoot enemies that are dead or have already reached the end of the path.
                    if enemy.isFinished == False and enemy.isDead == False:
                        if tower.inRange(enemy):
                            if enemy.blocksMoved > maxBlocks:
                                maxBlocks = enemy.blocksMoved
                                targetEnemy = enemy
                    
                    i += 1
                
                if targetEnemy != None:
                    projectile = tower.shoot(targetEnemy)
                    tower.lastShot = self.parent.timePassed
                    self.parent.gameboard.addProjectile(projectile)  
                    # self.statusBarMessage(tower.name + " shoots " + targetEnemy.name + " with " + projectile.name)
                
    
    def moveProjectiles(self):
        
        for projectile in self.parent.gameboard.projectiles:
            
            if not projectile.isFinished:
                projectile.move()
                
                if projectile.checkIfHit():
                    # self.statusBarMessage(projectile.destination.name + " takes a hit of " + str(projectile.damage) + " damage.")
                    if projectile.name == "Cannonball":
                        # Cannonballs damage all enemies in the same block.
                        # This method could also be improved. We should probably hit enemies that are within a certain range from the target enemy instead of being in the same block.
                        for enemy in self.parent.gameboard.enemiesSummoned:
                            if enemy != projectile.destination and enemy.currentBlock == projectile.destination.currentBlock:
                                enemy.getHit(projectile.damage)
                                enemy.checkIfDead()
                    
                    if projectile.destination.checkIfDead():
                        # self.statusBarMessage(projectile.destination.name + " is dead. You get " + str(projectile.destination.reward) + " coins.")
                        self.parent.gameboard.addMoney(projectile.destination.reward)
                        self.parent.gamestats.update()

                        self.checkIfGameEnded()
    
    
    def checkIfGameEnded(self):
        # This method checks if all waves have been sent and all summoned enemies have either reached their destination or died.
        allDone = False
        
        if self.parent.gameboard.currentWave >= len(self.parent.gameboard.waves):
            # self.statusBarMessage("Last wave!")
            # Check how many enemies the map has in total
            totalEnemies = 0
            for wave in self.parent.gameboard.waves:
                totalEnemies += len(wave[1])
            
            # Then we compare that number to the number of summoned enemies
            if len(self.parent.gameboard.enemiesSummoned) == totalEnemies:
                # self.statusBarMessage("All enemies summoned!")
                allDone = True
                # Then we check if they are all dead or finished
                for enemy in self.parent.gameboard.enemiesSummoned:
                    if enemy.isFinished == False and enemy.isDead == False:
                        allDone = False
        
        # If so the game has ended and the player is victorious               
        if allDone:
            self.parent.winGame()