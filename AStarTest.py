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


# 树结构，用于回溯路径
class Vector2Node:
    frontNode = None
    childNodes = []

    def __init__(self, pos):
        self.pos = pos


# 地图定义，0是空位，1是障碍
class Map:
    map = [[0]*MAP_SIZE]*MAP_SIZE
    tree = None

    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint

        self.tree = Vector2Node(startPoint)
        willProcessNodes = []
        willProcessNodes.append(self.tree)
        while not self.isFoundEnd or willProcessNodes.count == 0:
            node = willProcessNodes.pop()
            neighbors = self.getNeighbors(node.pos)
            for neighbor in neighbors:
                childNode = Vector2Node(neighbor)
                childNode.frontNode = node
                node.childNodes.append(childNode)
                willProcessNodes.insert(0, childNode)


    def getNeighbors(self, pos):
        result = []
        neighborDises = [ Vector2(1, 0), Vector2(0, 1), Vector2(-1, 0), Vector2(0, -1)]
        for neighborDis in neighborDises:
            newPos = pos + neighborDis
            if self.isObstacle(newPos) or self.isOpenedPos(newPos) :
                continue
            result.append(newPos)
        return result
    
    def isObstacle(self, pos):
        return self.map[pos.y][pos.x] == 1

    def isOpenedPos(self, pos):
        if self.tree == None:
            return True
        nodes = []
        nodes.append(self.tree)
        while nodes.count != 0:
            node = nodes.pop()
            if node.pos == pos:
                return False
            nodes.extend(node.childNodes)
        return True

    def isFoundEnd(self):
        if self.tree == None:
            return False
        nodes = []
        nodes.append(self.tree)
        while nodes.count != 0:
            node = nodes.pop()
            if node.pos == self.endPoint:
                return True
            nodes.extend(node.childNodes)
        return False



startPoint = Vector2(0, 0)
endPoint = Vector2(8, 8)

map = Map(startPoint, endPoint)
print(map.map)






GetBackGroundGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, edgecolor = 'gray', facecolor = 'w')
GetObstacleGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, color = 'gray')


ax = plt.gca()
ax.set_xlim([0, MAP_SIZE])
ax.set_ylim([0, MAP_SIZE])

for x in range(MAP_SIZE):
    for y in range(MAP_SIZE):
        ax.add_patch(GetBackGroundGrid(x, y))

plt.show()