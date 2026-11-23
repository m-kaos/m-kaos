"""Portfolio call-to-action card."""
from __future__ import annotations

from cards.theme import PAD, WIDTH, Theme, card, document, icon, text

HEIGHT = 156
URL = "dev.maugn.com"
ARROW = '<path d="M7 7h10v10"/><path d="M7 17 17 7"/>'  # lucide: arrow-up-right


def build(t: Theme, s: dict) -> str:
    cx, cy, r = WIDTH - PAD - 44, HEIGHT / 2, 44
    body = [
        card(t, HEIGHT),
        text(PAD, 66, "Portfolio", size=16, fill=t.muted, mono=True, spacing=0.5),
        text(PAD - 2, 112, URL, size=46, fill=t.fg, weight=700, spacing=-1.2),
        text(cx - r - 28, cy + 7, "Featured work and contact", size=20, fill=t.muted, anchor="end"),
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{t.accent}"/>',
        icon(ARROW, cx - 16, cy - 16, 32, "#FFFFFF"),
    ]
    return document(HEIGHT, f"Portfolio — {URL}", f"Link to the portfolio at {URL}.", body)
