from controller import KesslerController
from typing import Dict, Tuple, Any
from immutabledict import immutabledict
import math

class GlassBoxController(KesslerController):
    @property
    def name(self) -> str:
        return "GlassBoxController"

    def actions(self, ship_state: Dict[str, Any], game_state: immutabledict[Any, Any]) -> Tuple[float, float, bool, bool]:
        # Fuit l'astéroïde le plus proche
        pos = ship_state["position"]
        heading = ship_state["heading"]
        closest = None
        min_dist = float("inf")
        for asteroid in game_state["asteroids"]:
            dist = math.dist(pos, asteroid["position"])
            if dist < min_dist:
                min_dist = dist
                closest = asteroid

        if not closest:
            return 0.0, 0.0, False, False

        # Calcul direction opposée à l'astéroïde
        dx = pos[0] - closest["position"][0]
        dy = pos[1] - closest["position"][1]
        angle_to_away = math.degrees(math.atan2(dy, dx))
        turn_rate = angle_to_away - heading
        turn_rate = (turn_rate + 180) % 360 - 180  # normalise entre -180 et 180

        return 480.0, turn_rate, False, False