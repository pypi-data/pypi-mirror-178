# Standard lib
from pathlib import Path
import threading

# Third party
import appdirs

# Local
from .conf import Settings

# Event flag to trigger graceful shutdown
inactive_flag = threading.Event()

# Project settings
settings = Settings(
    appname="WillSpeak",
    appdata_path=Path(appdirs.user_data_dir("WillSpeak"))
)
