from uuid import UUID

from configs import configs
from .http_proxy import proxy_request


async def get_transcription_reference(text_id: UUID) -> str:
    """Получает данные о тексте по переданному идентификатору и возвращает
    его эталонную фонетическую запись.

    Args:
        text_id (UUID): Идентификатор текста.

    Returns:
        str: Эталонная фонетическая запись.
    """
    async with proxy_request(configs.services.texts.URL) as client:
        response = await client.get(f"/{text_id}")
        response.raise_for_status()

        return response.json()["transcription"]
