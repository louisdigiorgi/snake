class SnakeException(Exception):
    def __init__(self, message : str)-> None:
        super().__init__(message)

class GameOver(SnakeException):
    def __init__(self, message : str)-> None:
        super().__init__(message)

class SnakeError(SnakeException):
    def __init__(self, message : str)-> None:
        super().__init__(message)

class IntRangeError(SnakeError):
    def __init__(self, name : str, value : int, Vmin : int, Vmax : int)-> None:
        super().__init__(f"Value {value} of {name} is not between {Vmin} and {Vmax}.")

class ColorError(SnakeError):
    def __init__(self, color : str, name : str)-> None:
        super().__init__(f'wrong color {color} for {name}')