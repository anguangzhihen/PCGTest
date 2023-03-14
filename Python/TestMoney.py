import numpy as np
import matplotlib.pyplot as plt

moneys = [5000, 8000, 17000, 30000, 40000, 60000, 85000, 10000000]
taxes = [0., 0.03, 0.1, 0.2, 0.25, 0.3, 0.35, 0.45 ]
zero = np.zeros(len(moneys))

def func(xs):
    xsTmp = np.copy(xs)
    length = len(xsTmp)
    result = np.zeros(length)
    for i in range(0, len(result)):
        x = xsTmp[i]
        for j in range(0, len(moneys)):
            dMoney = x - moneys[j] 
            subMoney = 0.
            if(j >= 1):
                subMoney = moneys[j - 1]
            if(dMoney > 0.):
                result[i] += (moneys[j] - subMoney) * taxes[j]
            else:
                result[i] += (x - subMoney) * taxes[j]
                break

            # if(j > 1):
            #     mon -= moneys[j-1]
            # if(mon <= 0.):
            #     result[i] += (moneys[j] + x) * taxes[j]
            #     break
            # else:
            #     result[i] += moneys[j] * taxes[j]
        
    return result / xs
    # return np.divide(result, xs)


# print(func(np.array([8000, 10000])))

    # length = len(x)
    # tmpX = np.copy(x)
    # tax = np.zeros(length)
    # for i in range(0, len(moneys)):
    #     tmpX -= moneys[i]
    #     print("STAT")
    #     print(tmpX)
    #     tax += np.amin(np.concatenate((tmpX + moneys[i], np.linspace(moneys[i], moneys[i], length)))) * taxes[i]
    #     # tax += np.amin(np.array([moneys[i] + x, moneys[i]])) * taxes[i]
    #     tmpX = np.amax(np.concatenate((tmpX, np.linspace(0., 0., length))))
    # return tax / x

# def func2(x):
#     print(x)
#     return x + x


plt.ion()
x = np.linspace(0, 1000000, 100)
plt.plot(x, func(x))
plt.ioff()
plt.show()











