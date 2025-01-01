from typing import List, Tuple, Iterator
from .tile import Tile
from .direction import Dir
from .exceptions import GameOver
from .game_object import GameObject  # Import GameObject correctly


class Snake(GameObject):
    def __init__(self, positions: List[Tuple[int, int]], color: Tuple[int, int, int], direction: Dir) -> None:
        super().__init__()
        self._tiles: List[Tile] = [Tile(p[0], p[1], color) for p in positions]
        self._color: Tuple[int, int, int] = color
        self._direction: Dir = direction

    @property
    def dir(self) -> Dir:
        return self._direction

    @dir.setter
    def dir(self, new_direction: Dir) -> None:
        self._direction = new_direction

    def __len__(self) -> int:
        return len(self._tiles)

    def move(self, width: int, height: int) -> None:
        # Calculate the new head position
        new_head = self._tiles[0] + self._direction

        # Check if the snake slithers on itself
        if any(tile.row == new_head.row and tile.column == new_head.column for tile in self._tiles):
            raise GameOver("The snake slithered on itself.")

        # Check if the snake exits the board
        if not (0 <= new_head.row < height and 0 <= new_head.column < width):
            raise GameOver("The snake exited the board.")

        # Move the snake
        self._tiles.insert(0, new_head)  # Add the new head
        self._tiles.pop()  # Remove the tail
        self.notify_observers("notify_object_moved", self)

    def grow(self) -> None:
        self._tiles.append(self._tiles[-1])

    @property
    def tiles(self) -> Iterator[Tile]:
        return iter(self._tiles)
