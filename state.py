from __future__ import annotations

import functools
import typing

import openai
import PIL.Image
import requests


class _StateMetaclass(type):

    _instance: _StateMetaclass

    def __new__(
        cls: type[_StateMetaclass],
        name: str,
        bases: tuple[type, ...],
        classdict: dict,
    ) -> _StateMetaclass:
        new_cls = super().__new__(cls, name, bases, classdict)
        new_cls._instance = super(cls, new_cls).__call__()

        for base in bases:
            if isinstance(base, cls):
                setattr(base, name, new_cls._instance)

        return new_cls

    def __call__(cls: _StateMetaclass) -> _StateMetaclass:
        return cls._instance


class State(metaclass=_StateMetaclass):

    _oaiclient: openai.OpenAI | None = None

    def transition(self, input_: str | None = None) -> State:
        if input_ is None:
            return self

        if self.options.get(input_):
            return getattr(State, self.options[input_], self)

        return self

    @functools.cached_property
    def is_terminal(self) -> bool:
        return getattr(self.__class__, "TERMINAL", False)

    @functools.cached_property
    def description(self) -> str | None:
        desc: str = getattr(self.__class__, "DESCRIPTION", None)

        if desc:
            lines: list[str] = desc.strip().split("\n")
            return "\n".join(line.strip() for line in lines)

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
    def _client(self) -> openai.OpenAI:
        if not State._oaiclient:
            State._oaiclient = openai.OpenAI()
        return State._oaiclient

    @functools.cached_property
    def image(self) -> PIL.Image.Image | None:
        if self.image_description is None:
            return None

        response: openai.types.ImagesResponse = self._client.images.generate(
            model="dall-e-3",
            prompt=self.image_description,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        url: str = typing.cast(str, response.data[0].url)
        raw_image: typing.Any = requests.get(url, stream=True).raw

        return PIL.Image.open(raw_image)

    @functools.cache
    def __str__(self) -> str:
        return f"State: {self.__class__.__name__}"


del State._instance
