import pandas as pd

# 读取CSV文件
file_path = "sz.000516_2026-03-16_d.csv"
df = pd.read_csv(file_path)

# 确保peTTM列是数值类型
df['peTTM'] = pd.to_numeric(df['peTTM'], errors='coerce')

# 初始化排名列
df['pe_rank'] = None
df['pe_rank_percentile'] = None

# 对每个数据计算在前50个数据中的排名
window_size = 50
for i in range(len(df)):
    # 前50行数据不计算结果
    if i < window_size - 1:
        continue
    
    # 获取当前行及之前的50个数据
    window_data = df['peTTM'].iloc[i - window_size + 1:i + 1]
    
    # 去除NaN值
    window_data = window_data.dropna()
    
    if len(window_data) > 0:
        # 计算当前peTTM值
        current_pe = df.loc[i, 'peTTM']
        
        if not pd.isna(current_pe):
            # 计算排名
            rank = (window_data <= current_pe).sum() + 1
            # 计算排名百分比
            percentile = (rank / len(window_data)) * 100
            
            # 保存结果
            df.loc[i, 'pe_rank'] = rank
            df.loc[i, 'pe_rank_percentile'] = round(percentile, 2)

# 显示结果（从第50行开始）
print("从第50行开始的peTTM排名百分比：")
print(df[['date', 'peTTM', 'pe_rank', 'pe_rank_percentile']].iloc[window_size-1:window_size+9])

# 保存结果到新文件
output_file = "sz.000516_2026-03-16_d_with_pe_rank.csv"
df.to_csv(output_file, index=False)
print(f"\n结果已保存到 {output_file}")
