from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "BI Platform"
    api_v1_str: str = "/api/v1"
    secret_key: str = "CHANGE_ME_SUPER_SECRET"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/bi_app"
    upload_dir: str = "uploads"
    max_upload_size_mb: int = 25

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
