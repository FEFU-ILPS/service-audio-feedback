from typing import TypedDict
from uuid import UUID

from pydantic import BaseModel, Field

from .examples import ID_EXAMPLES, RESULT_EXAMPLES, ACCURACY_EXAMPLES, MISTAKES_EXAMPLES


class PhoneticMistake(TypedDict):
    """Типизированный словарь для описания фонетической ошибки пользователя."""

    position: int
    reference: str | None
    actual: str | None
    type: str


class FeedbackRequest(BaseModel):
    """Данные, необходимые для формирования  отчёта по произношению."""

    text_id: UUID = Field(description="Идентификатор текста", examples=ID_EXAMPLES)
    actual_result: str = Field(description="Результат транскрибирования", examples=RESULT_EXAMPLES)


class FeedbackResponse(BaseModel):
    """Данные, отправляемые после формирования отчёта по произношению."""

    accuracy: float = Field(
        description="Точность произношения", ge=0.0, le=100.0, examples=ACCURACY_EXAMPLES
    )
    mistakes: list[PhoneticMistake] = Field(
        description="Ошибки произношенияю", examples=MISTAKES_EXAMPLES
    )
