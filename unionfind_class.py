class UnionFind(object):
    def __init__(self, tdots):
        super().__init__()
        self.dots = {}
        self.size = {}
        self.visited = {}
        self.branches = {}
        self.cnt = len(tdots)
        self.parts = {}
        for i in tdots:
            self.dots[i] = i
            self.size[i] = 1
            self.visited[i] = False

    def findParent(self, dot):
        while (self.dots[dot] != dot):
            dot = self.dots[dot]
        return dot

    def union(self, dotA, dotB):
        parentA = self.findParent(self.dots[dotA])
        parentB = self.findParent(self.dots[dotB])
        if (parentA != parentB):
            if (self.size[parentA] < self.size[parentB]):
                self.dots[parentA] = parentB
                self.size[parentB] = self.size[parentB]+self.size[parentA]
            else:
                self.dots[parentB] = parentA
                self.size[parentA] = self.size[parentA]+self.size[parentB]
            self.cnt = self.cnt-1

    def createBranch(self):
        for i in self.dots.keys():
            if (self.dots[i] == i):
                self.branches[i] = set()
                self.branches[i].add(i)
                self.visited[i] = True
        for i in self.dots.keys():
            branch = set()
            if (self.visited[i] == True):
                continue
            j = i
            while (self.dots[j] != j):
                self.visited[j] = True
                branch.add(j)
                j = self.dots[j]
            self.branches[j] = self.branches[j] | branch

    def getBranchRoots(self):
        return self.branches.keys()

    def getBranchSubs(self, key):
        return self.branches[key]
