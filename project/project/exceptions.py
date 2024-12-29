class SnakeException(Exception):
    pass

class GameOver(SnakeException):
    def __init__(self, message: str) -> None:
        super().__init__(message)