import pulp
import numpy as np

nPT=6

#利得行列
#横列を自分、縦列を相手とみて
#自分有利な時は1を、相手有利な時は-1を入力して6×6行列を作る
A=np.array([
 [ 0,  1,  0, -1,  1,  1],
 [ 0,  0,  0,  1,  0,  1],
 [ 1, 0,  -1,  0,  0,  0],
 [-1, -1,  0, -1,  0,  0],
 [ 0,  0,  0,  0,  1,  0],
 [ 1,  1,  0,  0,  1, -1] ])

#線形計画法
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

print("最適な選出率")
for i in range(nPT):
    print(str(i)+"の選出率: ",x[i])
print("有利ポケモンの数-不利ポケモンの数: ",v.value())
