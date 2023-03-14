import numpy as np

var = np.arange(0, 4).reshape((2, 2))

#print(np.einsum("ji,kj->ik", var, var))
print(var)
print(np.einsum("ij,j->j", var, np.array([1, 1])))

print("--------xx------")
xx = np.tile(var, (3, 1, 1))
print(xx)
print("------zz--------")

zz = np.einsum("hji,hkj->hki", xx, xx)
# zz = np.einsum("ija,jka->ika", xx)
print(zz)

print("------yy---------")
var2 = np.array([1, 1])
yy = np.tile(var2, (3, 1))
print(yy)

print(np.einsum("hij,hj->hj", xx, yy))

