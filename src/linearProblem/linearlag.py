# -*- coding: utf-8 -*-  
#编程实现对数几率回归
import numpy as np
from numpy import random
def dataload(filename,l,r):#导入数据，感觉导入的有点困难
    f=open(filename)
    ar=f.readlines()
    num=len(ar)
    mat=np.zeros((r-l+1,num))
    ind=0
    for line in ar:
        line.split('\n')
        linelist=line.split(' ')
        mat[0:r-l,ind]=linelist[l:r]
        mat[r-l:r-l+1,ind]=1.0
        ind=ind+1
    return mat
x=dataload("1.txt",0,2)
y=dataload("1.txt",2,3)
beta=random.random(size=(3,1))#随机生成初始的beta矩阵
def p1(mat,p):
    ha=np.dot(mat.T,x[:,p])
    return np.exp(ha)/(1+np.exp(ha))
def one(mat):#求关于beta函数的一阶导
    tep=np.zeros((3,1))
    for i in range(17):
        temp=np.zeros((3,1))
        for j in range(3):
            temp[j,0]=x[j,i]
        tep=tep+temp*(y[0,i]-p1(mat,i))
    return -1.0*tep
def two(mat):#二阶导
    tep=np.zeros((3,3))
    for i in range(17):
        temp=np.zeros((3,1))
        for j in range(3):
            temp[j,0]=x[j,i]
        tep=tep+np.dot(temp,temp.T)*p1(mat,i)*(1-p1(mat,i))
    return tep
cnt=10000
for i in range(cnt):#使用牛顿法迭代cnt次得到beta矩阵
    tep=two(beta)
    if(np.linalg.det(tep)==0):
        break
    else :
        tep=np.linalg.inv(tep)
        beta=beta-np.dot(tep,one(beta))
ans=np.dot(beta.T,x)
def sigmoid(p):#sigmoid 函数（对数几率函数）
    return 1.0/(1+np.exp(-p))
for i in range(17):
    print(sigmoid(ans[0,i]))