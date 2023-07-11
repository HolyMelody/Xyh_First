from collections import defaultdict
import networkx as nx
import matplotlib.pyplot as plt
def draw_graph(graph,path,weight):
    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])
    # create networkx graph
    G=nx.Graph()
    # add nodes
    for node in nodes:
        G.add_node(node)
    # add edges
    G.add_edges_from(graph,color='b')
    G.add_edges_from(path,color='r')
    #G.add_edges_from(new)
    # draw graph
    pos=nx.spring_layout(G)
    edges = G.edges()
    colors = [G[u][v]['color'] for u,v in edges]
    nx.draw_networkx_nodes(G,pos,node_size=700)
    nx.draw_networkx_edges(G,pos,width=3,edge_color=colors)
    nx.draw_networkx_labels(G,pos,font_size=20)
    nx.draw_networkx_edge_labels(G,pos,weight,font_size=20)
    # show graph
    plt.show()



class bucket(object):
    """循环桶"""
    def __init__(self,ration):
        self.ration=int(ration)#桶的容量
        # print(self.ration)
        self.data=[[] for i in range(0,int(ration))]
        self.front=0#桶前指针
 
    def insert(self,newdata):
        index=(newdata[0])%self.ration
        self.data[index].append(newdata)
 
    def Exact_min(self): #取出离桶前指针最近的桶中第一个元素
       while not self.data[(self.front)%self.ration]:
                  self.front=self.front+1
       key=self.data[self.front % self.ration].pop(0)
       print(self.data)
       #[[(6, 0, 2)], [(7, 3, 2), (7, 3, 4)], [(8, 3, 5)], [], [(4, 1, 2)], []]
       #self.data[self.front % self.ration].pop(0)
       if(len(self.data[self.front % self.ration])==0):
            self.front=(self.front+1)%self.ration
       return key
#nodes[]
def dijkstra(edges,src_sw,dst_sw,bucket1):
    path={}#存储每个点离源点的最短路径
    path[src_sw]=0
    path_list = defaultdict(list)  # 存储每个点的路径
    visited=[]#已经永久标记过的点
    visited.append(src_sw)
    path_list[src_sw].append(src_sw)

    for i in edges[src_sw]:#取出与源节点相连接的所有邻居，加入桶
        edge_c,src_sw,node_next=i
        bucket1.insert((edge_c,src_sw,node_next))


    #开始
    flag=1
    while len(visited)!=13 and flag==1:   #len(nodes):遍历所有节点
        min_current_distance,front_node,node=bucket1.Exact_min()
        if node not in visited:
            for i in path_list[front_node]:#把它前面结点的路径加入新节点的路径中
                path_list[node].append(i)
            path_list[node].append(node)
            path[node]=min_current_distance
            if node==dst_sw:
               flag=0
            visited.append(node)
        
        #遍历当前节点的邻居
            for neighbor in edges[node]:
                if neighbor[2] not in visited:
                    edge,node_a,node_b=neighbor
                    current_distance=edge+path[node_a]
                    bucket1.insert((current_distance,node_a,node_b))
        


        
    return path[dst_sw],path_list[dst_sw] #返回各点最短权重和路径
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
I=99999    #  1  2  3  4  5  6 7 8 9 10 11 12 13
Matrix =    [[I, 4, I, I, I, I,I,I,I, I, I, I,I],
             [4, I, 5, 1, 2, I,I,I,I, I, I, I,I],
             [I, 5, I, 4, I, I,I,I,I, 2, I, I,2],
             [I, 1, 4, I, I, I,I,I,I, I, I, I,I],
             [I, 2, I, I, I, 4,2,2,2, I, I, I,I],
             [I, I, I, I, 4, I,I,I,I, I, I, I,I],
             [I, I, I, I, 2, I,I,I,I, I, I, I,I],
             [I, I, I, I, 2, I,I,I,2, I, I, I,I],
             [I, I, I, I, 2, I,I,2,I, 2, 2, I,I],
             [I, I, 2, I, I, I,I,I,2, 2, 2, I,2],
             [I, I, I, I, I, I,I,I,2, 2, I, 2,I],
             [I, I, I, I, I, I,I,I,I, I, 2, I,2],
             [I, I, 2, I, I, I,I,I,I, 2, I, 2,I]]


edges=defaultdict(list)
for i in range(len(Matrix)):
   for j in range(len(Matrix[0])):
        if(Matrix[i][j]!=I and i!=j):
            edges[i+1].append([Matrix[i][j],i+1,j+1])
            
print(edges)
bucket1=bucket(5+1)
ans,ans_list=dijkstra(edges,1,4,bucket1)
print("权重和：")
print(ans)
print("路径：")
print(ans_list)
#print(edges)
# defaultdict(<class 'list'>, {0: [(1, 0, 1), (5, 0, 2)], 
# 1: [(1, 1, 0), (9, 1, 2), (3, 1, 3)], 
# 2: [(5, 2, 0), (9, 2, 1), (4, 2, 3), (5, 2, 4)], 
# 3: [(3, 3, 1), (4, 3, 2), (4, 3, 4), (5, 3, 5)], 
# 4: [(5, 4, 2), (4, 4, 3), (4, 4, 5)], 
# 5: [(5, 5, 3), (4, 5, 4)]})


# 1: [(1, 1, 0), (9, 1, 2), (3, 1, 3)], 
# 2: [(5, 2, 0), (9, 2, 1), (4, 2, 3), (5, 2, 4)], 
# 3: [(3, 3, 1), (4, 3, 2), (4, 3, 4), (5, 3, 5)], 
# 4: [(5, 4, 2), (4, 4, 3), (4, 4, 5)], 
# 5: [(5, 5, 3), (4, 5, 4)]})

