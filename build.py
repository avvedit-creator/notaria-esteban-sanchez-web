#!/usr/bin/env python3
# Genera el sitio estático con estructura SEO (idempotente) y lo verifica.
#   python build.py                       -> producción (https://essnotario.com/)
#   DEMO=1 ORIGIN=https://x.github.io PREFIX=/repo/ python build.py   -> demo noindex
import io, json, os, re, html, datetime, glob
from PIL import Image
from content import *

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIGIN = os.environ.get("ORIGIN", "https://essnotario.com").rstrip("/")
P = os.environ.get("PREFIX", "/")
DEMO = bool(os.environ.get("DEMO"))
SITE = ORIGIN + P
TODAY = datetime.date.today().isoformat()

NAME = "Notaría Esteban Sánchez Sánchez"
TEL = "+34 914 77 67 50"; TEL_HREF = "+34914776750"
MAIL = "ess@essnotario.com"
ADDR = "C. de la Sierra Bermeja, 42, 2º C, Puente de Vallecas, 28018 Madrid"
MAPS = "https://maps.app.goo.gl/E72z9jYePPmoq8Zo6"
HOURS = "Lunes a viernes, de 9:00 a 14:30 h"
QUOTE = "El Notario es garante de la seguridad jurídica y controlador de la legalidad de los actos y contratos que autoriza."
SOCIAL = [("Facebook", "https://www.facebook.com/NotarioEstebanSanchez"), ("X", "https://x.com/essnotario"),
          ("LinkedIn", "https://www.linkedin.com/in/esteban-sánchez-sánchez-1101957a")]
LEGAL = [("Política de privacidad", "https://essnotario.com/politica-de-privacidad-politica-de-privacidad-y-proteccion-de-datos/"),
         ("Política de cookies", "https://essnotario.com/politica-de-cookies/")]
ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M2 8h11M9 3.5 13.5 8 9 12.5"/></svg>'
e = html.escape
def u(path=""): return P + path
def ab(path=""): return SITE + path

# --- Estructura -------------------------------------------------------------------
NAV = [("escrituras/", "Escrituras"), ("documentacion/", "Documentación"), ("arancel/", "Arancel"),
       ("servicios-online/", "Servicios online"), ("publicaciones/", "Publicaciones"), ("contacto/", "Contacto")]
D = {d[0]: d for d in DOCS}
FLAT_ONLINE = [x for _, items in ONLINE for x in items]
def onl(*starts): return [x for s in starts for x in FLAT_ONLINE if x[0].startswith(s)]

SERVICES = [
 dict(slug="testamentos", path="escrituras/testamentos/", name="Testamentos", h1="Testamento notarial <em>en Madrid</em>",
      title="Testamento notarial en Madrid | Esteban Sánchez",
      desc="Otorgue su testamento ante notario en Puente de Vallecas (Madrid). Documentación necesaria y trámite con el notario Esteban Sánchez Sánchez.",
      kw="testamento notarial Madrid", docs=["testamentos"], rel=["herencias", "declaracion-de-herederos", "poderes"],
      online=onl("Certificado de últimas voluntades"), img="atencion"),
 dict(slug="herencias", path="escrituras/herencias/", name="Herencias", h1="Herencias: aceptación <em>ante notario</em>",
      title="Aceptación de herencia en Madrid | Esteban Sánchez",
      desc="Escritura de manifestación y aceptación de herencia en Puente de Vallecas (Madrid): documentación a aportar, inventario y trámites con el notario.",
      kw="aceptación de herencia notario Madrid", docs=["herencias"], rel=["testamentos", "declaracion-de-herederos"],
      online=onl("Certificado de últimas voluntades", "Autoliquidación del Impuesto sobre Sucesiones", "Certificado de contratos de seguro", "Certificado de defunción"), img="despacho"),
 dict(slug="declaracion-de-herederos", path="escrituras/declaracion-de-herederos/", name="Declaración de herederos", h1="Declaración de herederos <em>abintestato</em>",
      title="Declaración de herederos en Madrid | Esteban Sánchez",
      desc="Acta de declaración de herederos abintestato en Puente de Vallecas (Madrid): certificados, libro de familia y testigos que necesita aportar.",
      kw="declaración de herederos notario Madrid", docs=["herederos"], rel=["herencias", "testamentos"],
      online=onl("Certificado de defunción", "Certificado de últimas voluntades", "Certificado de contratos de seguro", "Certificado de matrimonio", "Certificado de nacimiento"), img="techo"),
 dict(slug="compraventa-de-inmuebles", path="escrituras/compraventa-de-inmuebles/", name="Compraventas de inmuebles", h1="Compraventa de inmuebles <em>ante notario</em>",
      title="Notario para compraventa en Madrid | Esteban Sánchez",
      desc="Escritura de compraventa en Puente de Vallecas (Madrid): documentación de vendedor y comprador y trámites posteriores a la firma (impuestos e inscripción).",
      kw="notario compraventa vivienda Madrid", docs=["compraventas", "tramites-compraventa"], rel=["cancelacion-de-hipotecas", "obras-nuevas", "poderes"],
      online=onl("Autoliquidación del Impuesto de Transmisiones", "Autoliquidación del Impuesto de Plusvalía", "Consulta de datos catastrales", "Valores de referencia"), img="ciudad"),
 dict(slug="cancelacion-de-hipotecas", path="escrituras/cancelacion-de-hipotecas/", name="Cancelación de hipotecas", h1="Cancelación de hipotecas <em>en notaría</em>",
      title="Cancelación de hipoteca en Madrid | Esteban Sánchez",
      desc="Escritura de cancelación de hipoteca en Puente de Vallecas (Madrid): qué documentos aportar según el acreedor sea o no una entidad de crédito.",
      kw="cancelación de hipoteca notario Madrid", docs=["hipotecas"], rel=["compraventa-de-inmuebles"], online=[], img="techo"),
 dict(slug="poderes", path="escrituras/poderes/", name="Poderes civiles", h1="Poderes notariales <em>en Madrid</em>",
      title="Poderes notariales en Madrid | Esteban Sánchez",
      desc="Escritura de apoderamiento (poder general o especial) en Puente de Vallecas (Madrid): documentación del otorgante y del apoderado.",
      kw="poder notarial Madrid", docs=["poderes"], rel=["apostilla-de-la-haya", "compraventa-de-inmuebles", "constitucion-de-sociedades"], online=[], img="despacho"),
 dict(slug="constitucion-de-sociedades", path="escrituras/constitucion-de-sociedades/", name="Constitución de sociedades", h1="Constitución de sociedades <em>ante notario</em>",
      title="Constitución de sociedades en Madrid | Esteban Sánchez",
      desc="Constituya su sociedad ante notario en Puente de Vallecas (Madrid): certificado de denominación, desembolso, estatutos y cargos sociales.",
      kw="constitución de sociedad notario Madrid", docs=["sociedades"], rel=["compraventa-de-participaciones-sociales", "poderes"],
      online=onl("Certificación de denominación social"), img="estructura"),
 dict(slug="compraventa-de-participaciones-sociales", path="escrituras/compraventa-de-participaciones-sociales/", name="Compraventa de participaciones sociales", h1="Compraventa de participaciones <em>sociales</em>",
      title="Compraventa de participaciones sociales | Esteban Sánchez",
      desc="Escritura de compraventa de participaciones sociales en Puente de Vallecas (Madrid): documentación del vendedor y del comprador.",
      kw="compraventa participaciones sociales notario", docs=["participaciones"], rel=["constitucion-de-sociedades", "poderes"], online=[], img="estructura"),
 dict(slug="obras-nuevas", path="escrituras/obras-nuevas/", name="Obras nuevas", h1="Declaración de obras nuevas <em>ante notario</em>",
      title="Declaración de obra nueva en Madrid | Esteban Sánchez",
      desc="Escritura de declaración de obra nueva en Puente de Vallecas (Madrid): licencia, certificado técnico, libro del edificio, eficiencia energética y seguro decenal.",
      kw="declaración de obra nueva notario Madrid", docs=["obras-nuevas"], rel=["compraventa-de-inmuebles"],
      online=onl("Consulta de datos catastrales"), img="obra"),
 dict(slug="actas-de-presencia", path="escrituras/actas-de-presencia/", name="Actas de presencia", h1="Actas de presencia <em>notariales</em>",
      title="Acta de presencia notarial en Madrid | Esteban Sánchez",
      desc="Acta notarial de presencia en Puente de Vallecas (Madrid): qué necesita aportar y cómo incorporar fotografías al acta.",
      kw="acta de presencia notario Madrid", docs=["actas"], rel=["apostilla-de-la-haya", "poderes"], online=[], img="atencion"),
 dict(slug="apostilla-de-la-haya", path="apostilla-de-la-haya/", name="Apostilla de La Haya", h1="Trámite de la <em>apostilla de La Haya</em>",
      title="Apostilla de La Haya en Madrid | Esteban Sánchez",
      desc="Qué es la Apostilla de La Haya, a qué documentos se aplica, países firmantes, dónde presentarla en Madrid, plazo y precio orientativo.",
      kw="apostilla de La Haya Madrid", docs=["apostilla"], rel=["poderes", "actas-de-presencia"], online=[], img="ciudad", top=True),
]
SV = {s["slug"]: s for s in SERVICES}
ESC_LINK = {"Actas de presencia": "actas-de-presencia", "Cancelación de hipotecas": "cancelacion-de-hipotecas",
            "Compraventas de inmuebles": "compraventa-de-inmuebles", "Constitución de sociedades": "constitucion-de-sociedades",
            "Declaración de herederos": "declaracion-de-herederos", "Aceptación de la herencia": "herencias",
            "Obras nuevas": "obras-nuevas", "Poderes civiles": "poderes", "Testamentos": "testamentos"}
HOME_SERVICES = ["testamentos", "herencias", "compraventa-de-inmuebles", "poderes", "constitucion-de-sociedades", "cancelacion-de-hipotecas"]
FOOT_SERVICES = ["testamentos", "herencias", "compraventa-de-inmuebles", "poderes", "constitucion-de-sociedades", "apostilla-de-la-haya"]

def imgdim(name):
    with Image.open(os.path.join(ROOT, "assets/img", name + ".jpg")) as im: return im.size
FONTS = io.open(os.path.join(ROOT, "assets/fonts.css"), encoding="utf8").read().replace("url(fonts/", "url(" + P + "assets/fonts/")
PAGES = {}

# --- Schema (JSON-LD en @graph) ---------------------------------------------------
NOTARY_ID, WEB_ID, PERSON_ID = ab() + "#notary", ab() + "#website", ab() + "#esteban"
ADDRESS = {"@type": "PostalAddress", "streetAddress": "C. de la Sierra Bermeja, 42, 2º C", "addressLocality": "Madrid",
           "postalCode": "28018", "addressRegion": "Madrid", "addressCountry": "ES"}
def notary_node(full):
    base = {"@type": "Notary", "@id": NOTARY_ID, "name": NAME, "url": ab(), "telephone": TEL, "address": ADDRESS}
    if not full: return base
    cat = [{"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": ab(s["path"])}} for s in SERVICES]
    base.update({"image": ab("og-image.jpg"), "slogan": "Nihil prius fide", "email": MAIL, "hasMap": MAPS, "sameAs": [x for _, x in SOCIAL],
                 "description": "Notario en Madrid (Puente de Vallecas). Escrituras, testamentos, herencias, compraventas, poderes y constitución de sociedades. Más de 30 años de ejercicio.",
                 "areaServed": {"@type": "City", "name": "Madrid"}, "founder": {"@id": PERSON_ID},
                 "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "14:30"}],
                 "hasOfferCatalog": {"@type": "OfferCatalog", "name": "Escrituras y actas notariales", "itemListElement": cat}})
    return base
def graph(path, title, crumbs, kind="WebPage", service=None):
    url = ab(path)
    g = [notary_node(path == "")]
    if path == "":
        g += [{"@type": "Person", "@id": PERSON_ID, "name": "Esteban Sánchez Sánchez", "jobTitle": "Notario", "worksFor": {"@id": NOTARY_ID}, "sameAs": [x for _, x in SOCIAL]},
              {"@type": "WebSite", "@id": WEB_ID, "url": ab(), "name": NAME, "inLanguage": "es-ES", "publisher": {"@id": NOTARY_ID}}]
    wp = {"@type": kind, "@id": url + "#webpage", "url": url, "name": title, "inLanguage": "es-ES", "isPartOf": {"@id": WEB_ID},
          "about": {"@id": NOTARY_ID}}
    if path: wp["breadcrumb"] = {"@id": url + "#breadcrumb"}
    g.append(wp)
    if path:
        g.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": [
            {"@type": "ListItem", "position": i + 1, "name": n, "item": ab(p)} for i, (n, p) in enumerate(crumbs)]})
    if service:
        g.append({"@type": "Service", "@id": url + "#service", "name": service["name"], "serviceType": service["name"], "url": url,
                  "provider": {"@id": NOTARY_ID}, "areaServed": {"@type": "City", "name": "Madrid"}, "mainEntityOfPage": {"@id": url + "#webpage"}})
    return '<script type="application/ld+json">' + json.dumps({"@context": "https://schema.org", "@graph": g}, ensure_ascii=False) + '</script>'

# --- Plantilla ---------------------------------------------------------------------
def head(path, title, desc, schema_html, extra="", noindex=False):
    url = ab(path)
    robots = '<meta name="robots" content="noindex, nofollow">' if (DEMO or noindex) else '<meta name="robots" content="index, follow, max-image-preview:large">'
    canon = f'<link rel="canonical" href="{url}">' if not noindex else ""
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
{robots}
{canon}
<meta name="theme-color" content="#0B1729">
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:locale" content="es_ES">
<meta property="og:url" content="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{ab('og-image.jpg')}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="Notario en Madrid, Esteban Sánchez Sánchez">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{ab('og-image.jpg')}">
<link rel="icon" href="{u('assets/favicon.svg')}" type="image/svg+xml">
<link rel="preload" href="{u('assets/fonts/Fraunces-normal-latin.woff2')}" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{u('assets/fonts/PlusJakartaSans-normal-latin.woff2')}" as="font" type="font/woff2" crossorigin>
{extra}<style>{FONTS}</style>
<link rel="stylesheet" href="{u('assets/styles.css')}">
<script>document.documentElement.classList.add("js")</script>
{schema_html}
</head>'''

def header(cur, hero=True):
    links = "".join(f'<a href="{u(h)}"{" aria-current=\"page\"" if cur.startswith(h) else ""}>{t}</a>' for h, t in NAV)
    return f'''<body>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="site-header{' on-hero' if hero else ''}" id="hdr"><div class="wrap bar">
  <a class="brand" href="{u()}" aria-label="{NAME} — inicio"><span class="mono">ESS</span><span class="brand-t"><b>Esteban Sánchez Sánchez</b><small>Notario · Madrid</small></span></a>
  <button class="menu-btn" aria-label="Abrir menú" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  <nav class="nav" id="nav" aria-label="Principal">{links}<a class="btn" href="tel:{TEL_HREF}">Llamar</a></nav>
</div></header>'''

def footer():
    esc = "".join(f'<li><a href="{u(SV[s]["path"])}">{e(SV[s]["name"])}</a></li>' for s in FOOT_SERVICES)
    nav = "".join(f'<li><a href="{u(h)}">{t}</a></li>' for h, t in NAV)
    soc = "".join(f'<a href="{x}" rel="noopener" target="_blank">{n}</a>' for n, x in SOCIAL)
    leg = "".join(f'<a href="{x}" rel="noopener">{t}</a>' for t, x in LEGAL)
    return f'''<footer class="site-footer"><div class="wrap">
  <div class="foot">
    <div><a class="brand" href="{u()}"><span class="mono">ESS</span><span class="brand-t"><b>Esteban Sánchez Sánchez</b><small>Notario · Madrid</small></span></a><p class="foot-motto">Nihil prius fide.</p></div>
    <div><h4>Escrituras</h4><ul>{esc}<li><a href="{u('escrituras/')}">Todas las escrituras</a></li></ul></div>
    <div><h4>Navegación</h4><ul>{nav}</ul></div>
    <div><h4>Contacto</h4><ul><li><a href="tel:{TEL_HREF}">{TEL}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li>{e(ADDR)}</li><li>{HOURS}</li></ul><p class="soc">{soc}</p></div>
  </div>
  <div class="legal"><span>© 2026 {NAME}</span><span class="legal-l">{leg}</span></div>
</div></footer>
<script src="{u('assets/main.js')}" defer></script>
</body></html>'''

def cta_final():
    return f'''<section class="dark cta-final"><video class="bgvid" data-src="{u('assets/video/apreton.mp4')}" poster="{u('assets/video/apreton.jpg')}" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video><div class="wrap">
  <p class="label rule rv">Contacto</p>
  <p class="h-like rv">Resolvamos su trámite de manera <em>ágil y eficiente.</em></p>
  <a class="tel rv" href="tel:{TEL_HREF}">{TEL}</a>
  <div class="row rv"><a class="btn btn-solid" href="{u('contacto/')}">Escribir a la notaría {ARROW}</a><a class="btn btn-ghost" href="mailto:{MAIL}">{MAIL}</a></div>
</div></section>'''

def crumbs_html(crumbs):
    items = "".join(f'<li><a href="{u(p)}">{e(n)}</a></li>' for n, p in crumbs[:-1]) + f'<li aria-current="page">{e(crumbs[-1][0])}</li>'
    return f'<nav class="crumbs" aria-label="Migas de pan"><ol>{items}</ol></nav>'

def page_hero(crumbs, label, h1, lead, img):
    w, h = imgdim(img)
    return f'''<header class="page-hero"><img src="{u('assets/img/' + img + '.jpg')}" alt="" width="{w}" height="{h}" fetchpriority="high"><div class="wrap">
  {crumbs_html(crumbs)}<p class="label rule">{label}</p><h1>{h1}</h1><p class="lead">{lead}</p></div></header>'''

def write(path, s):
    full = os.path.join(ROOT, path); os.makedirs(os.path.dirname(full) or ROOT, exist_ok=True)
    io.open(full, "w", encoding="utf-8", newline="\n").write(s)

def emit(path, title, desc, crumbs, body, kind="WebPage", service=None, hero=True, extra=""):
    PAGES[path] = dict(title=title, desc=desc, kw=(service or {}).get("kw", ""))
    write(path + "index.html", head(path, title, desc, graph(path, title, crumbs, kind, service), extra) + header(path, hero) + body + footer())

# --- Piezas de contenido -----------------------------------------------------------
def render_block(b):
    k = b[0]
    if k == "h": return f"<h3>{e(b[1])}</h3>"
    if k == "p": return f"<p>{e(b[1])}</p>"
    if k == "note": return f'<p class="note">{e(b[1])}</p>'
    if k == "countries": return f'<h3>Países firmantes del Convenio</h3><p class="countries">{e(b[1])}</p>'
    if k == "ul": return "<ul>" + "".join(f"<li>{e(x)}</li>" for x in b[1]) + "</ul>"
    return ""

def service_page(s):
    top = s.get("top")
    crumbs = [("Inicio", "")] + ([] if top else [("Escrituras", "escrituras/")]) + [(s["name"], s["path"])]
    first = D[s["docs"][0]]
    lead = f'{first[2]} Notaría de Esteban Sánchez Sánchez, en Puente de Vallecas (Madrid).'
    arts, toc = "", []
    for i, did in enumerate(s["docs"]):
        _, t, sub, blocks = D[did]
        aid = "documentacion" if i == 0 else did
        h2 = "Documentación a aportar" if i == 0 else t
        if s["slug"] == "apostilla-de-la-haya": h2 = "Qué es y cómo se tramita"
        toc.append((aid, h2))
        arts += f'<article class="doc-block rv" id="{aid}"><h2>{e(h2)}</h2>' + "".join(render_block(b) for b in blocks) + "</article>"
    if s["online"]:
        toc.append(("online", "Trámites en línea relacionados"))
        arts += '<article class="doc-block rv" id="online"><h2>Trámites en línea relacionados</h2><ul class="ext">' + "".join(
            f'<li><a href="{x}" target="_blank" rel="noopener"><span class="t">{e(t)}</span><span class="o">{e(o)}</span></a></li>' for t, o, x in s["online"]) + "</ul></article>"
    if s["rel"]:
        toc.append(("relacionadas", "Escrituras relacionadas"))
        arts += '<article class="doc-block rv" id="relacionadas"><h2>Escrituras relacionadas</h2><ul class="index">' + "".join(
            f'<li><a href="{u(SV[r]["path"])}"><span class="name">{e(SV[r]["name"])}</span><span class="go">Ver</span></a></li>' for r in s["rel"]) + "</ul></article>"
    tochtml = "".join(f'<a href="#{a}">{e(t)}</a>' for a, t in toc)
    body = page_hero(crumbs, "Apostilla" if top else "Escrituras", s["h1"], lead, s["img"])
    body += f'<main id="main"><section><div class="wrap doc-layout"><nav class="toc" aria-label="En esta página">{tochtml}</nav><div>{arts}</div></div></section>{cta_final()}</main>'
    emit(s["path"], s["title"], s["desc"], crumbs, body, service=s)

def home():
    lis = "".join(f'<li><a href="{u(SV[k]["path"])}"><span class="name">{e(SV[k]["name"])}</span><span class="go">Ver</span></a></li>' for k in HOME_SERVICES)
    dcards = "".join(f'<li><a href="{u(SV[k]["path"])}#documentacion"><span class="name">{e(SV[k]["name"])}</span><span class="go">Qué aportar</span></a></li>' for k in ["compraventa-de-inmuebles", "herencias", "testamentos", "constitucion-de-sociedades", "cancelacion-de-hipotecas", "apostilla-de-la-haya"])
    title = "Notario en Madrid, Puente de Vallecas | Esteban Sánchez"
    desc = "Notaría en Puente de Vallecas, Madrid. Escrituras, testamentos, herencias, compraventas, poderes y sociedades, con atención personal y más de 30 años de ejercicio."
    body = f'''
<main id="main">
<section class="hero" style="padding:0">
 <video class="bgvid d" data-src="{u('assets/video/documento.mp4')}" poster="{u('assets/video/documento.jpg')}" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video>
 <video class="bgvid m" data-src="{u('assets/video/trato-movil.mp4')}" poster="{u('assets/video/trato-movil.jpg')}" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video>
 <div class="wrap">
  <p class="label rule">Nihil prius fide</p>
  <h1>Notario en Madrid, <em>Esteban Sánchez Sánchez</em></h1>
  <p class="lead">{QUOTE}</p>
  <div class="cta"><a class="btn btn-solid" href="tel:{TEL_HREF}">Llamar {TEL} {ARROW}</a><a class="btn btn-ghost" href="{u('contacto/')}">Escribir a la notaría</a></div>
  <div class="facts"><div><b>+30 años</b><span>De ejercicio profesional</span></div><div><b>9:00 – 14:30</b><span>Lunes a viernes</span></div><div><b>Puente de Vallecas</b><span>Sierra Bermeja, 42 · Madrid</span></div></div>
 </div>
</section>

<section><div class="wrap two">
  <div><h2 class="label rule rv">Notaría en Madrid</h2></div>
  <div><p class="statement rv">Atención <em>personal y profesional,</em> centrada en la seguridad jurídica preventiva.</p>
  <p class="lead rv" style="margin-top:32px">Nuestro compromiso con los clientes es resolver de manera ágil y eficiente cualquier tipo de trámite notarial. Más de 30 años de ejercicio, con seriedad y profesionalidad, nos avalan.</p></div>
</div></section>

<section class="white" style="padding-top:0"><div class="wrap">
  <div class="principles rv">
    <article><p class="label">Derecho del cliente</p><h3>Libre <em>elección</em></h3><p>Usted elige notario, con independencia de quién asuma los gastos.</p></article>
    <article><p class="label">Deber del notario</p><h3>Asesoramiento <em>gratuito</em></h3><p>El notario asesora, de forma obligatoria, sobre los medios jurídicos adecuados para lograr los fines que usted persigue.</p></article>
  </div>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><div><p class="label rule rv">Escrituras y actas</p><h2 class="rv">Lo que <em>autorizamos</em> en la notaría</h2></div>
  <p class="rv">Actas y escrituras públicas notariales: {len(ESCRITURAS)} servicios, de los testamentos a la constitución de sociedades.</p></div>
  <ul class="index rv">{lis}</ul>
  <p style="margin-top:36px" class="rv"><a class="link" href="{u('escrituras/')}">Ver las {len(ESCRITURAS)} escrituras y actas notariales</a></p>
</div></section>

<section class="band"><video class="bgvid" data-src="{u('assets/video/acuerdo.mp4')}" poster="{u('assets/video/acuerdo.jpg')}" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video><div class="wrap">
  <p class="label rule">Seguridad jurídica</p>
  <blockquote>«El notario es garante de la <em>seguridad jurídica</em> y controlador de la legalidad.»</blockquote>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><div><p class="label rule rv">Documentación y trámites</p><h2 class="rv">Sepa qué <em>aportar</em> antes de firmar</h2></div>
  <p class="rv">Para cada escritura, la lista de documentos que hay que traer y los trámites que siguen a la firma.</p></div>
  <ul class="index rv">{dcards}</ul>
  <p style="margin-top:36px" class="rv"><a class="link" href="{u('documentacion/')}">Toda la documentación a aportar</a></p>
</div></section>

<section class="dark"><div class="wrap">
  <p class="label rule rv">Compromiso</p>
  <h2 class="rv" style="font-size:clamp(34px,4.8vw,68px);margin-top:18px;max-width:18ch">Máxima profesionalidad, implicación y <em>confidencialidad</em></h2>
  <ul class="commit rv"><li>Soluciones eficaces</li><li>Resolución de dudas</li><li>Optimización de compraventas</li><li>Asesoramiento</li><li>Confidencialidad absoluta</li><li>Información detallada y trato personalizado</li></ul>
</div></section>

<section class="paper2"><div class="wrap contact-grid">
  <div><p class="label rule rv">Cómo llegar</p><h2 class="rv" style="font-size:clamp(34px,4.4vw,60px);margin-top:18px">Notaría en <em>Puente de Vallecas</em></h2></div>
  <div class="data rv"><dl>
    <div><dt>Dirección</dt><dd>{e(ADDR)}<br><a href="{MAPS}" target="_blank" rel="noopener">Abrir en Google Maps</a></dd></div>
    <div><dt>Horario</dt><dd>{HOURS}</dd></div>
    <div><dt>Teléfono</dt><dd><a href="tel:{TEL_HREF}">{TEL}</a> · <a href="tel:914776750">914 776 750</a></dd></div>
    <div><dt>Correo</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
  </dl></div>
</div></section>
{cta_final()}
</main>'''
    pre = (f'<link rel="preload" as="image" href="{u("assets/video/documento.jpg")}" media="(min-width:701px)" fetchpriority="high">\n'
           f'<link rel="preload" as="image" href="{u("assets/video/trato-movil.jpg")}" media="(max-width:700px)" fetchpriority="high">\n')
    emit("", title, desc, [], body, extra=pre)

def escrituras():
    crumbs = [("Inicio", ""), ("Escrituras", "escrituras/")]
    lis = ""
    for n, _ in ESCRITURAS:
        k = ESC_LINK.get(n)
        lis += (f'<li><a href="{u(SV[k]["path"])}"><span class="name">{e(n)}</span><span class="go">Ver documentación</span></a></li>' if k
                else f'<li><div class="row"><span class="name">{e(n)}</span><span></span></div></li>')
    otros = "".join(f'<li><a href="{u(SV[k]["path"])}"><span class="name">{e(SV[k]["name"])}</span><span class="go">Ver</span></a></li>' for k in ["compraventa-de-participaciones-sociales", "apostilla-de-la-haya"])
    body = page_hero(crumbs, "Escrituras", "Actas y escrituras <em>públicas notariales</em>", QUOTE, "despacho")
    body += f'<main id="main"><section><div class="wrap"><h2 class="group-title">Las {len(ESCRITURAS)} escrituras y actas de la notaría</h2><ul class="index cols-2 rv">{lis}</ul><h2 class="group-title" style="margin-top:72px">Otros trámites</h2><ul class="index rv">{otros}</ul></div></section>{cta_final()}</main>'
    emit("escrituras/", "Escrituras y actas notariales en Madrid | Esteban Sánchez",
         "Actas y escrituras públicas en Puente de Vallecas (Madrid): compraventas, testamentos, herencias, poderes, sociedades, hipotecas, capitulaciones y más.",
         crumbs, body, kind="CollectionPage")

def documentacion():
    crumbs = [("Inicio", ""), ("Documentación", "documentacion/")]
    where = {}
    for s in SERVICES:
        for i, did in enumerate(s["docs"]): where[did] = (s, "documentacion" if i == 0 else did)
    lis = ""
    for did, t, sub, _ in DOCS:
        s, a = where[did]
        lis += f'<li><a href="{u(s["path"])}#{a}"><span class="name">{e(t)}</span><span class="go">Qué aportar</span></a></li>'
    body = page_hero(crumbs, "Documentación", "Documentación <em>a aportar</em> y trámites", "Para cada escritura, lo que necesitamos de usted y los trámites que siguen a la firma.", "estructura")
    body += f'<main id="main"><section><div class="wrap"><h2 class="group-title">Elija el trámite</h2><ul class="index rv">{lis}</ul></div></section>{cta_final()}</main>'
    emit("documentacion/", "Documentación a aportar y trámites | Esteban Sánchez",
         "Qué documentos llevar a la notaría para compraventas, herencias, testamentos, poderes, sociedades, hipotecas, obras nuevas y apostilla. Madrid.",
         crumbs, body, kind="CollectionPage")

def online():
    crumbs = [("Inicio", ""), ("Servicios online", "servicios-online/")]
    groups = ""
    for g, items in ONLINE:
        groups += f'<h2 class="group-title">{e(g)}</h2><ul class="ext">' + "".join(
            f'<li><a href="{x}" target="_blank" rel="noopener"><span class="t">{e(t)}</span><span class="o">{e(o)}</span></a></li>' for t, o, x in items) + "</ul>"
    body = page_hero(crumbs, "Servicios online", "Trámites y certificados <em>en línea</em>", "Enlaces directos a las sedes oficiales para los trámites más habituales.", "atencion")
    body += f'<main id="main"><section><div class="wrap rv">{groups}</div></section>{cta_final()}</main>'
    emit("servicios-online/", "Servicios online: trámites y certificados | Esteban Sánchez",
         "Autoliquidación de impuestos, certificados de últimas voluntades, defunción, matrimonio y nacimiento, datos catastrales y registros: enlaces directos.",
         crumbs, body, kind="CollectionPage")

def arancel():
    crumbs = [("Inicio", ""), ("Arancel", "arancel/")]
    lis = "".join(f'<li><a href="https://essnotario.com/{x}" target="_blank" rel="noopener"><span><span class="t">{e(t)}</span><span class="s">{e(d)}</span></span><span class="o">Ampliar información</span></a></li>' for t, d, x in ARANCEL)
    body = page_hero(crumbs, "Arancel", "Normas <em>arancelarias</em>", "La normativa que regula los derechos de los notarios.", "techo")
    body += f'''<main id="main"><section><div class="wrap"><h2 class="group-title">Normativa aplicable</h2><ul class="ext rv">{lis}</ul>
<p class="lead rv" style="margin-top:48px">¿Necesita conocer el coste de una escritura? Llámenos al <a class="link" href="tel:{TEL_HREF}">{TEL}</a>.</p></div></section>{cta_final()}</main>'''
    emit("arancel/", "Arancel notarial: normas y aranceles | Esteban Sánchez",
         "Normativa que regula el arancel de los notarios: Real Decreto 1426/1989, Real Decreto 1612/2011, Ley 41/2007 y otras disposiciones.", crumbs, body, kind="CollectionPage")

def publicaciones():
    crumbs = [("Inicio", ""), ("Publicaciones", "publicaciones/")]
    posts = "".join(f'<li><a href="https://essnotario.com/{x}" target="_blank" rel="noopener"><time>{d}</time><span><span class="t">{e(t)}</span><span class="e">{e(z)}</span></span><span class="go" aria-hidden="true">↗</span></a></li>' for d, t, z, x in BLOG)
    misc = "".join(f'<li><div class="row"><span class="name">{e(t)}</span><span></span></div></li>' for t in MISC)
    body = page_hero(crumbs, "Publicaciones", "Blog y <em>miscelánea</em> jurídica", "Artículos y estudios sobre Derecho privado, contratación y práctica notarial.", "estructura")
    body += f'<main id="main"><section><div class="wrap"><h2 class="group-title">Blog</h2><ul class="posts rv">{posts}</ul><h2 class="group-title" style="margin-top:88px">Miscelánea</h2><ul class="index cols-2 rv">{misc}</ul></div></section>{cta_final()}</main>'
    emit("publicaciones/", "Blog y publicaciones jurídicas | Esteban Sánchez",
         "Artículos del notario Esteban Sánchez: pactos prematrimoniales, libertad de testar, AJD, cláusula suelo, firma digital, contratos bancarios y más.", crumbs, body, kind="CollectionPage")

def contacto():
    crumbs = [("Inicio", ""), ("Contacto", "contacto/")]
    body = page_hero(crumbs, "Contacto", "Localización y <em>contacto</em>", "Llámenos o escríbanos. Le atenderemos de forma personal.", "ciudad")
    body += f'''<main id="main"><section><div class="wrap contact-grid">
  <div class="data rv"><h2 class="group-title">Notaría en Puente de Vallecas, Madrid</h2><dl>
    <div><dt>Dirección</dt><dd>{e(ADDR)}<br><a href="{MAPS}" target="_blank" rel="noopener">Abrir en Google Maps</a></dd></div>
    <div><dt>Horario</dt><dd>{HOURS}</dd></div>
    <div><dt>Teléfono</dt><dd><a href="tel:{TEL_HREF}">{TEL}</a><br><a href="tel:914776750">914 776 750</a></dd></div>
    <div><dt>Correo</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
  </dl></div>
  <form class="card rv" id="f" action="mailto:{MAIL}" method="post" enctype="text/plain">
    <h2 class="group-title" style="margin:0 0 24px">Escríbanos</h2>
    <div class="field"><label for="n">Su nombre <i>*</i></label><input id="n" name="nombre" required autocomplete="name"></div>
    <div class="field"><label for="m">Su correo <i>*</i></label><input id="m" name="correo" type="email" required autocomplete="email"></div>
    <div class="field"><label for="a">Asunto</label><input id="a" name="asunto"></div>
    <div class="field"><label for="x">Su mensaje</label><textarea id="x" name="mensaje"></textarea></div>
    <button class="btn btn-dark" type="submit">Enviar mensaje {ARROW}</button>
    <p class="form-note">Se abrirá su programa de correo con el mensaje preparado. No incluya datos sensibles; para asuntos urgentes, llámenos.</p>
  </form>
</div></section></main>'''
    emit("contacto/", "Contacto y localización | Notaría Esteban Sánchez",
         "Notaría en C. de la Sierra Bermeja, 42, 2º C, Puente de Vallecas, Madrid. Tel. 914 77 67 50. Lunes a viernes de 9:00 a 14:30.", crumbs, body, kind="ContactPage")

def not_found():
    body = f'''<main id="main"><section class="dark" style="padding:200px 0 120px"><div class="wrap"><p class="label rule">Error 404</p><h1 style="color:#fff;font-size:clamp(40px,6vw,80px);margin:22px 0">Esta página <em>no existe</em></h1>
<p class="lead">Puede que el enlace haya cambiado. Estos son los accesos principales:</p><div class="cta-final"><div class="row"><a class="btn btn-solid" href="{u()}">Ir al inicio</a><a class="btn btn-ghost" href="{u('escrituras/')}">Escrituras</a><a class="btn btn-ghost" href="{u('contacto/')}">Contacto</a></div></div></div></section></main>'''
    write("404.html", head("404", "Página no encontrada | Notaría Esteban Sánchez", "Página no encontrada.", "", noindex=True) + header("404", False) + body + footer())

def extras():
    NL = chr(10)
    write("robots.txt", ("User-agent: *" + NL + "Disallow: /" + NL) if DEMO else ("User-agent: *" + NL + "Allow: /" + NL + NL + "Sitemap: " + ab("sitemap.xml") + NL))
    urls = "".join(f"  <url><loc>{ab(p)}</loc><lastmod>{TODAY}</lastmod></url>\n" for p in PAGES)
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + urls + "</urlset>\n")
    write("assets/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#0B1729"/><rect x="6" y="6" width="52" height="52" fill="none" stroke="#D2AE68" stroke-width="2"/><text x="32" y="40" font-family="Georgia,serif" font-size="22" font-weight="700" fill="#D2AE68" text-anchor="middle" letter-spacing="1">ESS</text></svg>')

# --- Ejecución ------------------------------------------------------------------------
for old in glob.glob(os.path.join(ROOT, "*.html")): os.remove(old)   # estructura plana anterior
home(); escrituras(); documentacion(); online(); arancel(); publicaciones(); contacto()
for s in SERVICES: service_page(s)
not_found(); extras()

# --- Verificación SEO ----------------------------------------------------------------
def verify():
    bad, inbound = [], {p: 0 for p in PAGES}
    for p, m in PAGES.items():
        t, d = m["title"], m["desc"]
        if len(t) > 60: bad.append(f"TITLE largo ({len(t)}): {p or '/'} · {t}")
        if not 110 <= len(d) <= 165: bad.append(f"DESC {len(d)} car.: {p or '/'}")
        h = io.open(os.path.join(ROOT, p + "index.html"), encoding="utf8").read()
        if len(re.findall(r"<h1[ >]", h)) != 1: bad.append(f"H1 != 1: {p or '/'}")
        if f'rel="canonical" href="{ab(p)}"' not in h: bad.append(f"canonical: {p}")
        if "@graph" not in h: bad.append(f"schema: {p}")
        for a in re.findall(r'<a [^>]*href="([^"]+)"', h):
            if not a.startswith(P) or a.startswith(P + "assets/"): continue
            tgt = a[len(P):].split("#")[0]
            if tgt in PAGES:
                if tgt != p: inbound[tgt] += 1
            elif tgt != "404.html": bad.append(f"enlace roto en {p or '/'}: {a}")
    for p, n in inbound.items():
        if n == 0: bad.append(f"HUÉRFANA: {p}")
    return bad, inbound
bad, inbound = verify()
print("páginas:", len(PAGES), "| problemas:", len(bad))
for b in bad: print(" -", b)
print("enlaces internos entrantes:", {(p or "/"): n for p, n in sorted(inbound.items(), key=lambda x: -x[1])})
print("títulos:", {(p or "/"): len(m["title"]) for p, m in PAGES.items()})
