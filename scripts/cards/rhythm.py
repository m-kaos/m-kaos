"""When-I-ship card: commits by weekday and hour, Monterrey time."""
from __future__ import annotations

import math

from cards.theme import PAD, WIDTH, Theme, card, document, text

HEIGHT = 470
DAYS = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
DAY_NAMES = ("Mondays", "Tuesdays", "Wednesdays", "Thursdays", "Fridays", "Saturdays", "Sundays")
GRID_X0, GRID_X1 = PAD + 84, WIDTH - PAD - 14
GRID_Y0, ROW = 150, 40
COL = (GRID_X1 - GRID_X0) / 23
MAX_R = 14


def _clock(hour: int) -> str:
    return f"{hour:02d}:00"


def _share(punch: list[list[int]], hours: range) -> int:
    total = sum(map(sum, punch)) or 1
    return round(100 * sum(row[h] for row in punch for h in hours) / total)


def build(t: Theme, s: dict) -> str:
    punch: list[list[int]] = s["punch"]
    peak = max(max(row) for row in punch) or 1
    peak_day, peak_hour = max(((d, h) for d in range(7) for h in range(24)), key=lambda p: punch[p[0]][p[1]])
    late = _share(punch, range(20, 24)) + _share(punch, range(0, 4))

    body = [
        card(t, HEIGHT),
        text(PAD, 84, f"Most commits land on {DAY_NAMES[peak_day]} around {_clock(peak_hour)}",
             size=28, fill=t.fg, weight=600, spacing=-0.5),
        text(PAD, 116, f"Monterrey time · {late}% after 20:00", size=17, fill=t.muted),
    ]
    for d, label in enumerate(DAYS):
        y = GRID_Y0 + d * ROW
        body.append(text(PAD, y + 5, label, size=15, fill=t.muted, mono=True))
        for h in range(24):
            x = round(GRID_X0 + h * COL, 2)
            count = punch[d][h]
            if count == 0:
                body.append(f'<circle cx="{x}" cy="{y}" r="2" fill="{t.faint}"/>')
                continue
            r = round(3 + (MAX_R - 3) * math.sqrt(count / peak), 2)
            if (d, h) == (peak_day, peak_hour):
                body.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t.accent}"/>')
            else:
                opacity = round(0.35 + 0.65 * count / peak, 2)
                body.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{t.bar}" fill-opacity="{opacity}"/>')
    for h in range(0, 24, 3):
        x = round(GRID_X0 + h * COL, 2)
        body.append(text(x, GRID_Y0 + 6 * ROW + 46, _clock(h)[:2], size=14, fill=t.dim, mono=True, anchor="middle"))

    desc = (f"Commits by weekday and hour over the last 12 months, Monterrey time. The busiest slot is "
            f"{DAY_NAMES[peak_day]} around {_clock(peak_hour)}; {late}% of commits land after 20:00.")
    return document(HEIGHT, "When I ship", desc, body)
