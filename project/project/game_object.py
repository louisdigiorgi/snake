from .observer import Subject
from .tile import Tile  # Import Tile correctly
from abc import ABC, abstractmethod  # Import ABC and abstractmethod correctly
from typing import Iterator

class GameObject(Subject):
    def __init__(self) -> None:
        super().__init__()

    @property
    @abstractmethod  # Use the correct abstractmethod decorator from abc
    def tiles(self) -> Iterator['Tile']:
        raise NotImplementedError

    # Check if a tile exists in the object's tiles
    def __contains__(self, tile: 'Tile') -> bool:
        if not isinstance(tile, Tile):
            return False
        return any(t.row == tile.row and t.column == tile.column for t in self.tiles)
