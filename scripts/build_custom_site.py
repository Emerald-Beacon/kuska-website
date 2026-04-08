#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from textwrap import dedent

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parent.parent
SITE_ROOT = ROOT / "kuska-website"
LOGO_PATH = "/wp-content/uploads/2025/05/kuska-autism-services-logo.png"
PHONE_DISPLAY = "(801) 980-7970"
PHONE_HREF = "tel:+18019807970"
EMAIL = "admin@kuska.co"
ANNOUNCEMENT = (
    "Now accepting new ABA therapy clients and autism evaluation inquiries in "
    "Bountiful and Draper, Utah."
)


@dataclass
class Post:
    slug: str
    title: str
    excerpt: str
    description: str
    date_iso: str
    date_display: str
    body_html: str
    featured_image: str


NAV_LINKS = [
    ("/", "Home", "index"),
    ("/about/", "About", "about"),
    ("/diagnostic-service/", "Diagnosing", "diagnostic-service"),
    ("/our-program/", "Our Program", "our-program"),
    ("/faqs/", "FAQs", "faqs"),
    ("/careers/", "Careers", "careers"),
    ("/contact/", "Contact", "contact"),
    ("/blog/", "Blog", "blog"),
    ("/social-skills-camps/", "Social Skills Camps", "social-skills-camps"),
]

POST_IMAGE_MAP = {
    "insurance-cover-aba-therapy": "/wp-content/uploads/2026/03/girl-drawing-on-blackboard-2026-01-05-06-14-59-utc.jpg",
    "preparing-for-your-childs-first-aba-session-what-utah-families-need-to-know": "/wp-content/uploads/2026/01/toddler-playing-in-living-room-2026-01-06-09-01-22-utc.jpg",
    "19-questions-every-utah-parent-should-ask-before-choosing-an-aba-provider": "/wp-content/uploads/2026/01/trying-to-learn-how-to-draw-holding-pencil-speec-2026-01-09-13-51-30-utc.jpg",
    "choosing-the-best-aba-therapy-provider-in-bountiful-a-guide-for-utah-parents": "/wp-content/uploads/2026/02/cute-black-little-girl-holding-planet-model-and-sm-2026-01-08-06-52-40-utc.jpg",
    "early-signs-of-autism-in-toddlers-seeking-timely-diagnosis-in-bountiful-and-draper-utah": "/wp-content/uploads/2026/02/smiling-parents-helping-their-son-with-homework-at-2026-01-11-11-14-02-utc.jpg",
    "when-aba-therapy-feels-overwhelming-managing-parent-burnout-while-supporting-your-child": "/wp-content/uploads/2025/12/woman-working-on-a-laptop-at-home-2024-11-05-10-21-43-utc.jpg",
    "supporting-your-whole-family-how-aba-therapy-impacts-siblings-and-what-parents-can-do": "/wp-content/uploads/2025/12/child-daughter-family-happy-mother-father-board-ga-2025-01-29-08-07-32-utc.jpg",
    "understanding-the-autism-evaluation-process-in-utah-a-parents-2026-guide": "/wp-content/uploads/2025/11/psychology-test-for-children-toddler-coloring-sh-2024-10-18-10-56-05-utc-scaled.jpg",
    "what-to-expect-during-your-childs-aba-assessment-a-parents-guide-to-the-evaluation-process": "/wp-content/uploads/2025/11/happy-parents-and-kids-spending-time-together-and-2025-03-18-14-21-06-utc.jpg",
    "when-aba-progress-feels-slow-understanding-your-childs-learning-journey-and-what-really-matters": "/wp-content/uploads/2025/11/a-woman-teaching-a-child-how-to-use-a-weighing-bal-2025-10-17-00-47-38-utc.jpg",
    "balancing-aba-therapy-with-family-life-managing-schedules-siblings-and-your-own-needs": "/wp-content/uploads/2025/11/mum-and-son-spending-time-together-2025-10-10-00-28-11-utc-scaled.jpg",
    "preparing-your-child-with-autism-for-holiday-gatherings-aba-strategies-for-family-events": "/wp-content/uploads/2025/10/outdoor-family-weekend-2025-03-06-07-46-26-utc-scaled.jpg",
    "the-utah-parents-evidence-based-guide-to-aba-therapy": "/wp-content/uploads/2025/09/occupational-therapist-using-sensory-integration-t-2025-07-09-06-23-51-utc-1-scaled.jpg",
    "in-home-vs-clinic-aba-therapy": "/wp-content/uploads/2025/09/caring-family-with-dog-2025-03-10-01-09-15-utc-2.jpg",
    "your-childs-first-aba-session-a-certified-behavior-analysts-complete-guide": "/wp-content/uploads/2025/09/little-boy-learns-words-from-cards-under-the-aba-t-2024-09-26-04-01-59-utc-1.jpg",
    "choosing-an-aba-provider-in-utah-10-critical-questions-from-kuska-autism-services": "/wp-content/uploads/2025/09/afro-parents-helping-their-children-with-his-homew-2024-10-18-03-36-16-utc.jpg",
    "how-aba-therapy-helps-kids-with-autism": "/wp-content/uploads/2025/08/enthusiastic-girl-showing-robot-to-classmates-in-c-2025-05-16-16-39-56-utc-1.jpg",
}


def clean_html_fragment(raw_html: str) -> str:
    soup = BeautifulSoup(raw_html, "lxml")

    for tag in soup.select("script, style"):
        tag.decompose()

    for tag in soup.find_all(True):
        allowed = {
            "a": {"href", "target", "rel"},
            "img": {"src", "alt", "title", "width", "height", "srcset", "sizes", "loading"},
            "iframe": {"src", "title", "aria-label", "width", "height", "style", "frameborder", "allow", "allowfullscreen"},
            "h2": {"id"},
            "h3": {"id"},
            "section": set(),
            "details": set(),
            "summary": set(),
        }
        keep = allowed.get(tag.name, set())
        attrs = dict(tag.attrs)
        for attr in attrs:
            if attr not in keep:
                del tag.attrs[attr]

    for node in soup.find_all(["p", "li", "h2", "h3", "h4"]):
        text = node.get_text(" ", strip=True)
        if not text:
            node.decompose()

    body = soup.body or soup
    return "".join(str(child) for child in body.children).strip()


def extract_post(slug: str) -> Post:
    post_path = SITE_ROOT / slug / "index.html"
    json_path = SITE_ROOT / "wp-json" / "wp" / "v2" / "posts"
    post_json = None
    for candidate in json_path.glob("*.bin"):
        data = json.loads(candidate.read_text())
        if data["slug"] == slug:
            post_json = data
            break

    if post_json is None:
        raise FileNotFoundError(f"Missing JSON data for post: {slug}")

    soup = BeautifulSoup(post_path.read_text(encoding="utf-8", errors="ignore"), "lxml")
    title = soup.select_one(".et_pb_post_title_0_tb_body .entry-title") or soup.select_one(".hero--article h1")
    date = soup.select_one(".et_pb_post_title_0_tb_body .published") or soup.select_one(".meta-line")
    image = soup.select_one(".et_pb_title_featured_container img") or soup.select_one(".hero-portrait")
    content = soup.select_one(".et_pb_post_content_0_tb_body .et_pb_text_inner")
    if content is None:
        content = soup.select_one(".et_pb_post_content_0_tb_body")
    if content is None:
        content = soup.select_one(".article-content")

    if not title or not content:
        raise ValueError(f"Unable to extract post content for {slug}")

    excerpt = re.sub(r"<[^>]+>", " ", post_json["excerpt"]["rendered"])
    excerpt = re.sub(r"\s+", " ", excerpt).strip().replace("[&hellip;]", "…")
    excerpt = excerpt.replace("[…]", "…")
    excerpt = excerpt or title.get_text(" ", strip=True)

    raw_date = post_json["date"][:10]
    date_obj = datetime.strptime(raw_date, "%Y-%m-%d")

    return Post(
        slug=slug,
        title=title.get_text(" ", strip=True),
        excerpt=excerpt,
        description=excerpt,
        date_iso=raw_date,
        date_display=date_obj.strftime("%B %d, %Y"),
        body_html=clean_html_fragment(content.decode_contents()),
        featured_image=POST_IMAGE_MAP.get(slug) or (image.get("src") if image else "/wp-content/uploads/2025/05/Image1.jpg"),
    )


def extract_privacy_html() -> str:
    soup = BeautifulSoup(
        (SITE_ROOT / "privacy-policy" / "index.html").read_text(encoding="utf-8", errors="ignore"),
        "lxml",
    )
    blocks = [node.decode_contents() for node in soup.select("#main-content .et_pb_text_inner")]
    return clean_html_fragment("".join(blocks))


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def page_path(slug: str) -> Path:
    if slug == "index":
        return SITE_ROOT / "index.html"
    return SITE_ROOT / slug / "index.html"


def nav_html(current_slug: str) -> str:
    items = []
    for href, label, slug in NAV_LINKS:
        current = ' aria-current="page"' if slug == current_slug else ""
        active = " is-active" if slug == current_slug else ""
        items.append(f'<a class="site-nav__link{active}" href="{href}"{current}>{label}</a>')
    return "\n".join(items)


def article_card(post: Post, featured: bool = False) -> str:
    cls = "post-card post-card--featured" if featured else "post-card"
    return dedent(
        f"""
        <article class="{cls}">
          <a class="post-card__image" href="/{post.slug}/">
            <img src="{post.featured_image}" alt="{html.escape(post.title)}" loading="lazy">
          </a>
          <div class="post-card__body">
            <p class="eyebrow">{post.date_display}</p>
            <h3><a href="/{post.slug}/">{html.escape(post.title)}</a></h3>
            <p>{html.escape(post.excerpt)}</p>
            <a class="text-link" href="/{post.slug}/">Read article</a>
          </div>
        </article>
        """
    ).strip()


def location_cards() -> str:
    return dedent(
        f"""
        <div class="location-grid">
          <article class="location-card">
            <p class="eyebrow">Bountiful</p>
            <h3>95 2200 S<br>Bountiful, UT 84010</h3>
            <p>Morning and daytime ABA therapy availability, plus autism evaluation support.</p>
            <div class="location-card__actions">
              <a class="button button--secondary" href="{PHONE_HREF}">{PHONE_DISPLAY}</a>
              <a class="text-link" href="https://www.google.com/maps/dir/?api=1&amp;destination=95+2200+S,+Bountiful,+UT+84010" target="_blank" rel="noopener">Get directions</a>
            </div>
          </article>
          <article class="location-card">
            <p class="eyebrow">Draper</p>
            <h3>12055 S 700 E<br>Draper, UT 84020</h3>
            <p>Flexible scheduling for families across Salt Lake County and surrounding communities.</p>
            <div class="location-card__actions">
              <a class="button button--secondary" href="{PHONE_HREF}">{PHONE_DISPLAY}</a>
              <a class="text-link" href="https://www.google.com/maps/dir/?api=1&amp;destination=12055+S+700+E,+Draper,+UT+84020" target="_blank" rel="noopener">Get directions</a>
            </div>
          </article>
        </div>
        """
    ).strip()


def insurance_strip() -> str:
    logos = [
        ("/wp-content/uploads/2025/05/medicaid-3.png", "Utah Medicaid"),
        ("/wp-content/uploads/2025/05/select-health-logo.jpg", "Select Health"),
        ("/wp-content/uploads/2025/05/Optum-Logo-2011-e1746217706743.png", "Optum"),
        ("/wp-content/uploads/2025/05/United-Healthcare-Logo.png", "United Healthcare"),
        ("/wp-content/uploads/2025/05/Evernorth_Logo.png", "Evernorth"),
        ("/wp-content/uploads/2025/05/blue-cross-blue-shield-vector-logo.png", "Blue Cross Blue Shield"),
    ]
    items = []
    for src, alt in logos:
        items.append(f'<li><img src="{src}" alt="{alt}" loading="lazy"></li>')
    return "<ul class=\"logo-strip\">" + "".join(items) + "</ul>"


def base_schema() -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "MedicalClinic",
        "name": "Kuska Autism Services",
        "url": "https://kuska.co/",
        "telephone": "+1-801-980-7970",
        "email": EMAIL,
        "logo": f"https://kuska.co{LOGO_PATH}",
        "address": [
            {
                "@type": "PostalAddress",
                "streetAddress": "95 2200 S",
                "addressLocality": "Bountiful",
                "addressRegion": "UT",
                "postalCode": "84010",
                "addressCountry": "US",
            },
            {
                "@type": "PostalAddress",
                "streetAddress": "12055 S 700 E",
                "addressLocality": "Draper",
                "addressRegion": "UT",
                "postalCode": "84020",
                "addressCountry": "US",
            },
        ],
        "sameAs": [
            "https://www.facebook.com/profile.php?id=61574835185465",
            "https://www.instagram.com/kuska_autismservices/",
        ],
    }
    return json.dumps(schema, separators=(",", ":"))


def layout(
    *,
    current_slug: str,
    title: str,
    description: str,
    canonical: str,
    body_html: str,
    og_type: str = "website",
    extra_schema: str | None = None,
) -> str:
    title_text = f"{title} | Kuska Autism Services"
    schema_tags = [
        f'<script type="application/ld+json">{base_schema()}</script>',
    ]
    if extra_schema:
        schema_tags.append(f'<script type="application/ld+json">{extra_schema}</script>')

    return dedent(
        f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="utf-8">
          <meta name="viewport" content="width=device-width, initial-scale=1">
          <title>{html.escape(title_text)}</title>
          <meta name="description" content="{html.escape(description)}">
          <link rel="canonical" href="https://kuska.co{canonical}">
          <meta property="og:type" content="{og_type}">
          <meta property="og:title" content="{html.escape(title_text)}">
          <meta property="og:description" content="{html.escape(description)}">
          <meta property="og:url" content="https://kuska.co{canonical}">
          <meta property="og:site_name" content="Kuska Autism Services">
          <meta name="twitter:card" content="summary_large_image">
          <meta name="theme-color" content="#3989c9">
          <link rel="preconnect" href="https://fonts.googleapis.com">
          <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
          <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800&family=Montserrat+Alternates:wght@500;600;700;800&display=swap" rel="stylesheet">
          <link rel="icon" href="/wp-content/uploads/2025/05/cropped-kuska-autism-services-logo-32x32.png" sizes="32x32">
          <link rel="apple-touch-icon" href="/wp-content/uploads/2025/05/cropped-kuska-autism-services-logo-180x180.png">
          <link rel="stylesheet" href="/site.css">
          {' '.join(schema_tags)}
        </head>
        <body data-page="{current_slug}">
          <a class="skip-link" href="#content">Skip to content</a>
          <div class="announcement-bar">
            <div class="shell announcement-bar__inner">
              <p>{html.escape(ANNOUNCEMENT)}</p>
            </div>
          </div>
          <header class="site-header">
            <div class="shell site-header__inner">
              <a class="site-brand" href="/" aria-label="Kuska Autism Services home">
                <img src="{LOGO_PATH}" alt="Kuska Autism Services">
              </a>
              <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button>
              <nav class="site-nav" id="site-nav" aria-label="Main navigation">
                {nav_html(current_slug)}
              </nav>
              <div class="site-header__cta">
                <a class="button button--secondary" href="{PHONE_HREF}">{PHONE_DISPLAY}</a>
                <a class="button" href="/get-started/">Get Started</a>
              </div>
            </div>
          </header>
          <main id="content">
            {body_html}
          </main>
          <footer class="site-footer">
            <div class="shell site-footer__grid">
              <div>
                <img class="site-footer__logo" src="{LOGO_PATH}" alt="Kuska Autism Services">
                <p>Kuska Autism Services provides autism evaluations and personalized ABA therapy for families in Bountiful, Draper, and nearby Utah communities.</p>
              </div>
              <div>
                <p class="eyebrow">Contact</p>
                <ul class="footer-list">
                  <li><a href="{PHONE_HREF}">{PHONE_DISPLAY}</a></li>
                  <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
                  <li><a href="/contact/">Contact page</a></li>
                  <li><a href="/privacy-policy/">Privacy policy</a></li>
                </ul>
              </div>
              <div>
                <p class="eyebrow">Locations</p>
                <ul class="footer-list">
                  <li>Bountiful, Utah</li>
                  <li>Draper, Utah</li>
                  <li>Davis County</li>
                  <li>Salt Lake County</li>
                </ul>
              </div>
            </div>
            <div class="shell site-footer__bottom">
              <p>Copyright © <span id="year">2026</span> Kuska Autism Services. All rights reserved.</p>
            </div>
          </footer>
          <script src="/site.js" defer></script>
        </body>
        </html>
        """
    ).strip() + "\n"


def home_page(posts: list[Post]) -> tuple[str, str]:
    latest_cards = "\n".join(article_card(post, featured=index == 0) for index, post in enumerate(posts[:4]))
    body = dedent(
        f"""
        <section class="hero hero--home">
          <div class="shell hero__grid">
            <div class="hero__content">
              <p class="eyebrow">ABA Therapy and Autism Diagnosis in Utah</p>
              <h1>Friendly, evidence-based support for young children and the parents who love them.</h1>
              <p class="lead">Kuska Autism Services helps families in Bountiful, Draper, and surrounding Utah communities move from uncertainty to a clear next step with autism evaluations, personalized ABA therapy, and warm, collaborative care.</p>
              <div class="button-row">
                <a class="button" href="/get-started/">Schedule a consultation</a>
                <a class="button button--secondary" href="/diagnostic-service/">Explore autism evaluations</a>
              </div>
              <div class="hero-highlights" aria-label="Kuska service highlights">
                <p class="hero-highlights__label">What families can expect</p>
                <ul class="hero-badges">
                  <li>No-waitlist evaluation inquiries</li>
                  <li>In-home, clinic, and hybrid ABA options</li>
                  <li>Parent partnership at every stage</li>
                </ul>
              </div>
            </div>
            <div class="hero__visual">
              <div class="hero-photo-stack">
                <img class="hero-photo hero-photo--large" src="/wp-content/uploads/2025/05/Image1.jpg" alt="Child playing with therapist" loading="eager">
                <img class="hero-photo hero-photo--small" src="/wp-content/uploads/2025/05/About-1.jpeg" alt="Parent and child smiling together" loading="lazy">
              </div>
            </div>
          </div>
        </section>

        <section class="section">
          <div class="shell">
            <div class="section-heading">
              <p class="eyebrow">How Kuska Helps</p>
              <h2>Support that feels personal, practical, and built for real family life.</h2>
            </div>
            <div class="service-grid">
              <article class="feature-card">
                <h3>Autism evaluations</h3>
                <p>We help families get answers, understand strengths and challenges, and move toward the right next level of care.</p>
              </article>
              <article class="feature-card">
                <h3>ABA therapy programs</h3>
                <p>Plans are individualized around communication, play, behavior support, school readiness, daily living skills, and independence.</p>
              </article>
              <article class="feature-card">
                <h3>In-home or clinic-based care</h3>
                <p>Choose the setting that works best for your child and your family schedule, with flexible options in Bountiful and Draper.</p>
              </article>
            </div>
            <div class="chip-cloud">
              <span>Speech and communication</span>
              <span>Social skills</span>
              <span>Emotional regulation</span>
              <span>Daily living skills</span>
              <span>School readiness</span>
              <span>Toilet training</span>
              <span>Coping skills</span>
              <span>Community connection</span>
              <span>Problem solving</span>
              <span>Play and leisure</span>
            </div>
          </div>
        </section>

        <section class="section section--tint">
          <div class="shell split-panel">
            <div>
              <p class="eyebrow">Why Parents Choose Kuska</p>
              <h2>Locally owned. Trauma-informed. Built on teamwork.</h2>
              <p>Families come to Kuska for clinical quality, but they stay because they feel genuinely supported. The current site already says it well: Kuska means “together,” and that spirit shows up in how clinicians work with children, coach caregivers, and communicate with honesty and respect.</p>
              <p>Our refreshed site keeps that message front and center while making it easier for parents to understand what ABA therapy is, what autism evaluations look like, and how to get started without feeling overwhelmed.</p>
            </div>
            <div class="value-stack">
              <article>
                <h3>Kuska</h3>
                <p>We succeed together, with parents and clinicians aligned around meaningful goals.</p>
              </article>
              <article>
                <h3>Quality Care</h3>
                <p>Evidence-based ABA paired with compassionate, individualized support.</p>
              </article>
              <article>
                <h3>Radical Candor</h3>
                <p>Clear, respectful, timely communication that helps families feel informed.</p>
              </article>
              <article>
                <h3>Play</h3>
                <p>Children learn best when therapy feels engaging, motivating, and human.</p>
              </article>
            </div>
          </div>
        </section>

        <section class="section">
          <div class="shell">
            <div class="section-heading">
              <p class="eyebrow">Getting Started</p>
              <h2>A simple path from first question to next step.</h2>
            </div>
            <div class="steps-grid">
              <article class="step-card">
                <span>1</span>
                <h3>Talk with our team</h3>
                <p>We’ll learn more about your child, answer questions, and help you understand the best starting point.</p>
              </article>
              <article class="step-card">
                <span>2</span>
                <h3>Complete an assessment</h3>
                <p>We identify strengths, challenges, and the clinical recommendations that make sense for your family.</p>
              </article>
              <article class="step-card">
                <span>3</span>
                <h3>Build the plan together</h3>
                <p>Goals, schedules, and service setting are shaped around what’s realistic, supportive, and meaningful.</p>
              </article>
            </div>
          </div>
        </section>

        <section class="section section--compact">
          <div class="shell">
            <div class="section-heading">
              <p class="eyebrow">Insurance</p>
              <h2>In-network with major funders families already use.</h2>
            </div>
            {insurance_strip()}
          </div>
        </section>

        <section class="section section--tint">
          <div class="shell">
            <div class="section-heading">
              <p class="eyebrow">Locations</p>
              <h2>Visit us in Bountiful or Draper.</h2>
            </div>
            {location_cards()}
          </div>
        </section>

        <section class="section">
          <div class="shell">
            <div class="section-heading">
              <p class="eyebrow">Helpful Reads</p>
              <h2>Parent-friendly resources that support your next step.</h2>
            </div>
            <div class="post-grid">{latest_cards}</div>
          </div>
        </section>

        <section class="cta-band">
          <div class="shell cta-band__inner">
            <div>
              <p class="eyebrow">Ready when you are</p>
              <h2>Let’s help your family feel more confident about what comes next.</h2>
            </div>
            <div class="button-row">
              <a class="button" href="/get-started/">Get started</a>
              <a class="button button--secondary" href="/contact/">Contact Kuska</a>
            </div>
          </div>
        </section>
        """
    ).strip()
    desc = (
        "Kuska Autism Services offers autism evaluations and personalized ABA therapy "
        "in Bountiful and Draper, Utah, with warm family-centered care and flexible options."
    )
    return body, desc


def standard_page(hero_eyebrow: str, hero_title: str, hero_copy: str, body: str, image: str) -> str:
    return dedent(
        f"""
        <section class="hero hero--interior">
          <div class="shell hero__grid">
            <div class="hero__content">
              <p class="eyebrow">{hero_eyebrow}</p>
              <h1>{hero_title}</h1>
              <p class="lead">{hero_copy}</p>
            </div>
            <div class="hero__visual">
              <img class="hero-portrait" src="{image}" alt="{hero_title}" loading="eager">
            </div>
          </div>
        </section>
        {body}
        """
    ).strip()


def page_bodies(posts: list[Post], privacy_html: str) -> dict[str, tuple[str, str, str]]:
    faq_items = [
        (
            "What is your waitlist?",
            "Availability depends on whether your child is best served in-home or in-clinic, the times of day you need, and current clinician openings. Kuska’s strongest message across the site is that they are actively welcoming new inquiries, especially for morning and daytime hours.",
        ),
        (
            "How long is a typical ABA session?",
            "Most sessions last around 3 to 3.5 hours, and some may extend to 4 hours depending on goals, tolerance, and schedule. Some learners may have two back-to-back sessions with different direct providers.",
        ),
        (
            "Is ABA only for young children?",
            "No. Kuska currently focuses heavily on early intervention, but the current site explains that ABA can support adolescents and adults too, especially with communication, independence, and coping skills.",
        ),
        (
            "What is the difference between an RBT and a BCBA?",
            "Registered Behavior Technicians provide most direct therapy sessions, while Board Certified Behavior Analysts assess, supervise, analyze progress, update plans, and provide parent training.",
        ),
        (
            "What does the initial assessment look like?",
            "The current Kuska process describes an assessment that usually takes 8 to 10 hours across direct observation, parent interview, and treatment-plan development, followed by insurance submission and ongoing re-evaluation.",
        ),
        (
            "Will my child be in ABA forever?",
            "No. Kuska describes ABA as a temporary service designed to build independence, help families feel confident, and support discharge once goals and readiness criteria are met.",
        ),
    ]
    faq_html = "".join(
        f"<details class=\"faq-item\"><summary>{q}</summary><p>{a}</p></details>" for q, a in faq_items
    )
    blog_cards = "".join(article_card(post, featured=index == 0) for index, post in enumerate(posts))

    pages: dict[str, tuple[str, str, str]] = {}

    about_body = standard_page(
        "About Kuska",
        "A name, a symbol, and a care philosophy rooted in togetherness.",
        "Kuska Autism Services is a locally owned Utah provider focused on helping children and families feel seen, supported, and equipped with real next steps.",
        dedent(
            """
            <section class="section">
              <div class="shell split-panel">
                <div>
                  <p class="eyebrow">Why the name matters</p>
                  <h2>Kuska means “together.”</h2>
                  <p>The current site shares that Kuska comes from the Quechua language and reflects how the team works shoulder to shoulder with the families they serve. That idea belongs at the center of the brand, because it tells parents immediately what kind of partner they can expect.</p>
                  <p>We’re preserving that story while making it more accessible, so families understand not only what Kuska means linguistically, but what it means practically: collaboration, trust, consistency, and compassionate care.</p>
                </div>
                <div class="feature-card feature-card--tall">
                  <h3>Family-centered by design</h3>
                  <p>Every plan is individualized. Every child is approached with warmth and dignity. Every caregiver is treated like a valuable part of the team.</p>
                </div>
              </div>
            </section>

            <section class="section section--tint">
              <div class="shell split-panel">
                <div class="feature-card feature-card--plain">
                  <p class="eyebrow">The logo story</p>
                  <h2>The two vicuñas in the mark are intentional.</h2>
                  <p>The current brand story explains that the logo features two hand-illustrated vicuñas forming a “K.” The vicuña is a sacred Andean animal with deep ties to Peru, symbolizing something rare, precious, and worth caring for with intention.</p>
                  <p>That symbolism aligns beautifully with Kuska’s work: honoring each child’s individuality while building something strong and steady around them.</p>
                </div>
                <div>
                  <img class="rounded-image" src="/wp-content/uploads/2025/05/About-2.jpg" alt="Kuska team story image" loading="lazy">
                </div>
              </div>
            </section>

            <section class="section">
              <div class="shell">
                <div class="section-heading">
                  <p class="eyebrow">Core Values</p>
                  <h2>The values already on the site are worth keeping.</h2>
                </div>
                <div class="service-grid">
                  <article class="feature-card"><h3>Kuska</h3><p>We do our best work together with families and with one another.</p></article>
                  <article class="feature-card"><h3>Quality Care</h3><p>Evidence-based, trauma-informed support tailored to each child and family.</p></article>
                  <article class="feature-card"><h3>Radical Candor</h3><p>Clear, direct communication delivered with respect and care.</p></article>
                  <article class="feature-card"><h3>Own It</h3><p>Accountability, follow-through, and a willingness to keep improving.</p></article>
                  <article class="feature-card"><h3>Play</h3><p>Children learn best when they feel engaged, motivated, and safe enough to explore.</p></article>
                </div>
              </div>
            </section>
            """
        ),
        "/wp-content/uploads/2025/05/About-1.jpeg",
    )
    pages["about"] = (
        "About",
        about_body,
        "Learn the story behind Kuska Autism Services, including the meaning of the name, the vicuña logo, and the values guiding ABA therapy and autism evaluations in Utah.",
    )

    diagnostic_body = standard_page(
        "Autism Evaluations",
        "Autism diagnosis support in Utah, with a clear and parent-friendly process.",
        "If you’re worried about communication, social development, or behavior, a professional autism evaluation can help your family understand what’s going on and what support makes sense next.",
        dedent(
            """
            <section class="section">
              <div class="shell service-grid">
                <article class="feature-card"><h3>Get answers sooner</h3><p>Families come to Kuska when they want more clarity around developmental differences and need a path forward that feels informed rather than confusing.</p></article>
                <article class="feature-card"><h3>Access support</h3><p>A diagnosis can open the door to ABA therapy, school accommodations, insurance-covered care, and more coordinated planning.</p></article>
                <article class="feature-card"><h3>Build a strong foundation</h3><p>Earlier understanding often means earlier intervention, which can support communication, regulation, and independence.</p></article>
              </div>
            </section>

            <section class="section section--tint">
              <div class="shell">
                <div class="section-heading">
                  <p class="eyebrow">What to Expect</p>
                  <h2>A four-step process that keeps families informed.</h2>
                </div>
                <div class="steps-grid">
                  <article class="step-card"><span>1</span><h3>Clinical interview</h3><p>We learn about concerns, developmental history, and day-to-day patterns.</p></article>
                  <article class="step-card"><span>2</span><h3>Observation and testing</h3><p>Professional observation helps us understand strengths, support needs, and behavior in context.</p></article>
                  <article class="step-card"><span>3</span><h3>Clear report</h3><p>Families receive a diagnosis summary and practical recommendations they can actually use.</p></article>
                  <article class="step-card"><span>4</span><h3>Connection to next steps</h3><p>If ABA therapy or other services are appropriate, we help map out what happens after the evaluation.</p></article>
                </div>
              </div>
            </section>

            <section class="cta-band">
              <div class="shell cta-band__inner">
                <div>
                  <p class="eyebrow">Need answers?</p>
                  <h2>Schedule an intake conversation about autism evaluations.</h2>
                </div>
                <div class="button-row">
                  <a class="button" href="/get-started/">Start here</a>
                  <a class="button button--secondary" href="/contact/">Ask a question</a>
                </div>
              </div>
            </section>
            """
        ),
        "/wp-content/uploads/2025/09/father-holding-little-daughter-at-the-beach-2025-04-03-02-22-04-utc.jpg",
    )
    pages["diagnostic-service"] = (
        "Autism Diagnosis in Utah",
        diagnostic_body,
        "Explore autism evaluation services in Utah with Kuska Autism Services, including what parents can expect, why diagnosis matters, and how to get started.",
    )

    program_body = standard_page(
        "ABA Programs",
        "A partner in your journey, with therapy plans that fit real family life.",
        "Kuska provides personalized ABA therapy in Utah through in-home, in-clinic, and hybrid models designed around each child’s goals, availability, and learning style.",
        dedent(
            """
            <section class="section">
              <div class="shell service-grid">
                <article class="feature-card">
                  <h3>Comprehensive ABA</h3>
                  <p>Typically 30 to 35 hours per week for children who benefit from broad, consistent support across communication, behavior, social skills, and daily living.</p>
                </article>
                <article class="feature-card">
                  <h3>Focused ABA</h3>
                  <p>Often 15 to 25 hours per week for more targeted goals, such as reducing a challenging behavior, improving a key social skill, or building independence.</p>
                </article>
                <article class="feature-card">
                  <h3>Flexible settings</h3>
                  <p>Families can choose in-home ABA therapy, clinic-based care in Bountiful or Draper, or a hybrid approach that fits their routines.</p>
                </article>
              </div>
            </section>

            <section class="section section--tint">
              <div class="shell">
                <div class="section-heading">
                  <p class="eyebrow">Areas of Growth</p>
                  <h2>Goals are personalized, but the outcomes families care about are often shared.</h2>
                </div>
                <div class="chip-cloud">
                  <span>Communication</span><span>Social development</span><span>Emotional regulation</span><span>School readiness</span><span>Daily living routines</span><span>Behavior support</span><span>Play skills</span><span>Coping skills</span><span>Independence</span>
                </div>
              </div>
            </section>

            <section class="section">
              <div class="shell split-panel">
                <div>
                  <p class="eyebrow">What makes the program feel different</p>
                  <h2>High expectations with a genuinely warm tone.</h2>
                  <p>The existing copy already communicates an important truth: Kuska is serious about evidence-based ABA, but also serious about the child behind the goals. That combination matters to parents who want progress without losing sight of play, trust, and relationship.</p>
                </div>
                <div>
                  <img class="rounded-image" src="/wp-content/uploads/2025/05/Our-Program-1.jpg" alt="ABA therapy session" loading="lazy">
                </div>
              </div>
            </section>
            """
        ),
        "/wp-content/uploads/2025/05/Our-Program-1.jpg",
    )
    pages["our-program"] = (
        "Our Program",
        program_body,
        "Learn about Kuska Autism Services ABA therapy programs in Utah, including comprehensive and focused ABA, in-home options, clinic services, and hybrid schedules.",
    )

    faq_body = standard_page(
        "FAQs",
        "Answers to the questions parents ask most often.",
        "From waitlists and assessment timelines to what ABA looks like at home, this page keeps the current site’s most helpful information while making it easier to scan.",
        f"""
        <section class="section">
          <div class="shell faq-list">{faq_html}</div>
        </section>
        <section class="cta-band">
          <div class="shell cta-band__inner">
            <div>
              <p class="eyebrow">Still unsure?</p>
              <h2>We’re happy to talk through your family’s questions.</h2>
            </div>
            <div class="button-row">
              <a class="button" href="/contact/">Contact Kuska</a>
              <a class="button button--secondary" href="/get-started/">Get started</a>
            </div>
          </div>
        </section>
        """,
        "/wp-content/uploads/2025/10/mother-and-son-drawing-with-crayons-at-home-and-cr-2025-04-01-13-04-25-utc.jpg",
    )
    pages["faqs"] = (
        "FAQs",
        faq_body,
        "Read frequently asked questions about ABA therapy, autism evaluations, session length, assessments, insurance, and parent involvement at Kuska Autism Services.",
    )

    careers_body = standard_page(
        "Careers",
        "Start with us, grow with us, and build meaningful work with children and families.",
        "Kuska’s careers messaging is already strong: this is a team that values growth, candor, accountability, and play. The refreshed page turns that message into a clearer recruitment experience.",
        dedent(
            """
            <section class="section">
              <div class="shell service-grid">
                <article class="feature-card"><h3>Mission-driven work</h3><p>Support children and families with clinically grounded care that makes daily life feel more possible.</p></article>
                <article class="feature-card"><h3>Strong team culture</h3><p>Kuska’s values emphasize collaboration, learning, psychological safety, and continuous growth.</p></article>
                <article class="feature-card"><h3>Clear path to apply</h3><p>Use the interest form below to share your information and the team will follow up with next steps.</p></article>
              </div>
            </section>
            <section class="section section--tint">
              <div class="shell">
                <div class="section-heading">
                  <p class="eyebrow">Apply</p>
                  <h2>Interested in joining Kuska?</h2>
                </div>
                <div class="embed-frame">
                  <iframe aria-label="Careers inquiry" src="https://survey.zohopublic.com/zs/AiD52g" loading="lazy"></iframe>
                </div>
              </div>
            </section>
            """
        ),
        "/wp-content/uploads/2025/05/About-1.jpeg",
    )
    pages["careers"] = (
        "Careers",
        careers_body,
        "Explore careers at Kuska Autism Services in Utah and learn about the team culture, mission, and application process for clinicians and support staff.",
    )

    contact_body = standard_page(
        "Contact Kuska",
        "Talk with a team that understands what early questions can feel like.",
        "Whether you’re looking for ABA therapy, exploring autism evaluations, or simply trying to understand your options, Kuska makes it easy to reach out.",
        dedent(
            f"""
            <section class="section">
              <div class="shell">
                {location_cards()}
              </div>
            </section>
            <section class="section section--tint">
              <div class="shell">
                <div class="section-heading">
                  <p class="eyebrow">Send a Message</p>
                  <h2>Use the contact form below and our team will follow up.</h2>
                </div>
                <div class="embed-frame">
                  <iframe aria-label="Basic Contact Form" src="https://forms.zohopublic.com/kuskaautismservices1/form/BasicContactForm/formperma/OAKPqQN6s5Ok3xjS2ZOqZj57twZLpgPaEy6DGMsHydM" loading="lazy"></iframe>
                </div>
              </div>
            </section>
            """
        ),
        "/wp-content/uploads/2025/05/Contact-1.png",
    )
    pages["contact"] = (
        "Contact",
        contact_body,
        "Contact Kuska Autism Services for ABA therapy, autism evaluations, or questions about locations, scheduling, and next steps in Bountiful and Draper, Utah.",
    )

    get_started_body = standard_page(
        "Get Started",
        "Take the first step with a quick intake form and a clear path forward.",
        "If you’re ready to ask about autism evaluations, ABA therapy availability, insurance, or scheduling, this is the easiest way to start the conversation.",
        dedent(
            """
            <section class="section">
              <div class="shell steps-grid">
                <article class="step-card"><span>1</span><h3>Tell us about your child</h3><p>Share your concerns, contact information, and what kind of support you’re looking for.</p></article>
                <article class="step-card"><span>2</span><h3>We review fit and availability</h3><p>Our team looks at service type, age, location, and scheduling needs so we can guide you well.</p></article>
                <article class="step-card"><span>3</span><h3>We connect with next steps</h3><p>From assessment to program placement, we help you understand what happens after you reach out.</p></article>
              </div>
            </section>
            <section class="section section--tint">
              <div class="shell">
                <div class="section-heading">
                  <p class="eyebrow">Intake Form</p>
                  <h2>Complete the form below to get started with Kuska.</h2>
                </div>
                <div class="embed-frame">
                  <iframe aria-label="Get Started V2" src="https://forms.zohopublic.com/kuskaautismservices1/form/GetStartedV2/formperma/_Iv6PB4abD3m0oOhsFwGAPnmL1ddTDePRsXau_XFdrI" loading="lazy"></iframe>
                </div>
              </div>
            </section>
            """
        ),
        "/wp-content/uploads/2025/11/cheerful-young-beautiful-woman-talking-on-the-phon-2024-10-19-12-34-00-utc-scaled.jpg",
    )
    pages["get-started"] = (
        "Get Started",
        get_started_body,
        "Start ABA therapy or autism evaluation services with Kuska Autism Services by submitting the intake form for Bountiful, Draper, and nearby Utah families.",
    )

    camps_body = standard_page(
        "Social Skills Camps",
        "Play-based connection opportunities designed to help children practice social interaction in a supportive setting.",
        "This page keeps Kuska’s existing camp registration route while adding helpful context for parents who want to know what social-skills-focused programming is meant to support.",
        dedent(
            """
            <section class="section">
              <div class="shell service-grid">
                <article class="feature-card"><h3>Peer interaction</h3><p>Children practice turn-taking, cooperative play, flexible thinking, and relationship-building in a more natural group setting.</p></article>
                <article class="feature-card"><h3>Confidence through practice</h3><p>Camp environments can support communication, emotional regulation, and trying new skills with adult guidance.</p></article>
                <article class="feature-card"><h3>Easy registration</h3><p>Use the current registration form below to inquire about upcoming social skills camp opportunities.</p></article>
              </div>
            </section>
            <section class="section section--tint">
              <div class="shell">
                <div class="section-heading">
                  <p class="eyebrow">Register</p>
                  <h2>Join the latest social skills camp.</h2>
                </div>
                <div class="embed-frame">
                  <iframe aria-label="Social Skills Camp registration" src="https://survey.zohopublic.com/zs/dLBnuc" loading="lazy"></iframe>
                </div>
              </div>
            </section>
            """
        ),
        "/wp-content/uploads/2025/10/adorable-multiethnic-schoolchildren-talking-and-sm-2024-11-19-04-51-28-utc-1.jpg",
    )
    pages["social-skills-camps"] = (
        "Social Skills Camps",
        camps_body,
        "Register for social skills camps from Kuska Autism Services and learn how structured group experiences can support peer interaction, communication, and confidence.",
    )

    blog_body = standard_page(
        "Kuska Blog",
        "Helpful, parent-first resources about ABA therapy, autism evaluations, insurance, and family life.",
        "We’re preserving Kuska’s article library so the site keeps its SEO equity while presenting the content in a clearer, more approachable reading experience.",
        f"""
        <section class="section">
          <div class="shell">
            <div class="post-grid">{blog_cards}</div>
          </div>
        </section>
        """,
        "/wp-content/uploads/2025/10/outdoor-family-weekend-2025-03-06-07-46-26-utc-scaled.jpg",
    )
    pages["blog"] = (
        "Blog",
        blog_body,
        "Browse Kuska Autism Services articles about ABA therapy in Utah, autism evaluation guidance, insurance coverage, parent burnout, provider selection, and family support.",
    )

    privacy_body = standard_page(
        "Privacy Policy",
        "How Kuska Autism Services handles personal information, website data, and protected health information.",
        "We’re keeping Kuska’s privacy policy available at the same route while rendering it in a cleaner, easier-to-read format.",
        f"""
        <section class="section">
          <div class="shell prose-card">
            {privacy_html}
          </div>
        </section>
        """,
        "/wp-content/uploads/2025/05/About-1.jpeg",
    )
    pages["privacy-policy"] = (
        "Privacy Policy",
        privacy_body,
        "Read the Kuska Autism Services privacy policy, including information about HIPAA, protected health information, contact data, and website privacy practices.",
    )

    return pages


def article_page(post: Post) -> tuple[str, str]:
    schema = json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": post.title,
            "datePublished": post.date_iso,
            "dateModified": post.date_iso,
            "description": post.description,
            "author": {"@type": "Organization", "name": "Kuska Autism Services"},
            "publisher": {"@type": "Organization", "name": "Kuska Autism Services", "logo": {"@type": "ImageObject", "url": f"https://kuska.co{LOGO_PATH}"}},
            "image": f"https://kuska.co{post.featured_image}",
            "mainEntityOfPage": f"https://kuska.co/{post.slug}/",
        },
        separators=(",", ":"),
    )
    body = dedent(
        f"""
        <section class="hero hero--article">
          <div class="shell hero__grid">
            <div class="hero__content">
              <p class="eyebrow">Kuska Blog</p>
              <h1>{html.escape(post.title)}</h1>
              <p class="meta-line">{post.date_display}</p>
              <p class="lead">{html.escape(post.excerpt)}</p>
            </div>
            <div class="hero__visual">
              <img class="hero-portrait" src="{post.featured_image}" alt="{html.escape(post.title)}" loading="eager">
            </div>
          </div>
        </section>

        <section class="section">
          <div class="shell article-shell">
            <article class="article-content">
              {post.body_html}
            </article>
            <aside class="article-sidebar">
              <div class="sidebar-card">
                <p class="eyebrow">Need support now?</p>
                <h2>Talk with Kuska about evaluations or ABA therapy.</h2>
                <p>Families in Utah often reach this article while they’re actively searching for answers. If that’s you, we’re here.</p>
                <a class="button" href="/get-started/">Get started</a>
              </div>
            </aside>
          </div>
        </section>
        """
    ).strip()
    return layout(
        current_slug="blog",
        title=post.title,
        description=post.description,
        canonical=f"/{post.slug}/",
        body_html=body,
        og_type="article",
        extra_schema=schema,
    ), post.slug


def build() -> None:
    post_slugs = [
        "insurance-cover-aba-therapy",
        "preparing-for-your-childs-first-aba-session-what-utah-families-need-to-know",
        "19-questions-every-utah-parent-should-ask-before-choosing-an-aba-provider",
        "choosing-the-best-aba-therapy-provider-in-bountiful-a-guide-for-utah-parents",
        "early-signs-of-autism-in-toddlers-seeking-timely-diagnosis-in-bountiful-and-draper-utah",
        "when-aba-therapy-feels-overwhelming-managing-parent-burnout-while-supporting-your-child",
        "supporting-your-whole-family-how-aba-therapy-impacts-siblings-and-what-parents-can-do",
        "understanding-the-autism-evaluation-process-in-utah-a-parents-2026-guide",
        "what-to-expect-during-your-childs-aba-assessment-a-parents-guide-to-the-evaluation-process",
        "when-aba-progress-feels-slow-understanding-your-childs-learning-journey-and-what-really-matters",
        "balancing-aba-therapy-with-family-life-managing-schedules-siblings-and-your-own-needs",
        "preparing-your-child-with-autism-for-holiday-gatherings-aba-strategies-for-family-events",
        "the-utah-parents-evidence-based-guide-to-aba-therapy",
        "in-home-vs-clinic-aba-therapy",
        "your-childs-first-aba-session-a-certified-behavior-analysts-complete-guide",
        "choosing-an-aba-provider-in-utah-10-critical-questions-from-kuska-autism-services",
        "how-aba-therapy-helps-kids-with-autism",
    ]
    posts = [extract_post(slug) for slug in post_slugs]
    privacy_html = extract_privacy_html()
    static_pages = page_bodies(posts, privacy_html)

    home_body, home_desc = home_page(posts)
    write(
        page_path("index"),
        layout(
            current_slug="index",
            title="ABA Therapy and Autism Diagnosis in Utah",
            description=home_desc,
            canonical="/",
            body_html=home_body,
        ),
    )

    for slug, (title, body, description) in static_pages.items():
        write(
            page_path(slug),
            layout(
                current_slug=slug,
                title=title,
                description=description,
                canonical=f"/{slug}/",
                body_html=body,
            ),
        )

    for post in posts:
        html_text, slug = article_page(post)
        write(page_path(slug), html_text)

    redirects = ["/home/ / 301"]
    for post in posts:
        redirects.append(f"/blog/{post.slug}/ /{post.slug}/ 301")
    write(SITE_ROOT / "_redirects", "\n".join(redirects) + "\n")

    write(page_path("home"), "<!DOCTYPE html><html><head><meta http-equiv=\"refresh\" content=\"0; url=/\"></head><body></body></html>\n")


if __name__ == "__main__":
    build()
