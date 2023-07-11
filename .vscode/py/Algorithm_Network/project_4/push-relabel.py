#push-relabel algorithm
import numpy as np
import time
start=time.perf_counter()


def MaxFlow(C, s, t):
     n = len(C) # C is the capacity matrix
     F = [[0] * n for i in range(n)]

     # the residual capacity from u to v is C[u][v] - F[u][v]
     height = [0] * n # height of node
     excess = [0] * n # flow into node minus flow from node
     seen   = [0] * n # neighbours seen since last relabel
     # node "queue"
     nodelist = [i for i in range(n) if i != s and i != t]

     #push operation
     def push(u, v):
         send = min(excess[u], C[u][v] - F[u][v])
         F[u][v] += send
         F[v][u] -= send
         excess[u] -= send
         excess[v] += send

     #relabel operation
     def relabel(u):
         # find smallest new height making a push possible,
         # if such a push is possible at all
         min_height = float('inf')
         for v in range(n):
             if C[u][v] - F[u][v] > 0:
                 min_height = min(min_height, height[v])
                 height[u] = min_height + 1
 
     def discharge(u):
         while excess[u] > 0:
             if seen[u] < n: # check next neighbour
                 v = seen[u]
                 if C[u][v] - F[u][v] > 0 and height[u] > height[v]:
                     push(u, v)
                 else:
                     seen[u] += 1
             else: # we have checked all neighbours. must relabel
                 relabel(u)
                 seen[u] = 0
 
     height[s] = n   # longest path from source to sink is less than n long
     excess[s] = float("inf") # send as much flow as possible to neighbours of source
     for v in range(n):
         push(s, v)
 
     p = 0
     while p < len(nodelist):
         u = nodelist[p]
         old_height = height[u]
         discharge(u)
         if height[u] > old_height:
             nodelist.insert(0, nodelist.pop(p)) # move to front of list
             p = 0 # start from front of list
         else:
             p += 1
     return sum(F[s])

# make a capacity graph
# node   s   o   p   q   r   t
line_num=100
list1=[]
i=0
with open('C:/Users/吴佳红/Desktop/test_3.txt','r') as f:
    line =f.readline()
    while line:
        line1=list(map(int,line.split()))
        list1.append(line1)
        line=f.readline()

        # for i in line_num:
        #     list1[i][0],list1[i][1],list1[i][2]=line 


	# inp=str(input())
	# inp=list(map(int,inp.split()))
n=50
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

source = 0  # A
sink = 2   # F
max_flow_value = MaxFlow(Matrix, source, sink)
print ("Push-Relabeled(Preflow-push) algorithm")
print ("max_flow_value is: ", max_flow_value)




end=time.perf_counter()
runTime=end-start
runTime_ms=runTime*1000
print("time:",runTime,"s")
print("time:",runTime_ms,"ms")