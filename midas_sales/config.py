from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env',
                                      env_file_encoding='utf-8')
    db_type: str | None
    db_user: str | None
    db_password: str | None
    db_host: str | None
    db_port: int | None
    db_name: str | None
    db_ssl: str | None
    secret_key: str | None
    algorithm: str | None
    access_token_expire_minutes: int | None
    stripe_api_key: str | None
    aws_access_key_id: str | None
    aws_secret_access_key: str | None
    aws_region_name: str | None
    aws_bucket_name: str | None
    broker_url: str | None
    celery_backend_url: str | None
    smtp_host: str | None
    smtp_port: int | None
    smtp_password: str | None
    pdf_turtle_url: str | None
    celery_broker_url: str | None
    celery_result_backend: str | None


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
