# def find(x, pres):
#     """
#     查找x的最上级（首级）
#     :param x: 要查找的数
#     :param pres: 每个元素的首级
#     :return: 根结点（元素的首领结点）
#     """
#     root, p = x, x  # root:根节点， p:指针

#     # 找根节点
#     while root != pres[root]:
#         root = pres[root]

#     # 路径压缩，把每个经过的结点的上一级设为root（直接设为首级）
#     while p != pres[p]:
#         p, pres[p] = pres[p], root
#     return root


# def join(x, y, pres, ranks):
#     """
#     合并两个元素（合并两个集合）
#     :param x: 第一个元素
#     :param y: 第二个元素
#     :param pres: 每个元素的上一级
#     :param ranks: 每个元素作为根节点时的秩（树的深度）
#     :return: None
#     """
#     h1, h2 = find(x, pres), find(y, pres)
#     # 当两个元素不是同一组的时候才合并
#     # 按秩合并
#     if h1 != h2:
#         if ranks[h1] < ranks[h2]:
#             pres[h1] = h2
#         else:
#             pres[h2] = h1
#             if ranks[h1] == ranks[h2]:
#                 ranks[h1] += 1


# def kruskal(n, edges):
#     """
#     kruskal算法
#     :param n: 结点数
#     :param edges: 带权边集
#     :return: 构成最小生成树的边集
#     """
#     # 初始化：pres一开始设置每个元素的上一级是自己，ranks一开始设置每个元素的秩为0
#     pres, ranks = [e for e in range(n)], [0] * n
#     # 边从大到小排序
#     edges = sorted(edges, key=lambda x: x[-1])
#     mst_edges, num = [], 0
#     for edge in edges:
#         if find(edge[0], pres) != find(edge[1], pres):
#             mst_edges.append(edge)
#             join(edge[0], edge[1], pres, ranks)
#             num += 1
#         else:
#             continue
#         if num == n:
#             break
#     return mst_edges


# 数据 采用mst图
edges = [
    [0, 1, 6],
    [0, 2, 1],
    [0, 3, 5],
    [2, 1, 5],
    [2, 3, 5],
    [2, 4, 5],
    [2, 5, 4],
    [1, 4, 3],
    [4, 5, 6],
    [5, 3, 2]
]

# 结点数
# edges=[
# [0, 2, 1],
# [5, 3, 2].
# [1, 4, 3]
# [2, 5, 4]
# [2, 1, 5]
#]
# n = 6
# mst_edges = kruskal(n, edges)
# print('edges:')
# for e in mst_edges:
#     print(e)
# print('Total cost of MST:', sum([e[-1] for e in mst_edges]))
# print('Maximum cost of MST:', max([e[-1] for e in mst_edges]))


# # std print
#
# edges:
# [0, 2, 1]
# [5, 3, 2]
# [1, 4, 3]
# [2, 5, 4]
# [2, 1, 5]
# Total cost of MST: 15
# Maximum cost of MST: 5
class topo():
    def find(self,x):
        if x != self.parent[x]:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]


    def join(self,x, y):
        x_root = self.find(x)
        y_root = self.find(y)
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
            return []
        for x in range(a):
            for y in range(x):
                if Matrix[x][y] < 999999:
                    edge.append((x, y, Matrix[x][y]))
        edge.sort(key=lambda i: i[2])
        tree = []
        for c in edge:
            if self.find(c[0]) != self.find(c[1]):
                self.join(c[0], c[1])
                tree.append(c)
        return tree


a=[]
s=topo() 
a=s.kruskal(edges)
print(a)