from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    PORT: int = 5000
    RELOAD: bool = True
    HOST: str = "127.0.0.1"

    DB_NAME: str = "charlie"
    DB_URI: str = "mongodb://localhost:27017"

    model_config = SettingsConfigDict(
        extra="ignore",
        env_file="environments/.env",
        env_prefix="CHARLIE_",
    )
