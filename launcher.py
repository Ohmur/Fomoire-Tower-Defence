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
        
        self.setFixedSize(400, 260)
        
        self.setWindowTitle('Fomoire!')
        fomoire = QPixmap(os.path.join('./Pictures/', "fomoire.png"))
        logo = QLabel(self)
        logo.setPixmap(fomoire)
        logo.setFixedSize(fomoire.size())
        logo.move(400 / 2 - fomoire.width() / 2, 15)
        
        towerDefence = QLabel('A Tower Defence Game', self)
        towerDefence.move(130, 66)
        
        selectMap = QLabel('Select map:', self)
        selectMap.move(50, 105)
        
        mapList = QComboBox(self)
        mapList.addItem('No map selected')
        
        for mapFile in os.listdir('./Maps/'):
            mapList.addItem(mapFile)
        
        mapList.move(135, 102)
        mapList.activated[str].connect(self.onActivated)
        
        setSpeed = QLabel('Set game speed:', self)
        setSpeed.move(50, 140)
        
        slow = QLabel('Slow', self)
        slow.move(170, 140)
        
        slider = QSlider(Qt.Horizontal, self)
        slider.setFocusPolicy(Qt.NoFocus)
        slider.setSliderPosition(100 - self.gameSpeed)
        slider.setGeometry(210, 140, 100, 20)
        slider.valueChanged[int].connect(self.changeValue)
        
        fast = QLabel('Fast', self)
        fast.move(325, 140)
        
        start = QPushButton('Start game!', self)
        start.move(145, 175)
        start.clicked[bool].connect(self.startGame)
        
        quitButton = QPushButton('Quit', self)
        quitButton.move(168, 210)
        quitButton.clicked[bool].connect(qApp.quit)
        
        barbarian = QLabel(self)
        brbr = QPixmap(os.path.join('./Pictures/', "barbaari.png"))
        barbarian.setPixmap(brbr)
        barbarian.move(70, 185)
        
        berserker = QLabel(self)
        berber = QPixmap(os.path.join('./Pictures/', "berserker_left.png"))
        berserker.setPixmap(berber)
        berserker.move(290, 185)
        
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