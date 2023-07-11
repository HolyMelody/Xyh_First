import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# 读取数据
data = pd.read_csv('F:/tex/pre.csv')
# 保留日期和租赁数这两列
data = data[['data', 'cnt']]
# 将日期列转换为datetime类型
data['data'] = pd.to_datetime(data['data'])
# 将时间序列设置为索引
data.set_index('data', inplace=True)

# 按月份对租赁数进行分组求和
monthly_data = data.resample('M').sum()

# 创建时间特征
monthly_data['month'] = monthly_data.index.month
monthly_data['year'] = monthly_data.index.year

# 将数据分为特征和目标变量
X = monthly_data[['month', 'year']]
y = monthly_data['cnt']

# 创建并拟合线性回归模型
model = LinearRegression()
model.fit(X, y)

# 构建未来一年的日期数据框
future_dates = pd.date_range(start='2012-12-31', periods=12, freq='M')
future_data = pd.DataFrame({'month': future_dates.month, 'year': future_dates.year}, index=future_dates)

# 预测未来一年的租赁数
predictions = model.predict(future_data)

# 绘制预测结果
plt.plot(monthly_data.index, monthly_data['cnt'], label='Actual')
plt.plot(future_dates, predictions, label='Forecast')
plt.xlabel('Month')
plt.ylabel('Total Rentals')
plt.title('Monthly Rentals')
plt.legend()
plt.savefig('F:/tex/Month.png')

# 将预测结果保存到CSV文件中
forecast_data = pd.DataFrame(predictions, columns=['cnt'], index=future_dates)
forecast_data.to_csv('F:/tex/Forecast.csv')
