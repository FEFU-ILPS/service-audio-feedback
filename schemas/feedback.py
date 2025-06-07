from uuid import UUID

from pydantic import BaseModel, Field

from routers.utils.evaluator import PhoneticMistake

from .examples import ACCURACY_EXAMPLES, ID_EXAMPLES, MISTAKES_EXAMPLES, RESULT_EXAMPLES


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
