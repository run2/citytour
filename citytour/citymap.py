class CityMap:
    def __init__(self):
        self.edges = {}
    
    def neighbors(self, id):
        return self.edges[id]