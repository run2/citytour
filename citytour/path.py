import logging
from collections import deque
import heapq
from citymap import CityMap

def findQuickestPath(map, start,end):
    
    """ Find quickest route between two nodes in a city
    
    Method checks 1) if map is of valid type 2) if start and end is part of map
    Then it uses Dijkstra's algorithm to find the quickest route between two nodes
    
    Each node has its own (wait) constraint. This constraint can be just a seconds value
    or it can be a complex criterion, which evaluates to a seconds values. Currently
    it is hard coded that ONLY node X can have a complex criterion. 
    
    The algorithm takes care of this wait constraint along with the edge distances,
    while evaluating the quickest route between two nodes. 
    
    Dijkstra's algorithm (https://en.wikipedia.org/wiki/Dijkstra's_algorithm)
    
    Keyword arguments:
    map -- {citymap.CityMap-like, graph}
    
    start -- {single character-like, start nextNode}
    
    end -- {single character-like, end nextNode}
    
    Returns :
    path,time : {tuple-like, (quickest path between start and end,time taken)}    
    """
    # check arguments
    if(not isinstance(map,CityMap)):
        raise ValueError('map is not type of CityMap')
    
    if(not map.contains(start) or not map.contains(end)):
        raise ValueError('map does not contain start and/or end')
    
    if(start == end):
        raise ValueError('Start and End is the same. This is not allowed.')

    # to keep track of parent node from a bfs perspective    
    previous_node = {}
    previous_node[start] = None
    
    # to keep track of local optimal
    time_till_now = {}
    time_till_now[start] = 0
    
    # Queue to hold the nodes for bfs according to priority
    visitedQueue = []
    # Priority Queue of bfs where the priority is greedy based on dynamically evaluated local optimal solution
    # items are tuples of type (cost,node) where cost the the time taken to reach node
    heapq.heappush(visitedQueue, (0,start))
    
    while not len(visitedQueue) == 0:
        # pop is best optimal solution
        currentNode = heapq.heappop(visitedQueue)[1]

        
        if currentNode == end:
            logging.debug('Goal %r found - breaking out' %currentNode)
            break   
                          
        logging.debug('Visiting %r' %currentNode)
        
        connectedNodes = map.getConnectedNodes(currentNode)
        
        for nextNode in connectedNodes:

            # avoid going back to parent            
            if nextNode == previous_node[currentNode]:
                continue
            
            # find the optimal time taken to reach nextNode
            # getEdgeTime gives the time to go from currentNode to nextNode
            # getWaitTime gives the time to wait on nextNode once nextNode is reached.
            time_to_reach = time_till_now[currentNode] + map.getEdgeTime(currentNode, nextNode) + map.getWaitTime(currentNode,nextNode)
            
            if nextNode not in time_till_now or time_to_reach < time_till_now[nextNode]:
                time_till_now[nextNode] = time_to_reach
                previous_node[nextNode] = currentNode

                priority = time_to_reach
                heapq.heappush(visitedQueue,(priority,nextNode))

    # Now Recontruct the path
    nextNode = end
    path = [end]
    
    while nextNode != start:
        nextNode = previous_node[nextNode]
        path.append(nextNode)
        
    path.reverse()        
    return path,time_till_now[end]
