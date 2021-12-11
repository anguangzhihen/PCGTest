import matplotlib.pyplot as plt
import math
from collections import deque
from matplotlib.patches import Rectangle

MAP_SIZE = 20
SQRT_2 = math.sqrt(2)

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
    pos = None  # 当前的x、y位置
    frontNode = None    # 当前节点的前置节点
    childNodes = None   # 当前节点的后置节点们
    g = 0   # 起点到当前界面所经过的距离
    h = 0   # 启发值
    D = 1

    def __init__(self, pos):
        self.pos = pos
        self.childNodes = []

    def f(self):
        return self.g + self.h

    def calcGH(self, targetPos):
        self.g = self.frontNode.g + math.sqrt(pow2(self.pos.x - self.frontNode.pos.x) + pow2(self.pos.y - self.frontNode.pos.y))
        dx = abs(targetPos.x - self.pos.x)
        dy = abs(targetPos.y - self.pos.y)
        self.h = (dx + dy + (SQRT_2 - 2) * min(dx, dy)) * self.D 


NEIGHBOR_DISES = [ Vector2(1, 0), Vector2(1, 1), Vector2(0, 1), Vector2(-1, 1), Vector2(-1, 0), Vector2(-1, -1), Vector2(0, -1), Vector2(1, -1)]


# 地图
class Map:
    map = None  # 地图，0是空位，1是障碍
    startPoint = None   # 起始点
    endPoint = None # 终点

    tree = None # 已经搜寻过的节点，是closed的集合
    foundEndNode = None # 寻找到的终点，用于判断算法结束

    addNodeCallback = None

    def __init__(self, startPoint, endPoint):
        self.startPoint = startPoint
        self.endPoint = endPoint
        row = [0]*MAP_SIZE
        self.map = []
        for i in range(MAP_SIZE):
            self.map.append(row.copy())

    # 判断当前点是否超出范围
    def isOutBound(self, pos):
        return pos.x < 0 or pos.y < 0 or pos.x >= MAP_SIZE or pos.y >= MAP_SIZE
    
    # 判断当前点是否是障碍点
    def isObstacle(self, pos):
        return self.map[pos.y][pos.x] == 1

    # 判断当前点是否已经遍历过
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

    # 获取周围可遍历的邻居节点
    def getNeighbors(self, pos):
        result = []
        for neighborDis in NEIGHBOR_DISES:
            newPos = pos + neighborDis
            if self.isOutBound(newPos) or self.isObstacle(newPos) or self.isClosedPos(newPos):
                continue
            result.append(newPos)
        return result

    def process(self):
        # 初始化open集合，并把起始点放入
        willProcessNodes = deque()
        self.tree = Vector2Node(self.startPoint)
        willProcessNodes.append(self.tree)

        # 开始迭代，直到找到终点，或找完了所有能找的点
        while self.foundEndNode == None and len(willProcessNodes) != 0:
            # 寻找下一个最合适的点，这里是最关键的函数，决定了使用什么算法
            node = self.popLowGHNode(willProcessNodes)

            if self.addNodeCallback != None:
                self.addNodeCallback(node.pos)

            # 获取合适点周围所有的邻居
            neighbors = self.getNeighbors(node.pos)
            for neighbor in neighbors:
                # 初始化邻居，并计算g和h
                childNode = Vector2Node(neighbor)
                childNode.frontNode = node
                childNode.calcGH(self.endPoint)
                node.childNodes.append(childNode)

                # 添加到open集合中
                willProcessNodes.append(childNode)

                # 找到了终点
                if neighbor == self.endPoint :
                    self.foundEndNode = childNode
    
    # 广度优先，直接弹出先遍历到的节点
    def popLeftNode(self, willProcessNodes):
        return willProcessNodes.popleft()
    
    # dijkstra，寻找g最小的节点
    def popLowGNode(self, willProcessNodes):
        foundNode = None
        for node in willProcessNodes:
            if foundNode == None:
                foundNode = node
            else:
                if node.g < foundNode.g:
                    foundNode = node
        if foundNode != None:
            willProcessNodes.remove(foundNode)
        return foundNode
    
    # A*，寻找f = g + h最小的节点
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


GetBackGroundGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, edgecolor = 'gray', facecolor = 'w')
GetObstacleGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, color = 'gray')
GetStartEndGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, color = 'orange')
GetPathGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, color = 'green')
GetFoundPathGrid = lambda x, y: Rectangle((x, y), width = 1, height = 1, color = 'blue')


# 定义地图
startPoint = Vector2(5, 5)
endPoint = Vector2(15, 15)
map = Map(startPoint, endPoint)
for i in range(2, 12):
    map.map[10][i] = 1
for i in range(10, 19):
    map.map[13][i] = 1

# 绘制地图
ax = plt.gca()
ax.set_xlim([0, MAP_SIZE])
ax.set_ylim([0, MAP_SIZE])

for x in range(MAP_SIZE):
    for y in range(MAP_SIZE):
        if map.map[y][x] == 0:
            ax.add_patch(GetBackGroundGrid(x, y))
        else:
            ax.add_patch(GetObstacleGrid(x, y))

ax.add_patch(GetStartEndGrid(map.startPoint.x, map.startPoint.y))
ax.add_patch(GetStartEndGrid(map.endPoint.x, map.endPoint.y))


plt.ion()

# 增加节点添加回调
def AddPathGrid(pos):
    if pos == endPoint or pos == startPoint:
        return
    plt.pause(0.05)
    ax.add_patch(GetPathGrid(pos.x, pos.y))
map.addNodeCallback = AddPathGrid

# 运行算法
map.process()

# 显示寻找到的路径
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

