from sklearn.cluster import KMeans
import numpy as np

# 创建一个包含 100 个数据点的二维数组
X = np.random.rand(100, 2)

# 创建一个 KMeans 对象，设置簇的数量为 3
kmeans = KMeans(n_clusters=3)

# 对数据进行聚类
kmeans.fit(X)

# 输出每个数据点所属的簇
print(kmeans.labels_)

# 输出每个簇的中心
print(kmeans.cluster_centers_)
