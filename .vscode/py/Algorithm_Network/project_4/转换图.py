import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pylab

def draw_graph(edges,n):
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
    pos=nx.random_layout(G)
    print('画出网络图像：')
    labels = nx.get_edge_attributes(G,'weight') 
    nx.draw_networkx_edge_labels(G,pos,edge_labels=labels, font_color='c')
    nx.draw(G,pos,with_labels=True, node_color='y', edge_color='red', node_size=100, alpha=0.5 )
    pylab.title('Self_Define Net',fontsize=15)
    pylab.show()




list1=[]
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
n=150#节点数
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
    # if(w!=0):
    #     print(Matrix[i][j],i,j)


draw_graph(edges,n)

print(edges)
np.savetxt('C:/Users/吴佳红/Desktop/test__1.txt',Matrix,fmt='%d')
#print(Matrix[0][394])


