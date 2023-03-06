# import geatpy as ea
# print(ea.__version__)
# print(__import__('sys').version)


# from deap import base, creator

# import deap as deap
# print(deap.__version__)


# creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
# creator.create("Individual", list, fitness=creator.FitnessMin)



import geatpy as ea
import numpy as np

# x ^3 + x - 128 = 0

# 构建问题
r = 1  # 目标函数需要用到的额外数据
@ea.Problem.single
def evalVars(Vars):  # 定义目标函数（含约束）
    x = Vars[0]
    f = x ** 10 + x - 128
    if(f > 0):
        f = -f
    return f, 0

problem = ea.Problem(name='soea quick start demo',
                        M=1,  # 目标维数
                        maxormins=[-1],  # 目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标
                        Dim=1,  # 决策变量维数
                        varTypes=[0],  # 决策变量的类型列表，0：实数；1：整数
                        lb=[0],  # 决策变量下界
                        ub=[100],  # 决策变量上界
                        evalVars=evalVars)
# 构建算法
algorithm = ea.soea_DE_currentToBest_1_bin_templet(problem,
                                    ea.Population(Encoding='RI', NIND=20),
                                    MAXGEN=500,  # 最大进化代数。
                                    logTras=1,  # 表示每隔多少代记录一次日志信息，0表示不记录。
                                    trappedValue=1e-6,  # 单目标优化陷入停滞的判断阈值。
                                    maxTrappedCount=100)  # 进化停滞计数器最大上限值。
# 求解
res = ea.optimize(algorithm, seed=1, verbose=True, drawing=1, outputMsg=True, drawLog=False, saveFlag=True, dirName='result')






