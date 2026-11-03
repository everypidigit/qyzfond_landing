import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent
app = FastAPI(title="QYZfond", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")
CONTENT = json.loads((BASE_DIR / "static/data/site-content.json").read_text())
PARTNERS = json.loads((BASE_DIR / "static/data/legacy-partners.json").read_text())
LANGS = ("ru", "kk", "en")
PROGRAMS = {
    "kumbel-lab": {"name": "Kumbel LAB", "color": "teal", "question": "i_tech"},
    "impactum": {"name": "Impactum!", "color": "orange", "question": "i_comms"},
    "kumbel-pro": {"name": "Kumbel PRO", "color": "gold", "question": "kumbel_pro_question"},
    "mayak-pro": {"name": "Mayak PRO", "color": "purple", "question": "mayak_pro_question"},
    "orkendarium": {"name": "Örkendarium", "color": "pink", "question": "i_business"},
}
TEAM_FILES = ["maria-javier", "aigerim", "maria-asinskaya", "zhanna", "zhanel", "ulpan", "aruzhan", None, None, "olesya", "kristina", "maria-helena", "yana"]
TEAM_LINKS = ["maria-javier-brugarolas", "aigerim-kubeyeva-57307a138", "mariya-asinskaya-msc-0ba943b0", "zhanna-tsoy-10218642", "zhanel-s-73356b1b7", "ulpan-yerzhanova-309063264", "aruzhankani", None, None, "olesya-pashakulova-0359ba8a", "кристина-крылова-b21894405", "mhravera", "yanakochshuk"]
REGISTRATION = "https://docs.google.com/forms/d/162aYKKHlEVZApIIo8_PH3OX20vvvf_s_baO0P6HAy44/viewform"
HALYK = "https://homebank.kz/payments/ofKfksor-blagotvoriteljnostj"
KASPI = "https://kaspi.kz/pay/kazfondksor"
GALA_DEADLINE = "2026-11-14T00:00:00+05:00"


def language(request: Request):
    query = request.query_params.get("lang", "").lower()
    if query in ("kz", "kk"): return "kk"
    if query in LANGS: return query
    prefix = request.url.path.strip("/").split("/")[0]
    return prefix if prefix in LANGS else "ru"


def render(request: Request, template: str, **context):
    lang = language(request)
    def c(section, key): return CONTENT[section][key][lang]
    def ui(key): return c("ui", key)
    def url(path="/"):
        pathname, sep, anchor = path.partition("#")
        pathname = pathname.strip("/")
        return f"/{lang}/{pathname}{'/' if pathname else ''}{sep}{anchor}"
    route = request.url.path.strip("/").split("/")
    if route[0] in LANGS: route = route[1:]
    page_path = "/".join(route).strip("/")
    origin = getattr(app.state, "public_url", "https://qyzfond.org").rstrip("/")
    title = context.get("page_title", c("meta", "title"))
    return templates.TemplateResponse(request=request, name=template, context={
        "lang":lang, "c":c, "ui":ui, "url":url, "content":CONTENT,
        "programs":PROGRAMS, "legacy_partners":PARTNERS,
        "team":[{**p,"image":image,"linkedin":link} for p,image,link in zip(CONTENT["team"],TEAM_FILES,TEAM_LINKS) if image],
        "registration":REGISTRATION, "halyk":HALYK, "kaspi":KASPI,
        "page_path":page_path, "page_title":title,
        "public_url":origin, "canonical":f"{origin}{url('/'+page_path)}",
        "gala_deadline":GALA_DEADLINE,
        "show_gala":datetime.now(ZoneInfo("Asia/Almaty")) < datetime.fromisoformat(GALA_DEADLINE),
        **context,
    })


async def home(request: Request): return render(request, "index.html")


async def program(request: Request, slug: str):
    if slug not in PROGRAMS: return Response(status_code=404)
    return render(request, "program.html", slug=slug, program=PROGRAMS[slug], page_title=f"{PROGRAMS[slug]['name']} — QYZfond")


async def content_page(request: Request):
    page = request.url.path.strip("/").split("/")[-1]
    lang = language(request)
    section = {"safeguarding":"safety", "oferta":"ui"}.get(page,page)
    title = CONTENT["ui"]["offer"][lang] if page=="oferta" else CONTENT[section]["title"][lang]
    return render(request, "content.html", page=page, page_title=f"{title} — QYZfond")


for prefix in ("", "/ru", "/kk", "/en"):
    app.add_api_route(prefix+"/", home, methods=["GET"])
    for page in ("gala", "safeguarding", "notice", "oferta"):
        app.add_api_route(prefix+"/"+page, content_page, methods=["GET"], include_in_schema=False)
        app.add_api_route(prefix+"/"+page+"/", content_page, methods=["GET"], include_in_schema=False)
    app.add_api_route(prefix+"/programs/{slug}", program, methods=["GET"])
    app.add_api_route(prefix+"/programs/{slug}/", program, methods=["GET"], include_in_schema=False)


@app.get("/ideathon")
async def ideathon(): return RedirectResponse("/ideathon/", status_code=308)


@app.get("/profidence")
@app.get("/profidence/")
async def removed_profidence(): return Response(status_code=404)


for old, new in {"politika-bezopasnosti":"safeguarding/", "pozhertvovanija":"#support", "dinner":"gala/", "about":"#about"}.items():
    def redirect(target=new): return RedirectResponse("/ru/"+target, status_code=301)
    app.add_api_route("/"+old+"/", redirect, methods=["GET"])


@app.get("/robots.txt")
async def robots(): return Response("User-agent: *\nAllow: /\nSitemap: https://qyzfond.org/sitemap.xml\n", media_type="text/plain")


@app.get("/sitemap.xml")
async def sitemap():
    paths=["", "gala/", "safeguarding/", "notice/", "oferta/", *[f"programs/{s}/" for s in PROGRAMS]]
    urls="".join(f"<url><loc>https://qyzfond.org/{lang}/{p}</loc></url>" for lang in LANGS for p in paths)
    return Response(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>', media_type="application/xml")

