from typing import Annotated

from fastapi import APIRouter, Body

from schemas.feedback import FeedbackRequest, FeedbackResponse
from service_logging import logger

from .utils.evaluator import PronunciationEvaluator
from .utils.texts import get_transcription_reference

router = APIRouter()


@router.post("/", summary="Создать отчет по произношению")
async def create_feedback(data: Annotated[FeedbackRequest, Body(...)]) -> FeedbackResponse:
    """Создает отчет по произношению и возвращает его в качестве ответа."""
    logger.info("Obtaining a reference transcription...")
    reference = await get_transcription_reference(data.text_id)

    logger.info("Evaluating actual result...")
    evaluator = PronunciationEvaluator(
        reference=reference,
        actual=data.actual_result,
    )
    feedback = evaluator.compare()

    item = FeedbackResponse.model_validate(feedback)
    logger.success(f"Detected {len(item.mistakes)} mistakes. Total accuracy {item.accuracy}")

    return item
