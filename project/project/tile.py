from typing import Tuple
import pygame

class Tile:
    def __init__(self, row: int, column: int, color: Tuple[int, int, int]) -> None:
        self.row = row
        self.column = column
        self.color = color

    def draw(self, screen: pygame.Surface, tile_size: int) -> None:
        rect = pygame.Rect(self.column * tile_size, self.row * tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self.color, rect)

    def __add__(self, other) -> "Tile":
        return Tile(self.row + other.value[1], self.column + other.value[0], self.color)
