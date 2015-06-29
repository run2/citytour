class CityMap:
    def __init__(self):
        self.edges = {}
        self.distances = {}
        self.waittimes = {}
    
    def getConnectedNodes(self, node):
        return self.edges[node]
    
    def getEdgeDistance(self, edge):
        return self.distances[edge]
    
    def getContraint(self,node):
        return self.waittimes[node]