# Config helps to connect with database securly by hiding database information
from pydantic import BaseSettings


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str

    class Config:
        env_file = "../.env"


settings = Settings()


#%%
