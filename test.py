'''
Created on 3.5.2016

@author: Rohmu
'''

import unittest, os
from io import StringIO
from gameboard import GameBoard
from corrupted_map_file_error import CorruptedMapFileError

class Test(unittest.TestCase):
    
    def testFlawlessMapFile(self):
        
        self.input_file = os.path.join('./Maps/', 'Test Map.txt')
        
        gb = GameBoard()
        
        game = None
        
        try:
            game = gb.readMapData(self.input_file)
        except CorruptedMapFileError:
            self.fail("Loading a correctly structured file caused an exception")
            
            
        self.assertEqual(gb.name, "Test Map", "Map name not correct")
        self.assertEqual(gb.width, 50, "Width not correc")
        self.assertEqual(gb.height, 20, "Height not correct")
        self.assertEqual(gb.startingLives, 10, "Lives not correct")
        self.assertEqual(gb.money, 100, "Money not correct")
        self.assertEqual(gb.getTowers(), ["t1", "t2"], "Towers not correct")
        self.assertEqual(gb.waves, [[50, ["e1","e2", "e1", "e1", "e1"]], [10, ["e1", "e1", "e2", "e1", "e1"]]], "Waves not correct")


    def testWidth(self):
        
        self.input_file = os.path.join('./Test_Files/', 'Wrong Size.txt')
        
        gb = GameBoard()
        
        raised = False
        try:
            game = gb.readMapData(self.input_file)
        except CorruptedMapFileError:
            raised = True
        
        self.assertTrue(raised, 'Exception raised')
    
    
    def testSymbols(self):
        

if __name__ == '__main__':
    unittest.main()