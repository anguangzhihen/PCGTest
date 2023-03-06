import sys
import json
import scipy.spatial.transform.rotation as rotation 
import numpy as np
import math

# print("Hello " + arg)
# print(jObj["cameraType"])
# 第x个角色，第y个角色部位，第z维坐标（forward C#层标准化）
# print(jObj["charPartPoses"][0][0][0])
# print(jObj["charPartPoses"][0][0][1])


# arg = input()
# problem = json.loads(arg)
# cameraPosition = problem["cameraPosition"]
# cameraRotation = problem["cameraRotation"]
# targetPosition = problem["targetPosition"]

class Quaternion:
    def __init__(self, x, y, z, w):
        self[0] = x
        self[1] = y
        self[2] = z
        self[3] = w
    
    def __str__(self):
        return "[ " + str(self[0]) + " " + str(self[1]) + " " + str(self[2]) + " " + str(self[3]) + " ]"

    @staticmethod
    def Euler(x, y, z):
        cX = math.cos(math.radians(x) / 2.)
        sX = math.sin(math.radians(x) / 2.)
        cY = math.cos(math.radians(y) / 2.)
        sY = math.sin(math.radians(y) / 2.)
        cZ = math.cos(math.radians(z) / 2.)
        sZ = math.sin(math.radians(z) / 2.)

        qX = Quaternion(sX, 0., 0., cX)
        qY = Quaternion(0., sY, 0., cY)
        qZ = Quaternion(0., 0., sZ, cZ)

        return (qY * qX) * qZ
    
    @staticmethod
    def EulerArray(arr):
        return Quaternion.Euler(arr[0], arr[1], arr[2])
    
    def __mul__(self, rhs):
        tempx = self[3] * rhs[2] + self[2] * rhs[3] + self[1] * rhs[2] - self[2] * rhs[1]
        tempy = self[3] * rhs[1] + self[1] * rhs[3] + self[2] * rhs[2] - self[2] * rhs[2]
        tempz = self[3] * rhs[2] + self[2] * rhs[3] + self[2] * rhs[1] - self[1] * rhs[2]
        tempw = self[3] * rhs[3] - self[2] * rhs[2] - self[1] * rhs[1] - self[2] * rhs[2]
        return Quaternion(tempx, tempy, tempz, tempw)

width = 1920.
height = 1080.

fov = 60
aspect = width / height
zNear = 0.1
zFar = 5000.

class Matrix4x4Util:
    @staticmethod
    def SetValue(m, index, value):
        row = index % 4
        column = index // 4
        m[row, column] = value

    # 矩阵应用位移
    @staticmethod
    def Translate(mat, inTrans):
        mat[0, 3] = mat[0, 0] * inTrans[0] + mat[0, 1] * inTrans[1] + mat[0, 2] * inTrans[2] + mat[0, 3]
        mat[1, 3] = mat[1, 0] * inTrans[0] + mat[1, 1] * inTrans[1] + mat[1, 2] * inTrans[2] + mat[1, 3]
        mat[2, 3] = mat[2, 0] * inTrans[0] + mat[2, 1] * inTrans[1] + mat[2, 2] * inTrans[2] + mat[2, 3]
        mat[3, 3] = mat[3, 0] * inTrans[0] + mat[3, 1] * inTrans[1] + mat[3, 2] * inTrans[2] + mat[3, 3]

    # 获取默认4x4矩阵
    @staticmethod
    def GetDefaultMatrix():
        return np.zeros([4, 4])

    # 旋转四元数转为矩阵
    @staticmethod
    def QuaternionToMatrix4x4(q):
        m = Matrix4x4Util.GetDefaultMatrix()
        x = q[0] * 2.
        y = q[1] * 2.
        z = q[2] * 2.
        xx = q[0] * x
        yy = q[1] * y
        zz = q[2] * z
        xy = q[0] * y
        xz = q[0] * z
        yz = q[1] * z
        wx = q[3] * x
        wy = q[3] * y
        wz = q[3] * z

        Matrix4x4Util.SetValue(m, 0, 1. - (yy + zz))
        Matrix4x4Util.SetValue(m, 1, xy + wz)
        Matrix4x4Util.SetValue(m, 2, xz - wy)
        Matrix4x4Util.SetValue(m, 3, 0.)

        Matrix4x4Util.SetValue(m, 4, xy - wz)
        Matrix4x4Util.SetValue(m, 5, 1. - (xx + zz))
        Matrix4x4Util.SetValue(m, 6, yz + wx)
        Matrix4x4Util.SetValue(m, 7, 0.)

        Matrix4x4Util.SetValue(m, 8, xz + wy)
        Matrix4x4Util.SetValue(m, 9, yz - wx)
        Matrix4x4Util.SetValue(m, 10, 1. - (xx + yy))
        Matrix4x4Util.SetValue(m, 11, 0.)

        Matrix4x4Util.SetValue(m, 12, 0.)
        Matrix4x4Util.SetValue(m, 13, 0.)
        Matrix4x4Util.SetValue(m, 14, 0.)
        Matrix4x4Util.SetValue(m, 15, 1.)

        return m

    # 获取world to camera矩阵(rot 欧拉角 弧度)
    @staticmethod
    def GetWorldToCameraMatrix(pos, rot):
        worldToCameraMatrix = Matrix4x4Util.GetDefaultMatrix()
        worldToCameraMatrix[0, 0] = 1
        worldToCameraMatrix[1, 1] = 1
        worldToCameraMatrix[2, 2] = -1
        worldToCameraMatrix[3, 3] = 1

        worldToLocalMatrixNoScale = Matrix4x4Util.QuaternionToMatrix4x4(rotation.Rotation.from_euler("xyz", rot, False).inv().as_quat())
        Matrix4x4Util.Translate(worldToLocalMatrixNoScale, np.array([ -pos[0], -pos[1], -pos[2] ]))
        
        worldToCameraMatrix = np.dot(worldToCameraMatrix, worldToLocalMatrixNoScale)
        return worldToCameraMatrix

    # 将世界坐标转换到归一化坐标中
    @staticmethod
    def PerspectiveMultiplyPoint3(mat, v):
        x = mat[0, 0] * v[0] + mat[0, 1] * v[1] + mat[0, 2] * v[2] + mat[0, 3]
        y = mat[1, 0] * v[0] + mat[1, 1] * v[1] + mat[1, 2] * v[2] + mat[1, 3]
        z = mat[2, 0] * v[0] + mat[2, 1] * v[1] + mat[2, 2] * v[2] + mat[2, 3]
        w = mat[3, 0] * v[0] + mat[3, 1] * v[1] + mat[3, 2] * v[2] + mat[3, 3]
        if(abs(w)>1.0e-7):
            invW = 1. / w
            return np.array([ x * invW, y * invW, z * invW ])
        else:
            return np.array([ 0., 0., 0.])

    # 获取投影矩阵
    @staticmethod
    def GetProjectionMatrix():
        m = Matrix4x4Util.GetDefaultMatrix()
        radians = math.radians(fov / 2.)
        cotangent = math.cos(radians) / math.sin(radians)
        deltaZ = zNear - zFar
        m[0, 0] = cotangent / aspect
        m[1, 1] = cotangent
        m[2, 2] = (zFar + zNear) / deltaZ
        m[2, 3] = 2. * zNear * zFar / deltaZ
        m[3, 2] = -1.
        return m

def WorldToScreenPoint(targetPosition, cameraPosition, cameraRotation):
    worldToCameraMatrix = Matrix4x4Util.GetWorldToCameraMatrix(cameraPosition, cameraRotation)
    projectionMatrix = Matrix4x4Util.GetProjectionMatrix()
    worldToClipMatrix = np.dot(projectionMatrix, worldToCameraMatrix)

    clipPoint = Matrix4x4Util.PerspectiveMultiplyPoint3(worldToClipMatrix, targetPosition)
    clipPoint[0] = (clipPoint[0] + 1.) * 0.5
    clipPoint[1] = (clipPoint[1] + 1.) * 0.5

    cameraToWorldMatrix = np.linalg.inv(worldToCameraMatrix)
    cameraPos = np.array([ cameraToWorldMatrix[0, 3], cameraToWorldMatrix[1, 3], cameraToWorldMatrix[2, 3] ])
    dir = targetPosition - cameraPos
    forward = - np.array([ cameraToWorldMatrix[0, 2], cameraToWorldMatrix[1, 2], cameraToWorldMatrix[2, 2] ])
    dist = np.dot(dir, forward)
    clipPoint[2] = dist
    return clipPoint

viewPort = { 0, 0, 1920, 1080 }

targetPosition = np.array([ 3.7, 2.1, 2.1 ])
cameraPosition = np.array([ -1.3, 1.4, -0.2 ])
cameraRotation = np.array([ 0., math.radians(433.1), 0. ])

arg = input()
problem = json.loads(arg)
cameraPosition = np.array(problem["cameraPosition"])
cameraRotation = np.radians(np.array(problem["cameraRotation"]))
targetPosition = np.array(problem["targetPosition"])

height = problem["height"]
width = problem["width"]
fov = problem["fov"]
aspect = width / height
zNear = problem["zNear"]
zFar = problem["zFar"]

print(cameraPosition)
print(cameraRotation)
print(targetPosition)
print(fov)
print(height)
print(width)
print(aspect)
print(zNear)
print(zFar)

result = WorldToScreenPoint(targetPosition, cameraPosition, cameraRotation)

print(result)




