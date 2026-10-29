"""Export the FastAPI site as static files suitable for GitHub Pages."""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

from fastapi.testclient import TestClient

from main import app


ROOT = Path(__file__).resolve().parent
PAGES = ("", "gala", "profidence", "safeguarding", "oferta", "notice")
REDIRECTS = {
    "ideathon": "https://qyzfond.org/",
    "politika-bezopasnosti": "safeguarding/",
    "pozhertvovanija": "#donate",
    "dinner": "gala/",
    "about": "#about",
}


def normalize_base_path(value: str) -> str:
    value = value.strip()
    if not value or value == "/":
        return ""
    return "/" + value.strip("/")


def rewrite_root_urls(html: str, base_path: str) -> str:
    """Prefix root-relative HTML asset and navigation URLs."""
    if not base_path:
        return html
    return re.sub(r'(?P<prefix>(?:href|src|content)=["\'])/(?!/)', rf'\g<prefix>{base_path}/', html)


def redirect_document(target: str, base_path: str) -> str:
    if target.startswith("https://"):
        url = target
    elif target.startswith("#"):
        url = f"{base_path or '/'}{target}"
    else:
        url = f"{base_path}/{target}" if base_path else f"/{target}"
    return f"""<!doctype html>
<html lang="ru"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta http-equiv="refresh" content="0; url={url}">
<link rel="canonical" href="{url}"><title>QYZfond</title></head>
<body><p><a href="{url}">Перейти на страницу QYZfond</a></p></body></html>"""


def export(output: Path, base_path: str, site_url: str | None) -> None:
    base_path = normalize_base_path(base_path)
    if output.exists():
        shutil.rmtree(output)
    output.mkdir(parents=True)
    shutil.copytree(ROOT / "static", output / "static")
    (output / ".nojekyll").touch()

    client = TestClient(app)
    for page in PAGES:
        route = f"/{page}" if page else "/"
        response = client.get(route)
        response.raise_for_status()
        destination = output / page / "index.html" if page else output / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(rewrite_root_urls(response.text, base_path), encoding="utf-8")

    for route, target in REDIRECTS.items():
        destination = output / route / "index.html"
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(redirect_document(target, base_path), encoding="utf-8")

    # A missing demo URL shows the landing page instead of GitHub's generic 404.
    shutil.copy2(output / "index.html", output / "404.html")

    public_url = (site_url or "https://example.github.io").rstrip("/") + base_path
    sitemap = "".join(
        f"<url><loc>{public_url}/{page}</loc></url>" if page else f"<url><loc>{public_url}/</loc></url>"
        for page in PAGES
    )
    (output / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{sitemap}</urlset>",
        encoding="utf-8",
    )
    (output / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {public_url}/sitemap.xml\n", encoding="utf-8"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "dist")
    parser.add_argument("--base-path", default="", help="For example: /qyzfond_landing")
    parser.add_argument("--site-url", help="For example: https://username.github.io")
    args = parser.parse_args()
    export(args.output.resolve(), args.base_path, args.site_url)
    print(f"Static site exported to {args.output.resolve()}")

