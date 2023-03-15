import numpy as np
import time


matrix = np.arange(0, 16).reshape((4,4))
inTrans = np.array([1, 0, 1, 0])
print(matrix)
print(inTrans)
# outTrans = np.dot(matrix, inTrans)
# matrix[:,3] = outTrans

# print(outTrans)
# newMatrix = matrix[:,3]
# print(matrix)

# np.dot(matrix, inTrans, out = np.ascontiguousarray(matrix[:,3]))
# print(matrix)

mt = matrix.T.copy()
it = inTrans.copy()


outTrans = np.empty(4, dtype=np.int32)

startTime = time.time()
for _ in range(0, 10000):
    np.dot(it, mt, out = mt[3,:])
print(mt)
print(time.time() - startTime)


startTime = time.time()
for _ in range(0, 10000):
    np.dot(matrix, inTrans, out=outTrans)
    matrix[:,3] = outTrans
print(matrix)
print(time.time() - startTime)

startTime = time.time()
for _ in range(0, 10000):
    matrix[:,3] = np.dot(matrix, inTrans)
print(matrix)
print(time.time() - startTime)


startTime = time.time()
for _ in range(0, 10000):
    np.dot(matrix, inTrans, out=outTrans)
    matrix[:,3] = outTrans
print(matrix)
print(time.time() - startTime)

startTime = time.time()
for _ in range(0, 10000):
    np.dot(matrix, inTrans, out=outTrans)
    matrix[:,3] = outTrans
print(matrix)
print(time.time() - startTime)

startTime = time.time()
for _ in range(0, 10000):
    matrix[:,3] = np.dot(matrix, inTrans)
print(matrix)
print(time.time() - startTime)








