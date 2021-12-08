import matplotlib.pyplot as plt
import math
from collections import deque
from matplotlib.patches import Rectangle

MAP_SIZE = 20

def pow2(a):
    return a*a


# 点的定义
class Vector2:
    x = 0
    y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


# 树结构，用于回溯路径
class Vector2Node:
    frontNode = None
    childNodes = None
    pos = None
    g = 0
    h = 0
    D = 1

    def __init__(self, pos):
        self.pos = pos
        self.childNodes = []

    def iterateFrontNode(self, includeSelf):
        node = self
        if includeSelf:
            yield node
        while node != None:
            node = node.frontNode
            if node != None:
                yield node

    def calcGH(self, targetPos):
        # g经过的距离
        for node in self.iterateFrontNode(False):
            self.g += 1
        self.h = (abs(targetPos.x - self.pos.x) + abs(targetPos.y - self.pos.y)) * self.D
        # self.g = pow2(self.g)

        # h预估剩余的距离
        #self.h = math.sqrt(pow2(targetPos.x - self.pos.x) + pow2(targetPos.y - self.pos.y))

    def f(self):
        return self.g + self.h


# 地图定义，0是空位，1是障碍
class Map:
    tree = None
    foundEndNode = None
    addNodeCallback = None

    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint
        row = [0]*MAP_SIZE
        self.map = []
        for i in range(MAP_SIZE):
            self.map.append(row.copy())

    def process(self):
        self.tree = Vector2Node(self.startPoint)
        willProcessNodes = deque()
        willProcessNodes.append(self.tree)
        while self.foundEndNode == None and len(willProcessNodes) != 0:
            node = self.simpleLeftPop(willProcessNodes)

            if self.addNodeCallback != None:
                self.addNodeCallback(node.pos)

            neighbors = self.getNeighbors(node.pos)
            for neighbor in neighbors:
                childNode = Vector2Node(neighbor)
                childNode.frontNode = node
                childNode.calcGH(self.endPoint)

                node.childNodes.append(childNode)
                willProcessNodes.append(childNode)

                if neighbor == self.endPoint :
                    self.foundEndNode = childNode
    
    def simpleLeftPop(self, willProcessNodes):
        return willProcessNodes.popleft()
    
    def popLowGHNode(self, willProcessNodes):
        foundNode = None
        for node in willProcessNodes:
            if foundNode == None:
                foundNode = node
            else:
                if node.f() < foundNode.f():
                    foundNode = node
        if foundNode != None:
            willProcessNodes.remove(foundNode)
        return foundNode

    def getNeighbors(self, pos):
        result = []
        neighborDises = [ Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0), Vector2(0, -1)]
        for neighborDis in neighborDises:
            newPos = pos + neighborDis
            if self.isOutBound(newPos) or self.isObstacle(newPos) or self.isClosedPos(newPos):
                continue
            result.append(newPos)
        return result

    def isOutBound(self, pos):
        return pos.x < 0 or pos.y < 0 or pos.x >= MAP_SIZE or pos.y >= MAP_SIZE
    
    def isObstacle(self, pos):
        return self.map[pos.y][pos.x] == 1

    def isClosedPos(self, pos):
        if self.tree == None:
            return False
        nodes = []
        nodes.append(self.tree)
        while len(nodes) != 0:
            node = nodes.pop()
            if node.pos == pos:
                return True
            if node.childNodes != None:
                for nodeTmp in node.childNodes:
                    nodes.append(nodeTmp)
        return False

GetBackGroundGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, edgecolor = 'gray', facecolor = 'w')
GetObstacleGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, color = 'gray')
GetStartEndGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, color = 'red')
GetPathGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, color = 'green')
GetFoundPathGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, color = 'blue')

ax = plt.gca()
ax.set_xlim([0, MAP_SIZE])
ax.set_ylim([0, MAP_SIZE])


startPoint = Vector2(5, 5)
endPoint = Vector2(15, 15)
map = Map(startPoint, endPoint)
for i in range(2, 12):
    map.map[10][i] = 1
for i in range(10, 19):
    map.map[13][i] = 1

for x in range(MAP_SIZE):
    for y in range(MAP_SIZE):
        if map.map[y][x] == 0:
            ax.add_patch(GetBackGroundGrid(x, y))
        else:
            ax.add_patch(GetObstacleGrid(x, y))

ax.add_patch(GetStartEndGrid(map.startPoint.x, map.startPoint.y))
ax.add_patch(GetStartEndGrid(map.endPoint.x, map.endPoint.y))


plt.ion()
def AddPathGrid(pos):
    plt.pause(0.05)
    ax.add_patch(GetPathGrid(pos.x, pos.y))

map.addNodeCallback = AddPathGrid
map.process()

if map.foundEndNode == None:
    print("没有找到终点")
else:
    nodes = []
    node = map.foundEndNode
    while node != None:
        nodes.append(node)
        node = node.frontNode
    
    for nodeTmp in nodes[::-1]:
        if nodeTmp.pos == startPoint or nodeTmp.pos == endPoint:
            continue
        plt.pause(0.05)
        ax.add_patch(GetFoundPathGrid(nodeTmp.pos.x, nodeTmp.pos.y))

plt.ioff()

plt.show()

