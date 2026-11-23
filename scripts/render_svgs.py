"""Render every profile card in light and dark from data/stats.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path

from cards import areas, cta, hero, now, rhythm, stack
from cards.theme import THEMES

ROOT = Path(__file__).resolve().parent.parent
CARDS = {"hero": hero, "cta": cta, "areas": areas, "rhythm": rhythm, "now": now, "stack": stack}


def main() -> int:
    stats = json.loads((ROOT / "data" / "stats.json").read_text(encoding="utf-8"))
    out = ROOT / "assets"
    out.mkdir(exist_ok=True)
    for name, module in CARDS.items():
        for theme in THEMES:
            (out / f"{name}-{theme.name}.svg").write_text(module.build(theme, stats), encoding="utf-8", newline="\n")
    print(f"rendered {len(CARDS) * len(THEMES)} cards")
    return 0


if __name__ == "__main__":
    sys.exit(main())
