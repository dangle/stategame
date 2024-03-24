from __future__ import annotations

import functools
import typing

import openai
import PIL as pillow
import PIL.Image
import requests

_CLIENT = openai.OpenAI()


T = typing.TypeVar("T", bound="_StateMetaclass")


class _StateMetaclass(type):

    _instance: T

    def __new__(
        cls: type[_StateMetaclass],
        name: str,
        bases: tuple[type, ...],
        classdict: dict,
    ) -> _StateMetaclass:
        new_cls = super().__new__(cls, name, bases, classdict)
        new_cls._instance = super(cls, new_cls).__call__()
        new_cls._instance.image

        for base in bases:
            if isinstance(base, cls):
                setattr(base, name, new_cls._instance)

        return new_cls

    def __call__(cls: type[T], *_, **__) -> T:
        return cls._instance


class State(metaclass=_StateMetaclass):

    @functools.cache
    def transition(self, input: str) -> State:
        if self.options.get(input):
            return getattr(State, self.options[input], self)
        return self

    @functools.cached_property
    def is_terminal(self) -> bool:
        return getattr(self.__class__, "TERMINAL", None)

    @functools.cached_property
    def description(self) -> str | None:
        return getattr(self.__class__, "DESCRIPTION", None)

    @functools.cached_property
    def image_description(self) -> str | None:
        return getattr(self.__class__, "IMAGE_DESCRIPTION", None)

    @functools.cached_property
    def options(self) -> dict[str, str]:
        return getattr(self.__class__, "OPTIONS", {})

    @functools.cached_property
    def prompt(self) -> str | None:
        return getattr(self.__class__, "PROMPT", None)

    @functools.cached_property
    def image(self) -> pillow.Image | None:
        if self.image_description is None:
            return None

        response: openai.ImagesResponse = _CLIENT.images.generate(
            model="dall-e-3",
            prompt=self.image_description,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        url: str = response.data[0].url
        raw_image: typing.Any = requests.get(url, stream=True).raw
        return pillow.Image.open(raw_image)

    @functools.cache
    def __str__(self) -> str:
        return f"State: {self.__class__.__name__}"


del State._instance
