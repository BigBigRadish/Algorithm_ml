# -*- coding: utf-8 -*-  
"""
Created on Sat Mar 03 16:58:05 2018
CART algorithm
@author: Agnostic
"""

import numpy as np
import pickle
import treePlotter


def loadDataSet(filename):
  '''
    ���룺�ļ���ȫ·��
    ���ܣ����������ݱ�����datamat
    �����datamat
  '''
    fr = open(filename)
    datamat = []
    for line in fr.readlines():
        cutLine = line.strip().split('\t')
        floatLine = map(float,cutLine)
        datamat.append(floatLine)
    return datamat


def binarySplitDataSet(dataset,feature,value):
    '''
    ���룺���ݼ������ݼ���ĳһ�����У����������е�ĳ��ȡֵ
    ���ܣ������ݼ��������е�ĳһȡֵ����Ϊ�������������ݼ�
    ��������������ݼ�
    '''
    matLeft = dataset[np.nonzero(dataset[:,feature] <= value)[0],:]
    matRight = dataset[np.nonzero(dataset[:,feature] > value)[0],:]
    return matLeft,matRight

#--------------�ع��������Ӻ���---------------#

def regressLeaf(dataset):
    '''
    ���룺���ݼ�
    ���ܣ������ݼ�����еľ�ֵ
    �������Ӧ���ݼ���Ҷ�ڵ�
    '''
    return np.mean(dataset[:,-1])


def regressErr(dataset):
    '''
    ���룺���ݼ�(numpy.mat����)
    ���ܣ������ݼ��������������ݼ������ƽ����֮��
    ���: ���ݼ����ֺ�����ƽ����
    '''
    #���ڻع�����������ľ�ֵ��ΪҶ�ڵ㣬���������������ƽ����ʵ���Ͼ��Ƿ���
    return np.var(dataset[:,-1]) * np.shape(dataset)[0]

def regressData(filename):
    fr = open(filename)
    return pickle.load(fr)

#--------------�ع����Ӻ���  END  --------------#

def chooseBestSplit(dataset,leafType=regressLeaf,errType=regressErr,threshold=(1,4)):#������Ϊ������ͦ����˼
    thresholdErr = threshold[0];thresholdSamples = threshold[1]
    #�����������ֵ�����ʱ��feature = None,value = ���ֵ�ľ�ֵ��Ҷ�ڵ㣩
    if len(set(dataset[:,-1].T.tolist()[0])) == 1:
        return None,leafType(dataset)
    m,n = np.shape(dataset)
    Err = errType(dataset)
    bestErr = np.inf; bestFeatureIndex = 0; bestFeatureValue = 0
    for featureindex in range(n-1):
        for featurevalue in dataset[:,featureindex]:
            matLeft,matRight = binarySplitDataSet(dataset,featureindex,featurevalue)
            if (np.shape(matLeft)[0] < thresholdSamples) or (np.shape(matRight)[0] < thresholdSamples):
                continue
            temErr = errType(matLeft) + errType(matRight)
            if temErr < bestErr:
                bestErr = temErr
                bestFeatureIndex = featureindex
                bestFeatureValue = featurevalue
    #��������ѡ�������Ż�����������ȡֵ�£����ƽ������δ����ʱ�Ĳ��Ƿ�С����ֵ�����ǣ����ʺϻ���
    if (Err - bestErr) < thresholdErr:
        return None,leafType(dataset)
    matLeft,matRight = binarySplitDataSet(dataset,bestFeatureIndex,bestFeatureValue)
    #��������ѡ�������Ż�����������ȡֵ�£����ֵ��������ݼ����������Ƿ�С����ֵ�����ǣ����ʺϻ���
    if (np.shape(matLeft)[0] < thresholdSamples) or (np.shape(matRight)[0] < thresholdSamples):
        return None,leafType(dataset)
    return bestFeatureIndex,bestFeatureValue


def createCARTtree(dataset,leafType=regressLeaf,errType=regressErr,threshold=(1,4)):

    '''
    ���룺���ݼ�dataset��Ҷ�ӽڵ���ʽleafType��regressLeaf���ع�������modelLeaf��ģ������
         ��ʧ����errType:���ƽ����Ҳ��ΪregressLeaf��modelLeaf���û��Զ�����ֵ������
         �����ٵ���ֵ����������Ӧ������������������
    ���ܣ������ع�����ģ����
    ��������ֵ�Ƕ��������ʽ�����ӻع�������ģ������Ҷ���
    '''
    feature,value = chooseBestSplit(dataset,leafType,errType,threshold)
    #����������ֵ��ĳһ�����ݼ������ȫ���ʱ������Ҷ�ڵ�
    if feature == None: return value
    returnTree = {}
    returnTree['bestSplitFeature'] = feature
    returnTree['bestSplitFeatValue'] = value
    leftSet,rightSet = binarySplitDataSet(dataset,feature,value)
    returnTree['left'] = createCARTtree(leftSet,leafType,errType,threshold)
    returnTree['right'] = createCARTtree(rightSet,leafType,errType,threshold)
    return returnTree

#----------�ع�����֦����----------#
def isTree(obj):#��Ҫ��Ϊ���жϵ�ǰ�ڵ��Ƿ���Ҷ�ڵ�
    return (type(obj).__name__ == 'dict')

def getMean(tree):#������Ƕ���ֵ�
    if isTree(tree['left']): tree['left'] = getMean(tree['left'])
    if isTree(tree['right']): tree['right'] = getMean(tree['right'])
    return (tree['left'] + tree['right'])/2.0

def prune(tree, testData):
    if np.shape(testData)[0] == 0: return getMean(tree)#���ڲ��Լ���û��ѵ���������ݵ����
    if isTree(tree['left']) or isTree(tree['right']):
        leftTestData, rightTestData = binarySplitDataSet(testData,tree['bestSplitFeature'],tree['bestSplitFeatValue'])
    #�ݹ����prune��������������,ע��������������Ӧ�������Ӳ������ݼ�
    if isTree(tree['left']): tree['left'] = prune(tree['left'],leftTestData)
    if isTree(tree['right']): tree['right'] = prune(tree['right'],rightTestData)
    #���ݹ�����������������ΪҶ�ڵ�ʱ������������ݼ������ƽ����
    if not isTree(tree['left']) and not isTree(tree['right']):
        leftTestData, rightTestData = binarySplitDataSet(testData,tree['bestSplitFeature'],tree['bestSplitFeatValue'])
        errorNOmerge = sum(np.power(leftTestData[:,-1] - tree['left'],2)) +sum(np.power(rightTestData[:,-1] - tree['right'],2))
        errorMerge = sum(np.power(testData[:,1] - getMean(tree),2))
        if errorMerge < errorNOmerge:
            print ('Merging')
            return getMean(tree)
        else: return tree
    else: return tree

#---------�ع�����֦END-----------#    

#-----------ģ�����Ӻ���-----------#
def linearSolve(dataset):
    m,n = np.shape(dataset)
    X = np.mat(np.ones((m,n)));Y = np.mat(np.ones((m,1)))
    X[:,1:n] = dataset[:,0:(n-1)]
    Y = dataset[:,-1]
    xTx = X.T * X
    if np.linalg.det(xTx) == 0:
        raise NameError('This matrix is singular, cannot do inverse,\n\
        try increasing the second value of threshold')
        ws = xTx.I * (X.T * Y)
        return ws, X,Y

def modelLeaf(dataset):
    ws,X,Y = linearSolve(dataset)
    return ws

def modelErr(dataset):
    ws,X,Y = linearSolve(dataset)
    yHat = X * ws
    return sum(np.power(Y - yHat,2))

#------------ģ�����Ӻ���END-------#

#------------CARTԤ���Ӻ���------------#

def regressEvaluation(tree, inputData):
    #ֻ�е�treeΪҶ�ڵ�ʱ���Ż����
    return float(tree)

def modelTreeEvaluation(model,inputData):
    #inoutDataΪ������Ϊ1������������
    n = np.shape(inputData)
    X = np.mat(np.ones((1,n+1)))
    X[:,1:n+1] = inputData
    return float(X * model)

def treeForeCast(tree, inputData, modelEval = regressEvaluation):
    if not isTree(tree): return modelEval(tree,inputData)
    if inputData[tree['bestSplitFeature']] <= tree['bestSplitFeatValue']:
        if isTree(tree['left']):
            return treeForeCast(tree['left'],inputData,modelEval)
        else:
            return modelEval(tree['left'],inputData)
    else:
        if isTree(tree['right']):
            return treeForeCast(tree['right'],inputData,modelEval)
        else:
            return modelEval(tree['right'],inputData)

def createForeCast(tree,testData,modelEval=regressEvaluation):
    m = len(testData)
    yHat = np.mat(np.zeros((m,1)))
    for i in range(m):
        yHat = treeForeCast(tree,testData[i],modelEval)
    return yHat

#-----------CARTԤ���Ӻ��� END------------#    

if __name__ == '__main__':

    trainfilename = 'e:\\python\\ml\\trainDataset.txt'
    testfilename = 'e:\\python\\ml\\testDataset.txt'

    trainDataset = regressData(trainfilename)
    testDataset = regressData(testfilename)

    cartTree = createCARTtree(trainDataset,threshold=(1,4))
    pruneTree=prune(cartTree,testDataset)
    treePlotter.createPlot(cartTree)
    y=createForeCast(cartTree,np.mat([0.3]),modelEval=regressEvaluation)