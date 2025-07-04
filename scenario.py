from typing import List, Tuple, Dict, Any, Optional
import random
from .ship import Ship
from .asteroid import Asteroid

class Scenario:
    def __init__(self, name: str = "Unnamed", num_asteroids: int = 0, asteroid_states: Optional[List[Dict[str, Any]]] = None,
                 ship_states: Optional[List[Dict[str, Any]]] = None, map_size: Optional[Tuple[int, int]] = None, seed: Optional[int] = None,
                 time_limit: float = float("inf"), ammo_limit_multiplier: float = 0.0, stop_if_no_ammo: bool = False) -> None:
        self._name: Optional[str] = None
        self.name = name
        self.map_size = map_size if map_size else (1000, 800)
        self.ship_states = ship_states if ship_states else [{"position": (self.map_size[0]/2, self.map_size[1]/2)}]
        self.time_limit = time_limit
        self.seed = seed
        self.asteroid_states = list()

        if ammo_limit_multiplier < 0:
            raise ValueError("Ammo limit multiplier must be >= 0.")
        else:
            self._ammo_limit_multiplier = ammo_limit_multiplier

        if ammo_limit_multiplier and stop_if_no_ammo:
            self.stop_if_no_ammo = True
        elif not ammo_limit_multiplier and stop_if_no_ammo:
            self.stop_if_no_ammo = False
            raise ValueError("Cannot enforce no ammo stopping condition because ammo is unlimited")
        else:
            self.stop_if_no_ammo = False

        if num_asteroids and asteroid_states:
            raise ValueError("Both `num_asteroids` and `asteroid_states` are specified.")
        elif asteroid_states:
            self.asteroid_states = asteroid_states
        elif num_asteroids:
            self.asteroid_states = [dict() for _ in range(num_asteroids)]
        else:
            raise (ValueError("Define `num_asteroids` or `asteroid_states`."))

    @property
    def name(self) -> None | str:
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = str(name)

    @property
    def num_starting_asteroids(self) -> float:
        return len(self.asteroid_states)

    @property
    def is_random(self) -> bool:
        return not all(state for state in self.asteroid_states) if self.asteroid_states else True

    @property
    def max_asteroids(self) -> int:
        return sum([Scenario.count_asteroids(asteroid.size) for asteroid in self.asteroids()])

    @property
    def bullet_limit(self) -> int:
        if self._ammo_limit_multiplier:
            temp = round(self.max_asteroids * self._ammo_limit_multiplier)
            return temp if temp > 0 else 1
        else:
            return -1

    @staticmethod
    def count_asteroids(asteroid_size: int) -> int:
        return sum([3 ** (size - 1) for size in range(1, asteroid_size + 1)])

    def asteroids(self) -> List[Asteroid]:
        asteroids = []
        if self.seed is not None:
            random.seed(self.seed)
        for asteroid_state in self.asteroid_states:
            if asteroid_state:
                asteroids.append(Asteroid(**asteroid_state))
            else:
                asteroids.append(Asteroid(
                    position=(random.randrange(0, self.map_size[0]),
                              random.randrange(0, self.map_size[1])),
                ))
        return asteroids

    def ships(self) -> List[Ship]:
        return [Ship(idx, bullets_remaining=self.bullet_limit, **ship_state) for idx, ship_state in enumerate(self.ship_states)]
