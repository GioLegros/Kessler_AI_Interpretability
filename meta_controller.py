from controller import KesslerController
from typing import Dict, Tuple, Any, List
from immutabledict import immutabledict
import math

class MetaController(KesslerController):
    def __init__(self, glass_controllers: List[KesslerController], black_controllers: List[KesslerController]):
        self.glass_controllers = glass_controllers
        self.black_controllers = black_controllers
        self.ship_states: Dict[int, Any] = {}
        self._last_actions: Dict[int, Tuple[float, float, bool, bool]] = {}
        self.game_state: immutabledict[Any, Any] = {}

    @property
    def name(self):
        return "MetaController"

    def actions(self, ship_state: Dict[str, Any], game_state: immutabledict[Any, Any]) -> Tuple[float, float, bool, bool]:
        idx = ship_state["id"]
        self.ship_states[idx] = ship_state
        self.game_state = game_state

        if len(self.ship_states) == len(self.glass_controllers):
            self._last_actions = self.compute_actions()
            self.ship_states.clear()

        return self._last_actions.get(idx, (0.0, 0.0, False, False))

    def compute_actions(self) -> Dict[int, Tuple[float, float, bool, bool]]:
        scores = {}
        for i, ship in self.ship_states.items():
            pos = ship["position"]
            closest = min(
                (self._distance(pos, ast["position"]) for ast in self.game_state["asteroids"]),
                default=9999
            )
            scores[i] = closest

        # Choisir les 2 ships les plus proches d'un astéroïde
        danger_ids = sorted(scores, key=scores.get)[:2]

        actions = {}
        for i, ship in self.ship_states.items():
            if i >= len(self.glass_controllers):
                print(f"[⚠️] ship.id={i} hors limites du nombre de contrôleurs !")
                continue
            ctrl = self.black_controllers[i] if i in danger_ids else self.glass_controllers[i]
            actions[i] = ctrl.actions(ship, self.game_state)

        return actions

    def _distance(self, p1, p2):
        dx = p1[0] - p2[0]
        dy = p1[1] - p2[1]
        return math.hypot(dx, dy)
