"""Integration checks for translated pages, navigation and the final feedback package."""
import re
import unittest
from datetime import datetime
from unittest.mock import patch
from html.parser import HTMLParser
from pathlib import Path

from fastapi.testclient import TestClient
from main import CONTENT, LANGS, PROGRAMS, app


class Document(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class SiteTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        clock_patch = patch("main.datetime")
        self.clock = clock_patch.start()
        self.addCleanup(clock_patch.stop)
        self.clock.now.return_value = datetime.fromisoformat("2026-11-01T12:00:00+05:00")
        self.clock.fromisoformat.side_effect = datetime.fromisoformat

    def test_translations_are_rendered_without_javascript(self):
        for lang in LANGS:
            for path in ["", "gala/", "safeguarding/", "notice/", "oferta/", *[f"programs/{s}/" for s in PROGRAMS]]:
                with self.subTest(lang=lang, path=path):
                    response = self.client.get(f"/{lang}/{path}")
                    self.assertEqual(response.status_code, 200)
                    self.assertIn(f'<html lang="{lang}">', response.text)
                    self.assertIn(CONTENT["foundation"]["footer"][lang], response.text)
                    doc = Document(response.text)
                    images = [a["content"] for t, a in doc.tags if t=="meta" and a.get("property")=="og:image"]
                    self.assertTrue(images[0].startswith("https://"))
                    self.assertTrue(images[0].endswith(".jpg"))
                    internal = [a["href"] for t,a in doc.tags if t=="a" and a.get("href", "").startswith("/") and not a.get("hreflang")]
                    self.assertTrue(all(h.startswith(f"/{lang}/") or h.startswith("/static/") for h in internal))

    def test_legacy_language_links_and_kazakh_alias(self):
        for code, expected in [("en","en"),("KZ","kk"),("kk","kk"),("ru","ru"),("unknown","ru")]:
            with self.subTest(code=code):
                self.assertIn(f'<html lang="{expected}">', self.client.get(f"/?lang={code}").text)

    def test_homepage_order_and_approved_results(self):
        for lang in LANGS:
            html = self.client.get(f"/{lang}/").text
            ids = re.findall(r'<section[^>]+id="([^"]+)"', html)
            self.assertEqual(ids,["about","events","ideathon","projects","history","team","reports","partners","contacts"])
            for text in ["882","56","172",CONTENT["ideathon"]["intro"][lang]]:
                self.assertIn(text,html)
            self.assertIn(CONTENT["ui"]["report_pending"][lang],html)
            self.assertNotIn('href="mailto:info@qyzfond.org?subject=Отчёт%202026"',html)

    def test_all_ten_tracks_and_five_programs(self):
        self.assertEqual(len(CONTENT["tracks"]),10)
        self.assertEqual(len(PROGRAMS),5)
        for lang in LANGS:
            for slug in PROGRAMS:
                html = self.client.get(f"/{lang}/programs/{slug}/").text
                self.assertIn(CONTENT["programs"][slug]["description"][lang],html)
                self.assertIn(CONTENT["programs"][slug]["result"][lang],html)

    def test_documents_use_correct_language_and_no_private_presentation(self):
        for lang in LANGS:
            safety=self.client.get(f"/{lang}/safeguarding/").text
            self.assertIn(f"safeguarding-policy-{lang}.pdf",safety)
            self.assertIn(f"code-of-ethics-{lang}.pdf",safety)
            gala=self.client.get(f"/{lang}/gala/").text
            self.assertIn("162aYKKHlEVZApIIo8_PH3OX20vvvf_s_baO0P6HAy44",gala)
            self.assertIn("https://kaspi.kz/pay/kazfondksor",gala)
            self.assertIn("https://homebank.kz/payments/ofKfksor-blagotvoriteljnostj",gala)
            self.assertNotIn("gala-avanti-2026.pdf",gala)
            self.assertNotIn('href="tel:',gala)
        self.assertFalse((Path(__file__).resolve().parents[1]/"static/docs/gala-avanti-2026.pdf").exists())

    def test_profidence_page_removed_but_approach_retained(self):
        self.assertEqual(self.client.get("/profidence").status_code,404)
        self.assertNotIn("profidence",self.client.get("/sitemap.xml").text)
        self.assertIn("profidence",self.client.get("/en/").text)

    def test_gala_hides_after_the_event_in_almaty_time(self):
        self.clock.now.return_value = datetime.fromisoformat("2026-11-14T00:00:00+05:00")
        for lang in LANGS:
            html = self.client.get(f"/{lang}/").text
            self.assertNotIn('id="events"',html)
            self.assertNotIn(f'href="/{lang}/#events"',html)
            self.assertIn('id="ideathon"',html)


if __name__ == "__main__":
    unittest.main()
