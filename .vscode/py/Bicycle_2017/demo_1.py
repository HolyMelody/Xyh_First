import os
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
from datetime import timedelta
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


# 读取数据
data_path = "F:\\tex\\Bicycel_2017\\Data1.xlsx"
df = pd.read_excel(data_path)

# 预处理数据
df['ds'] = pd.to_datetime(df.iloc[:, 0])
df.drop(df.columns[0], axis=1, inplace=True)

# 创建输出目录
output_dir = "F:\\tex\\Bicycel_2017\\"
os.makedirs(output_dir, exist_ok=True)

# 预测未来三个月的租赁数
forecast_results = []
for column in df.columns:
    temp_df = df[['ds', column]]
    temp_df.columns = ['ds', 'y']
    model = Prophet()
    model.fit(temp_df)
    future = model.make_future_dataframe(periods=90)
    forecast = model.predict(future)
    forecast_results.append((column, forecast))

# 保存预测结果到CSV文件
forecast_dfs = []
for column, forecast in forecast_results:
    temp_df = forecast[['ds', 'yhat']]
    temp_df.columns = ['ds', column]
    forecast_dfs.append(temp_df)
result_df = pd.concat(forecast_dfs, axis=1)
result_df = result_df.loc[:, ~result_df.columns.duplicated()]
result_df.to_csv(os.path.join(output_dir, "Forecast.csv"), index=False)

# 绘制树状图
for i, (column, forecast) in enumerate(forecast_results):
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(forecast['ds'], forecast['yhat'])
    ax.set_title(f"站点 {column} 未来一个月的租赁数预测")
    ax.set_xlabel("日期")
    ax.set_ylabel("租赁数")
    ax.set_xlim(forecast['ds'].iloc[-90], forecast['ds'].iloc[-60])
    plt.savefig(os.path.join(output_dir, f"Forecast_{i + 1}.png"), dpi=300)
    plt.close(fig)

# 绘制柱状图
total_rentals = []
for column, forecast in forecast_results[:-1]:
    total_rentals.append(max(int(forecast['yhat'].iloc[-90:-60].sum()), 0))

fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(df.columns[:-1], total_rentals) # exclude the last element in both lists
ax.set_title("各站点未来一个月的总租赁数预测")
ax.set_xlabel("站点")
ax.set_ylabel("租赁数")
plt.xticks(rotation=45)
ax.set_ylim(bottom=0)
plt.savefig(os.path.join(output_dir, "contrast.png"), dpi=300)
plt.close(fig)
