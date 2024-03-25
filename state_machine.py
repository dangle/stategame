from __future__ import annotations

from state import State


class StateMachine:

    def __init__(self, start_state: State):
        self._state = start_state

    def run(self):
        while 1:
            self.display_state()

            if self._state.is_terminal:
                return

            input_: str = self.get_transition()
            self._state = self._state.transition(input_)

    def display_state(self):
        pass

    def get_transition(self) -> str:
        pass
