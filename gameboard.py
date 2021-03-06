'''
Created on 4.3.2016

@author: Rohmu
'''
from corrupted_map_file_error import *
from globals import towerTypes
from globals import enemyTypes


class GameBoard:

    def __init__(self):
        self._name = ''
        self._width = 50
        self._height = 20
        self._startingLives = 10
        self._currentLives = self._startingLives
        self._money = 100
        self._noOfWaves = 0
        self._currentWave = 1
        self._currenEnemy = 1
        self._waves = []
        self._towersAvailable = []
        self._towersBuild = []
        self._pathStart = []
        self._enemyPath = []
        self._enemiesSummoned = []
        self._projectiles = []
        self._river = []
        self._occupied = []
        self._unoccupied = []
        self._cave = []
        self._mountain = []
        self._bridge = []
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
                                    self._name = line_parts[1].strip()
                                    
                                elif line_parts[0].strip().lower() == "size":
                                    heightAndWidth = line_parts[1].split("x")
                                    try:
                                        self._width, self._height = int(heightAndWidth[0].strip()), int(heightAndWidth[1].strip())
                                        mapSize = True
                                    except ValueError:
                                        raise CorruptedMapFileError("Reading map size failed.")
                                    
                                    if self._height < 7 or self._width < 25:
                                        raise CorruptedMapFileError("The map is too small. It should be at least 25 blocks wide and 7 blocks high.")
                                    elif self._height > 28 or self._width > 70:
                                        raise CorruptedMapFileError("The map is too big. It should be maximum 70 blocks wide and 28 blocks high.")
                                    
                                elif line_parts[0].strip().lower() == "lives":
                                    try:
                                        lives = int(line_parts[1].strip())
                                        self.setCurrentLives(lives)
                                        self.setStartingLives(lives)
                                    except ValueError:
                                        raise CorruptedMapFileError("Reading starting lives failed.")
                                    if self._startingLives <= 0 or self._startingLives > 20:
                                        raise CorruptedMapFileError("Starting lives should be between at least 1 and maximum 20.")
                                    
                                elif line_parts[0].strip().lower() == "money":
                                    try:
                                        self.setStartingMoney(int(line_parts[1].strip()))
                                    except ValueError:
                                        raise CorruptedMapFileError("Reading starting money failed.")
                                    if self._money < 100:
                                        raise CorruptedMapFileError("Starting money should be at least 100.")
                                    
                                elif line_parts[0].strip().lower() == "towers":
                                    towerlist = line_parts[1].split(",")
                                    for tower in towerlist:
                                        temp = tower.strip().lower()
                                        if temp in towerTypes:
                                            self._towersAvailable.append(temp)
                                        else:
                                            raise CorruptedMapFileError("Unknown tower type.")
                                        
                                elif line_parts[0].strip().lower() == "path start":
                                    coordinates = line_parts[1].split(",")
                                    try:
                                        for number in coordinates:
                                            self._pathStart.append(int(number.strip().lower()) - 1)
                                    except ValueError:
                                        raise CorruptedMapFileError("Reading path start coordinate failed.")
                                    if len(self._pathStart) != 2:
                                        raise CorruptedMapFileError("Reading path start coordinate failed. There should be two values x, y.")
                                    for number in self._pathStart:
                                        if number < 0:
                                            raise CorruptedMapFileError("Reading path start coordinate failed. Value can not be less than 0.")
                                    
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
                                        # The first number on this list gives us the enemy interval
                                        try:
                                            Interval = int(line_parts[0].strip())
                                        except ValueError:
                                            raise CorruptedMapFileError("Reading enemy interval failed.")    
                                        EnemiesInWave = []
                                        x = 1
                                        
                                        while x < len(line_parts):
                                            enemy = line_parts[x].strip().lower()
                                            if enemy in enemyTypes:
                                                EnemiesInWave.append(enemy)
                                                x += 1
                                            else:
                                                raise CorruptedMapFileError("Unkown enemy type.") 
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
                                                # grass
                                                self._unoccupied.append([x, y])
                                            elif symbol == "0":
                                                # road
                                                self._occupied.append([x, y])
                                                self._road.append([x, y])
                                            elif symbol == "R":
                                                # river/water
                                                self._occupied.append([x, y])
                                                self._river.append([x, y])
                                            elif symbol == "D":
                                                # path on water
                                                self._occupied.append([x, y])
                                                self._river.append([x, y])
                                                self._enemyPath.append([x, y])
                                            elif symbol == "P":
                                                # path on a road
                                                self._occupied.append([x, y])
                                                self._road.append([x, y])
                                                self._enemyPath.append([x, y])
                                            elif symbol == "B": 
                                                # path on a bridge
                                                self._occupied.append([x, y])
                                                self._bridge.append([x, y])
                                                self._enemyPath.append([x, y])
                                            elif symbol == "W":
                                                # wood/bridge
                                                self._occupied.append([x, y])
                                                self._bridge.append([x, y])
                                            elif symbol == "C":
                                                # cave/black
                                                self._occupied.append([x, y])
                                                self._cave.append([x, y])
                                            elif symbol == "Q":
                                                # path in cave
                                                self._occupied.append([x, y])
                                                self._cave.append([x, y])
                                                self._enemyPath.append([x, y])
                                            elif symbol == "M":
                                                # mountain/gray
                                                self._occupied.append([x, y])
                                                self._mountain.append([x, y])
                                            elif symbol == "X":
                                                self._occupied.append([x, y])
                                                self._mountain.append([x, y])
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
            
            # We need to sort the coordinates on the enemy path list.
            self.sortEnemyPath(self._enemyPath, self._pathStart)

        
        except IOError:
            raise CorruptedMapFileError("Reading the map data failed.")
        
    
    def sortEnemyPath(self, path, startcoordinate):
        # First we search for the path start coordinate and place it first in the list.
        i = 0
        while i < len(path):
            if path[i] == self._pathStart:
                temp = path[0]
                path[0] = path[i]
                path[i] = temp
                break
            i += 1
        
        # Then we sort the rest
        x = 1
        while x < len(path):
            y = x
            while y < len(path):
                if path[y][0] == path[x-1][0] and ((path[y][1] == path[x-1][1] - 1) or (path[y][1] == path[x-1][1] + 1)):
                    temp = path[x]
                    path[x] = path[y]
                    path[y] = temp
                    y += 1
                    break
                elif path[y][1] == path[x-1][1] and ((path[y][0] == path[x-1][0] - 1) or (path[y][0] == path[x-1][0] + 1)):
                    temp = path[x]
                    path[x] = path[y]
                    path[y] = temp
                    y += 1
                    break
                y += 1
            x += 1
    
    
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
 
    
    def addSummonedEnemy(self, enemy):
        self._enemiesSummoned.append(enemy)
    
 
    def getEnemiesSummoned(self):
        return self._enemiesSummoned
    
    
    def getCurrentEnemy(self):
        return self._currenEnemy
    
    
    def setCurrentEnemy(self, enemyIndex):
        self._currenEnemy = enemyIndex
        
    
    def setCurrentWave(self, waveIndex):
        self._currentWave = waveIndex
       
       
    def getWaves(self):
        return self._waves 
    
    
    def getCave(self):
        return self._cave
    
    
    def getMountain(self):
        return self._mountain
    
    
    def getBridge(self):
        return self._bridge
        
    
    def removeFromUnoccupied(self, coordinates):
        self._unoccupied.remove(coordinates)
        
        
    def addProjectile(self, projectile):
        self._projectiles.append(projectile)
        
    
    def getProjectiles(self):
        return self._projectiles
    
    
    def addMoney(self, amount):
        self._money += amount

        
    def printMapInfo(self):
        # I made this to check if the readMapData method worked properly.
        print("Map _name " + str(self._name) + "\n"
              +"Height " + str(self._height) + " and _width " + str(self._width) + "\n"
              +"Starting lives " + str(self._startingLives) + "\n"
              +"Starting _money " + str(self._money) + "\n"
              +"Number of Waves " + str(self._noOfWaves) + "\n"
              +"Waves " + str(self._waves) + "\n"
              +"Towers" + str(self._towersAvailable) + "\n"
              +"Enemy path " + str(self._enemyPath) + "\n"
              +"River " + str(self._river) + "\n"
              +"Cave " + str(self._cave) + "\n"
              +"Occupied " + str(self._occupied) + "\n"
              +"Unoccupied " + str(self._unoccupied))
    
    
    name = property(getName)
    height = property(getHeight)
    width = property(getWidth)
    currentLives = property(getCurrentLives, setCurrentLives)
    startingLives = property(getStartingLives)
    money = property(getMoney)
    currentWave = property(getCurrentWave, setCurrentWave)
    currentEnemy = property(getCurrentEnemy, setCurrentEnemy)
    noOfWaves = property(getNoOfWaves)
    waves = property(getWaves)
    enemyPath = property(getEnemyPath)
    occupied = property(getOccupied)
    river = property(getRiver)
    road = property(getRoad)
    unoccupied = property(getUnoccupied)
    enemiesSummoned = property(getEnemiesSummoned)
    cave = property(getCave)
    mountain = property(getMountain)
    bridge = property(getBridge)
    towersBuild = property(getBuildTowers)
    projectiles = property(getProjectiles)
    
    
'''
def main():
    
    gameboard1 = GameBoard()
    gameboard1.readMapData("Map1.txt")
    gameboard1.printMapInfo()

main()
'''