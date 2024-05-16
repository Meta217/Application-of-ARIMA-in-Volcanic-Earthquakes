# 第一步：导入所需的库
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from pandas.plotting import register_matplotlib_converters
from sklearn.metrics import mean_squared_error
register_matplotlib_converters()
'''
# 第二步：数据加载和预处理
# 加载数据
data = pd.read_csv('output_jingpohu.csv', delimiter=',', parse_dates=['date'], index_col='date')

# 删除重复的日期
data = data[~data.index.duplicated(keep='first')]

# 检查数据
print(data.head(10))  # 显示前10行数据

# 第三步：数据可视化
# 绘制magnitude数据图
data['magnitude'].plot(title='Volcanic Magnitude Over Time')
plt.xlabel('Date')
plt.ylabel('Magnitude')
plt.show()
'''

# 检查是否提供了数据集名称作为命令行参数
if len(sys.argv) != 2:
    print("Usage: python arima_v5.py <dataset_name>")
    sys.exit(1)

# 获取命令行参数中的数据集名称
dataset_name = sys.argv[1]

# 根据数据集名称构建数据文件的路径
data_file_path = f"./data/data_{dataset_name}.csv"

# 第二步：数据加载和预处理
# 加载数据
data = pd.read_csv(data_file_path, delimiter=',', parse_dates=['date'], index_col='date')

# 删除重复的日期
data = data[~data.index.duplicated(keep='first')]

# 检查数据
print(data.head(10))  # 显示前10行数据

# 第三步：数据可视化
# 绘制magnitude数据图
data['magnitude'].plot(title=f'Volcanic Magnitude Over Time for {dataset_name}')
plt.xlabel('Date')
plt.ylabel('Magnitude')
plt.show()

# 第四步：进行ARIMA模型的参数选择
# 自动相关和偏自动相关图
plot_acf(data['magnitude'], lags=40)
plt.show()

plot_pacf(data['magnitude'], lags=40)
plt.show()

# 根据ACF和PACF图，手动选择参数。
p = 4  # 自回归项
d = 1  # 差分项
q = 0  # 移动平均项

# 第五步：建立ARIMA模型并拟合数据
# 使用全部观测值作为训练数据
train_data = data['magnitude']
model = ARIMA(train_data, order=(p, d, q))
model_fit = model.fit()

# 打印模型摘要
print(model_fit.summary())

# 第六步：进行预测
# 调整为未来三年每10天一次的预测，总共预测108次
end_point = len(train_data) + 108  # 计算预测的结束点
forecast = model_fit.get_forecast(steps=108)  # 使用get_forecast和步长为108来进行预测

# 提取预测的均值
forecast_mean = forecast.predicted_mean


# 第七步：模型诊断
model_fit.plot_diagnostics(figsize=(15, 8))

# 第八步：预测值与实际值对比
# 绘制真实值、拟合值和预测值对比图
plt.figure(figsize=(10, 6))
plt.plot(data.index, train_data, label='Actual Magnitude', marker='o')
plt.plot(data.index, model_fit.fittedvalues, label='Fitted Magnitude', linestyle='--', marker='x')
plt.plot(pd.date_range(start=data.index[-1], periods=108, freq='10D'), forecast_mean, label='Predicted Magnitude', linestyle='--', marker='x')
plt.xlabel('Date')
plt.ylabel('Magnitude')
plt.title('Actual vs Fitted vs Predicted Magnitude')
plt.legend()
plt.show()

# 计算 MSE
mse = mean_squared_error(train_data, model_fit.fittedvalues[:len(train_data)])
print(f"Mean Squared Error between actual and fitted values: {mse}")

