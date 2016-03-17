'''
Created on 6.3.2016

@author: Rohmu
'''

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QFrame, QPushButton, QAbstractButton, QLabel, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QPixmap, QDrag
from globals import *
from PyQt5.QtCore import Qt, QMimeData
from gameboard import Gameboard
from tower import *
from PyQt5.Qt import QHBoxLayout, QVBoxLayout
        

class UserInterface(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.gameboard = Gameboard()
        
        self.isTowerSelected = False
        self.selectedTower = None
        
        self.gameboard.readMapData("Map1.txt")
        self.initUI()
        

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
    

    def getGameStats(self):
        return self.gameStats

class MapView(QFrame):
    
    def __init__(self, parent):
        super(MapView, self).__init__(parent)
        self.parent = parent
        self.initUI(self.parent.getGameboard())
    
        
    def initUI(self, gameboard): 

        #self.setStyleSheet("QWidget { background: #5ea352    }")
        self.setFixedSize(gameboard.getWidth()*blockSize, gameboard.getHeight()*blockSize)
        self.show()
    
    
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawMap(qp)
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
                
                    mouse_x = e.pos().x()
                    mouse_y = e.pos().y()
                    
                    closest_corner_x = 0
                    closest_corner_y = 0
                    
                    if mouse_x % 20 < 10:
                        closest_corner_x = mouse_x - (mouse_x % 20)
                    else:
                        closest_corner_x = mouse_x + (20 - mouse_x % 20)
                        
                    if mouse_y % 20 < 10:
                        closest_corner_y = mouse_y - (mouse_y % 20)
                    else:
                        closest_corner_y = mouse_y + (20 - mouse_x % 20)
                    
                    block1 = [int(closest_corner_x / 20), int(closest_corner_y / 20)]
                    block2 = [block1[0] - 1, block1[1]]
                    block3 = [block1[0] - 1, block1[1] - 1]
                    block4 = [block1[0], block1[1] - 1]
                    
                    blocks = [block1, block2, block3, block4]
                    
                    occupied = self.parent.getGameboard().getOccupied()
                    
                    if block1 not in occupied and block2 not in occupied and block3 not in occupied and block4 not in occupied:
                        #draws the tower on the map
                        #can draw outside of map at the moment
                        tower_pic = self.parent.getSelectedTower().getPicture()
                        placedTower = QLabel(self)
                        placedTower.setPixmap(tower_pic)
                        placedTower.move(block3[0] * 20, block3[1] * 20)
                        placedTower.show()
                        
                        for block in blocks:
                            self.parent.getGameboard().addToOccupied(block)
                        
                        self.parent.getGameboard().addBuildTower(self.parent.getSelectedTower())    
                        self.parent.getGameboard().buy(self.parent.getSelectedTower().getPrice())
                        self.parent.getGameStats().update()
                        
                        self.parent.statusBar().showMessage('Tower build') 
                        self.parent.setSelectedTower(None)
                        self.parent.setIsTowerSelected(False)
                    
                    else:
                        self.parent.statusBar().showMessage("Can't place it there")    
                
                else:
                    self.parent.setSelectedTower(None)
                    self.parent.setIsTowerSelected(False)
                    self.parent.statusBar().showMessage("Not enough money")   
        
        else:
            self.parent.setSelectedTower(None)
            self.parent.setIsTowerSelected(False)
            self.parent.statusBar().showMessage('No tower selected')
                
            
class BottomButtons(QFrame):
    
    def __init__(self, parent):
        super(BottomButtons, self).__init__(parent)
        self.parent = parent
        self.isPaused = False
        self.initUI(self.parent.getGameboard())
    
        
    def initUI(self, gameboard): 
        
        hbox = QHBoxLayout()
        self.setStyleSheet("QWidget { background: #D1D1D1}") 
        
        vbox = QVBoxLayout()
        
        buildLabel = QLabel('Build', self)
        buildLabel.move(10, 0)
        vbox.addWidget(buildLabel)
        
        vbox.addStretch(1)
        vbox.addLayout(hbox)
        self.setLayout(vbox)

        towers = gameboard.getTowers()
        i = 0
        buttons = 0
        while i < len(towers):
            if towers[i] == "t1":
                self.musketeerButton = PictureButton(QPixmap("musketeer.png"), QPixmap("musketeer_hover.png"), QPixmap("musketeer_pressed.png"), self)
                self.musketeerButton.move(buttons*towerButtonSize + 10, 10)
                self.musketeerButton.clicked.connect(self.musketeerButtonClick)
                hbox.addWidget(self.musketeerButton)
                buttons += 1
            elif towers[i] == "t2":
                self.cannonButton = PictureButton(QPixmap("cannon.png"), QPixmap("cannon_hover.png"), QPixmap("cannon_pressed.png"), self)
                self.cannonButton.move(buttons*towerButtonSize + 10, 10)
                self.cannonButton.clicked.connect(self.cannonButtonClick)
                hbox.addWidget(self.cannonButton)
                buttons += 1
            i += 1
        
        hbox.addStretch()
        self.pauseButton = QPushButton("Pause", self)
        self.pauseButton.clicked.connect(self.pauseGame)
        hbox.addWidget(self.pauseButton)
        
        self.show()
        
        
    def musketeerButtonClick(self):
        self.parent.isTowerSelected = True
        self.parent.setSelectedTower(Musketeer())
        self.parent.statusBar().showMessage('Musketeer tower selected')
        
        
    def cannonButtonClick(self):
        self.parent.isTowerSelected = True
        self.parent.setSelectedTower(Cannon())
        self.parent.statusBar().showMessage('Cannon tower selected')
        

    def pauseGame(self, pressed):
        #not yet implemented
        if self.isPaused == False:
            self.parent.statusBar().showMessage('Game paused')
            self.pauseButton.setText('Play') 
            self.isPaused = True 
            #self.controller.timer.stop()  
        else:
            self.parent.statusBar().showMessage('')
            self.pauseButton.setText('Pause')
            self.isPaused = False 
            #self.controller.timer.start(globals.gameSpeed, self.controller)
 
      
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

     
class PictureButton(QAbstractButton):

    
    def __init__(self, pixmap,pixmap_hover, pixmap_pressed, parent):
        super(PictureButton, self).__init__(parent)
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


        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())