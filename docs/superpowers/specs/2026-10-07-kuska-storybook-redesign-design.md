# Kuska Storybook Redesign — Design Spec

**Date:** 2026-10-07
**Status:** Awaiting review
**Project:** Kuska Website (`kuska-website/`, deployed to Netlify from `github.com/jaymdenn/kuska-website`, branch `main`)

## 1. Intent

Make kuska.co feel **fun, playful, whimsical, imaginative, and inviting — while staying professional and upscale** — with far more imagery than today.

- **Audience:** parents (often anxious, often newly navigating an autism diagnosis) choosing an ABA / evaluation provider in Bountiful and Draper, Utah.
- **Success looks like:** a parent lands on the site and feels delight and warmth within seconds, and still trusts Kuska as a serious clinical provider. Whimsical, never childish.
- **Known problem to fix:** the homepage hero is too wordy (H1 + subtitle + 40-word paragraph + two buttons + checklist).

### Decisions made
| Decision | Choice |
|---|---|
| Source of whimsy | Storybook illustrations |
| Art production | Hybrid: AI-generated key art (Higgsfield/OpenArt) + hand-coded SVG |
| Rollout | Homepage + design system first, then main pages, then blog/legal |
| Creative direction | **A — "The Kuska Valley" journey** |
| Hero headline | **"Your child's story is just getting started."** |
| Scope of change | Anything on the site may change (copy, layout, structure), subject to the constraints below |

### Constraints
- Stays a static HTML/CSS/JS site on Netlify — no framework, no build step.
- Pages are hand-maintained; **do not re-run `scripts/build_custom_site.py`**.
- Header/footer markup is duplicated across every `index.html` and `404.html` — changes must be applied to all.
- Preserve SEO work: keyword-bearing H1s, meta descriptions, canonicals, `og:` tags, JSON-LD, `sitemap.xml`, `_redirects`.
- Preserve the WCAG 2.2 accessibility fixes already shipped.
- Zoho iframe forms on Contact / Get Started remain the form mechanism.
- Existing `/wp-content/uploads/...` image paths remain valid.
- Business facts unchanged: (801) 980-7970, admin@kuska.co, 95 2200 S Bountiful UT 84010, 12055 S 700 E Draper UT 84020.
- Nothing is pushed to GitHub (which auto-deploys) without explicit approval.

## 2. Concept — "The Kuska Valley"

The site is one continuous illustrated landscape blending **Andean vicuña country with Utah's Wasatch range**. Scrolling down the homepage moves through a day: **dawn → day → dusk → night**. A vicuña character, **Kuska**, appears as a gentle guide. The brand meaning — *Kuska* = "together" — is the emotional thread, and the storybook framing ("Your child's story…") is the narrative thread.

## 3. Visual language

### 3.1 Typography
| Role | Font | Notes |
|---|---|---|
| Display / headings | **Fraunces** (Google Fonts, variable) | Use `SOFT` and `WONK` axes for a soft, storybook-serif feel; sentence case; generous sizes |
| Body / UI | **Montserrat** (existing) | Body copy, nav, buttons, labels |
| Hand-written accents | **Caveat** | Sparse annotations only (e.g. trail labels, "← that's Kuska!"); never for essential information |

Load only the weights actually used, with `display=swap`. Montserrat Alternates is retired unless a specific use remains.

### 3.2 Palette (CSS custom properties in `site.css :root`)
| Token | Hex | Use |
|---|---|---|
| `--cream` | `#FFF8EC` | Dawn backgrounds, cards |
| `--sky` | `#B7D9F3` | Dawn sky, soft fills (existing brand light blue) |
| `--sun` | `#EBC94E` | Kuska Yellow — primary CTA, sun, highlights |
| `--kuska-blue` | `#3989C9` | Kuska Blue — links, day sky, accents |
| `--sage` | `#8FBF9F` | Meadow / hills |
| `--coral` | `#F08A6C` | Warm accents, stickers |
| `--deep-blue` | `#004E85` | Dusk, footer base, headings on light |
| `--twilight` | `#5B5AA6` | Dusk gradient |
| `--star-gold` | `#F6D77A` | Stars, footer links |
| `--ink` | `#17344A` | Body text |

Every text/background pairing must pass **WCAG AA** (4.5:1 body, 3:1 large text/UI). Decorative colors (sage, coral, sky) are not used for body text on light backgrounds unless darkened variants pass.

### 3.3 Illustration
- **Style:** soft flat shapes, rounded edges, gentle gradients, subtle paper-grain texture. Modern picture book — not clip art, not cartoonish.
- **Kuska the vicuña:** cream-and-caramel vicuña with a Kuska Blue scarf. Poses: **waving, walking, reading with a child, pointing, sleeping under stars**. Consistent character across poses.
- **AI-generated (Higgsfield/OpenArt):** vicuña poses (transparent background) and 1–2 hero background paintings. Generated, shown to the client as a contact sheet, only approved pieces used.
- **Hand-coded SVG:** layered hills, Wasatch ridgelines, clouds, sun, moon, stars, trail paths, wavy/hill section edges, doodles (sparkles, hearts, flowers). Collected in a single sprite `illustrations.svg`, referenced with `<use>`.
- Decorative art is `aria-hidden="true"` / `alt=""`.

### 3.4 Photography
Existing family/child photos remain central for trust, framed as part of the world:
- `.photo-window` — rounded "window" shapes set into hills
- `.polaroid` — white-bordered, slightly rotated, pinned with a doodled star
- circular crops with a hand-drawn ring

More photos per section than today. Photos keep meaningful `alt` text.

### 3.5 Motion
Calm, CSS-driven:
- clouds drift slowly; stars twinkle; vicuña blinks
- cards lift with ~1° tilt on hover
- sections fade/rise into view (IntersectionObserver in `site.js`)
- subtle hill parallax in the hero

All motion is disabled under `prefers-reduced-motion: reduce`.

## 4. Shared components (`site.css`)

| Component | Purpose |
|---|---|
| `.scene` | Layered illustrated background container (sky + SVG hills + art) |
| `.sky--dawn` / `--day` / `--dusk` / `--night` | Section mood backgrounds |
| `.edge--wave` / `.edge--hills` | Organic section transitions |
| `.photo-window`, `.polaroid`, `.photo-ring` | Photo frames |
| `.sticker` | Badge/pill with doodle icon (trust points, values) |
| `.trail`, `.trail__stop` | Winding dotted path with numbered signposts |
| `.story-card` | Card with photo, doodle, short copy, link; hover lift/tilt |
| `.flower-tag` | Pill tag with tiny flower icon (skills field) |
| `.book-card` | Blog card styled as a picture-book cover |
| `.chapter-hero` | Short illustrated hero for interior pages |
| `.letter-card` | Framed container for Zoho iframe forms |
| `.question-card` | Expandable FAQ item (`<details>/<summary>`) |
| `.button` (primary sun-yellow pill), `.button--ghost`, `.text-link` | Actions |

### Header
Cream bar with a soft scalloped bottom edge; logo; tightened nav; sun-yellow "Get Started" pill. Resources dropdown keeps hover (pointer) + click/keyboard behavior. Mobile: full-screen "sky" menu panel.

### Footer
Night-sky continuation: deep blue with twinkling SVG stars, a moon, star-gold links, existing footer content (locations linked to Google Maps, contact, nav, legal).

## 5. Homepage, section by section

Target: roughly **half** the current homepage word count.

1. **Hero — "Sunrise over the valley"** (`.sky--dawn`)
   - H1 contains a small keyword label + the display headline:
     *ABA Therapy & Autism Evaluations · Bountiful & Draper* / **Your child's story is just getting started.**
   - Sub-line: *Compassionate ABA therapy and evaluations in Bountiful & Draper.* (may be reworded to avoid repeating the label verbatim)
   - Primary button **Schedule a consultation**; text link *Explore evaluations →*
   - Scene: layered hills + Wasatch peaks, rising sun, drifting clouds, Kuska waving; two family photos in hillside windows.
   - Floating stickers: *No-waitlist evaluations* · *In-home, clinic & hybrid* · *Parents as partners*.

2. **How we help — "The meadow"** (`.sky--day`)
   - Three `.story-card`s: Autism Evaluations, ABA Therapy, In-home or Clinic — photo, doodle, one line, link.
   - Ten skill areas as a scattered `.flower-tag` field.

3. **Why Kuska — "The name story"**
   - Split layout: Kuska-reading-with-child illustration + 2–3 sentence story ("*Kuska* means *together*…").
   - Four values (Kuska, Quality Care, Radical Candor, Play) as `.sticker` badges with one-liners.

4. **Getting started — "The winding trail"**
   - SVG dotted `.trail` with three signposts: Talk with us → Assessment → Build the plan; one line + small photo/illustration each.
   - Kuska walking at the trailhead; **Get started** button at the trail's end.

5. **Insurance — "Friends along the way"**
   - Insurer logos on cream cards in a gently scrolling row (pauses on hover/focus; static under reduced motion). One line: *In-network with the plans Utah families use.*

6. **Locations — "Two homes in the valley"**
   - Bountiful and Draper storybook-cottage cards: photo window, address, phone, directions button.

7. **Helpful reads — "Stories for the journey"**
   - Three `.book-card`s + link to all posts.

8. **Closing CTA — "Under the stars"** (`.sky--dusk` → `.sky--night`)
   - Stars, moon, Kuska sleeping on a hill. Headline *Ready when you are.* + consultation button + phone.
   - Flows directly into the night-sky footer.

## 6. Rollout phases

Each phase is reviewed and approved before the next begins.

**Phase 1 — System + homepage**
- Rewrite `site.css` around new tokens and components.
- Create `illustrations.svg` sprite and `/images/storybook/` art directory.
- Generate and approve key art (vicuña poses, hero background).
- New header/footer applied to **all** `index.html` files and `404.html` (scripted, diff-reviewed).
- Fully redesigned homepage.
- Interior pages must remain readable with the new CSS even before their own redesign (no broken layouts in between).

**Phase 2 — Main pages**
About, Our Program, Diagnostic Service, FAQs, Insurance (`insurance-cover-aba-therapy`), Get Started, Contact, Careers, Our Organization, Social Skills Camps.
- `.chapter-hero` with a vicuña pose and photo on each.
- About: name story and vicuña mark as a storybook spread.
- FAQs: `.question-card`s.
- Contact/Get Started: Zoho iframes inside `.letter-card`.

**Phase 3 — Blog and legal**
- Blog index: `.book-card` grid.
- Posts: small illustrated header band, Fraunces headings, comfortable measure, illustrated drop cap; article content untouched.
- Privacy, Terms, Non-discrimination: typography only.

## 7. Performance
- Hero art preloaded/eager; all other images `loading="lazy"` with explicit `width`/`height`.
- Art exported as WebP, responsive sizes via `srcset`.
- One shared SVG sprite (cached across pages).
- Animation in CSS; `site.js` gains only a small reveal observer.
- **Target:** Lighthouse mobile Performance ≥ 90, CLS < 0.1.

## 8. Accessibility
- AA contrast for all text and interactive states.
- Decorative art hidden from assistive tech; photos keep real alt text.
- `prefers-reduced-motion` disables all animation including the logo scroller.
- Visible focus styles; keyboard-operable nav dropdown, mobile menu, FAQ cards.
- Handwritten Caveat text never carries essential information.
- Retain all prior WCAG 2.2 fixes (skip link, landmarks, labels).

## 9. SEO
- Keep keyword H1s (hero H1 includes the service + location label), title tags, meta descriptions, canonicals, `og:` tags, JSON-LD, `sitemap.xml`, `_redirects`.
- Trimmed copy retains service and location keywords in headings.
- No URL changes.

## 10. Verification
- Local preview: `cd kuska-website && python3 -m http.server 8000`, checked in Chrome at ~375px, ~768px, and ~1280px.
- Check reduced-motion, keyboard-only navigation, contrast, and console errors.
- Lighthouse run on homepage (and representative interior page in later phases).
- Diff review of the scripted header/footer change across all pages.
- Client review at the end of each phase; **no push until explicitly approved**.

## 11. Out of scope
- New pages or URL restructuring.
- Replacing Zoho forms with native forms.
- Changing blog article body content.
- Hiring a human illustrator (the hybrid approach replaces this; art can be swapped later since slots are isolated in `/images/storybook/`).
