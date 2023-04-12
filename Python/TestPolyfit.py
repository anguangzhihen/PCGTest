# coding=utf-8

import pylab
import numpy as np

def PolyfitSimple(title, x, y):
    factor = np.polyfit(x, y, 2)
    factorFunc = np.poly1d(factor)
    print(factorFunc)
    
    xTest = np.arange(np.min(x) - 1., np.max(x) + 1., 0.2)
    yTest = factorFunc(xTest)

    pylab.plot(x, y, '*')
    pylab.plot(xTest, yTest, 'r')
    pylab.title(title)
    pylab.legend(loc=3, borderaxespad=0., bbox_to_anchor=(0, 0))
    pylab.show()

    return factor

if __name__ == "__main__":

    fov = np.array([ 22.5, 27.5, 30., 40. ])
    x = np.array([ 1.738238617, 2.208913971, 3.476142084, 9.968383385 ])
    y = np.array([ 0.101664792, 0.163572614, 0.146000479, 0.443979966 ])

    xInScreen = x * np.tan(np.radians(fov) / 2)

    PolyfitSimple("Camera Movement", xInScreen, y)
    # 结果：0.01324 x^2 + 0.04565 x + 0.1039
