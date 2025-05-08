from uuid import UUID

import httpx
from fastapi import HTTPException

from configs import configs


async def get_transcription_reference(text_id: UUID) -> str:
    """Получает данные о тексте по переданному идентификатору и возвращает
    его эталонную фонетическую запись.

    Args:
        text_id (UUID): Идентификатор текста.

    Raises:
        HTTPException: Проксирует ошибки с сервиса service-texts.

    Returns:
        str: Эталонная фонетическая запись.
    """
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{configs.services.texts.URL}/{text_id}")

            response.raise_for_status()

            return response.json()["transcription"]

        except httpx.HTTPStatusError as e:
            raise HTTPException(
                status_code=e.response.status_code,
                detail=e.response.json().get("detail", "Unknown error"),
            )
