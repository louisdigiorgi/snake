from .direction import Dir
from typing import Tuple
import pygame


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
