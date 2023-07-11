import copy

# 首先给出邻接矩阵,两个节点之间距离无穷大用-1表示
matrix = [[0, 2, 5, 1, -1, -1],
          [2, 0, 3, 2, -1, -1],
          [5, 3, 0, 3, 1, 5],
          [1, 2, 3, 0, 1, -1],
          [-1, -1, 1, 1, 0, 2],
          [-1, -1, 5, -1, 2, 0]]


def dijkstra(adjacent_matrix):
    # 获取节点数
    node_number = len(adjacent_matrix)

    # 置定节点集
    G_p = []

    # 未置定节点集
    g_p = []

    # 全部的节点集,用数字表示节点
    G = []

    for i in range(node_number):
        G.append(i + 1)
        g_p.append(i + 1)

    # 用一个一维数组表示v_s节点到其他结点的距离,初始时,这个距离就是邻接矩阵的第s行
    s = 1
    distance = copy.deepcopy(adjacent_matrix[s - 1])
    # 记录路径和径长
    path = []
    w = copy.deepcopy(adjacent_matrix[s - 1])
    # 由于从v_s结点开始,路径的起点都是v_s
    for i in range(node_number):
        path.append([s])

    # 开始迭代
    for i in range(node_number):
        # 遍历整个列表,找最小值,初始时假定最小值为最大值
        min_value = max(distance)
        min_index = distance.index(min_value)
        for j in range(len(distance)):#访问所有邻居
            if 0 <= distance[j] < min_value:
                min_value = distance[j]
                min_index = j
        # 找到索引为min_index的节点是到v_s距离最短的,把他加入G_p中,并从g_p中移除,同时记录下最短距离
        G_p.append(min_index + 1)
        g_p.remove(min_index + 1)
        w[min_index] = min_value
        # -2表示这个点已经被选过了
        distance[min_index] = -2

        # 更新G_p后,需要对distance进行更新
        # 对distance中的每一个数据,当添入新节点后是否有变化
        # 只需考虑g_p中的节点即可
        for j in g_p:
            # 如果索引为min_index的节点可以到达v_j,并且从v_s到min_value再到v_j的距离比原来从v_s到v_j的距离要小
            # 或者原来v_s无法到达v_j
            if adjacent_matrix[min_index][j-1] > 0 and (
                    adjacent_matrix[min_index][j-1] + min_value < distance[j-1]
                    or distance[j-1] == -1):
                distance[j-1] = adjacent_matrix[min_index][j-1] + min_value
                for item in path[min_index]:
                    path[j-1].append(item)
                path[j-1] = list(set(path[j-1]))
                path[j-1].append(min_index+1)

        print("第%d次迭代:" % i, distance, path, w)


dijkstra(matrix)

