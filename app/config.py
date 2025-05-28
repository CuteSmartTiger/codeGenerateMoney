from pydantic.v1 import BaseSettings
from dotenv import load_dotenv
from functools import lru_cache


# 加载环境变量
load_dotenv()

class Settings(BaseSettings):
    LARK_URL: str
    PORT: int = 5000

    class Config:
        env_file = "../.env"


@lru_cache()
def get_settings() -> Settings:
    """获取Settings实例的单例，确保配置只被加载一次"""
    return Settings()


settings = get_settings()

indexIds = ["BTC-USDT", "ETH-USDT", "LTC-USDT", "OKB-USDT", "DOGE-USDT",
           "AVAX-USDT", "ADA-USDT", "BNB-USDT", "AIDOGE-USDT", "SOL-USDT",
           "APT-USDT", "EIGEN-USDT"]