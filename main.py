from __future__ import annotations

import time

from cli_state_machine import CliStateMachine
from state import State
from tk_state_machine import TkStateMachine


class Apartment(State):
    DESCRIPTION: str = """
    You are inside of a small apartment downtown.
    There is a couch, a TV, and a messy bed.
    You can see a window with a view overlooking a snowy park.
    """
    IMAGE_DESCRIPTION: str = """
    A first-person view of a small apartment on the sixth floor of a building
    downtown.
    There is a couch, a TV. There is another room with a messy bed.
    There is a small window with a view overlooking a small snowy park.
    There are several people walking around outside.
    They are wearing heavy coats and scarfs because it is cold.
    There is no one else in the apartment
    """
    PROMPT: str = "Would you like to go outside or take a nap?"
    OPTIONS: dict[str, str] = {
        "outside": "OutsideApartment",
        "nap": "Nap",
    }


class OutsideApartment(State):
    DESCRIPTION: str = """
    You are standing outside of an apartment building downtown.
    All around are tall buildings.
    People are walking by.
    You can see a park in the distance.
    It is very cold.
    """
    IMAGE_DESCRIPTION: str = """
    A first-person view from someone standing outside of building downtown.
    All around are tall buildings.
    Several people are walking by.
    There is a park in the distance.
    It is very cold.
    There is about two inches of snow on the ground.
    """
    PROMPT: str = "Would you like to go back inside?"
    OPTIONS: dict[str, str] = {
        "yes": "Apartment",
    }


class Nap(State):
    DESCRIPTION: str = """
    You have decided to take a nap. Good night!
    """
    IMAGE_DESCRIPTION: str = """
    A person in a small apartment sleeping in a bed with a blanket over them.
    The moon is visible through the window.
    """

    def transition(self, _: str | None = None) -> State:
        time.sleep(5)
        return State.ExitGame


class ExitGame(State):
    TERMINAL: bool = True


if __name__ == "__main__":
    try:
        game = TkStateMachine(State.Apartment)
        game.run()
    except KeyboardInterrupt:
        pass
