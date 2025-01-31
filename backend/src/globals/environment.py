from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class EnvironmentSettings(BaseSettings):
    supabase_url: str
    supabase_key: str
    pinecone_api_key: str
    openai_api_key: str

    model_config = SettingsConfigDict(env_file="./.env")


DraftEnvironment: EnvironmentSettings = EnvironmentSettings()
