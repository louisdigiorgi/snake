class SnakeException(Exception):
    pass


class GameOver(SnakeException):
    pass


class IntRangeError(SnakeException):
    def __init__(self, name: str, value: int, Vmin: int, Vmax: int) -> None:
        super().__init__(f"Value {value} of {name} is not between {Vmin} and {Vmax}.")


class ColorError(SnakeException):
    def __init__(self, color: str, name: str) -> None:
        super().__init__(f"Wrong color {color} for {name}")
