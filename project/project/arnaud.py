import pygame
import argparse
import random
import abc
import enum
from typing import List, Iterator, Tuple, TypedDict, final

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
@final
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
        # Initialize the snake's body as a list of tiles
        self._tiles: List[Tile] = [Tile(p[0], p[1], color) for p in positions]
        self._color: Tuple[int, int, int] = color  # Snake's color
        self._direction: Dir = direction  # Snake's initial direction

    @property
    def dir(self) -> Dir:
        # Get the current direction of the snake
        return self._direction

    @dir.setter
    def dir(self, new_direction: Dir) -> None:
        # Set the new direction for the snake
        self._direction = new_direction

    def __len__(self) -> int:
        # Return the length of the snake (number of tiles)
        return len(self._tiles)

    def move(self) -> None:
        # Move the snake in the current direction
        self._tiles.insert(0, self._tiles[0] + self._direction)  # Add a new head
        self._tiles.pop()  # Remove the tail
        self.notify_observers("notify_object_moved", self)  # Notify observers about the move

    def grow(self) -> None:
        # Grow the snake by adding a tile at the tail
        self._tiles.append(self._tiles[-1])

    @property
    def tiles(self) -> Iterator[Tile]:
        # Return an iterator over the snake's tiles
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

# Function to parse window size from command-line arguments
def windowsize() -> WindowSize:
    DEFAULT_WIDTH = 20  # Default width in tiles
    DEFAULT_HEIGHT = 15  # Default height in tiles

    parser = argparse.ArgumentParser(description='Window size with numbers of tiles.')
    parser.add_argument('-w', '--width', type=int, default=DEFAULT_WIDTH, help="Width in tiles.")
    parser.add_argument('-e', '--height', type=int, default=DEFAULT_HEIGHT, help="Height in tiles.")
    args = parser.parse_args()

    return {"width": args.width, "height": args.height}

# Main game function
def game() -> None:
    DEFAULT_TILE_SIZE = 20  # Size of each tile in pixels
    DEFAULT_STARTING_SNAKE = [(10, 7), (10, 6), (10, 5)]  # Initial snake position
    DEFAULT_DIRECTION = Dir.RIGHT  # Initial snake direction

    # Initialize the game window
    size = windowsize()
    pygame.init()
    screen = pygame.display.set_mode((size["width"] * DEFAULT_TILE_SIZE, size["height"] * DEFAULT_TILE_SIZE))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake - score : 0")

    # Create game objects
    board = Board(screen=screen, tile_size=DEFAULT_TILE_SIZE)
    checkerboard = CheckerBoard(size, (0, 0, 0), (255, 255, 255))
    snake = Snake(DEFAULT_STARTING_SNAKE, (0, 255, 0), DEFAULT_DIRECTION)
    fruit = Fruit((3, 3), (255, 0, 0))
    board.add_object(checkerboard)
    board.add_object(snake)
    board.add_object(fruit)

    # Main game loop
    game_running = True
    while game_running:
        clock.tick(5)  # Control game speed (frames per second)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_running = False

                # Change the snake's direction based on arrow keys
                elif event.key == pygame.K_UP and snake.dir != Dir.DOWN:
                    snake.dir = Dir.UP
                elif event.key == pygame.K_DOWN and snake.dir != Dir.UP:
                    snake.dir = Dir.DOWN
                elif event.key == pygame.K_RIGHT and snake.dir != Dir.LEFT:
                    snake.dir = Dir.RIGHT
                elif event.key == pygame.K_LEFT and snake.dir != Dir.RIGHT:
                    snake.dir = Dir.LEFT

        # Update game state
        snake.move()
        board.draw()
        pygame.display.set_caption(f"Snake - score : {len(snake) - 3}")  # Update score
        pygame.display.update()

    # Cleanup and exit
    pygame.quit()
    import sys
    sys.exit(0)
