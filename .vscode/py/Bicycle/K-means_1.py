import random
import math

# 计算两个点之间的欧几里得距离
def distance(p1, p2):
    return math.sqrt(sum([(p1[i] - p2[i]) ** 2 for i in range(len(p1))]))

# 初始化簇中心
def init_centers(data, k):
    centers = []
    for i in range(k):
        center = random.choice(data)
        while center in centers:
            center = random.choice(data)
        centers.append(center)
    return centers

# 对数据进行聚类
def kmeans(data, k, max_iter=100):
    centers = init_centers(data, k)
    for i in range(max_iter):
        # 初始化簇
        clusters = [[] for _ in range(k)]
        # 将每个数据点分配到距离最近的簇中心所在的簇中
        for point in data:
            distances = [distance(point, center) for center in centers]
            cluster_index = distances.index(min(distances))
            clusters[cluster_index].append(point)
        # 计算每个簇的中心
        new_centers = []
        for cluster in clusters:
            if len(cluster) > 0:
                new_center = [sum([point[i] for point in cluster]) / len(cluster) for i in range(len(cluster[0]))]
                new_centers.append(new_center)
            else:
                new_centers.append(random.choice(data))
        # 如果簇中心不再发生变化，则停止迭代
        if new_centers == centers:
            break
        centers = new_centers
    return clusters, centers

# 测试代码
data = [[1, 2], [2, 1], [2, 3], [4, 5], [5, 4], [5, 6], [7, 8], [8, 7], [8, 9]]
clusters, centers = kmeans(data, 3)
print(clusters)
print(centers)
