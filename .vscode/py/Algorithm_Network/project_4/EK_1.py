import time
import numpy as np

start=time.perf_counter()

def max_flow(C, s, t):
        n = len(C) # C is the capacity matrix
        F = [[0] * n for i in range(n)]
        path = bfs(C, F, s, t)
      #  print path
        while path != None:
            flow = min(C[u][v] - F[u][v] for u,v in path)
            for u,v in path:
                F[u][v] += flow
                F[v][u] -= flow
            path = bfs(C, F, s, t)
        return sum(F[s][i] for i in range(n))

#find path by using BFS
def bfs(C, F, s, t):
        queue = [s]
        paths = {s:[]}
        if s == t:
            return paths[s]
        while queue: 
            u = queue.pop(0)
            for v in range(len(C)):
                    if(C[u][v]-F[u][v]>0) and v not in paths:
                        paths[v] = paths[u]+[(u,v)]
                        #print (paths)
                        if v == t:
                            return paths[v]
                        queue.append(v)
        return None
    
# make a capacity graph
# node   s   o   p   q   r   t
line_num=100
list1=[]
i=0
with open('C:/Users/吴佳红/Desktop/test_4.txt','r') as f:
    line =f.readline()
    while line:
        line1=list(map(int,line.split()))
        list1.append(line1)
        line=f.readline()

        # for i in line_num:
        #     list1[i][0],list1[i][1],list1[i][2]=line 


	# inp=str(input())
	# inp=list(map(int,inp.split()))
n=150
#print(list1)
edges=[]
Matrix = np.array(np.ones((n,n))*0)
for list_1 in list1:
    i=list_1[0]-1
    j=list_1[1]-1
    w=list_1[2]

    edges.append((i,j,w))

    weight={}
    weight[(i,j)]=w
    Matrix[i][j]=w



C = [[ 0, 3, 3, 0, 0, 0 ],  # s
     [ 0, 0, 2, 3, 0, 0 ],  # o
     [ 0, 0, 0, 0, 2, 0 ],  # p
     [ 0, 0, 0, 0, 4, 2 ],  # q
     [ 0, 0, 0, 0, 0, 2 ],  # r
     [ 0, 0, 0, 0, 0, 3 ]]  # t

source = 1# A
sink = 13# F
max_flow_value = max_flow(Matrix, source, sink)
print ("Edmonds-Karp algorithm")
print ("max_flow_value is: ", max_flow_value)



end=time.perf_counter()
runTime=end-start
runTime_ms=runTime*1000
print("time:",runTime,"s")
print("time:",runTime_ms,"ms")