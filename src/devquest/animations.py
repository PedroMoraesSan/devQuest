from time import sleep

from rich.progress import track


def loading(message: str):
    for _ in track(range(40), description=message):
        sleep(0.02)
