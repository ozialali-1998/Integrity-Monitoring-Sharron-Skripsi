from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FIM Security Monitor"
    api_v1_prefix: str = "/api/v1"
    database_url: str = "sqlite:///./backend/app/db/fim.sqlite"
    default_allowed_base_path: str = ""

    model_config = SettingsConfigDict(env_file="backend/.env", env_file_encoding="utf-8")


settings = Settings()
