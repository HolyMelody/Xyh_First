import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA

# 读取数据
data = pd.read_csv('F:\\tex\\data.csv', index_col='instant', parse_dates=True)

# 按日期排序
data = data.sort_index()

# 拆分数据集
train_data = data[:-365]  # 训练集为前一年的数据
test_data = data[-365:]   # 测试集为最后一年的数据

# 训练模型
model = ARIMA(train_data['cnt'], order=(2, 1, 2))  # ARIMA模型，阶数为(2, 1, 2)
result = model.fit()

# 对测试集进行预测
pred = result.predict(start='2012-01-01', end='2012-12-31', dynamic=False)

# 绘制预测结果和实际值
plt.plot(pred, label='Predicted')
plt.plot(test_data['cnt'], label='Actual')
plt.legend()
plt.show()