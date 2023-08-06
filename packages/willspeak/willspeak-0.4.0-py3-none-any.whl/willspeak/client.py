# Third party
import requests

# Local
from .dataobjects import Voice, EngineSpec, Settings
from .tts import get_engine_spec


class TTSClient(object):
    """
    TTS driver module to control microsoft SAPI TTS Engine.
    """

    # Methods
    GET = "GET"
    PUT = "PUT"
    POST = "POST"

    # Endpoints
    EPT_SETTINGS = "/api/settings"
    EPT_ENGINES = "/api/engines"
    EPT_VOICES = "/api/voices"
    EPT_SPEAK = "/api/speak"
    EPT_STOP = "/api/stop"

    def __init__(self, addr: str, port: int):
        self.base_url = f"http://{addr}:{port}"
        self.session = requests.Session()
        self.speaker = None

        # Instantiate speaker for current speech engine
        setting = self.get_settings()
        self._set_current_spec(setting.engine)

    def _set_current_spec(self, spec: EngineSpec):
        """
        Sets the current engine spec and change to correct speaker
        """
        # Close current speaker before creating new one
        if self.speaker is not None:
            self.speaker.close()

        speaker_class = spec.get_speaker_class()
        self.speaker = speaker_class()
        self.speaker.start()
        self.spec = spec

    def _make_json_request(self, method: str, url: str, **kwargs) -> list | dict | None:
        url = self.base_url + url
        resp = self.session.request(method, url, **kwargs)
        try:
            resp.raise_for_status()
            if resp.status_code != 204:
                return resp.json()
        finally:
            resp.close()

    def get_voices(self) -> list[Voice]:
        """
        Return list of available voices as a Voice object.
        """
        voices = []
        for voice in self._make_json_request(self.GET, self.EPT_VOICES):
            voice_obj = Voice(**voice)
            voices.append(voice_obj)

        return voices

    def get_engines(self) -> list[EngineSpec]:
        """
        Return list of available TTS engines as a EngineSpec object.
        """
        engines = []
        for engine in self._make_json_request(self.GET, self.EPT_ENGINES):
            spec = get_engine_spec(engine["name"])
            engines.append(spec)

        return engines

    def get_settings(self) -> Settings:
        """
        Return settings related to the speech engine.
        """
        resp = self._make_json_request(self.GET, self.EPT_SETTINGS)
        resp["engine"] = get_engine_spec(resp["engine"]["name"])
        return Settings(self.set_settings, resp)

    def set_settings(self, settings: dict):
        """
        Apply changed settings.
        """
        if isinstance(settings.get("voice"), Voice):
            settings["voice"] = settings["voice"].id
        if isinstance(settings.get("engine"), EngineSpec):
            settings["engine"] = settings["engine"].name

        # Check if engine has changed and update speaker accordingly
        changed = self._make_json_request(self.PUT, self.EPT_SETTINGS, json=settings)
        if changed and changed["engine"]["name"] != self.spec.name:
            spec = get_engine_spec(changed["engine"]["name"])
            self._set_current_spec(spec)

    def speak(self, text):
        """
        Send text to tts engine and speak.
        """
        raw_text = text.encode("utf8")
        url = self.base_url + self.EPT_SPEAK
        headers = {"content-type": "text/plain; charset=UTF-8", "content-length": str(len(raw_text))}
        resp = self.session.request(self.POST, url, data=raw_text, headers=headers, stream=True)
        resp.raise_for_status()

        # Stream the response into the speaker
        iterator = resp.iter_content(4096)
        self.speaker.play_iterator(iterator)
        resp.close()

    def stop(self):
        """
        Stop current speak request.
        """
        self.speaker.stop()
        self._make_json_request(self.GET, self.EPT_STOP)
        self.speaker.stop()  # We do it again to be sure

    def close(self):
        self.speaker.close()
        self.session.close()
