from __future__ import annotations

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

            options_list: str = " / ".join(self._state.options.keys())
            print(f"{self._state.prompt} ({options_list})")
            print("> ", end="")
            input_ = input()
            self._state = self._state.transition(input_)
