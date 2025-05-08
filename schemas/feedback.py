from uuid import UUID

from pydantic import BaseModel, Field

from routers.utils.evaluator import PronunciationAssessment
from typing import Annotated

from .examples import ID_EXAMPLES, RESULT_EXAMPLES


class FeedbackRequest(BaseModel):
    """Данные, необходимые для формирования  отчёта по произношению."""

    text_id: UUID = Field(description="Идентификатор текста", examples=ID_EXAMPLES)
    actual_result: str = Field(description="Результат транскрибирования", examples=RESULT_EXAMPLES)


class FeedbackResponse(BaseModel):
    """Данные, отправляемые после формирования отчёта по произношению."""

    accuracy: float = Field(description="Точность произношения", ge=0, le=100)
    assessment: Annotated[str, PronunciationAssessment] = Field(description="Оценка произношения")
    errors: list[dict[str, int | str]] = Field(description="Ошибки произношенияю")
