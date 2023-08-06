# Standard lib
from typing import Iterator
import hashlib

# Third party
# noinspection PyUnresolvedReferences
from comtypes.client import CreateObject
# noinspection PyUnresolvedReferences
from _ctypes import COMError

# Local
from . import BaseTTSEngine
from .. import settings as conf
from ..dataobjects import Voice, Settings

# Stream Formats
SAFT22kHz16BitMono = 22
SAFT22kHz16BitStereo = 23
SAFT24kHz16BitMono = 26
SAFT24kHz16BitStereo = 27
SAFT32kHz16BitMono = 30
SAFT32kHz16BitStereo = 31
SAFT44kHz16BitMono = 34
SAFT44kHz16BitStereo = 35
SAFT48kHz16BitMono = 38
SAFT48kHz16BitStereo = 39

# Speak Flags
SVSFDefault = 0
SVSFlagsAsync = 1
SVSFPurgeBeforeSpeak = 2
SVSFIsFilename = 4
SVSFIsXML = 8
SVSFIsNotXML = 16
SVSFPersistXML = 32


def create_voice_obj(voice_token, selected=False) -> Voice:
    """Takes a C SpObjectToken voice object converting to a python data object."""
    # The description contains both the name and lang
    # The real lang attribute is a number (strange)
    full_name = voice_token.GetDescription()
    name, lang = full_name.split(" - ", 1)
    name = name.replace("Desktop", "").replace("Mobile", "").strip()
    lang = lang.strip()

    # We create ID instead of using the available one
    # The available one is a mix of version and name with some other crap
    voice_id = int(str(int(hashlib.sha1(full_name.encode("utf8")).hexdigest(), 16))[:8])

    return Voice(
        id=voice_id,
        name=name,
        lang=lang,
        age=voice_token.GetAttribute("Age"),
        gender=voice_token.GetAttribute("Gender"),
        token=voice_token,
        selected=selected,
    )


class TTSEngine(BaseTTSEngine):
    """
    TTS driver module to control microsoft SAPI TTS Engine.
    """

    def __setstate__(self, state):
        self._engine = CreateObject("SAPI.SPVoice")
        super(TTSEngine, self).__setstate__(state)

    def __init__(self, *args, **kwargs):
        super(TTSEngine, self).__init__(*args, **kwargs)
        self._engine = CreateObject("SAPI.SPVoice")

    # noinspection PyMethodMayBeStatic
    def _create_memory_stream(self):
        """
        Create SAPI in memory audio stream.
        """
        stream = CreateObject("SAPI.SpMemoryStream")
        # Mono keeps the transfer size down
        # Audio stream can always be converted to stereo after the fact
        stream.Format.Type = SAFT48kHz16BitMono
        return stream

    def get_voices(self) -> list[Voice]:
        """
        Return list of available voices as a Voice object.
        """
        c_voice = self._engine.Voice
        return [create_voice_obj(attr, selected=c_voice.Id == attr.Id) for attr in self._engine.GetVoices()]

    def get_settings(self) -> Settings:
        """
        Return settings related to the speech engine.
        """
        return Settings(self.set_settings, dict(
            rate=self._engine.Rate,
            volume=self._engine.Volume,
            voice=create_voice_obj(self._engine.Voice, selected=True),
            engine=self.spec,
        ))

    def set_settings(self, settings: dict):
        """
        Apply changed settings.
        """
        if "rate" in settings:
            self._set_rate(settings["rate"])
        if "volume" in settings:
            self._set_volume(settings["volume"])
        if "voice" in settings:
            self._set_voice(settings["voice"])

    def _set_voice(self, value: Voice | int | str):
        """
        Change voice to selected voice.
        """
        if isinstance(value, Voice):
            self._engine.Voice = value.token
            return

        # Search for voice using given id or name
        for voice in self.get_voices():
            # Do the check as strings, as the voice ID can be a string
            if str(voice.id) == str(value) or voice.name == value:
                self._engine.Voice = voice.token
                break
        else:
            message = f"No voice found matching ID: {value}"
            raise ValueError(message)

    def _set_rate(self, rate: int):
        """
        Change the speach rate of the voice.
        """
        if rate < -10 or rate > 10:
            raise ValueError("invalid rate %s" % rate)
        else:
            self._engine.Rate = rate

    def _set_volume(self, value: int):
        """
        Change the volume of the voice.
        """
        if value < 0 or value > 100:
            raise ValueError("invalid volume %s" % value)
        else:
            self._engine.Volume = value

    def speak(self, text: str) -> Iterator[bytes]:
        """
        Send text to tts engine and speak.
        """
        try:
            stream = self._create_memory_stream()
            self._engine.AudioOutputStream = stream
            self._engine.Speak(text, SVSFlagsAsync)
        except COMError:
            print("Speech engine failed to process request.")
            return iter([])

        # Now we can wait and stream the audio
        chunks = self._speak(stream)
        if self.speaker is not None:
            self.speaker.play_iterator(chunks)
        else:
            return chunks

    def _speak(self, stream) -> Iterator[bytes]:
        """
        Call the speach engin and send all audio to the given stream.

        :returns bool: Returns True if command completed, False if command timed out.
        """
        # Wait 10 seconds for the conversion to complete
        # Any longer than that and there must be an issue
        # WaitUntilDone returns False when it times out
        completed = not self._engine.WaitUntilDone(conf.speak_timeout)
        if completed:
            self.stop()
            self._engine.Speak("Error: Speak Request timed out")

        stream.Seek(0)
        while True:
            audio_chunk, data_size = stream.read(conf.chunk)
            if data_size:
                yield bytes(audio_chunk)
            else:
                break

        return completed

    def stop(self):
        """
        Stop current speak request.
        """
        self._engine.Speak("", SVSFPurgeBeforeSpeak)
        if self.speaker is not None:
            self.speaker.stop()
