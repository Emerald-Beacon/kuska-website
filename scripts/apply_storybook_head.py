#!/usr/bin/env python3
"""Point every page at the storybook fonts and stylesheet. Safe to re-run."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "kuska-website"
FONT_URL = (
    "https://fonts.googleapis.com/css2?family=Caveat:wght@500;700"
    "&family=Fraunces:opsz,wght,SOFT,WONK@9..144,500..700,0..100,0..1"
    "&family=Montserrat:wght@400;500;600;700;800&display=swap"
)
SITE_LINK = '<link rel="stylesheet" href="/site.css">'
STORY_LINK = '<link rel="stylesheet" href="/storybook.css">'


def pages():
    out = [ROOT / "index.html", ROOT / "404.html"]
    out += sorted(p for p in ROOT.glob("*/index.html") if p.parent.name != "feed")
    return out


def main():
    changed = 0
    for page in pages():
        html = page.read_text(encoding="utf-8")
        new = re.sub(
            r'href="https://fonts\.googleapis\.com/css2\?[^"]*"',
            f'href="{FONT_URL}"',
            html,
            count=1,
        )
        if STORY_LINK not in new:
            if SITE_LINK not in new:
                raise SystemExit(f"{page}: no {SITE_LINK} to anchor on")
            indent = re.search(r"([ \t]*)" + re.escape(SITE_LINK), new).group(1)
            new = new.replace(SITE_LINK, f"{SITE_LINK}\n{indent}{STORY_LINK}", 1)
        if new != html:
            page.write_text(new, encoding="utf-8")
            changed += 1
    print(f"updated {changed} of {len(pages())} pages")


if __name__ == "__main__":
    main()
