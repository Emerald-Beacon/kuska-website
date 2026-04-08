#!/usr/bin/env python3
"""
Generate a static multi-page site from a WordPress export XML file.
"""

from __future__ import annotations

import argparse
import html
import os
import re
import textwrap
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


NS = {
    "wp": "http://wordpress.org/export/1.2/",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "excerpt": "http://wordpress.org/export/1.2/excerpt/",
}


@dataclass
class Item:
    post_id: str
    title: str
    slug: str
    post_type: str
    post_date: str
    author: str
    content: str
    excerpt: str
    featured_image_id: str

    @property
    def date_display(self) -> str:
        if not self.post_date:
            return ""
        try:
            return datetime.strptime(self.post_date[:19], "%Y-%m-%d %H:%M:%S").strftime("%B %d, %Y")
        except ValueError:
            return self.post_date[:10]


def clean_content(raw_html: str) -> str:
    if not raw_html:
        return ""

    # Remove Divi/shortcode wrappers while preserving normal HTML.
    cleaned = re.sub(r"\[(\/)?et_pb[^\]]*\]", "", raw_html)
    cleaned = re.sub(r"\[(\/)?vc_[^\]]*\]", "", cleaned)
    cleaned = re.sub(r"\[(\/)?\/?[a-zA-Z0-9_]+(?:\s+[^\]]*)?\]", "", cleaned)
    cleaned = cleaned.strip()

    # Keep dangerous tags out of static output.
    cleaned = re.sub(r"<script[\s\S]*?</script>", "", cleaned, flags=re.IGNORECASE)
    return cleaned


def slug_to_path(slug: str, post_type: str) -> str:
    if post_type == "post":
        return f"blog/{slug}/index.html"
    if slug in ("", "home"):
        return "index.html"
    return f"{slug}/index.html"


def nav_pages(pages: list[Item]) -> list[tuple[str, str]]:
    wanted = [
        ("home", "Home"),
        ("about", "About"),
        ("our-program", "Our Program"),
        ("faqs", "FAQs"),
        ("careers", "Careers"),
        ("contact", "Contact"),
        ("get-started", "Get Started"),
        ("diagnostic-service", "Diagnosing"),
        ("social-skills-camps", "Social Skills Camps"),
        ("blog", "Blog"),
    ]
    available = {p.slug: p for p in pages}
    links: list[tuple[str, str]] = []
    for slug, label in wanted:
        if slug in available:
            href = "/" if slug in ("", "home") else f"/{slug}/"
            links.append((href, label))
    if "/blog/" not in [href for href, _ in links]:
        links.append(("/blog/", "Blog"))
    return links


def root_prefix(path_html: str) -> str:
    depth = path_html.count("/")
    if depth == 0:
        return "./"
    return "../" * depth


def base_template(title: str, body_html: str, nav_html: str, prefix: str, description: str = "") -> str:
    escaped_title = html.escape(title)
    escaped_description = html.escape(description or title)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{escaped_description}">
  <title>{escaped_title} | Kuska Autism Services</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}css/style.css">
</head>
<body>
  <header class="site-header">
    <div class="container header-row">
      <a href="/" class="brand-link">
        <img src="{prefix}images/kuska-autism-services-logo.png" alt="Kuska Autism Services" class="brand-logo">
      </a>
      <button class="menu-toggle" aria-label="Toggle menu">Menu</button>
      <nav class="site-nav">
        <ul>{nav_html}</ul>
      </nav>
    </div>
  </header>
  <main class="container page-content">
    {body_html}
  </main>
  <footer class="site-footer">
    <div class="container">
      <p>&copy; 2026 Kuska Autism Services. All rights reserved.</p>
    </div>
  </footer>
  <script src="{prefix}js/script.js"></script>
</body>
</html>
"""


def extract_items(xml_path: Path) -> tuple[list[Item], dict[str, str]]:
    root = ET.parse(xml_path).getroot()
    items = root.findall("./channel/item")
    records: list[Item] = []
    attachments_by_id: dict[str, str] = {}

    for it in items:
        post_type = it.findtext("wp:post_type", default="", namespaces=NS)
        status = it.findtext("wp:status", default="", namespaces=NS)
        if post_type == "attachment":
            post_id = it.findtext("wp:post_id", default="", namespaces=NS)
            attachment_url = it.findtext("wp:attachment_url", default="", namespaces=NS)
            if post_id and attachment_url:
                attachments_by_id[post_id] = attachment_url
            continue

        if status != "publish" or post_type not in {"page", "post"}:
            continue

        featured_image_id = ""
        for pm in it.findall("wp:postmeta", NS):
            key = pm.findtext("wp:meta_key", default="", namespaces=NS)
            if key == "_thumbnail_id":
                featured_image_id = pm.findtext("wp:meta_value", default="", namespaces=NS)
                break

        records.append(
            Item(
                post_id=it.findtext("wp:post_id", default="", namespaces=NS),
                title=(it.findtext("title", default="Untitled") or "Untitled").strip(),
                slug=(it.findtext("wp:post_name", default="", namespaces=NS) or "").strip(),
                post_type=post_type,
                post_date=it.findtext("wp:post_date", default="", namespaces=NS),
                author=(it.findtext("dc:creator", default="", namespaces=NS) or "").strip(),
                content=clean_content(it.findtext("content:encoded", default="", namespaces=NS) or ""),
                excerpt=(it.findtext("excerpt:encoded", default="", namespaces=NS) or "").strip(),
                featured_image_id=featured_image_id,
            )
        )
    return records, attachments_by_id


def download_file(url: str, destination: Path) -> str | None:
    try:
        destination.parent.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(url, destination)
        return destination.name
    except Exception:
        return None


def relink_images(html_content: str, site_root: Path, media_dir: Path) -> str:
    if not html_content:
        return html_content

    def repl(match: re.Match) -> str:
        original_url = html.unescape(match.group(1))
        parsed = urllib.parse.urlparse(original_url)
        filename = os.path.basename(parsed.path)
        if not filename:
            return match.group(0)
        local_path = media_dir / filename
        if not local_path.exists():
            download_file(original_url, local_path)
        return f'src="/images/wp/{filename}"'

    return re.sub(r'src="(https?://[^"]+)"', repl, html_content, flags=re.IGNORECASE)


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_site(xml_path: Path, output_root: Path) -> None:
    items, attachments_by_id = extract_items(xml_path)
    pages = [i for i in items if i.post_type == "page"]
    posts = sorted([i for i in items if i.post_type == "post"], key=lambda x: x.post_date, reverse=True)
    media_dir = output_root / "images" / "wp"

    links = nav_pages(pages)
    nav_html = "\n".join([f'<li><a href="{href}">{html.escape(label)}</a></li>' for href, label in links])

    post_card_html: list[str] = []

    for item in items:
        path_html = slug_to_path(item.slug, item.post_type)
        prefix = root_prefix(path_html)

        item_content = relink_images(item.content, output_root, media_dir)
        featured_html = ""
        if item.featured_image_id and item.featured_image_id in attachments_by_id:
            featured_url = attachments_by_id[item.featured_image_id]
            filename = os.path.basename(urllib.parse.urlparse(featured_url).path)
            if filename:
                local = media_dir / filename
                if not local.exists():
                    download_file(featured_url, local)
                featured_html = f'<img src="{prefix}images/wp/{html.escape(filename)}" alt="{html.escape(item.title)}" class="featured-image">'

        if not item_content.strip():
            fallback = html.escape(item.excerpt or "Content imported from WordPress export.")
            item_content = f"<p>{fallback}</p>"

        if item.post_type == "post":
            body = textwrap.dedent(
                f"""
                <article class="wp-entry">
                  <p class="meta">Published {html.escape(item.date_display)}{(" by " + html.escape(item.author)) if item.author else ""}</p>
                  <h1>{html.escape(item.title)}</h1>
                  {featured_html}
                  <div class="content">{item_content}</div>
                </article>
                """
            ).strip()

            excerpt = html.escape(item.excerpt or "Read this article on ABA therapy and family support.")
            post_card_html.append(
                f'<article class="post-card"><p class="meta">{html.escape(item.date_display)}</p><h2><a href="/blog/{html.escape(item.slug)}/">{html.escape(item.title)}</a></h2><p>{excerpt}</p></article>'
            )
        else:
            body = textwrap.dedent(
                f"""
                <article class="wp-entry">
                  <h1>{html.escape(item.title)}</h1>
                  {featured_html}
                  <div class="content">{item_content}</div>
                </article>
                """
            ).strip()

        page_html = base_template(
            item.title,
            body,
            nav_html,
            prefix,
            item.excerpt or f"{item.title} page for Kuska Autism Services",
        )
        write_file(output_root / path_html, page_html)
        if item.post_type == "page" and item.slug == "home":
            write_file(output_root / "home" / "index.html", page_html)

    # Build canonical blog index page from posts.
    blog_cards = "\n".join(post_card_html)
    blog_body = f"""
    <section class="blog-index">
      <h1>Blog</h1>
      <p>Articles imported from the live WordPress site with original publish dates preserved.</p>
      <div class="post-grid">
        {blog_cards}
      </div>
    </section>
    """
    blog_html = base_template(
        "Blog",
        blog_body,
        nav_html,
        "../",
        "Kuska Autism Services blog posts and resources.",
    )
    write_file(output_root / "blog" / "index.html", blog_html)


def main() -> None:
    parser = argparse.ArgumentParser(description="Migrate WordPress XML to static HTML pages.")
    parser.add_argument("--xml", required=True, help="Path to WordPress XML export")
    parser.add_argument("--output", required=True, help="Output site root directory")
    args = parser.parse_args()

    xml_path = Path(args.xml).expanduser().resolve()
    output_root = Path(args.output).expanduser().resolve()
    build_site(xml_path, output_root)
    print(f"Migration complete: {output_root}")


if __name__ == "__main__":
    main()
