import pandas as pd
import matplotlib.pyplot as plt
import bisect
### 计算PE分位 ###
# 获取时间窗口内每个交易日的PE值，形成数据集：PE历史窗口=[PE1,PE2,PE3,...]，将历史PE数据从小到大排序
# 计算PE分位：PE分位=当前PE在历史PE中的排名/历史PE的总交易日数


# 读取数据
df=pd.read_csv('sz.301047_2026-03-10_d.csv')

# 确保日期列是日期类型
df['date'] = pd.to_datetime(df['date'])

# 提取 peTTM 列并转换为数值类型
df['peTTM'] = pd.to_numeric(df['peTTM'], errors='coerce')

# 计算n年窗口的 PE 分位，一般为5年
def calculate_pe_percentile(row, years=1):
    # 获取当前日期
    current_date = row['date']
    # 计算窗口开始日期（5年前）
    window_start = current_date - pd.Timedelta(days=365*years)
    # 获取窗口内的 PE 数据
    window_data = df[(df['date'] >= window_start) & (df['date'] <= current_date)]['peTTM']
    # 去除 NaN 值
    window_data = window_data.dropna()
    # 确保窗口数据量足够（至少80%的预期数据量）
    expected_days = 252 * years  # 每年约252个交易日
    if len(window_data) < expected_days * 0.8:
        return (None, None)
    # 计算当前 PE
    current_pe = row['peTTM']
    if pd.isna(current_pe):
        return (None, None)
    # 排序窗口数据
    sorted_pe = sorted(window_data)
    # 使用二分查找计算排名（从1开始）
    rank = bisect.bisect_left(sorted_pe, current_pe) + 1
    # 计算分位并保留四位小数
    percentile = round(rank / len(window_data), 4)
    return (rank, percentile)

# 应用函数计算排名和分位
df[['pe_rank', 'pe_percentile']] = df.apply(calculate_pe_percentile, axis=1, result_type='expand')

# 显示最后10行结果
print("\n最后10行 PE 分位计算结果：")
print(df[['date', 'peTTM', 'pe_rank', 'pe_percentile']].tail(10))

# 保存结果到新文件
output_file = 'sz.301047_2026-03-10_d_with_pe_percentile_final.csv'
df.to_csv(output_file, index=False)
print(f"\n结果已保存到 {output_file}")

