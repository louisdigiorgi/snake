from .tile import Tile
from .direction import Dir
from .exceptions import GameOver
from typing import List, Tuple, Iterator

class Snake:
    def __init__(self, positions: List[Tuple[int, int]], color: Tuple[int, int, int], direction: Dir) -> None:
        self._tiles = [Tile(p[0], p[1], color) for p in positions]
        self._color = color
        self._direction = direction

    @property
    def dir(self) -> Dir:
        return self._direction

    @dir.setter
    def dir(self, new_direction: Dir) -> None:
        self._direction = new_direction

    def move(self, width: int, height: int) -> None:
        new_head = self._tiles[0] + self._direction
        if any(tile.row == new_head.row and tile.column == new_head.column for tile in self._tiles):
            raise GameOver("The snake slithered on itself.")
        if not (0 <= new_head.row < height and 0 <= new_head.column < width):
            raise GameOver("The snake exited the board.")
        self._tiles.insert(0, new_head)
        self._tiles.pop()

    def grow(self) -> None:
        self._tiles.append(self._tiles[-1])

    @property
    def tiles(self) -> Iterator[Tile]:
        return iter(self._tiles)
