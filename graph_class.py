class Graph(object):
    def __init__(self):
        super().__init__()
        self.adjacentDotListening = {}
        self.adjacentDotBroadcasting = {}

    def addToAdjListening(self, key, value):
        self.adjacentDotListening[key] = value

    def addToAdjBroadcasting(self, key, value):
        self.adjacentDotBroadcasting[key] = value

    def getAllItemsFromAdjListening(self):
        return self.adjacentDotListening.items()

    def getAllItemsFromAdjBroadcasting(self):
        return self.adjacentDotBroadcasting.items()

    def getAllKeysFromAdjListening(self):
        return self.adjacentDotListening.keys()

    def getAllKeysFromAdjBroadcasting(self):
        return self.adjacentDotBroadcasting.keys()

    def getAllValuesFromAdjListening(self):
        return self.adjacentDotListening.values()

    def getAllValuesFromAdjBroadcasting(self):
        return self.adjacentDotBroadcasting.values()

    def getValueFromAdjListening(self, key):
        return self.adjacentDotListening[key]

    def getValueFromAdjBroadcasting(self, key):
        return self.adjacentDotBroadcasting[key]

    def getAllListeningDots(self):
        listeningDots=set()
        broadcastingDots=self.getAllKeysFromAdjListening()
        for broadcastingDot in broadcastingDots:
            listeningDots=listeningDots|self.getValueFromAdjListening(broadcastingDot)
        return listeningDots