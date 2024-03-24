from __future__ import annotations

from state import State
from state_machine import StateMachine

if __name__ == "__main__":
    game = StateMachine(State.Appartment)
    game.run()
