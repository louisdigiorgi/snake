from typing import List, Tuple, Iterator
from .observer import Subject, Observer
from .tile import Tile
from .fruit import Fruit
from .game_object import GameObject  # Import GameObject correctly
from .snake import Snake
from .utils import WindowSize  # Import WindowSize from utils
import pygame
import random


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
