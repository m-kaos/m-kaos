"""Stack card: the tools I reach for, grouped by layer."""
from __future__ import annotations

from cards.theme import PAD, Theme, card, document, text

LAYERS = (
    ("Build", ("TypeScript", "Next.js", "React", "Tailwind CSS v4", "shadcn/ui", "Motion", "GSAP")),
    ("Data", ("PostgreSQL", "Supabase", "Drizzle", "Payload CMS", "Python")),
    ("Automate", ("Claude Code", "MCP", "n8n", "Kommo CRM", "WhatsApp")),
    ("Sell", ("Shopify Liquid", "Klaviyo", "Wix")),
    ("Ship", ("Vercel", "Cloudflare Workers", "Docker", "VPS")),
)
ROW = 64
TOP = 56
CHIP_H = 42
CHIP_X0 = PAD + 168
FONT = 17
CHAR_W = FONT * 0.6  # monospace advance
GAP = 12
HEIGHT = TOP * 2 + ROW * (len(LAYERS) - 1) + CHIP_H


def build(t: Theme, s: dict) -> str:
    body = [card(t, HEIGHT)]
    for row, (layer, tools) in enumerate(LAYERS):
        cy = TOP + row * ROW + CHIP_H / 2
        body.append(text(PAD, round(cy + 5, 2), layer.upper(), size=14, fill=t.dim, mono=True, spacing=1.5))
        x = CHIP_X0
        for tool in tools:
            w = round(len(tool) * CHAR_W + 32, 2)
            body.append(f'<rect x="{x}" y="{round(cy - CHIP_H / 2, 2)}" width="{w}" height="{CHIP_H}" rx="10" '
                        f'fill="{t.chip}" stroke="{t.border}"/>')
            body.append(text(round(x + w / 2, 2), round(cy + 6, 2), tool, size=FONT, fill=t.fg, mono=True,
                             anchor="middle"))
            x = round(x + w + GAP, 2)
    desc = " ".join(f"{layer}: {', '.join(tools)}." for layer, tools in LAYERS)
    return document(HEIGHT, "Stack", desc, body)
