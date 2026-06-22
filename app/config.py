from pydantic import SecretStr, IPvAnyAddress
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="app/.env",
        env_file_encoding="utf-8",
    )

    secret_key: SecretStr
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    db: str
    username: SecretStr
    password: SecretStr
    host_address: IPvAnyAddress
    port: int
    db_name: str

settings = Settings()