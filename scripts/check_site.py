#!/usr/bin/env python3
"""Static checks for the Kuska site.

Run from the git root:  python3 -I scripts/check_site.py
Exits 0 when every check passes; otherwise prints each failure and exits 1.
"""
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "kuska-website"

FONT_URL = (
    "https://fonts.googleapis.com/css2?family=Caveat:wght@500;700"
    "&family=Fraunces:opsz,wght,SOFT,WONK@9..144,500..700,0..100,0..1"
    "&family=Montserrat:wght@400;500;600;700;800&display=swap"
)


def site_pages():
    pages = [ROOT / "index.html", ROOT / "404.html"]
    pages += sorted(p for p in ROOT.glob("*/index.html") if p.parent.name != "feed")
    return pages


class Element:
    def __init__(self, tag, attrs):
        self.tag = tag
        self.attrs = attrs
        self.classes = set((attrs.get("class") or "").split())


class Doc(HTMLParser):
    _cache = {}

    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.elements = []
        self._depth = {"h1": 0, "main": 0}
        self._text = {"h1": [], "main": []}
        self.raw = path.read_text(encoding="utf-8")
        self.feed(self.raw)

    @classmethod
    def load(cls, path):
        if path not in cls._cache:
            cls._cache[path] = cls(path)
        return cls._cache[path]

    def handle_starttag(self, tag, attrs):
        self.elements.append(Element(tag, {k: (v or "") for k, v in attrs}))
        if tag in self._depth:
            self._depth[tag] += 1

    def handle_endtag(self, tag):
        if tag in self._depth and self._depth[tag] > 0:
            self._depth[tag] -= 1

    def handle_data(self, data):
        for key, depth in self._depth.items():
            if depth:
                self._text[key].append(data)

    def find(self, tag=None, cls=None):
        return [
            e for e in self.elements
            if (tag is None or e.tag == tag) and (cls is None or cls in e.classes)
        ]

    def text_of(self, key):
        text = " ".join(self._text[key]).replace("’", "'")
        return re.sub(r"\s+", " ", text).strip()


def rel(path):
    return str(path.relative_to(ROOT))


def local_target(url):
    url = url.split("#", 1)[0].split("?", 1)[0]
    if not url.startswith("/") or url.startswith("//"):
        return None
    target = ROOT / url.lstrip("/")
    if url.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


def contrast(hex_a, hex_b):
    def lum(h):
        h = h.lstrip("#")
        chans = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
        chans = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in chans]
        return 0.2126 * chans[0] + 0.7152 * chans[1] + 0.0722 * chans[2]

    a, b = lum(hex_a), lum(hex_b)
    return (max(a, b) + 0.05) / (min(a, b) + 0.05)


# ---------------------------------------------------------------- site-wide

def check_head():
    failures = []
    for page in site_pages():
        doc = Doc.load(page)
        hrefs = [e.attrs.get("href", "") for e in doc.find("link")]
        if FONT_URL not in hrefs:
            failures.append(f"{rel(page)}: missing storybook Google Fonts link")
        if "Montserrat+Alternates" in doc.raw:
            failures.append(f"{rel(page)}: still loads Montserrat Alternates")
        sheets = [e.attrs.get("href") for e in doc.find("link") if e.attrs.get("rel") == "stylesheet"]
        if "/site.css" not in sheets or "/storybook.css" not in sheets:
            failures.append(f"{rel(page)}: must link /site.css and /storybook.css")
        elif sheets.index("/storybook.css") < sheets.index("/site.css"):
            failures.append(f"{rel(page)}: /storybook.css must load after /site.css")
    return failures


def check_local_refs():
    failures = []
    for page in site_pages():
        for el in Doc.load(page).elements:
            urls = [el.attrs.get(k, "") for k in ("src", "href", "xlink:href")]
            urls += [part.strip().split(" ")[0] for part in el.attrs.get("srcset", "").split(",") if part.strip()]
            for url in urls:
                target = local_target(url)
                if target is not None and not target.exists():
                    failures.append(f"{rel(page)}: broken local reference {url}")
    return failures


def check_img_alt():
    failures = []
    for page in site_pages():
        for img in Doc.load(page).find("img"):
            if "alt" not in img.attrs:
                failures.append(f"{rel(page)}: <img src={img.attrs.get('src')}> has no alt")
    return failures


def check_css_base():
    failures = []
    site_css = (ROOT / "site.css").read_text(encoding="utf-8")
    if "Montserrat Alternates" in site_css:
        failures.append("site.css: still references Montserrat Alternates")
    story = ROOT / "storybook.css"
    if not story.exists():
        failures.append("storybook.css: missing")
    elif "@media (prefers-reduced-motion: reduce)" not in story.read_text(encoding="utf-8"):
        failures.append("storybook.css: missing prefers-reduced-motion block")
    return failures


TOKENS_REQUIRED = {
    "cream": "#fff8ec", "sky": "#b7d9f3", "sun": "#ebc94e", "kuska-blue": "#3989c9",
    "sage": "#8fbf9f", "coral": "#f08a6c", "deep-blue": "#004e85", "twilight": "#5b5aa6",
    "star-gold": "#f6d77a", "night": "#0b2a47", "mist": "#eaf3fb", "ink": "#17344a",
}

# (foreground token, background token, minimum ratio)
CONTRAST_PAIRS = [
    ("ink", "cream", 4.5), ("ink", "sky", 4.5), ("ink", "sun", 4.5), ("ink", "mist", 4.5),
    ("deep-blue", "cream", 4.5), ("deep-blue", "mist", 4.5), ("deep-blue", "sun", 4.5),
    ("brand-muted", "cream", 4.5),
    ("mist", "night", 4.5), ("star-gold", "night", 4.5), ("star-gold", "deep-blue", 4.5),
    ("mist", "twilight", 4.5),
    ("kuska-blue", "cream", 3.0),  # large display text only
]


def check_tokens_and_contrast():
    failures = []
    css = (ROOT / "site.css").read_text(encoding="utf-8")
    root = re.search(r":root\s*{(.*?)}", css, re.S)
    tokens = dict(re.findall(r"--([\w-]+):\s*(#[0-9a-fA-F]{6})", root.group(1) if root else ""))
    tokens = {k: v.lower() for k, v in tokens.items()}
    tokens.setdefault("mist", "#eaf3fb")
    for name, value in TOKENS_REQUIRED.items():
        if tokens.get(name) != value:
            failures.append(f"site.css :root: --{name} should be {value}, found {tokens.get(name)}")
    for fg, bg, minimum in CONTRAST_PAIRS:
        if fg in tokens and bg in tokens:
            ratio = contrast(tokens[fg], tokens[bg])
            if ratio < minimum:
                failures.append(f"contrast --{fg} on --{bg} is {ratio:.2f}, needs {minimum}")
    return failures


SPRITE_IDS = {"hills-back", "hills-front", "wasatch", "cloud", "sun", "moon",
              "star", "heart", "flower", "trail", "edge-wave"}


def check_sprite():
    failures = []
    sprite = ROOT / "images/storybook/illustrations.svg"
    if not sprite.exists():
        return ["images/storybook/illustrations.svg: missing"]
    ids = set(re.findall(r'<symbol[^>]*\bid="([\w-]+)"', sprite.read_text(encoding="utf-8")))
    for missing in sorted(SPRITE_IDS - ids):
        failures.append(f"illustrations.svg: missing symbol #{missing}")
    if not (ROOT / "images/storybook/stars-tile.svg").exists():
        failures.append("images/storybook/stars-tile.svg: missing")
    for page in site_pages():
        for el in Doc.load(page).elements:
            href = el.attrs.get("href", "")
            if el.tag == "use" and "#" in href:
                if href.split("#", 1)[1] not in ids:
                    failures.append(f"{rel(page)}: <use> points at unknown symbol {href}")
    return failures


CHECKS = [
    check_head,
    check_local_refs,
    check_img_alt,
    check_css_base,
    check_tokens_and_contrast,
    check_sprite,
]


def main():
    failures = []
    for check in CHECKS:
        failures += check()
    for failure in failures:
        print(f"FAIL {failure}")
    print(f"{len(CHECKS)} checks, {len(failures)} failures")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
