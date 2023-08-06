**⚠️ Current status of this project**

- Run `remote` to serve
    - Commands are not supported yet.
- Supported Operating Systems:
    - [x] Linux (Xorg) - by pynput
    - [x] Windows - by pynput
- Not yet supported Operating Systems:
    - [ ] Linux (Wayland)
    - [ ] macos - requires testing

---

# Couch Remote

A utility, available at [PyPI](https://pypi.org/project/couch-remote/), which serves a remote keyboard to control a computer.

## Usage

1. **To install:** `pip install couch-remote` (in a venv or globally)
2. Now, your `remote` should be available.
3. **Optionally,** `remote scaffold-config`, creates a basic settings file, then `remote global settings.py` copies it to a [global configuration directory](#install-a-global-settings-file-remote-global-settingspy).
4.  **Finally,** `remote control` serves an instance at [0.0.0.0:4444](http://localhost:4444). This is the **only** command, you're going to need from now on.



## Settings

```python
from pynput.keyboard import Key
from remote.models import Button

buttons = {
    'play_pause_media': Button(key=Key.media_play_pause, label='⏯️'),
    'esc': Button(key=Key.esc, label='Esc'),
    'caps': Button(key=Key.caps_lock, label='Caps Lock'),
    'space': Button(key=Key.space, label='Space'),
}

port = 4444
```

Q: Do jakiego formatu zapisują się i wczytują configi w settingsach?


### Install a global settings file `remote global settings.py `

When ran, stores settings at a default path: `~/.config/couch-remote/settings.py`

The app will default to this path when not specified.
