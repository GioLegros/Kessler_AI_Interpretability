from controller import KesslerController
from typing import Dict, Tuple, Any
from immutabledict import immutabledict
import math

class BlackBoxController(KesslerController):
    @property
    def name(self) -> str:
        return "BlackBoxController"

    def actions(self, ship_state: Dict[str, Any], game_state: immutabledict[Any, Any]) -> Tuple[float, float, bool, bool]:
        # Placeholder : va vers le centre et tire
        x, y = ship_state["position"]
        heading = ship_state["heading"]
        dx = 500 - x
        dy = 400 - y
        target_angle = math.degrees(math.atan2(dy, dx))
        turn_rate = (target_angle - heading + 180) % 360 - 180
        return 480.0, turn_rate, True, False