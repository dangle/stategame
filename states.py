from __future__ import annotations

from state import State


class Appartment(State):
    DESCRIPTION: str = """
    You are inside of a small appartment downtown. There is a couch, a TV, and
    a messy bed. You can see a window with a view overlooking a snowy park.
    """

    IMAGE_DESCRIPTION: str = """
    A first-person view of a small appartment on the sixth floor of a building
    downtown. There is a couch, a TV, and a messy bed. There is a window with a
    view overlooking a snowy park. There are a people walking around outside.
    They are wearing heavy coats and scarfs because it is cold.
    """

    PROMPT: str = "Would you like to go outside or take a nap?"

    OPTIONS: dict[str, State] = {
        "outside": "OutsideAppartment",
        "nap": "Nap",
    }


class OutsideAppartment(State):
    DESCRIPTION: str = """
    You are standing outside of an appartment building downtown. All around are
    tall buildings. People are walking by. You can see a park in the distance.
    It is very cold.
    """

    IMAGE_DESCRIPTION: str = """
    A first-person view from someone standing outside of an appartment building
    downtown. All around are tall buildings. People are walking by. There is a
    park in the distance. It is very cold. There is snow everywhere.
    """

    PROMPT: str = "Would you like to go back inside?"

    OPTIONS: dict[str, State] = {
        "inside": "Appartment",
    }


class Nap(State):
    DESCRIPTION: str = """
    You have decided to take a nap. Good night!
    """

    TERMINAL: bool = True
