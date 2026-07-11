import math
import sys
import time

from rich.live import Live
from rich.panel import Panel

from devquest.config import get as config_get
from devquest.ui import border_style, console

LUMINANCE = ".,-~:;=!*#$@"
FRAMES = 30
FRAME_SLEEP = 0.05

SHAPES = {
    "orb": {"R1": 0.4, "R2": 1.0, "kind": "torus"},
    "siege": {"R1": 0.25, "R2": 0.85, "kind": "sphere"},
}


def _torus_point(theta, phi, A, B, R1, R2):
    costheta = math.cos(theta)
    sintheta = math.sin(theta)
    cosphi = math.cos(phi)
    sinphi = math.sin(phi)

    circlex = R2 + R1 * costheta
    x = circlex * (math.cos(B) * cosphi + math.sin(A) * math.sin(B) * sinphi)
    y = circlex * (math.sin(phi) * math.cos(B) + math.sin(A) * math.sin(B) * cosphi)
    z = R1 * sintheta * math.cos(A) + R2 * math.sin(A)

    luminance = (
        cosphi * costheta * math.sin(B)
        - math.cos(A) * costheta * sinphi
        - math.sin(A) * sintheta
        + math.cos(B)
        * (math.cos(A) * sintheta - costheta * math.sin(A) * sinphi)
    )

    return x, y, z, luminance


def _sphere_point(theta, phi, A, B, radius):
    cosphi = math.cos(phi)
    sinphi = math.sin(phi)
    costheta = math.cos(theta)
    sintheta = math.sin(theta)

    x = radius * cosphi * costheta
    y = radius * sinphi
    z = radius * cosphi * sintheta

    xr = x * math.cos(B) + z * math.sin(B)
    zr = -x * math.sin(B) + z * math.cos(B)
    yr = y * math.cos(A) - zr * math.sin(A)
    zr = y * math.sin(A) + zr * math.cos(A)

    nx = cosphi * costheta
    ny = sinphi
    nz = cosphi * sintheta

    luminance = nx * math.cos(B) + ny * math.sin(A) + nz * math.cos(A)

    return xr, yr, zr, luminance


def render_frame(
    shape: str,
    A: float,
    B: float,
    width: int = 40,
    height: int = 20,
) -> str:
    preset = SHAPES.get(shape, SHAPES["orb"])
    R1 = preset["R1"]
    R2 = preset["R2"]
    kind = preset["kind"]

    K2 = 5
    K1 = width * K2 * 3 / (4 * (R1 + R2 if kind == "torus" else R2))

    output = [[" " for _ in range(width)] for _ in range(height)]
    zbuffer = [0.0] * (width * height)

    theta_step = 0.07
    phi_step = 0.02

    theta = 0.0
    while theta < 2 * math.pi:
        phi = 0.0
        while phi < 2 * math.pi:
            if kind == "torus":
                x, y, z, luminance = _torus_point(theta, phi, A, B, R1, R2)
            else:
                x, y, z, luminance = _sphere_point(theta, phi, A, B, R2)

            ooz = 1 / (K2 + z)
            xp = int(width / 2 + K1 * ooz * x)
            yp = int(height / 2 - K1 * ooz * y)

            if 0 <= xp < width and 0 <= yp < height:
                idx = yp * width + xp
                if ooz > zbuffer[idx]:
                    zbuffer[idx] = ooz
                    lum_idx = int((luminance + 1) * 4)
                    lum_idx = max(0, min(lum_idx, len(LUMINANCE) - 1))
                    output[yp][xp] = LUMINANCE[lum_idx]

            phi += phi_step
        theta += theta_step

    return "\n".join("".join(row) for row in output)


def play_spin(shape: str = "orb", title: str = "", frames: int = FRAMES) -> None:
    if not config_get("animations"):
        return

    if not sys.stdout.isatty():
        return

    preset = SHAPES.get(shape, SHAPES["orb"])
    spin_a = 0.04 if preset["kind"] == "torus" else 0.03
    spin_b = 0.02

    A = 0.0
    B = 0.0

    with Live(console=console, refresh_per_second=20, transient=True) as live:
        for _ in range(frames):
            frame = render_frame(shape, A, B)
            live.update(
                Panel(
                    frame,
                    title=title or " ",
                    border_style=border_style(),
                    padding=(0, 1),
                )
            )
            A += spin_a
            B += spin_b
            time.sleep(FRAME_SLEEP)
