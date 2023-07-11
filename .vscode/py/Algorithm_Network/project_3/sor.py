from collections import defaultdict
 
class bucket(object):
    """循环桶"""
    def __init__(self,ration):
        self.ration=int(ration)#桶的容量
        # print(self.ration)
        self.data=[[] for i in range(0,int(ration))]
        self.front=1#桶前指针
 
    def insert(self,newdata):
        index=(newdata[0])%self.ration
        self.data[index].append(newdata)
 
    def Exact_min(self): #取出离桶前指针最近的桶中第一个元素
       while not self.data[(self.front)%self.ration]:
                  self.front=self.front+1
       key=self.data.pop(self.front % self.ration)
       self.front=self.front+1
       print(key)
       return key
 
nodes=[]
edges=defaultdict(list)
edge_size=[]
 
 
def get_graph(Matrix):#读取文件数据
    edge_num = 0
    Max_edge=-1
    for i in range(len(Matrix)):
        for j in range(i):
            if Matrix[i][j]!=-1:
                edge_num +=1
                Max_edge=max(Max_edge,Matrix[i][j])
    
    node_num=len(Matrix)
    return edge_num,node_num,Max_edge
 
 
def find_edge_max(edge_size):#找出最大边
    return max(edge_size)
 
 #edges[node_a].append((int(edge_c),node_a,node_b))
def dijkstra(edges,src_sw,bucket1):
    path={}#存储每个点离源点的最短路径
    path[src_sw]=0
    path_list = defaultdict(list)  # 存储每个点的路径
    visited=[]#已经永久标记过的点
    visited.append(src_sw)
    path_list[src_sw].append(src_sw)
    print(path_list)
    for i in edges[src_sw]:
        #print("1")
        edge_c,src_sw,node_next=i
        bucket1.insert((edge_c,src_sw,node_next))
    while len(visited)!=6:   #len(nodes):
        #print("2")
        min_current_distance,front_node,node=bucket1.Exact_min()
        for i in path_list[front_node]:#把它前面结点的路径加入新节点的路径中
            # print("i")
            # print(i)
            # print(path_list)
            path_list[node].append(i)
        path_list[node].append(node)
        if node not in visited:
         path[node]=min_current_distance
         visited.append(node)
         for neighbor in edges[node]:
            #print("4")
            if neighbor[2] not in visited:
                edge,node_a,node_b=neighbor
                current_distance=edge+path[node_a]
                bucket1.insert((current_distance,node_a,node_b))
    return path,path_list #返回各点最短权重和路径
 
I=-1
Matrix =    [[0, 1, 5, I, I, I],
            [1, 0, 9, 3, I, I],
            [5, 9, 0, 4, 5, I],
            [I, 3, 4, 0, 4, 5],
            [I, I, 5, 4, 0, 4],
            [I, I, I, 5, 4, 0]]




edges=defaultdict(list)
for i in range(len(Matrix)):
   for j in range(len(Matrix[0])):
     if(Matrix[i][j]!=I):
        edges[i].append((Matrix[i][j],i,j))

#a,b,c=get_graph(Matrix)
bucket1=bucket(5+1)
ans,ans_list=dijkstra(edges,1,bucket1)
print("权重和：")
print(ans[5])
print("路径：")
print(ans_list[5])
 



# {1: [3, 17, 2, 3, 17, 2], 
# 3: [1, 1, 5, 8, 5, 8, 11], 
# 17: [1, 1], 
# 2: [1, 20, 19, 1, 20, 19],
#  4: [6, 8, 8, 6], 
# 6: [4, 4], 
# 7: [8, 8], 
# 8: [7, 4, 7, 3, 3, 4], 
# 12: [14, 13, 15, 14, 13, 15], 
# 14: [12, 5, 5, 12], 
# 5: [14, 3, 14, 3],
#  13: [16, 12, 12, 16], 
# 16: [13, 18, 13, 18], 
# 15: [12, 12], 
# 20: [2, 2],
#  19: [2, 2], 10: [11], 
# 11: [10, 3, 9], 
# 18: [16, 16], 
# 9: [11]}
