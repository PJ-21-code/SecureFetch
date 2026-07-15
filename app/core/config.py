from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, Field

class Settings(BaseSettings):

    SAP_ODATA_URL: str
    SAP_USERNAME: str
    SAP_PASSWORD: SecretStr

    XSRF_HEADER_NAME: str= Field(default="X-CSRF-Token")
    XSRF_FETCH_VALUE: str= Field(default="Fetch")

    model_config= SettingsConfigDict(env_file=".env")


settings= Settings()    