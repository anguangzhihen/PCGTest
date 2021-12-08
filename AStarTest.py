import matplotlib.pyplot as plt
import numpy as np

from matplotlib.patches import Rectangle

MAP_SIZE = 10

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

    def __init__(self, pos):
        self.pos = pos
        self.childNodes = []


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
        willProcessNodes = []
        willProcessNodes.append(self.tree)
        while self.foundEndNode == None and len(willProcessNodes) != 0:
            node = willProcessNodes.pop()

            if self.addNodeCallback != None:
                self.addNodeCallback(node.pos)

            neighbors = self.getNeighbors(node.pos)
            for neighbor in neighbors:
                childNode = Vector2Node(neighbor)
                childNode.frontNode = node
                node.childNodes.append(childNode)
                willProcessNodes.insert(0, childNode)

                if neighbor == endPoint :
                    self.foundEndNode = childNode
                

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

print("-------------------------")

GetBackGroundGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, edgecolor = 'gray', facecolor = 'w')
GetObstacleGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, color = 'gray')
GetStartEndGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, color = 'red')
GetPathGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, color = 'green')
GetFoundPathGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, color = 'blue')

ax = plt.gca()
ax.set_xlim([0, MAP_SIZE])
ax.set_ylim([0, MAP_SIZE])



startPoint = Vector2(0, 0)
endPoint = Vector2(8, 8)
map = Map(startPoint, endPoint)
for i in range(1, 10):
    map.map[5][i] = 1
for i in range(0, 9):
    map.map[2][i] = 1

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
        ax.add_patch(GetFoundPathGrid(nodeTmp.pos.x, nodeTmp.pos.y))

plt.ioff()

plt.show()

