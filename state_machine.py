from __future__ import annotations

import states as _
from state import State


class StateMachine:

    def __init__(self, start_state: State):
        self._state = start_state

    def run(self):
        while 1:
            print(self._state.description)

            if self._state.image:
                self._state.image.show()

            if self._state.is_terminal:
                return

            print(f'{self._state.prompt} ({" / ".join(self._state.options.keys())})')
            print("> ", end="")
            input_ = input()
            self._state = self._state.transition(input_)
