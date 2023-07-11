import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet

# 读取数据
data = pd.read_csv('F:/tex/pre.csv')
# 保留日期和租赁数这两列
data = data[['data', 'cnt']]
# 将列名更改为Prophet库所需的格式
data.columns = ['ds', 'y']

# 将日期列转换为datetime类型
data['ds'] = pd.to_datetime(data['ds'])

# 创建Prophet模型并拟合数据
model = Prophet()
model.fit(data)

# 构建未来一年的日期数据框
future = model.make_future_dataframe(periods=365)

# 预测未来一年的租赁数
forecast = model.predict(future)

# 绘制预测结果
fig1 = model.plot(forecast)
plt.savefig('F:/tex/Month.png')

# 将预测结果保存到CSV文件中
forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv('F:/tex/Forecast.csv', index=False)
