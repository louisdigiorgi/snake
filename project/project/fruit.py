from .tile import Tile
from typing import Tuple

class Fruit:
    def __init__(self, position: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        self._tile = Tile(position[0], position[1], color)

    @property
    def tiles(self):
        return [self._tile]
