from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    earthdata_token: str  # Solo tu token de NASA Earthdata

    class Config:
        env_file = ".env"
        extra = "forbid"

def get_settings():
    return Settings()
