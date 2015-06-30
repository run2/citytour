from sets import Set
import logging
import math

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
    
    
    def setXWaitingList(self,left_right,top_bottom,leftWait,rightWait,topWait,bottomWait):
        
        if(len(left_right.split(','))!=2):
            raise ValueError('Invalid left right nodes')
        else:
            [left,right]=left_right.split(',')
        
        if(len(top_bottom.split(','))!=2):
            raise ValueError('Invalid top bottom nodes')
        else:
            [top,bottom]=top_bottom.split(',')
        
        if(not left in self.nodes or not right in self.nodes or not top in self.nodes or not bottom in self.nodes):
            raise ValueError('One or more of left,top,right,bottom not present in map %r %r %r %r' %(left,top,right,bottom))
        
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
    
    def XWait(self,nextNode):
        initialWait = 0
        waitOppSignal = 30
        selfTime = 10
        if nextNode in self.X_left_right:
            wait = initialWait + math.ceil(self.waitingLeftRight/3)*60 + waitOppSignal + (self.waitingLeftRight%3)*10 + selfTime
        else:
            wait = initialWait + math.ceil(self.waitingTopBottom/3)*60 + waitOppSignal + (self.waitingTopBottom%3)*10 + selfTime
            
        return wait

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
            
        
        logging.info('Wait times initialized as ' + str(waitTimes))
        self.waitTimes = waitTimes
        
    def contains(self,node):
        return node in self.nodes
    
    def getConnectedNodes(self, node):
        return self.edges[node]
    
    def getAvgSpeed(self):
        return self.avgSpeed
    
    def getEdgeDistance(self, start, end):
        # distances are in km
        # converting into seconds @ 60 kmph
        return float(self.distances[start+'-'+end])*self.avgSpeed
    
    def getWaitTime(self,parentNode,nextNode):
        if(None == parentNode or (None != parentNode and parentNode <> 'X' ) ):
            return float(self.waitTimes[nextNode])
        else:
            return float(self.XWait(nextNode)) + float(self.waitTimes[nextNode])
        