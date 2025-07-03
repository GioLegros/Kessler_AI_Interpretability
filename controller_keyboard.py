from kesslergame.controller import KesslerController
from typing import Dict, Tuple, Any
from immutabledict import immutabledict

class MouseKeyboardController(KesslerController):
    def __init__(self):
        self._thrust = 0.0
        self._turn_rate = 0.0
        self._fire = False
        self._drop_mine = False

        self._key_state = set()
        self._mouse_state = set()

    @property
    def name(self) -> str:
        return "Keyboard/Mouse"

    def actions(self, ship_state: Dict[str, Any], game_state: immutabledict[Any, Any]) -> Tuple[float, float, bool, bool]:
        self._thrust = 480.0 if 'z' in self._key_state else -480.0 if 's' in self._key_state else 0.0
        self._turn_rate = 180.0 if 'q' in self._key_state else -180.0 if 'd' in self._key_state else 0.0
        self._fire = 'mouse1' in self._mouse_state
        self._drop_mine = 'mouse3' in self._mouse_state
        return self._thrust, self._turn_rate, self._fire, self._drop_mine

    def bind_events(self, window):
        window.bind("<KeyPress>", self._on_key_press)
        window.bind("<KeyRelease>", self._on_key_release)
        window.bind("<ButtonPress>", self._on_mouse_press)
        window.bind("<ButtonRelease>", self._on_mouse_release)

    def _on_key_press(self, event):
        self._key_state.add(event.keysym.lower())

    def _on_key_release(self, event):
        self._key_state.discard(event.keysym.lower())

    def _on_mouse_press(self, event):
        if event.num == 1:
            self._mouse_state.add("mouse1")
        elif event.num == 3:
            self._mouse_state.add("mouse3")

    def _on_mouse_release(self, event):
        if event.num == 1:
            self._mouse_state.discard("mouse1")
        elif event.num == 3:
            self._mouse_state.discard("mouse3")
