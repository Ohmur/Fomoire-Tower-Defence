'''
Created on 4.3.2016

@author: Rohmu
'''
from corrupted_map_file_error import *


class Gameboard:

    def __init__(self):
        self.name = ''
        self.height = 20
        self.width = 50
        self.startingLives = 10
        self.currentLives = self.startingLives
        self.money = 100
        self.noOfWaves = 0
        self.currentWave = 1
        self.waves = []
        self.towersAvailable = []
        self.towersBuild = []
        self.enemyPath = []
        self.river = []
        self.occupied = []
        self.unoccupied = []
        self.road = []

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
                                        self.height, self.width = int(heightAndWidth[0].strip()), int(heightAndWidth[1].strip())
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
                                        self.towersAvailable.append(tower.strip().lower())
                                        #I have to add code that checks if the tower name is correct before adding it.
                                    
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
                                    while i < self.noOfWaves:
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
                                        self.waves.append([Interval, EnemiesInWave])
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
                                    while y < self.height:
                                        symbols = list(current_line)
                                        x = 0
                                        while x < self.width:
                                            symbol = str(symbols[x].strip())
                                            if symbol == "+":
                                                self.unoccupied.append([x, y])
                                            elif symbol == "0":
                                                self.occupied.append([x, y])
                                                self.road.append([x, y])
                                            elif symbol == "R":
                                                self.occupied.append([x, y])
                                                self.river.append([x, y])
                                            elif symbol == "P":
                                                self.occupied.append([x, y])
                                                self.road.append([x, y])
                                                self.enemyPath.append([x, y])
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
        self.name = name
        
    def setStartingLives(self, lives):
        self.startingLives = lives

    def setCurrentLives(self, lives):
        self.currentLives = lives
    
    def setStartingMoney(self, money):
        self.money = money
    
    def setNoOfWaves(self, waves):
        self.noOfWaves = waves
    
    def getRoad(self):
        return self.road
    
    def getRiver(self):
        return self.river
    
    def getWidth(self):
        return self.width
    
    def getHeight(self):
        return self.height
    
    def getName(self):
        return self.name
    
    def getTowers(self):
        return self.towersAvailable
    
    def getMoney(self):
        return self.money
    
    def buy(self, cost):
        self.money -= cost
    
    def getCurrentWave(self):
        return self.currentWave
    
    def getNoOfWaves(self):
        return self.noOfWaves
    
    def getCurrentLives(self):
        return self.currentLives
    
    def getStartingLives(self):
        return self.startingLives
    
    def getOccupied(self):
        return self.occupied 
    
    def addToOccupied(self, coordinates):
        self.occupied.append(coordinates)
        
    def getUnoccupied(self):
        return self.unoccupied
    
    def addBuildTower(self, tower):
        self.towersBuild.append(tower)
    
    def getBuildTowers(self):
        return self.towersBuild
        
        
    def printMapInfo(self):
        #I made this to check if the readMapData method worked properly.
        print("Map name " + str(self.name) + "\n"
              +"Height " + str(self.height) + " and width " + str(self.width) + "\n"
              +"Starting lives " + str(self.startingLives) + "\n"
              +"Starting money " + str(self.money) + "\n"
              +"Number of Waves " + str(self.noOfWaves) + "\n"
              +"Waves " + str(self.waves) + "\n"
              +"Towers" + str(self.towersAvailable) + "\n"
              +"Enemy path " + str(self.enemyPath) + "\n"
              +"River " + str(self.river) + "\n"
              +"Occupied " + str(self.occupied) + "\n"
              +"Unoccupied " + str(self.unoccupied))
    