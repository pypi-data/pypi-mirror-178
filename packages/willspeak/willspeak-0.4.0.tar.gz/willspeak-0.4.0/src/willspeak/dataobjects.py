# Standard lib
from dataclasses import dataclass, field, fields, replace
from typing import Callable, Any, Literal

# Local
from .utils import import_from_string


@dataclass(eq=False)
class TextFilter:
    filter_func: Callable[[str], str | None]
    description: str = field(init=False)
    filter_name: str = field(init=False)
    filter_type: Literal['filter', 'decider'] = field(kw_only=True)
    enabled: bool = True

    def __post_init__(self):
        self.description = self.filter_func.__doc__.strip()
        self.filter_name = self.filter_func.__name__.replace("_", " ").title()

    def __call__(self, text: str) -> str:
        try:
            return self.filter_func(text)
        except Exception as e:
            print("Filter Error:", self.filter_name, e)
            return text  # Return the text unchanged

    @property
    def is_filter(self) -> bool:
        return self.filter_type == "filter"

    @property
    def is_decider(self) -> bool:
        return self.filter_type == "decider"


@dataclass(eq=False, frozen=True)
class Voice:
    """
    Voice dataclass.

    :ivar id: ID of the voice.
    :ivar name: The voice name.
    :ivar lang: The language of the voice, including the region, (United States) or (Great Britain).
    :ivar gender: The gender, male or female.
    :ivar age: The age group of the voice. e.g. Adult, child.
    """

    id: int | str
    name: str
    lang: str = field(kw_only=True, default="")
    gender: str = field(kw_only=True, default="")
    age: str = field(kw_only=True, default="")
    token: Any = field(kw_only=True, default=None, repr=False)
    selected: bool = field(kw_only=True, default=False)

    def as_dict(self) -> dict:
        """Converts the dataclass obj to a dict using a shallow copy only."""
        # We do not want the token variable to be return, token is internal
        return dict((_field.name, getattr(self, _field.name)) for _field in fields(self) if _field.name != "token")

    def __eq__(self, other) -> bool:
        return self.id == other.id


@dataclass
class EngineSpec:
    """
    Engine spec dataclass.
    """
    name: str
    installed: bool
    platforms: list[str]

    # Optionals
    selected: bool | None = False
    speaker_class: str | None = None
    engine_class: str | None = None

    def __post_init__(self):
        # Ensure all platform items are lowercase
        self.platforms = list(map(str.lower, self.platforms))

    def as_dict(self, current_engine: str = None) -> dict:
        """
        Return the objects as a dict but without any class vars.
        """
        return dict(
            name=self.name,
            installed=self.installed,
            selected=current_engine == self.name,
            platforms=self.platforms,
        )

    def copy(self, **changes):
        return replace(self, **changes)

    def get_engine_class(self):
        return import_from_string(self.engine_class)

    def get_speaker_class(self):
        return import_from_string(self.speaker_class)

    def initialize(self, **kwargs):
        engine_class = self.get_engine_class()
        return engine_class(self, **kwargs)


class Settings:
    """
    TTS engine settings,
    """

    def __init__(self, save_callback, settings: dict):
        _settings = {}
        object.__setattr__(self, "_callback", save_callback)
        object.__setattr__(self, "_settings", _settings)

        # Save setting while converting any data objects
        for key, val in settings.items():
            if key == "voice" and not isinstance(val, Voice):
                _settings[key] = Voice(**val)
            elif key == "engine" and not isinstance(val, EngineSpec):
                _settings[key] = EngineSpec(**val)
            else:
                _settings[key] = val

    def __getattr__(self, item):
        if item in self._settings:
            return self._settings[item]
        else:
            raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")

    def __setattr__(self, key, value):
        if value is not None:
            self._settings[key] = value

    def as_dict(self, shallow=False) -> dict:
        """
        Return the settings while also converting any known objects to dict as well.
        """
        resp_data = {}
        for key, val in self._settings.items():
            if isinstance(val, Voice):
                val = val.id if shallow else val.as_dict()
            elif isinstance(val, EngineSpec):
                val = val.name if shallow else val.as_dict()
            resp_data[key] = val
        return resp_data

    def save(self):
        self._callback(self._settings)

    def __enter__(self) -> "Settings":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.save()
