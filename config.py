from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    LARK_URL: str

    class Config:
        env_file = ".env"


def get_settings():
    return Settings()


if __name__ == '__main__':
    settings = get_settings()

