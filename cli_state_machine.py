from __future__ import annotations

from state_machine import StateMachine


class CliStateMachine(StateMachine):

    def display_state(self):
        print(self._state.description)

    def get_transition(self) -> str:
        options_list: str = " / ".join(self._state.options.keys())

        print(f"{self._state.prompt} ({options_list})")
        print("> ", end="")

        return input()
