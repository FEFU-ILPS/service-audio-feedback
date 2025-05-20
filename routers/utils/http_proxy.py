from contextlib import asynccontextmanager
from json import JSONDecodeError
from typing import AsyncGenerator

from fastapi import HTTPException, status
from httpx import AsyncClient, ConnectError, ConnectTimeout, HTTPStatusError

from service_logging import logger


@asynccontextmanager
async def proxy_request(service_url: str) -> AsyncGenerator[AsyncClient, None]:
    """Асинхронный контекстный менеджер проксирования HTTP запросов
    к связанным микросервисам по их URL. Выполняет автоматический
    отлов и проксирование ошибок, а также логирование хода запроса.

    Args:
        service_url (str): URL адрес сервиса.

    Raises:
        HTTPException: Проксированная ошибка от сервиса.
        HTTPException: 503. Ошибка подключения к сервису.

    Yields:
        AsyncGenerator[AsyncClient, None]: Генератор асинхронного клиента httpx.
    """
    logger.info(f"Proxying a service request to {service_url}")
    async with AsyncClient(base_url=service_url) as client:
        try:
            yield client

        except HTTPStatusError as error:
            status_code = error.response.status_code

            try:
                content = error.response.json()
                detail = content.get("detail", "Unknown error")

            except JSONDecodeError:
                detail = error.response.content

            message = f"Service at {service_url} returned an error respose: {detail}"
            logger.error(message)

            raise HTTPException(
                status_code=status_code,
                detail=detail,
            )

        except (ConnectError, ConnectTimeout) as error:
            detail = str(error)

            message = f"Service at {service_url} is unavailable: {detail}"
            logger.error(message)

            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=detail,
            )
