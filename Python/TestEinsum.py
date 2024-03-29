import numpy as np
import time
import timeit



def TestEinsum():
    var = np.arange(0, 4).reshape((2, 2))

    count = 3

    #print(np.einsum("ji,kj->ik", var, var))
    print(var)
    print(np.einsum("ij,j->j", var, np.array([1, 1])))

    print("--------xx------")
    xx = np.tile(var, (count, 1, 1))
    print(xx)
    print("------zz--------")

    zz = np.einsum("hji,hkj->hki", xx, xx)
    # zz = np.einsum("ija,jka->ika", xx)
    print(zz)

    print("------yy---------")
    var2 = np.array([1, 1])
    yy = np.tile(var2, (count, 1))
    print(yy)

    print(np.einsum("hij,hj->hj", xx, yy))


    # 测试爱因斯坦积的速度
    count = 10000
    xx = np.tile(var, (count, 1, 1))
    yy = np.tile(var2, (count, 1))

    def func():
        # return np.matmul(xx, yy)
        return np.einsum("hij,hj->hi", xx, yy)

    print(func())

    print("爱因斯坦积", timeit.timeit("func()",  setup='from __main__ import func', number=100))



    # count = 3
    xx = np.tile(var, (count, 1, 1))
    yy = np.tile(var2, (count, 1))
    def func2():
        result = np.zeros((count, 2))
        for i in range(0, count):
            x = xx[i]
            y = yy[i]
            result[i] = np.dot(x, y)
        return result
    # print(var)
    # print(var2)
    # print(func2())
    # print("循环方法", timeit.timeit("func2()",  setup='from __main__ import func2', number=100)) # 1.6679876999987755


def Test2():

    # aa = np.arange(0, 6).reshape(2, 3)
    # bb = np.arange(0, 6).reshape(3, 2)
    # print("---aa----")
    # print(aa)
    # print("---bb----")
    # print(bb)
    # print("---dot----")
    # abDot = np.dot(aa, bb)
    # print(abDot, abDot.shape)
    # print("---matmul----")
    # abMatmul = np.matmul(aa, bb)
    # print(abMatmul, abMatmul.shape)
    # print("---@----")
    # abMul = aa @ bb
    # print(abMul, abMul.shape)


    a = np.arange(0, 12).reshape(2, 2, 3)
    b = np.arange(0, 12).reshape(2, 3, 2)
    print("---a----")
    print(a)
    print("---b----")
    print(b)
    print("---dot----")
    abDot = np.dot(a, b)
    print(abDot, abDot.shape)
    print("---matmul----")
    abMatmul = np.matmul(a, b)
    print(abMatmul, abMatmul.shape)
    print("---@----")
    abMul = a @ b
    print(abMul, abMul.shape)


Test2()
