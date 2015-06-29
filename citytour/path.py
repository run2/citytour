import logging
from collections import deque
import heapq
from citymap import CityMap

def findQuickestPath(map, start,end):
    
    """ Find quickest route between two nodes in a city
    
    Method checks 1) if map is of valid type 2) if start and end is part of map
    Then it uses A* to find the quickest route between two nodes
    
    Each nextNode has its own (wait) constraint. This constraint can be just a seconds value
    or it can be a complex criterion, which evaluates to a seconds values
    
    The algorithm takes care of this wait constraint along with the edge distances,
    while evaluating the quickest route between two nodes. 
    
    
    Keyword arguments:
    map -- {citymap.CityMap-like, graph}
    
    start -- {single character-like, start nextNode}
    
    end -- {single character-like, end nextNode}
    
    Returns :
    path : {array-like, quickest path between start and end}    
    """
    
    if(not isinstance(map,CityMap)):
        raise ValueError('map is not type of CityMap')
    if(not map.contains(start) or not map.contains(end)):
        raise ValueError('map does not contain start and/or end')
    
    previous_node = {}
    previous_node[start] = None
    
    time_till_now = {}
    time_till_now[start] = 0
    #visitedQueue = deque()
    #visitedQueue.append(start)
    visitedQueue = []
    # Push the first item into heap
    heapq.heappush(visitedQueue, (start,0))
    
    while not len(visitedQueue) == 0:
        currentNode = heapq.heappop(visitedQueue)[0]

        if currentNode == end:
            logging.debug('Goal %r found - breaking out' %currentNode)
            break   
                          
        logging.debug('Visiting %r' %currentNode)
        
        connectedNodes = map.getConnectedNodes(currentNode)
        
        for nextNode in connectedNodes:
            
            time_to_be = time_till_now[currentNode] + map.getEdgeDistance(currentNode, nextNode) + map.getWaitTime(nextNode)
            
            if nextNode not in time_till_now or time_to_be < time_till_now[nextNode]:
                time_till_now[nextNode] = time_to_be
                previous_node[nextNode] = currentNode

                priority = time_to_be
                heapq.heappush(visitedQueue,(nextNode,priority))

    # Now Recontruct the path
    nextNode = end
    path = [end]
    
    while nextNode != start:
        nextNode = previous_node[nextNode]
        path.append(nextNode)
        
    
    path.reverse()        
    return path
