import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.svm import SVR
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
import matplotlib.dates as mdates

# 读取数据
data = pd.read_csv('F:/tex/pre.csv')
# 保留日期和租赁数这两列
data = data[['data', 'cnt']]
# 将日期列转换为datetime类型
data['data'] = pd.to_datetime(data['data'])
# 将时间序列设置为索引
data.set_index('data', inplace=True)

# 按天对租赁数进行分组求和
daily_data = data.resample('D').sum()

# 创建时间特征
daily_data['day'] = daily_data.index.day
daily_data['month'] = daily_data.index.month
daily_data['year'] = daily_data.index.year
daily_data['weekday'] = daily_data.index.weekday

# 将数据分为特征和目标变量
X = daily_data[['day', 'month', 'year', 'weekday']]
y = daily_data['cnt']

# 创建并拟合支持向量回归模型
model = make_pipeline(StandardScaler(), SVR(kernel='rbf', C=100, gamma=0.1, epsilon=.1))
model.fit(X, y)

# 构建未来两年的日期数据框
future_dates = pd.date_range(start='2014-12-31', periods=730, freq='D')
future_data = pd.DataFrame({'day': future_dates.day, 'month': future_dates.month, 'year': future_dates.year, 'weekday': future_dates.weekday}, index=future_dates)

# 预测未来两年的租赁数
predictions = model.predict(future_data)

# 绘制预测结果
fig, ax = plt.subplots(figsize=(20, 10))
ax.plot(daily_data.index, daily_data['cnt'], label='Actual')
ax.plot(future_dates, predictions, label='Forecast')
ax.set_xlabel('Date')
ax.set_ylabel('Total Rentals')
ax.set_title('Daily Rentals')
ax.legend()
# 设置横轴刻度间隔为一个月
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
# 旋转横轴标签
plt.xticks(rotation=45)
plt.savefig('F:/tex/Daily.png')

# 将预测结果保存到CSV文件中
forecast_data = pd.DataFrame(predictions, columns=['cnt'], index=future_dates)
forecast_data.to_csv('F:/tex/Forecast.csv')
