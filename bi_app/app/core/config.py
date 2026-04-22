from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "BI Platform (Jinja)"
    api_prefix: str = "/api/v1"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    database_url: str = "postgresql+psycopg2://postgres:postgres@db:5432/bi_app"
    max_upload_mb: int = 25
    upload_dir: str = "uploads"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
