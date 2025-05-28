import okx.MarketData as MarketData
import pandas as pd

flag = "0"  # 实盘:0 , 模拟盘：1
marketDataAPI =  MarketData.MarketAPI(flag=flag)

# 定义列名
columns = ['ts', 'o', 'h', 'l', 'c', 'confirm']


def get_index_data(index, limit='7', bar='4H'):
    # 获取指数K线数据
    result = marketDataAPI.get_index_candlesticks(instId=index, limit=limit, bar=bar)
    # 原始数据
    return result['data']


def calculate_index_data(index_data):
    # 创建DataFrame
    df = pd.DataFrame(index_data, columns=columns)

    # 转换数值列的类型
    numeric_cols = ['o', 'h', 'l', 'c']
    df[numeric_cols] = df[numeric_cols].astype(float)
    df['confirm'] = df['confirm'].astype(int)
    df['ts'] = pd.to_datetime(df['ts'].astype('int64'), unit='ms', utc=True)
    # 转为北京时间（中国标准时间）
    df['beijing'] = df['ts'].dt.tz_convert('Asia/Shanghai')
    df['beijing'] = df['beijing'].dt.strftime('%Y-%m-%d %H:%M')

    # 计算收益M和振幅Z
    df['ts'] = df['ts'].astype('int64') * 100

    df['profit'] = (df['c'] - df['o'])/(df['o'].astype(float)/100) # 收益 = 收盘价 - 开盘价
    df['amplitudeRatio'] = (df['h'] - df['l'])/(df['o'].astype(float)/100)  # 振幅 = 最高 - 最低
    return df




if __name__ == '__main__':
    instId = "BNB-USDT"
    data = get_index_data(instId)
    df = calculate_index_data(data)
