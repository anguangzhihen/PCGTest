import math
import numpy as np
import scipy.spatial.transform.rotation as R 

# def iterateNum():
#     yield 1
#     yield 2

# for i in iterateNum():
#     print(i)



mat = R.Rotation.from_euler("xyz", [ 0, -np.pi / 2., 0 ], False).as_matrix()
print(mat)

result = np.matmul(mat, np.array([1, 0, 0]))
print(result)

