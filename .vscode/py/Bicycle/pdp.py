import numpy as np
from sklearn.cluster import KMeans
import random
import matplotlib.pyplot as plt

# 生成模拟数据
def generate_data(num_points):
    data = []
    for _ in range(num_points):
        x = random.uniform(0, 1000)
        y = random.uniform(0, 1000)
        data.append((x, y))
    return np.array(data)

# 预测车辆需求者的概率分布
def predict_demand_distribution(data, num_clusters):
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(data)
    return kmeans.cluster_centers_

# 贪心算法解决set cover问题
def greedy_set_cover(demand_centers, bike_centers, radius):
    covered_demand = set()
    selected_bike_centers = []

    while len(covered_demand) < len(demand_centers):
        max_covered = 0
        best_center = None
        best_covered = None

        for bike_center in bike_centers:
            covered = set()
            for i, demand_center in enumerate(demand_centers):
                if np.linalg.norm(bike_center - demand_center) <= radius:
                    covered.add(i)
            if len(covered - covered_demand) > max_covered:
                max_covered = len(covered - covered_demand)
                best_center = bike_center
                best_covered = covered

        selected_bike_centers.append(best_center)
        covered_demand |= best_covered
        bike_centers.remove(best_center)

    return selected_bike_centers

# 可视化
def plot_data(demand_centers, bike_centers, radius):
    plt.scatter(demand_centers[:, 0], demand_centers[:, 1], c='r', marker='o')
    plt.scatter(bike_centers[:, 0], bike_centers[:, 1], c='b', marker='x')
    for demand_center in demand_centers:
        circle = plt.Circle(demand_center, radius, color='r', fill=False)
        plt.gcf().gca().add_artist(circle)
    plt.show()

# 主函数
#测试数量为1000，聚类数量为100，投放半径为10
def main():
    num_points = 1000
    num_clusters = 100
    radius = 10

    data = generate_data(num_points)
    demand_centers = predict_demand_distribution(data, num_clusters)
    bike_centers = list(demand_centers)  # 假设共享单车的初始投放位置与需求中心相同

    optimal_bike_centers = greedy_set_cover(demand_centers, bike_centers, radius)
    print("Optimal bike centers:", optimal_bike_centers)

    plot_data(demand_centers, np.array(optimal_bike_centers), radius)

if __name__ == "__main__":
    main()
