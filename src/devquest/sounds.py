import math
import platform
import shutil
import struct
import subprocess
import tempfile
import wave
from pathlib import Path

from devquest.config import get as config_get

SAMPLE_RATE = 22050

EVENTS = {
    "level_up": [(523, 0.08), (659, 0.08), (784, 0.12)],
    "critical": [(880, 0.05), (1100, 0.08)],
    "achievement": [(440, 0.06), (554, 0.06), (659, 0.1)],
    "quest_complete": [(392, 0.06), (494, 0.06), (587, 0.1)],
    "victory": [(523, 0.05), (659, 0.05), (784, 0.05), (1047, 0.12)],
}


def _tone(freq: float, duration: float, volume: float = 0.3) -> list[int]:
    samples = int(SAMPLE_RATE * duration)
    return [
        int(volume * 32767 * math.sin(2 * math.pi * freq * i / SAMPLE_RATE))
        for i in range(samples)
    ]


def _write_wav(path: Path, notes: list[tuple[float, float]]) -> None:
    frames: list[int] = []

    for freq, duration in notes:
        frames.extend(_tone(freq, duration))

    with wave.open(str(path), "w") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(struct.pack(f"<{len(frames)}h", *frames))


def _play_file(path: Path) -> None:
    system = platform.system()

    if system == "Darwin" and shutil.which("afplay"):
        subprocess.run(
            ["afplay", str(path)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
        )
        return

    if system == "Linux":
        for cmd in ("paplay", "aplay"):
            if shutil.which(cmd):
                subprocess.run(
                    [cmd, str(path)],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
                return

    if system == "Windows":
        try:
            import winsound

            winsound.PlaySound(str(path), winsound.SND_FILENAME | winsound.SND_ASYNC)
        except Exception:
            pass


def play(event: str) -> None:
    if not config_get("sounds"):
        return

    if event not in EVENTS:
        return

    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        path = Path(tmp.name)

    try:
        _write_wav(path, EVENTS[event])
        _play_file(path)
    finally:
        path.unlink(missing_ok=True)
