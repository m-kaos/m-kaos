"""Shared palette, fonts and SVG primitives for the profile cards."""
from __future__ import annotations

from dataclasses import dataclass
from html import escape

WIDTH = 1200
PAD = 64
SANS = "'General Sans',-apple-system,BlinkMacSystemFont,'Segoe UI',Inter,Helvetica,Arial,sans-serif"
MONO = "'Geist Mono',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"


@dataclass(frozen=True)
class Theme:
    name: str
    bg: str
    chip: str
    border: str
    fg: str
    muted: str
    dim: str
    bar: str
    faint: str
    accent: str


THEMES = (
    Theme("dark", "#121212", "#1A1A1A", "#262626", "#FAFAFA", "#A3A3A3", "#737373", "#8A8A8A", "#2A2A2A", "#EF4444"),
    Theme("light", "#FFFFFF", "#F5F5F5", "#E5E5E5", "#0A0A0A", "#525252", "#737373", "#525252", "#E5E5E5", "#DC2626"),
)

BASE_CSS = f"""
    .sans{{font-family:{SANS}}}
    .mono{{font-family:{MONO}}}
    .num{{font-variant-numeric:tabular-nums}}"""
REDUCED_MOTION = "\n    @media (prefers-reduced-motion:reduce){*{animation:none!important}}"


def document(height: int, title: str, desc: str, body: list[str], css: str = "") -> str:
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" aria-labelledby="t d">',
        f'  <title id="t">{escape(title)}</title>',
        f'  <desc id="d">{escape(desc)}</desc>',
        f"  <style>{BASE_CSS}{css}{REDUCED_MOTION}\n  </style>",
        *(f"  {line}" for line in body),
        "</svg>",
    ]
    return "\n".join(lines) + "\n"


def card(t: Theme, height: int) -> str:
    return f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="24" fill="{t.bg}" stroke="{t.border}"/>'


def text(x: float, y: float, content: str, *, size: int, fill: str, mono: bool = False,
         weight: int | None = None, anchor: str | None = None, spacing: float | None = None,
         cls: str = "") -> str:
    classes = " ".join(c for c in ("mono" if mono else "sans", cls) if c)
    attrs = [f'x="{x}"', f'y="{y}"', f'class="{classes}"', f'font-size="{size}"', f'fill="{fill}"']
    if weight:
        attrs.append(f'font-weight="{weight}"')
    if anchor:
        attrs.append(f'text-anchor="{anchor}"')
    if spacing is not None:
        attrs.append(f'letter-spacing="{spacing}"')
    return f'<text {" ".join(attrs)}>{escape(content)}</text>'


def icon(paths: str, x: float, y: float, size: int, stroke: str) -> str:
    """Draw a 24x24 Lucide icon (ISC license) at the given size."""
    scale = round(size / 24, 4)
    return (f'<g transform="translate({x} {y}) scale({scale})" fill="none" stroke="{stroke}" '
            f'stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round">{paths}</g>')
