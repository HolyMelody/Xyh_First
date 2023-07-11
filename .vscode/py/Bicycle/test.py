import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import numpy as np

# 加载数据
data = pd.read_csv('F:\\tex\\data.csv')

# 特征和目标变量
X = data.drop(['instant', 'data', 'cnt'], axis=1)
y = data['cnt']

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 训练线性回归模型
model = LinearRegression()
model.fit(X_train, y_train)

# 预测
y_pred = model.predict(X_test)

# 评估模型
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# 可视化结果
plt.plot(y_test.index, y_test.values, label='实际租赁数')
plt.plot(y_test.index, y_pred, label='预测租赁数')
plt.legend()
plt.show()
