from fastapi.responses import JSONResponse

from app.execution.execution import Execution
from app.config import get_settings

settings = get_settings()


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
    while True:
        Execution.execute("strategy_one")
        await asyncio.sleep(60*15)



@app.get("/")
async def read_strategy(name: str):
    return {"message": "Hello from FastAPI + lifespan!,strategy name is {}".format(name)}


@app.get("/healthz")
def health_check():
    return JSONResponse(content={"status": "ok"})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
