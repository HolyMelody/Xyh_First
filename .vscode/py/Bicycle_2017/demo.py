import pandas as pd

# 读取数据
file_path = "F:\\tex\\Bicycel_2017\\Data.xlsx"
df = pd.read_excel(file_path, index_col=0)

# 转置数据
df_transposed = df.transpose()

# 计算每10个站点的总和
group_size = 10
grouped_data = {}
for i in range(0, len(df_transposed.columns), group_size):
    group_columns = df_transposed.columns[i:i + group_size]
    grouped_data[f'{group_columns[0]}-{group_columns[-1]}'] = df_transposed[group_columns].sum(axis=1)

# 创建新的数据框
df_grouped = pd.DataFrame(grouped_data)

# 保存数据到新文件
output_file_path = "F:\\tex\\Bicycel_2017\\Data1.xlsx"
df_grouped.to_excel(output_file_path)
