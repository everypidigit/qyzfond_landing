from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="QYZfond", docs_url=None, redoc_url=None)
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

SUPPORTED_LANGS = {"ru", "kk", "en"}


def language(request: Request) -> str:
    value = request.query_params.get("lang", "ru").lower()
    return value if value in SUPPORTED_LANGS else "ru"


def render(request: Request, template: str, **context):
    return templates.TemplateResponse(
        request=request,
        name=template,
        context={"lang": language(request), **context},
    )


@app.get("/")
async def home(request: Request):
    return render(request, "index.html")


@app.get("/gala")
async def gala(request: Request):
    return render(
        request,
        "content.html",
        page="gala",
        title={"ru": "Гала-ужин QYZfond", "kk": "QYZfond гала-кешкі асы", "en": "QYZfond Gala Dinner"},
        eyebrow={"ru": "Событие", "kk": "Іс-шара", "en": "Event"},
    )


@app.get("/profidence")
async def profidence(request: Request):
    return render(
        request,
        "content.html",
        page="profidence",
        title={"ru": "Уверенность, подкреплённая опытом", "kk": "Тәжірибемен бекітілген сенім", "en": "Confidence built through experience"},
        eyebrow={"ru": "profidence", "kk": "profidence", "en": "profidence"},
    )


@app.get("/safeguarding")
async def safeguarding(request: Request):
    return render(
        request,
        "content.html",
        page="safeguarding",
        title={"ru": "Политика безопасности", "kk": "Қауіпсіздік саясаты", "en": "Safeguarding policy"},
        eyebrow={"ru": "Документы", "kk": "Құжаттар", "en": "Documents"},
    )


@app.get("/oferta")
async def oferta(request: Request):
    return render(
        request,
        "content.html",
        page="oferta",
        title={"ru": "Публичная оферта", "kk": "Жария оферта", "en": "Public offer"},
        eyebrow={"ru": "Документы", "kk": "Құжаттар", "en": "Documents"},
    )


@app.get("/notice")
async def notice(request: Request):
    return render(
        request,
        "content.html",
        page="notice",
        title={"ru": "Официальное уведомление", "kk": "Ресми хабарлама", "en": "Official notice"},
        eyebrow={"ru": "Информация", "kk": "Ақпарат", "en": "Information"},
    )


@app.get("/ideathon")
async def ideathon():
    return RedirectResponse("https://qyzfond.org/", status_code=307)


@app.get("/politika-bezopasnosti/")
async def old_safeguarding():
    return RedirectResponse("/safeguarding", status_code=301)


@app.get("/oferta/")
async def old_offer():
    return RedirectResponse("/oferta", status_code=301)


@app.get("/pozhertvovanija/")
async def old_donate():
    return RedirectResponse("/#donate", status_code=301)


@app.get("/dinner/")
async def old_dinner():
    return RedirectResponse("/gala", status_code=301)


@app.get("/about/")
async def old_about():
    return RedirectResponse("/#about", status_code=301)


@app.get("/robots.txt", response_class=Response)
async def robots():
    return Response("User-agent: *\nAllow: /\nSitemap: https://qyzfond.org/sitemap.xml\n", media_type="text/plain")


@app.get("/sitemap.xml", response_class=Response)
async def sitemap():
    paths = ["", "gala", "safeguarding", "oferta", "notice", "profidence"]
    urls = "".join(f"<url><loc>https://qyzfond.org/{path}</loc></url>" for path in paths)
    body = f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'
    return Response(body, media_type="application/xml")

