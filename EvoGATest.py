import numpy as np
import matplotlib.pyplot as plt

POP_SIZE = 4    # 种群规模
MAX_X = 0b11111 # x最大的值
X_BOUND = [0, MAX_X]
N_GENERATIONS = 10  # 最大循环的代数

def pow2(x):
    return x * x

def func(x) : 
    return pow2(x)

# 获取适应度
def getFitness(pred):
    return pred

# 选种
def select(pop, fitness):
    pass

# 交叉
def crossover():
    pass

# 突变
def mutate():
    pass

# 初始化种群，从[0, MAX_X]中随机选出4个个体
pop = np.random.randint(MAX_X + 1, size = POP_SIZE)

print(pop)

plt.ion()

# 生成x序列，从0到5，等分为200个数字
x = np.linspace(0, MAX_X, 200)

# 传入x序列和y序列绘制曲线，y序列的生成类似于C#中Linq执行x.Select(x=>func(x))操作
plt.plot(x, func(x))

for i in range(N_GENERATIONS):
    print(1)


plt.ioff()
plt.show()


