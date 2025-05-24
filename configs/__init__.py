from pydantic_settings import BaseSettings, SettingsConfigDict

from .graylog import GraylogConfiguration
from .services import ServicesConfiguration


class ProjectConfiguration(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="FEEDBACK_")

    # * Вложенные группы настроек
    services: ServicesConfiguration = ServicesConfiguration()
    graylog: GraylogConfiguration = GraylogConfiguration()

    # * Опциональные переменные
    DEBUG_MODE: bool = True
    SERVICE_NAME: str = "ilps-service-audio-feedback"


configs = ProjectConfiguration()

__all__ = ("configs",)
