# Standard lib
from typing import Iterator
import platform
import time

# Local
from ..dataobjects import Voice, EngineSpec, Settings
from ..audio import SpeakerBase


class BaseTTSEngine:
    """
    TTS driver module to control microsoft SAPI TTS Engine.
    """
    def __getstate__(self):
        return dict(
            settings=self.get_settings().as_dict(shallow=True),
            build_speaker=self.speaker is not None
        )

    def __setstate__(self, state):
        settings = state["settings"]
        self.spec = get_engine_spec(settings["engine"])
        self.speaker = self._build_speaker() if state["build_speaker"] else None
        self.set_settings(settings)
        self.update_access_time()

    def __init__(self, spec: EngineSpec, server_mode=False):
        self.spec: EngineSpec = spec.copy(selected=True)
        self.speaker = None if server_mode else self._build_speaker()
        self.last_used = time.time()

    def _build_speaker(self) -> SpeakerBase:
        """Build Speaker when not running in server mode."""
        speaker_class = self.spec.get_speaker_class()
        speaker = speaker_class()
        speaker.start()
        return speaker

    def update_access_time(self):
        """
        Update the last used tracker.

        This is used when clearing stale connections.
        If the engine has not been used in a while, then garbage collect it.
        """
        self.last_used = time.time()

    @property
    def is_stale(self) -> bool:
        """Return True if the engine has not been used in a while (stale)."""
        return time.time() - self.last_used > 86400  # 24 hours

    @property
    def name(self) -> str:
        """Return the name of this speech engine."""
        return self.spec.name

    def get_voices(self) -> list[Voice]:
        """
        Return list of available voices as a Voice object.
        """
        raise NotImplementedError()

    def get_settings(self) -> Settings:
        """
        Return settings related to the speech engine.
        """
        raise NotImplementedError()

    def set_settings(self, settings: dict):
        """
        Apply changed settings.
        """
        raise NotImplementedError()

    def speak(self, text: str):
        """
        Send text to tts engine and speak.
        """
        raise NotImplementedError()

    def stop(self):
        """
        Stop current speak request.
        """
        raise NotImplementedError()

    def close(self):
        if self.speaker is not None:
            self.speaker.close()


def get_supported_engines() -> Iterator[EngineSpec]:
    """
    Return an iterator of all supported tts engines specs.
    """
    _platform = platform.system().lower()
    for spec in tts_engine_specs:
        if "all" in spec.platforms or _platform in spec.platforms:
            yield spec


def get_engine_spec(name: str) -> EngineSpec | None:
    """
    Return the specification for given engine name.
    """
    return spec_map[name]


# Each speech engine is required to be defined here
# This allows for speech engines to be imported only when required
tts_engine_specs = [
    EngineSpec(
        name="sapi5",
        platforms=["windows"],
        speaker_class="willspeak.audio:WaveSpeaker",
        engine_class="willspeak.tts.sapi5:TTSEngine",
        installed=True,
    )
]

# Map engine names for faster lookup
spec_map = {spec.name: spec for spec in tts_engine_specs}
