'''
Created on 6.3.2016

@author: Rohmu
'''

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFrame, QLabel, QPushButton
from globals import *
from gameboard import Gameboard
from tower import *
from PyQt5.Qt import QVBoxLayout, QBasicTimer, QHBoxLayout
from PyQt5.QtGui import QIcon
from bottombuttons import BottomButtons
from gamestats import GameStats
from mapview import MapView
from enemy import *
import time
        

class UserInterface(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self._gameboard = Gameboard()
        
        self._gameover = False
        
        self._isTowerSelected = False
        self._isTowerHovered = False
        self._towerBeingHovered = None
        self._selectedTower = None
        self._timePassed = 0
        self.timer = QBasicTimer()
        
        self._gameboard.readMapData("Map1.txt")
        self.initUI()
        self.timer.start(gameSpeed, self)
        

    def initUI(self):

        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.setWindowTitle(self._gameboard.name)
        self.setWindowIcon(QIcon('berserker_icon.png')) #Apparently this doens't work the same way on mac.
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
        return self._gameboard
    
    
    def getIsTowerSelected(self):
        return self._isTowerSelected
    
    
    def setIsTowerSelected(self, boolean):
        self._isTowerSelected = boolean
        
    
    def getSelectedTower(self):
        return self._selectedTower
    
    
    def setSelectedTower(self, towerType):
        self._selectedTower = towerType
    
    
    def getIsTowerBeingHovered(self):
        return self._isTowerHovered
    
    
    def setIsTowerBeingHovered(self, boolean, tower):
        self._isTowerHovered = boolean
        self._towerBeingHovered = tower
    
    
    def getTowerBeingHovered(self):
        return self._towerBeingHovered
    

    def getGameStats(self):
        return self.gameStats


    def getTimePassed(self):
        return self._timePassed
    
    
    def getGameOver(self):
        return self._gameover
    
    
    def timerEvent(self, event):
        self._timePassed += 1
        self.mapView.summonEnemy()
        self.mapView.moveEnemies()
       
                    
    def checkIsWaveDone(self):

        waveIndex = self._gameboard.currentWave - 1

        if self._gameboard.currentEnemy > len(self._gameboard.waves[waveIndex][1]):
            self._gameboard.currentEnemy = 1
            self._gameboard.currentWave += 1
            self.gamestats.update()
            return True
        else:
            return False
    
    
    def loseGame(self):
        self.bottomButtons.clockTimer.stop()
        self.timer.stop()
        self.statusBar().showMessage('Game has ended. You lost.')
        self._gameover = True
        
        self.popUp = QFrame()
        self.popUp.setGeometry(500, 500, 100, 100)
        
        vbox = QVBoxLayout()
        
        youLost = QLabel()
        youLost.setPixmap(QPixmap("game_over.png"))
        vbox.addWidget(youLost)
        
        doneButton = QPushButton("Done")
        vbox.addWidget(doneButton)

        self.popUp.setLayout(vbox)
        self.popUp.move(self.mapToGlobal(QPoint(0,0)).x() + self.gameboard.width*blockSize / 2 - 130, self.mapToGlobal(QPoint(0,0)).y() + self.gameboard.height*blockSize / 2)
        self.popUp.show()
        doneButton.clicked.connect(self.popUp.deleteLater)
    
    
    def winGame(self):
        self.bottomButtons.clockTimer.stop()
        self.timer.stop()
        self.statusBar().showMessage('Game has ended. You won.')
        self._gameover = True
        
        self.popUp = QFrame()
        self.popUp.setGeometry(500, 500, 100, 100)
        
        vbox = QVBoxLayout()
        
        youLost = QLabel()
        youLost.setPixmap(QPixmap("victory.png"))
        vbox.addWidget(youLost)
        
        doneButton = QPushButton("Done")
        vbox.addWidget(doneButton)

        self.popUp.setLayout(vbox)
        self.popUp.move(self.mapToGlobal(QPoint(0,0)).x() + self.gameboard.width*blockSize / 2 - 130, self.mapToGlobal(QPoint(0,0)).y() + self.gameboard.height*blockSize / 2)
        self.popUp.show()
        doneButton.clicked.connect(self.popUp.deleteLater)
    

    isTowerSelected = property(getIsTowerSelected, setIsTowerSelected)
    selectedTower = property(getSelectedTower, setSelectedTower)
    isTowerHovered = property(getIsTowerBeingHovered)
    towerBeingHovered = property(getTowerBeingHovered)
    gamestats = property(getGameStats)
    gameboard = property(getGameboard)
    timePassed = property(getTimePassed)
    gameover = property(getGameOver)

        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())