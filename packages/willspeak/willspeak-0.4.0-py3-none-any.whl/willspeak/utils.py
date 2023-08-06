# Standard lib
from typing import Coroutine, Callable
import importlib
import functools
import asyncio

# Local
from willspeak import inactive_flag


background_tasks = set()


def graceful_exception(func):
    """
    Decorator function to handle exceptions gracefully.
    And signal any threads to end.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> int:
        try:
            ret = func(*args, **kwargs)
        except KeyboardInterrupt:
            return 143
        else:
            # Return 0 if no return code was returned
            return ret if ret is not None else 0
        finally:
            inactive_flag.set()

    return wrapper


def ensure_int_range(min_value: int, max_value: int) -> Callable[[str], int]:
    """
    Function that converts a string into an integer while ensuring the value is within the given range.

    :param min_value: The minimum allowed value.
    :param max_value: The maximum allowed value.
    """

    def wrapper(string: str) -> int:
        value = int(string)
        if min_value <= value <= max_value:
            return value
        else:
            raise ValueError(f"'{value}' is outside range, must be anywhere from {min_value} and {max_value}")

    return wrapper


def import_from_string(string: str):
    """
    Import an object form a module given the full import path to said module.
    """
    _import, obj_name = string.split(":", 1)
    module = importlib.import_module(_import)
    return getattr(module, obj_name)


def create_background_task(coroutine: Coroutine):
    """Create an async background task that cleans up after itself."""
    task = asyncio.create_task(coroutine)

    # Add task to the set. This creates a strong reference.
    background_tasks.add(task)

    # To prevent keeping references to finished tasks forever,
    # make each task remove its own reference from the set after completion
    task.add_done_callback(background_tasks.discard)
