from time import time
from BucketSet import BucketSet

from copy import deepcopy
from time import time
class BucketSet(object):
   """
   循环桶类
   """
   __header_location = 0  # 桶头位置
   __thing_amount = 0     # 所有桶中节点数量
   def __init__(self, bucket_num):
       self.__bucket_num = bucket_num     # 桶数量
       self.__buckets = [None]*bucket_num  # 建桶
       self.__init_buckets(bucket_num)     # 初始化桶
       self.__header = self.__buckets[0]   # 桶头是第一个桶

   def __move_header_to_next(self):
       """
       头节点下移一个位置
       :return: None
       """
       self.__header_location = (self.__header_location+1) % self.__bucket_num
       self.__header = self.__buckets[self.__header_location]

   def __init_buckets(self, bucket_num):
       """
       初始化桶
       :param bucket_num: 桶数量
       :return: None
       """
       for i in range(bucket_num):
           self.__buckets[i] = BucketSet.__Bucket(i)

   def __hash(self, length):
       """
       根据距离标记计算哈希值，决定放入的桶
       :param length: 距离标记
       :return: 返回桶编号
       """
       return length % self.__bucket_num

   def add_thing(self, thing):
       """
       节点添加到桶中
       :param thing:
       :return:
       """
       length = thing[0]   # 距离标记
       bucket_id = self.__hash(length)  # 计算桶编号
       self.__buckets[bucket_id].add_thing(thing)  # 放入桶中
       self.__thing_amount += 1   # 更新节点数量

   def is_empty(self):
       """
       判断循环桶是否空
       :return: Boolean  所有桶空返回TRUE,否者FALSE
       """
       return self.__thing_amount == 0

   def pop_min(self):
       """
       取最小距离标记的的节点
       :return: 返回距离标记最小的桶的集合
       """
       while self.__header.is_empty():  # 该桶空就往后查询
           self.__move_header_to_next()
       min_things = self.__header.pop()  # 取桶中所有节点
       self.__thing_amount = self.__thing_amount - len(min_things)  # 更新循环桶中节点数量
       self.__move_header_to_next()     # 头桶往后移动
       return min_things.copy()



#    class __Bucket(object):
#        """
#        桶类
#        """
#        __thing_amount = 0  # 桶中的节点
#        def __init__(self, bucket_id):
#            """
#            初始化
#            :param bucket_id: 桶id
#            """
#            self.list_thing = list()  # 节点容器list
#            self.id = bucket_id

#        def add_thing(self, thing):
#            """
#            往桶里放节点
#            :param thing:
#            :return:
#            """
#            self.list_thing.append(thing)
#            self.__thing_amount += 1  # 更新节点数量

#        def pop(self):
#            """
#            取出桶内节点
#            :return: 返回节点集合
#            """
#            things = self.list_thing.copy()
#            self.list_thing.clear()
#            self.__thing_amount = 0  # 桶内节点数量更新为0
#            return things

#        def is_empty(self):
#            """
#            判断桶是否为空
#            :return: 桶空返回true,否则返回FALSE
#            """
#            return self.__thing_amount == 0


def bucket_dijkstra(graph, s, max_edge_weight):
    """
    桶实现的迪杰斯特拉算法
    :param graph: 图
    :param s: 源节点
    :param max_edge_weight: 最大边权
    :return: 距离字典
    """
    buckets = BucketSet(max_edge_weight+1)  # 创建循环桶对象
    node_s = (0, str(s))            # 源节点二元组（距离标记，节点）
    visited = {}                    # 永久标记集合key是标记节点，所有value是1
    buckets.add_thing(node_s)       # 添加源节点到桶
    path_length = {}                # 路径长度字典
    while not buckets.is_empty():   # 所有的桶未空
        min_list = buckets.pop_min()  # 取最小距离标记集合 返回列表
        while not len(min_list) == 0:
            min_node = min_list.pop()
            if visited.get(min_node[1]) is None:  # 该节点没有永久标记
                visited[min_node[1]] = 1          # 永久标记该节点
                path_length[min_node[1]] = min_node[0]  # 记下路径长度
                node_neighbor_edges = graph.get_node_edges(min_node[1])  # 将所有邻接节点加入桶中
                for e in node_neighbor_edges:
                    buckets.add_thing((e[0]+min_node[0], e[2]))
    return path_length   # 返回各点距离字典


I=-1
Matrix =    [[0, 1, 5, I, I, I],
            [1, 0, 9, 3, I, I],
            [5, 9, 0, 4, 5, I],
            [I, 3, 4, 0, 4, 5],
            [I, I, 5, 4, 0, 4],
            [I, I, I, 5, 4, 0]]
