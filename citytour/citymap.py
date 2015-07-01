from sets import Set
import logging
import math

"""A class to hold a city map with the following assumption

1) There can be n number of nodes/(traffic lights)

2) If there is a connection between two nodes, that is called an edge

3) Each edge has a length l in KM. This l parameter per edge is configurable

4) There is a special node/light called X

5) All nodes, have a constraint s.t a vehicle reaching that node/light
will have to wait for t_n seconds before it can go. This t_n second parameter
or "waittime" per node is configurable. Think about it as cost of overcoming
congestion just before the light. This is fixed value per node.

All nodes except X, does not have a light per say. Imagine these nodes are 4-way
over bridges where the cars can move out of the node as long as they have crossed
the t_n congestion minutes.

6) X is a node/light which allows traffic from ONLY two ways. Left-right-left, and top-bottom-top.
It has a traffic light which flips on and off between both these sides. Each side gets 30 seconds
time. Only one car can move through the light at a time. And each car needs 10 seconds to move
through the intersection. Imagine that X is a cross bridge. The bridge takes 10 minutes to cross
and it wide enough to allow only 1 vehicle at a time.

7) There is a control room, which has the real time information about the number of cars waiting
to cross X in both directions.

8) A car driver can call this control room from any light/node in the city and ask for fastest
route to any other light/node in the city.

9) Say the driver calls control room at time t1 to get directions from N1 to N2. Say the number of 
cars waiting to cross X left-right-left at time t1 is C1 and similarly for top-bottom-top is C2. 
The control room needs to give the fastest route between N1 and N2. To do so, it assumes the 
following worst case situation at X

a) For all routes which go through X, it assumes that in worst case, when the routed car reaches X,
it will be the same C1 and C2 number of cars waiting to cross left-right-left and top-bottom-top directions respectively.

b) It also assumes that after the routed car has got over its initial congestion (Wait Time) at X, the light
will first turn green on the opposite direction compared to the one in the route

Example:
                         C
                         |
    Say X has 4 edges. A-X-B
                         |
                         D
    A and B is on left-X-right
    C and D is on top-X-bottom
    
    Suppose at time t1, there are 3 cars waiting in A-X-B/B-X-A direction and 3 cars waiting in C-X-D/D-X-C direction
    Suppose the route being evaluated will have the routed car approach X (from any of A C or B) and then go towards D.
    Worst case, when it is ready to cross X, the left-right-left light will turn green first. 
    
    So the wait time at X will be the following
    (congestion time e.g 30 seconds) + 
    (30 seconds for 3 cars to go in A-X-B/B-X-A direction) + 
    (30 seconds for 3 cars to go in C-X-D/D-X-C) + 
    (30 seconds no car goes in A-X-B/B-X-A direction) + 
    10 seconds for the routed car to go
    = 30 + 30 + 30 + 30 + 10 = 130 seconds

9) The routed car has a default avg running speed of 60 KMPH. It is configurable.

10) The number of cars waiting on opposite directions at X is configurable

11) The nodes towards left, right, top and bottom of X is configurable

Attributes:
    edges (dict): Edge information for each node. E.g 'A:B,C,D;B:X,C,F'. The nodes are separated by ; edges are separated from source by : and each edge is separated by ,
    distances (dict): Distance information for each edge. E.g 'A:10,2,4;B:5,7,9'. The nodes are separated by ; distances are separated from source by : and the each edge distance is separated by , 
    waitTimes (dict): Wait/Congestion time at each Node. E.g 'A:30;B:30'. The nodes are separated by ; and the source and time is separated by :
    nodes (set): Interally maintained set of all nodes in the city (populated while reading the edge information)
    avgSpeed (float): avg speed as floating point in kmph
    X_left_right (list) : list of two nodes left and right of X
    X_top_bottom (list) : list of two nodes top and bottom of X
    waitingLeftRight (int) : no of cars waiting at X to go left-right-left direction
    waitingTopBottom (int) : no of cars waiting at X to go top-bottom-top direction

"""

class CityMap:
    def __init__(self):
        self.edges = {}
        self.distances = {}
        self.waitTimes = {}
        self.nodes = Set()
        
        self.avgSpeed = 60.0 # kmph
        self.X_left_right = []
        self.X_top_bottom = []
        self.waitingLeftRight = 0
        self.waitingTopBottom = 0
        
        
    def setAvgSpeed(self,speed):
        try:
           self.avgSpeed = float(speed)
        except ValueError:
            raise ValueError('Speed needs to be floating point')
       
        if(self.avgSpeed <=0.0 ):
           raise ValueError('Speed cannot be less or equal to zero')
    
    
    def setXWaitingList(self,left_right,top_bottom,leftWait,rightWait,topWait,bottomWait):
        
        if (not 'X' in self.edges or len(self.edges['X'])!= 4):
            raise ValueError('Set edges of map first including edges of X correctly (must have 4 edges)')
        
        if(len(left_right.split(','))!=2):
            raise ValueError('Invalid left right nodes')
        else:
            [left,right]=left_right.split(',')
        
        if(len(top_bottom.split(','))!=2):
            raise ValueError('Invalid top bottom nodes')
        else:
            [top,bottom]=top_bottom.split(',')

        checkXNeighbours = Set()
        checkXNeighbours.add(left)
        checkXNeighbours.add(right)
        checkXNeighbours.add(top)
        checkXNeighbours.add(bottom)
        
        if(len(checkXNeighbours)!=4):
            raise ValueError('One or more of left,top,right,bottom of X is same. This is not possible - please check config ')
        
        if(not left in self.nodes or not right in self.nodes or not top in self.nodes or not bottom in self.nodes):
            raise ValueError('One or more of left,top,right,bottom not present in map %r %r %r %r' %(left,top,right,bottom))

        if(not left in self.edges['X'] or not right in self.edges['X'] or not top in self.edges['X'] or not bottom in self.edges['X']):
            raise ValueError('One or more of left,top,right,bottom not present as edges of X %r ' %str(self.edges['X']))
        
        self.X_left_right.append(left)
        self.X_left_right.append(right)
        self.X_top_bottom.append(top)
        self.X_top_bottom.append(bottom)
        
        try:
            self.waitingLeftRight += int(leftWait)
            self.waitingLeftRight += int(rightWait)
            self.waitingTopBottom += int(topWait)
            self.waitingTopBottom += int(bottomWait)
        except:
            raise ValueError('Invalid values for waiting number of cars')
    
    def setEdges(self,valueString):
        edges = {}
        
        noOfEdges = len(valueString.split(';'))
        
        if(noOfEdges == 0 ):
            raise ValueError('No Edges are specified')
        
        for node in valueString.split(';'):
            logging.debug('Next node ' + node)
            
            if(len(node.split(':')) <=1 ):
                raise ValueError('Invalid edge format for node %r ' %node)
            
            source = node.split(':')[0]
            destinations = node.split(':') [1]
            if (source == '' or destinations == ''):
                raise ValueError('Invalid source and destinations for node %r ' %node)
            
            if(source=='X' and len(destinations.split(',')) <> 4 ):
                raise ValueError('The node X needs to have 4 and only 4 edges' )
            
            edges[source] = destinations.split(',')
            self.nodes.add(source)
            [self.nodes.add(dest) for dest in destinations.split(',')]
        
        logging.debug('Edges initialized as ' + str(edges))
        self.edges = edges
        
    def setDistances(self,valueString):
        
        if(len(self.edges)==0):
            raise ValueError('Please set Edges first by calling setEdges')
        
        noOfDistances = len(valueString.split(';'))

        if(noOfDistances == 0 or noOfDistances != len(self.edges)):
            raise ValueError('No Distances specified OR does not match with edges')

        edgeDistances = {}
        for currentNode in valueString.split(';'):
            logging.debug('Next node ' + currentNode)
            
            if(len(currentNode.split(':')) <= 1 ):
                raise ValueError('There is no distance information for edges from %r ' %currentNode)

            source = currentNode.split(':')[0]
            
            if(source == '' or not source in self.nodes):
                raise ValueError('There is no source information in edge %r , or this source was not a edge source ' %currentNode)
            
            distances = currentNode.split(':')[1].split(',')
            destinations = self.edges[source]
            
            if(len(distances)!=len(destinations)):
                raise ValueError('The edges and distances do not match up for %r . Edges %r Distances %r ' %(source ,destinations ,distances))
            
            for dist, dest  in zip(distances,destinations):
                edgeDistances[source + '-' + dest] = dist
        
        logging.debug('Distances initialized as ' + str(edgeDistances))
        self.distances = edgeDistances
    
    def setWaitTimes(self,valueString):
        if(len(self.edges)==0 or len(self.distances)==0 ):
            raise ValueError('Please set Edges and Distances first by calling setEdges and setDistances')
        
        noOfWaits = len(valueString.split(';'))

        if(noOfWaits ==0 or noOfWaits!= len(self.nodes) ):
            raise ValueError('No Wait times specified OR does not match with number of nodes')

        waitTimes = {}
        for currentNode in valueString.split(';'):
            
            logging.debug('Next node ' + currentNode)
            
            if(len(currentNode.split(':')) <=1 ):
                raise ValueError('No Wait times specified OR does not match with edge for node %r ' %currentNode)
            
            source = currentNode.split(':')[0]
            waittime = currentNode.split(':')[1]
            
            if(source == '' or not source in self.nodes):
                raise ValueError('No source specified OR does not match with edge for node %r ' %currentNode)

            try:
               waitTimes[source] = float(waittime)
            except ValueError:
                raise ValueError('Speed needs to be floating point at %r ' %currentNode)
            
        
        logging.debug('Wait times initialized as ' + str(waitTimes))
        self.waitTimes = waitTimes
        
    def contains(self,node):
        return node in self.nodes

    def getXWait(self,nextNode):
        #initialWait = 0
        oneLightCycleTime = 60
        oneCarTime = 10
        noOfCarsMovingInOneGreen = 3

        waitingCarsInSameDirection = self.waitingLeftRight if nextNode in self.X_left_right else self.waitingTopBottom 
                
        # opposite side signal green time + 
        # n number of green/red cycles where n is the number of full green signals needed in same direction + 
        # remaining cars to move in same direction partially within a green signal
        # time for this routed car to move
        wait = oneLightCycleTime/2 + math.ceil(waitingCarsInSameDirection/noOfCarsMovingInOneGreen)*(oneLightCycleTime) + (waitingCarsInSameDirection % noOfCarsMovingInOneGreen)*oneCarTime + oneCarTime
        return wait
    
    def getConnectedNodes(self, node):
        return self.edges[node]
    
    def getAvgSpeed(self):
        return self.avgSpeed
    
    def getEdgeTime(self, start, end):
        # distances are in km
        # converting into seconds @ 60 kmph
        return float(self.distances[start+'-'+end])*self.avgSpeed
    
    def getWaitTime(self,parentNode,nextNode):
        if(None == parentNode or (None != parentNode and parentNode <> 'X' ) ):
            return float(self.waitTimes[nextNode])
        else:
            return float(self.getXWait(nextNode)) + float(self.waitTimes[nextNode])
        