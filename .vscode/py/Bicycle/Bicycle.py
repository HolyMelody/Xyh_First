import numpy as np
from sklearn.cluster import KMeans
import random
import matplotlib.pyplot as plt

# 生成拟数据
def generate_data(num_points):
    data = []
    for _ in range(num_points):
        x = random.uniform(0, 1000)  # 在0到1000之间生成一个随机数作为x坐标
        y = random.uniform(0, 1000)  # 在0到1000之间生成一个随数作为y坐标
        data.append((x, y))  # 将坐标作为一个元组添加到数据列表中
    return np.array(data)  # 将数据列表转换为NumPy数组并返回

# 预测车辆需求者的概率分布
def predict_demand_distribution(data, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters)  # 创建KMeans聚类器，将聚类数量设置为num_clusters
    kmeans.fit(data)  # 对数据进行聚类
    return kmeans.cluster_centers_  # 返回聚类中心

# 贪心算法解决set cover问题
def greedy_set_cover(demand_centers, bike_centers, radius):
    covered_demand = set()  # 已覆盖的需求心集合
    selected_bike_centers = []  # 已选择的共享单车投放位置列表

    while len(covered_demand) < len(demand_centers):  # 当还有未覆盖的需求中心时
        max_covered = 0  # 最大覆盖数量
        best_center = None  # 最佳共享单车投放位置
        best_covered = None  # 最佳覆盖的需求中心集合

        for bike_center in bike_centers:  # 遍历所有共享单车投放位置
            covered = set()  # 覆盖的需求中心集合
            for i, demand_center in enumerate(demand_centers):  # 遍历所有需求中心
                if np.linalg.norm(bike_center - demand_center) <= radius:  # 如果共享单车投放位置可以覆盖需求中心
                    covered.add(i)  # 将需求中心添加到覆盖集合中
            if len(covered - covered_demand) > max_covered:  # 如果覆盖的需求心数量大于当前最大值
                max_covered = len(covered - covered_demand)  # 更新最大覆盖数量
                best_center = bike_center  # 更新最佳共享单车投放位置
                best_covered = covered  # 更新最佳覆盖的需求中心集合

        selected_bike_centers.append(best_center)  # 将最佳共享单车投放位置添加到已选择列表中
        covered_demand |= best_covered  # 将最佳覆盖的需求中心集合添加到已覆盖集合中
        bike_centers.remove(best_center)  # 从共享单车投放位置列表中移除最佳位置
        print("Selected bike center:", best_center)  # 输出已选择的共享单车投放位置

    return selected_bike_centers  # 返回已选择的共享单车投放位置列表

# 可视化
def plot_data(demand_centers, bike_centers, radius):
    plt.scatter(demand_centers[:, 0], demand_centers[:, 1], c='r', marker='o')  # 绘制求中心散点图
    plt.scatter(bike_centers[:, 0], bike_centers[:, 1], c='b', marker='x')  # 绘制共享单车投放位置散点图
    for demand_center in demand_centers:  # 遍历所有需求中心
        circle = plt.Circle(demand_center, radius, color='r', fill=False)  # 创建需求中心的圆形
        plt.gcf().gca().add_artist(circle)  # 将圆形添加到图形中
    plt.show()  # 显示图形

# 主函数
def main(num_points, num_clusters, radius):
    data = generate_data(num_points)  # 生成拟数据
    demand_centers = predict_demand_distribution(data, num_clusters)  # 预测需求中心
    bike_centers = list(demand_centers)  # 假设共享单车的初始投放位置与需求中心相同

    optimal_bike_centers = greedy_set_cover(demand_centers, bike_centers, radius)  # 使用贪心算法选择最优共享单车投放位置
    print("Optimal bike centers:", optimal_bike_centers)  # 输出最优共享单车投放位置

    plot_data(demand_centers, np.array(optimal_bike_centers), radius)  # 可视化结果

if __name__ == "__main__":
    num_points = 1000  # 数据点数量
    num_clusters = 200  # 需求中心数量
    radius = 20 # 共享单车的覆盖范围

    main(num_points, num_clusters, radius)  # 调用主函数
