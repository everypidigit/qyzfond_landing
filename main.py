import json
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
LEGACY_PARTNERS = json.loads((BASE_DIR / "static/data/legacy-partners.json").read_text())

PROGRAMS = {
    "kumbel-lab": {
        "name": "Kumbel LAB", "color": "teal", "image": "kumbel-lab.jpg",
        "tagline": "Расшифровываем таланты. Развиваем женщин.",
        "audience": "Студентки колледжей Алматы, которые начинают путь в IT.",
        "format": "9 месяцев · офлайн · русский и казахский",
        "description": "Практическая программа по мобильной разработке и современным AI-инструментам. Участницы изучают Flutter, Dart, Firebase, Figma и AI-first подход, развивают коммуникацию, тайм-менеджмент и навыки публичных выступлений.",
        "result": "Каждая участница планирует, создаёт и защищает собственное мобильное приложение.",
        "facts": ["Запущена в марте 2022 года", "Текущий поток: октябрь 2026 — июнь 2027", "Практические занятия на базе KIMEP до трёх раз в неделю"],
    },
    "impactum": {
        "name": "Impactum!", "color": "orange", "image": "impactum.jpg",
        "tagline": "Запускаем изменения. Развиваем женщин.",
        "audience": "Студентки колледжей Алматы 16–21 года, которым интересны коммуникации и управление проектами.",
        "format": "8–9 месяцев · офлайн · русский",
        "description": "Практическая программа по SMM, контенту, креативным коммуникациям, управлению проектами и социальному воздействию. Участницы работают в командах, меняются ролями и решают задачи реальных клиентов.",
        "result": "Финал программы — личный кейс и портфолио с реализованными проектами.",
        "facts": ["Запуск: октябрь 2026 года", "До 30–40 участниц", "Шесть модулей: SMM, коммуникации, управление проектами и социальное воздействие"],
    },
    "kumbel-pro": {
        "name": "Kumbel Pro", "color": "gold", "image": "kumbel-pro.jpg",
        "tagline": "Совершенствуем мастерство. Развиваем женщин.",
        "audience": "Педагоги, мастера производственного обучения и руководители организаций ТиПО Казахстана.",
        "format": "2 месяца · онлайн · 80 академических часов · русский и казахский",
        "description": "Аккредитованная программа профессионального развития об эмоциональном интеллекте, профилактике выгорания, коммуникации, командной устойчивости и преподавании с опорой на эмоциональные навыки.",
        "result": "Участники проводят практические тренинги для коллег и распространяют инструменты внутри своих организаций.",
        "facts": ["Запущена в январе 2019 года", "Аккредитованная программа — 80 академических часов", "Для системы технического и профессионального образования Казахстана"],
    },
    "orkendarium": {
        "name": "Örkendarium", "color": "pink", "image": "orkendarium.jpg", "logo": "orkendarium-logo.png",
        "tagline": "Открываем потенциал. Развиваем женщин.",
        "audience": "Женщины и мамы из Алматы и пригорода, которые развивают собственное дело.",
        "format": "Практические занятия · наставничество · сообщество",
        "description": "Образовательная программа объединяет обучение, практику и поддержку сообщества. Первый уровень «Старт с уверенностью» знакомит с основами предпринимательства, коммуникацией, цифровыми инструментами и AI. Второй — «Рост через лидерство» — посвящён управлению бизнесом, финансовому планированию, продвижению и лидерству.",
        "result": "В сезоне 2025 года поступило 246 заявок, 60 женщин завершили обучение и разработали 37 бизнес-идей; 92% участниц остались довольны программой.",
        "facts": ["Запущена в 2025 году", "Победитель Aiqyn Social Impact Awards 2025 в категории «Образование»", "Партнёры: Офис программ ОБСЕ в Астане, Social Impact Awards и Kazakhstan Growth Forum"],
    },
}


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
    return render(request, "index.html", legacy_partners=LEGACY_PARTNERS)


@app.get("/programs/{slug}")
async def program(request: Request, slug: str):
    item = PROGRAMS.get(slug)
    if not item:
        return RedirectResponse("/#projects", status_code=302)
    return render(request, "program.html", program=item)


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
    return RedirectResponse("/#support", status_code=301)


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

