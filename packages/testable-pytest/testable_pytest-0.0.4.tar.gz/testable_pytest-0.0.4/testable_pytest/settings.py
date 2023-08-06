from pydantic import BaseSettings


class Settings(BaseSettings):
    testable_base_url: str

    class Config:
        env_file = ".env"
        env_nested_delimiter = "__"
