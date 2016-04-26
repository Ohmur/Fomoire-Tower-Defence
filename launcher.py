'''
Created on 8.3.2016

@author: Rohmu
'''

import sys, os
from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QApplication, QSlider, QComboBox, qApp
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from globals import defaultGameSpeed
from userinterface import UserInterface


class Launcher(QWidget):
    
    def __init__(self):
        super().__init__()
        self.gameSpeed = defaultGameSpeed
        self.selectedMap = None
        self.initUI()
        
    
    def initUI(self):
        
        self.setFixedSize(400, 250)
        
        self.setWindowTitle('Fomoire!')
        fomoire = QPixmap(os.path.join('./Pictures/', "fomoire.png"))
        logo = QLabel(self)
        logo.setPixmap(fomoire)
        logo.setFixedSize(fomoire.size())
        logo.move(400 / 2 - fomoire.width() / 2, 15)
        
        selectMap = QLabel("Select map:", self)
        selectMap.move(50, 85)
        
        mapList = QComboBox(self)
        mapList.addItem('No map selected')
        
        for map in os.listdir('./Maps/'):
            mapList.addItem(map)
        
        mapList.move(135, 82)
        mapList.activated[str].connect(self.onActivated)
        
        gameSpeed = QLabel('Set game speed:', self)
        gameSpeed.move(50, 120)
        
        gameSpeed = QLabel('Slow', self)
        gameSpeed.move(170, 120)
        
        slider = QSlider(Qt.Horizontal, self)
        slider.setFocusPolicy(Qt.NoFocus)
        slider.setSliderPosition(100 - self.gameSpeed)
        slider.setGeometry(210, 120, 100, 20)
        slider.valueChanged[int].connect(self.changeValue)
        
        gameSpeed = QLabel('Fast', self)
        gameSpeed.move(325, 120)
        
        self.start = QPushButton('Start game!', self)
        self.start.move(145, 175)
        self.start.clicked[bool].connect(self.startGame)
        
        self.quit = QPushButton('Quit', self)
        self.quit.move(168, 205)
        self.quit.clicked[bool].connect(qApp.quit)
        
        
        '''
        self.speed = QLabel(self)
        self.speed.setNum(self.gameSpeed)
        self.speed.move(310, 120)
        '''
        
        self.show()
        
    
    def changeValue(self, value):
        
        self.gameSpeed = 100 - value
        #self.speed.setNum(self.gameSpeed)
        
    
    def onActivated(self, text):
        self.selectedMap = text
        
        
    def startGame(self):
        
        if self.selectedMap != None and self.selectedMap != 'No map selected':
            UserInterface(self)
            self.hide()


    def getSelectedMap(self):
        return self.selectedMap
    
    
    def getGameSpeed(self):
        return self.gameSpeed
    
    
    map = property(getSelectedMap)
    speed = property(getGameSpeed)


if __name__ == '__main__':
        
    app = QApplication(sys.argv)
    ex = Launcher()
    sys.exit(app.exec_())