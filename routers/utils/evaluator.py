import json
from enum import Enum
from typing import Literal, TypedDict

from service_logging import logger

type DPTable = list[list[int]]


class CompareType(Enum):
    """Список результирующих типов сравнения фонем."""

    REPLACEMENT = "Replacement"
    INSERTION = "Insertion"
    DELETION = "Deletion"
    MATCH = "Match"


class Phoneme(TypedDict):
    """Представление единичной фонемы из фонетической записи."""

    position: int
    value: str


class PhoneticMistake(TypedDict):
    """Представление фонетической ошибки при сравнении
    эталонной и фактической записи.
    """

    reference: Phoneme | None
    actual: Phoneme | None
    type: CompareType


class Feedback(TypedDict):
    """Представление отчёта по произношению."""

    accuracy: float
    mistakes: list[PhoneticMistake]


class SequenceAligner:
    """Класс выравнивания двух последовательностей по алгоритму Нидлмана-Вунша."""

    def __init__(self, reference: str, actual: str):
        """Инициализация класса поиска выравнивания.

        Args:
            reference (str): Эталонная строка.
            actual (str): Фактическая строка.
        """
        self.reference = reference
        self.actual = actual

        self.dimension_x = 0
        self.dimension_y = 0

    def get_align(self) -> list[CompareType]:
        """Получает результирующее выравнивание между эталонной и фактической
        строкой.

        Выравниванием называется разница между символами двух сравниваемых строк.
        Разница между символами - это некий результат сравнения соответствующих
        позиций в строке, который дает понять, был ли символ заменён, удалён или
        вставлен туда, где его быть не должно. Т.е. выравнивание - это множество,
        отвечающее на вопрос "какую последовательность операций нужно совершить,
        чтобы привести эталон к сравниваемой строке кратчайшим путём?".

        Returns:
            list[CompareType]: Вектор операций выравнивания.
        """
        self.dimension_x, self.dimension_y = len(self.reference), len(self.actual)

        dpt = self._initialize_dp_table()
        self._fill_dp_table(dpt)

        return self._traceback_alignment(dpt)

    def _initialize_dp_table(self) -> DPTable:
        """Инициализирует таблицу динамического программирования.

        Подробнее про таблицу ДП можно прочесть тут:
        https://ru.wikipedia.org/wiki/Динамическое_программирование

        Returns:
            DPTable: Таблица ДП.
        """
        dpt = [[0] * (self.dimension_y + 1) for _ in range(self.dimension_x + 1)]

        for i in range(self.dimension_x + 1):
            dpt[i][0] = i
        for j in range(self.dimension_y + 1):
            dpt[0][j] = j

        return dpt

    def _fill_dp_table(self, dpt: DPTable) -> None:
        """Заполняет таблицу ДП согласно правилам Нидлмана-Вунша.

        Args:
            dp (DPTable): Таблица ДП.
        """
        for i in range(1, self.dimension_x + 1):
            for j in range(1, self.dimension_y + 1):
                match_cost = 0 if self.reference[i - 1] == self.actual[j - 1] else 1
                match = dpt[i - 1][j - 1] + match_cost
                delete = dpt[i - 1][j] + 1
                insert = dpt[i][j - 1] + 1
                dpt[i][j] = min(match, delete, insert)

    def _traceback_alignment(self, dp: DPTable) -> list[CompareType]:
        """Выполняет обратный проход по таблице ДП для получения
        последовательности операций выравнивания.

        Args:
            dp (DPTable): Заполненная таблица ДП.

        Returns:
            list[CompareType]: Вектор операций выравнивания.
        """
        alignment: list[CompareType] = []
        i, j = self.dimension_x, self.dimension_y

        while i > 0 or j > 0:
            if (is_match := self._is_match(i, j, dp)) or self._is_replacement(i, j, dp):
                alignment.append(CompareType.MATCH if is_match else CompareType.REPLACEMENT)
                i -= 1
                j -= 1
            elif self._is_deletion(i, j, dp):
                alignment.append(CompareType.DELETION)
                i -= 1
            else:
                alignment.append(CompareType.INSERTION)
                j -= 1

        return alignment[::-1]

    def _is_match(self, i: int, j: int, dp: DPTable) -> bool:
        """Проверяет, был ли текущий шаг совпадением символов.

        Args:
            i (int): Позиция в первом измерении.
            j (int): Позиция во втором измерении.
            dp (DPTable): Таблица ДП.

        Returns:
            bool: Флаг статуса совпадения.
        """
        if i <= 0 or j <= 0:
            return False

        return self.reference[i - 1] == self.actual[j - 1] and dp[i][j] == dp[i - 1][j - 1]

    def _is_replacement(self, i: int, j: int, dp: DPTable) -> bool:
        """Проверяет, был ли текущий шаг заменой символов.

        Args:
            i (int): Позиция в первом измерении.
            j (int): Позиция во втором измерении.
            dp (DPTable): Таблица ДП.

        Returns:
            bool: Флаг статуса замены.
        """
        if i <= 0 or j <= 0:
            return False

        return self.reference[i - 1] != self.actual[j - 1] and dp[i][j] == dp[i - 1][j - 1] + 1

    def _is_deletion(self, i: int, j: int, dp: DPTable) -> bool:
        """Проверяет, был ли текущий шаг удалением символов.

        Args:
            i (int): Позиция в первом измерении.
            j (int): Позиция во втором измерении.
            dp (DPTable): Таблица ДП.

        Returns:
            bool: Флаг статуса удаления.
        """
        return i > 0 and dp[i][j] == dp[i - 1][j] + 1


class PronunciationEvaluator:
    """Класс оценки произношения пользователя."""

    def __init__(self, reference: str, actual: str) -> None:
        """Инициализация класса оценки произношения.

        Args:
            reference (str): Эталонная фонетическая запись.
            actual (str): Фактическая фонетическая запись.
        """
        self.reference: list[str] = reference.split()
        self.actual: list[str] = actual.split()
        self.mistakes: list[PhoneticMistake] = []
        self.matches: int = 0
        self.aligner = SequenceAligner(self.reference, self.actual)

    def _construct_error(
        self, ref_pos: int, act_pos: int, cmp_type: CompareType
    ) -> PhoneticMistake:
        """Формирует ошибку на основе текущей позиции символа и типа
        операции выравнивания в векторе операций выравнивания.

        Args:
            ref_pos (int): Позиция символа в эталонной записи.
            act_pos (int): Позиция символа в фактической записи.
            cmp_type (CompareType): Тип операции выравнивания.

        Returns:
            PhoneticError: Ошибка произношения фонемы.
        """
        return PhoneticMistake(
            reference=Phoneme(position=ref_pos, value=self.reference[ref_pos])
            if cmp_type != CompareType.INSERTION
            else None,
            actual=Phoneme(position=act_pos, value=self.actual[act_pos])
            if cmp_type != CompareType.DELETION
            else None,
            type=cmp_type.value,
        )

    def _check_mistakes(self, sequences_aligment: list[CompareType]) -> None:
        """Выполняет проверку на ошибки произношения,
        используя вектор выравнивания фонетических записей.

        Наличие операции выравнивания, отличной от "Совпадение", явялется
        фонетической ошибкой.

        Args:
            sequences_aligment (list[CompareType]): Вектор операций выравнивания.
        """
        ref_pos = 0
        act_pos = 0

        for compare_type in sequences_aligment:
            if compare_type != CompareType.MATCH:
                error = self._construct_error(ref_pos, act_pos, compare_type)
                self.mistakes.append(error)

            else:
                self.matches += 1

            match compare_type:
                case CompareType.MATCH | CompareType.REPLACEMENT:
                    ref_pos += 1
                    act_pos += 1

                case CompareType.DELETION:
                    ref_pos += 1

                case CompareType.INSERTION:
                    act_pos += 1

    def _сalculate_accuracy(self) -> float:
        """Метод высчитывает точность произношения, путём учета штрафа за отличие
        длины фактического результата от длины эталона.

        Returns:
            float: Точность произношения.
        """
        fine = 1 + abs(len(self.reference) - len(self.actual)) / len(self.reference)
        accuracy = self.matches / (len(self.reference) * fine) * 100

        return round(accuracy, 2)

    def compare(self, format_: Literal["dict", "json"] = "dict") -> Feedback | str:
        """Производит сравнение эталонной и фактической фонетической записи, возвращает
        полный отчёт.

        Args:
            format_ (Literal["dict", "json"], optional): Формат возвращаемых данных.
                Defaults to "dict".

        Returns:
            Feedback | str: Отчет по произношению.
        """
        logger.info("Creating a shift vector for alignment...")
        seq_alignment = self.aligner.get_align()

        logger.info("Mistakes detection...")
        self._check_mistakes(seq_alignment)

        logger.info("Calculating accuracy...")
        accuracy = self._сalculate_accuracy()

        feedback = Feedback(
            accuracy=accuracy,
            mistakes=self.mistakes,
        )

        return feedback if format_ == "dict" else json.dumps(feedback)
