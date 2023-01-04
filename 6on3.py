import pulp
import numpy as np

nPT=6
nComb=20
pokemonName=["a","b","c","d","e","f"]

#利得行列
#横列を自分、縦列を相手とみて
#自分有利な時は1を、相手有利な時は-1を入力して6×6行列を作る
A=np.array([
 [ 0, -1,  1,  1, -1,  1],  #a
 [ 0,  0, -1,  1,  0,  1],  #b
 [ 1,  0,  0,  0,  0, -1],  #c
 [-1, -1,  0, -1,  0,  0],  #d
 [ 0,  0,  0,  0,  1,  0],  #e
 [ 0,  1,  1,  0,  1, -1] ])#f
U=np.array([
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

#線形計画法
def selection(A):
  lp = pulp.LpProblem(sense=pulp.LpMaximize)
  v = pulp.LpVariable("v") 
  x = [ pulp.LpVariable("x_"+str(i)) for i in range(nPT) ]
  for i in range(nPT):
    for j in range(i+1,nPT):
      for k in range(j+1,nPT):
        lp += v <= pulp.lpDot(A[:,i], x)+pulp.lpDot(A[:,j], x)+pulp.lpDot(A[:,k], x)
  for i in range(nPT):
    lp += x[i] >= 0
    lp += x[i] <= 1
  lp += pulp.lpSum(x) == 3
  lp += v
  lp.solve(pulp.PULP_CBC_CMD(msg=False))
  x = np.array([ x[i].value() for i in range(nPT) ])
  
  print("選出率")
  for i in range(nPT):
      print(pokemonName[i]+"の選出率: ",100*x[i],"%")
  print("有利ポケモンの数-不利ポケモンの数: ",v.value())
  return x,v.value()

#３匹の組み合わせで計算
def selectionTrio(A):
  B=U.dot(A.dot(U.T))
  lp = pulp.LpProblem(sense=pulp.LpMaximize)
  v = pulp.LpVariable("v") 
  x = [ pulp.LpVariable("x_"+str(i)) for i in range(nComb) ]
  
  for i in range(nComb):
    lp += v <= pulp.lpDot(B[:,i], x)
  for i in range(nComb):
    lp += x[i] >= 0
    lp += x[i] <= 1
  lp += pulp.lpSum(x) == 1
  lp += v
  lp.solve(pulp.PULP_CBC_CMD(msg=False))
  x = np.array([ x[i].value() for i in range(nComb) ])

  print("3匹の組で作った利得行列により求めた選出率")
  print(" a b c d e f")
  for i in range(nComb):
    print(U[i],int(x[i]*100),"%")
  print("有利ポケモンの数-不利ポケモンの数: ",v.value())
  return x,v.value()

x,v=selection(A)
#↓3匹の組み合わせで確率を書く場合用 コメント外して使う
#x,v=selectionTrio(A)

