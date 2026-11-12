import argparse
import signal
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import sounddevice as sd
import soundfile as sf
from pynput import keyboard

executor = ThreadPoolExecutor(max_workers=4)

BASE_DIR = Path(__file__).parent
SOUND_FILE = BASE_DIR / "audio" / "better_quack.wav"

audio, sample_rate = sf.read(SOUND_FILE, dtype="float32")


def parse_key(value):
    value = value.lower()

    # Single-character keys
    if len(value) == 1:
        return value

    # Special keys such as esc, space, enter, f8
    try:
        return keyboard.Key[value]
    except KeyError:
        raise argparse.ArgumentTypeError(f"Invalid key: {value}")


def play_sound():
    sd.play(audio, sample_rate)


def main():
    shutdown_event = threading.Event()
    pressed_keys = set()
    parser = argparse.ArgumentParser(description="Play a sound when a key is pressed.")

    parser.add_argument(
        "keys",
        nargs="*",
        type=parse_key,
        help="One or more keys to listen for",
    )

    args = parser.parse_args()

    target_keys = set(args.keys) if args.keys else {keyboard.Key.esc}

    # print(f"Listening for: {target_key}")
    # print("Press Ctrl+C to exit.")

    def handle_sigint(signum, frame):
        shutdown_event.set()

    signal.signal(signal.SIGINT, handle_sigint)

    def on_press(key):
        pressed_keys.add(key)

        ctrl_pressed = (
            keyboard.Key.ctrl_l in pressed_keys or keyboard.Key.ctrl_r in pressed_keys
        )

        c_pressed = getattr(key, "char", None) == "c"

        if ctrl_pressed and c_pressed:
            shutdown_event.set()
            return False

        if isinstance(key, keyboard.Key):
            matched = key in target_keys
        else:
            char = getattr(key, "char", None)
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

    try:
        while listener.is_alive() and not shutdown_event.wait(0.1):
            pass

    finally:
        # print("\nCtrl+C detected. Stopping Quack...")hsa sa sa sa

        listener.stop()
        listener.join()

        # Stop audio before Python begins its exit cleanup
        sd.stop(ignore_errors=True)

    print(" 🦆 ╾━╤デ╦︻ (•_- ) ")


if __name__ == "__main__":
    main()
