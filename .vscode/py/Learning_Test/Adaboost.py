
# 导入必要的库
import numpy as np
 # 定义Adaboost类
class Adaboost:
    def __init__(self, n_learners=10):
        self.n_learners = n_learners  # 学习器的数量，默认为10
    def fit(self, X, y):
        m, n = X.shape  # 获取数据集的行数和列数
        self.learners = []  # 用于存储学习器
        self.alphas = []  # 用于存储每个学习器的权重
        w = np.full(m, 1 / m)  # 初始化每个样本的权重
         
        for _ in range(self.n_learners):  # 循环学习器的数量次（默认为10）
            learner = self._build_learner(X, y, w)  # 构建一个学习器
            y_pred = learner.predict(X)  # 对数据集进行预测
            err = w[(y_pred != y)].sum()  # 计算分类错误的样本的权重和
            alpha = 0.5 * np.log((1 - err) / err)  # 计算当前学习器的权重
            w = w * np.exp(-alpha * y * y_pred)  # 更新每个样本的权重
            w = w / w.sum()  # 归一化每个样本的权重
            self.learners.append(learner)  # 将当前学习器添加到学习器列表中
            self.alphas.append(alpha)  # 将当前学习器的权重添加到权重列表中
    def predict(self, X):
        m, _ = X.shape  # 获取数据集的行数和列数
        predictions = np.zeros(m)  # 初始化预测结果为m个零
        for learner, alpha in zip(self.learners, self.alphas):  # 循环每个学习器及其权重
            predictions += alpha * learner.predict(X)  # 根据每个学习器对数据集进行预测，并加权累加
        return np.sign(predictions)  # 返回预测结果的符号（正号或负号）
    def _build_learner(self, X, y, w):
        best_learner = None  # 初始化最佳学习器为空
        best_error = np.inf  # 初始化最小错误率为正无穷
        m, n = X.shape  # 获取数据集的行数和列数
        for feature in range(n):  # 循环数据集的每一列
            for threshold in np.unique(X[:, feature]):  # 循环该列上取值的唯一值
                for direction in [1, -1]:  # 循环方向（大于等于或小于）
                    y_pred = np.ones(m)  # 初始化预测结果为全部为1
                    y_pred[direction * X[:, feature] < direction * threshold] = -1  # 根据方向和阈值，将预测结果修改为1或-1
                    error = w[(y_pred != y)].sum()  # 计算分类错误的样本的权重和
                    
                    if error < best_error:  # 如果当前错误率小于最小错误率
                        best_error = error  # 更新最小错误率
                        best_learner = DecisionStump(feature, threshold, direction)  # 更新最佳学习器
        return best_learner  # 返回最佳学习器
 # 定义一个简单的决策树桩学习器
class DecisionStump:
    def __init__(self, feature, threshold, direction):
        self.feature = feature  # 学习器所选用的特征
        self.threshold = threshold  # 学习器所选用的阈值
        self.direction = direction  # 学习器所选用的方向
    def predict(self, X):
        m, _ = X.shape  # 获取数据集的行数和列数
        y_pred = np.ones(m)  # 初始化预测结果为全部为1
        y_pred[self.direction * X[:, self.feature] < self.direction * self.threshold] = -1  # 根据方向和阈值，将预测结果修改为1或-1
        return y_pred  # 返回预测结果
 # 示例
from sklearn.datasets import make_classification  # 导入数据集生成函数
from sklearn.metrics import accuracy_score  # 导入准确率函数
from sklearn.model_selection import train_test_split  # 导入数据集分割函数
 # 生成数据集
X, y = make_classification(n_samples=200, n_features=2, n_redundant=0, random_state=42)
y[y == 0] = -1  # 将标签中的0换成-1
 # 分割数据集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
 # 构建Adaboost分类器
adaboost = Adaboost(n_learners=10)  # 实例化Adaboost对象
adaboost.fit(X_train, y_train)  # 在训练集上拟合Adaboost分类器
 # 在测试集上进行预测
y_pred = adaboost.predict(X_test)  # 预测测试集标签
 # 计算分类准确率
accuracy = accuracy_score(y_test, y_pred)
print(f"Adaboost accuracy: {accuracy:.2f}")  # 输出Adaboost分类器的分类准确率