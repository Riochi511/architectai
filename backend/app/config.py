from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    DATABASE_URL: str

    JWT_SECRET_KEY: str

    # AI Provider
    MODEL_PROVIDER: str

    # OpenAI
    OPENAI_API_KEY: str = ""

    # OpenRouter
    OPENROUTER_API_KEY: str = ""

    # Model Name
    MODEL_NAME: str = "gpt-4.1-mini"

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


settings = Settings()