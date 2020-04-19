import dot_class
import graph_class
import unionfind_class
import status_enum
import random
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import xlwt

def calculateDistance(dotA, dotB):
    return math.sqrt((dotA.getx()-dotB.getx())**2+(dotA.gety()-dotB.gety())**2+(dotA.getz()-dotB.getz())**2)


def showAllDots(dots):
    for dot in dots:
        dot.showPosition()


def printSaparator():
    print('----------------------------------------')


def initializeDots(size, broadcastTime, n):
    dots = []
    for i in range(0, n):
        dot = dot_class.Dot(size, broadcastTime)
        for j in dots:
            while (j.equals(dot)):
                dot.move(size, size)
        dots.append(dot)
    return dots


def moveDots(dots, size, distance):
    for i in range(0, len(dots)):
        dots[i].move(size, distance)

        for j in range(0, i):
            while (dots[j].equals(dots[i])):
                dots[i].move(size, distance)
        if (dots[i].getStatus() == status_enum.Status.NORMAL):
            dots[i].updateReadyThreshold()


def updateBroadcastingDots(dots):
    for dot in dots:
        if (dot.getStatus() == status_enum.Status.BROADCASTING):
            dot.broadcast()


def updateCheckReady(dots):
    for dot in dots:
        if (dot.getStatus() == status_enum.Status.NORMAL):
            dot.checkReady()


def updateDotsToBroadcastingOrWaiting(dots, graph):
    listeningDots = graph.getAllListeningDots()
    for dot in dots:
        if (dot.getStatus() == status_enum.Status.READY):
            if (dot in listeningDots):
                dot.wait()
            else:
                dot.beginBroadcast()
        elif (dot.getStatus() == status_enum.Status.WAITING):
            if (dot in listeningDots):
                dot.wait()
            else:
                dot.beginBroadcast()


def updateGraph(dots, broadcastRange):
    graph = graph_class.Graph()
    for dot in dots:
        if (dot.getStatus() == status_enum.Status.BROADCASTING):
            adjacentListeningDots = set()
            adjacentBroadcastingDots = set()
            for i in dots:
                if (i == dot):
                    continue
                else:
                    distance = calculateDistance(dot, i)
                    if (distance <= broadcastRange):
                        adjacentListeningDots.add(i)
                    if (i.getStatus() == status_enum.Status.BROADCASTING and distance <= broadcastRange*2):
                        adjacentBroadcastingDots.add(i)
            graph.addToAdjListening(dot, adjacentListeningDots)
            graph.addToAdjBroadcasting(dot, adjacentBroadcastingDots)
    return graph


def updateUnionFind(graph):
    broadcastingDots = graph.getAllKeysFromAdjBroadcasting()
    uf = unionfind_class.UnionFind(broadcastingDots)
    for dot in broadcastingDots:
        adjacentBroadcastingDots = graph.getValueFromAdjBroadcasting(dot)
        for i in adjacentBroadcastingDots:
            uf.union(dot, i)
    uf.createBranch()
    return uf


def solveConfliction(dots, graph, uf):
    dotToBeSilenced = set()
    rootDots = uf.getBranchRoots()
    for rootDot in rootDots:
        subDots = uf.getBranchSubs(rootDot)
        for subDot in subDots:
            audienceOfSubDot = graph.getValueFromAdjListening(subDot)
            for i in subDots:
                if (i == subDot):
                    continue
                elif (i in audienceOfSubDot):
                    dotToBeSilenced.add(i)
    for dot in dotToBeSilenced:
        dots[dots.index(dot)].silent()


def updateAudienceOfDots(dots, graph, uf):
    rootDots = uf.getBranchRoots()
    for rootDot in rootDots:
        subDots = uf.getBranchSubs(rootDot)
        for subDot in subDots:
            coveredAudience = graph.getValueFromAdjListening(subDot)
            for i in subDots:
                if (i == subDot):
                    continue
                else:
                    coveredAudience = coveredAudience.difference(
                        coveredAudience & graph.getValueFromAdjListening(i))
            dots[dots.index(subDot)].operateAudienceSet(coveredAudience)


def initializeAudienceOfDots(dots, graph, broadcastTime):
    for dot in dots:
        if (dot.getStatus()==status_enum.Status.BROADCASTING and dot.getBroadcastTimeLeft() == broadcastTime):
            dot.initializeAudienceSet(graph.getValueFromAdjListening(dot))


def calculateEfficiency(dots):
    efficiency = []
    for dot in dots:
        broadCastCnt = dot.getValidBroadcastCnt()+dot.getInvalidBroadcastCnt()
        workTime = dot.getWaitTimeSum()+dot.getBroadcastTimeSum()
        if (workTime == 0):
            continue
        else:
            if (broadCastCnt==0):
                efficiency.append(0.0)
            else:
                validrate = float(dot.getValidBroadcastCnt())/broadCastCnt
                efficiency.append(float(dot.getBroadcastTimeSum())*validrate/float(workTime))

    sum = 0
    for i in efficiency:
        sum = sum+i

    if (len(efficiency) == 0):
        e = 0
    else:
        e = sum/len(efficiency)

    return e

# SIZE = 10
# N = 10
# STEP = 100


# MOVEDISTANCE = 0.1
# BROADCASTRANGE = 1
# BROADCASTTIME = 1

# timeCnt = 0
# dots = initializeDots(SIZE, BROADCASTTIME, N)
# while (timeCnt < STEP):
#     timeCnt = timeCnt+1
#     moveDots(dots, SIZE, MOVEDISTANCE)
#     # showAllDots(dots)
#     # printSaparator()
#     graph = updateGraph(dots, BROADCASTRANGE)
#     uf = updateUnionFind(graph)
#     updateCheckReady(dots)
#     # showAllDots(dots)
#     # printSaparator()
#     updateDotsToBroadcastingOrWaiting(dots, graph)
#     # showAllDots(dots)
#     # printSaparator()
#     graph = updateGraph(dots, BROADCASTRANGE)
#     uf = updateUnionFind(graph)
#     solveConfliction(dots, graph, uf)
#     # showAllDots(dots)
#     # printSaparator()
#     graph = updateGraph(dots, BROADCASTRANGE)
#     uf = updateUnionFind(graph)
#     initializeAudienceOfDots(dots,graph,BROADCASTTIME)
#     updateAudienceOfDots(dots, graph, uf)
#     updateBroadcastingDots(dots)
#     # showAllDots(dots)
#     # printSaparator()
# e=calculateEfficiency(dots)
# print(str(e))

SIZE=10
STEP=100
MOVEDISTANCE=0.1
BROADCASTRANGE=1
BROADCASTTIME=1

workBook=xlwt.Workbook()
workBookSheet=workBook.add_sheet('n')
for row in range(1,101):
    workBookSheet.write(row,0,row*10)
for col in range(1,11):
    workBookSheet.write(0,col,col)
ansDic={}
for i in range(1,101):
    # ansDic[i*10]=[]
    for j in range(1,11):
        print(str(i*10)+' '+str(j))
        timeCnt = 0
        dots = initializeDots(SIZE, BROADCASTTIME, i*10)
        while (timeCnt < STEP):
            timeCnt = timeCnt+1
            moveDots(dots, SIZE, MOVEDISTANCE)
            # showAllDots(dots)
            # printSaparator()
            graph = updateGraph(dots, BROADCASTRANGE)
            uf = updateUnionFind(graph)
            updateCheckReady(dots)
            # showAllDots(dots)
            # printSaparator()
            updateDotsToBroadcastingOrWaiting(dots, graph)
            # showAllDots(dots)
            # printSaparator()
            graph = updateGraph(dots, BROADCASTRANGE)
            uf = updateUnionFind(graph)
            solveConfliction(dots, graph, uf)
            # showAllDots(dots)
            # printSaparator()
            graph = updateGraph(dots, BROADCASTRANGE)
            uf = updateUnionFind(graph)
            initializeAudienceOfDots(dots,graph,BROADCASTTIME)
            updateAudienceOfDots(dots, graph, uf)
            updateBroadcastingDots(dots)
            # showAllDots(dots)
            # printSaparator()
        e=calculateEfficiency(dots)
        # ansDic[i*10].append(e)
        workBookSheet.write(i,j,e)
workBook.save('n.xls')
print('\n')
   

