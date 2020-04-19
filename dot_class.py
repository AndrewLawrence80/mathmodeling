import random
import status_enum


class Dot(object):
    def __init__(self, size, broadcastTime):
        super().__init__()
        self.x = random.random()*size
        self.y = random.random()*size
        self.z = random.random()*size
        self.status = status_enum.Status.NORMAL

        self.defaultGetReadyThreshold = random.random()
        self.defaultBroadcastTime = broadcastTime

        self.broadcastTimeLeft = 0

        self.broadcastTimeSum = 0
        self.waitTimeSum = 0

        self.validBroadcastCnt = 0
        self.invalidBroadcastCnt = 0

        self.broadcastFailed = False

        self.audience = set()

    def updateReadyThreshold(self):
        self.defaultGetReadyThreshold = random.random()

    def move(self, size, distance):
        tmpx = self.x
        tmpy = self.y
        tmpz = self.z
        tmpx = tmpx+random.random()*distance-distance/2
        while (tmpx < 0 or tmpx >= size):
            tmpx = self.x
            tmpx =tmpx+ random.random()*distance-distance/2
        tmpy =tmpy+ random.random()*distance-distance/2
        while (tmpy < 0 or tmpy >= size):
            tmpy = self.y
            tmpy =tmpy+ random.random()*distance-distance/2
        tmpz = tmpz+random.random()*distance-distance/2
        while (tmpz < 0 or tmpz >= size):
            tmpz = self.z
            tmpz = tmpz+random.random()*distance-distance/2
        self.x = tmpx
        self.y = tmpy
        self.z = tmpz

    def equals(self, dot):
        return self.x == dot.x and self.y == dot.y and self.z == dot.z

    def getx(self):
        return self.x

    def gety(self):
        return self.y

    def getz(self):
        return self.z

    def showPosition(self):
        print('('+str(self.x)+','+str(self.y)+',' +
              str(self.z)+')'+' '+str(self.status))

    def showSum(self):
        print('broadsum='+str(self.broadcastTimeSum)+' waitsum='+str(self.waitTimeSum) +
              ' validcnt='+str(self.validBroadcastCnt)+' invalidcnt='+str(self.invalidBroadcastCnt))

    def getStatus(self):
        return self.status

    def getBroadcastTimeLeft(self):
        return self.broadcastTimeLeft

    def getBroadcastTimeSum(self):
        return self.broadcastTimeSum

    def getWaitTimeSum(self):
        return self.waitTimeSum

    def getValidBroadcastCnt(self):
        return self.validBroadcastCnt

    def getInvalidBroadcastCnt(self):
        return self.invalidBroadcastCnt

    def checkReady(self):
        if (random.random() > self.defaultGetReadyThreshold):
            self.status = status_enum.Status.READY

    def beginBroadcast(self):
        self.status = status_enum.Status.BROADCASTING
        self.broadcastTimeLeft = self.defaultBroadcastTime

    def initializeAudienceSet(self, audienceSet):
        self.audience = self.audience | audienceSet

    def deleteFromAudienceSet(self, audienceTarget):
        self.audience.remove(audienceTarget)

    def operateAudienceSet(self, audienceSet):
        self.audience = self.audience & audienceSet

    def broadcast(self):
        if (len(self.audience) == 0):
            self.broadcastFailed = True
        self.broadcastTimeLeft = self.broadcastTimeLeft-1
        self.broadcastTimeSum = self.broadcastTimeSum + 1
        if (self.broadcastTimeLeft == 0):
            if (self.broadcastFailed == False):
                self.validBroadcastCnt = self.validBroadcastCnt+1
            else:
                self.invalidBroadcastCnt = self.invalidBroadcastCnt+1
            self.audience.clear()
            self.broadcastFailed = False
            self.status = status_enum.Status.NORMAL

    def wait(self):
        self.status = status_enum.Status.WAITING
        self.waitTimeSum = self.waitTimeSum+1

    def silent(self):
        self.invalidBroadcastCnt = self.invalidBroadcastCnt+1
        self.broadcastTimeLeft = 0
        self.audience.clear()
        self.status = status_enum.Status.NORMAL
