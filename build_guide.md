# MacOs Quack KeyBoard

- pynput: Global keyboard monitoring.
- sounddevice: Audio playback.
- soundfile: Loading audio files.

# Updating project wheel:

- rm -rf dist
  uv build
- `uv tool uninstall quack-keys`
- `uv tool install ./dist/quack_keys-0.1.0-py3-none-any.whl`

---

# Updating project wheel pt2:

- rm -rf build dist
- rm -f Quack.spec QuackListener.spec
- rm -rf "$HOME/Library/Application Support/pyinstaller"

---

rebuild listener:

```
uv run pyinstaller \
  --onedir \
  --name QuackListener \
  --console \
  --clean \
  --noconfirm \
  listener.py
```

rebuild gui:

```
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

# Create DMG:

```
cd ~/git/quack-keys

mkdir -p dist/dmg
rm -rf dist/dmg/*

cp -R dist/Quack.app dist/dmg/
ln -s /Applications dist/dmg/Applications

hdiutil create \
    -volname "Quack" \
    -srcfolder dist/dmg \
    -ov \
    -format UDZO \
    dist/Quack.dmg
```

# Test DMG:

```
Double-click dist/Quack.dmg.



Drag Quack into Applications.



Eject the DMG.



Open Quack from Applications.



Test the keyboard shortcut and sound.

```

# Running:

example

```
  quack --help
  quack f8 a space
```
