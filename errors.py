class InputValidationError(Exception):
    """Виняток для помилок валідації вхідних даних"""

    def __init__(self, message: str, recommendation: str):
        self.message = message
        self.recommendation = recommendation
        super().__init__(self.message)


class GeometryError(Exception):
    """Виняток для геометричних помилок"""

    def __init__(self, message: str, recommendation: str):
        self.message = message
        self.recommendation = recommendation
        super().__init__(self.message)