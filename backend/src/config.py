from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    load_fake_data: bool = False
    database_url: str = "sqlite:///./test.db"

    class Config:
        env_file = ".env"


settings = Settings()
