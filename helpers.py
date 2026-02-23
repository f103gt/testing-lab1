from constants import EPSILON, MIN_VALUE, MAX_VALUE
from errors import InputValidationError


def is_zero(value: float) -> bool:
    """
    Перевіряє, чи дорівнює значення нулю з урахуванням точності

    Args:
        value: Число для перевірки

    Returns:
        True, якщо |value| <= EPSILON, інакше False
    """
    return abs(value) <= EPSILON


def validate_input(value: float, param_name: str) -> float:
    """
    Перевіряє, чи належить значення допустимому діапазону

    Args:
        value: Значення для перевірки
        param_name: Назва параметра для повідомлення про помилку

    Raises:
        InputValidationError: Якщо значення поза допустимим діапазоном
    """
    if not (MIN_VALUE <= value <= MAX_VALUE):
        raise InputValidationError(
            message=f"Значення {param_name} повинно бути в діапазоні [{MIN_VALUE}, {MAX_VALUE}]",
            recommendation=f"Будь ласка, введіть {param_name} в межах допустимого діапазону.",
        )


def safe_input_float(prompt: str, param_name: str) -> float:
    """
    Безпечне введення числа з перевіркою на валідність та діапазон

    Args:
        prompt: Текст запиту для користувача
        param_name: Назва параметра для повідомлення про помилку

    Returns:
        Введене число, якщо воно валідне і в межах допустимого діапазону
    """
    while True:
        try:
            user_input = input(prompt)
            value = float(user_input)
            validate_input(value, param_name)
            return value
        except ValueError:
            print(f"ПОМИЛКА: Введено некоректне значення '{user_input}'")
            print(
                f"РЕКОМЕНДАЦІЯ: Введіть ціле або дійсне число (наприклад: 5, -10, 3.14)"
            )
        except InputValidationError as e:
            print(f"ПОМИЛКА: {e.message}")
            print(f"РЕКОМЕНДАЦІЯ: {e.recommendation}")
