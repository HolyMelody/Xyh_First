class Topo(object):
    def __init__(self, logger):

        self.adjacent = defaultdict(lambda s1,s2: None)
        # datapathes
        self.switches = None

        self.host_mac_to={}
        self.logger=logger
        self.parent = [i for i in range(0, 500)]
    def reset(self):
        self.adjacent=defaultdict(lambda s1s2:None)
        self.switches=None
        self.host_mac_to=None
    
    def get_adjacent(self,s1,s2):
        return self.adjacent.get((s1,s2))
    
    def set_adjacent(self,s1,s2,port,weight):
        self.adjacent[(s1,s2)]=(port,weight)
    
    def get_graph(self):
        Matrix = np.array(np.ones((20,20))*999999)

     def get_graph(self):
    Matrix = np.array(np.ones((20, 20)) * 999999)
    for (a, b) in self.adjacent.keys():
        Matrix[a - 1][b - 1] = random.randint(1, 10)
        Matrix[b - 1][a - 1] = Matrix[a - 1][b - 1]
    return Matrix



def find(x):
    if x != self.parent[x]:
        self.parent[x] = find(self.parent[x])
    return self.parent[x]


def join(x, y):
    x_root = find(x)
    y_root = find(y)
    if x_root != y_root:
        self.parent[x_root] = y_root


def findnode(self, Matrix):
    x=len(Matrix)
    return x


def findedge(self, Matrix):
    num = 0
    for x in range(len(Matrix)):
        for y in range(x):
            if Matrix[x][y] > 0 and Matrix[x][y] < 999999:
                num = num + 1
    return num


def kruskal(self, Matrix):
    edge = []
    a = self.findnode(Matrix)
    b = self.findedge(Matrix)
    if a<=0 or a>b+1:
        return
    for x in range(a):
        for y in range(x):
            if Matrix[x][y] < 999999:
                edge.append((x, y, Matrix[x][y]))
    edge.sort(key=lambda i: i[2])
    tree = []
    for c in edge:
        if find(c[0]) != find(c[1]):
            join(c[0], c[1])
            tree.append(c)
    return tree

    def comput_tree(self,src,list):
        list1 = list
        links = [[] for i in range(len(list) + 1)]
        for i in range(len(list) + 1):
            for edge in list1:
                pass
                if i == edge[0]:
                    links[i].append(edge[1])
                elif i == edge[1]:
                    links[i].append(edge[0])
        return links

    def compute_links(self,src,pre_src,links):
        result = []
        if len(links[src]) < 1:
            return result

        for node in links[src]:
            if node != pre_src:
                result.append((pre_src,src,node))
                newresult = self.compute_links(node,src,links)
                result.extend(newresult)

        return result

    #收到包之后调用该函数，计算流表的转发，流表匹配源ip，向生成树上其他端口转发
    def compute_flowTables(self,src_dw,first_port):
        Matrix = self.get_graph()
        linkList1 = self.kruskal(Matrix)
        tree = self.comput_tree(src_dw-1,linkList1)
        links = self.compute_links(src_dw-1,None,tree)
        print('src:',src_dw)
        print('linkList:',linkList1)

         #draw
        G=nx.Graph()  
 
        weight={}
        graph=[]
        for i in range(len(Matrix)):
            for j in range(i):
                if Matrix[i][j] > 0 and Matrix[i][j] < 999999:
                    graph.append((i+1,j+1))
                    graph.append((j+1,i+1))
                    weight[(i+1,j+1)]=Matrix[i][j]
                    weight[(j+1,i+1)]=Matrix[i][j]
        
        path=[]
        for link1 in linkList1:
            path.append((link1[0]+1,link1[1]+1))
            path.append((link1[1]+1,link1[0]+1))

        for gra in graph:
            G.add_edge(gra[0],gra[1],color='black')
        
        for pat in path:
            G.add_edge(pat[0],pat[1],color='r')

        #elargse=[(u,v) for (u,v,d) in G.edges(data=True)]
        pos=nx.spring_layout(G)
        edges = G.edges()
        colors = [G[u][v]['color'] for u,v in edges]
        nx.draw_networkx_nodes(G,pos,node_size=700)
        nx.draw_networkx_edges(G,pos,width=3,edge_color=colors)
        nx.draw_networkx_labels(G,pos,font_size=20)


        
        nx.draw_networkx_edge_labels(G,pos,weight,font_size=20)


        plt.show()
        #draw end

        temp1 = {}
        for link in links:
            if(link[0],link[1]) not in temp1.keys():
                temp1[(link[0],link[1])] = [link[2]]
            else:
                temp1[(link[0],link[1])].append(link[2])

        #print('temp1:',temp1)

        newresult = []
        index = [key[1] for key in temp1.keys()]
        #print(index)
        for i in range(20):
            if i not in index:
                for key in temp1.keys():
                    if i in temp1[key]:
                        newresult.append((key[1],i,None))
            else:
                for key in temp1.keys():
                    if i == key[1]:
                        newresult.append((key[0],key[1],temp1[key]))
        #print('newresult:',newresult)

        result = []

        for item in newresult:
            if item[0] is not None:
                if item[2] is None:
                    inport,_ = self.get_adjacent(item[1]+1,item[0]+1)
                    outportList = [1]
                    result.append((item[1]+1,inport,outportList))
                else:
                    inport,_ = self.get_adjacent(item[1]+1,item[0]+1)
                    outportList = [1]
                    for node in item[2]:
                        op,_ = self.get_adjacent(item[1]+1,node+1)
                        outportList.append(op)
                    result.append((item[1]+1,inport,outportList))
            else:
                inport = first_port
                outportList = [1]
                for node in item[2]:
                    op,_ = self.get_adjacent(item[1]+1,node+1)
                    outportList.append(op)
                result.append((item[1]+1,inport,outportList))

        #print('result:',result)
        return result
        #result: [(s1,inport,outportList),...(sn,inport,outportList)]

    def show(self):
        print("switches: ",self.switches)

    def test(self):
        result = self.compute_flowTables(4,-1)
        print("result: ",result)

# TODO Port status monitor
   