
'''
Created on 6.3.2016

@author: Rohmu
'''

import sys
from PyQt5.QtWidgets import (QWidget, QApplication, QGridLayout)
from PyQt5.QtGui import QPainter
from globals import blockSize, roadColor, riverColor
from gameboard import Gameboard

class UserInterface(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()

    def initUI(self):

        grid = QGridLayout()
        self.setLayout(grid)
        mapView = MapView("Map1.txt")
        grid.addWidget(mapView, 0, 0)


class MapView(QWidget):
    
    def __init__(self, file):
        super().__init__()
        self.mapFile = file
        self.initUI()
        
        
    def initUI(self): 

        self.setStyleSheet("QWidget { background: #006600}")
        self.setFixedSize(50*blockSize, 20*blockSize)
        self.setWindowTitle('Testi')
        self.show()
    
    def paintEvent(self, e):

        qp = QPainter()
        qp.begin(self)
        self.drawMap(qp, self.mapFile)
        qp.end()
        
    def drawMap(self, qp, file):
        gameboard = Gameboard()
        gameboard.readMapData(file)
        self.drawMapBlocks(qp, gameboard.getRiver(), riverColor)
        self.drawMapBlocks(qp, gameboard.getRoad(), roadColor)
            
    def drawMapBlocks(self, qp, coordinateList, color):
        qp.setPen(color) #Qt.NoPen not working...
        qp.setBrush(color)
        for i in coordinateList:
            qp.drawRect(i[0]*blockSize, i[1]*blockSize, 20, 20)
            
class bottomButtons(QWidget):
    
    def __init__(self, file):
        super().__init__()
        self.mapFile = file
        self.initUI()
        
        
    def initUI(self): 

        self.setStyleSheet("QWidget { background: #006600}") 
        self.setFixedSize(50*blockSize, 20*blockSize)
        self.setWindowTitle('Testi')
        self.show()
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = MapView("Map1.txt")
    sys.exit(app.exec_())
        