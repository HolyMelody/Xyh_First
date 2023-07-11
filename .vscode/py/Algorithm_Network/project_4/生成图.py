from cyaron import *
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import os
def draw_graph(graph,weight,n):
    G=nx.Graph()
    # add nodes
    for node in n:
        G.add_node(node)
    # add edges
    G.add_edges_from(graph,color='b')
    #G.add_edges_from(new)
    # draw graph
    pos=nx.spring_layout(G)
    nx.draw_networkx_nodes(G,pos,node_size=700)
    nx.draw_networkx_labels(G,pos,font_size=20)
    nx.draw_networkx_edge_labels(G,pos,font_size=20)
    # show graph
    plt.show()

n=150#节点数
m=100#边数
#graph = Graph.DAG(n, m,weight_limit=(1, 20))
tree = Graph.tree(n,weight_limit=(1, 20))
with open('C:/Users/吴佳红/Desktop/test_4.txt','a') as file0:
    print(tree,file=file0)
#graph = Graph.graph(n, m, directed=True, weight_limit=(1, 20))
# print(type(graph))
# print(graph)