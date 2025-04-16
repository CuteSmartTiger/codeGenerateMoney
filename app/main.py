import datetime

import okx.MarketData as MarketData

import requests
import json
import pandas as pd


flag = "0"  # 实盘:0 , 模拟盘：1
from app.config import get_settings

settings = get_settings()

marketDataAPI =  MarketData.MarketAPI(flag=flag)

# 定义列名
columns = ['ts', 'o', 'h', 'l', 'c', 'confirm']


def get_index_data(index, limit='6', bar='1H'):
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

    # 计算收益M和振幅Z
    df['M'] = df['c'] - df['o']  # 收益 = 收盘价 - 开盘价
    df['Z'] = df['M'] / df['o']  # 振幅 = 收益 / 开盘价
    return df


def trigger_lark(body):
    requests.post(url=settings.LARK_URL, json=body, headers={'Content-Type': 'application/json'})


def meet_strategy_one(k_data_df):
    if  not k_data_df['M'][0:2].min() > 0:
    #     若最近两个 K 线 bar 有一个是跌的，则不满足上涨趋势
        return False

    if not k_data_df['M'][2:6].max() < 0:
        return False

    return True



from fastapi import FastAPI
from contextlib import asynccontextmanager
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # ✅ 启动时：启动后台任务
    task = asyncio.create_task(background_worker())

    yield  # <-- 应用运行中

    # ✅ 关闭时：取消任务
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        print("后台任务被取消")

app = FastAPI(lifespan=lifespan)

async def background_worker():
    instIds = ["BTC-USDT", "ETH-USDT", "LTC-USDT", "OKB-USDT", "DOGE-USDT",
               "AVAX-USDT", "ADA-USDT", "BNB-USDT", "AIDOGE-USDT", "SOL-USDT",
               "LTC-USDT"]
    while True:
        for instId in instIds:
            # instId = "BTC-USDT"
            data = get_index_data(instId)
            df = calculate_index_data(data)
            # print(df)
            # if  df['M'][0:3].min() > 0 and (df['M'][0] > df['M'][1]):
            if meet_strategy_one(df):
                body_data = {'instId': instId,
                             'bar': '1H',
                             'M': json.loads(df.to_json())['M']
                             }
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "{}有上涨趋势".format(instId))
                trigger_lark(body_data)
            else:
                print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "{}没有上涨趋势".format(instId))

            await asyncio.sleep(2)

        await asyncio.sleep(60 * 15)


@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI + lifespan!"}
