from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    MONGO_USER: str = Field("test_user", validate_default=False)
    MONGO_PASSWORD: str = Field("test_password", validate_default=False)
    MONGO_USER_DATABASE: str = Field("test_database", validate_default=False)
    MONGO_URI: str = Field(
        "mongodb://test_user:test_password@localhost/test_database",
        validate_default=False,
    )
    SECRET_KEY: str = Field("your_secret_key", validate_default=False)
    ALGORITHM: str = Field("HS256", validate_default=False)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, validate_default=False)
