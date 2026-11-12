# MacOs Quack KeyBoard

- pynput: Global keyboard monitoring.
- sounddevice: Audio playback.
- soundfile: Loading audio files.

# Updating project wheel:

- rm -rf dist
  uv build
- `uv tool uninstall quack-keys`
- `uv tool install ./dist/quack_keys-0.1.0-py3-none-any.whl`

# Running:

example

```
  quack --help
  quack f8 a space
```
