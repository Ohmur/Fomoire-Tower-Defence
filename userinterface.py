
'''
Created on 6.3.2016

@author: Rohmu
'''

import sys
from PyQt5.QtWidgets import QWidget, QApplication, QGridLayout, QFrame, QPushButton, QAbstractButton, QLabel
from PyQt5.QtGui import QPainter, QColor, QPixmap
from globals import blockSize, roadColor, riverColor, towerButtonSize
from PyQt5.QtCore import Qt
from gameboard import Gameboard
from PyQt5.Qt import QHBoxLayout, QVBoxLayout


class UserInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.gameboard = Gameboard()
        self.gameboard.readMapData("Map1.txt")
        self.initUI(self.gameboard)

    def initUI(self, gameboard):

        self.setWindowTitle(gameboard.getName())
        grid = QGridLayout()
        self.setLayout(grid)
        gameStats = GameStats(gameboard)
        mapView = MapView(gameboard)
        bottomButtons = BottomButtons(gameboard)
        grid.addWidget(gameStats, 0, 0)
        grid.addWidget(mapView, 1, 0)
        grid.addWidget(bottomButtons, 2, 0)
        self.show()
        

class MapView(QFrame):
    
    def __init__(self, gameboard):
        super().__init__()
        self.gameboard = gameboard
        self.initUI(self.gameboard)
        
    def initUI(self, gameboard): 

        self.setStyleSheet("QFrame { background: #006600}")
        self.setFixedSize(gameboard.getWidth()*blockSize, gameboard.getHeight()*blockSize)
        self.show()
    
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawMap(qp)
        qp.end()
        
    def drawMap(self, qp):
        
        self.drawMapBlocks(qp, self.gameboard.getRiver(), riverColor)
        self.drawMapBlocks(qp, self.gameboard.getRoad(), roadColor)
            
    def drawMapBlocks(self, qp, coordinateList, color):
        qp.setPen(color) #Qt.NoPen not working...
        qp.setBrush(color)
        for i in coordinateList:
            qp.drawRect(i[0]*blockSize, i[1]*blockSize, 20, 20)
    
            
class BottomButtons(QFrame):
    
    def __init__(self, gameboard):
        super().__init__()
        self.gameboard = gameboard
        self.initUI(self.gameboard)
        
    def initUI(self, gameboard): 

        hbox = QHBoxLayout()
        self.setStyleSheet("QWidget { background: #D1D1D1}") 
        self.setFixedSize(gameboard.getWidth()*blockSize, 90)
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
                musketeerButton = PictureButton(QPixmap("musketeer.png"), QPixmap("musketeer_hover.png"), QPixmap("musketeer_pressed.png"))
                musketeerButton.move(buttons*towerButtonSize + 10, 10)
                hbox.addWidget(musketeerButton)
                buttons += 1
            elif towers[i] == "t2":
                cannonButton = PictureButton(QPixmap("cannon.png"), QPixmap("cannon_hover.png"), QPixmap("cannon_pressed.png"))
                cannonButton.move(buttons*towerButtonSize + 10, 10)
                hbox.addWidget(cannonButton)
                buttons += 1
            i += 1
        
        hbox.addStretch()
        
        self.show()
        
        
class GameStats(QFrame):
    
    def __init__(self, gameboard):
        super().__init__()
        self.gameboard = gameboard
        self.initUI(self.gameboard)    
    
    def initUI(self, gameboard): 

        self.setStyleSheet("QWidget { background: #D1D1D1}") 
        self.setFixedSize(gameboard.getWidth()*blockSize, 20)
        self.show()
    
    def paintEvent(self, event):

        qp = QPainter()
        qp.begin(self)
        self.drawGameStats(event, qp)
        qp.end()

    def drawGameStats(self, event, qp):
        
        qp.setPen(QColor(0, 0, 0, 255))
        qp.drawText(event.rect(), Qt.AlignLeft, "Money: " + str(self.gameboard.getMoney()))
        qp.drawText(event.rect(), Qt.AlignCenter, "Wave: " + str(self.gameboard.getCurrentWave()) + "/" + str(self.gameboard.getNoOfWaves()))
        qp.drawText(event.rect(), Qt.AlignRight, "Lives " + str(self.gameboard.getCurrentLives()) + "/" + str(self.gameboard.getStartingLives()))
    
    
class PictureButton(QAbstractButton):
    def __init__(self, pixmap,pixmap_hover, pixmap_pressed, parent=None):
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
        