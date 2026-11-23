"""Hero card: name, yearly numbers and one bar per day of commits."""
from __future__ import annotations

import math
from datetime import date, timedelta

from cards.theme import PAD, WIDTH, Theme, card, document, text

HEIGHT = 524
BASE, MAX_H = 464, 80
PITCH = (WIDTH - 2 * PAD) / 365
BAR_W = round(PITCH * 0.6, 2)
HOT = 40  # days with this many commits or more are drawn in the accent

TRAVEL = WIDTH - 2 * PAD
# A playhead sweeps the year once. Bars never depend on the animation, so a
# renderer that freezes at t=0 still shows the full chart.
CSS = f"""
    .playhead{{animation:play 2.6s cubic-bezier(.45,0,.25,1) .3s both}}
    @keyframes play{{0%{{transform:translateX(0);opacity:0}}6%{{opacity:1}}90%{{transform:translateX({TRAVEL}px);opacity:1}}100%{{transform:translateX({TRAVEL}px);opacity:0}}}}"""


def _bars(t: Theme, daily: list[int], peak: int) -> list[str]:
    out = []
    for i, count in enumerate(daily):
        x = round(PAD + i * PITCH, 2)
        if count == 0:
            out.append(f'<rect x="{x}" y="{BASE - 2}" width="{BAR_W}" height="2" fill="{t.faint}"/>')
            continue
        h = round(4 + (MAX_H - 4) * math.sqrt(count / peak), 2)
        color = t.accent if count >= HOT else t.bar
        out.append(f'<rect x="{x}" y="{round(BASE - h, 2)}" width="{BAR_W}" height="{h}" rx="0.6" fill="{color}"/>')
    return out


def _months(t: Theme, start: date) -> list[str]:
    out = []
    for i in range(365):
        day = start + timedelta(days=i)
        if day.day == 1:
            x = round(PAD + i * PITCH, 2)
            out.append(text(x, BASE + 32, day.strftime("%b").upper(), size=13, fill=t.dim, mono=True, spacing=1))
    return out


def _stats(t: Theme, s: dict) -> list[str]:
    items = [
        (f"{s['commits']:,}", "commits"),
        (str(s["repositories"]), "repositories"),
        (str(s["active_days"]), "active days"),
        (str(s["longest_streak"]), "day longest streak"),
    ]
    out = []
    for n, (value, label) in enumerate(items):
        x = PAD + n * 270
        out.append(text(x, 296, value, size=48, fill=t.fg, weight=600, spacing=-1.5, cls="num"))
        out.append(text(x, 326, label, size=17, fill=t.muted))
    return out


def build(t: Theme, s: dict) -> str:
    daily: list[int] = s["daily"]
    start, end = date.fromisoformat(s["start"]), date.fromisoformat(s["end"])
    peak = max(daily) or 1
    peak_i = daily.index(peak)
    peak_day = start + timedelta(days=peak_i)
    px = round(PAD + peak_i * PITCH + BAR_W / 2, 2)
    period = f"{start.strftime('%b %Y')} — {end.strftime('%b %Y')}"

    body = [
        card(t, HEIGHT),
        text(PAD, 80, "m-kaos  ·  Monterrey, MX", size=16, fill=t.muted, mono=True, spacing=0.5),
        text(WIDTH - PAD, 80, period, size=16, fill=t.muted, mono=True, anchor="end", spacing=0.5),
        text(PAD - 4, 168, "Mauricio Guerra", size=80, fill=t.fg, weight=700, spacing=-2.5),
        text(PAD, 212, "Full-stack developer · systems, AI agents and commerce", size=26, fill=t.muted),
        *_stats(t, s),
        '<g>',
        f'  <line x1="{px}" y1="{BASE - MAX_H - 2}" x2="{px}" y2="{BASE - MAX_H - 10}" stroke="{t.accent}" stroke-width="1.5"/>',
        "  " + text(round(px - 8, 2), BASE - MAX_H - 8, f"{peak} commits · {peak_day.strftime('%b')} {peak_day.day}",
                    size=14, fill=t.muted, mono=True, anchor="end"),
        "</g>",
        "<g>",
        *(f"  {bar}" for bar in _bars(t, daily, peak)),
        "</g>",
        f'<line class="playhead" x1="{PAD}" y1="{BASE - MAX_H - 6}" x2="{PAD}" y2="{BASE + 4}" stroke="{t.accent}" stroke-width="2"/>',
        *_months(t, start),
    ]
    desc = (f"Last 12 months: {s['commits']:,} commits across {s['repositories']} repositories on "
            f"{s['active_days']} active days, {s['longest_streak']}-day longest streak. Each bar is one day; "
            f"the peak was {peak} commits on {peak_day.strftime('%B')} {peak_day.day}, {peak_day.year}.")
    return document(HEIGHT, "Mauricio Guerra — full-stack developer, Monterrey, MX", desc, body, CSS)
