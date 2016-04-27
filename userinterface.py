'''
Created on 6.3.2016

@author: Rohmu
'''

import sys, os.path, time
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow, QFrame, QLabel, QPushButton
from globals import *
from gameboard import GameBoard
from tower import *
from PyQt5.Qt import QVBoxLayout, QBasicTimer, QHBoxLayout, QDesktopWidget
from PyQt5.QtGui import QIcon
from bottombuttons import BottomButtons
from gamestats import GameStats
from mapview import MapView
from enemy import *
        

class UserInterface(QMainWindow):
    
    def __init__(self, parent):
        super().__init__(parent) 
        self._gameBoard = GameBoard()
        self._parent = parent
        
        self._gameover = False
        
        self._isTowerSelected = False
        self._isTowerHovered = False
        self._towerBeingHovered = None
        self._selectedTower = None
        
        self._waveFinishTime = 0
        
        self._gameSpeed = self._parent.speed
        self._timePassed = 0
        self.timer = QBasicTimer()
        
        self._gameBoard.readMapData(os.path.join('./Maps/', self._parent.map))
        self.timer.start(self._gameSpeed, self)
        self.initUI()
              

    def initUI(self):
        
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.setWindowTitle(self._gameBoard.name)
        self.setWindowIcon(QIcon(os.path.join('./Pictures/', 'berserker_icon.png'))) #Apparently this doens't work the same way on a mac.
        self.statusBar().showMessage('Ready!')
        vbox = QVBoxLayout()
        centralWidget.setLayout(vbox)
        self.gameStats = GameStats(self)
        self.mapView = MapView(self)
        self.bottomButtons = BottomButtons(self)
        vbox.addWidget(self.gameStats)
        vbox.addWidget(self.mapView)
        vbox.addWidget(self.bottomButtons)
        
        screen = QDesktopWidget().screenGeometry()
        self.setGeometry((screen.width() - (self.gameboard.width - 1) * 20) / 2, (screen.height() - self.gameboard.height * 20 - 200) / 2, 500, 400)
        
        self.show()
        
        
    def getGameboard(self):
        return self._gameBoard
    
    
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
        # The time passed attribute helps with setting the enemy appearance interval and tower firerate.
        self._timePassed += 1
        self.mapView.summonEnemy()
        self.mapView.moveEnemies()
        self.mapView.checkShooting()
        self.mapView.moveProjectiles()
        self.mapView.update()
       
                    
    def checkIsWaveDone(self):

        waveIndex = self._gameBoard.currentWave - 1

        if self._gameBoard.currentEnemy > len(self._gameBoard.waves[waveIndex][1]):
            self._gameBoard.currentEnemy = 1
            self._gameBoard.currentWave += 1
            self._waveFinishTime = self._timePassed
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
        youLost.setPixmap(QPixmap(os.path.join('./Pictures/', "game_over.png")))
        vbox.addWidget(youLost)
        
        done = QPushButton("Done")
        vbox.addWidget(done)

        self.popUp.setLayout(vbox)
        self.popUp.move(self.mapToGlobal(QPoint(0,0)).x() + self.gameboard.width*blockSize / 2 - 130, self.mapToGlobal(QPoint(0,0)).y() + self.gameboard.height*blockSize / 2)
        self.popUp.show()
        done.clicked.connect(self.backToMainMenu)
    
    
    def winGame(self):
        self.bottomButtons.clockTimer.stop()
        self.timer.stop()
        self.statusBar().showMessage('Game has ended. You won.')
        self._gameover = True
        
        self.popUp = QFrame()
        self.popUp.setGeometry(500, 500, 100, 100)
        
        vbox = QVBoxLayout()
        
        youLost = QLabel()
        youLost.setPixmap(QPixmap(os.path.join('./Pictures/', "victory.png")))
        vbox.addWidget(youLost)
        
        done = QPushButton("Done")
        vbox.addWidget(done)

        self.popUp.setLayout(vbox)
        self.popUp.move(self.mapToGlobal(QPoint(0,0)).x() + self.gameboard.width*blockSize / 2 - 130, self.mapToGlobal(QPoint(0,0)).y() + self.gameboard.height*blockSize / 2)
        self.popUp.show()
        done.clicked.connect(self.backToMainMenu)
        
        
    def backToMainMenu(self):
        self._parent.show()
        self.popUp.deleteLater()
        self.deleteLater()
    

    def getGameSpeed(self):
        return self._gameSpeed


    def getWaveFinishTime(self):
        return self._waveFinishTime
    

    isTowerSelected = property(getIsTowerSelected, setIsTowerSelected)
    selectedTower = property(getSelectedTower, setSelectedTower)
    isTowerHovered = property(getIsTowerBeingHovered)
    towerBeingHovered = property(getTowerBeingHovered)
    gamestats = property(getGameStats)
    gameboard = property(getGameboard)
    timePassed = property(getTimePassed)
    gameover = property(getGameOver)
    gameSpeed = property(getGameSpeed)
    waveFinishTime = property(getWaveFinishTime)


''' 
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())
'''