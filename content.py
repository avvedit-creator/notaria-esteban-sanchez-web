# Contenido extraído de essnotario.com (ver LEEME: qué es literal y qué no)
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

