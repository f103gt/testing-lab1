# 2,6,6 Дві неспівпадаючі впорядковані пари (x1, y1), (x2, y2), (x1 - x2)2+ (у1 - у2) 2 0, що є координатами двох
# різних точок, через які проходить одна пряма, подана рівнянням (2);
# дві неспівпадаючі впорядковані четвірки (x0i,y0i,ai,bi), ai2 +bi2 0, де (x0i,y0i) – координати точки, через яку
# проходить пряма, подана рівнянням (6), (ai,bi) – її нормальний вектор, i=1,2
# [-147;147]

import sys
from constants import MIN_VALUE, MAX_VALUE
from helpers import is_zero, safe_input_float
from structures import (
    Line,
    line_perpendicular_to_vector,
    are_lines_parallel,
    are_lines_coincident,
    find_intersection,
    line_from_two_points,
)
from errors import InputValidationError, GeometryError


def analyze_three_lines(line1: Line, line2: Line, line3: Line) -> str:
    """
    Аналізує взаємне розміщення трьох прямих на площині

    Args:
        line1, line2, line3: Три прямі для аналізу

    Returns:
        Рядок з описом результату аналізу
    """
    # Спеціальний випадок - всі три прямі ідентичні (вимога 2.б)
    # Уникаємо надлишкових обчислень, якщо всі коефіцієнти однакові
    if line1 == line2 == line3:
        return "Прямі співпадають"
    
    # Перевіряємо попарну паралельність і збіг
    parallel_12 = are_lines_parallel(line1, line2)
    parallel_13 = are_lines_parallel(line1, line3)
    parallel_23 = are_lines_parallel(line2, line3)

    coincident_12 = are_lines_coincident(line1, line2)
    coincident_13 = are_lines_coincident(line1, line3)
    coincident_23 = are_lines_coincident(line2, line3)

    # Випадок 1: Всі три прямі співпадають
    if coincident_12 and coincident_13:
        return "Прямі співпадають"

    # Випадок 2: Дві прямі співпадають, третя паралельна або перетинає
    if coincident_12:
        if parallel_13:  # Третя паралельна до перших двох
            return "Прямі не перетинаються"
        else:  # Третя перетинає перші дві в одній точці
            p = find_intersection(line1, line3)
            return (
                f"Єдина точка перетину прямих (x0, y0), x0 = {p.x:.6f}, y0 = {p.y:.6f}"
            )

    if coincident_13:
        if parallel_12:
            return "Прямі не перетинаються"
        else:
            p = find_intersection(line1, line2)
            return (
                f"Єдина точка перетину прямих (x0, y0), x0 = {p.x:.6f}, y0 = {p.y:.6f}"
            )

    if coincident_23:
        if parallel_12:
            return "Прямі не перетинаються"
        else:
            p = find_intersection(line1, line2)
            return (
                f"Єдина точка перетину прямих (x0, y0), x0 = {p.x:.6f}, y0 = {p.y:.6f}"
            )

    # Випадок 3: Прямі паралельні, але не співпадають
    if parallel_12 and parallel_13:
        return "Прямі не перетинаються"

    if parallel_12 and not parallel_13:
        # Перші дві паралельні, третя їх перетинає
        p1 = find_intersection(line1, line3)
        p2 = find_intersection(line2, line3)
        return f"Дві точки перетину прямих (x1, y1) = {p1}, (x2, y2) = {p2}"

    if parallel_13 and not parallel_12:
        # Перша і третя паралельні, друга їх перетинає
        p1 = find_intersection(line1, line2)
        p2 = find_intersection(line2, line3)
        return f"Дві точки перетину прямих (x1, y1) = {p1}, (x2, y2) = {p2}"

    if parallel_23 and not parallel_12:
        # Друга і третя паралельні, перша їх перетинає
        p1 = find_intersection(line1, line2)
        p2 = find_intersection(line1, line3)
        return f"Дві точки перетину прямих (x1, y1) = {p1}, (x2, y2) = {p2}"

    # Випадок 4 і 5: Жодна пара не паралельна
    # Знаходимо всі три точки перетину
    p12 = find_intersection(line1, line2)
    p13 = find_intersection(line1, line3)
    p23 = find_intersection(line2, line3)

    # Перевіряємо, чи всі три точки співпадають
    if (
        is_zero(p12.x - p13.x)
        and is_zero(p12.y - p13.y)
        and is_zero(p12.x - p23.x)
        and is_zero(p12.y - p23.y)
    ):
        return (
            f"Єдина точка перетину прямих (x0, y0), x0 = {p12.x:.6f}, y0 = {p12.y:.6f}"
        )

    # Три різні точки перетину
    return (
        f"Три точки перетину прямих:\n"
        f"  (x1, y1) = {p12}\n"
        f"  (x2, y2) = {p13}\n"
        f"  (x3, y3) = {p23}"
    )


def input_line1() -> Line:
    """
    Введення параметрів першої прямої (рівняння 2: через дві точки)

    Returns:
        Line: Перша пряма в загальному вигляді
    """
    print("\n" + "=" * 60)
    print("ВВЕДЕННЯ ПАРАМЕТРІВ ПЕРШОЇ ПРЯМОЇ")
    print("Рівняння (2): Пряма через дві точки (x1, y1) і (x2, y2)")
    print("=" * 60)

    x1 = safe_input_float("Задайте x1 (абсциса першої точки): ", "x1")
    y1 = safe_input_float("Задайте y1 (ордината першої точки): ", "y1")
    x2 = safe_input_float("Задайте x2 (абсциса другої точки): ", "x2")
    y2 = safe_input_float("Задайте y2 (ордината другої точки): ", "y2")

    from structures import Point
    p1 = Point(x1, y1)
    p2 = Point(x2, y2)
    return line_from_two_points(p1, p2)


def input_line_perpendicular(line_number: int) -> Line:
    """
    Введення параметрів прямої (рівняння 6: через точку перпендикулярно до вектора)

    Args:
        line_number: Номер прямої (2 або 3)

    Returns:
        Line: Пряма в загальному вигляді
    """
    print("\n" + "=" * 60)
    print(f"ВВЕДЕННЯ ПАРАМЕТРІВ {line_number}-ї ПРЯМОЇ")
    print("Рівняння (6): Пряма через точку (x0, y0) перпендикулярно до вектора (a, b)")
    print("=" * 60)

    x0 = safe_input_float(
        f"Задайте x0 (абсциса точки для прямої {line_number}): ", f"x0_{line_number}"
    )
    y0 = safe_input_float(
        f"Задайте y0 (ордината точки для прямої {line_number}): ", f"y0_{line_number}"
    )
    a = safe_input_float(
        f"Задайте a (перша компонента нормального вектора для прямої {line_number}): ",
        f"a_{line_number}",
    )
    b = safe_input_float(
        f"Задайте b (друга компонента нормального вектора для прямої {line_number}): ",
        f"b_{line_number}",
    )

    from structures import Point
    p0 = Point(x0, y0)
    return line_perpendicular_to_vector(p0, a, b)


def main():
    """
    Головна функція програми
    """
    print("=" * 60)
    print("АНАЛІЗ ВЗАЄМНОГО РОЗМІЩЕННЯ ТРЬОХ ПРЯМИХ НА ПЛОЩИНІ")
    print("Варіант 2,6,6")
    print(f"Допустимий діапазон значень: [{MIN_VALUE}; {MAX_VALUE}]")
    print("=" * 60)

    try:
        # Введення трьох прямих
        line1 = input_line1()
        line2 = input_line_perpendicular(2)
        line3 = input_line_perpendicular(3)

        # Виведення отриманих рівнянь
        print("\n" + "=" * 60)
        print("ОТРИМАНІ РІВНЯННЯ ПРЯМИХ У ЗАГАЛЬНОМУ ВИГЛЯДІ:")
        print("=" * 60)
        print(f"Пряма 1: {line1}")
        print(f"Пряма 2: {line2}")
        print(f"Пряма 3: {line3}")

        # Аналіз взаємного розміщення
        print("\n" + "=" * 60)
        print("РЕЗУЛЬТАТ АНАЛІЗУ:")
        print("=" * 60)
        result = analyze_three_lines(line1, line2, line3)
        print(result)
        print("=" * 60)

    except InputValidationError as e:
        print("\n" + "!" * 60)
        print("ПОМИЛКА ВАЛІДАЦІЇ ВХІДНИХ ДАНИХ")
        print("!" * 60)
        print(f"Опис помилки: {e.message}")
        print(f"Рекомендовані дії: {e.recommendation}")
        print("!" * 60)
        return 1

    except GeometryError as e:
        print("\n" + "!" * 60)
        print("ГЕОМЕТРИЧНА ПОМИЛКА")
        print("!" * 60)
        print(f"Опис помилки: {e.message}")
        print(f"Рекомендовані дії: {e.recommendation}")
        print("!" * 60)
        return 1

    except ZeroDivisionError:
        print("\n" + "!" * 60)
        print("КРИТИЧНА ПОМИЛКА")
        print("!" * 60)
        print("Опис помилки: Спроба ділення на нуль під час обчислень")
        print("Рекомендовані дії: Перевірте коректність введених даних")
        print("!" * 60)
        return 1

    except Exception as e:
        print("\n" + "!" * 60)
        print("НЕПЕРЕДБАЧЕНА ПОМИЛКА")
        print("!" * 60)
        print(f"Опис помилки: {type(e).__name__}: {str(e)}")
        print(
            "Рекомендовані дії: Зверніться до розробника або спробуйте інші вхідні дані"
        )
        print("!" * 60)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
