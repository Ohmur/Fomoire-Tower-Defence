'''
Created on 4.3.2016

@author: Rohmu
'''
from corrupted_map_file_error import *


class Gameboard:

    def __init__(self):
        self._name = ''
        self._height = 20
        self._width = 50
        self._startingLives = 10
        self._currentLives = self._startingLives
        self._money = 100
        self._noOfWaves = 0
        self._currentWave = 1
        self._waves = []
        self._towersAvailable = []
        self._towersBuild = []
        self._enemyPath = []
        self._river = []
        self._occupied = []
        self._unoccupied = []
        self._road = []
    

    def readMapData(self, file):
        
        mapSize = False
        
        try:
            mapData = open(file)
            
            current_line = mapData.readline()
            
            while current_line != '':
                
                if current_line.strip().lower() == "#mapinfo":
                    current_line = mapData.readline()
                    if current_line == '':
                        break
                    else:
                        while current_line != '' and current_line[0] != "#":
                            if current_line.strip() != "":
                                line_parts = current_line.split(":")
                                if line_parts[0].strip().lower() == "name":
                                    self.setMapName(line_parts[1].strip())
                                elif line_parts[0].strip().lower() == "size":
                                    heightAndWidth = line_parts[1].split("x")
                                    try:
                                        self._height, self._width = int(heightAndWidth[0].strip()), int(heightAndWidth[1].strip())
                                        mapSize = True
                                    except ValueError:
                                        raise CorruptedMapFileError("Reading map size failed.")  
                                elif line_parts[0].strip().lower() == "lives":
                                    try:
                                        lives = int(line_parts[1].strip())
                                        self.setCurrentLives(lives)
                                        self.setStartingLives(lives)
                                    except ValueError:
                                        raise CorruptedMapFileError("Reading starting lives failed.")
                                elif line_parts[0].strip().lower() == "money":
                                    try:
                                        self.setStartingMoney(int(line_parts[1].strip()))
                                    except ValueError:
                                        raise CorruptedMapFileError("Reading starting money failed.")
                                elif line_parts[0].strip().lower() == "towers":
                                    towerlist = line_parts[1].split(",")
                                    for tower in towerlist:
                                        self._towersAvailable.append(tower.strip().lower())
                                        #I have to add code that checks if the tower _name is correct before adding it.
                                    
                            current_line = mapData.readline()
                                    
                elif current_line.strip().lower() == "#waves":
                    current_line = mapData.readline()
                    if current_line == '':
                        break
                    else:
                        while current_line != '' and current_line[0] != "#":
                            if current_line.strip() != "":
                                line_parts = current_line.split(":")
                                if line_parts[0].strip().lower() == "number of waves":
                                    try:
                                        self.setNoOfWaves(int(line_parts[1].strip()))
                                    except ValueError:
                                        raise CorruptedMapFileError("Reading number of waves failed.")
                                    i = 0
                                    while i < self._noOfWaves:
                                        current_line = mapData.readline()
                                        line_parts = current_line.split(",")
                                        try:
                                            Interval = int(line_parts[0].strip())
                                        except ValueError:
                                            raise CorruptedMapFileError("Reading enemy interval failed.")    
                                        EnemiesInWave = []
                                        x = 1
                                        while x < len(line_parts):
                                            EnemiesInWave.append(line_parts[x].strip().lower())
                                            x += 1
                                        self._waves.append([Interval, EnemiesInWave])
                                        i += 1
                                            
                            current_line = mapData.readline()
                                                
                elif current_line.strip().lower() == "#map":
                    current_line = mapData.readline()
                    if current_line == '':
                        break
                    else:
                        if mapSize:
                            while current_line != '' and current_line[0] != "#":
                                if current_line.strip() != "":
                                    y = 0
                                    while y < self._height:
                                        symbols = list(current_line)
                                        x = 0
                                        while x < self._width:
                                            symbol = str(symbols[x].strip())
                                            if symbol == "+":
                                                self._unoccupied.append([x, y])
                                            elif symbol == "0":
                                                self._occupied.append([x, y])
                                                self._road.append([x, y])
                                            elif symbol == "R":
                                                self._occupied.append([x, y])
                                                self._river.append([x, y])
                                            elif symbol == "P":
                                                self._occupied.append([x, y])
                                                self._road.append([x, y])
                                                self._enemyPath.append([x, y])
                                            else:
                                                raise CorruptedMapFileError("Unknown symbol in map layout.")
                                            x += 1
                                        y += 1
                                        current_line = mapData.readline()
                                
                                current_line = mapData.readline()
                            
                        else:
                            raise CorruptedMapFileError("Map size info not before map layout.")
                else:
                    current_line = mapData.readline()
    
            
            mapData.close()
            
            return -1
        
        except IOError:
            raise CorruptedMapFileError("Reading the map data failed.")
        
        
    def setMapName(self, name):
        self._name = name
        
        
    def setStartingLives(self, lives):
        self._startingLives = lives


    def setCurrentLives(self, lives):
        self._currentLives = lives
    
    
    def setStartingMoney(self, money):
        self._money = money
    
    
    def setNoOfWaves(self, waves):
        self._noOfWaves = waves
    
    
    def getRoad(self):
        return self._road
    
    
    def getEnemyPath(self):
        return self._enemyPath
    
    
    def getRiver(self):
        return self._river
    
    
    def getWidth(self):
        return self._width
    
    
    def getHeight(self):
        return self._height
    
    
    def getName(self):
        return self._name
    
    
    def getTowers(self):
        return self._towersAvailable
    
    
    def getMoney(self):
        return self._money
    
    
    def buy(self, cost):
        self._money -= cost
    
    
    def getCurrentWave(self):
        return self._currentWave
    
    
    def getNoOfWaves(self):
        return self._noOfWaves
    
    
    def getCurrentLives(self):
        return self._currentLives
    
    
    def getStartingLives(self):
        return self._startingLives
    
    
    def getOccupied(self):
        return self._occupied 
    
    
    def addToOccupied(self, coordinates):
        self._occupied.append(coordinates)
        
        
    def getUnoccupied(self):
        return self._unoccupied
    
    
    def addBuildTower(self, tower):
        self._towersBuild.append(tower)
    
    
    def getBuildTowers(self):
        return self._towersBuild
    
    
    def removeFromUnoccupied(self, coordinates):
        self._unoccupied.remove(coordinates)

        
    def printMapInfo(self):
        #I made this to check if the readMapData method worked properly.
        print("Map _name " + str(self._name) + "\n"
              +"Height " + str(self._height) + " and _width " + str(self._width) + "\n"
              +"Starting lives " + str(self._startingLives) + "\n"
              +"Starting _money " + str(self._money) + "\n"
              +"Number of Waves " + str(self._noOfWaves) + "\n"
              +"Waves " + str(self._waves) + "\n"
              +"Towers" + str(self._towersAvailable) + "\n"
              +"Enemy path " + str(self._enemyPath) + "\n"
              +"River " + str(self._river) + "\n"
              +"Occupied " + str(self._occupied) + "\n"
              +"Unoccupied " + str(self._unoccupied))
    
    
    name = property(getName)
    height = property(getHeight)
    width = property(getWidth)
    currentLives = property(getCurrentLives)
    startingLives = property(getStartingLives)
    money = property(getMoney)
    currentWave = property(getCurrentWave)
    noOfWaves = property(getNoOfWaves)
    enemyPath = property(getEnemyPath)
    occupied = property(getOccupied)
    river = property(getRiver)
    road = property(getRoad)
    unoccupied = property(getUnoccupied)
    