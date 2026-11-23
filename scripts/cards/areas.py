"""What-I-build card: three areas of work with a few concrete examples each."""
from __future__ import annotations

from cards.theme import PAD, WIDTH, Theme, card, document, icon, text

HEIGHT = 312
COLUMN = (WIDTH - 2 * PAD) / 3

AREAS = (
    (
        "Systems",
        '<rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/>'
        '<rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/>',
        ("Clinical records and scheduling", "Self-serve quoting panels", "WhatsApp sales copilots"),
    ),
    (
        "AI agents",
        '<path d="M12 8V4H8"/><rect width="16" height="12" x="4" y="8" rx="2"/><path d="M2 14h2"/>'
        '<path d="M20 14h2"/><path d="M15 13v2"/><path d="M9 13v2"/>',
        ("Bid intelligence agent", "WhatsApp agents on n8n + Kommo", "KAOS, my own AI system"),
    ),
    (
        "Web and commerce",
        '<circle cx="12" cy="12" r="10"/><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"/>'
        '<path d="M2 12h20"/>',
        ("Next.js sites and landings", "Shopify themes, Klaviyo flows", "Vercel and Cloudflare Workers"),
    ),
)


def build(t: Theme, s: dict) -> str:
    body = [card(t, HEIGHT)]
    for n, (title, paths, lines) in enumerate(AREAS):
        x = round(PAD + n * COLUMN + (24 if n else 0), 2)
        if n:
            divider_x = round(PAD + n * COLUMN, 2)
            body.append(f'<line x1="{divider_x}" y1="56" x2="{divider_x}" y2="{HEIGHT - 56}" stroke="{t.border}"/>')
        body.append(icon(paths, x, 56, 30, t.accent))
        body.append(text(x, 140, title, size=28, fill=t.fg, weight=600, spacing=-0.5))
        for i, line in enumerate(lines):
            body.append(text(x, 186 + i * 34, line, size=20, fill=t.muted))
    desc = " ".join(f"{title}: {', '.join(lines)}." for title, _, lines in AREAS)
    return document(HEIGHT, "What I build", desc, body)
