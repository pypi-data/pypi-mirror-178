# WillSpeak - Work in Progress
Python Text to Speach using Microsoft Sapi5 with a server/client model.

# Progress update
The core functionality is now working, and is ready for testing.
Some cleanup is still required, but it works.
Only supports SAPI5 for now. More to come in the future.

# Info
I created this project as a way to have good TTS on linux, because TTS on linux at the moment is dreadful.
For a long time I wanted to switch to linux, but I needed a good linux TTS software but could not find one.
So I decided to create this project to interface with the windows SAPI5 TTS engine.

How it works is by running this software in server mode on a Windows machine. 
Then configure the linux client to communicate with that Windows TTS server.
The client will monitor for text that was copied to the clipboard and converts the text into speech.

# Usage
This software has 2 different operational modes, "Local" & "Server/Client". If the TTS engine that you have selected 
works natively on your operating system, Then you can use Local mode. e.g. SAPI5 is native to windows, so you can use
Local mode on Windows when using SAPI5. You should use Server/Client if you want to use SAPI5 on linux.
It requires python 3.10 or grater.

Install using pip
```shell
python3 -m pip install willspeak
```

Run locally on Windows
```shell
willspeak local
```

To run in server mode do.
```shell
willspeak server
```

And on the client machine run. "--addr" is the address of the server running the server component.
```shell
# 192.168.1.60 is just an example
willspeak client --addr=192.168.1.60
```

There is one last command that is used to stop any current speech.
```shell
willspeak stop
```

# TODO
* Setup prometheus metrics to track usage. This is useful if you wish to use a paid for TTS Service.
* Add support for other text to speech engines, like eSpeak.
* Add support for running the server component as a Windows service.
* Change the way things are configured from CLI args to web interface.
* Document how to enable more SAPI5 voices.
* See if there is a way to hide the useless stderr output from pyaudio on linux.

# Enable Extra SAPI5 Voices
Extra SAPI5 voices can be installed by going to Settings -> Time & Language -> Speech.
Click the plus icon next to add voices in the Manage voices section. Here you will see a full
list of available voices for a given language. Select language voice you want and click add.
This will download and install the new voices. They will be available for preview when you close and
re-open the settings app.

You can even use the Cortana voice (Eva) for SAPI5, but this requires a registry tweak to be able to enable it.
And also requires you to have the English (US) language pack installed. This is the best female voice in my opinion.
But if you are looking for a male voice then Richard is the best, available in the English (Canada) voice package.




# Links
https://winaero.com/unlock-extra-voices-windows-10/

## Version
0.3.0
