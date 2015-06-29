'''
Created on Jun 29, 2015

@author: run2
'''
import unittest
from os import path
import sys
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from citymap import CityMap
SHOW_ERROR_MESSAGES = True

class Test(unittest.TestCase):

    def test_setAvgSpeed(self):
        map = CityMap()
        with self.assertRaises(ValueError):
            map.setAvgSpeed('hello')

        with self.assertRaises(ValueError):
            map.setAvgSpeed('')

        map.setAvgSpeed(0)
        self.assertEqual(map.getAvgSpeed(), 0)

        map.setAvgSpeed('0')
        self.assertEqual(map.getAvgSpeed(), 0)

        map.setAvgSpeed('60.0')
        self.assertEqual(map.getAvgSpeed(), 60.0)

    def test_setDistances(self):
        map = CityMap()
        with self.assertRaises(ValueError):
            map.setDistances('1;1')

        map.setEdges('A:B,C;B:C,D')
        
        with self.assertRaises(ValueError):
            map.setDistances('1;1')

        map.setEdges('A:B,C;B:C,D')
        
        with self.assertRaises(ValueError):
            map.setDistances('A:1,2;B:1')

        map.setEdges('A:B,C,E;B:C,D')
        
        with self.assertRaises(ValueError):
            map.setDistances('A:1,2;B:1,3')

        map.setEdges('A:B,C,E;B:C,D')
        
        map.setDistances('A:1,2,3;B:1,3')
        
        self.assertTrue(map.getEdgeDistance('A','E'), 3)
        

    def test_setWaitTimes(self):
        map = CityMap()
        with self.assertRaises(ValueError):
            map.setWaitTimes('1;1')

        map.setEdges('A:B,C;B:C,D')
        
        with self.assertRaises(ValueError):
            map.setWaitTimes('A:30;B:30;C:30;D:30')

        map.setEdges('A:B,C;B:C,D')
        map.setDistances('A:2,5;B:1,3')
        
        with self.assertRaises(ValueError):
            map.setWaitTimes('A:30;B:30;X:30;D:30')

        map.setEdges('A:B,C;B:C,D')
        map.setDistances('A:2,5;B:1,3')
        
        with self.assertRaises(ValueError):
            map.setWaitTimes('B:30;C:30;D:30')

        map.setEdges('A:B,C;B:C,D')
        map.setDistances('A:2,5;B:1,3')
        
        with self.assertRaises(ValueError):
            map.setWaitTimes('A:20;B:30;C:30;D:30;E:45')


        map.setEdges('A:B,C;B:C,D')
        map.setDistances('A:2,5;B:1,3')

        with self.assertRaises(ValueError):
            map.setWaitTimes('A:;B:H;C:30;D:30;E:45')


        map.setEdges('A:B,C;B:C,D,E')
        map.setDistances('A:2,5;B:1,3,6')

        with self.assertRaises(ValueError):
            map.setWaitTimes('A:30;B:30;C:30;D:30')

        map.setEdges('A:B,C;B:C,D,E')
        map.setDistances('A:2,5;B:1,3,6')

        map.setWaitTimes('A:30;B:30;C:30;D:30;E:10')
        
        self.assertTrue(map.getWaitTime('E'), 10)        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()