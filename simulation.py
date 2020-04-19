import dot_class
import graph_class
import unionfind_class
import status_enum
import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

SIZE = 10
N = 10
STEP = 3
MOVEDISTANCE = 2
BROADCASTRANGE = 3
BROADCASTTIME = 2

timeCnt=0
dots=initializeDots(SIZE,BROADCASTTIME)
while (timeCnt<STEP):
    timeCnt+=1
    moveDots(dots,SIZE,MOVEDISTANCE)
    graph=updateGraph(dots,BROADCASTRANGE)
    uf=updateUnionFind(graph)
    updateCheckReady(dots)
    updateDotsToBroadcastingOrWaiting(dots,graph)
    graph=updateGraph(dots,BROADCASTRANGE)
    uf=updateUnionFind(graph)
    solveConfliction(dots,graph,uf)
    updateAudienceOfDots(dots,graph,uf)
    updateBroadcastingDots(dots)
    
def calculateDistance(dotA,dotB):
    return math.sqrt((dotA.getx()-dotB.getx())**2+(dotA.gety()-dotB.gety())**2+(dotA.getz()-dotB.getz())**2)

def initializeDots(size, broadcastTime):
    dots = []
    for i in range(0, N):
        dot = dot_class.Dot(size, broadcastTime)
        for j in dots:
            while (dots[j].equals(dot)):
                dot.move(size, size)
        dots.append(dot)
    return dots

def moveDots(dots,size,distance):
    for dot in dots:
        dot.move(size,distance)
        if (dot.getStauts()==status_enum.Status.NORMAL):
            dot.updateReadyThreshold()

def updateBroadcastingDots(dots):
    for dot in dots:
        if (dot.getStatus()==status_enum.Status.BROADCASTING):
            dot.broadcast()

def updateCheckReady(dots):
    for dot in dots:
        if (dot.getStatus()==status_enum.Status.NORMAL):
            dot.checkReady()

def updateDotsToBroadcastingOrWaiting(dots,graph):
    listeningDots=graph.getAllListeningDots()
    for dot in dots:
        if (dot.getStatus()==status_enum.Status.READY):
            if (dot in listeningDots):
                dot.wait()
            else:
                dot.beginBroadcast()
        elif (dot.getStatus()==status_enum.Status.WAITING):
            if (dot in listeningDots):
                dot.wait()
            else:
                dot.beginBroadcast()

def updateGraph(dots,broadcastRange):
    graph=graph_class.Graph()
    for dot in dots:
        if (dot.getStatus()==status_enum.Status.BROADCASTING):
            adjacentListeningDots=set()
            adjacentBroadcastingDots=set()
            for i in dots:
                if (i==dot):
                    continue
                else:
                    distance=calculateDistance(dot,i)
                    if (distance<=broadcastRange):
                        adjacentListeningDots.add(i)
                    if (i.getStatus()==status_enum.Status.BROADCASTING and distance<=broadcastRange*2):
                        adjacentBroadcastingDots.add(i)
    graph.addToAdjListening(dot,adjacentListeningDots)
    graph.addToAdjBroadcasting(dot,adjacentBroadcastingDots)

def updateUnionFind(graph):
    broadcastingDots=graph.getAllKeysFromAdjBroadcasting()
    uf=unionfind_class.UnionFind(broadcastingDots)
    for dot in broadcastingDots:
        adjacentBroadcastingDots=graph.getValueFromAdjBroadcasting(dot)
        for i in adjacentBroadcastingDots:
            uf.union(dot,i)
    uf.createBranch()
    return uf

def solveConfliction(dots,graph,uf):
    dotToBeSilenced=set()
    rootDots=uf.getBranchRoots()
    for rootDot in rootDots:
        subDots=uf.getBranchSubs(rootDot)
        for subDot in subDots:
            audienceOfSubDot=graph.getValueFromAdjListening(subDot)
            for i in subDots:
                if (i==subDot):
                    continue
                elif (i in audienceOfSubDot):
                    dotToBeSilenced.add(i)
    for dot in dotToBeSilenced:
        dots[dots.index(dot)].silence()

def updateAudienceOfDots(dots,graph,uf):
    rootDots=uf.getBranchRoots()
    for rootDot in rootDots:
        subDots=uf.getBranchSubs(rootDot)
        for subDot in subDots:
            coveredAudience=graph.getValueFromAdjListening(subDot)
            for i in subDots:
                if (i==subDot):
                    continue
                else:
                    coveredAudience=coveredAudience.difference(coveredAudience&graph.getValueFromAdjListening(i))
            dots[dots.index(subDot)].operateAudience(coveredAudience)        

