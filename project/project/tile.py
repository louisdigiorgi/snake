from typing import Tuple
import pygame

class Tile:
    def __init__(self, row: int, column: int, color: Tuple[int, int, int]):
        self.row = row
        self.column = column
        self.color = color

    def draw(self, screen, tile_size):
        rect = pygame.Rect(self.column * tile_size, self.row * tile_size, tile_size, tile_size)
        pygame.draw.rect(screen, self.color, rect)
