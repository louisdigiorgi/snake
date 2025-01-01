from typing import Tuple, Iterator, List
from .tile import Tile
from .game_object import GameObject  # Import GameObject correctly

class Fruit(GameObject):
    def __init__(self, position: Tuple[int, int], color: Tuple[int, int, int]) -> None:
        super().__init__()
        # Initialize the fruit as a single tile
        self._tiles: List[Tile] = [Tile(row=position[0], column=position[1], color=color)]

    @property
    def tiles(self) -> Iterator[Tile]:
        # Return an iterator over the fruit's tiles
        return iter(self._tiles)
