import pygame
import argparse
import random
import abc
import enum
from typing import List, Iterator, Tuple, TypedDict, final
import re

FPS_MIN = 3
FPS_MAX = 15

# Define a structure for the window size using TypedDict
class WindowSize(TypedDict):
    width: int
    height: int

# Enum to represent directions with (x, y) vector offsets
class Dir(enum.Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

# Abstract base class for Observer pattern
class Observer(abc.ABC):
    def __init__(self) -> None:
        super().__init__()

    # Called when an object is eaten
    def notify_object_eaten(self, obj: 'GameObject') -> None:
        pass

    # Called when an object moves
    def notify_object_moved(self, obj: 'GameObject') -> None:
        pass

    # Called when a collision occurs
    def notify_collision(self, obj: 'GameObject') -> None:
        pass

# Abstract base class for Subject in the Observer pattern
class Subject(abc.ABC):
    def __init__(self) -> None:
        super().__init__()
        self._observers: List[Observer] = []  # List of attached observers

    @property
    def observers(self) -> List[Observer]:
        return self._observers

    # Attach an observer to the subject
    def attach_obs(self, obs: Observer) -> None:
        self._observers.append(obs)

    # Detach an observer from the subject
    def detach_obs(self, obs: Observer) -> None:
        self._observers.remove(obs)

    # Notify all observers of an event
    def notify_observers(self, method_name: str, obj: 'GameObject') -> None:
        for observer in self._observers:
            if hasattr(observer, method_name):
                getattr(observer, method_name)(obj)
            else:
                raise AttributeError(f"Observer does not have method {method_name}")

# Board class, both a Subject and Observer
class Board(Subject, Observer):
    def __init__(self, screen: pygame.Surface, tile_size: int) -> None:
        super().__init__()
        self._screen = screen  # Pygame screen object
        self._tile_size = tile_size  # Size of each tile in pixels
        self._objects: List[GameObject] = []  # List of all game objects on the board

    # Draw all objects on the screen
    def draw(self) -> None:
        for obj in self._objects:
            for tile in obj.tiles:
                tile.draw(self._screen, self._tile_size)

    # Add a game object to the board
    def add_object(self, gameobject: 'GameObject') -> None:
        self._objects.append(gameobject)
        if isinstance(gameobject, Subject):
            gameobject.attach_obs(self)

    # Handle movement notifications
    def notify_object_moved(self, obj: 'GameObject') -> None:
        for other in self._objects:
            if other is not obj:
                # Check if the object's tiles overlap with another object's tiles
                for tile in obj.tiles:
                    if tile in other:
                        if isinstance(other, Fruit):
                            self.notify_object_eaten(other)

    # Handle notifications when an object is eaten
    def notify_object_eaten(self, obj: 'GameObject') -> None:
        if isinstance(obj, Fruit):
            self._objects.remove(obj)
            snake = next((o for o in self._objects if isinstance(o, Snake)), None)
            if snake is None:
                raise ValueError("No Snake object found in the board.")
            snake.grow()
            new_position = (
                random.randint(0, self._screen.get_height() // self._tile_size - 1),
                random.randint(0, self._screen.get_width() // self._tile_size - 1),
            )
            new_fruit = Fruit(new_position, (255, 0, 0))
            self.add_object(new_fruit)

# Abstract base class for game objects
class GameObject(Subject):
    def __init__(self) -> None:
        super().__init__()

    @property
    @abc.abstractmethod
    def tiles(self) -> Iterator['Tile']:
        raise NotImplementedError

    # Check if a tile exists in the object's tiles
    def __contains__(self, tile: 'Tile') -> bool:
        if not isinstance(tile, Tile):
            return False
        return any(t.row == tile.row and t.column == tile.column for t in self.tiles)

# Tile class represents individual cells on the board
class Tile:
    def __init__(self, row: int, column: int, color: Tuple[int, int, int]) -> None:
        self._row = row
        self._column = column
        self._color = color

    @property
    def row(self) -> int:
        return self._row

    @property
    def column(self) -> int:
        return self._column

    # Draw the tile on the screen
    def draw(self, screen: pygame.Surface, tile_size: int) -> None:
        rect = pygame.Rect(self._column * tile_size, self._row * tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self._color, rect)

    # Add a direction to a tile to create a new tile
    def __add__(self, other: Dir) -> 'Tile':
        if not isinstance(other, Dir):
            raise ValueError('Type is wrong')
        return Tile(self._row + other.value[1], self._column + other.value[0], self._color)

# CheckerBoard class represents a checkerboard pattern on the board
class CheckerBoard(GameObject):
    def __init__(self, size: WindowSize, color1: Tuple[int, int, int], color2: Tuple[int, int, int]) -> None:
        super().__init__()
        self._size = size  # Dimensions of the board
        self._color1 = color1  # Primary color
        self._color2 = color2  # Secondary color

    @property
    def tiles(self) -> Iterator[Tile]:
        # Yield tiles with alternating colors
        for row in range(self._size["height"]):
            for column in range(self._size["width"]):
                yield Tile(row=row, column=column, color=self._color1 if (row + column) % 2 == 0 else self._color2)

# Snake class represents the snake in the game
class Snake(GameObject):
    def __init__(self, positions: List[Tuple[int, int]], color: Tuple[int, int, int], direction: Dir) -> None:
        super().__init__()
        self._tiles: List[Tile] = [Tile(p[0], p[1], color) for p in positions]
        self._color: Tuple[int, int, int] = color
        self._direction: Dir = direction

    @property
    def dir(self) -> Dir:
        return self._direction

    @dir.setter
    def dir(self, new_direction: Dir) -> None:
        self._direction = new_direction

    def __len__(self) -> int:
        return len(self._tiles)

    def move(self, width: int, height: int) -> None:
        # Calculate the new head position
        new_head = self._tiles[0] + self._direction

        # Check if the snake slithers on itself
        if any(tile.row == new_head.row and tile.column == new_head.column for tile in self._tiles):
            raise GameOver("The snake slithered on itself.")

        # Check if the snake exits the board
        if not (0 <= new_head.row < height and 0 <= new_head.column < width):
            raise GameOver("The snake exited the board.")

        # Move the snake
        self._tiles.insert(0, new_head)  # Add the new head
        self._tiles.pop()  # Remove the tail
        self.notify_observers("notify_object_moved", self)

    def grow(self) -> None:
        self._tiles.append(self._tiles[-1])

    @property
    def tiles(self) -> Iterator[Tile]:
        return iter(self._tiles)

# Fruit class represents a fruit on the board
class Fruit(GameObject):
    def __init__(self, position: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        super().__init__()
        # Initialize the fruit as a single tile
        self._tiles: List[Tile] = [Tile(row=position[0], column=position[1], color=color)]

    @property
    def tiles(self) -> Iterator[Tile]:
        # Return an iterator over the fruit's tiles
        return iter(self._tiles)

# Function to parse window size from command-line arguments, changer le nom
def windowsize() -> WindowSize:
    DEFAULT_WIDTH = 20
    DEFAULT_HEIGHT = 15
    DEFAULT_TILE_SIZE = 20
    DEFAULT_FPS = 10

    parser = argparse.ArgumentParser(description='Configure game parameters.')
    parser.add_argument('-w', '--width', type=int, default=DEFAULT_WIDTH,
                        help="Width of the game board in tiles (minimum: 20).")
    parser.add_argument('-e', '--height', type=int, default=DEFAULT_HEIGHT,
                        help="Height of the game board in tiles (minimum: 15).")
    parser.add_argument('--tile-size', type=int, default=DEFAULT_TILE_SIZE,
                        help="Size of each tile in pixels (minimum: 10, maximum: 100).")
    parser.add_argument('--fps', type=int, default=DEFAULT_FPS,
                        help="Frames per second (minimum: 3, maximum: 60).")
    parser.add_argument('--fruit-color', type=str, default='#FF0000',
                        help="Hexadecimal color code for the fruit (e.g., #FF0000).")
    parser.add_argument('--gameover-on-exit', action='store_true',
                        help="End the game if the snake exits the board.")
    args = parser.parse_args()

    # Validate arguments
    if args.width < 20:
        raise IntRangeError("width", args.width, 20, float('inf'))
    if args.height < 15:
        raise IntRangeError("height", args.height, 15, float('inf'))
    if not (10 <= args.tile_size <= 100):
        raise IntRangeError("tile-size", args.tile_size, 10, 100)
    if not (3 <= args.fps <= 60):
        raise IntRangeError("fps", args.fps, 3, 60)
    if not re.match(r'^#[0-9A-Fa-f]{6}$', args.fruit_color):
        raise ColorError(args.fruit_color, "fruit-color")

    return {
        "width": args.width,
        "height": args.height,
        "tile_size": args.tile_size,
        "fps": args.fps,
        "fruit_color": args.fruit_color,
        "gameover_on_exit": args.gameover_on_exit
    }




class SnakeException(Exception):
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

class GameOver(SnakeException):
    def __init__(self, message : str)-> None:
        super().__init__(message)





# Main game function
def game() -> None:
    DEFAULT_STARTING_SNAKE = [(10, 7), (10, 6), (10, 5)]
    DEFAULT_DIRECTION = Dir.RIGHT

    # Initialize the game window
    args = {
        "width": 20,
        "height": 15,
        "tile_size": 20,
        "fps": 10,
        "fruit_color": (255, 0, 0),
    }

    pygame.init()
    try:
        screen = pygame.display.set_mode(
            (args["width"] * args["tile_size"], args["height"] * args["tile_size"])
        )
        clock = pygame.time.Clock()
        pygame.display.set_caption("Snake - score : 0")

        board = Board(screen=screen, tile_size=args["tile_size"])
        checkerboard = CheckerBoard(
            {"width": args["width"], "height": args["height"]},
            (0, 0, 0), (255, 255, 255)
        )
        snake = Snake(DEFAULT_STARTING_SNAKE, (0, 255, 0), DEFAULT_DIRECTION)
        fruit = Fruit((3, 3), args["fruit_color"])
        board.add_object(checkerboard)
        board.add_object(snake)
        board.add_object(fruit)

        game_running = True
        while game_running:
            clock.tick(args["fps"])

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and snake.dir != Dir.DOWN:
                        snake.dir = Dir.UP
                    elif event.key == pygame.K_DOWN and snake.dir != Dir.UP:
                        snake.dir = Dir.DOWN
                    elif event.key == pygame.K_RIGHT and snake.dir != Dir.LEFT:
                        snake.dir = Dir.RIGHT
                    elif event.key == pygame.K_LEFT and snake.dir != Dir.RIGHT:
                        snake.dir = Dir.LEFT

            try:
                snake.move(args["width"], args["height"])
                board.draw()
                pygame.display.set_caption(f"Snake - score : {len(snake) - 3}")
                pygame.display.update()
            except GameOver as e:
                print(e)  # Print "Game Over" message
                game_running = False
    finally:
        pygame.quit()
        print("Game Over!")