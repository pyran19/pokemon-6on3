import pulp
import numpy as np
import random

nPT=6

#利得行列
#横列を自分、縦列を相手とみて
#自分有利な時は1を、相手有利な時は-1を入力して6×6行列を作る
A=np.array([
 [ 0, -1,  1,  1, -1,  1],
 [ 0,  0, -1,  1,  0,  1],
 [ 1,  0,  0,  0,  0, -1],
 [-1, -1,  0, -1,  0,  0],
 [ 0,  0,  0,  0,  1,  0],
 [ 1,  1,  0,  0,  1, -1] ])
basis=np.array([
      [1,1,1,0,0,0],
      [1,1,0,1,0,0],
      [1,1,0,0,1,0],
      [1,1,0,0,0,1],
      [1,0,1,1,0,0],
      [1,0,1,0,1,0],
      [1,0,1,0,0,1],
      [1,0,0,1,1,0],
      [1,0,0,1,0,1],
      [1,0,0,0,1,1],
      [0,1,1,1,0,0],
      [0,1,1,0,1,0],
      [0,1,1,0,0,1],
      [0,1,0,1,1,0],
      [0,1,0,1,0,1],
      [0,1,0,0,1,1],
      [0,0,1,1,1,0],
      [0,0,1,1,0,1],
      [0,0,1,0,1,1],
      [0,0,0,1,1,1]])

#三匹一組での利得行列への変換
def convertTrio(A):
  B=basis.dot(A.dot(basis.T))
  return B

#利得行列のランダム生成
def randMatEle(good,bad):
    r=random.random()
    if r<good:
        result=1
    elif r<good+bad:
        result=-1
    else:
        result=0
    return result
def randMatrix():
    temp=[]
    for i in range(36):
        temp.append(randMatEle(0.2,0.2))
    return np.reshape(np.array(temp),(6,6))

#線形計画法
def selection(A):
  lp = pulp.LpProblem(sense=pulp.LpMaximize)
  v = pulp.LpVariable("v") 
  x = [ pulp.LpVariable("x_"+str(i)) for i in range(20) ]
  for i in range(20):
    lp += v <= pulp.lpDot(A[:,i], x)
  for i in range(20):
    lp += x[i] >= 0
    lp += x[i] <= 1
  lp += pulp.lpSum(x) == 1
  lp += v
  lp.solve(pulp.PULP_CBC_CMD(msg=False))
  x = np.array([ x[i].value() for i in range(20) ])

  print("最適な選出率(1が選出、0が非選出)")
  for i in range(20):
    print(basis[i],int(x[i]*100),"%")
  print("有利ポケモンの数-不利ポケモンの数: ",v.value())
  return x

#A=randMatrix()
B=convertTrio(A)
x=selection(B)

