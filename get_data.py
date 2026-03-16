import baostock as bs
import pandas as pd
from datetime import datetime
    
#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:'+lg.error_code)
print('login respond  error_msg:'+lg.error_msg)

#### 获取沪深A股历史K线数据 ####
# frequency：数据类型，默认为d，日k线；d=日k线、w=周、m=月、5=5分钟、15=15分钟、30=30分钟、60=60分钟k线数据
# adjustflag：复权类型，默认不复权：3；1：后复权；2：前复权
end_date = datetime.now().strftime('%Y-%m-%d') # 获取当天日期
# 定义股票代码和频率
stock_code = "sz.000516"
frequency = "d"
rs = bs.query_history_k_data_plus(stock_code,
    "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,isST,peTTM,pbMRQ",
    start_date='2005-01-01', end_date=end_date,
    frequency=frequency, adjustflag="2")
print('query_history_k_data_plus respond error_code:'+rs.error_code)
print('query_history_k_data_plus respond  error_msg:'+rs.error_msg)
    
#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

# 清洗数据，删除volume列数值为0的行
result = result[result['volume'] != '0']
    
#### 结果集输出到csv文件 ####   
# 构造文件名：股票代码_end date_frequency
file_name = f"{stock_code}_{end_date}_{frequency}.csv"
result.to_csv(file_name, index=False)
print(result)
    
#### 登出系统 ####
bs.logout()