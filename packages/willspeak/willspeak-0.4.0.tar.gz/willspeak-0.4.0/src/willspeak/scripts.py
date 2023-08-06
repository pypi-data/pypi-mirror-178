# Third party
import colorama

# Local
from .monitors import ClipboardMonitor, ProcessMonitor
from .utils import graceful_exception
from .tts import get_engine_spec

# noinspection PyUnresolvedReferences
colorama.just_fix_windows_console()


@graceful_exception
def send_signal(args):
    """Send a simple command to running process."""
    return ProcessMonitor.send_simple_cmd(args.cmd)


@graceful_exception
def server(args):
    """Set up the TTS engine in server mode."""
    from . import server as tts_server
    engine_spec = get_engine_spec("sapi5")
    tts_server.start(engine_spec, args.bind_addr, args.bind_port)


@graceful_exception
def client(args):
    """Set up the TTS engine in client mode. Requires a running tts server."""
    from willspeak.client import TTSClient
    engine = TTSClient(addr=args.addr, port=args.port)
    return speaking_mode(engine, args)


@graceful_exception
def local(args):
    """Set up the TTS engine in local mode."""
    engine_spec = get_engine_spec("sapi5")
    engine = engine_spec.initialize()
    return speaking_mode(engine, args)


def speaking_mode(engine, args):
    """Run the tts engine, monitor clipboard and speak any text."""
    # Welcome the user
    with engine.get_settings() as tts_settings:
        tts_settings.volume = args.volume
        tts_settings.rate = args.rate
        tts_settings.voice = args.voice

    # List available voices
    voices = engine.get_voices()
    display_voices(voices)

    # Welcome user
    engine.speak("Welcome to the new will speak!")

    process_pipe = ProcessMonitor()
    monitor = ClipboardMonitor()

    # Allow for process communication to control current state
    process_pipe.start_server(
        stop=engine.stop,
        pause=monitor.pause,
        unpause=monitor.unpause,
        toggle=monitor.toggle,
    )

    # Monitor clipboard for text to speak
    monitor.wait_for_text(engine.speak)
    return 0


def display_voices(voices: list):
    """List all available voices."""
    print("Available Voices")
    print("----------------")
    for voice in voices:
        if voice.selected:
            print(f"{colorama.Fore.GREEN}{voice.id} - {voice.name} - {voice.lang}{colorama.Style.RESET_ALL}")
        else:
            print(f"{voice.id} - {voice.name} - {voice.lang}")
