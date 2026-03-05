import pandas as pd
import matplotlib.pyplot as plt
### 计算PE分位 ###
# 获取时间窗口内每个交易日的PE值，形成数据集：PE历史窗口=[PE1,PE2,PE3,...]，将历史PE数据从小到大排序
# 计算PE分位：PE分位=当前PE在历史PE中的排名/历史PE的总交易日数


# 读取数据
df=pd.read_csv('sh.600703_2026-03-04_d.csv')

# 确保日期列是日期类型
df['date'] = pd.to_datetime(df['date'])

# 提取 peTTM 列并转换为数值类型
df['peTTM'] = pd.to_numeric(df['peTTM'], errors='coerce')

# 计算 30 天窗口的 PE 分位
def calculate_pe_percentile(row, window=30):
    # 获取当前行的索引
    idx = row.name
    # 只有当数据量达到窗口大小时才计算
    if idx < window - 1:
        return (None, None)
    # 确定窗口范围（前30天）
    start_idx = idx - window + 1
    # 获取窗口内的 PE 数据
    window_data = df['peTTM'].iloc[start_idx:idx+1]
    # 去除 NaN 值
    window_data = window_data.dropna()
    # 确保窗口数据量足够
    if len(window_data) < window:
        return (None, None)
    # 计算当前 PE
    current_pe = row['peTTM']
    # 排序窗口数据
    sorted_pe = sorted(window_data)
    # 计算排名（从1开始）
    rank = sorted_pe.index(current_pe) + 1 if current_pe in sorted_pe else None
    # 计算分位并保留四位小数
    percentile = round(rank / len(window_data), 4) if rank is not None else None
    return (rank, percentile)

# 应用函数计算排名和分位
df[['pe_rank', 'pe_percentile']] = df.apply(calculate_pe_percentile, axis=1, result_type='expand')

# 显示最后10行结果
print("\n最后10行 PE 分位计算结果：")
print(df[['date', 'peTTM', 'pe_rank', 'pe_percentile']].tail(10))

# 保存结果到新文件
output_file = 'sh.600703_2026-03-04_d_with_pe_percentile_final.csv'
df.to_csv(output_file, index=False)
print(f"\n结果已保存到 {output_file}")

# 绘制 PE 分位和收盘价曲线
plt.figure(figsize=(12, 6))

# 创建主坐标轴（PE 分位）
ax1 = plt.gca()
ax1.plot(df['date'], df['pe_percentile'], marker='o', markersize=3, linestyle='-', linewidth=1, color='blue', label='PE 分位')
ax1.set_xlabel('日期')
ax1.set_ylabel('PE 分位', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')
ax1.grid(True, linestyle='--', alpha=0.7)

# 创建次要坐标轴（收盘价）
ax2 = ax1.twinx()
# 确保收盘价是数值类型
df['close'] = pd.to_numeric(df['close'], errors='coerce')
ax2.plot(df['date'], df['close'], marker='s', markersize=3, linestyle='-', linewidth=1, color='red', label='收盘价')
ax2.set_ylabel('收盘价', color='red')
ax2.tick_params(axis='y', labelcolor='red')

# 添加标题和图例
plt.title('PE 分位与收盘价走势')
plt.legend(loc='upper left')

plt.xticks(rotation=45)
plt.tight_layout()

# 保存图表
plt.savefig('pe_percentile_with_close_trend.png', dpi=150)
print("\nPE 分位与收盘价折线图已保存到 pe_percentile_with_close_trend.png")

# 显示图表
plt.show()