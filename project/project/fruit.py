from typing import Tuple, Iterator
from .tile import Tile

class Fruit:
    def __init__(self, position: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        self._tiles = [Tile(row=position[0], column=position[1], color=color)]

    @property
    def tiles(self) -> Iterator[Tile]:
        return iter(self._tiles)

    def __repr__(self):
        return f"Fruit(position=({self._tiles[0].row}, {self._tiles[0].column}))"

