import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pylab

def draw_graph(edges,n,weight):
    #自定义网络

    print('生成一个空的有向图')
    G=nx.DiGraph() # 实例化有向图
    print('为这个网络添加节点...')
    for i in range(0,n):
        G.add_node(i)  #一个一个的添加结点
    print('在网络中添加带权中的边...')
    for i in range(len(edges)):
        G.add_weighted_edges_from(edges) # 格式（结点1，结点2，权重）

    print('给网路设置布局...')
    pos=nx.spring_layout(G,scale=2)
    print('画出网络图像：')
    labels = nx.get_edge_attributes(G,'weight') 
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels, font_color='c')
    nx.draw(G,pos,with_labels=True, node_color='g', edge_color='red', node_size=100, alpha=0.5 )
    pylab.title('Self_Define Net',fontsize=15)
    pylab.show()

graphs=[
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
weight={}
edges=[]
for graph in graphs:
    i=graph[0]+1
    j=graph[1]+1
    w=graph[2]
    weight[(i,j)]=w
    edges.append((i,j,w))
print(weight)
print(graphs)
print(edges)
draw_graph(edges,9,weight)
