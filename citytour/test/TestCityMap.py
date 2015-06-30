'''
Created on Jun 29, 2015

@author: run2
'''
import unittest
from os import path
import sys
sys.path.append( path.dirname( path.dirname( path.abspath(__file__) ) ) )
from citymap import CityMap
from path import findQuickestPath
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
        
        self.assertTrue(map.getWaitTime(None,'E'), 10)        
    
    def test_worstWaitAtX(self):
        map = CityMap()

        with self.assertRaises(ValueError):
            map.setXWaitingList('A','B,C',2,3,0,1)

        with self.assertRaises(ValueError):
            map.setXWaitingList('A','B,C',2,3,0,1)

        map.setEdges('A:B,C;B:C,D')
        map.setXWaitingList('A,B','C,D',2,3,0,1)
        
        self.assertEqual(map.X_left_right, ['A','B'])
        
        self.assertEqual(map.X_top_bottom, ['C','D'])
        
        self.assertEqual(map.waitingLeftRight, 5)
        
        self.assertEqual(map.waitingTopBottom, 1)
        
        self.assertEqual(map.XWait('A'),120)
        
        self.assertEqual(map.XWait('C'),50)
    
    def test_algo(self):
        
        map = CityMap()
        map.setEdges('A:X,D;X:E,B,C,A;E:B,X;B:D,C,X,E;D:C,B,A;C:X,B,D')
        map.setDistances('A:1,6;X:0.5,1,0.5,1;E:1,0.5;B:2,2,1,1;D:2,2,6;C:0.5,2,2')
        map.setWaitTimes('A:30;X:30;E:30;B:30;D:30;C:30')
        map.setAvgSpeed('60.0')
        map.setXWaitingList('C,E','A,B','3','0','0','3')
        
        self.assertEqual(findQuickestPath(map,'E','B')[0], ['E','B'])
        
        self.assertEqual(findQuickestPath(map,'E','B')[1], 90)
                
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()