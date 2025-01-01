from typing import List
from .observer import Subject, Observer
from .tile import Tile
from .fruit import Fruit
from .snake import Snake
import pygame
import random


class Board(Subject, Observer):
    def __init__(self, screen: pygame.Surface, tile_size: int) -> None:
        super().__init__()
        self._screen = screen
        self._tile_size = tile_size
        self._objects: List = []

    def draw(self) -> None:
        for obj in self._objects:
            for tile in obj.tiles:
                tile.draw(self._screen, self._tile_size)

    def add_object(self, gameobject) -> None:
        self._objects.append(gameobject)
        if isinstance(gameobject, Subject):
            gameobject.attach_obs(self)

    def notify_object_moved(self, obj) -> None:
        for other in self._objects:
            if other is not obj:
                for tile in obj.tiles:
                    if tile in other.tiles:
                        if isinstance(other, Fruit):
                            self.notify_object_eaten(other)

    def notify_object_eaten(self, obj) -> None:
        if isinstance(obj, Fruit):
            self._objects.remove(obj)
            snake = next((o for o in self._objects if isinstance(o, Snake)), None)
            if snake:
                snake.grow()
            while True:
                new_position = (
                    random.randint(0, self._screen.get_height() // self._tile_size - 1),
                    random.randint(0, self._screen.get_width() // self._tile_size - 1),
                )
                if all(new_position != (tile.row, tile.column) for obj in self._objects for tile in obj.tiles):
                    break
            new_fruit = Fruit(new_position, (255, 0, 0))
            self.add_object(new_fruit)



class CheckerBoard(Subject):
    def __init__(self, size, color1, color2) -> None:
        super().__init__()
        self._size = size
        self._color1 = color1
        self._color2 = color2

    @property
    def tiles(self):
        for row in range(self._size["height"]):
            for column in range(self._size["width"]):
                yield Tile(
                    row=row,
                    column=column,
                    color=self._color1 if (row + column) % 2 == 0 else self._color2,
                )
