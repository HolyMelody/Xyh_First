import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
from datetime import timedelta

# 加载数据
data = pd.read_excel('F:\\tex\\Bicycel_2017\\Data.xlsx', index_col=0)
data.columns = pd.to_datetime(data.columns)

# 数据处理
data = data.T.resample('M').sum().T
X = np.array(data.columns).reshape(-1, 1)
y = data.values

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

# 预测未来三个月的数据
start_date = data.columns[-1] + timedelta(days=1)
end_date = start_date + timedelta(days=90)
future_dates = pd.date_range(start=start_date, end=end_date, freq='D')
X_future = np.array(future_dates).reshape(-1, 1)
y_future = model.predict(X_future)

# 保存预测结果
forecast = pd.DataFrame(y_future, index=future_dates, columns=data.index)
forecast.to_csv('F:\\tex\\Bicycel_2017\\Forecast.csv')

# 可视化结果
num_plots = 4
stations_per_plot = len(data.index) // num_plots

for i in range(num_plots):
    start = i * stations_per_plot
    end = (i + 1) * stations_per_plot if i < num_plots - 1 else len(data.index)
    plt.figure(figsize=(12, 6))
    plt.bar(data.index[start:end], forecast.iloc[:30, start:end].mean(axis=0))
    plt.xlabel('站点')
    plt.ylabel('平均使用量')
    plt.title(f'未来一个月站点 {start}-{end} 的预测结果')
    plt.savefig(f'F:\\tex\\Bicycel_2017\\Forecast_{i + 1}.png')
