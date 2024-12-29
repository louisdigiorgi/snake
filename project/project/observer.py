from abc import ABC
from typing import List

class Observer(ABC):
    def notify_object_eaten(self, obj) -> None:
        pass

    def notify_object_moved(self, obj) -> None:
        pass

class Subject(ABC):
    def __init__(self) -> None:
        self._observers: List[Observer] = []

    def attach_obs(self, obs: Observer) -> None:
        self._observers.append(obs)

    def detach_obs(self, obs: Observer) -> None:
        self._observers.remove(obs)

    def notify_observers(self, method_name: str, obj) -> None:
        for observer in self._observers:
            getattr(observer, method_name)(obj)
