#!/usr/bin/env python3
from __future__ import annotations

import argparse
import os
import posixpath
import re
import shutil
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

import requests
from bs4 import BeautifulSoup


USER_AGENT = "Mozilla/5.0 (compatible; KuskaStaticMirror/1.0)"
ASSET_ATTRS = {
    "img": ["src", "srcset"],
    "script": ["src"],
    "link": ["href"],
    "source": ["src", "srcset"],
    "video": ["src", "poster"],
    "audio": ["src"],
    "iframe": ["src"],
}


def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def fetch_xml_urls(s: requests.Session, url: str) -> list[str]:
    resp = s.get(url, timeout=30)
    resp.raise_for_status()
    root = ET.fromstring(resp.text)
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    if root.tag.endswith("sitemapindex"):
        urls: list[str] = []
        for loc in root.findall("./sm:sitemap/sm:loc", ns):
            if loc.text:
                urls.extend(fetch_xml_urls(s, loc.text.strip()))
        return urls
    if root.tag.endswith("urlset"):
        out: list[str] = []
        for loc in root.findall("./sm:url/sm:loc", ns):
            if loc.text:
                out.append(loc.text.strip())
        return out
    return []


def local_path_for_url(base_netloc: str, output_dir: Path, url: str, is_asset: bool) -> Path | None:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc and parsed.netloc != base_netloc:
        return None

    path = parsed.path or "/"
    path = urllib.parse.unquote(path)
    path = re.sub(r"/+", "/", path)
    if path.endswith("/"):
        path = path + "index.html"
    if path == "/":
        path = "/index.html"

    ext = os.path.splitext(path)[1].lower()
    if not ext and is_asset:
        path = path + ".bin"

    return output_dir / path.lstrip("/")


def make_root_relative(url: str, base_netloc: str) -> str:
    parsed = urllib.parse.urlparse(url)
    if parsed.netloc and parsed.netloc != base_netloc:
        return url
    path = parsed.path or "/"
    query = f"?{parsed.query}" if parsed.query else ""
    fragment = f"#{parsed.fragment}" if parsed.fragment else ""
    return f"{path}{query}{fragment}"


def parse_srcset_value(srcset: str, base_netloc: str) -> str:
    parts = []
    for item in srcset.split(","):
        candidate = item.strip()
        if not candidate:
            continue
        bits = candidate.split()
        url = bits[0]
        suffix = " " + " ".join(bits[1:]) if len(bits) > 1 else ""
        parts.append(f"{make_root_relative(url, base_netloc)}{suffix}")
    return ", ".join(parts)


def download_binary(s: requests.Session, url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        return
    r = s.get(url, timeout=45)
    r.raise_for_status()
    target.write_bytes(r.content)


def mirror_site(base_url: str, output_dir: Path) -> None:
    s = session()
    parsed_base = urllib.parse.urlparse(base_url)
    base_origin = f"{parsed_base.scheme}://{parsed_base.netloc}"
    base_netloc = parsed_base.netloc

    sitemap_url = f"{base_origin}/wp-sitemap.xml"
    urls = fetch_xml_urls(s, sitemap_url)
    urls = sorted({u for u in urls if urllib.parse.urlparse(u).netloc == base_netloc})
    if not urls:
        urls = [base_origin + "/"]

    asset_queue: set[str] = set()
    seen_pages = 0

    for page_url in urls:
        try:
            resp = s.get(page_url, timeout=45)
            resp.raise_for_status()
        except Exception:
            continue
        seen_pages += 1
        soup = BeautifulSoup(resp.text, "html.parser")

        # Collect and rewrite links/assets.
        for tag_name, attrs in ASSET_ATTRS.items():
            for tag in soup.find_all(tag_name):
                for attr in attrs:
                    if not tag.has_attr(attr):
                        continue
                    val = tag[attr]
                    if attr == "srcset":
                        tag[attr] = parse_srcset_value(str(val), base_netloc)
                        for token in str(val).split(","):
                            u = token.strip().split(" ")[0]
                            abs_u = urllib.parse.urljoin(page_url, u)
                            if urllib.parse.urlparse(abs_u).netloc == base_netloc:
                                asset_queue.add(abs_u)
                    else:
                        abs_u = urllib.parse.urljoin(page_url, str(val))
                        tag[attr] = make_root_relative(abs_u, base_netloc)
                        if urllib.parse.urlparse(abs_u).netloc == base_netloc:
                            asset_queue.add(abs_u)

        for a in soup.find_all("a"):
            if not a.has_attr("href"):
                continue
            abs_u = urllib.parse.urljoin(page_url, str(a["href"]))
            a["href"] = make_root_relative(abs_u, base_netloc)

        for form in soup.find_all("form"):
            if form.has_attr("action"):
                abs_u = urllib.parse.urljoin(page_url, str(form["action"]))
                form["action"] = make_root_relative(abs_u, base_netloc)

        page_path = local_path_for_url(base_netloc, output_dir, page_url, is_asset=False)
        if not page_path:
            continue
        page_path.parent.mkdir(parents=True, exist_ok=True)
        page_path.write_text(str(soup), encoding="utf-8")

    # Download static assets referenced by pages.
    for asset_url in sorted(asset_queue):
        target = local_path_for_url(base_netloc, output_dir, asset_url, is_asset=True)
        if not target:
            continue
        try:
            download_binary(s, asset_url, target)
        except Exception:
            continue

    print(f"Mirrored {seen_pages} pages and {len(asset_queue)} assets")


def main() -> None:
    parser = argparse.ArgumentParser(description="Mirror live WordPress site to static files.")
    parser.add_argument("--url", required=True, help="Base site URL (e.g. https://kuska.co)")
    parser.add_argument("--output", required=True, help="Output directory for mirrored site")
    args = parser.parse_args()

    out = Path(args.output).expanduser().resolve()
    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True, exist_ok=True)

    mirror_site(args.url.rstrip("/"), out)


if __name__ == "__main__":
    main()
