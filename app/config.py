from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-5.6-luna"
    database_url: str = "sqlite:///./database/interview.db"
    max_answer_length: int = 6000
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()
