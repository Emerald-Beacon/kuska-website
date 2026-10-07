# Kuska Storybook Redesign — Phase 1 (System + Homepage) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give the whole site the "Kuska Valley" storybook look: new fonts, palette, header and footer on every page, plus a fully redesigned homepage. Then commit and deploy.

**Architecture:** This is a static HTML/CSS/JS site with no build step. `site.css` keeps the global base, re-skinned in place: new tokens, Fraunces headings, buttons, cream header with a scalloped edge, and a night-sky footer. A new `storybook.css` holds the illustrated-world components the homepage uses now and interior pages will use in Phase 2. A single SVG sprite (`images/storybook/illustrations.svg`) supplies hills, clouds, stars and doodles through `<use>`. AI-generated vicuña art, approved by the client, lives in `images/storybook/`. The shared header and footer **markup does not change**, so only `<head>` is edited across all 34 pages, by an idempotent script. A stdlib Python checker (`scripts/check_site.py`) is the test suite. Visual behaviour is verified in a real browser.

**Tech Stack:** HTML5, CSS (custom properties, grid, keyframes), vanilla ES5 JS (matches existing `site.js`), inline SVG sprite, Google Fonts (Fraunces, Montserrat, Caveat), Python 3 stdlib for checks, `cwebp`/`magick`/`sips` for images, Higgsfield MCP for art generation, Playwright MCP for browser verification, Lighthouse via `npx`.

**Spec:** `docs/superpowers/specs/2026-10-07-kuska-storybook-redesign-design.md`

## Global Constraints

- Paths in this plan are relative to the git root `Kuska Website/`. The deploy root is `kuska-website/` (Netlify `publish = "kuska-website"`).
- No framework, no build step, no new npm dependencies in the repo.
- **Do not run `scripts/build_custom_site.py`**: it would overwrite the hand-edited pages.
- Pages = `kuska-website/index.html`, `kuska-website/404.html`, and every `kuska-website/*/index.html` **except** `feed/index.html` (RSS). There are 34 pages.
- Header/footer **markup** stays identical on every page. Only `<head>` changes site-wide.
- Preserve on every page: `<title>`, meta description, canonical, `og:`/`twitter:` tags, JSON-LD, `data-page` attribute. Keep `sitemap.xml`, `robots.txt` and `_redirects` unchanged.
- Business facts are verbatim: `(801) 980-7970` / `tel:+18019807970`, `admin@kuska.co`, `95 2200 S, Bountiful, UT 84010`, `12055 S 700 E, Draper, UT 84020`.
- Hero H1 must contain exactly: `ABA Therapy & Autism Evaluations · Bountiful & Draper` and `Your child’s story is just getting started.`
- Homepage `<main>` visible text must be **≤ 380 words** (currently 727).
- Palette tokens (exact hex): cream `#fff8ec`, sky `#b7d9f3`, sun `#ebc94e`, kuska-blue `#3989c9`, sage `#8fbf9f`, coral `#f08a6c`, deep-blue `#004e85`, twilight `#5b5aa6`, star-gold `#f6d77a`, night `#0b2a47`, mist `#eaf3fb`, ink `#17344a`.
- Text contrast must meet WCAG AA: 4.5:1 for body text and 3:1 for large text. `kuska-blue`, `sage`, `coral` and `sun` are **never** used for body-size text on light backgrounds.
- Fonts URL (exact): `https://fonts.googleapis.com/css2?family=Caveat:wght@500;700&family=Fraunces:opsz,wght,SOFT,WONK@9..144,500..700,0..100,0..1&family=Montserrat:wght@400;500;600;700;800&display=swap`
- Caveat (handwritten) is only ever decorative or a duplicate of information available elsewhere.
- Decorative SVG/art: `aria-hidden="true"` (+ `focusable="false"` on `<svg>`), `alt=""` on decorative `<img>`. Photos keep descriptive alt text.
- All motion is disabled under `prefers-reduced-motion: reduce`, and content must never be invisible without JS.
- Every `<img>` inside homepage `<main>` has `width` and `height`. All but the first hero photo have `loading="lazy"`.
- Git: work on local branch `storybook-phase-1`; commit at the end of each task. Push only in Task 13, after verification. The user authorized "commit and deploy" when done.
- Local preview: `python3 -m http.server 8000 --directory kuska-website` from the git root (background), then `http://localhost:8000/`.

## Review Focus

1. **Phone width (375px):** the hero art, vicuña and stickers must not overlap the headline or cause horizontal scroll. Expect `scrollWidth <= innerWidth`. Tested in Task 6, Step 6 and Task 12, Step 2.
2. **JavaScript disabled or slow:** scroll-reveal content must stay visible. Hidden-until-revealed styles only apply under `.can-reveal`, which only JS adds. Tested by a static check in Task 11.
3. **Reduced-motion visitors:** the insurance marquee must show a static, wrapped logo set (not stuck mid-scroll), with the duplicate track hidden, and no drifting or bobbing. Tested in Task 9, Step 6 and Task 11, Step 6.
4. **Interior pages after the global re-skin:** About, Contact (Zoho iframe), a blog post, and 404 must still look intentional with yellow buttons, Fraunces headings and the new header/footer. Tested in Task 4, Step 6.
5. **Mobile sky menu:** it must open full-screen with links reachable by Tab, close with Escape, return focus to the toggle, and release the body scroll lock. Tested in Task 4, Step 7.

---

## File Structure

| File | Status | Responsibility |
|---|---|---|
| `scripts/check_site.py` | Create | Static test suite: head/fonts, local refs, alt text, contrast, sprite, art files, homepage structure and word budget |
| `scripts/apply_storybook_head.py` | Create | Idempotent `<head>` update across all pages (fonts URL + `storybook.css` link) |
| `kuska-website/site.css` | Modify | Tokens, base typography, buttons, header, mobile sky menu, night footer |
| `kuska-website/storybook.css` | Create | Illustrated-world components (scene, skies, photo frames, stickers, cards, trail, marquee, cottages, book cards, starry CTA, reveal, motion) |
| `kuska-website/images/storybook/illustrations.svg` | Create | SVG `<symbol>` sprite |
| `kuska-website/images/storybook/stars-tile.svg` | Create | Repeating star background tile |
| `kuska-website/images/storybook/kuska-*.webp`, `valley-dawn.webp` | Create | Approved AI art |
| `kuska-website/images/storybook/photos/*.webp` | Create | Optimized derivatives of two large photos |
| `kuska-website/index.html` | Modify | Homepage `<main>` rebuilt section by section |
| `kuska-website/site.js` | Modify | Scroll reveal + hero parallax |
| All other page `index.html` + `404.html` | Modify (head only) | Fonts + stylesheet link |

---

### Task 1: Static checker (test harness) + branch

**Files:**
- Create: `scripts/check_site.py`

**Interfaces:**
- Produces: `python3 -I scripts/check_site.py` → exit 0 / exit 1 listing failures. Internals later tasks extend: `ROOT`, `FONT_URL`, `site_pages()`, `Doc(path)` with `.elements` (each has `.tag`, `.attrs`, `.classes`), `.find(tag=None, cls=None)`, `.text_of(key)` for `"h1"`/`"main"`, `.raw`; `CHECKS` list of zero-arg functions returning `list[str]` of failures; helper `contrast(hex_a, hex_b) -> float`.

- [ ] **Step 1: Create the branch**

```bash
P="/Users/joshdennis/Documents/App Projects/Websites/Kuska Website"
git -C "$P" rev-parse --show-toplevel   # must end in /Kuska Website
git -C "$P" status --short              # must be empty apart from docs/
git -C "$P" switch -c storybook-phase-1
```

- [ ] **Step 2: Write the checker with the site-wide checks (these are the failing tests for Task 2)**

Create `scripts/check_site.py`:

```python
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


CHECKS = [
    check_head,
    check_local_refs,
    check_img_alt,
    check_css_base,
    check_tokens_and_contrast,
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
```

- [ ] **Step 3: Run it and confirm it fails only for the expected reasons**

Run: `python3 -I scripts/check_site.py`
Expected: exit 1. Failures are only of these kinds: `missing storybook Google Fonts link` and `still loads Montserrat Alternates` (×34 each), `must link /site.css and /storybook.css` (×34), `site.css: still references Montserrat Alternates`, `storybook.css: missing`, and `--<token> should be …` lines. There should be **no** `broken local reference` or `has no alt` lines (the baseline is clean).

- [ ] **Step 4: Commit**

```bash
git -C "$P" add scripts/check_site.py docs/superpowers/specs/2026-10-07-kuska-storybook-redesign-design.md docs/superpowers/plans/2026-10-07-kuska-storybook-phase-1.md
git -C "$P" commit -m "Add static site checker and storybook redesign spec/plan"
```

---

### Task 2: Tokens, typography, fonts on every page, `storybook.css` shell

**Files:**
- Create: `scripts/apply_storybook_head.py`, `kuska-website/storybook.css`
- Modify: `kuska-website/site.css` (`:root` block lines 1–18; all 5 `font-family: "Montserrat Alternates", sans-serif;` lines 299, 310, 492, 622, 827; heading rule at 304–314; `.eyebrow` at 330–337)
- Modify: `<head>` of all 34 pages (via script)

**Interfaces:**
- Consumes: `check_site.py` from Task 1.
- Produces: CSS custom properties `--cream --sky --sun --kuska-blue --sage --coral --deep-blue --twilight --star-gold --night --mist --ink --font-display --font-body --font-hand`; legacy aliases `--brand-*` still resolve; `storybook.css` linked on every page.

- [ ] **Step 1: Write the head-update script**

Create `scripts/apply_storybook_head.py`:

```python
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
```

- [ ] **Step 2: Run it, then run it again (idempotence)**

Run: `python3 -I scripts/apply_storybook_head.py && python3 -I scripts/apply_storybook_head.py`
Expected: `updated 34 of 34 pages` then `updated 0 of 34 pages`.

Then confirm the diff touched only `<head>`:
Run: `git -C "$P" diff --stat -- kuska-website | tail -1` → `34 files changed, 68 insertions(+), 34 deletions(-)` (2 insertions, 1 deletion each).

- [ ] **Step 3: Create `kuska-website/storybook.css`**

```css
/* Kuska Valley storybook components.
   Loaded after site.css on every page. Homepage uses all of it in Phase 1;
   interior pages adopt components in Phase 2. */

/* Motion off switch — every animated selector added later is listed here. */
@media (prefers-reduced-motion: reduce) {
}
```

- [ ] **Step 4: Replace the `:root` block in `site.css` (lines 1–18)**

```css
:root {
  /* Kuska Valley palette */
  --cream: #fff8ec;
  --sky: #b7d9f3;
  --sun: #ebc94e;
  --kuska-blue: #3989c9;
  --sage: #8fbf9f;
  --coral: #f08a6c;
  --deep-blue: #004e85;
  --twilight: #5b5aa6;
  --star-gold: #f6d77a;
  --night: #0b2a47;
  --mist: #eaf3fb;
  --ink: #17344a;
  --brand-muted: #567184;
  --brand-line: #d7e7f2;
  --brand-cloud: #f4fbff;

  /* Legacy names used throughout the existing rules */
  --brand-blue: var(--kuska-blue);
  --brand-blue-deep: var(--deep-blue);
  --brand-blue-soft: var(--sky);
  --brand-yellow: var(--sun);
  --brand-ink: var(--ink);
  --brand-cream: var(--cream);

  --font-display: "Fraunces", Georgia, "Times New Roman", serif;
  --font-body: "Montserrat", system-ui, sans-serif;
  --font-hand: "Caveat", "Comic Sans MS", cursive;

  --shadow-soft: 0 20px 45px rgba(0, 78, 133, 0.12);
  --shadow-card: 0 12px 30px rgba(16, 55, 80, 0.08);
  --radius-xl: 32px;
  --radius-lg: 24px;
  --radius-md: 18px;
  --radius-sm: 14px;
  --shell: min(1180px, calc(100vw - 40px));
}
```

- [ ] **Step 5: Body and headings**

In `site.css`, replace the `body { … }` rule (lines 31–40 before this task's edits) with:

```css
body {
  margin: 0;
  font-family: var(--font-body);
  color: var(--ink);
  background: var(--cream);
  line-height: 1.72;
}

h1,
h2,
h3,
h4 {
  font-family: var(--font-display);
  font-weight: 600;
  font-variation-settings: "SOFT" 100, "WONK" 1;
  letter-spacing: -0.01em;
}
```

Replace every `font-family: "Montserrat Alternates", sans-serif;` (5 occurrences) with `font-family: var(--font-display);`:

Run this **before** pasting the `h1–h4` rule above, or the count below will read `6`:
`sed -i '' 's/font-family: "Montserrat Alternates", sans-serif;/font-family: var(--font-display);/' kuska-website/site.css && grep -c 'var(--font-display)' kuska-website/site.css`
Expected: `5`. Then paste the `body` and `h1–h4` rules.

In the shared heading rule (`.hero__content h1, .section-heading h2, .split-panel h2, .cta-band h2`), change `letter-spacing: -0.03em;` to `letter-spacing: -0.015em;` and `line-height: 1.12;` to `line-height: 1.08;`.

In `.eyebrow, .meta-line`, change `letter-spacing: 0.18em;` to `letter-spacing: 0.16em;` and `font-weight: 800;` to `font-weight: 700;`.

- [ ] **Step 6: Run the checker**

Run: `python3 -I scripts/check_site.py`
Expected: `5 checks, 0 failures`, exit 0.

- [ ] **Step 7: Commit**

```bash
git -C "$P" add scripts/apply_storybook_head.py kuska-website/storybook.css kuska-website/site.css kuska-website
git -C "$P" status --short   # only kuska-website/ files + scripts/ — nothing outside the project
git -C "$P" commit -m "Storybook tokens, Fraunces/Caveat fonts, storybook.css on every page"
```

---

### Task 3: SVG illustration library

**Files:**
- Create: `kuska-website/images/storybook/illustrations.svg`, `kuska-website/images/storybook/stars-tile.svg`
- Modify: `scripts/check_site.py` (add `check_sprite`)

**Interfaces:**
- Produces: sprite symbol ids, referenced as `/images/storybook/illustrations.svg#<id>`: `hills-back`, `hills-front`, `wasatch`, `cloud`, `sun`, `moon`, `star`, `heart`, `flower`, `trail`, `edge-wave`. All fill/stroke with `currentColor` (colour comes from CSS `color`). Landscape symbols use `preserveAspectRatio="none"` so they stretch to their box. Background tile: `/images/storybook/stars-tile.svg`.

- [ ] **Step 1: Add the failing check**

Append to `scripts/check_site.py` above `CHECKS`, and add `check_sprite` to `CHECKS`:

```python
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
```

Run: `python3 -I scripts/check_site.py` → expect `FAIL images/storybook/illustrations.svg: missing`.

- [ ] **Step 2: Create the sprite `kuska-website/images/storybook/illustrations.svg`**

```svg
<svg xmlns="http://www.w3.org/2000/svg">
  <symbol id="hills-back" viewBox="0 0 1440 320" preserveAspectRatio="none">
    <path fill="currentColor" d="M0 220C180 150 320 120 480 170C640 220 760 120 920 110C1080 100 1220 170 1440 140V320H0Z"/>
  </symbol>
  <symbol id="hills-front" viewBox="0 0 1440 320" preserveAspectRatio="none">
    <path fill="currentColor" d="M0 250C200 190 360 225 540 245C720 265 860 195 1040 205C1220 215 1320 255 1440 235V320H0Z"/>
  </symbol>
  <symbol id="wasatch" viewBox="0 0 1440 320" preserveAspectRatio="none">
    <path fill="currentColor" d="M0 230L120 150L190 190L300 70L380 140L450 100L560 190L660 120L760 170L880 60L980 150L1080 110L1200 180L1310 90L1440 160V320H0Z"/>
    <path fill="#fff" opacity=".85" d="M300 70L336 102L316 98L298 110L276 96ZM880 60L914 94L894 90L876 102L852 88ZM1310 90L1340 117L1322 114L1305 124L1286 110Z"/>
  </symbol>
  <symbol id="cloud" viewBox="0 0 120 60">
    <g fill="currentColor">
      <circle cx="38" cy="36" r="18"/>
      <circle cx="64" cy="26" r="22"/>
      <circle cx="88" cy="38" r="16"/>
      <rect x="20" y="36" width="84" height="20" rx="10"/>
    </g>
  </symbol>
  <symbol id="sun" viewBox="0 0 100 100">
    <circle cx="50" cy="50" r="24" fill="currentColor"/>
    <g stroke="currentColor" stroke-width="6" stroke-linecap="round">
      <path d="M50 6v12M50 82v12M6 50h12M82 50h12M19 19l8 8M73 73l8 8M81 19l-8 8M27 73l-8 8"/>
    </g>
  </symbol>
  <symbol id="moon" viewBox="0 0 100 100">
    <path fill="currentColor" d="M62 12a38 38 0 1 0 26 64A32 32 0 0 1 62 12Z"/>
  </symbol>
  <symbol id="star" viewBox="0 0 24 24">
    <path fill="currentColor" d="M12 1C13 8 16 11 23 12C16 13 13 16 12 23C11 16 8 13 1 12C8 11 11 8 12 1Z"/>
  </symbol>
  <symbol id="heart" viewBox="0 0 24 24">
    <path fill="currentColor" d="M12 21s-7.5-4.6-9.6-9.2C.9 8.4 3 4.5 6.7 4.5c2.1 0 3.6 1.2 4.3 2.6.7-1.4 2.2-2.6 4.3-2.6 3.7 0 5.8 3.9 4.3 7.3C19.5 16.4 12 21 12 21Z"/>
  </symbol>
  <symbol id="flower" viewBox="0 0 24 24">
    <g fill="currentColor">
      <circle cx="12" cy="6" r="4"/>
      <circle cx="17.7" cy="10.2" r="4"/>
      <circle cx="15.5" cy="17" r="4"/>
      <circle cx="8.5" cy="17" r="4"/>
      <circle cx="6.3" cy="10.2" r="4"/>
    </g>
    <circle cx="12" cy="12" r="3.2" fill="#ebc94e"/>
  </symbol>
  <symbol id="trail" viewBox="0 0 1000 200" preserveAspectRatio="none">
    <path d="M20 160C200 40 320 180 500 100S800 30 980 120" fill="none" stroke="currentColor" stroke-width="6" stroke-linecap="round" stroke-dasharray="2 18" vector-effect="non-scaling-stroke"/>
  </symbol>
  <symbol id="edge-wave" viewBox="0 0 1440 80" preserveAspectRatio="none">
    <path fill="currentColor" d="M0 40C240 80 480 0 720 40C960 80 1200 0 1440 40V80H0Z"/>
  </symbol>
</svg>
```

- [ ] **Step 3: Create `kuska-website/images/storybook/stars-tile.svg`**

```svg
<svg xmlns="http://www.w3.org/2000/svg" width="240" height="240" viewBox="0 0 240 240">
  <g fill="#f6d77a">
    <circle cx="18" cy="24" r="1.4" opacity=".9"/>
    <circle cx="92" cy="12" r="1" opacity=".6"/>
    <circle cx="160" cy="40" r="1.6" opacity=".85"/>
    <circle cx="214" cy="18" r="1" opacity=".5"/>
    <circle cx="48" cy="96" r="1.1" opacity=".55"/>
    <circle cx="130" cy="110" r="1.4" opacity=".8"/>
    <circle cx="200" cy="140" r="1" opacity=".5"/>
    <circle cx="26" cy="170" r="1.5" opacity=".85"/>
    <circle cx="104" cy="196" r="1" opacity=".55"/>
    <circle cx="176" cy="220" r="1.3" opacity=".7"/>
    <path d="M70 52c.4 3 1.6 4.2 4.6 4.6-3 .4-4.2 1.6-4.6 4.6-.4-3-1.6-4.2-4.6-4.6 3-.4 4.2-1.6 4.6-4.6Z"/>
    <path d="M222 92c.4 3 1.6 4.2 4.6 4.6-3 .4-4.2 1.6-4.6 4.6-.4-3-1.6-4.2-4.6-4.6 3-.4 4.2-1.6 4.6-4.6Z" opacity=".8"/>
    <path d="M150 168c.4 3 1.6 4.2 4.6 4.6-3 .4-4.2 1.6-4.6 4.6-.4-3-1.6-4.2-4.6-4.6 3-.4 4.2-1.6 4.6-4.6Z" opacity=".9"/>
  </g>
</svg>
```

- [ ] **Step 4: Run the checker**

Run: `python3 -I scripts/check_site.py` → `6 checks, 0 failures`.

- [ ] **Step 5: Visual sanity check of the sprite**

Start the preview server (background): `python3 -m http.server 8000 --directory kuska-website`. Leave it running for the rest of the plan.
Open `http://localhost:8000/images/storybook/illustrations.svg` and `http://localhost:8000/images/storybook/stars-tile.svg` with Playwright (`browser_navigate`). Expected: both load with status 200 and no XML parse error. The sprite renders blank, which is normal because symbols aren't drawn until used.

- [ ] **Step 6: Commit**

```bash
git -C "$P" add kuska-website/images/storybook scripts/check_site.py
git -C "$P" commit -m "Add Kuska Valley SVG sprite and star tile"
```

---

### Task 4: Global re-skin: buttons, scalloped header, mobile sky menu, night footer

**Files:**
- Modify: `kuska-website/site.css`: `.site-header` (≈102–117), `.site-nav__link` hover/active (≈154–160), `.button` rules (≈216–265), `.nav-toggle` (≈274–284), footer block (≈1013–1046), the `@media (max-width: 820px)` nav rules (≈1099–1135), and the reduced-motion block at the end.

**Interfaces:**
- Consumes: tokens (Task 2), `stars-tile.svg` (Task 3).
- Produces: `.button` (sun-yellow chunky pill, ink text), `.button--secondary` (white), **new** `.button--ghost` (for dark sections), night-sky `.site-footer`, full-screen `.site-nav` on ≤820px.

- [ ] **Step 1: Header**

Replace `.site-header { … }`:

```css
.site-header {
  position: sticky;
  top: 0;
  z-index: 30;
  background: var(--cream);
}

/* Scalloped bottom edge — pure CSS, no image request. */
.site-header::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  top: 100%;
  height: 12px;
  background: radial-gradient(circle at 12px 0, var(--cream) 11.5px, transparent 12px) repeat-x;
  background-size: 24px 12px;
  filter: drop-shadow(0 4px 3px rgba(0, 78, 133, 0.08));
  pointer-events: none;
}
```

Replace the two nav-link state rules:

```css
.site-nav__link:hover,
.site-nav__link:focus-visible {
  background: rgba(183, 217, 243, 0.5);
}

.site-nav__link.is-active {
  background: rgba(235, 201, 78, 0.38);
}
```

- [ ] **Step 2: Buttons**

Replace the `.button, .button:visited { … }`, `.button:hover`, and `.button { transition … }` rules with:

```css
.button,
.button:visited {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 52px;
  padding: 0 26px;
  border: 0;
  border-radius: 999px;
  background: var(--sun);
  color: var(--ink);
  text-decoration: none;
  font-weight: 700;
  box-shadow: 0 5px 0 #c9a632, 0 14px 24px rgba(23, 52, 74, 0.14);
  transition: transform 0.18s ease, box-shadow 0.18s ease;
}

.button:hover {
  transform: translateY(-2px);
  box-shadow: 0 7px 0 #c9a632, 0 18px 28px rgba(23, 52, 74, 0.16);
}

.button:active {
  transform: translateY(3px);
  box-shadow: 0 2px 0 #c9a632, 0 8px 14px rgba(23, 52, 74, 0.12);
}
```

Replace `.button--secondary, .button--secondary:visited { … }` and add `.button--ghost`:

```css
.button--secondary,
.button--secondary:visited {
  background: #fff;
  color: var(--deep-blue);
  border: 2px solid var(--sky);
  box-shadow: 0 5px 0 var(--sky);
}

.button--secondary:hover {
  box-shadow: 0 7px 0 var(--sky);
}

.button--ghost,
.button--ghost:visited {
  background: transparent;
  color: #fff;
  border: 2px solid rgba(255, 255, 255, 0.7);
  box-shadow: none;
}

.button--ghost:hover {
  background: rgba(255, 255, 255, 0.12);
  box-shadow: none;
}

.button--ghost:focus-visible {
  outline-color: #fff;
}
```

In `.nav-toggle`, change `border: 1px solid rgba(0, 78, 133, 0.14);` to `border: 2px solid var(--sky);` and `position` is added in Step 4.

- [ ] **Step 3: Night-sky footer**

Replace the footer block (`.site-footer` through `.site-footer__bottom`) with:

```css
.site-footer {
  position: relative;
  margin-top: 30px;
  padding: 80px 0 28px;
  overflow: hidden;
  background:
    url("/images/storybook/stars-tile.svg") repeat,
    linear-gradient(180deg, var(--night) 0%, #071d33 100%);
  color: var(--mist);
}

/* Crescent moon */
.site-footer::before {
  content: "";
  position: absolute;
  top: 34px;
  right: max(24px, 8vw);
  width: 54px;
  height: 54px;
  border-radius: 50%;
  box-shadow: inset -14px 8px 0 0 var(--star-gold);
  transform: rotate(-20deg);
}

/* Second star layer that twinkles */
.site-footer::after {
  content: "";
  position: absolute;
  inset: 0;
  background: url("/images/storybook/stars-tile.svg") repeat;
  background-position: 120px 80px;
  opacity: 0.6;
  animation: kuska-twinkle 5s ease-in-out infinite alternate;
  pointer-events: none;
}

@keyframes kuska-twinkle {
  from { opacity: 0.15; }
  to { opacity: 0.7; }
}

.site-footer .shell {
  position: relative;
  z-index: 1;
}

.site-footer__grid {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr 0.8fr;
  gap: 32px;
}

.site-footer__logo {
  width: min(220px, 100%);
  margin-bottom: 14px;
  padding: 12px 16px;
  border-radius: 18px;
  background: var(--cream);
}

.site-footer .eyebrow {
  color: var(--star-gold);
}

.footer-list {
  display: grid;
  gap: 12px;
}

.footer-list a {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  color: var(--mist);
  text-decoration: none;
}

.footer-list a:hover {
  color: var(--star-gold);
  text-decoration: underline;
}

.site-footer :focus-visible {
  outline-color: var(--star-gold);
}

.site-footer__bottom {
  margin-top: 32px;
  padding-top: 22px;
  border-top: 1px solid rgba(234, 243, 251, 0.15);
  font-size: 0.9rem;
}
```

Add `.site-footer::after` to the existing `@media (prefers-reduced-motion: reduce)` block at the bottom of `site.css`:

```css
  .site-footer::after {
    animation: none;
  }
```

- [ ] **Step 4: Mobile sky menu**

Inside `@media (max-width: 820px)`, replace the `.site-nav { … }` and `body.nav-open .site-nav { … }` rules with:

```css
  .site-brand,
  .nav-toggle {
    position: relative;
    z-index: 2;
  }

  .site-nav {
    display: none;
    position: fixed;
    inset: 0;
    z-index: 1;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 8px;
    padding: 110px 24px 48px;
    overflow-y: auto;
    background: linear-gradient(180deg, var(--sky) 0%, var(--cream) 75%);
  }

  body.nav-open {
    overflow: hidden;
  }

  body.nav-open .site-nav {
    display: flex;
  }

  .site-nav .site-nav__link {
    min-height: 52px;
    padding: 0 20px;
    font-family: var(--font-display);
    font-size: 1.6rem;
  }
```

(Leave the existing `.nav-dropdown, .nav-dropdown__menu { display: contents; }` and `.nav-dropdown__toggle { display: none; }` rules in place.)

- [ ] **Step 5: Static checks still pass**

Run: `python3 -I scripts/check_site.py` → `6 checks, 0 failures`.

- [ ] **Step 6: Browser check: interior pages after re-skin (Review Focus #4)**

With Playwright at 1280×900, navigate to and screenshot each: `/about/`, `/contact/`, `/how-long-does-aba-therapy-last/`, `/404.html`, and the bottom of `/` (`browser_evaluate`: `window.scrollTo(0, document.body.scrollHeight)`).
Expected on every page:
- headings render in Fraunces (`browser_evaluate`: `getComputedStyle(document.querySelector('h1')).fontFamily` starts with `Fraunces`)
- the header is cream with a visible scalloped edge
- primary buttons are yellow with dark text
- the Zoho iframe on `/contact/` still loads
- the footer is a dark starry sky with a crescent moon, gold section labels, and a readable cream logo badge
- no console errors (`browser_console_messages`)
- the interior `.cta-band` (dark blue) still reads well with the yellow button

If anything looks broken, fix it in `site.css` before continuing.

- [ ] **Step 7: Browser check: mobile sky menu (Review Focus #5)**

Resize to 375×812 on `/about/`. Click `button.nav-toggle`.
Expected:
- the menu covers the viewport with the sky gradient
- the logo and toggle stay visible above it
- `document.body.classList.contains('nav-open')` is `true` and `getComputedStyle(document.body).overflow === 'hidden'`
- `browser_press_key` Tab moves through About → Diagnosing → Our Program → FAQs → Blog → Contact
- Escape closes the menu, `document.activeElement` is the `.nav-toggle`, and body overflow is no longer `hidden`

- [ ] **Step 8: Commit**

```bash
git -C "$P" add kuska-website/site.css
git -C "$P" commit -m "Storybook re-skin: chunky buttons, scalloped header, sky menu, night footer"
```

---

### Task 5: Key art: generate, client approval, process

**Files:**
- Create: `kuska-website/images/storybook/kuska-waving.webp`, `kuska-walking.webp`, `kuska-reading.webp`, `kuska-sleeping.webp`, `kuska-pointing.webp`, `valley-dawn.webp` (only if approved), `photos/kuska-team-800.webp`, `photos/drawing-800.webp`
- Modify: `scripts/check_site.py` (add `check_art`)

**Interfaces:**
- Produces: the files above, plus a recorded `width×height` for each (needed in Tasks 6–10). Kuska poses are transparent-background WebP, 720px wide. `valley-dawn.webp` is 1920px wide, opaque.

- [ ] **Step 1: Add the failing check**

```python
ART_FILES = ["kuska-waving.webp", "kuska-walking.webp", "kuska-reading.webp",
             "kuska-sleeping.webp", "kuska-pointing.webp",
             "photos/kuska-team-800.webp", "photos/drawing-800.webp"]


def check_art():
    base = ROOT / "images/storybook"
    return [f"images/storybook/{name}: missing" for name in ART_FILES if not (base / name).exists()]
```

Add `check_art` to `CHECKS`. Run the checker → expect 7 `missing` failures.

- [ ] **Step 2: Photo derivatives (no approval needed)**

```bash
mkdir -p kuska-website/images/storybook/photos
cwebp -q 80 -resize 800 0 kuska-website/wp-content/uploads/2026/04/kuska-team-hero.jpeg -o kuska-website/images/storybook/photos/kuska-team-800.webp
cwebp -q 80 -resize 800 0 kuska-website/wp-content/uploads/2026/01/trying-to-learn-how-to-draw-holding-pencil-speec-2026-01-09-13-51-30-utc.jpg -o kuska-website/images/storybook/photos/drawing-800.webp
sips -g pixelWidth -g pixelHeight kuska-website/images/storybook/photos/*.webp
```

Expected: `kuska-team-800.webp` 800×600, `drawing-800.webp` 800×533. Each file is under 120 KB (`du -k`).

- [ ] **Step 3: Generate the character and scene with Higgsfield**

1. Load the Higgsfield tools (`ToolSearch` `select:mcp__claude_ai_Higgsfield__models_explore,mcp__claude_ai_Higgsfield__generate_image,mcp__claude_ai_Higgsfield__jobs_wait,mcp__claude_ai_Higgsfield__remove_background,mcp__claude_ai_Higgsfield__balance`). Call `balance`, and tell the user the credit cost before generating.
2. `models_explore` → pick an image model that is strong at illustration and accepts a reference image.
3. Every prompt starts with this **style block**:
   > Children's picture-book illustration, modern and upscale. Soft flat shapes, rounded edges, gentle gradients, subtle paper-grain texture. Warm limited palette: cream #FFF8EC, caramel and tan, Kuska blue #3989C9, sun yellow #EBC94E, sage green #8FBF9F, coral #F08A6C. No text, no letters, no watermark, no border.
4. Every character prompt adds this **character block**:
   > A friendly young vicuña named Kuska: cream-and-caramel fleece, big gentle dark eyes, small kind smile, long elegant neck, wearing a soft knitted Kuska-blue scarf. Full body, centered, isolated on a plain white background.
5. Generate **waving** first: "…standing on a small grassy mound, raising one front hoof in a cheerful wave." Generate 4 variations and choose the best one. Use that image as the **reference image** for the remaining poses so the character stays consistent:
   - **walking:** "walking to the right along a path, mid-step, looking back over its shoulder with a smile"
   - **reading:** "sitting on the grass reading an open picture book with a small child of about four leaning against its side, both smiling" (the child should have simple, friendly features)
   - **sleeping:** "curled up asleep on a small grassy hill, eyes closed, one tiny star floating above"
   - **pointing:** "standing and pointing ahead with one front hoof, curious happy expression"
6. **valley-dawn** (style block only, no character block): "Wide panoramic landscape at sunrise: gentle rolling green hills in the foreground blending Andean highlands with Utah's Wasatch mountain peaks lightly dusted with snow, soft peach-and-cream sky, a few puffy clouds, lots of calm empty sky in the upper-left third. No characters." Aspect ratio 16:9.
7. Save every result into a fresh, empty scratch directory (`$SCRATCH/art-raw/`, where `$SCRATCH` is the session scratchpad). Download only the result URLs that Higgsfield returns.

- [ ] **Step 4: Contact sheet → client approval (GATE)**

```bash
magick montage "$SCRATCH"/art-raw/*.png -tile 3x -geometry 520x520+18+18 -background '#FFF8EC' -label '%t' "$SCRATCH"/contact-sheet.png
open "$SCRATCH"/contact-sheet.png
```

Show the user the contact sheet and ask them to approve or reject **each** piece by name (waving, walking, reading, sleeping, pointing, valley-dawn). **Stop until they answer.**
- Rejected pose: regenerate with their feedback and show the sheet again. All 5 poses must be approved before continuing. If after three rounds a pose is still rejected, ask the user how to proceed (drop it from the homepage, or keep iterating).
- `valley-dawn` rejected: skip it. Tasks 6 and 11 say exactly what to omit.

- [ ] **Step 5: Process approved art**

For each approved pose (example shown for waving):

1. Call Higgsfield `remove_background` on the approved image and download the transparent PNG to `$SCRATCH/art-cut/kuska-waving.png`.
2. Convert and check:

```bash
cwebp -q 82 -alpha_q 90 -resize 720 0 "$SCRATCH"/art-cut/kuska-waving.png -o kuska-website/images/storybook/kuska-waving.webp
sips -g pixelWidth -g pixelHeight kuska-website/images/storybook/kuska-waving.webp
```

If `valley-dawn` was approved:
`cwebp -q 78 -resize 1920 0 "$SCRATCH"/art-raw/valley-dawn.png -o kuska-website/images/storybook/valley-dawn.webp`

Record every file's width×height in a scratch note (`$SCRATCH/art-sizes.txt`). Each pose should be ≤ 90 KB, and `valley-dawn.webp` ≤ 220 KB. If a file is larger, lower `-q` in steps of 5.

- [ ] **Step 6: Run the checker** → `7 checks, 0 failures`.

- [ ] **Step 7: Commit**

```bash
git -C "$P" add kuska-website/images/storybook scripts/check_site.py
git -C "$P" commit -m "Add approved Kuska vicuña art and optimized photo derivatives"
```

---

### Task 6: Homepage hero, "Sunrise over the valley"

**Files:**
- Modify: `kuska-website/index.html`: replace `<section class="hero hero--home"> … </section>` (the whole first section inside `<main>`)
- Modify: `kuska-website/storybook.css`: append scene/sky/photo-window/sticker/hero rules
- Modify: `scripts/check_site.py`: add `check_home_hero`

**Interfaces:**
- Consumes: sprite ids `sun cloud wasatch hills-back hills-front star flower heart`; `kuska-waving.webp`; `valley-dawn.webp` (optional).
- Produces: reusable classes `.scene`, `.scene__painting`, `.scene__sun`, `.scene__cloud(--one|--two)`, `.scene__ridge`, `.scene__hills-back`, `.scene__hills`, `.sky--dawn`, `.sky--meadow`, `.photo-window(--arch|--round)`, `.sticker-row`, `.sticker(--sun|--sage|--coral)`, `.kuska`; `data-parallax="<factor>"` attribute (read by Task 11 JS).

- [ ] **Step 1: Add the failing check**

```python
HERO_LABEL = "ABA Therapy & Autism Evaluations · Bountiful & Draper"
HERO_TITLE = "Your child's story is just getting started."


def check_home_hero():
    doc = Doc.load(ROOT / "index.html")
    failures = []
    if len(doc.find("h1")) != 1:
        failures.append(f"index.html: expected exactly one <h1>, found {len(doc.find('h1'))}")
    h1 = doc.text_of("h1")
    for needed in (HERO_LABEL, HERO_TITLE):
        if needed not in h1:
            failures.append(f"index.html: <h1> must contain '{needed}' (found '{h1}')")
    if not doc.find(cls="valley-hero"):
        failures.append("index.html: missing .valley-hero section")
    if len(doc.find("li", "sticker")) != 3:
        failures.append("index.html: hero needs exactly 3 .sticker items")
    exposed = re.findall(r'<svg\b(?![^>]*aria-hidden="true")[^>]*>\s*<use', doc.raw)
    if exposed:
        failures.append(f"index.html: {len(exposed)} sprite <svg> without aria-hidden='true'")
    return failures
```

Add to `CHECKS`. Run → expect the hero failures.

- [ ] **Step 2: Replace the hero markup**

Replace the entire `<section class="hero hero--home"> … </section>` with the block below. **If `valley-dawn.webp` was not approved, delete the one `<img class="scene__painting" …>` line.** Fill `width`/`height` on `kuska-waving.webp` from `$SCRATCH/art-sizes.txt`. Before keeping the alt text, open `happy-parents-and-kids-…-683x1024.jpg` and confirm the alt describes what the photo actually shows; adjust the wording if it doesn't.

```html
        <section class="valley-hero sky--dawn" aria-labelledby="hero-title">
          <div class="scene" aria-hidden="true">
            <img class="scene__painting" src="/images/storybook/valley-dawn.webp" alt="" width="1920" height="1080">
            <svg class="scene__sun" aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#sun"></use></svg>
            <svg class="scene__cloud scene__cloud--one" aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#cloud"></use></svg>
            <svg class="scene__cloud scene__cloud--two" aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#cloud"></use></svg>
            <svg class="scene__ridge" data-parallax="0.12" aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#wasatch"></use></svg>
            <svg class="scene__hills-back" data-parallax="0.06" aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#hills-back"></use></svg>
          </div>
          <div class="shell valley-hero__grid">
            <div class="valley-hero__copy">
              <h1 id="hero-title">
                <span class="valley-hero__label">ABA Therapy &amp; Autism Evaluations · Bountiful &amp; Draper</span>
                <span class="valley-hero__title">Your child’s story is just getting started.</span>
              </h1>
              <p class="valley-hero__lead">Warm, evidence-based care for curious kids and the families who love them.</p>
              <div class="button-row">
                <a class="button" href="/get-started/">Schedule a consultation</a>
                <a class="text-link" href="/diagnostic-service/">Explore evaluations <span aria-hidden="true">→</span></a>
              </div>
              <ul class="sticker-row" aria-label="What families can expect">
                <li class="sticker sticker--sun"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#star"></use></svg>No-waitlist evaluations</li>
                <li class="sticker sticker--sage"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#flower"></use></svg>In-home, clinic &amp; hybrid</li>
                <li class="sticker sticker--coral"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#heart"></use></svg>Parents as partners</li>
              </ul>
            </div>
            <div class="valley-hero__art">
              <figure class="photo-window photo-window--arch valley-hero__photo-a">
                <img src="/wp-content/uploads/2025/11/a-woman-teaching-a-child-how-to-use-a-weighing-bal-2025-10-17-00-47-38-utc-980x653.jpg" alt="A clinician and a young child learning together with a balance scale" width="980" height="653" fetchpriority="high">
              </figure>
              <figure class="photo-window photo-window--round valley-hero__photo-b">
                <img src="/wp-content/uploads/2025/11/happy-parents-and-kids-spending-time-together-and-2025-03-18-14-21-06-utc-683x1024.jpg" alt="Parents and children laughing together" width="683" height="1024" loading="lazy">
              </figure>
              <img class="kuska valley-hero__kuska" src="/images/storybook/kuska-waving.webp" alt="" width="720" height="WAVING_HEIGHT">
            </div>
          </div>
          <svg class="scene__hills" aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#hills-front"></use></svg>
        </section>
```

`WAVING_HEIGHT` is the measured height from Step 5 of Task 5. Replace the literal before saving, then confirm with `grep -c WAVING_HEIGHT kuska-website/index.html` → `0`.

- [ ] **Step 3: Append hero styles to `storybook.css`** (above the reduced-motion block)

```css
/* ---------- Skies ---------- */
.sky--dawn {
  background: linear-gradient(180deg, #fde9c9 0%, var(--cream) 48%, #eef7fd 100%);
}

.sky--meadow {
  background: linear-gradient(180deg, #d6ebdc 0%, #f1f8f2 38%, var(--cream) 100%);
}

/* ---------- Scene layers ---------- */
.scene {
  position: absolute;
  inset: 0;
  z-index: -1;
  overflow: hidden;
  pointer-events: none;
}

.scene__painting {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.55;
}

.scene__sun {
  position: absolute;
  top: 7%;
  right: 10%;
  width: clamp(80px, 9vw, 140px);
  height: clamp(80px, 9vw, 140px);
  color: var(--sun);
  animation: kuska-spin 90s linear infinite;
}

.scene__cloud {
  position: absolute;
  width: clamp(90px, 11vw, 160px);
  height: clamp(45px, 5.5vw, 80px);
  color: #fff;
  opacity: 0.92;
  animation: kuska-drift 22s ease-in-out infinite alternate;
}

.scene__cloud--one {
  top: 10%;
  left: 5%;
}

.scene__cloud--two {
  top: 26%;
  left: 46%;
  width: clamp(70px, 8vw, 120px);
  height: clamp(35px, 4vw, 60px);
  opacity: 0.75;
  animation-duration: 28s;
}

.scene__ridge,
.scene__hills-back,
.scene__hills {
  position: absolute;
  left: 0;
  width: 100%;
}

.scene__ridge {
  bottom: 70px;
  height: clamp(120px, 18vw, 260px);
  color: #a9cce8;
}

.scene__hills-back {
  bottom: 20px;
  height: clamp(100px, 14vw, 200px);
  color: #bfe0c9;
}

.scene__hills {
  bottom: -1px;
  height: clamp(70px, 9vw, 140px);
  color: #d6ebdc; /* = top of .sky--meadow so the hero melts into the next section */
}

@keyframes kuska-drift {
  from { transform: translateX(0); }
  to { transform: translateX(48px); }
}

@keyframes kuska-spin {
  to { transform: rotate(360deg); }
}

@keyframes kuska-bob {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-6px); }
}

/* ---------- Photo frames ---------- */
.photo-window {
  margin: 0;
  overflow: hidden;
  border: 6px solid #fff;
  border-radius: var(--radius-xl);
  background: var(--sky);
  box-shadow: var(--shadow-soft);
}

.photo-window img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-window--arch {
  border-radius: 999px 999px var(--radius-xl) var(--radius-xl);
}

.photo-window--round {
  border-radius: 50%;
}

/* ---------- Stickers ---------- */
.sticker-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin: 34px 0 0;
  padding: 0;
  list-style: none;
}

.sticker {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  border-radius: 999px;
  background: #fff;
  color: var(--ink);
  font-size: 0.92rem;
  font-weight: 600;
  box-shadow: 0 8px 18px rgba(23, 52, 74, 0.08);
  transform: rotate(-1.5deg);
}

.sticker:nth-child(even) {
  transform: rotate(1.5deg);
}

.sticker svg {
  flex: none;
  width: 18px;
  height: 18px;
}

.sticker--sun svg { color: #d9a92a; }
.sticker--sage svg { color: #5f9a72; }
.sticker--coral svg { color: var(--coral); }

/* ---------- Characters ---------- */
.kuska {
  height: auto;
  filter: drop-shadow(0 12px 16px rgba(23, 52, 74, 0.16));
}

/* ---------- Hero ---------- */
.valley-hero {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  padding: clamp(48px, 7vw, 96px) 0 clamp(130px, 15vw, 210px);
}

.valley-hero__grid {
  display: grid;
  grid-template-columns: minmax(0, 1.05fr) minmax(0, 0.95fr);
  align-items: center;
  gap: clamp(32px, 5vw, 72px);
}

.valley-hero h1 {
  margin: 0 0 18px;
}

.valley-hero__label {
  display: block;
  margin-bottom: 14px;
  color: var(--deep-blue);
  font-family: var(--font-body);
  font-size: 0.82rem;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
}

.valley-hero__title {
  display: block;
  color: var(--ink);
  font-size: clamp(2.6rem, 6vw, 5.2rem);
  line-height: 1.02;
  letter-spacing: -0.02em;
  font-variation-settings: "SOFT" 100, "WONK" 1, "opsz" 144;
}

.valley-hero__lead {
  max-width: 34ch;
  margin: 0 0 28px;
  font-size: clamp(1.08rem, 1.4vw, 1.25rem);
}

.valley-hero .button-row {
  align-items: center;
  gap: 22px;
}

.valley-hero__art {
  position: relative;
  min-height: clamp(360px, 40vw, 540px);
}

.valley-hero__photo-a {
  position: absolute;
  top: 0;
  right: 6%;
  width: 60%;
  aspect-ratio: 4 / 5;
}

.valley-hero__photo-b {
  position: absolute;
  bottom: 8%;
  left: 0;
  width: 38%;
  aspect-ratio: 1;
}

.valley-hero__kuska {
  position: absolute;
  right: -2%;
  bottom: -6%;
  width: clamp(140px, 17vw, 230px);
  animation: kuska-bob 5s ease-in-out infinite;
}

@media (max-width: 820px) {
  .valley-hero__grid {
    grid-template-columns: 1fr;
  }

  .valley-hero__art {
    min-height: 340px;
    max-width: 460px;
    width: 100%;
    margin: 0 auto;
  }

  .scene__sun {
    top: 3%;
    right: 4%;
  }
}

@media (max-width: 480px) {
  .valley-hero__art {
    min-height: 290px;
  }

  .valley-hero__kuska {
    right: 0;
    width: 120px;
  }

  .sticker {
    font-size: 0.86rem;
  }
}
```

Fill the reduced-motion block in `storybook.css` with:

```css
@media (prefers-reduced-motion: reduce) {
  .scene__sun,
  .scene__cloud,
  .kuska {
    animation: none !important;
  }
}
```

- [ ] **Step 4: Remove now-unused homepage hero CSS**

Delete the rules in `site.css` that only the old homepage hero used: `.hero-photo-stack`, `.hero-photo`, `.hero-photo--large`, `.hero-photo--small`, `.hero-badges` (and `.hero-badges li` in the 640px media query), and `.hero-highlights*` if present. First confirm no other page uses them:
Run: `grep -l 'hero-photo\|hero-badges\|hero-highlights' kuska-website/*/index.html kuska-website/404.html` → expected: no output. If any page is listed, keep the rules it uses.

- [ ] **Step 5: Run the checker** → `8 checks, 0 failures`.

- [ ] **Step 6: Browser check (Review Focus #1)**

Load `http://localhost:8000/` at 1280×900, 768×1024 and 375×812, and screenshot each.
Expected:
- the label sits above the large Fraunces headline
- the sun, clouds, Wasatch ridge and hills are layered behind the content
- the arch photo and round photo are visible, with Kuska waving at the lower right of the art
- the hills melt into a soft green, with no hard seam
- at 375px: copy first, then art, no overlap between Kuska/photos and the headline, and `document.documentElement.scrollWidth <= window.innerWidth` is `true` (`browser_evaluate`)

If the result fails, adjust sizes in the 820/480 media queries and recheck.

- [ ] **Step 7: Commit**

```bash
git -C "$P" add kuska-website/index.html kuska-website/storybook.css kuska-website/site.css scripts/check_site.py
git -C "$P" commit -m "Homepage hero: sunrise valley scene with Kuska and new headline"
```

---

### Task 7: "How we help": the meadow

**Files:**
- Modify: `kuska-website/index.html`: replace the section whose heading is `How Kuska Helps` (`<section class="section"> … service-grid … chip-cloud … </section>`)
- Modify: `kuska-website/storybook.css`, `scripts/check_site.py`

**Interfaces:**
- Consumes: `.sky--meadow` (Task 6), sprite `star heart flower`.
- Produces: `.section-heading--center`, `.story-grid`, `.story-card`, `.story-card__photo`, `.story-card__body`, `.story-card__doodle`, `.flower-field`, `.flower-field__title`, `.flower-field__list`, `.flower-tag`. Elements carry `data-reveal` (styled in Task 11).

- [ ] **Step 1: Add the failing check**

```python
def check_home_meadow():
    doc = Doc.load(ROOT / "index.html")
    failures = []
    if len(doc.find("article", "story-card")) != 3:
        failures.append("index.html: meadow needs exactly 3 .story-card articles")
    if len(doc.find("li", "flower-tag")) != 10:
        failures.append("index.html: meadow needs exactly 10 .flower-tag items")
    return failures
```

Add to `CHECKS`; run → expect both failures.

- [ ] **Step 2: Replace the markup**

```html
        <section class="section sky--meadow" aria-labelledby="help-title">
          <div class="shell">
            <div class="section-heading section-heading--center" data-reveal>
              <p class="eyebrow">How we help</p>
              <h2 id="help-title">Support that grows with your family.</h2>
            </div>
            <div class="story-grid">
              <article class="story-card" data-reveal>
                <figure class="story-card__photo">
                  <img src="/wp-content/uploads/2025/11/psychology-test-for-children-toddler-coloring-sh-2024-10-18-10-56-05-utc-683x1024.jpg" alt="A toddler coloring during a playful developmental assessment" width="683" height="1024" loading="lazy">
                </figure>
                <div class="story-card__body">
                  <svg class="story-card__doodle" aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#star"></use></svg>
                  <h3>Autism evaluations</h3>
                  <p>Clear answers, and a caring guide for what comes next.</p>
                  <a class="text-link" href="/diagnostic-service/">About evaluations <span aria-hidden="true">→</span></a>
                </div>
              </article>
              <article class="story-card" data-reveal>
                <figure class="story-card__photo">
                  <img src="/wp-content/uploads/2025/09/little-boy-learns-words-from-cards-under-the-aba-t-2024-09-26-04-01-59-utc-1-980x655.jpg" alt="A young boy learning words from picture cards with his therapist" width="980" height="655" loading="lazy">
                </figure>
                <div class="story-card__body">
                  <svg class="story-card__doodle" aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#heart"></use></svg>
                  <h3>ABA therapy</h3>
                  <p>Personalized plans built around play, connection, and everyday skills.</p>
                  <a class="text-link" href="/our-program/">Our ABA program <span aria-hidden="true">→</span></a>
                </div>
              </article>
              <article class="story-card" data-reveal>
                <figure class="story-card__photo">
                  <img src="/wp-content/uploads/2025/10/mother-and-son-drawing-with-crayons-at-home-and-cr-2025-04-01-13-04-25-utc-980x652.jpg" alt="A mother and son drawing with crayons at home" width="980" height="652" loading="lazy">
                </figure>
                <div class="story-card__body">
                  <svg class="story-card__doodle" aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#flower"></use></svg>
                  <h3>In-home or clinic</h3>
                  <p>Therapy where your child feels at home, in Bountiful or Draper.</p>
                  <a class="text-link" href="/get-started/">Find your fit <span aria-hidden="true">→</span></a>
                </div>
              </article>
            </div>
            <div class="flower-field" data-reveal>
              <h3 class="flower-field__title">Skills we grow together</h3>
              <ul class="flower-field__list">
                <li class="flower-tag"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#flower"></use></svg>Speech and communication</li>
                <li class="flower-tag"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#flower"></use></svg>Social skills</li>
                <li class="flower-tag"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#flower"></use></svg>Emotional regulation</li>
                <li class="flower-tag"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#flower"></use></svg>Daily living skills</li>
                <li class="flower-tag"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#flower"></use></svg>School readiness</li>
                <li class="flower-tag"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#flower"></use></svg>Toilet training</li>
                <li class="flower-tag"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#flower"></use></svg>Coping skills</li>
                <li class="flower-tag"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#flower"></use></svg>Community connection</li>
                <li class="flower-tag"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#flower"></use></svg>Problem solving</li>
                <li class="flower-tag"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#flower"></use></svg>Play and leisure</li>
              </ul>
            </div>
          </div>
        </section>
```

Open the three new photos and confirm each alt text matches what the photo shows. Adjust the wording if it doesn't.

- [ ] **Step 3: Append styles to `storybook.css`**

```css
/* ---------- Shared section bits ---------- */
.section-heading--center {
  margin-inline: auto;
  text-align: center;
}

/* ---------- Meadow: story cards ---------- */
.story-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 28px;
}

.story-card {
  position: relative;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  border-radius: var(--radius-xl);
  background: #fff;
  box-shadow: var(--shadow-card);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.story-card:hover,
.story-card:focus-within {
  transform: translateY(-6px) rotate(-1deg);
  box-shadow: var(--shadow-soft);
}

.story-card:nth-child(2):hover,
.story-card:nth-child(2):focus-within {
  transform: translateY(-6px) rotate(1deg);
}

.story-card__photo {
  margin: 0;
  aspect-ratio: 4 / 3;
  overflow: hidden;
  border-radius: 0 0 50% 50% / 0 0 14% 14%;
}

.story-card__photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.story-card__body {
  position: relative;
  display: flex;
  flex: 1;
  flex-direction: column;
  gap: 10px;
  padding: 30px 28px 30px;
}

.story-card__body h3 {
  margin: 0;
  color: var(--deep-blue);
  font-size: 1.5rem;
}

.story-card__body p {
  margin: 0;
}

.story-card__body .text-link {
  margin-top: auto;
}

.story-card__doodle {
  position: absolute;
  top: -28px;
  right: 24px;
  width: 54px;
  height: 54px;
  padding: 13px;
  border-radius: 50%;
  background: var(--sun);
  color: #fff;
  box-shadow: var(--shadow-card);
}

.story-card:nth-child(2) .story-card__doodle { background: var(--coral); }
.story-card:nth-child(3) .story-card__doodle { background: var(--sage); }

/* ---------- Meadow: flower field ---------- */
.flower-field {
  margin-top: 56px;
  text-align: center;
}

.flower-field__title {
  margin: 0 0 18px;
  color: var(--deep-blue);
  font-family: var(--font-hand);
  font-size: 2rem;
  font-weight: 700;
  font-variation-settings: normal;
}

.flower-field__list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 12px 14px;
  max-width: 920px;
  margin: 0 auto;
  padding: 0;
  list-style: none;
}

.flower-tag {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 9px 16px 9px 12px;
  border: 1px solid #cfe6d6;
  border-radius: 999px;
  background: #fff;
  color: var(--ink);
  font-size: 0.92rem;
  font-weight: 600;
}

.flower-tag:nth-child(odd) {
  transform: translateY(5px);
}

.flower-tag svg {
  width: 20px;
  height: 20px;
  color: var(--coral);
}

.flower-tag:nth-child(3n + 2) svg { color: var(--kuska-blue); }
.flower-tag:nth-child(3n) svg { color: var(--sage); }

@media (max-width: 1080px) {
  .story-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 820px) {
  .story-grid {
    grid-template-columns: 1fr;
    max-width: 520px;
    margin-inline: auto;
  }
}
```

Add `.story-card` to the reduced-motion block's selector list, so the hover lift has `transition: none !important;` (add a separate rule inside the block: `.story-card { transition: none !important; }`).

- [ ] **Step 4: Remove the now-unused `.chip-cloud` CSS** only if `grep -l 'chip-cloud' kuska-website/*/index.html` returns nothing. Otherwise leave it.

- [ ] **Step 5: Run the checker** → `9 checks, 0 failures`.

- [ ] **Step 6: Browser check**

At 1280 and 375: three cards with photos curved at the bottom edge and a coloured doodle bubble overlapping each photo; hovering a card lifts and tilts it. The flower field wraps nicely, with a "Skills we grow together" label in handwriting. No horizontal scroll at 375.

- [ ] **Step 7: Commit**

```bash
git -C "$P" add kuska-website/index.html kuska-website/storybook.css kuska-website/site.css scripts/check_site.py
git -C "$P" commit -m "Homepage meadow: story cards and skills flower field"
```

---

### Task 8: "Why Kuska": the name story

**Files:**
- Modify: `kuska-website/index.html`: replace the `<section class="section section--tint"> … split-panel … value-stack … </section>` (heading `Why Parents Choose Kuska`)
- Modify: `kuska-website/storybook.css`, `scripts/check_site.py`

**Interfaces:**
- Consumes: `kuska-reading.webp`, `photos/kuska-team-800.webp`, sprite `heart star sun flower`.
- Produces: `.sky--cream`, `.name-story`, `.name-story__grid`, `.name-story__art`, `.name-story__kuska`, `.name-story__polaroid`, `.name-story__copy`, `.polaroid`, `.value-badges`, `.value-badge`.

- [ ] **Step 1: Add the failing check**

```python
def check_home_name_story():
    doc = Doc.load(ROOT / "index.html")
    failures = []
    if len(doc.find("li", "value-badge")) != 4:
        failures.append("index.html: name story needs exactly 4 .value-badge items")
    if not doc.find("figure", "polaroid"):
        failures.append("index.html: name story needs a .polaroid photo")
    return failures
```

Add to `CHECKS`; run → expect failures.

- [ ] **Step 2: Replace the markup** (fill `READING_HEIGHT` from `art-sizes.txt`; confirm `grep -c READING_HEIGHT` → 0)

```html
        <section class="section name-story sky--cream" aria-labelledby="why-title">
          <div class="shell name-story__grid">
            <div class="name-story__art" data-reveal>
              <figure class="polaroid name-story__polaroid">
                <img src="/images/storybook/photos/kuska-team-800.webp" alt="The Kuska Autism Services team" width="800" height="600" loading="lazy">
                <figcaption>Team Kuska</figcaption>
              </figure>
              <img class="kuska name-story__kuska" src="/images/storybook/kuska-reading.webp" alt="" width="720" height="READING_HEIGHT" loading="lazy">
            </div>
            <div class="name-story__copy" data-reveal>
              <p class="eyebrow">Why Kuska</p>
              <h2 id="why-title"><em>Kuska</em> means “together.”</h2>
              <p>We’re locally owned, trauma-informed, and side by side with parents at every step. Just asking questions, or already holding a diagnosis? We’ll help you take the next step without feeling overwhelmed.</p>
              <ul class="value-badges">
                <li class="value-badge"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#heart"></use></svg><strong>Kuska</strong><span>Parents and clinicians, one team.</span></li>
                <li class="value-badge"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#star"></use></svg><strong>Quality care</strong><span>Evidence-based and individualized.</span></li>
                <li class="value-badge"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#sun"></use></svg><strong>Radical candor</strong><span>Clear, kind, timely communication.</span></li>
                <li class="value-badge"><svg aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#flower"></use></svg><strong>Play</strong><span>Kids learn best when it’s fun.</span></li>
              </ul>
            </div>
          </div>
        </section>
```

- [ ] **Step 3: Append styles**

```css
/* ---------- Name story ---------- */
.sky--cream {
  background: var(--cream);
}

.name-story__grid {
  display: grid;
  grid-template-columns: minmax(0, 0.9fr) minmax(0, 1.1fr);
  align-items: center;
  gap: clamp(36px, 6vw, 88px);
}

.name-story__art {
  position: relative;
  min-height: 460px;
}

.polaroid {
  position: relative;
  margin: 0;
  padding: 12px 12px 14px;
  border-radius: 6px;
  background: #fff;
  box-shadow: var(--shadow-soft);
  transform: rotate(-3deg);
}

/* Washi tape */
.polaroid::before {
  content: "";
  position: absolute;
  top: -12px;
  left: calc(50% - 45px);
  width: 90px;
  height: 26px;
  background: rgba(235, 201, 78, 0.72);
  transform: rotate(4deg);
}

.polaroid img {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
  border-radius: 3px;
}

.polaroid figcaption {
  margin-top: 8px;
  color: var(--deep-blue);
  font-family: var(--font-hand);
  font-size: 1.5rem;
  text-align: center;
}

.name-story__polaroid {
  position: absolute;
  top: 0;
  left: 0;
  width: 72%;
}

.name-story__kuska {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 60%;
}

.name-story__copy h2 {
  margin: 0 0 16px;
  color: var(--deep-blue);
  font-size: clamp(2rem, 3.6vw, 3.4rem);
  line-height: 1.08;
}

.name-story__copy h2 em {
  color: var(--kuska-blue);
}

.value-badges {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 14px;
  margin: 28px 0 0;
  padding: 0;
  list-style: none;
}

.value-badge {
  display: grid;
  grid-template-columns: 44px 1fr;
  column-gap: 12px;
  align-items: start;
  padding: 16px;
  border-radius: var(--radius-md);
  background: #fff;
  box-shadow: var(--shadow-card);
  font-size: 0.95rem;
  line-height: 1.5;
}

.value-badge svg {
  grid-row: span 2;
  width: 44px;
  height: 44px;
  padding: 10px;
  border-radius: 50%;
  background: var(--sky);
  color: var(--deep-blue);
}

.value-badge:nth-child(2) svg { background: #fbeec0; color: #8a6a00; }
.value-badge:nth-child(3) svg { background: #fcdcd2; color: #a8432a; }
.value-badge:nth-child(4) svg { background: #d6ebdc; color: #3f7a52; }

.value-badge strong {
  color: var(--deep-blue);
  font-family: var(--font-display);
  font-size: 1.15rem;
  font-weight: 600;
}

@media (max-width: 820px) {
  .name-story__grid {
    grid-template-columns: 1fr;
  }

  .name-story__art {
    min-height: 380px;
    max-width: 460px;
    width: 100%;
    margin: 0 auto;
  }
}

@media (max-width: 480px) {
  .value-badges {
    grid-template-columns: 1fr;
  }

  .name-story__art {
    min-height: 320px;
  }
}
```

- [ ] **Step 4: Remove unused `.split-panel` / `.value-stack` CSS** only if `grep -l 'split-panel\|value-stack' kuska-website/*/index.html kuska-website/404.html` returns nothing. Otherwise keep it.

- [ ] **Step 5: Run the checker** → `10 checks, 0 failures`.

- [ ] **Step 6: Browser check** at 1280 and 375: a tilted polaroid with yellow tape and a "Team Kuska" caption; Kuska reading with a child overlaps its lower right; four value badges in a 2×2 grid (1 column at 375). No overlap with the text, and no horizontal scroll.

- [ ] **Step 7: Commit**

```bash
git -C "$P" add kuska-website/index.html kuska-website/storybook.css kuska-website/site.css scripts/check_site.py
git -C "$P" commit -m "Homepage name story: polaroid, Kuska reading, value badges"
```

---

### Task 9: "Getting started" trail + "Friends along the way" insurance

**Files:**
- Modify: `kuska-website/index.html`: replace the `Getting Started` section (`steps-grid`) and the `Insurance` section (`logo-strip`)
- Modify: `kuska-website/storybook.css`, `scripts/check_site.py`

**Interfaces:**
- Consumes: `kuska-walking.webp`, sprite `trail`.
- Produces: `.sky--day`, `.trail`, `.trail__path`, `.trail__kuska`, `.trail__stops`, `.trail__stop`, `.trail__photo`, `.trail__num`, `.trail__end`, `.trail__note`, `.logo-marquee`, `.logo-marquee__track`.

- [ ] **Step 1: Add the failing check**

```python
def check_home_trail_and_insurance():
    doc = Doc.load(ROOT / "index.html")
    failures = []
    if len(doc.find("li", "trail__stop")) != 3:
        failures.append("index.html: trail needs exactly 3 .trail__stop items")
    tracks = doc.find("ul", "logo-marquee__track")
    if len(tracks) != 2 or tracks[1].attrs.get("aria-hidden") != "true":
        failures.append("index.html: marquee needs 2 tracks, the second aria-hidden='true'")
    for img in doc.find("img"):
        if "/wp-content/uploads/2025/05/" in img.attrs.get("src", "") and not img.attrs.get("width"):
            failures.append(f"index.html: logo {img.attrs['src']} needs width/height")
    return failures
```

Add to `CHECKS`; run → expect failures.

- [ ] **Step 2: Replace the Getting Started section** (fill `WALKING_HEIGHT`; confirm grep → 0)

```html
        <section class="section sky--day" aria-labelledby="start-title">
          <div class="shell">
            <div class="section-heading section-heading--center" data-reveal>
              <p class="eyebrow">Getting started</p>
              <h2 id="start-title">Three easy steps down the trail.</h2>
            </div>
            <div class="trail">
              <svg class="trail__path" aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#trail"></use></svg>
              <img class="kuska trail__kuska" src="/images/storybook/kuska-walking.webp" alt="" width="720" height="WALKING_HEIGHT" loading="lazy">
              <ol class="trail__stops">
                <li class="trail__stop" data-reveal>
                  <figure class="photo-window photo-window--round trail__photo">
                    <img src="/wp-content/uploads/2025/11/cheerful-young-beautiful-woman-talking-on-the-phon-2024-10-19-12-34-00-utc-683x1024.jpg" alt="A smiling parent talking on the phone" width="683" height="1024" loading="lazy">
                  </figure>
                  <span class="trail__num" aria-hidden="true">1</span>
                  <h3>Talk with us</h3>
                  <p>Tell us about your child. We’ll answer every question.</p>
                </li>
                <li class="trail__stop" data-reveal>
                  <figure class="photo-window photo-window--round trail__photo">
                    <img src="/wp-content/uploads/2026/04/dyslexia-treatment-pediatrician-working-with-litt-2026-03-26-23-23-32-utc-1280.jpg" alt="A clinician working one-on-one with a young child" width="1280" height="854" loading="lazy">
                  </figure>
                  <span class="trail__num" aria-hidden="true">2</span>
                  <h3>Assessment</h3>
                  <p>We get to know your child’s strengths and needs.</p>
                </li>
                <li class="trail__stop" data-reveal>
                  <figure class="photo-window photo-window--round trail__photo">
                    <img src="/wp-content/uploads/2026/02/smiling-parents-helping-their-son-with-homework-at-2026-01-11-11-14-02-utc-980x653.jpg" alt="Smiling parents helping their son at the kitchen table" width="980" height="653" loading="lazy">
                  </figure>
                  <span class="trail__num" aria-hidden="true">3</span>
                  <h3>Build the plan</h3>
                  <p>Goals and schedules that fit real family life.</p>
                </li>
              </ol>
              <div class="trail__end">
                <a class="button" href="/get-started/">Get started</a>
                <span class="trail__note" aria-hidden="true">you’ve got this!</span>
              </div>
            </div>
          </div>
        </section>
```

- [ ] **Step 3: Replace the Insurance section**

The six `<li>` entries reuse today's links, with `width`/`height` added. The second track is identical except for `tabindex="-1"` on each link.

```html
        <section class="section section--compact sky--cream" aria-labelledby="ins-title">
          <div class="shell">
            <div class="section-heading section-heading--center" data-reveal>
              <p class="eyebrow">Insurance</p>
              <h2 id="ins-title">Friends along the way.</h2>
              <p>In-network with the plans Utah families use.</p>
            </div>
          </div>
          <div class="logo-marquee">
            <ul class="logo-marquee__track">
              <li><a href="https://medicaid.utah.gov/" target="_blank" rel="noopener noreferrer" aria-label="Utah Medicaid"><img src="/wp-content/uploads/2025/05/medicaid-3.png" alt="Utah Medicaid" width="361" height="140" loading="lazy"></a></li>
              <li><a href="https://www.selecthealth.org/" target="_blank" rel="noopener noreferrer" aria-label="Select Health"><img src="/wp-content/uploads/2025/05/select-health-logo.jpg" alt="Select Health" width="200" height="125" loading="lazy"></a></li>
              <li><a href="https://www.optum.com/" target="_blank" rel="noopener noreferrer" aria-label="Optum"><img src="/wp-content/uploads/2025/05/Optum-Logo-2011-e1746217706743.png" alt="Optum" width="500" height="244" loading="lazy"></a></li>
              <li><a href="https://www.uhc.com/" target="_blank" rel="noopener noreferrer" aria-label="UnitedHealthcare"><img src="/wp-content/uploads/2025/05/United-Healthcare-Logo.png" alt="UnitedHealthcare" width="500" height="268" loading="lazy"></a></li>
              <li><a href="https://www.evernorth.com/" target="_blank" rel="noopener noreferrer" aria-label="Evernorth"><img src="/wp-content/uploads/2025/05/Evernorth_Logo.png" alt="Evernorth" width="500" height="266" loading="lazy"></a></li>
              <li><a href="https://www.bcbs.com/" target="_blank" rel="noopener noreferrer" aria-label="Blue Cross Blue Shield"><img src="/wp-content/uploads/2025/05/blue-cross-blue-shield-vector-logo.png" alt="Blue Cross Blue Shield" width="500" height="278" loading="lazy"></a></li>
            </ul>
            <ul class="logo-marquee__track" aria-hidden="true">
              <li><a href="https://medicaid.utah.gov/" target="_blank" rel="noopener noreferrer" tabindex="-1"><img src="/wp-content/uploads/2025/05/medicaid-3.png" alt="" width="361" height="140" loading="lazy"></a></li>
              <li><a href="https://www.selecthealth.org/" target="_blank" rel="noopener noreferrer" tabindex="-1"><img src="/wp-content/uploads/2025/05/select-health-logo.jpg" alt="" width="200" height="125" loading="lazy"></a></li>
              <li><a href="https://www.optum.com/" target="_blank" rel="noopener noreferrer" tabindex="-1"><img src="/wp-content/uploads/2025/05/Optum-Logo-2011-e1746217706743.png" alt="" width="500" height="244" loading="lazy"></a></li>
              <li><a href="https://www.uhc.com/" target="_blank" rel="noopener noreferrer" tabindex="-1"><img src="/wp-content/uploads/2025/05/United-Healthcare-Logo.png" alt="" width="500" height="268" loading="lazy"></a></li>
              <li><a href="https://www.evernorth.com/" target="_blank" rel="noopener noreferrer" tabindex="-1"><img src="/wp-content/uploads/2025/05/Evernorth_Logo.png" alt="" width="500" height="266" loading="lazy"></a></li>
              <li><a href="https://www.bcbs.com/" target="_blank" rel="noopener noreferrer" tabindex="-1"><img src="/wp-content/uploads/2025/05/blue-cross-blue-shield-vector-logo.png" alt="" width="500" height="278" loading="lazy"></a></li>
            </ul>
          </div>
        </section>
```

- [ ] **Step 4: Append styles**

```css
/* ---------- Trail ---------- */
.sky--day {
  background: linear-gradient(180deg, var(--cream) 0%, #eef7fd 28%, #eef7fd 72%, var(--cream) 100%);
}

.trail {
  position: relative;
  padding-top: 40px;
}

.trail__path {
  position: absolute;
  top: 90px;
  left: 0;
  width: 100%;
  height: 200px;
  color: var(--sun);
}

.trail__kuska {
  position: absolute;
  top: -50px;
  left: -10px;
  width: clamp(110px, 12vw, 170px);
}

.trail__stops {
  position: relative;
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 32px;
  margin: 0;
  padding: 0;
  list-style: none;
}

.trail__stop {
  position: relative;
  padding: 0 12px;
  text-align: center;
}

.trail__stop:nth-child(2) {
  margin-top: 70px;
}

.trail__photo {
  width: 160px;
  height: 160px;
  margin: 0 auto 18px;
}

.trail__num {
  position: absolute;
  top: 118px;
  left: calc(50% + 44px);
  display: grid;
  place-items: center;
  width: 46px;
  height: 46px;
  border-radius: 50%;
  background: var(--sun);
  color: var(--ink);
  font-family: var(--font-display);
  font-size: 1.3rem;
  font-weight: 700;
  box-shadow: var(--shadow-card);
}

.trail__stop h3 {
  margin: 0 0 6px;
  color: var(--deep-blue);
  font-size: 1.4rem;
}

.trail__stop p {
  max-width: 26ch;
  margin: 0 auto;
}

.trail__end {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 16px;
  margin-top: 44px;
}

.trail__note {
  color: var(--twilight);
  font-family: var(--font-hand);
  font-size: 1.6rem;
  transform: rotate(-4deg);
}

@media (max-width: 820px) {
  .trail__path {
    display: none;
  }

  .trail__kuska {
    position: static;
    display: block;
    margin: 0 auto 12px;
  }

  .trail__stops {
    grid-template-columns: 1fr;
    gap: 36px;
  }

  .trail__stop:nth-child(2) {
    margin-top: 0;
  }
}

/* ---------- Insurance marquee ---------- */
.logo-marquee {
  display: flex;
  gap: 20px;
  overflow: hidden;
  padding: 10px 0 24px;
  -webkit-mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent);
  mask-image: linear-gradient(90deg, transparent, #000 8%, #000 92%, transparent);
}

.logo-marquee__track {
  display: flex;
  flex: none;
  gap: 20px;
  margin: 0;
  padding: 0;
  list-style: none;
  animation: kuska-marquee 36s linear infinite;
}

.logo-marquee:hover .logo-marquee__track,
.logo-marquee:focus-within .logo-marquee__track {
  animation-play-state: paused;
}

.logo-marquee__track a {
  display: grid;
  place-items: center;
  width: 190px;
  height: 104px;
  padding: 18px 22px;
  border-radius: var(--radius-md);
  background: #fff;
  box-shadow: var(--shadow-card);
}

.logo-marquee__track img {
  width: auto;
  max-width: 100%;
  height: auto;
  max-height: 60px;
  object-fit: contain;
}

@keyframes kuska-marquee {
  to { transform: translateX(calc(-100% - 20px)); }
}
```

Add to the `storybook.css` reduced-motion block:

```css
  .logo-marquee {
    justify-content: center;
    -webkit-mask-image: none;
    mask-image: none;
  }

  .logo-marquee__track {
    flex: 1 1 auto;
    flex-wrap: wrap;
    justify-content: center;
    animation: none !important;
  }

  .logo-marquee__track[aria-hidden="true"] {
    display: none;
  }
```

- [ ] **Step 5: Remove unused `.steps-grid`/`.step-card`/`.logo-strip` CSS** only if `grep -l 'steps-grid\|step-card\|logo-strip' kuska-website/*/index.html kuska-website/404.html` returns nothing for each class. Remove only the classes that return nothing.

- [ ] **Step 6: Run the checker, then check in the browser (Review Focus #3)**

Run the checker → `11 checks, 0 failures`.
At 1280: a dotted yellow trail behind three round photo stops, with the middle stop lower; Kuska walking at the trail start; the "you've got this!" note beside the button; the logos scroll continuously and pause on hover; Tab reaches only the first six logo links.
Then `browser_emulate_media` with `reducedMotion: "reduce"` and reload. Expect `getComputedStyle(document.querySelector('.logo-marquee__track')).animationName === 'none'`, the second track hidden (`display: none`), and the logos wrapped and centred. Check 375px too: stops stack in one column, there's no trail path, and no horizontal scroll.

- [ ] **Step 7: Commit**

```bash
git -C "$P" add kuska-website/index.html kuska-website/storybook.css kuska-website/site.css scripts/check_site.py
git -C "$P" commit -m "Homepage trail steps and insurance logo marquee"
```

---

### Task 10: Locations cottages, "Stories for the journey", "Under the stars" CTA, word budget

**Files:**
- Modify: `kuska-website/index.html`: replace the `Locations` section, the `Helpful Reads` section, and the `cta-band` section
- Modify: `kuska-website/storybook.css`, `scripts/check_site.py`

**Interfaces:**
- Consumes: `kuska-sleeping.webp`, `photos/drawing-800.webp`, sprite `moon hills-back edge-wave`, `.button--ghost` (Task 4).
- Produces: `.cottage-grid`, `.cottage`, `.cottage__window`, `.cottage__body`, `.cottage__address`, `.cottage__actions`, `.book-grid`, `.book-card`, `.book-card__cover`, `.book-card__body`, `.book-card__date`, `.book-card__link`, `.stories__more`, `.sky--dusk`, `.starry-cta`, `.starry-cta__inner`, `.starry-cta__kuska`, `.scene__moon`, `.edge-wave--top`.

- [ ] **Step 1: Add the failing checks (including the homepage-wide budget and image rules)**

```python
def check_home_finale():
    doc = Doc.load(ROOT / "index.html")
    failures = []
    if len(doc.find("article", "cottage")) != 2:
        failures.append("index.html: locations need exactly 2 .cottage cards")
    if len(doc.find("article", "book-card")) != 3:
        failures.append("index.html: stories need exactly 3 .book-card articles")
    if not doc.find("section", "starry-cta"):
        failures.append("index.html: missing .starry-cta section")
    for phone in ("tel:+18019807970",):
        if phone not in doc.raw:
            failures.append(f"index.html: missing {phone}")
    for address in ("95 2200 S", "12055 S 700 E"):
        if address not in doc.raw:
            failures.append(f"index.html: missing address {address}")
    return failures


def check_home_budget_and_images():
    doc = Doc.load(ROOT / "index.html")
    failures = []
    words = len(doc.text_of("main").split())
    if words > 380:
        failures.append(f"index.html: <main> has {words} words, budget is 380")
    main_start = doc.raw.index("<main")
    main_end = doc.raw.index("</main>")
    main_html = doc.raw[main_start:main_end]
    imgs = re.findall(r"<img\b[^>]*>", main_html)
    for i, tag in enumerate(imgs):
        if 'width="' not in tag or 'height="' not in tag:
            failures.append(f"index.html: main <img> #{i + 1} missing width/height")
        is_first_hero_photo = 'fetchpriority="high"' in tag
        is_hero_layer = 'class="scene__painting"' in tag or "valley-hero__kuska" in tag
        if not (is_first_hero_photo or is_hero_layer) and 'loading="lazy"' not in tag:
            failures.append(f"index.html: main <img> #{i + 1} should be loading=lazy")
    return failures
```

Add both to `CHECKS`; run → expect failures, including the word budget if the old sections remain.

- [ ] **Step 2: Replace the Locations section**

```html
        <section class="section sky--day" aria-labelledby="loc-title">
          <div class="shell">
            <div class="section-heading section-heading--center" data-reveal>
              <p class="eyebrow">Locations</p>
              <h2 id="loc-title">Two homes in the valley.</h2>
            </div>
            <div class="cottage-grid">
              <article class="cottage" data-reveal>
                <figure class="photo-window photo-window--arch cottage__window">
                  <img src="/wp-content/uploads/2025/10/children-playing-with-toys-in-an-indoor-sand-cover-2025-02-23-19-08-17-utc-980x653.jpg" alt="Children playing together with sensory toys" width="980" height="653" loading="lazy">
                </figure>
                <div class="cottage__body">
                  <h3>Bountiful</h3>
                  <p class="cottage__address">95 2200 S<br>Bountiful, UT 84010</p>
                  <p>Daytime ABA therapy and evaluation support.</p>
                  <div class="cottage__actions">
                    <a class="button button--secondary" href="tel:+18019807970">(801) 980-7970</a>
                    <a class="text-link" href="https://www.google.com/maps/dir/?api=1&amp;destination=95+2200+S,+Bountiful,+UT+84010" target="_blank" rel="noopener">Get directions</a>
                  </div>
                </div>
              </article>
              <article class="cottage" data-reveal>
                <figure class="photo-window photo-window--arch cottage__window">
                  <img src="/wp-content/uploads/2025/09/occupational-therapist-using-sensory-integration-t-2025-07-09-06-23-51-utc-1-980x551.jpg" alt="A therapist guiding a child through a sensory play activity" width="980" height="551" loading="lazy">
                </figure>
                <div class="cottage__body">
                  <h3>Draper</h3>
                  <p class="cottage__address">12055 S 700 E<br>Draper, UT 84020</p>
                  <p>Flexible scheduling across Salt Lake County.</p>
                  <div class="cottage__actions">
                    <a class="button button--secondary" href="tel:+18019807970">(801) 980-7970</a>
                    <a class="text-link" href="https://www.google.com/maps/dir/?api=1&amp;destination=12055+S+700+E,+Draper,+UT+84020" target="_blank" rel="noopener">Get directions</a>
                  </div>
                </div>
              </article>
            </div>
          </div>
        </section>
```

- [ ] **Step 3: Replace the Helpful Reads section**

```html
        <section class="section sky--cream" aria-labelledby="stories-title">
          <div class="shell">
            <div class="section-heading section-heading--center" data-reveal>
              <p class="eyebrow">Helpful reads</p>
              <h2 id="stories-title">Stories for the journey.</h2>
            </div>
            <div class="book-grid">
              <article class="book-card" data-reveal>
                <img class="book-card__cover" src="/wp-content/uploads/2026/03/girl-drawing-on-blackboard-2026-01-05-06-14-59-utc-980x653.jpg" alt="" width="980" height="653" loading="lazy">
                <div class="book-card__body">
                  <p class="book-card__date">March 3, 2026</p>
                  <h3><a class="book-card__link" href="/insurance-cover-aba-therapy/">Does Insurance Cover ABA Therapy in Utah?</a></h3>
                </div>
              </article>
              <article class="book-card" data-reveal>
                <img class="book-card__cover" src="/wp-content/uploads/2026/01/toddler-playing-in-living-room-2026-01-06-09-01-22-utc-980x654.jpg" alt="" width="980" height="654" loading="lazy">
                <div class="book-card__body">
                  <p class="book-card__date">February 25, 2026</p>
                  <h3><a class="book-card__link" href="/preparing-for-your-childs-first-aba-session-what-utah-families-need-to-know/">Preparing for Your Child’s First ABA Session</a></h3>
                </div>
              </article>
              <article class="book-card" data-reveal>
                <img class="book-card__cover" src="/images/storybook/photos/drawing-800.webp" alt="" width="800" height="533" loading="lazy">
                <div class="book-card__body">
                  <p class="book-card__date">February 25, 2026</p>
                  <h3><a class="book-card__link" href="/19-questions-every-utah-parent-should-ask-before-choosing-an-aba-provider/">19 Questions to Ask Before Choosing an ABA Provider</a></h3>
                </div>
              </article>
            </div>
            <p class="stories__more"><a class="button button--secondary" href="/blog/">See all stories</a></p>
          </div>
        </section>
```

(The cover images are decorative because the link text names the article, so `alt=""` is correct.)

- [ ] **Step 4: Replace the `cta-band` section** (fill `SLEEPING_HEIGHT`; confirm grep → 0)

```html
        <section class="starry-cta sky--dusk" aria-labelledby="cta-title">
          <svg class="edge-wave--top" aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#edge-wave"></use></svg>
          <div class="scene" aria-hidden="true">
            <svg class="scene__moon" aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#moon"></use></svg>
            <svg class="scene__hills scene__hills--night" aria-hidden="true" focusable="false"><use href="/images/storybook/illustrations.svg#hills-back"></use></svg>
          </div>
          <div class="shell starry-cta__inner" data-reveal>
            <h2 id="cta-title">Ready when you are.</h2>
            <p>Have a question? We’d love to hear from you.</p>
            <div class="button-row">
              <a class="button" href="/get-started/">Schedule a consultation</a>
              <a class="button button--ghost" href="tel:+18019807970">Call (801) 980-7970</a>
            </div>
          </div>
          <img class="kuska starry-cta__kuska" src="/images/storybook/kuska-sleeping.webp" alt="" width="720" height="SLEEPING_HEIGHT" loading="lazy">
        </section>
```

- [ ] **Step 5: Append styles**

```css
/* ---------- Locations: cottages ---------- */
.cottage-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 40px;
  max-width: 980px;
  margin: 0 auto;
}

.cottage {
  position: relative;
  isolation: isolate;
  margin-top: 36px;
  padding: 22px 22px 28px;
  border-radius: var(--radius-xl);
  background: #fff;
  box-shadow: var(--shadow-card);
}

/* Roof */
.cottage::before {
  content: "";
  position: absolute;
  top: -34px;
  left: 50%;
  z-index: -1;
  width: 64%;
  height: 70px;
  background: var(--coral);
  clip-path: polygon(50% 0, 100% 100%, 0 100%);
  transform: translateX(-50%);
}

.cottage:nth-child(2)::before {
  background: var(--kuska-blue);
}

.cottage__window {
  aspect-ratio: 16 / 10;
}

.cottage__body {
  padding: 22px 8px 0;
}

.cottage__body h3 {
  margin: 0 0 6px;
  color: var(--deep-blue);
  font-size: 1.7rem;
}

.cottage__address {
  margin: 0 0 8px;
  font-weight: 600;
}

.cottage__body p {
  margin: 0 0 8px;
}

.cottage__actions {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 18px;
  margin-top: 18px;
}

/* ---------- Stories: book cards ---------- */
.book-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 28px;
}

.book-card {
  position: relative;
  overflow: hidden;
  border-left: 12px solid var(--kuska-blue);
  border-radius: 6px var(--radius-md) var(--radius-md) 6px;
  background: #fff;
  box-shadow: var(--shadow-card);
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.book-card:nth-child(2) { border-left-color: var(--coral); }
.book-card:nth-child(3) { border-left-color: var(--sage); }

.book-card:hover,
.book-card:focus-within {
  transform: translateY(-6px) rotate(-1.2deg);
  box-shadow: var(--shadow-soft);
}

.book-card__cover {
  width: 100%;
  aspect-ratio: 4 / 3;
  object-fit: cover;
}

.book-card__body {
  padding: 18px 22px 24px;
}

.book-card__date {
  margin: 0 0 6px;
  color: var(--brand-muted);
  font-size: 0.85rem;
  font-weight: 600;
}

.book-card h3 {
  margin: 0;
  font-size: 1.25rem;
  line-height: 1.25;
}

.book-card__link {
  color: var(--deep-blue);
  text-decoration: none;
}

/* Whole card is clickable */
.book-card__link::after {
  content: "";
  position: absolute;
  inset: 0;
}

.book-card__link:focus-visible {
  outline: none;
}

.book-card:focus-within {
  outline: 3px solid var(--deep-blue);
  outline-offset: 3px;
}

.stories__more {
  margin: 36px 0 0;
  text-align: center;
}

/* ---------- Under the stars ---------- */
.sky--dusk {
  background:
    url("/images/storybook/stars-tile.svg") repeat,
    linear-gradient(180deg, var(--twilight) 0%, #22396b 55%, var(--night) 100%);
  color: #fff;
}

.starry-cta {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  padding: clamp(110px, 12vw, 160px) 0 clamp(150px, 16vw, 220px);
  text-align: center;
}

.edge-wave--top {
  position: absolute;
  top: -1px;
  left: 0;
  z-index: 1;
  width: 100%;
  height: 60px;
  color: var(--cream); /* = previous section background */
  transform: scaleY(-1);
}

.starry-cta__inner h2 {
  margin: 0 0 12px;
  color: #fff;
  font-size: clamp(2.4rem, 5vw, 4.2rem);
}

.starry-cta__inner p {
  margin: 0 0 28px;
  color: var(--mist);
  font-size: 1.15rem;
}

.starry-cta .button-row {
  justify-content: center;
}

.scene__moon {
  position: absolute;
  top: 22%;
  right: 12%;
  width: clamp(60px, 7vw, 100px);
  height: clamp(60px, 7vw, 100px);
  color: var(--star-gold);
}

.scene__hills--night {
  height: clamp(90px, 11vw, 160px);
  color: var(--night); /* = footer top colour */
}

.starry-cta__kuska {
  position: absolute;
  bottom: 18px;
  left: 8%;
  width: clamp(130px, 14vw, 200px);
}

body[data-page="index"] .site-footer {
  margin-top: 0;
}

@media (max-width: 1080px) {
  .book-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 820px) {
  .cottage-grid,
  .book-grid {
    grid-template-columns: 1fr;
    max-width: 520px;
  }

  .book-grid {
    margin-inline: auto;
  }

  .starry-cta__kuska {
    left: 50%;
    width: 120px;
    transform: translateX(-50%);
  }
}
```

Add `.book-card { transition: none !important; }` to the reduced-motion block.

- [ ] **Step 6: Remove now-unused old homepage CSS** (`.location-grid`, `.location-card*`, `.post-grid`, `.post-card*`, `.cta-band*`) **only** for classes that `grep -l '<class>' kuska-website/*/index.html kuska-website/404.html` reports nowhere. `post-card` and `cta-band` are very likely still used by `blog/` and interior pages, so keep those.

- [ ] **Step 7: Run the checker** → `13 checks, 0 failures`. If the word budget fails, print `doc.text_of("main")` and trim the longest sentences. Never trim the H1, the addresses, or the phone number.

- [ ] **Step 8: Browser check** at 1280 and 375:
- two cottage cards with a coral and a blue roof peak, arch photos, phone and directions
- three book cards with coloured spines that tilt on hover; the whole card is clickable and Tab shows a focus ring around the card
- the CTA section waves down from cream into a twilight starry sky with a moon, white text, a yellow button plus a ghost phone button, and Kuska asleep on the dark hills
- the dark hills meet the night footer with no visible seam
- no horizontal scroll at 375

- [ ] **Step 9: Commit**

```bash
git -C "$P" add kuska-website/index.html kuska-website/storybook.css kuska-website/site.css scripts/check_site.py
git -C "$P" commit -m "Homepage locations cottages, story books, and under-the-stars CTA"
```

---

### Task 11: Motion: scroll reveal and hero parallax

**Files:**
- Modify: `kuska-website/site.js` (insert after the `year` block, **before** the `if (!toggle) { return; }` early return)
- Modify: `kuska-website/storybook.css`, `scripts/check_site.py`

**Interfaces:**
- Consumes: `[data-reveal]` attributes (Tasks 7–10), `[data-parallax="<factor>"]` (Task 6).
- Produces: `html.can-reveal` (added only by JS when motion is allowed); `.is-revealed` on revealed elements.

- [ ] **Step 1: Add the failing check (Review Focus #2)**

```python
def check_motion_safety():
    failures = []
    css = (ROOT / "storybook.css").read_text(encoding="utf-8")
    js = (ROOT / "site.js").read_text(encoding="utf-8")
    for selector, body in re.findall(r"([^{}]*\[data-reveal\][^{}]*)\{([^}]*)\}", css):
        if "opacity: 0" in body and ".can-reveal" not in selector:
            failures.append("storybook.css: [data-reveal] hidden without .can-reveal guard")
    if ".can-reveal [data-reveal]" not in css:
        failures.append("storybook.css: missing .can-reveal [data-reveal] rule")
    if "can-reveal" not in js or "prefers-reduced-motion" not in js:
        failures.append("site.js: reveal must add can-reveal and respect prefers-reduced-motion")
    elif js.index("can-reveal") > js.index("if (!toggle)"):
        failures.append("site.js: reveal code must run before the nav-toggle early return")
    count = Doc.load(ROOT / "index.html").raw.count("data-reveal")
    if count < 12:
        failures.append(f"index.html: expected at least 12 data-reveal elements, found {count}")
    return failures
```

Add to `CHECKS`; run → expect the `storybook.css`/`site.js` failures.

- [ ] **Step 2: Insert into `site.js`** directly after the `if (year) { … }` block:

```js
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  var revealables = document.querySelectorAll("[data-reveal]");
  if (revealables.length && "IntersectionObserver" in window && !reduceMotion) {
    document.documentElement.classList.add("can-reveal");
    var revealObserver = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("is-revealed");
          revealObserver.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -10% 0px" });
    revealables.forEach(function (el) {
      revealObserver.observe(el);
    });
  }

  var parallaxLayers = document.querySelectorAll("[data-parallax]");
  if (parallaxLayers.length && !reduceMotion) {
    var parallaxQueued = false;
    window.addEventListener("scroll", function () {
      if (parallaxQueued) {
        return;
      }
      parallaxQueued = true;
      window.requestAnimationFrame(function () {
        var y = window.scrollY;
        parallaxLayers.forEach(function (el) {
          var shift = (y * parseFloat(el.getAttribute("data-parallax"))).toFixed(1);
          el.style.transform = "translate3d(0, " + shift + "px, 0)";
        });
        parallaxQueued = false;
      });
    }, { passive: true });
  }
```

- [ ] **Step 3: Append reveal styles to `storybook.css`**

```css
/* ---------- Scroll reveal (only when JS opted in) ---------- */
.can-reveal [data-reveal] {
  opacity: 0;
  transform: translateY(24px);
  transition: opacity 0.7s ease, transform 0.7s ease;
}

.can-reveal [data-reveal].is-revealed {
  opacity: 1;
  transform: none;
}
```

These elements' hover transforms (`.story-card`, `.book-card`) must still work after reveal. `.is-revealed` sets `transform: none`, which beats `:hover` on specificity, so add:

```css
.can-reveal .story-card.is-revealed:hover,
.can-reveal .story-card.is-revealed:focus-within,
.can-reveal .book-card.is-revealed:hover,
.can-reveal .book-card.is-revealed:focus-within {
  transform: translateY(-6px) rotate(-1deg);
}
```

- [ ] **Step 4: Run the checker** → `14 checks, 0 failures`.

- [ ] **Step 5: Browser check: motion on**

At 1280, load `/` and scroll slowly with `browser_evaluate` (`window.scrollBy(0, 600)` in steps, `browser_wait_for` 1s between).
Expected:
- cards fade and rise in as they enter
- clouds drift, the sun turns slowly, and Kuska in the hero bobs
- the ridge shifts slightly on scroll (parallax)
- story and book cards still lift and tilt on hover
- the footer stars twinkle
- no console errors

- [ ] **Step 6: Browser check: reduced motion and no-JS fallback (Review Focus #2, #3)**

`browser_emulate_media` `reducedMotion: "reduce"` and reload.
Expected:
- `document.documentElement.classList.contains('can-reveal') === false`
- every `[data-reveal]` has computed opacity `1`
- the hero clouds have `animationName === 'none'`
- the ridge has no inline `transform` after scrolling

Then simulate no JS: `browser_evaluate` `document.documentElement.classList.remove('can-reveal')` on a normal-motion load. Every `[data-reveal]` must have opacity `1`.

- [ ] **Step 7: Commit**

```bash
git -C "$P" add kuska-website/site.js kuska-website/storybook.css scripts/check_site.py
git -C "$P" commit -m "Gentle scroll reveal and hero parallax, motion-safe"
```

---

### Task 12: Full verification pass

**Files:** none expected; fix forward in the owning file if anything fails.

- [ ] **Step 1: Static suite**

Run: `python3 -I scripts/check_site.py` → `14 checks, 0 failures`.

- [ ] **Step 2: Responsive sweep (Review Focus #1)**

For widths 375, 768, 1024, 1280 and 1440 on `/`: screenshot the full scroll (scroll through first so reveals fire) and run `document.documentElement.scrollWidth <= window.innerWidth`. All must be `true`. Also confirm the sticky header's scallop never covers the hero headline.

- [ ] **Step 3: Keyboard pass**

From the top of `/`, press Tab through the whole page. Expected order: skip link → logo → nav → header CTAs → hero button → "Explore evaluations" → 3 story-card links → (no focus on decorative art) → trail "Get started" → 6 logo links (only the first track) → cottage phone/directions ×2 → 3 book cards → "See all stories" → CTA buttons → footer links. Every stop must have a visible focus ring, including on the dark CTA and footer.

- [ ] **Step 4: Lighthouse (mobile)**

```bash
npx -y lighthouse@12 http://localhost:8000/ --form-factor=mobile --only-categories=performance,accessibility,seo,best-practices --output=json --output-path="$SCRATCH"/lh-home.json --chrome-flags="--headless=new" --quiet
python3 -I -c "import json,sys; r=json.load(open(sys.argv[1])); print({k:round(v['score']*100) for k,v in r['categories'].items()}, 'CLS', r['audits']['cumulative-layout-shift']['displayValue'])" "$SCRATCH"/lh-home.json
```

Expected: performance ≥ 90, accessibility ≥ 95, SEO ≥ 95, CLS < 0.1.
If performance is below 90, check (in this order): the size of `valley-dawn.webp` and the Kuska webps (re-encode lower), the `fetchpriority` hero photo, and the font weights requested. Fix, then re-run.

- [ ] **Step 5: Interior smoke test**

Load `/about/`, `/our-program/`, `/diagnostic-service/`, `/faqs/`, `/contact/`, `/get-started/`, `/blog/`, `/insurance-cover-aba-therapy/` and `/404.html` at 1280 and 375. Expect no broken layout, no console errors, new fonts, header and footer in place, and Zoho iframes rendering.

- [ ] **Step 6: Show the user**

Share screenshots at desktop and phone width (hero, middle sections, CTA and footer) and the Lighthouse scores. Note anything that deviates from the spec. Raster art can't blink, so Kuska **bobs** gently instead; say that explicitly. Then move to Task 13.

---

### Task 13: Commit and deploy

The user asked: "once you're done commit and deploy." Kuska is **not** in the workspace project→repo table, so confirm the remote with the user once before the first push.

- [ ] **Step 1: Verify the repo (workspace CLAUDE.md protocol)**

```bash
P="/Users/joshdennis/Documents/App Projects/Websites/Kuska Website"
git -C "$P" rev-parse --show-toplevel   # must end in /Kuska Website
git -C "$P" remote get-url origin       # expected: https://github.com/jaymdenn/kuska-website.git
git -C "$P" status --short              # must be empty (everything committed per task)
git -C "$P" fetch origin
git -C "$P" log --oneline storybook-phase-1..origin/main   # must be empty; if not, stop and ask
```

If the toplevel or remote differs, or `origin/main` has new commits, **stop and ask**. Otherwise, confirm with the user: "Pushing to `github.com/jaymdenn/kuska-website` `main`, which Netlify deploys to kuska.co. OK?" (This is skipped if the user already confirmed this remote in this session.)

- [ ] **Step 2: Fast-forward `main` and push**

```bash
git -C "$P" switch main
git -C "$P" merge --ff-only storybook-phase-1
git -C "$P" branch --show-current          # must print: main
git -C "$P" push origin main
```

- [ ] **Step 3: Confirm the deploy**

Use the Netlify MCP (`netlify-deploy-services-reader`) to find the latest deploy for the site linked to `jaymdenn/kuska-website`. Wait until its state is `ready`, then load `https://kuska.co/` in the browser. Confirm the new hero headline and the night footer are live and there are no console errors. If the deploy fails, report the build log and do **not** retry blindly.

- [ ] **Step 4: Report**

Tell the user which repo and branch were pushed (`jaymdenn/kuska-website` → `main`) and the deploy status and URL. Mention that Phase 2 (main interior pages) is next and gets its own plan.
