from abc import ABC  # Correct import for abstract base classes
from typing import List


class Observer(ABC):
    def __init__(self) -> None:
        super().__init__()

    # Called when an object is eaten
    def notify_object_eaten(self, obj: 'GameObject') -> None:
        pass

    # Called when an object moves
    def notify_object_moved(self, obj: 'GameObject') -> None:
        pass

    # Called when a collision occurs
    def notify_collision(self, obj: 'GameObject') -> None:
        pass


class Subject(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._observers: List[Observer] = []  # List of attached observers

    @property
    def observers(self) -> List[Observer]:
        return self._observers

    # Attach an observer to the subject
    def attach_obs(self, obs: Observer) -> None:
        self._observers.append(obs)

    # Detach an observer from the subject
    def detach_obs(self, obs: Observer) -> None:
        self._observers.remove(obs)

    # Notify all observers of an event
    def notify_observers(self, method_name: str, obj: 'GameObject') -> None:
        for observer in self._observers:
            if hasattr(observer, method_name):
                getattr(observer, method_name)(obj)
            else:
                raise AttributeError(f"Observer does not have method {method_name}")
