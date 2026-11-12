import argparse
from pathlib import Path

import sounddevice as sd
import soundfile as sf
from pynput import keyboard


def parse_key(value: str):
    value = value.lower().strip()

    if len(value) == 1:
        return value

    try:
        return keyboard.Key[value]
    except KeyError:
        raise argparse.ArgumentTypeError(f"Invalid key: {value}")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--sound", required=True)
    parser.add_argument("--keys", nargs="*", default=["esc"])

    args = parser.parse_args()

    sound_file = Path(args.sound)
    audio, sample_rate = sf.read(sound_file, dtype="float32")

    target_keys = {parse_key(value) for value in args.keys}
    pressed_keys = set()

    def on_press(key):
        if key in pressed_keys:
            return

        pressed_keys.add(key)

        ctrl_pressed = (
            keyboard.Key.ctrl_l in pressed_keys or keyboard.Key.ctrl_r in pressed_keys
        )

        char = getattr(key, "char", None)

        if ctrl_pressed and char and char.lower() in ("c", "\x03"):
            print("STOPPED", flush=True)
            return False

        if isinstance(key, keyboard.Key):
            matched = key in target_keys
        else:
            matched = char is not None and char.lower() in target_keys

        if matched:
            sd.play(audio, sample_rate)

    def on_release(key):
        pressed_keys.discard(key)

    listener = keyboard.Listener(
        on_press=on_press,
        on_release=on_release,
    )

    listener.start()
    print("READY", flush=True)

    try:
        listener.join()
    finally:
        listener.stop()
        sd.stop(ignore_errors=True)


if __name__ == "__main__":
    main()
