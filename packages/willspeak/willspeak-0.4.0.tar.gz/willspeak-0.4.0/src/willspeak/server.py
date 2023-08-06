# Standard lib
from pathlib import Path
import asyncio
import pickle

# Third party
from starlette.responses import JSONResponse, StreamingResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException
from starlette.applications import Starlette
from starlette.endpoints import HTTPEndpoint
from starlette.middleware import Middleware
from starlette.requests import Request
from starlette.routing import Route
import uvicorn

# Local
from .dataobjects import EngineSpec
from .tts import BaseTTSEngine, get_supported_engines, get_engine_spec
from .utils import create_background_task
from . import settings as conf


# Views
######################################################################

async def api_root(request: Request):
    """
    This is the api root. It should list the urls to all the api endpoints.

    Endpoints:
        * /speak: Convert text to speach and respond with a raw wav file.
        * /settings: Get/set TTS engine parameters.
        * /voices: Get list of all available voices.
    """
    data = dict(
        speak=request.url_for("speak"),
        stop=request.url_for("stop"),
        settings=request.url_for("settings"),
        voices=request.url_for("voices"),
        engines=request.url_for("engines"),
        keep_alive=request.url_for("keep_alive"),
    )
    return JSONResponse(data)


# noinspection PyUnresolvedReferences
async def get_engines(request: Request):
    """
    Return list of all available speach engines.
    """
    engine = request.scope["engine"]
    resp_data = [spec.as_dict(engine.name) for spec in get_supported_engines()]
    return JSONResponse(resp_data)


# noinspection PyUnresolvedReferences
async def get_voices(request: Request):
    """
    Return list of all available voices.
    """
    data = []
    engine = request.scope["engine"]
    for voice in engine.get_voices():
        voice_dict = voice.as_dict()
        data.append(voice_dict)
    return JSONResponse(data)


# noinspection PyMethodMayBeStatic
class Settings(HTTPEndpoint):
    # noinspection PyUnresolvedReferences
    async def get(self, request: Request):
        """
        Return the current settings values.

        Settings:
            * rate: The current speaking rate.
            * volume: The current speaking volume.
            * voice: The currently selected voice.
        """
        engine = request.scope["engine"]
        settings = engine.get_settings()
        return JSONResponse(settings.as_dict())

    # noinspection PyUnresolvedReferences
    async def put(self, request: Request):
        """
        Change any or all of the tts settings.
        """
        engine = request.scope["engine"]
        req_data = await request.json()

        # Check if a tts engine change is requested
        if "engine" in req_data and req_data["engine"] != engine.name:
            engine = self.change_engine(request, req_data["engine"])

        # Return the full settings response with changes
        request.scope["state_manager"].save_state(request.client.host, engine)
        engine.set_settings(req_data)
        return await self.get(request)

    # noinspection PyUnresolvedReferences
    def change_engine(self, request: Request, engine_name: str) -> BaseTTSEngine:
        """
        Change the TTS engine to the given engine name for the current user.
        """
        engine = request.scope["engine"]
        if engine_spec := get_engine_spec(engine_name):
            engine.close()
            engine = engine_spec.initialize(server_mode=True)
            request.app.state.host_map[request.client.host] = engine
            return engine
        else:
            message = f"No TTS engine found matching name: {engine_name}"
            raise ValueError(message)


# noinspection PyMethodMayBeStatic
class Speak(HTTPEndpoint):
    """
    Convert any given text into speach.

    The text can be given by using url params, or by using the request body.
    The url param to use is called 'text', the value needs to be url encoded.
    When sending the text using the body it can just be a plain text post request.
    The response will be a raw wave file.

    Support for other response types are planned.
    """

    async def get(self, request: Request):
        """Handle text from url params."""
        if "text" not in request.query_params:
            message = "Missing required url parameter: text"
            return JSONResponse({"error": message}, status_code=400)

        texts = request.query_params.getlist("text")
        text = ". ".join(texts)
        return await self.speak(request, text)

    async def post(self, request: Request):
        """Handel text from post request."""
        body = await request.body()
        if not body:
            message = "Missing required text body"
            return JSONResponse({"error": message}, status_code=400)

        return await self.speak(request, body.decode("utf8"))

    # noinspection PyUnresolvedReferences
    async def speak(self, request: Request, text: str):
        """Convert text into speach."""
        # Call TTS engine in another thread as the call is a blocking call
        engine = request.scope["engine"]
        engine.update_access_time()
        chunks = engine.speak(text)
        resp = StreamingResponse(chunks, media_type="audio/wave")
        return resp


async def stop_speak(request: Request):
    request.scope["engine"].stop()
    return JSONResponse("", status_code=204)


routes = [
    Route("/",                  endpoint=api_root,      name=""),
    Route("/api/engines",       endpoint=get_engines,   name="engines"),
    Route("/api/voices",        endpoint=get_voices,    name="voices"),
    Route("/api/settings",      endpoint=Settings,      name="settings"),
    Route("/api/speak",         endpoint=Speak,         name="speak"),
    Route("/api/stop",          endpoint=stop_speak,    name="stop"),
]


# Async Setup
######################################################################

class StateMachine:
    """
    Manage engine states.

    Active engine states for each client is stored in memory.
    When state has not been used recently it will get paged out to disk.
    This manager will also handle the creation of new engine states for new clients.
    """
    def __init__(self, default_spec):
        self.host_map = {}
        self.default_spec = default_spec
        self.state_dir = conf.appdata_path / "engine-states"
        self.state_dir.mkdir(parents=True, exist_ok=True)

    def host_state_file(self, host: str) -> Path:
        """Return the state file for given host."""
        return self.state_dir / f"{host.replace('.', '-')}.pickle"

    def save_state(self, host: str, engine: BaseTTSEngine):
        """Save the engine state for the given host to disk."""
        state_file = self.host_state_file(host)
        with state_file.open("wb") as stream:
            pickle.dump(engine, stream, protocol=pickle.HIGHEST_PROTOCOL)

    def save_all_states(self):
        """Save all clients engine states to disk."""
        for host, engine in self.host_map.items():
            self.save_state(host, engine)

    def load_state(self, host: str) -> BaseTTSEngine | None:
        """Load the engine state for the given host from disk."""
        state_file = self.host_state_file(host)
        if state_file.exists():
            with state_file.open("rb") as stream:
                try:
                    engine = pickle.load(stream)
                except pickle.UnpicklingError:
                    state_file.unlink()
                    return None
                else:
                    return engine

    def get_engine(self, host: str) -> BaseTTSEngine:
        """
        Return the engine for the given host.

        Engine may be stored in memory or on disk.
        If no engine is stored then a new engine state is created.
        """
        if engine := self.host_map.get(host):
            return engine
        elif engine := self.load_state(host):
            self.host_map[host] = engine
            return engine
        else:
            engine = self.default_spec.initialize(server_mode=True)
            self.host_map[host] = engine
            return engine

    async def memory_cleanup(self):
        """Periodically purge memory of stale engine states."""
        while True:
            await asyncio.sleep(14400)  # 4 Hours
            # Remove stale engines from server state
            for host, engine in list(self.host_map.items()):
                if engine.is_stale:
                    self.save_state(host, engine)
                    del self.host_map[host]

    async def on_startup(self):
        """Startup procedures."""
        create_background_task(self.memory_cleanup())

    async def on_shutdown(self):
        """Shutdown procedures."""
        self.save_all_states()


class SpeechEngineMiddleware(BaseHTTPMiddleware):
    """
    Add the speech engine assigned to the remote user to the request object.
    """
    def __init__(self, app, state_manager=None):
        self.state_manager = state_manager
        super().__init__(app)

    async def dispatch(self, request, call_next):
        """Each user's connection has its own engine."""
        engine = self.state_manager.get_engine(request.client.host)
        request.scope["state_manager"] = self.state_manager
        request.scope["engine"] = engine
        return await call_next(request)


async def http_exception(_: Request, exc: HTTPException):
    return JSONResponse({"error": exc.detail}, status_code=exc.status_code, headers=exc.headers)


async def value_exception(_: Request, exc: HTTPException):
    return JSONResponse({"error": str(exc)}, status_code=400)


# noinspection PyTypeChecker
def start(default_spec: EngineSpec, host: str, port: int):
    """
    Start the async event loop server.
    """
    state_manager = StateMachine(default_spec)
    middleware = [Middleware(SpeechEngineMiddleware, state_manager=state_manager)]
    app = Starlette(
        routes=routes,
        middleware=middleware,
        on_startup=[
            state_manager.on_startup
        ],
        on_shutdown=[
            state_manager.on_shutdown
        ],
        exception_handlers={
            HTTPException: http_exception,
            ValueError: value_exception,
        },
    )
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
