# ![App Screenshot](Quack.iconset/icon_16x16@2x.png) Quack

**Bring a little more quack to every keystroke.**

Quack is a macOS application that plays a sound whenever you press a configured keyboard key. It includes a graphical interface for starting and stopping the listener, along with a standalone command-line version.

## Features

- Play a custom sound when a configured key is pressed.
- Configure which keyboard keys trigger the sound.
- Start and stop keyboard listening from the GUI.
- Runs the keyboard listener as a separate process.
- Includes a bundled audio file.
- Distributed as a standalone macOS application.

## Installation

## Download

**[Download Quack for macOS](https://github.com/PatrickDohn/quack-keys/releases/latest)**

Download the latest release, open `Quack.dmg`, and drag Quack into your Applications folder.

Currently supports Apple Silicon Macs.

1. Open `Quack.dmg`.
2. Drag **Quack** into your Applications folder.
3. Eject the mounted installer.
4. Open Quack from Applications.

### macOS Security Permissions

Quack requires keyboard permissions to detect key presses.

On first launch, macOS may ask you to approve permissions.

If keyboard input is not detected:

1. Open **System Settings**.
2. Navigate to **Privacy & Security**.
3. Open **Input Monitoring**.
4. Enable permission for Quack or its keyboard-listener helper, if listed.
5. Restart Quack.

Depending on your macOS security settings, you may also need to approve the application manually the first time you open it.

> **Note:** Quack is currently distributed as an ad-hoc signed application and is not notarized by Apple. macOS may display a security warning when opening it.

## Using Quack

1. Launch Quack.
2. Configure the keys you want to use.
3. Click **Start**.
4. Press one of your configured keys to play the sound.
5. Click **Stop** when you're finished.

## Command-Line Version

Quack also has a standalone CLI version.

The CLI is separate from the graphical application and is not currently included in the DMG installer.

The command-line version can be installed and run independently.

## Project Structure

```text
quack-keys/
├── audio/
│   └── better_quack.wav
├── app_icon.png
├── Quack.icns
├── gui.py
├── listener.py
├── main.py
├── pyproject.toml
└── README.md
```

| File           | Purpose                            |
| -------------- | ---------------------------------- |
| `gui.py`       | PySide6 graphical application      |
| `listener.py`  | Separate keyboard-listener process |
| `main.py`      | Command-line application           |
| `audio/`       | Sound files                        |
| `app_icon.png` | GUI logo                           |
| `Quack.icns`   | macOS application icon             |

## Development

### Requirements

- macOS
- Python 3.14
- [uv](https://docs.astral.sh/uv/)
- PySide6
- PyInstaller

### Set Up

Clone the repository:

```bash
git clone <repository-url>
cd quack-keys
```

Install dependencies:

```bash
uv sync
```

Run the GUI:

```bash
uv run python gui.py
```

Run the standalone listener directly:

```bash
uv run python listener.py \
    --sound audio/better_quack.wav \
    --keys esc
```

## Building the macOS Application

Quack uses PyInstaller to package the GUI and keyboard listener separately.

### 1. Clean Previous Builds

```bash
rm -rf build dist
rm -f Quack.spec QuackListener.spec
```

### 2. Build the Listener

```bash
uv run pyinstaller \
    --onedir \
    --name QuackListener \
    --console \
    --clean \
    --noconfirm \
    listener.py
```

### 3. Build the GUI

```bash
uv run pyinstaller \
    --windowed \
    --name Quack \
    --osx-bundle-identifier com.quackkeys.Quack \
    --icon Quack.icns \
    --add-data "audio:audio" \
    --add-data "app_icon.png:." \
    --add-data "dist/QuackListener:QuackListener" \
    --clean \
    --noconfirm \
    gui.py
```

The resulting application will be:

```text
dist/Quack.app
```

### 4. Create the DMG Installer

```bash
mkdir -p dist/dmg
rm -rf dist/dmg/*

cp -R dist/Quack.app dist/dmg/
ln -s /Applications dist/dmg/Applications
```

Create the installer:

```bash
hdiutil create \
    -volname "Quack" \
    -srcfolder dist/dmg \
    -ov \
    -format UDZO \
    dist/Quack.dmg
```

Verify the installer:

```bash
hdiutil verify dist/Quack.dmg
```

The finished installer will be located at:

```text
dist/Quack.dmg
```

## Platform Support

- macOS Apple Silicon (arm64)
- Intel Mac support is not currently configured.

## License

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![GPLv3 License](https://img.shields.io/badge/License-GPL%20v3-yellow.svg)](https://opensource.org/licenses/)
[![AGPL License](https://img.shields.io/badge/license-AGPL-blue.svg)](http://www.gnu.org/licenses/agpl-3.0)
