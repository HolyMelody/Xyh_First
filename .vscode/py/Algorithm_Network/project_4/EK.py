import time
start=time.perf_counter()



MAXN = 10
INF = 2147483646

def bfs(s, t,check) :
	parent = [-1 for i in range(MAXN)]
	path_flow = [0 for i in range(MAXN)]
	q=[s]
	parent[s] = -2
	path_flow[s] = INF
	while(q):
		u = q.pop(0)
		for i in range(len(graph[u])) :	#取出所有邻居
			v = graph[u][i]#邻居
			if(parent[v] == -1):#未访问
				if(capacity[u][v] - flowPassed[u][v] >0):#还有容量
					parent[v] = u
            #path_flow记录着从源节点到该点的最小容量边
					path_flow[v] = min(path_flow[u], capacity[u][v]- flowPassed[u][v])
					if(v == t):
						if(check==True):return path_flow[t]
						else: return parent#check控制返回的目标

					q.append(v)  
	return 0

def max_flow(source,sink):
	maxFlow = 0 
	while(True):
		flow = bfs(source,sink,True)
		parent=bfs(source,sink,False)
		if(flow == 0):#说明不可达
			break
		u = sink
		maxFlow += flow
		while (u!=source):
			v = parent[u]
			flowPassed[v][u] += flow
			flowPassed[u][v] -+ flow
			u=v
	return maxFlow

n=6#最大邻居数
e=9#边数
s=0#源点
t=5#目标
capacity = [[0]*n for i in range(e)]
graph = [[0]*n for i in range(e)]
flowPassed = [[0]*n for i in range(e)]
graph=[
[0,1,10],
[0,2,10],
[1,2,2],
[1,3,4],
[2,4,9],
[1,4,8],
[4,3,6],
[3,5,10],
[4,5,10]
]
for inp in graph:
	From=inp[0]
	to=inp[1]
	cap=inp[2]
	capacity[From][to]=cap#有向图
	graph[From].append(to)#记录邻居
	graph[to].append(From)

#print(graph)
#print(len(graph[0]))
maxFlow = max_flow(s,t)
print(maxFlow)
# 6
# 9
# 0
# 5
# 0 1 10
# 0 2 10 
# 1 2 2
# 1 3 4
# 2 4 9
# 1 4 8
# 4 3 6
# 3 5 10
# 4 5 10



end=time.perf_counter()
runTime=end-start
runTime_ms=runTime*1000
print("time:",runTime,"s")
print("time:",runTime_ms,"ms")