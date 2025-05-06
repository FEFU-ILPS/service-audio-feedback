from pydantic_settings import BaseSettings, SettingsConfigDict
from .database import DatabaseConfiguration


class ProjectConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="FEEDBACK_")

    # * Вложенные группы настроек
    models: DatabaseConfiguration = DatabaseConfiguration()

    # * Опциональные переменные
    DEBUG_MODE: bool = True
    SERVICE_NAME: str = "ilps-service-audio-feedback"


configs = ProjectConfiguration()

__all__ = ("configs",)
