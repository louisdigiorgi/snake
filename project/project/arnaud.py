import pygame
import argparse
import random
import abc
import enum

class Dir(enum.Enum):
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)

class Observer(abc.ABC):

    def __init__(self) -> None:
        super().__init__()

    def notify_object_eaten(self, obj: 'GameObject') -> None:
        pass

    def notify_object_moved(self, obj: 'GameObject') -> None:
        pass

    def notify_collision(self, obj: 'GameObject') -> None:
        pass

class Subject(abc.ABC):

    def __init__(self) -> None:
        super().__init__()
        self._observers: list[Observer] = []

    @property
    def observers(self) -> list[Observer]:
        return self._observers

    def attach_obs(self, obs: Observer) -> None:
        self._observers.append(obs)

    def detach_obs(self, obs: Observer) -> None:
        self._observers.remove(obs)

    def notify_observers(self, method_name: str, obj: 'GameObject') -> None:
        for observer in self._observers:
            getattr(observer, method_name)(obj)

class Board(Subject, Observer):

    def __init__(self, screen, tile_size):
        super().__init__()
        self._screen = screen
        self._tile_size = tile_size
        self._objects = []

    def draw(self):
        for obj in self._objects:
            for tile in obj.tiles:
                tile.draw(self._screen, self._tile_size)

    def add_object(self, gameobject):
        self._objects.append(gameobject)
        if isinstance(gameobject, Subject):
            gameobject.attach_obs(self)

    def notify_object_moved(self, obj):
        for other in self._objects:
            if other is not obj and obj in other:
                if isinstance(other, Fruit):
                    self.notify_object_eaten(other)

    def notify_object_eaten(self, obj):
        if isinstance(obj, Fruit):
            self._objects.remove(obj)
            snake = next(o for o in self._objects if isinstance(o, Snake))
            snake.grow()
            new_position = (random.randint(0, self._screen.get_height() // self._tile_size - 1),
                            random.randint(0, self._screen.get_width() // self._tile_size - 1))
            new_fruit = Fruit(new_position, (255, 0, 0))
            self.add_object(new_fruit)

class GameObject(Subject):

    def __init__(self):
        super().__init__()

    @property
    @abc.abstractmethod
    def tiles(self):
        raise NotImplementedError

    def __contains__(self, tile):
        return any(t._row == tile._row and t._column == tile._column for t in self.tiles)

class Tile:

    def __init__(self, row, column, color):
        self._row = row
        self._column = column
        self._color = color

    def draw(self, screen, tile_size):
        rect = pygame.Rect(self._column * tile_size, self._row * tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self._color, rect)

    def __add__(self, other):
        if not isinstance(other, Dir):
            raise ValueError('Type is wrong')
        return Tile(self._row + other.value[1], self._column + other.value[0], self._color)

class CheckerBoard(GameObject):

    def __init__(self, size, color1, color2):
        super().__init__()
        self._size = size
        self._color1 = color1
        self._color2 = color2

    @property
    def tiles(self):
        for row in range(self._size.height):
            for column in range(self._size.width):
                yield Tile(row=row, column=column, color=self._color1 if (row + column) % 2 == 0 else self._color2)

class Snake(GameObject):

    def __init__(self, positions, color, direction):
        super().__init__()
        self._tiles = [Tile(p[0], p[1], color) for p in positions]
        self._color = color
        self._direction = direction

    @property
    def dir(self):
        return self._direction

    @dir.setter
    def dir(self, new_direction):
        self._direction = new_direction

    def __len__(self):
        return len(self._tiles)

    def move(self):
        self._tiles.insert(0, self._tiles[0] + self._direction)
        self._tiles.pop()
        self.notify_observers("notify_object_moved", self)

    def grow(self):
        self._tiles.append(self._tiles[-1])

    @property
    def tiles(self):
        return iter(self._tiles)

class Fruit(GameObject):

    def __init__(self, position, color):
        super().__init__()
        self._tiles = [Tile(row=position[0], column=position[1], color=color)]

    @property
    def tiles(self):
        return iter(self._tiles)

def windowsize():
    DEFAULT_WIDTH = 20
    DEFAULT_HEIGHT = 15

    parser = argparse.ArgumentParser(description='Window size with numbers of tiles.')
    parser.add_argument('-w', '--width', type=int, default=DEFAULT_WIDTH, help="Width in tiles.")
    parser.add_argument('-e', '--height', type=int, default=DEFAULT_HEIGHT, help="Height in tiles.")
    args = parser.parse_args()

    return args

def game():
    DEFAULT_TILE_SIZE = 20
    DEFAULT_STARTING_SNAKE = [(10, 7), (10, 6), (10, 5)]
    DEFAULT_DIRECTION = Dir.RIGHT

    size = windowsize()
    pygame.init()
    screen = pygame.display.set_mode((size.width * DEFAULT_TILE_SIZE, size.height * DEFAULT_TILE_SIZE))
    clock = pygame.time.Clock()
    pygame.display.set_caption("Snake - score : 0")

    board = Board(screen=screen, tile_size=DEFAULT_TILE_SIZE)

    checkerboard = CheckerBoard(size, (0, 0, 0), (255, 255, 255))
    snake = Snake(DEFAULT_STARTING_SNAKE, (0, 255, 0), DEFAULT_DIRECTION)
    fruit = Fruit((3, 3), (255, 0, 0))
    board.add_object(checkerboard)
    board.add_object(snake)
    board.add_object(fruit)

    game_running = True

    while game_running:
        clock.tick(5)

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                game_running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_running = False

                if event.key == pygame.K_UP:
                    snake.dir = Dir.UP
                elif event.key == pygame.K_DOWN:
                    snake.dir = Dir.DOWN
                elif event.key == pygame.K_RIGHT:
                    snake.dir = Dir.RIGHT
                elif event.key == pygame.K_LEFT:
                    snake.dir = Dir.LEFT

        snake.move()
        board.draw()
        pygame.display.set_caption(f"Snake - score : {len(snake) - 3}")
        pygame.display.update()

    pygame.quit()
    quit(0)
