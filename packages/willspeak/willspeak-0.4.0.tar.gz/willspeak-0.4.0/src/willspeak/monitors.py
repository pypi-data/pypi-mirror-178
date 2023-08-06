"""
This module monitors the clipboard for changes and add any copied
text to a processing queue.
"""

# Standard lib
from multiprocessing.connection import Listener, Client
from threading import Thread, Event
from typing import Callable
import queue

# Third party
from pyclip.base import ClipboardException
import pyclip

# Local
from willspeak import inactive_flag, settings, filters


class ClipboardMonitor(Thread):
    """Monitors the clipboard for changes and adds to processing queue."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._process_queue = queue.Queue()
        self._paused = Event()
        filters.prepare()

    def pause(self):
        """
        Pause monitoring of the clipboard.
        """
        self._paused.set()
        print("Clipboard monitoring disabled")

    def unpause(self):
        """
        Unpause clipboard monitoring.
        """
        self._paused.clear()
        print("Clipboard monitoring enabled")

    def toggle(self):
        """
        Toggle clipboard monitoring between paused and un paused.
        """
        if self._paused.is_set():
            self.unpause()
        else:
            self.pause()

    # noinspection PyUnusedLocal
    def run(self) -> None:
        """
        This function call blocks until a new text string exists on the
        clipboard that is different from the text that was there when the function
        was first called.
        """
        # We ignore the first clipboard text on startup
        prev_text = self.get_clipboard()
        while not inactive_flag.wait(settings.timeout):
            text = self.get_clipboard()
            # Ensure that we don't have the same text again
            if text and text != prev_text:
                prev_text = text
                if not self._paused.is_set():
                    for processed_text in filters.process_text(text):
                        self._process_queue.put(processed_text)

    # noinspection PyMethodMayBeStatic
    def get_clipboard(self) -> str:
        """Return text from clipboard."""
        try:
            return pyclip.paste(text=True).strip()
        except ClipboardException:
            return ""

    def wait_for_text(self, callback: Callable[[str], None]):
        """
        Continuously monitor the queue for text to convert to speach.
        Filtering the text as it runs.
        """
        # This will start the background clipboard monitor
        self.start()

        # This will wait for available text
        while not inactive_flag.is_set():
            try:
                text = self._process_queue.get(timeout=settings.timeout)
            except queue.Empty:
                continue

            try:
                callback(text)
            except Exception as e:
                print(f"Error: Speak failed - {e}")
            finally:
                self._process_queue.task_done()


class ProcessMonitor(Thread):
    LISTEN_PORT = 33950

    def __init__(self, *args, **kwargs):
        super().__init__(*args, daemon=True, **kwargs)
        self._commands = None

    def run(self) -> None:
        listener = Listener(("127.0.0.1", self.LISTEN_PORT))

        while not inactive_flag.is_set():
            conn = listener.accept()
            command = conn.recv()
            if command in self._commands:
                func = self._commands[command]
                func()

            conn.close()
        listener.close()

    def start_server(self, **commands):
        """Start the process listener server to check for process commands."""
        self._commands = commands
        self.start()

    @classmethod
    def send_simple_cmd(cls, command: str):
        """Send the stop signal to master process."""
        try:
            conn = Client(("127.0.0.1", cls.LISTEN_PORT))
        except ConnectionRefusedError:
            return 1
        else:
            conn.send(command)
            conn.close()
            return 0
