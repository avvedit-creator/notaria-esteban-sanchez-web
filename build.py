#!/usr/bin/env python3
# Genera el sitio estático (idempotente). Todo el texto sale de essnotario.com;
# lo único escrito de cero es microcopy de interfaz (etiquetas, botones).
import io, json, os, html
ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.environ.get("BASE", "https://essnotario.com/")
DEMO = bool(os.environ.get("DEMO"))  # demo de prospección: no indexable
NAME = "Notaría Esteban Sánchez Sánchez"
TEL = "+34 914 77 67 50"; TEL_HREF = "+34914776750"
MAIL = "ess@essnotario.com"
ADDR = "C. de la Sierra Bermeja, 42, 2º C, Puente de Vallecas, 28018 Madrid"
MAPS = "https://maps.app.goo.gl/E72z9jYePPmoq8Zo6"
HOURS = "Lunes a viernes, de 9:00 a 14:30 h"
QUOTE = "El Notario es garante de la seguridad jurídica y controlador de la legalidad de los actos y contratos que autoriza."
SOCIAL = [("Facebook", "https://www.facebook.com/NotarioEstebanSanchez"),
          ("X", "https://x.com/essnotario"),
          ("LinkedIn", "https://www.linkedin.com/in/esteban-sánchez-sánchez-1101957a")]
LEGAL = [("Política de privacidad", "https://essnotario.com/politica-de-privacidad-politica-de-privacidad-y-proteccion-de-datos/"),
         ("Política de cookies", "https://essnotario.com/politica-de-cookies/")]

ARROW = '<svg viewBox="0 0 16 16" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M2 8h11M9 3.5 13.5 8 9 12.5"/></svg>'
e = html.escape

NAV = [("escrituras.html", "Escrituras"), ("documentacion.html", "Documentación"), ("arancel.html", "Arancel"),
       ("servicios-online.html", "Servicios online"), ("publicaciones.html", "Publicaciones"), ("contacto.html", "Contacto")]

# --- Contenido -------------------------------------------------------------
ESCRITURAS = [  # (nombre, ancla en documentacion.html o None)
    ("Actas de presencia", "actas"), ("Cancelación de hipotecas", "hipotecas"), ("Capitulaciones matrimoniales", None),
    ("Compraventas de inmuebles", "compraventas"), ("Conciliación extrajudicial", None), ("Consignaciones", None),
    ("Constitución de sociedades", "sociedades"), ("Contador partidor dativo", None), ("Declaración de herederos", "herederos"),
    ("Desafectación de portería", None), ("Documento fehaciente de liquidación", None), ("Interpelación al heredero", None),
    ("Aceptación de la herencia", "herencias"), ("Matrimonios", None), ("Modificaciones estatutarias", None),
    ("Monitorio notarial", None), ("Notificaciones", None), ("Obras antiguas", None), ("Obras nuevas", "obras-nuevas"),
    ("Poderes civiles", "poderes"), ("Préstamos", None), ("Recuperación del IVA", None), ("Testamentos", "testamentos"),
    ("Testimonios", None)]

def L(*items): return ("ul", list(items))
DOCS = [
 ("actas", "Actas notariales", "Documentación para la preparación de un acta de presencia.", [
   L("D.N.I. del requirente.", "Descripción del objeto, que ha de ser lícito y concreto."),
   ("p", "En muchas ocasiones puede ser de utilidad el requerimiento al notario para que tome fotografías en el lugar, las cuales serán incorporadas como documentación unida al acta.")]),
 ("hipotecas", "Cancelación de hipotecas", "Documentación necesaria para la preparación de la escritura de cancelación de hipoteca.", [
   ("h", "Si el acreedor no es una entidad de crédito"), L("Título de constitución de la hipoteca."),
   ("h", "Si el acreedor es una institución de crédito"),
   L("Certificado de cancelación económica, si firman apoderados de otra oficina.", "Datos del solicitante.", "Copia de la escritura de préstamo que se cancela o nota del Registro de la Propiedad sobre la carga."),
   ("h", "Si se constituyó en garantía de precio aplazado"),
   L("Si la otorga el vendedor: título de constitución de la carga.", "Si hay letras de cambio: todas las letras y la escritura de compraventa.")]),
 ("compraventas", "Compraventas", "Documentación para escrituras de compraventa.", [
   ("h", "Relativos al vendedor (persona física)"),
   L("D.N.I. vigente.", "Título de propiedad.", "Referencia catastral.", "Si es propiedad horizontal: certificación del administrador, con el visto bueno del presidente, sobre la situación de gastos de comunidad."),
   ("h", "Vendedor sociedad"), L("Los documentos anteriores, más la acreditación de la legitimación del representante."),
   ("h", "Relativos al comprador"),
   L("D.N.I. vigente de los compradores y domicilio actualizado.", "Régimen económico matrimonial, si aplica.", "Copia autorizada de poder, si actúan por representación.", "Precio de la compraventa y forma de pago.", "IVA, si es primera transmisión.", "Pactos especiales y sobre gastos.")]),
 ("tramites-compraventa", "Trámites en escrituras de compraventa", "Gestiones posteriores a la firma, para comprador y vendedor.", [
   ("h", "Parte compradora · vivienda usada"),
   L("Sujeta al Impuesto sobre Transmisiones Patrimoniales (modelo 601). Tipo en Madrid: 6 % sobre el precio de compra.", "Plazo de presentación: un mes, contado desde el día de otorgamiento de la escritura.", "Inscripción: copia autorizada de la escritura y el modelo de autoliquidación sellado, en el Registro de la Propiedad."),
   ("h", "Parte compradora · vivienda nueva"),
   L("Sujeta al IVA y al Impuesto de Actos Jurídicos Documentados (modelo 603): 1 % del valor declarado de la vivienda.", "Trámites idénticos a los de vivienda usada."),
   ("h", "Parte vendedora"),
   L("Liquidación del Impuesto sobre el Incremento del Valor de los Terrenos de Naturaleza Urbana (plusvalía): copia de la escritura y último recibo del IBI en el Ayuntamiento.", "Plazo: un mes, contado desde el día de otorgamiento de la escritura.")]),
 ("sociedades", "Sociedades", "Documentación necesaria para la constitución de sociedades.", [
   L("Certificado negativo de denominación del Registro Mercantil Central, expedido a instancia de alguno de los socios y vigente (validez de dos meses).",
     "Certificación bancaria del desembolso dinerario en una cuenta de la sociedad, con fecha de ingreso no superior a dos meses.",
     "Título de las aportaciones no dinerarias, si las hubiera.", "Forma de organizar la administración de la sociedad.",
     "Identidad de los socios con D.N.I. vigente y número de acciones o participaciones que cada uno suscribe o asume.",
     "Si intervienen personalmente o por medio de apoderado; en este caso, copia autorizada del documento del que resulte su legitimación.",
     "Estatutos sociales o, al menos, objeto social, domicilio y capital social.", "Personas designadas para ocupar los cargos sociales."),
   ("note", "La utilización de estatutos-tipo constriñe la posibilidad de configuración de la sociedad. Se admiten todos los pactos que no contravengan la ley ni los principios del tipo social elegido. Consulte con el notario. Para modificaciones posteriores (ampliaciones de capital, cambios administrativos, disolución), contacte directamente.")]),
 ("participaciones", "Compraventas de participaciones sociales", "Documentación para la compraventa de participaciones.", [
   ("h", "Relativos al vendedor"),
   L("Persona física: D.N.I. vigente y título de propiedad.", "Sociedad: lo anterior, más los documentos que acrediten la legitimación del representante."),
   ("h", "Relativos al comprador"),
   L("D.N.I. vigente y domicilio actualizado.", "Si es matrimonio: régimen económico matrimonial (gananciales, consorciales, separación de bienes o participación).", "Indicación de si actúan personalmente o por poder (con copia autorizada en el segundo caso).", "Precio de la compraventa y forma de pago.", "Pactos especiales sobre la compraventa y gastos.")]),
 ("herederos", "Declaración de herederos", "Documentación para la preparación del acta de declaración de herederos abintestato.", [
   L("Certificado literal de defunción. Se solicita en el Registro Civil.",
     "Certificado literal de últimas voluntades y certificado de cobertura de seguros del fallecido. Se solicitan en el Ministerio de Justicia.",
     "Libro de familia. Si no existe o se ha extraviado: certificado literal de nacimiento de hijo o hijos y certificado literal del matrimonio del fallecido.",
     "Fotocopia del D.N.I. del viudo o viuda y de los herederos.", "D.N.I. original del fallecido."),
   ("note", "El día de la firma deberán comparecer dos testigos cualesquiera que conozcan, por amistad o vecindad, al fallecido y a su familia. Se aportarán fotocopias de sus D.N.I. junto a toda la documentación.")]),
 ("herencias", "Herencias", "Documentación necesaria para la escritura de manifestación y aceptación de herencia.", [
   ("h", "Si el fallecido dejó testamento"), L("Copia autorizada del testamento.", "Certificado de defunción.", "Certificado del Registro de Actos de Última Voluntad."),
   ("h", "Si falleció sin testamento"), L("Copia autorizada del acta de declaración de herederos."),
   ("h", "En ambos casos"), L("Identidad de los herederos (D.N.I. vigentes y domicilios actualizados).", "Datos para formar el inventario y avalúo de bienes."),
   ("h", "Activo"), L("Títulos de propiedad de bienes inmuebles.", "Certificaciones o extracto de cuentas, fondos de inversión y títulos valores.", "Recibos del IBI de los inmuebles y valoración asignada."),
   ("h", "Pasivo"), L("Documentos que acrediten deudas pendientes al fallecimiento."),
   ("h", "Gastos deducibles"), L("Facturas de última enfermedad, entierro y funeral (deducibles si los pagan los herederos, no si se cargan a la herencia)."),
   ("note", "En cuanto al modo de distribución de la herencia, póngase en contacto con nosotros.")]),
 ("obras-nuevas", "Declaración de obras nuevas", "Documentación a aportar para la tramitación de obras nuevas.", [
   L("Identificación del declarante: persona física, D.N.I. en vigor; persona jurídica, las escrituras que acrediten la representación.",
     "La facultad de declarar la obra corresponde al propietario. Si el bien es ganancial, la declaración la hacen ambos cónyuges, o el titular registral si la adquisición la hizo uno de ellos para la sociedad conyugal. Si la finca pertenece a una comunidad hereditaria, otorgan la escritura todos los herederos y, en su caso, los legitimarios.",
     "Autorización administrativa.", "Certificado firmado por técnico competente, con su firma legitimada notarialmente; en otro caso, habrá de comparecer en la notaría.",
     "El libro del edificio.", "La licencia de ocupación.", "El certificado de eficiencia energética.", "La póliza acreditativa de la constitución del seguro decenal.")]),
 ("poderes", "Poderes", "Documentación necesaria para la preparación de una escritura de apoderamiento.", [
   ("h", "Poderes generales y especiales"),
   L("Identificación del otorgante por D.N.I. vigente, con comparecencia ante notario.", "Si actúa una persona jurídica: escritura de la que dimane la legitimación de su representante.", "Identidad del apoderado, sin necesidad de su comparecencia.")]),
 ("testamentos", "Testamentos", "Documentación para el otorgamiento de un testamento notarial.", [
   ("h", "Quien sabe leer y escribir"), L("D.N.I. vigente."),
   ("h", "Quien no sabe o no puede leer y escribir"),
   L("D.N.I. vigente.", "Dos testigos que conozcan al testador y que no sean familiares, dentro del cuarto grado de consanguinidad o segundo de afinidad, del testador ni de los herederos.")]),
 ("apostilla", "Trámite de la apostilla", "La Apostilla de La Haya.", [
   ("p", "A través de la denominada Apostilla de La Haya, un país firmante del Convenio reconoce la eficacia jurídica de un documento público emitido en otro país firmante. Consiste en colocar sobre el propio documento público un sello o anotación que certifica su autenticidad."),
   ("h", "Documentos a los que se aplica"),
   L("Documentos notariales: poderes, actas de manifestaciones, cartas de invitación.", "Certificaciones oficiales sobre documentos privados: certificación del registro de un documento, certificación sobre la certeza de una fecha y autenticaciones oficiales y notariales de firmas."),
   ("h", "Quién puede solicitarla"), L("Cualquier persona portadora de un documento público cuya autenticidad desee certificar."),
   ("h", "Dónde, cuándo y cuánto"),
   L("En Madrid: Colegio Notarial de Madrid, calle Ruiz de Alarcón, nº 3, 28014 Madrid. Horario de atención: de 9 a 14 horas.", "Plazo: un día si se presenta antes de las 13 horas; dos días si se presenta a partir de las 13 horas.", "Precio: aproximadamente 15,00 € por unidad.", "Verificación: eregister.justicia.es"),
   ("countries", "Alemania, Andorra, Antigua y Barbuda, Argentina, Armenia, Australia, Austria, Bahamas, Barbados, Bélgica, Belice, Bielorrusia, Bosnia y Herzegovina, Botswana, Brunei Darussalam, Bulgaria, Chipre, Colombia, Croacia, El Salvador, Eslovaquia, Eslovenia, España, Estados Unidos de América, Estonia, Federación de Rusia, Fiyi, Finlandia, Francia, Granada, Grecia, Honduras, Hungría, India, Irlanda, Islas Marshall, Isla Mauricio, Israel, Italia, Japón, Kazajistán, Lesotho, Letonia, Liberia, Liechtenstein, Lituania, Luxemburgo, Macedonia, Malawi, Malta, México, Namibia, Niue, Noruega, Nueva Zelanda, Países Bajos, Panamá, Polonia, Portugal, Reino Unido de Gran Bretaña e Irlanda del Norte, República Checa, Rumanía, San Cristóbal y Nieves, San Marino, San Vicente y las Granadinas, Santa Lucía, Serbia y Montenegro, Seychelles, Sudáfrica, Suecia, Suiza, Surinam, Swazilandia, Tonga, Trinidad y Tobago, Turquía, Ucrania y Venezuela.")]),
]

ONLINE = [
 ("Impuestos y tributación", [
  ("Autoliquidación del Impuesto de Plusvalía en Madrid", "Ayuntamiento de Madrid", "https://sede.madrid.es/portal/site/tramites/menuitem.62876cb64654a55e2dbd7003a8a409a0/?vgnextoid=6258ef82e1bed010VgnVCM1000000b205a0aRCRD&vgnextchannel=d4968173cec9c410VgnVCM100000171f5a0aRCRD&vgnextfmt=default"),
  ("Autoliquidación del Impuesto de Transmisiones Patrimoniales", "Comunidad de Madrid", "https://www.comunidad.madrid/servicios/atencion-contribuyente/transmisiones-patrimoniales-onerosas"),
  ("Autoliquidación del Impuesto sobre Sucesiones y Donaciones", "Comunidad de Madrid", "https://www.comunidad.madrid/servicios/atencion-contribuyente/impuesto-sucesiones"),
  ("Valores de referencia de inmuebles en Madrid", "Comunidad de Madrid", "https://www.comunidad.madrid/servicios/atencion-contribuyente/valoracion-bienes-inmuebles-urbanos-rusticos"),
  ("Certificados tributarios", "Agencia Tributaria", "https://sede.agenciatributaria.gob.es/")]),
 ("Registros y certificados", [
  ("Certificado de últimas voluntades", "Ministerio de Justicia", "https://sede.mjusticia.gob.es/es/tramites/certificado-actos-ultima"),
  ("Certificado de contratos de seguro de fallecimiento", "Ministerio de Justicia", "https://sede.mjusticia.gob.es/es/tramites/certificado-contratos-seguro"),
  ("Certificado de defunción", "Registro Civil online", "https://www.registrocivilonline.info/certificado-defuncion.php"),
  ("Certificado de matrimonio", "Registro Civil online", "https://www.registrocivilonline.info/"),
  ("Certificado de nacimiento", "Registro Civil online", "https://www.registrocivilonline.info/certificado-nacimiento.php"),
  ("Certificación de denominación social", "Registro Mercantil Central", "http://www.rmc.es/Deno_solicitud.aspx"),
  ("Registro Nacional de Asociaciones", "Ministerio del Interior", "https://sede.mir.gob.es/nfrontal/webasocia2.html"),
  ("Registro Público Concursal", "Registro Público Concursal", "https://www.publicidadconcursal.es/concursal-web/afectado/buscar")]),
 ("Información catastral", [
  ("Consulta de datos catastrales", "Sede electrónica del Catastro", "http://www1.sedecatastro.gob.es/")])]

ARANCEL = [
 ("Real Decreto 1612/2011, de 14 de noviembre", "Por el que se modifican los Reales Decretos 1426/1989, de 17 de noviembre, y 1427/1989.", "real-decreto-16122011/"),
 ("Ley 41/2007, de 7 de diciembre", "Por la que se modifica la Ley 2/1981, de 25 de marzo, de Regulación del Mercado Hipotecario.", "ley-412007-de-7-de-diciembre-por-la-que-se-modifica-la-ley-21981-de-25-de-marzo-de-regulacion-del-mercado-hipotecario/"),
 ("Real Decreto 1131/2007, de 31 de agosto", "Por el que se fija la reducción de los derechos arancelarios de los notarios y registradores.", "real-decreto-11312007/"),
 ("Instrucción de la D.G.R.N. de 22 de mayo de 2002", "Se convierten a euros los aranceles de los notarios y registradores.", "notariado-de-22-de-mayo-de-2002/"),
 ("Real Decreto-ley 6/2000, de 23 de junio", "De medidas urgentes de intensificación de la competencia en mercados de bienes y servicios.", "real-decreto-ley-62000-de-23-de-junio-de-medidas-urgentes-de-intensificacion-de-la-competencia-en-mercados-de-bienes-y-servicios-b-o-e-1512000-de-24-jun/"),
 ("Resolución-Circular 17972, de 14 de julio de 1998", "Forma de aplicación de los aranceles por parte de notarios y registradores.", "resolucion-circular-17972-de14-julio-de-1998/"),
 ("Real Decreto 2484/1996, de 5 de diciembre", "Sobre reducción de los derechos notariales y honorarios de los registradores.", "real-decreto-24841996-de-5-de-diciembre-sobre-reduccion-de-los-derechos-notariales-y-honorarios/"),
 ("Real Decreto 1426/1989, de 17 de noviembre", "Por el que se aprueba el arancel de los notarios.", "real-decreto-14261989-de-17-de-noviembre-por-el-que-se-aprueba-el-arancel-de-los-notarios/"),
 ("Decreto 2079/1971, de 23 de julio", "Arancel especial de los derechos de los registradores y notarios.", "decreto-20791971-de-23-de-julio/"),
 ("Decreto de 15 de diciembre de 1950", "Sobre aranceles de los agentes de Cambio y Bolsa y corredores colegiados de comercio.", "decreto-de-15-12-1950-sobre-aranceles-de-los-agentes-de-cambio-y-bolsa-y-corredores-colegiados-de-comercio/")]

BLOG = [
 ("29 mayo 2019", "Pactos prematrimoniales en previsión de crisis conyugal", "Los pactos prematrimoniales van más allá de lo económico: pueden incluir otras disposiciones flexibles sobre la vida matrimonial.", "pactos-prematrimoniales-en-prevision-de-crisis-conyugal/"),
 ("27 octubre 2018", "AJD: la solución final", "Análisis de la sentencia del Tribunal Supremo sobre quién debe pagar el impuesto en los préstamos con garantía hipotecaria.", "ajd-la-solucion-final-para-un-impuesto-odioso/"),
 ("18 junio 2018", "Libertad de testar", "Los errores más habituales de los clientes sobre la libertad de testar y las limitaciones de la legítima.", "libertad-de-testar/"),
 ("22 mayo 2018", "La transacción sobre cláusula suelo", "Una sentencia del Tribunal Supremo de 2018 sobre las transacciones en litigios por cláusulas suelo.", "la-transaccion-sobre-clausula-suelo/")]
MISC = ["Índice de legislación de Derecho Privado", "Análisis financiero de una nueva modalidad de préstamo", "El coste real del crédito bancario",
        "Crédito al consumo: más cerca de Europa", "Inversiones extranjeras y R.D. 664/1999", "Incorporación de técnicas electrónicas a la actividad notarial",
        "La firma digital y el notario electrónico", "La interpretación de los contratos bancarios", "La protección al consumidor en USA: el A.P.R.",
        "La sociedad unipersonal", "La seguridad en las redes informáticas", "Personalidad jurídica y registros públicos", "Pagaré en blanco"]

FONTS = io.open(os.path.join(ROOT, "assets/fonts.css"), encoding="utf8").read().replace("url(fonts/", "url(assets/fonts/")

# --- Plantilla ---------------------------------------------------------------
def schema():
    d = {"@context": "https://schema.org", "@type": "Notary", "name": NAME, "url": BASE,
         "description": "Notario en Madrid (Puente de Vallecas). Escrituras, testamentos, herencias, compraventas, poderes y constitución de sociedades. Más de 30 años de ejercicio.",
         "telephone": TEL, "email": MAIL, "image": BASE + "og-image.jpg", "slogan": "Nihil prius fide",
         "address": {"@type": "PostalAddress", "streetAddress": "C. de la Sierra Bermeja, 42, 2º C", "addressLocality": "Madrid",
                     "postalCode": "28018", "addressRegion": "Madrid", "addressCountry": "ES"},
         "areaServed": {"@type": "City", "name": "Madrid"},
         "openingHoursSpecification": [{"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "09:00", "closes": "14:30"}],
         "founder": {"@type": "Person", "name": "Esteban Sánchez Sánchez", "jobTitle": "Notario"},
         "sameAs": [u for _, u in SOCIAL], "hasMap": MAPS}
    return '<script type="application/ld+json">' + json.dumps(d, ensure_ascii=False) + '</script>'

def head(title, desc, path, og="og-image.jpg"):
    url = BASE + path
    NOINDEX = '<meta name="robots" content="noindex, nofollow">' if DEMO else ""
    return f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0B1729">
{NOINDEX}
<meta property="og:type" content="website"><meta property="og:site_name" content="{NAME}"><meta property="og:locale" content="es_ES">
<meta property="og:url" content="{url}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{BASE}{og}"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{e(title)}"><meta name="twitter:description" content="{e(desc)}"><meta name="twitter:image" content="{BASE}{og}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="assets/fonts/Fraunces-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="assets/fonts/PlusJakartaSans-normal-latin.woff2" as="font" type="font/woff2" crossorigin>
<style>{FONTS}</style>
<link rel="stylesheet" href="assets/styles.css">
<script>document.documentElement.classList.add("js")</script>
{schema()}
</head>'''

def header(cur, hero):
    links = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == cur else ""}>{t}</a>' for h, t in NAV)
    return f'''<body>
<a class="skip" href="#main">Saltar al contenido</a>
<header class="site-header{' on-hero' if hero else ''}" id="hdr"><div class="wrap bar">
  <a class="brand" href="index.html" aria-label="{NAME} — inicio"><span class="mono">ESS</span><span class="brand-t"><b>Esteban Sánchez Sánchez</b><small>Notario · Madrid</small></span></a>
  <button class="menu-btn" aria-label="Abrir menú" aria-expanded="false" aria-controls="nav"><span></span><span></span><span></span></button>
  <nav class="nav" id="nav" aria-label="Principal">{links}<a class="btn" href="tel:{TEL_HREF}">Llamar</a></nav>
</div></header>'''

def footer():
    links = "".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV)
    soc = "".join(f'<li><a href="{u}" rel="noopener" target="_blank">{n}</a></li>' for n, u in SOCIAL)
    leg = "".join(f'<a href="{u}" rel="noopener">{t}</a>' for t, u in LEGAL)
    return f'''<footer class="site-footer"><div class="wrap">
  <div class="foot">
    <div><a class="brand" href="index.html"><span class="mono">ESS</span><span class="brand-t"><b>Esteban Sánchez Sánchez</b><small>Notario · Madrid</small></span></a><p class="foot-motto">Nihil prius fide.</p></div>
    <div><h4>Navegación</h4><ul>{links}</ul></div>
    <div><h4>Síguenos</h4><ul>{soc}</ul></div>
    <div><h4>Contacto</h4><ul><li><a href="tel:{TEL_HREF}">{TEL}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li>{e(ADDR)}</li><li>{HOURS}</li></ul></div>
  </div>
  <div class="legal"><span>© 2026 {NAME}</span><span class="legal-l">{leg}</span></div>
</div></footer>
<script src="assets/main.js" defer></script>
</body></html>'''

def cta_final():
    return f'''<section class="dark cta-final"><video class="bgvid" data-src="assets/video/apreton.mp4" poster="assets/video/apreton.jpg" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video><div class="wrap">
  <p class="label rule rv">Contacto</p>
  <h2 class="rv">Resolvamos su trámite de manera <em>ágil y eficiente.</em></h2>
  <a class="tel rv" href="tel:{TEL_HREF}">{TEL}</a>
  <div class="row rv"><a class="btn btn-solid" href="contacto.html">Escribir a la notaría {ARROW}</a><a class="btn btn-ghost" href="mailto:{MAIL}">{MAIL}</a></div>
</div></section>'''

def page_hero(label, h1, lead, img):
    return f'''<header class="page-hero"><img src="assets/img/{img}" alt="" width="1400" height="933" fetchpriority="high"><div class="wrap">
  <p class="label rule">{label}</p><h1>{h1}</h1><p class="lead">{lead}</p></div></header>'''

def write(name, s):
    io.open(os.path.join(ROOT, name), "w", encoding="utf-8", newline="\n").write(s)

# --- Páginas -------------------------------------------------------------------
def index():
    top = ESCRITURAS[:8]
    lis = "".join(f'<li><a href="escrituras.html"><span class="name">{e(n)}</span><span class="go">Ver</span></a></li>' for n, _ in top)
    dcards = "".join(f'<li><a href="documentacion.html#{a}"><span class="name">{e(t)}</span><span class="go">Qué aportar</span></a></li>' for a, t, _, _ in DOCS[:6])
    s = head("Notario en Madrid · Esteban Sánchez Sánchez", "Notaría en Puente de Vallecas, Madrid. Escrituras, testamentos, herencias, compraventas, poderes y sociedades, con atención personal y más de 30 años de ejercicio.", "")
    s += header("index.html", True)
    s += f'''
<main id="main">
<section class="hero" style="padding:0"><video class="bgvid d" data-src="assets/video/documento.mp4" poster="assets/video/documento.jpg" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video>
 <video class="bgvid m" data-src="assets/video/trato-movil.mp4" poster="assets/video/trato-movil.jpg" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video>
 <div class="wrap">
  <p class="label rule">Nihil prius fide</p>
  <h1>Notario en Madrid, <em>Esteban Sánchez Sánchez</em></h1>
  <p class="lead">{QUOTE}</p>
  <div class="cta"><a class="btn btn-solid" href="tel:{TEL_HREF}">Llamar {TEL} {ARROW}</a><a class="btn btn-ghost" href="contacto.html">Escribir a la notaría</a></div>
  <div class="facts"><div><b>+30 años</b><span>De ejercicio profesional</span></div><div><b>9:00 – 14:30</b><span>Lunes a viernes</span></div><div><b>Puente de Vallecas</b><span>Sierra Bermeja, 42 · Madrid</span></div></div>
 </div>
</section>

<section><div class="wrap two">
  <div><p class="label rule rv">Notaría en Madrid</p></div>
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
  <p style="margin-top:36px" class="rv"><a class="link" href="escrituras.html">Ver las {len(ESCRITURAS)} escrituras y actas</a></p>
</div></section>

<section class="band"><video class="bgvid" data-src="assets/video/acuerdo.mp4" poster="assets/video/acuerdo.jpg" muted loop playsinline preload="none" aria-hidden="true" tabindex="-1"></video><div class="wrap">
  <p class="label rule">Seguridad jurídica</p>
  <blockquote>«El notario es garante de la <em>seguridad jurídica</em> y controlador de la legalidad.»</blockquote>
</div></section>

<section><div class="wrap">
  <div class="sec-head"><div><p class="label rule rv">Documentación y trámites</p><h2 class="rv">Sepa qué <em>aportar</em> antes de firmar</h2></div>
  <p class="rv">Para cada escritura, la lista de documentos que hay que traer y los trámites que siguen a la firma.</p></div>
  <ul class="index rv">{dcards}</ul>
  <p style="margin-top:36px" class="rv"><a class="link" href="documentacion.html">Toda la documentación a aportar</a></p>
</div></section>

<section class="dark"><div class="wrap">
  <p class="label rule rv">Compromiso</p>
  <h2 class="rv" style="font-size:clamp(34px,4.8vw,68px);margin-top:18px;max-width:18ch">Máxima profesionalidad, implicación y <em>confidencialidad</em></h2>
  <ul class="commit rv"><li>Soluciones eficaces</li><li>Resolución de dudas</li><li>Optimización de compraventas</li><li>Asesoramiento</li><li>Confidencialidad absoluta</li><li>Información detallada y trato personalizado</li></ul>
</div></section>

<section class="paper2"><div class="wrap contact-grid">
  <div><p class="label rule rv">Cómo llegar</p><h2 class="rv" style="font-size:clamp(34px,4.4vw,60px);margin-top:18px">En <em>Puente de Vallecas</em></h2></div>
  <div class="data rv"><dl>
    <div><dt>Dirección</dt><dd>{e(ADDR)}<br><a href="{MAPS}" target="_blank" rel="noopener">Abrir en Google Maps</a></dd></div>
    <div><dt>Horario</dt><dd>{HOURS}</dd></div>
    <div><dt>Teléfono</dt><dd><a href="tel:{TEL_HREF}">{TEL}</a> · <a href="tel:914776750">914 776 750</a></dd></div>
    <div><dt>Correo</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
  </dl></div>
</div></section>
{cta_final()}
</main>'''
    s += footer(); write("index.html", s)

def escrituras():
    lis = "".join(
        f'<li><div class="row"><span class="name">{e(n)}</span>' + (f'<a class="doc" href="documentacion.html#{a}">Documentación</a>' if a else '<span></span>') + '</div></li>'
        for n, a in ESCRITURAS)
    s = head("Escrituras y actas notariales en Madrid · Notaría Esteban Sánchez", "Actas y escrituras públicas: compraventas, testamentos, herencias, poderes, sociedades, hipotecas, capitulaciones y más. Notaría en Puente de Vallecas, Madrid.", "escrituras.html")
    s += header("escrituras.html", True)
    s += page_hero("Escrituras", "Actas y escrituras <em>públicas notariales</em>", QUOTE, "despacho.jpg")
    s += f'<main id="main"><section><div class="wrap"><ul class="index cols-2 rv">{lis}</ul></div></section>{cta_final()}</main>'
    s += footer(); write("escrituras.html", s)

def render_block(b):
    k = b[0]
    if k == "h": return f"<h3>{e(b[1])}</h3>"
    if k == "p": return f"<p>{e(b[1])}</p>"
    if k == "note": return f'<p class="note">{e(b[1])}</p>'
    if k == "countries": return f'<h3>Países firmantes del Convenio</h3><p class="countries">{e(b[1])}</p>'
    if k == "ul": return "<ul>" + "".join(f"<li>{e(x)}</li>" for x in b[1]) + "</ul>"
    return ""

def documentacion():
    toc = "".join(f'<a href="#{a}">{e(t)}</a>' for a, t, _, _ in DOCS)
    blocks = "".join(
        f'<article class="doc-block rv" id="{a}"><p class="label">Documentación</p><h2>{e(t)}</h2><p>{e(sub)}</p>' + "".join(render_block(b) for b in bl) + "</article>"
        for a, t, sub, bl in DOCS)
    s = head("Documentación a aportar y trámites · Notaría Esteban Sánchez", "Qué documentos llevar a la notaría para compraventas, herencias, testamentos, poderes, sociedades, hipotecas, obras nuevas y apostilla. Notario en Madrid.", "documentacion.html")
    s += header("documentacion.html", True)
    s += page_hero("Documentación", "Documentación <em>a aportar</em> y trámites", "Para cada escritura, lo que necesitamos de usted y los trámites que siguen a la firma.", "estructura.jpg")
    s += f'<main id="main"><section><div class="wrap doc-layout"><nav class="toc" aria-label="Temas">{toc}</nav><div>{blocks}</div></div></section>{cta_final()}</main>'
    s += footer(); write("documentacion.html", s)

def online():
    groups = ""
    for g, items in ONLINE:
        groups += f'<h2 class="group-title">{e(g)}</h2><ul class="ext">' + "".join(
            f'<li><a href="{u}" target="_blank" rel="noopener"><span class="t">{e(t)}</span><span class="o">{e(o)}</span></a></li>' for t, o, u in items) + "</ul>"
    s = head("Servicios online: trámites y certificados · Notaría Esteban Sánchez", "Autoliquidación de impuestos, certificados de últimas voluntades, defunción, matrimonio y nacimiento, datos catastrales y registros. Enlaces directos.", "servicios-online.html")
    s += header("servicios-online.html", True)
    s += page_hero("Servicios online", "Trámites y certificados <em>en línea</em>", "Enlaces directos a las sedes oficiales para los trámites más habituales.", "atencion.jpg")
    s += f'<main id="main"><section><div class="wrap rv">{groups}</div></section>{cta_final()}</main>'
    s += footer(); write("servicios-online.html", s)

def arancel():
    lis = "".join(f'<li><a href="https://essnotario.com/{u}" target="_blank" rel="noopener"><span><span class="t">{e(t)}</span><span class="s">{e(d)}</span></span><span class="o">Ampliar información</span></a></li>' for t, d, u in ARANCEL)
    s = head("Normas arancelarias notariales · Notaría Esteban Sánchez", "Normativa que regula el arancel de los notarios: Real Decreto 1426/1989, Real Decreto 1612/2011, Ley 41/2007 y otras disposiciones.", "arancel.html")
    s += header("arancel.html", True)
    s += page_hero("Arancel", "Normas <em>arancelarias</em>", "La normativa que regula los derechos de los notarios.", "techo.jpg")
    s += f'''<main id="main"><section><div class="wrap"><ul class="ext rv">{lis}</ul>
<p class="lead rv" style="margin-top:48px">¿Necesita conocer el coste de una escritura? Llámenos al <a class="link" href="tel:{TEL_HREF}">{TEL}</a>.</p></div></section>{cta_final()}</main>'''
    s += footer(); write("arancel.html", s)

def publicaciones():
    posts = "".join(f'<li><a href="https://essnotario.com/{u}" target="_blank" rel="noopener"><time>{d}</time><span><span class="t">{e(t)}</span><span class="e">{e(x)}</span></span><span class="go" aria-hidden="true">↗</span></a></li>' for d, t, x, u in BLOG)
    misc = "".join(f'<li><div class="row"><span class="name">{e(t)}</span><span></span></div></li>' for t in MISC)
    s = head("Blog y publicaciones jurídicas · Notaría Esteban Sánchez", "Artículos del notario Esteban Sánchez: pactos prematrimoniales, libertad de testar, AJD, cláusula suelo, firma digital, contratos bancarios y más.", "publicaciones.html")
    s += header("publicaciones.html", True)
    s += page_hero("Publicaciones", "Blog y <em>miscelánea</em> jurídica", "Artículos y estudios sobre Derecho privado, contratación y práctica notarial.", "estructura.jpg")
    s += f'''<main id="main"><section><div class="wrap"><h2 class="group-title">Blog</h2><ul class="posts rv">{posts}</ul>
<h2 class="group-title" style="margin-top:88px">Miscelánea</h2><ul class="index cols-2 rv">{misc}</ul></div></section>{cta_final()}</main>'''
    s += footer(); write("publicaciones.html", s)

def contacto():
    s = head("Contacto y localización · Notaría Esteban Sánchez Sánchez", "Notaría en C. de la Sierra Bermeja, 42, 2º C, Puente de Vallecas, Madrid. Tel. 914 77 67 50. Lunes a viernes de 9:00 a 14:30.", "contacto.html")
    s += header("contacto.html", True)
    s += page_hero("Contacto", "Localización y <em>contacto</em>", "Llámenos o escríbanos. Le atenderemos de forma personal.", "ciudad.jpg")
    s += f'''<main id="main"><section><div class="wrap contact-grid">
  <div class="data rv"><dl>
    <div><dt>Dirección</dt><dd>{e(ADDR)}<br><a href="{MAPS}" target="_blank" rel="noopener">Abrir en Google Maps</a></dd></div>
    <div><dt>Horario</dt><dd>{HOURS}</dd></div>
    <div><dt>Teléfono</dt><dd><a href="tel:{TEL_HREF}">{TEL}</a><br><a href="tel:914776750">914 776 750</a></dd></div>
    <div><dt>Correo</dt><dd><a href="mailto:{MAIL}">{MAIL}</a></dd></div>
  </dl></div>
  <form class="card rv" id="f" action="mailto:{MAIL}" method="post" enctype="text/plain">
    <div class="field"><label for="n">Su nombre <i>*</i></label><input id="n" name="nombre" required autocomplete="name"></div>
    <div class="field"><label for="m">Su correo <i>*</i></label><input id="m" name="correo" type="email" required autocomplete="email"></div>
    <div class="field"><label for="a">Asunto</label><input id="a" name="asunto"></div>
    <div class="field"><label for="x">Su mensaje</label><textarea id="x" name="mensaje"></textarea></div>
    <button class="btn btn-dark" type="submit">Enviar mensaje {ARROW}</button>
    <p class="form-note">Se abrirá su programa de correo con el mensaje preparado. No incluya datos sensibles; para asuntos urgentes, llámenos.</p>
  </form>
</div></section></main>'''
    s += footer(); write("contacto.html", s)

def extras():
    NL = chr(10)
    write("robots.txt", ("User-agent: *" + NL + "Disallow: /" + NL) if DEMO else ("User-agent: *" + NL + "Allow: /" + NL + NL + "Sitemap: " + BASE + "sitemap.xml" + NL))
    urls = [""] + [h for h, _ in NAV]
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' +
          "".join(f"  <url><loc>{BASE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
    write("assets/favicon.svg", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" fill="#0B1729"/><rect x="6" y="6" width="52" height="52" fill="none" stroke="#D2AE68" stroke-width="2"/><text x="32" y="40" font-family="Georgia,serif" font-size="22" font-weight="700" fill="#D2AE68" text-anchor="middle" letter-spacing="1">ESS</text></svg>')

for f in (index, escrituras, documentacion, online, arancel, publicaciones, contacto, extras): f()
print("ok")
