import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
import matplotlib.dates as mdates

# 读取数据
data = pd.read_csv('F:/tex/pre.csv')
# 保留日期、租赁数、季节、天气条件、假日、作日、温度和风速这些列
data = data[['data', 'cnt', 'season', 'weathersit', 'holiday', 'workingday', 'temp', 'windspeed']]
# 将日期列转换为datetime类型
data['data'] = pd.to_datetime(data['data'])
# 将时间序列设置为索引
data.set_index('data', inplace=True)

# 按天对租赁分组和
daily_data = data.resample('D').sum()

# 创建时间特征
daily_data['day'] = daily_data.index.day
daily_data['month'] = daily_data.index.month
daily_data['year'] = daily_data.index.year
daily_data['weekday'] = daily_data.index.weekday

# 将季节、天气条件、假日、工作日进行独热编码
ct = ColumnTransformer(transformers=[('encoder', OneHotEncoder(), ['season', 'weathersit', 'holiday', 'workingday'])], remainder='passthrough')
X = ct.fit_transform(daily_data[['day', 'month', 'year', 'weekday', 'season', 'weathersit', 'holiday', 'workingday', 'temp', 'windspeed']])
y = daily_data['cnt']

# 创建并拟合随机森林回归模型
rf_model = make_pipeline(RandomForestRegressor(n_estimators=100, random_state=42))
rf_model.fit(X, y)
print("Random Forest Regressor Model Training Completed.")

# 创建并拟合XGBoost回归模型
xgb_model = make_pipeline(xgb.XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42))
xgb_model.fit(X, y, xgbregressor__eval_set=[(X, y)], xgbregressor__verbose=2)
print("XGBoost Regressor Model Training Completed.")

# 构建未来一年的日期数据框
future_dates = pd.date_range(start='2012-12-31', periods=365, freq='D')
future_data = pd.DataFrame({'day': future_dates.day, 'month': future_dates.month, 'year': future_dates.year, 'weekday': future_dates.weekday, 'season': 4, 'weathersit': 1, 'holiday': 0, 'workingday': 1, 'temp': 0, 'windspeed': 0})

# 预测未来一年的租赁数
future_data = ct.transform(future_data)
rf_predictions = rf_model.predict(future_data)
xgb_predictions = xgb_model.predict(future_data)
print("Predictions Completed.")

# 将预测保存到CSV文件中
rf_forecast_data = pd.DataFrame(rf_predictions, columns=['cnt'], index=future_dates)
rf_forecast_data.to_csv('F:/tex/RF_Forecast.csv')
xgb_forecast_data = pd.DataFrame(xgb_predictions, columns=['cnt'], index=future_dates)
xgb_forecast_data.to_csv('F:/tex/XGB_Forecast.csv')
print("Forecasts Saved to CSV Files.")

# 绘制预测结果
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(daily_data.index, daily_data['cnt'], label='Actual')
ax.plot(future_dates, rf_forecast_data['cnt'], label='RF Forecast')
ax.plot(future_dates, xgb_forecast_data['cnt'], label='XGB Forecast')
ax.set_xlabel('Date')
ax.set_ylabel('Total Rentals')
ax.set_title('Daily Rentals')
ax.legend()
# 设置横轴刻度间隔为一个月
ax.xaxis.set_major_locator(mdates.MonthLocator(interval=1))
# 旋转横轴标签
plt.xticks(rotation=45)
plt.savefig('F:/tex/Daily.png')
print("Plot Saved to File.")
# 可视化特征重要性
xgb.plot_importance(xgb_model)
plt.show()
