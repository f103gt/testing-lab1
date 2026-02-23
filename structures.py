from dataclasses import dataclass
from helpers import is_zero
from typing import Optional
from errors import GeometryError


@dataclass
class Point:
    """Клас для представлення точки на площині"""

    x: float
    y: float

    def __str__(self):
        return f"({self.x:.6f}, {self.y:.6f})"

    def __sub__(self, other):
        """Віднімання двох точок для отримання вектора"""
        return Point(self.x - other.x, self.y - other.y)


@dataclass
class Line:
    """Клас для представлення прямої в загальному вигляді Ax + By + C = 0"""

    A: float
    B: float
    C: float

    def __str__(self):
        return f"{self.A:.6f}x + {self.B:.6f}y + {self.C:.6f} = 0"
    
    def __eq__(self, other):
        """Перевірка чи дві прямі ідентичні (однакові коефіцієнти)"""
        if not isinstance(other, Line):
            return False
        return (is_zero(self.A - other.A) and 
                is_zero(self.B - other.B) and 
                is_zero(self.C - other.C))



def line_from_two_points(p1: Point, p2: Point) -> Line:
    """
    Перетворює пряму з рівняння (2) у загальний вигляд Ax + By + C = 0
    Рівняння (2): (x - x1)/(x2 - x1) = (y - y1)/(y2 - y1)

    Args:
        p1: Перша точка
        p2: Друга точка

    Returns:
        Line: Пряма в загальному вигляді

    Raises:
        GeometryError: Якщо точки співпадають
    """
    # Перевіряємо, чи точки не співпадають
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    distance_squared = dx * dx + dy * dy
    
    if is_zero(distance_squared):
        raise GeometryError(
            message="Точки співпадають, неможливо визначити пряму",
            recommendation="Будь ласка, введіть дві різні точки для визначення прямої.",
        )

    # Перетворення до загального вигляду:
    # (x - x1)(y2 - y1) - (y - y1)(x2 - x1) = 0
    # x(y2 - y1) - y(x2 - x1) - x1(y2 - y1) + y1(x2 - x1) = 0
    # A = y2 - y1
    # B = x1 - x2
    # C = y1*x2 - y2*x1

    A = p2.y - p1.y
    B = p1.x - p2.x
    C = p1.y * p2.x - p2.y * p1.x

    return Line(A, B, C)


def line_perpendicular_to_vector(p0: Point, a: float, b: float) -> Line:
    """
    Перетворює пряму з рівняння (6) у загальний вигляд Ax + By + C = 0
    Рівняння (6): a(x - x0) + b(y - y0) = 0

    Args:
        p0: Точка, через яку проходить пряма
        a, b: Компоненти нормального вектора

    Returns:
        Line: Пряма в загальному вигляді

    Raises:
        GeometryError: Якщо вектор нульовий
    """
    # Перевірка: вектор не може бути нульовим
    if is_zero(a) and is_zero(b):
        raise GeometryError(
            f"Нормальний вектор ({a}, {b}) є нульовим, пряму неможливо визначити",
            "Введіть ненульовий вектор (принаймні одна з компонент a або b не дорівнює нулю)",
        )

    # Перетворення до загального вигляду:
    # a(x - x0) + b(y - y0) = 0
    # ax - ax0 + by - by0 = 0
    # ax + by - ax0 - by0 = 0
    # A = a
    # B = b
    # C = -a*x0 - b*y0
    A = a
    B = b
    C = -a * p0.x - b * p0.y

    return Line(A, B, C)


def are_lines_parallel(line1: Line, line2: Line) -> bool:
    """
    Перевіряє, чи є дві прямі паралельними
    Умова паралельності: A1*B2 - A2*B1 = 0

    Args:
        line1, line2: Прямі для перевірки

    Returns:
        True, якщо прямі паралельні (включаючи збіг), інакше False
    """
    determinant = line1.A * line2.B - line2.A * line1.B
    return is_zero(determinant)


def are_lines_coincident(line1: Line, line2: Line) -> bool:
    """
    Перевіряє, чи співпадають дві прямі
    Умова збігу: A1/A2 = B1/B2 = C1/C2 (за умови паралельності)

    Args:
        line1, line2: Прямі для перевірки

    Returns:
        True, якщо прямі співпадають, інакше False
    """
    if not are_lines_parallel(line1, line2):
        return False

    # Перевірка пропорційності коефіцієнтів
    # Знаходимо ненульовий коефіцієнт для визначення пропорції
    if not is_zero(line1.A):
        ratio_A = line1.A / line2.A
        return is_zero(line1.B - ratio_A * line2.B) and is_zero(
            line1.C - ratio_A * line2.C
        )
    elif not is_zero(line1.B):
        ratio_B = line1.B / line2.B
        return is_zero(line1.A - ratio_B * line2.A) and is_zero(
            line1.C - ratio_B * line2.C
        )
    else:
        # Якщо A і B обох ліній нульові, перевіряємо C
        return is_zero(line1.C) and is_zero(line2.C)


def find_intersection(line1: Line, line2: Line) -> Optional[Point]:
    """
    Знаходить точку перетину двох прямих за формулами Крамера

    Args:
        line1, line2: Прямі для знаходження перетину

    Returns:
        Point з координатами перетину або None, якщо прямі паралельні
    """
    # Обчислюємо визначник системи
    det = line1.A * line2.B - line2.A * line1.B

    if is_zero(det):
        # Прямі паралельні або співпадають
        return None

    # Формули Крамера для системи:
    # A1*x + B1*y = -C1
    # A2*x + B2*y = -C2
    # x = (-C1*B2 + C2*B1) / det = (C2*B1 - C1*B2) / det
    # y = (A1*(-C2) - A2*(-C1)) / det = (A2*C1 - A1*C2) / det
    x = -(line1.C * line2.B - line2.C * line1.B) / det
    y = -(line1.A * line2.C - line2.A * line1.C) / det

    return Point(x, y)
