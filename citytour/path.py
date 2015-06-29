import logging
from collections import deque
import heapq

def findQuickestPath(map, start,end):
    
    """ Find quickest route between two nodes in a city
    
    Method checks 1) if map is of valid type 2) if start and end is part of map
    Then it uses A* to find the quickest route between two nodes
    
    Each node has its own (wait) constraint. This constraint can be just a seconds value
    or it can be a complex criterion, which evalues to a seconds values
    
    The algorithm takes care of this wait constraint along with the edge distances,
    while evaluating the quickest route between two nodes
    
    Keyword arguments:
    map -- {citymap.CityMap-like, graph}
    
    start -- {single character-like, start node}
    
    end -- {single character-like, end node}
    
    Returns :
    path : {array-like, quickest path between start and end}    
    """
    parent = {}
    parent[start] = None
    visitedQueue = deque()
    visitedQueue.append(start)
    
    while not len(visitedQueue) == 0:
        currentNode = visitedQueue.popleft()

        if currentNode == end:
            logging.debug('Goal %r found - breaking out' %currentNode)
            break   
                          
        logging.debug('Visiting %r' %currentNode)
        connectedNodes = map.getConnectedNodes(currentNode)
        for node in connectedNodes:
            if node not in parent:
                visitedQueue.append(node)
                parent[node] = currentNode


    # Now Recontruct the path
    node = end
    path = [end]
    
    while node != start:
        node = parent[node]
        path.append(node)
        
    
    path.reverse()        
    return path
