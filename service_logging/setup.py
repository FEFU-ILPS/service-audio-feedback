from __future__ import annotations

import sys

import graypy
import loguru
from loguru import logger

from configs import configs


def loguru_formatter(record: loguru.Record) -> str:
    """Возвращает строку формата логирования для loguru.

    Args:
        record (loguru.Record): Объект записи лога loguru.

    Returns:
        str: Строка формата.
    """
    request_hash = record["extra"].get("request_hash")

    hash_id = ""
    if request_hash:
        hash_id = f"<blue>{request_hash}</blue> | "

    # Формат: дата | время | сервис | уровень | файл:строка - сообщение (reques_id)
    return (
        "<green>{time:DD-MM-YYYY}</green> | "
        "<green>{time:HH:mm:ss}</green> | "
        "<cyan>{extra[service]}</cyan> | "
        "<level>{level: <8}</level> | "
        f"{hash_id}"
        "<cyan>{file}:{line}</cyan> - "
        "<level>{message}</level>\n"
    )


def setup_logger() -> loguru.Logger:
    """Функция инициализации кастомного логера loguru.

    В процессе инициализации устанавливается хендлер stdout,
    с уровнем DEBUG и кастомным оформлением формата лога.

    Дополнительно, если в конфигурации проекта установлена
    переменная GRAYLOG_ENABLE, подключается GELF хендлер
    для оправки логов в Graylog.
    """
    logger.remove()

    logger.add(
        sink=sys.stdout,  # ?
        format=loguru_formatter,
        level="DEBUG",
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    if configs.graylog.ENABLE:
        gelf_handler = graypy.GELFUDPHandler(
            configs.graylog.HOST,
            configs.graylog.PORT,
        )
        logger.add(
            sink=gelf_handler,
            format=loguru_formatter,
            level="DEBUG",
            backtrace=True,
            diagnose=True,
        )

    return logger.bind(service=configs.SERVICE_NAME)
