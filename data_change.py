import csv
from datetime import datetime

# 原始数据文件名
input_filename = 'jingpohu.txt'
# 输出CSV文件名
output_filename = 'output_jingpohu.csv'

# 读取原始数据文件，并按时间排序
data = []
with open(input_filename, 'r') as file:
    for line in file:
        parts = line.strip().split('\t')
        # 解析每一行数据
        record = {
            'date': datetime.strptime(parts[1], '%Y-%m-%d %H:%M:%S'),
            'magnitude': float(parts[4])
        }
        data.append(record)

# 按时间从早到晚排序
data.sort(key=lambda x: x['date'])

# 将排序后的数据写入CSV文件
with open(output_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    # 写入标题行
    writer.writerow(['date', 'magnitude'])
    # 写入数据行
    for record in data:
        writer.writerow([record['date'].strftime('%Y-%m-%d'), record['magnitude']])

print(f'CSV file {output_filename} has been created.')



