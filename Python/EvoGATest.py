import numpy as np
import matplotlib.pyplot as plt

def pow2(x):
    return x * x

def fillBits(size):
    return (1 << size) - 1

POP_SIZE = 10    # 种群规模
DNA_SIZE = 5    # 基因最大值
MAX_X = fillBits(DNA_SIZE) # x最大的值
N_GENERATIONS = 100  # 最大循环的代数
MUTATION_RATE = 0.01

def func(x):
    return pow2(x)

# 获取适应度
def getFitness(pred):
    return pred + 1e-3 - min(pred)

# 选择父代，使用适合比例选择（FPS）机制
def select(pop, fitness):
    return np.random.choice(pop, size = POP_SIZE, replace = True, p = fitness / fitness.sum())

# 重组
def crossover(parent, pop):
    # 选择一个交叉的个体
    other = np.random.choice(pop)
    # 选择交叉点
    point = np.random.randint(1, DNA_SIZE - 1)
    cross = [fillBits(point), fillBits(point) ^ MAX_X]
    np.random.shuffle(cross)
    return (parent & cross[0]) + (other & cross[1])

# 突变（本问题中可以使用格雷码以保证连续整数在二进制变化中的汉明距离也为1）
def mutate(child):
    for i in range(DNA_SIZE):
        # 获得突变位置
        point = 1 << i
        if np.random.rand() < MUTATION_RATE:
            child = child ^ point
    return child


# 初始化种群，从[0, MAX_X]中随机选出
pop = np.random.randint(1, size = POP_SIZE)

plt.ion()

# 生成x序列，从0到5，等分为200个数字
x = np.linspace(0, MAX_X, 200)

# 绘制适应度曲线，传入x序列和y序列，y序列的生成类似于C#中Linq执行x.Select(x=>func(x))操作
plt.plot(x, func(x))

for i in range(N_GENERATIONS):
    # 获取适应度
    fitness = getFitness(pop)

    if 'sca' in globals():
        sca.remove()
    sca = plt.scatter(pop, func(pop), s = 200, lw = 0, c = 'red', alpha = 0.5)
    plt.pause(0.02)

    print(pop, ", max:", max(pop))

    # 父代选择
    pop = select(pop, fitness)
    popCopy = pop.copy()
    for popIndex in range(len(pop)):
        parent = pop[popIndex]
        # 重组，使用单点交叉
        child = crossover(parent, popCopy)
        # 突变，使用位翻转
        child = mutate(child)
        # 生存选择，使用基于年龄的替代策略，但父代和子代数量相同，所以将所有子代替换成父代
        pop[popIndex] = child

plt.ioff()
plt.show()


