# QYZfond landing

FastAPI implementation of the QYZfond public website concept.

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000.

## GitHub Pages demo

This repository includes a static exporter and an automatic GitHub Pages workflow.
FastAPI remains the production application; GitHub Pages receives only rendered HTML,
CSS, JavaScript and images.

### Publish for the first time

1. Create an empty GitHub repository, preferably named `qyzfond_landing`.
2. In this folder, run the commands below, replacing `YOUR_USERNAME`:

```bash
git init
git add .
git commit -m "Initial QYZfond website"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/qyzfond_landing.git
git push -u origin main
```

3. On GitHub, open **Settings → Pages** and set **Source** to **GitHub Actions**.
4. Open the **Actions** tab. The “Deploy static demo to GitHub Pages” workflow will
   publish the site. The URL will be:

```text
https://YOUR_USERNAME.github.io/qyzfond_landing/
```

Every later push to `main` updates the demo automatically.

### Test the static export locally

```bash
python export_static.py
python -m http.server 8001 --directory dist
```

Then open http://127.0.0.1:8001. The `dist/` directory is generated and should not
be committed.

## Languages and approved content

The site renders complete Russian (`/ru/`), Kazakh (`/kk/`) and English (`/en/`) pages.
Use these URLs when sharing links: their social previews are localized without JavaScript.
Old `?lang=en`, `?lang=kk` and `?lang=kz` entry links are also supported.
The static exporter includes every language, internal page and localized legal document.

Approved content from the final feedback document is in `static/data/site-content.json`.
The implementation checklist and remaining foundation-supplied assets are in
[FEEDBACK_CHECKLIST.md](FEEDBACK_CHECKLIST.md).

Run the integration checks with `python -m unittest discover -s tests -v`.

The homepage gala block hides automatically after 13 November 2026 (Almaty time).
Before moving this site to qyzfond.org, give the existing Ideathon website a separate
URL and update the event button and redirect to prevent a link back to this homepage.
