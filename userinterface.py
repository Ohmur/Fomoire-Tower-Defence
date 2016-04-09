'''
Created on 6.3.2016

@author: Rohmu
'''

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow
from globals import *
from gameboard import Gameboard
from tower import *
from PyQt5.Qt import QVBoxLayout, QBasicTimer
from bottombuttons import BottomButtons
from gamestats import GameStats
from mapview import MapView
        

class UserInterface(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self._gameboard = Gameboard()
        
        self._isTowerSelected = False
        self._isTowerHovered = False
        self._towerBeingHovered = None
        self._selectedTower = None
        self.timepassed = 0
        self.timer = QBasicTimer()
        
        self._gameboard.readMapData("Map1.txt")
        self.initUI()
        self.timer.start(gameSpeed, self)
        

    def initUI(self):
        
        centralWidget = QWidget()
        self.setCentralWidget(centralWidget)
        self.setWindowTitle(self._gameboard.getName())
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
    
    
    
    isTowerSelected = property(getIsTowerSelected, setIsTowerSelected)
    selectedTower = property(getSelectedTower, setSelectedTower)
    isTowerHovered = property(getIsTowerBeingHovered)
    towerBeingHovered = property(getTowerBeingHovered)
    gamestats = property(getGameStats)
    gameboard = property(getGameboard)
    
      
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = UserInterface()
    sys.exit(app.exec_())