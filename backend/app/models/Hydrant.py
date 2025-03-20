from backend.app.utils.calculation import calculate_distance

class Hydrant:
    def __init__(self, level, lon, lat,index):
        self.level = level
        self.lon = lon
        self.lat = lat
        self.index = index

    def getIndex(self):
        return self.index

    def getLocation(self):
        return [self.lat, self.lon]

    def isLevelRequired(self, level):
        if(level == 0): return True
        return self.level == level
    
    def getLevel(self):
        return self.level

    def isNear(self, other,range):
        return calculate_distance(self.getLocation(), other.getLocation()) <= range