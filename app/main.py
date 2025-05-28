import datetime


from fastapi.responses import JSONResponse

import requests
import json

from app.real_data.okex import get_index_data,calculate_index_data,meet_strategy_one


from app.config import get_settings

settings = get_settings()


has_trigger ={}

def trigger_lark(body,remove_duplicates=True):
    if remove_duplicates:
        if not body['timeId'] in has_trigger:
            requests.post(url=settings.LARK_URL, json=body, headers={'Content-Type': 'application/json'})
            has_trigger[body['timeId']] = True


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
    except Exception as e:
        print("任务取消异常原因{}".format(e))

app = FastAPI(lifespan=lifespan)

async def background_worker():
    instIds = ["BTC-USDT", "ETH-USDT", "LTC-USDT", "OKB-USDT", "DOGE-USDT",
               "AVAX-USDT", "ADA-USDT", "BNB-USDT", "AIDOGE-USDT", "SOL-USDT",
               "APT-USDT","EIGEN-USDT"]
    while True:
        try:
            for instId in instIds:
                print("循环中",instId)
                data = get_index_data(instId)
                df = calculate_index_data(data)
                if meet_strategy_one(df):
                    msg = "{} {} 有上涨趋势 ".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), instId)
                    body_data = {'instId': instId,
                                 'bar': '4H',
                                 'timeId':df['beijing'].iloc[0],
                                 'profit': json.loads(df.to_json())['profit'],
                                 'amplitudeRatio':json.loads(df.to_json())['amplitudeRatio'],
                                 'msg':msg
                                 }

                    trigger_lark(body_data)
                else:
                    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "{} 没有上涨趋势".format(instId))
                await asyncio.sleep(2)
        except Exception as e:
            print(e)

        await asyncio.sleep(60*15)



@app.get("/")
async def read_root():
    return {"message": "Hello from FastAPI + lifespan!"}


@app.get("/healthz")
def health_check():
    return JSONResponse(content={"status": "ok"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
