"""Building-now card: the projects in progress, names only."""
from __future__ import annotations

from cards.theme import PAD, WIDTH, Theme, card, document, text

PROJECTS = (
    ("SalesHub",),
    ("Agency", "Studio"),
    ("Harü", "Studio"),
    ("Persona", "Club"),
    ("Groovies",),
)
GAP = 18
TILE_W = (WIDTH - 2 * PAD - GAP * (len(PROJECTS) - 1)) / len(PROJECTS)
TILE_H = 148
TOP = 56
HEIGHT = TOP * 2 + TILE_H
FONT = 30
LEADING = 34

CSS = """
    .pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2.4s ease-out infinite}
    @keyframes pulse{0%{transform:scale(1);opacity:.6}100%{transform:scale(3);opacity:0}}"""


def build(t: Theme, s: dict) -> str:
    body = [card(t, HEIGHT)]
    for i, words in enumerate(PROJECTS):
        x = round(PAD + i * (TILE_W + GAP), 2)
        dot_x, dot_y = round(x + 26, 2), TOP + 28
        body += [
            f'<rect x="{x}" y="{TOP}" width="{round(TILE_W, 2)}" height="{TILE_H}" rx="16" fill="{t.chip}" stroke="{t.border}"/>',
            f'<circle class="pulse" style="animation-delay:{i * 0.35:.2f}s" cx="{dot_x}" cy="{dot_y}" r="4.5" fill="{t.accent}"/>',
            f'<circle cx="{dot_x}" cy="{dot_y}" r="4.5" fill="{t.accent}"/>',
        ]
        last_baseline = TOP + TILE_H - 28
        for line, word in enumerate(words):
            y = last_baseline - (len(words) - 1 - line) * LEADING
            body.append(text(round(x + 22, 2), y, word, size=FONT, fill=t.fg, weight=600, spacing=-0.8))
    names = ", ".join(" ".join(words) for words in PROJECTS)
    return document(HEIGHT, "Building now", f"Projects in progress: {names}.", body, CSS)
