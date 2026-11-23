"""Building-now card: KAOS, the personal AI system, as a small node diagram."""
from __future__ import annotations

import math

from cards.theme import PAD, Theme, card, document, text

HEIGHT = 480
CENTER = (830, 246)
RADIUS_X, RADIUS_Y = 210, 150  # an ellipse keeps the two bottom nodes apart
NODE_W, NODE_H = 196, 62

PARTS = (
    ("Brain", "thinks with Claude"),
    ("Memory", "one shared memory"),
    ("Hands", "runs jobs on a VPS"),
    ("Voice", "panel and WhatsApp"),
    ("World model", "of itself and the world"),
)

CSS = """
    .pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.8s ease-out infinite}
    @keyframes pulse{0%{transform:scale(1);opacity:.55}100%{transform:scale(1.9);opacity:0}}"""


def _node(t: Theme, x: float, y: float, title: str, sub: str) -> list[str]:
    left, top = round(x - NODE_W / 2, 2), round(y - NODE_H / 2, 2)
    return [
        f'<rect x="{left}" y="{top}" width="{NODE_W}" height="{NODE_H}" rx="14" fill="{t.chip}" stroke="{t.border}"/>',
        text(round(x, 2), round(y - 3, 2), title, size=18, fill=t.fg, weight=600, anchor="middle"),
        text(round(x, 2), round(y + 19, 2), sub, size=14, fill=t.muted, anchor="middle"),
    ]


def build(t: Theme, s: dict) -> str:
    cx, cy = CENTER
    points = [
        (cx + RADIUS_X * math.cos(math.radians(-90 + 72 * i)), cy + RADIUS_Y * math.sin(math.radians(-90 + 72 * i)))
        for i in range(len(PARTS))
    ]
    body = [
        card(t, HEIGHT),
        text(PAD - 3, 152, "KAOS", size=76, fill=t.fg, weight=700, spacing=-2),
        text(PAD, 198, "My personal AI system.", size=24, fill=t.muted),
        text(PAD, 232, "One assistant, self-hosted.", size=24, fill=t.muted),
        text(PAD - 2, 384, f"{s['kaos_commits']:,}", size=64, fill=t.accent, weight=700, spacing=-2, cls="num"),
        text(PAD, 418, "commits in the last 12 months", size=18, fill=t.muted),
    ]
    body += [f'<line x1="{cx}" y1="{cy}" x2="{round(x, 2)}" y2="{round(y, 2)}" stroke="{t.border}" stroke-width="1.5"/>'
             for x, y in points]
    body += [
        f'<circle class="pulse" cx="{cx}" cy="{cy}" r="52" fill="none" stroke="{t.accent}" stroke-width="2"/>',
        f'<circle cx="{cx}" cy="{cy}" r="52" fill="{t.bg}" stroke="{t.accent}" stroke-width="2"/>',
        text(cx, cy + 7, "KAOS", size=20, fill=t.fg, mono=True, weight=600, anchor="middle", spacing=1),
    ]
    for (x, y), (title, sub) in zip(points, PARTS):
        body += _node(t, x, y, title, sub)

    desc = ("KAOS, my personal AI system: one self-hosted assistant with a shared memory, a model of itself and "
            "the world, a voice in its own panel and on WhatsApp, a brain that thinks with Claude and hands that "
            f"run jobs on a VPS. {s['kaos_commits']:,} commits in the last 12 months.")
    return document(HEIGHT, "KAOS — my personal AI system", desc, body, CSS)
