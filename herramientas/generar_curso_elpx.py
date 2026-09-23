#!/usr/bin/env python3
"""Genera el curso «Agentes de IA y Microsoft Copilot para tu día a día» como paquete .elpx.

Entrada : guión_curso_copilot_exelearning.md (revisión V) + recursos/imagenes/
Salida  : entregables/curso_copilot_agentes.elpx  (+ entregables/content.xml)

El paquete se valida contra el DTD y el XSD oficiales (xmllint) antes de darse por bueno.

Uso:
    python3 herramientas/generar_curso_elpx.py            # genera y valida
    python3 herramientas/generar_curso_elpx.py --check    # además, informe de fidelidad de textos

Notas de diseño (decisiones tomadas y documentadas en idevices_equivalencias_exelearning4.md):
  - 25 nodos (guion y curso coinciden: no se excluye ninguno), UN iDevice por página, en un bloque
    único y SIN nombre de bloque (nada de la etiqueta «Texto»).
  - «Acordeón»  -> efecto nativo `exeeffects` (<div class="exe-fx exe-accordion">) dentro del iDevice Texto.
  - «Tabla» / «Lista numerada» -> HTML dentro del iDevice Texto.
  - «Nota»      -> cita destacada (<blockquote>) con el icono del guion, dentro del iDevice Texto.
  - «Cuestionario» -> iDevice `quick-questions` con el estado real extraído del fixture oficial.
  - Portada: el título, el subtítulo y «Duración · Nivel» van superpuestos sobre la foto (overlay con
    degradado + sombra, definido en ESTILOS_PROPIOS); el CSS decide si se superpone o se apila debajo
    según el ancho real de la columna (`@container`).
"""
import json
import pathlib
import random
import re
import string
import subprocess
import sys
import urllib.parse
import zipfile
from datetime import datetime

RAIZ = pathlib.Path(__file__).resolve().parent.parent
GUION = RAIZ / "guión_curso_copilot_exelearning.md"
IMGS = RAIZ / "recursos" / "imagenes"
PLANTILLAS = RAIZ / "herramientas" / "plantillas"
SALIDA = RAIZ / "entregables"
DTD_DESTINO = SALIDA / "content.dtd"
XOR_KEY = 146

# --------------------------------------------------------------------------- revisión IV (13-sep-2026)
# Ajustes pedidos por el autor sobre el resultado exportado:
#   1. Un único iDevice Texto por página -> un solo bloque, sin scroll innecesario.
#   2. Los bloques van SIN nombre: se elimina la etiqueta «Texto» de cada uno.
#   3. Menú lateral: «N. Título» (se quita la etiqueta decorativa «MÓDULO x —»).
#   4. Tema Nova (antes: base).
#   5. La página «EJERCICIOS» sale del curso.
#   6. Se elimina del cuestionario la referencia colgante a Latidos.gif que arrastraba la
#      plantilla (procedía del fixture oficial; el iDevice real no la usa).
TEMA = "nova"

# --------------------------------------------------------------------------- revisión VI (13-sep-2026)
# Remediación de cumplimiento (Art. 4 del AI Act):
#   - 7 páginas nuevas: fundamentos de IA (2), uso responsable (sobreexposición y política) y marco
#     legal y obligaciones (3).
#   - La página «EJERCICIOS PRÁCTICOS» vuelve al paquete con 4 de los 8 ejercicios (los otros 4
#     quedan documentados en el guion).
#   - El cuestionario pasa de 10 a 20 preguntas (14 correctas para aprobar, 70 %).
#   - El despacho de iDevices pasa a ser por CLAVE (título del nodo), no por número: así se pueden
#     insertar o reordenar páginas sin tocar la lógica de montaje.
# Guion y curso tienen ya las MISMAS 25 páginas. NODOS_EXCLUIDOS queda vacío a propósito: se
# mantiene el mecanismo por si una decisión futura vuelve a sacar una página del montaje.
NODOS_EXCLUIDOS = set()
NODOS_ESPERADOS = 25
JSON_PLANTILLA_QUIZ = PLANTILLAS / "quiz_quick-questions.json"
# El .elpx mínimo re-importable que escribe este script es un INTERMEDIO. El entregable
# `entregables/curso_copilot_agentes.elpx` lo produce el CLI de eXeLearning (formato `elpx`), que
# añade tema, html renderizado e iDevices: paquete completo y abrible en la app.
ELPX_MINIMO = SALIDA / "_trabajo" / "curso_copilot_agentes_minimo.elpx"

# CSS propio del proyecto, inyectado en el <head> de cada página vía pp_extraHeadContent (el
# importador de eXeLearning NO lee pp_customStyles, pero sí pp_extraHeadContent). Las páginas llevan
# un único bloque SIN titular: en el tema Nova la cabecera vacía del bloque reserva 60 px y deja
# suelto el botón de plegado. Aquí se anulan los dos, para que el texto empiece limpio.
ESTILOS_PROPIOS = """<style>
/* Bloques sin titular: sin franja de cabecera ni botón de plegado suelto. */
body.exe-export .box.no-header > header.box-head{min-height:0 !important;border-bottom:0 !important;padding:0 !important}
body.exe-export .box.no-header .box-toggle{display:none !important}
/* Navegación «Anterior / Siguiente» al pie de la página, en el flujo y alineada con la columna de
   texto (Nova la fija arriba a la derecha). El div .nav-buttons ya viene en el HTML justo después de
   </main>; el post-proceso lo mete dentro de <main> para que herede el hueco del menú lateral y los
   puntos de ruptura del tema. Es el mismo esquema que usa .page-content. */
body.exe-export .nav-buttons{display:flex;justify-content:space-between;align-items:center;gap:16px;
  flex-wrap:wrap;max-width:1280px;margin:40px auto 0;padding:0 90px}
body.exe-export .nav-buttons .nav-button{position:static;top:auto;right:auto}
/* Nova oculta las etiquetas de los botones por debajo de 1024 px porque arriba compartían barra con
   los togglers; al pie vuelve a caber el texto, así que se recuperan. */
@media (max-width:1024px){
  body.exe-export .nav-buttons .nav-button{height:auto;width:auto;padding:18px}
  body.exe-export .nav-buttons .nav-button-left{padding-left:48px;background-position:left 14px center}
  body.exe-export .nav-buttons .nav-button-right{padding-right:48px;background-position:right 14px center}
  body.exe-export .nav-buttons .nav-button span{display:inline}}
/* los mismos márgenes que .page-content en cada punto de ruptura del tema */
@media (max-width:750px){body.exe-export .nav-buttons{padding:0 20px;margin:0 auto}}
@media (max-width:650px){body.exe-export .nav-buttons{padding:0 30px}}
/* Portada. Por defecto el texto va DEBAJO de la imagen: es lo seguro a cualquier ancho y en
   cualquier navegador. Cuando la columna de contenido da de sí (container query sobre la propia
   portada, no sobre el viewport: el tema cambia la columna según el menú lateral), el título pasa a
   superponerse sobre la foto. La foto es clara por zonas (contraste medio del blanco: 4,96:1 en la
   franja baja y hasta 2,87:1 en la esquina inferior derecha), así que el texto superpuesto va sobre
   un degradado oscuro Y con sombra propia. */
body.exe-export .portada{position:relative;margin:0 0 1.6em;overflow:hidden;border-radius:12px}
body.exe-export .portada > img{display:block;width:100%;height:auto;margin:0}
body.exe-export .portada .portada-texto{line-height:1.3;padding:1.1em 0 0}
body.exe-export .portada .portada-titulo{margin:0 0 .3em;font-weight:800;line-height:1.15;color:#282573;
  font-size:clamp(1.35rem,2.4vw,2rem) !important}
body.exe-export .portada .portada-subtitulo{margin:0;color:#3c3c3c;
  font-size:clamp(1rem,1.5vw,1.15rem) !important}
body.exe-export .portada .portada-datos{margin:.7em 0 0}
body.exe-export .portada .portada-datos p{margin:0;color:#3c3c3c;
  font-size:clamp(.85rem,1.1vw,.95rem) !important}
body.exe-export .portada{container-type:inline-size}
@container (min-width:520px){
  body.exe-export .portada .portada-texto{position:absolute;left:0;right:0;bottom:0;padding:
    clamp(30px,6.5cqw,84px) clamp(18px,5cqw,64px) clamp(16px,3.5cqw,44px);
    /* el degradado llega a .62 antes de que empiece el texto: por debajo hay píxeles muy claros
       (pantalla del móvil, cuaderno) y con menos opacidad el blanco se perdía */
    background:linear-gradient(180deg,rgba(8,12,26,0) 0%,rgba(8,12,26,.62) 20%,rgba(8,12,26,.86) 46%,rgba(8,12,26,.91) 100%)}
  body.exe-export .portada .portada-titulo{color:#fff;font-size:clamp(1.3rem,4.2cqw,2.6rem) !important;
    text-shadow:0 1px 3px rgba(0,0,0,.95),0 3px 10px rgba(0,0,0,.8),0 8px 30px rgba(0,0,0,.65)}
  body.exe-export .portada .portada-subtitulo{color:#fff;font-size:clamp(.95rem,2cqw,1.3rem) !important;
    text-shadow:0 1px 3px rgba(0,0,0,.95),0 3px 10px rgba(0,0,0,.75)}
  body.exe-export .portada .portada-datos p{color:#fff;opacity:.95;
    font-size:clamp(.8rem,1.4cqw,.95rem) !important;
    text-shadow:0 1px 3px rgba(0,0,0,.95),0 2px 8px rgba(0,0,0,.8)}
  body.exe-export .portada .portada-datos strong{color:#fff}
}
/* Recuadro de ideas clave (revisión VII). Es un recurso didáctico de refuerzo que va a MITAD de
   página y solo en las páginas donde el guion lo pide: si apareciera en todas, el lector dejaría
   de fijarse en él. Fondo secundario de la paleta del proyecto y borde de acento azul; la etiqueta
   en versalitas. Contrastes comprobados con la fórmula de luminancia de WCAG 2.1:
   #1E293B sobre #F8FAFC = 13,98:1 y #2563EB sobre #F8FAFC = 4,94:1 (AA texto normal los dos). */
body.exe-export .caja-ideas-clave{margin:1.9em 0;padding:1.05em 1.25em 1.05em 1.35em;
  background:#F8FAFC;border:1px solid #E2E8F0;border-left:5px solid #2563EB;border-radius:0 8px 8px 0}
body.exe-export .caja-ideas-clave .caja-ideas-clave-titulo{margin:0 0 .55em;color:#2563EB;
  font-size:.8rem;font-weight:700;letter-spacing:.09em;text-transform:uppercase;line-height:1.2}
body.exe-export .caja-ideas-clave ul{margin:0;padding-left:1.25em}
body.exe-export .caja-ideas-clave li{margin:.3em 0;color:#1E293B}
body.exe-export .caja-ideas-clave li::marker{color:#2563EB}
body.exe-export .caja-ideas-clave p{margin:.4em 0}
@media (max-width:600px){body.exe-export .caja-ideas-clave{margin:1.5em 0;
  padding:.9em 1em .9em 1.1em;border-left-width:4px}}
</style>"""

DTD_LOCAL = None  # se resuelve desde el contenedor si hace falta

# --------------------------------------------------------------------------- helpers


def oid(ts: str, sufijo: str) -> str:
    """Identificador ODE: YYYYMMDDHHmmss + 6 caracteres [A-Z0-9]."""
    return ts + sufijo


def nuevo_sufijo(usados: set) -> str:
    alfabeto = string.ascii_uppercase + string.digits
    while True:
        s = "".join(random.choice(alfabeto) for _ in range(6))
        if s not in usados:
            usados.add(s)
            return s


def xml_escape(texto: str) -> str:
    return (texto.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))


def cdata(texto: str) -> str:
    """Envuelve en CDATA partiendo cualquier ]]> interno (regla del formato)."""
    return "<![CDATA[" + texto.replace("]]>", "]]]]><![CDATA[>") + "]]>"


# --------------------------------------------------------------------------- markdown -> HTML

RE_BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)
RE_ITAL = re.compile(r"(?<!\*)\*(?!\s)([^*]+?)(?<!\s)\*(?!\*)", re.S)
RE_LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")
RE_LI_BULLET = re.compile(r"^[-*]\s+(.*)$")
RE_LI_NUM = re.compile(r"^(\d+)[.)]\s+(.*)$")
RE_H = re.compile(r"^(#{1,6})\s+(.*)$")


def en_linea(texto: str) -> str:
    """Enlaces, negritas y cursivas. Preserva el resto tal cual."""
    texto = RE_LINK.sub(r'<a href="\2" target="_blank" rel="noopener">\1</a>', texto)
    texto = RE_BOLD.sub(r"<strong>\1</strong>", texto)
    texto = RE_ITAL.sub(r"<em>\1</em>", texto)
    return texto


def fila_tabla(linea: str):
    celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
    return celdas


def escape_atributo(texto: str) -> str:
    """Texto seguro para un valor de atributo HTML (`value="..."`)."""
    return (texto.replace("&", "&amp;").replace('"', "&quot;")
            .replace("<", "&lt;").replace(">", "&gt;"))


def render_tabla(lineas):
    filas = [fila_tabla(l) for l in lineas]
    # descarta la fila de guiones (|---|)
    filas = [f for f in filas if not all(re.fullmatch(r":?-{2,}:?", c or "-") for c in f)]
    if not filas:
        return ""
    html = ['<table class="exe-table">', "<thead>", "<tr>"]
    for c in filas[0]:
        html.append(f"<th>{en_linea(c)}</th>")
    html += ["</tr>", "</thead>", "<tbody>"]
    for f in filas[1:]:
        html.append("<tr>")
        for c in f:
            html.append(f"<td>{en_linea(c)}</td>")
        html.append("</tr>")
    html += ["</tbody>", "</table>"]
    return "".join(html)


def render_bloque(bloque: str) -> str:
    """Convierte un bloque (separado por <br><br>) en HTML."""
    lineas = [l.strip() for l in re.split(r"<br\s*/?>", bloque)]
    lineas = [l for l in lineas if l]
    if not lineas:
        return ""

    # tabla
    if all(l.startswith("|") for l in lineas) and len(lineas) >= 2:
        return render_tabla(lineas)

    salida = []
    lista = None      # 'ul' | 'ol' | None

    def cierra():
        nonlocal lista
        if lista:
            salida.append(f"</{lista}>")
            lista = None

    for linea in lineas:
        if linea.startswith(">"):
            cierra()
            cita = linea.lstrip(">").strip()
            salida.append(f"<blockquote><p>{en_linea(cita)}</p></blockquote>")
            continue
        m_b = RE_LI_BULLET.match(linea)
        m_n = RE_LI_NUM.match(linea)
        if m_b:
            if lista != "ul":
                cierra()
                salida.append("<ul>")
                lista = "ul"
            salida.append(f"<li>{en_linea(m_b.group(1))}</li>")
        elif m_n:
            if lista != "ol":
                cierra()
                salida.append("<ol>")
                lista = "ol"
            salida.append(f"<li>{en_linea(m_n.group(2))}</li>")
        else:
            cierra()
            m_h = RE_H.match(linea)
            if m_h:
                nivel = min(len(m_h.group(1)) + 1, 6)  # # -> h2 (el h1 es el título de página)
                salida.append(f"<h{nivel}>{en_linea(m_h.group(2))}</h{nivel}>")
            else:
                salida.append(f"<p>{en_linea(linea)}</p>")
    cierra()
    return "".join(salida)


def markdown_a_html(contenido: str) -> str:
    """Convierte el «Contenido en pantalla» del guion a HTML."""
    # Separadores decorativos del guion («---» sueltos). NO vale un replace a secas: las filas de
    # separación de las tablas están hechas de guiones («|-------|») y un replace de «---» las
    # troceaba, dejando una fila fantasma de guiones dentro de la tabla.
    contenido = re.sub(r"(?<![\w|-])---(?![\w|-])", "\n", contenido)
    bloques = re.split(r"(?:<br\s*/?>\s*){2,}", contenido)
    return "".join(render_bloque(b) for b in bloques if b.strip())


# ------------------------------------------------------- recuadro de ideas clave (revisión VII)
# Recurso de refuerzo que se coloca a mitad de página y solo en algunas páginas. Su texto vive en
# el guion (fila «Recuadro de ideas clave»), con esta forma:
#     **POSICIÓN:** tras «Título del bloque»<br><br>**Ideas clave**<br><br>- viñeta<br>- viñeta
# El generador no inventa texto: solo lo coloca donde el guion dice.
ANCLA_RECUADRO = re.compile(r"«([^»]+)»")


def texto_recuadro(campo: str) -> str:
    """Solo el texto del recuadro (la parte tras el salto doble), sin la línea «POSICIÓN:».

    La línea de posición es una instrucción de montaje: no es texto que deba verse en la página,
    así que queda fuera de la comprobación de fidelidad.
    """
    partes = re.split(r"(?:<br\s*/?>\s*){2,}", campo or "", maxsplit=1)
    return partes[1].strip() if len(partes) == 2 else ""


def _caja_html(campo: str):
    """Convierte el campo del guion en (ancla del bloque, HTML del recuadro)."""
    cuerpo = texto_recuadro(campo)
    if not cuerpo:
        raise ValueError("el recuadro necesita «**POSICIÓN:** tras «...»» y, tras un salto doble, "
                         f"el texto: {campo[:80]!r}")
    ancla_m = ANCLA_RECUADRO.search(campo.split("**")[0] or campo)
    if not ancla_m:
        raise ValueError("la posición del recuadro no cita el bloque de anclaje entre «»: "
                         f"{campo[:80]!r}")
    # La primera línea en negrita es el título del recuadro: hace de etiqueta visible y accesible.
    m_titulo = re.match(r"\*\*(.+?)\*\*\s*(?:<br\s*/?>)?\s*", cuerpo)
    titulo = m_titulo.group(1).strip() if m_titulo else "Ideas clave"
    if m_titulo:
        cuerpo = cuerpo[m_titulo.end():]
    html = (f'<aside class="caja-ideas-clave" role="note" aria-label="{titulo}">'
            f'<p class="caja-ideas-clave-titulo">{titulo}</p>'
            f'{markdown_a_html(cuerpo)}</aside>')
    return ancla_m.group(1).strip(), html


# Cierres que delimitan el elemento que contiene el ancla: el recuadro entra justo después.
CIERRES_ELEMENTO = ("</p>", "</li>", "</h2>", "</h3>", "</h4>", "</h5>", "</h6>",
                    "</blockquote>", "</td>", "</th>", "</table>", "</ul>", "</ol>")
# Encabezados del HTML ya montado (el generador los emite como h2..h6).
RE_ENCABEZADO = re.compile(r"<h([2-6])[^>]*>(.*?)</h\1>", re.DOTALL)


def patron_ancla(ancla: str):
    """Regex del ancla: admite etiquetas y espacios entre sus palabras.

    El ancla se escribe en el guion como texto normal («tras «Cuatro conceptos...»»), pero en el
    HTML puede llevar negritas dentro, así que no vale un `find` literal.
    """
    palabras = [re.escape(p) for p in ancla.split()]
    return re.compile(r"(?:<[^>]+>|\s)*".join(palabras), re.IGNORECASE)


def _dentro_de_lista(html: str, pos: int) -> bool:
    """¿La posición cae dentro de una lista? (entonces el recuadro va tras la lista entera)."""
    abre = max(html.rfind("<ul", 0, pos), html.rfind("<ol", 0, pos))
    cierra = max(html.rfind("</ul>", 0, pos), html.rfind("</ol>", 0, pos))
    return abre > cierra


def insertar_recuadro(html: str, ancla: str, caja: str) -> str:
    """Coloca el recuadro justo después del párrafo, título o cita que contiene el ancla.

    Falla en voz alta si el ancla no existe o si aparece más de una vez: montar la página sin el
    recuadro (o con él en el sitio equivocado) en silencio es justo lo que no queremos, igual que
    en la red de seguridad de las claves de nodo.
    """
    coincidencias = list(patron_ancla(ancla).finditer(html))
    if not coincidencias:
        raise ValueError(f"no encuentro el ancla «{ancla}» para el recuadro")
    if len(coincidencias) > 1:
        raise ValueError(f"el ancla «{ancla}» aparece {len(coincidencias)} veces; usa un texto único")
    inicio_ancla, fin_ancla = coincidencias[0].start(), coincidencias[0].end()

    # 1) Si el ancla es un ENCABEZADO, el recuadro cierra la sección entera: va antes del siguiente
    #    encabezado de nivel igual o superior (o al final de la página si no hay ninguno).
    for m in RE_ENCABEZADO.finditer(html):
        if m.start() <= inicio_ancla and fin_ancla <= m.end():
            nivel = int(m.group(1))
            for otro in RE_ENCABEZADO.finditer(html, m.end()):
                if int(otro.group(1)) <= nivel:
                    return html[:otro.start()] + caja + html[otro.start():]
            return html + caja

    # 2) Si el ancla cae en una lista, va tras la lista completa (no dentro del <ul>).
    if _dentro_de_lista(html, fin_ancla):
        cierres = [html.find(c, fin_ancla) for c in ("</ul>", "</ol>")]
        cierres = [p for p in cierres if p != -1]
        if not cierres:
            raise ValueError(f"la lista del ancla «{ancla}» no cierra")
        fin = min(cierres) + len("</ul>")
        return html[:fin] + caja + html[fin:]

    # 3) Párrafo, cita o etiqueta en negrita: el recuadro entra justo detrás de ese elemento.
    candidatos = [(html.find(c, fin_ancla), c) for c in CIERRES_ELEMENTO]
    candidatos = [(p, c) for p, c in candidatos if p != -1]
    if not candidatos:
        raise ValueError(f"el ancla «{ancla}» no está dentro de ningún elemento que cierre")
    pos, cierre = min(candidatos)
    fin = pos + len(cierre)
    return html[:fin] + caja + html[fin:]


# --------------------------------------------------------------------------- iDevices


def componente_texto(ts, usados, bloques_html, idevice_id=None,
                      feedback_titulo="", feedback_texto=""):
    """iDevice Texto (patrón Standard JSON).

    Cada página lleva UN SOLO iDevice Texto: `bloques_html` es la concatenación de todos los
    fragmentos de la página (intro + acordeón + notas + imágenes). Así la página tiene un único
    bloque y el lector no se ve obligado a hacer scroll entre bloques.

    `feedback_texto` activa el botón de retroalimentación que trae el propio iDevice (el export
    llama a `createFeedbackHTML` cuando `textFeedbackTextarea` no está vacío): el alumno escribe
    su respuesta y el botón le muestra la respuesta modelo. Es el iDevice nativo que convierte una
    actividad de respuesta abierta en algo interactivo, sin JavaScript propio (regla 7).
    """
    idevice_id = idevice_id or oid(ts, nuevo_sufijo(usados))
    cuerpo = f'<div class="exe-text">{bloques_html}</div>'
    # La retroalimentación va DENTRO del htmlView, no solo en las propiedades del iDevice.
    # Motivo (verificado en el export): el exportador solo copia `ideviceId` al atributo
    # `data-idevice-json-data`, así que el `text.js` del iDevice nunca recibe
    # `textFeedbackTextarea` y la respuesta modelo no llegaba al curso: el ejercicio quedaba sin
    # su respuesta. El marcado es el que genera el propio `createFeedbackHTML` del iDevice, para
    # que su JS lo enganche y lo muestre y oculte al pulsar el botón.
    feedback_html = ""
    if feedback_texto:
        titulo_btn = feedback_titulo or "Mostrar retroalimentación"
        feedback_html = (
            '<div class="iDevice_buttons feedback-button js-required">'
            f'<input type="button" class="feedbacktooglebutton" value="{escape_atributo(titulo_btn)}">'
            "</div>"
            f'<div class="feedback js-feedback js-hidden">{feedback_texto}</div>'
        )
    html_view = (
        '<div class="exe-text-template"><div class="textIdeviceContent">\n'
        '  <div class="exe-text-activity">\n    <div>\n'
        f"      {cuerpo}\n"
        f'    </div>\n    <p class="clearfix"></p>\n    {feedback_html}\n  </div>\n</div></div>'
    )
    props = {
        "ideviceId": idevice_id,
        "textInfoDurationInput": "",
        "textInfoDurationTextInput": "Duración",
        "textInfoParticipantsInput": "",
        "textInfoParticipantsTextInput": "Agrupamiento",
        "textTextarea": cuerpo,
        "textFeedbackInput": feedback_titulo or "Mostrar retroalimentación",
        "textFeedbackTextarea": feedback_texto,
    }
    return {"tipo": "text", "id": idevice_id, "htmlView": html_view,
            "jsonProperties": json.dumps(props, ensure_ascii=False)}


ALT_PORTADA = ("Vista aérea de un escritorio de trabajo moderno con un portátil, un teléfono móvil, "
               "un cuaderno y una lámpara, con espacio libre")


def portada_con_overlay(nombre_img, titulo_html, subtitulo_html, datos_html, alt=ALT_PORTADA):
    """Imagen de portada con el texto superpuesto.

    El texto va sobre un degradado oscuro (el CSS del proyecto lo pinta) y además lleva sombra
    propia, porque la foto es clara por zonas: sin el degradado, el blanco se perdería sobre el
    portátil y el cuaderno.
    """
    return (
        '<div class="portada">'
        f'<img src="{{{{context_path}}}}/{nombre_img}" alt="{alt}">'
        '<div class="portada-texto">'
        f"{titulo_html}{subtitulo_html}"
        f'<div class="portada-datos">{datos_html}</div>'
        "</div></div>"
    )


def imagen(nombre, alt, ancho=None, alto=None, extra_estilo=""):
    dims = ""
    if ancho:
        dims += f' width="{ancho}"'
    if alto:
        dims += f' height="{alto}"'
    estilo = f' style="{extra_estilo}"' if extra_estilo else ""
    return f'<img src="{{{{context_path}}}}/{nombre}" alt="{alt}"{dims}{estilo}>'


def acordeon(secciones):
    """Efecto «Acordeón» del plugin exeeffects.

    Ojo: el JS del plugin (libs/exe_effects/exe_effects.js) enlaza cada título con su contenido
    por identificador — el título lleva href="#<id del contenido>" y un id del que el script
    deriva el contenedor a cerrar. Si no se reproduce su nomenclatura exacta, el clic no
    despliega nada (el contenido se queda en display:none). Formato verificado contra el plugin:
      contenedor: exe-accordion-<n>
      contenido : exe-accordion-<n>-<m>   (id del div de contenido)
      título    : id = el del contenido con los dos primeros guiones como guion bajo, + "-trigger"
    """
    n = 0
    partes = [f'<div class="exe-fx exe-accordion"><div id="exe-accordion-{n}">'
              '<div class="fx-accordion-section">']
    for m, (titulo, cuerpo) in enumerate(secciones):
        cid = f"exe-accordion-{n}-{m}"
        tid = cid.replace("-", "_", 2) + "-trigger"
        partes.append(
            f'<a class="fx-accordion-title fx-accordion-title-{m} fx-C1" '
            f'href="#{cid}" id="{tid}"><h2>{titulo}</h2></a>'
        )
        partes.append(f'<div class="fx-accordion-content" id="{cid}">{cuerpo}</div>')
    partes.append("</div></div></div>")
    return "".join(partes)


def lista_pasos_bold(contenido: str) -> str:
    """Convierte «**1. Título**<br>cuerpo...» en una lista ordenada."""
    marcas = list(re.finditer(r"\*\*(\d+)\.\s*(.+?)\*\*", contenido))
    if not marcas:
        return markdown_a_html(contenido)
    salida = ["<ol>"]
    for i, m in enumerate(marcas):
        inicio = m.end()
        fin = marcas[i + 1].start() if i + 1 < len(marcas) else len(contenido)
        cuerpo = contenido[inicio:fin]
        cuerpo = re.sub(r"^(?:<br\s*/?>)+", "", cuerpo, flags=re.I).strip()
        cuerpo = re.sub(r"(?:<br\s*/?>)+$", "", cuerpo, flags=re.I).strip()
        cuerpo_html = markdown_a_html(cuerpo) if cuerpo else ""
        salida.append(f"<li><strong>{m.group(2)}</strong>{cuerpo_html}</li>")
    salida.append("</ol>")
    return "".join(salida)


def partes_acordeon(contenido: str):
    """Devuelve (intro_html, [(titulo, html_seccion), ...])."""
    marcas = list(re.finditer(r"\*\*Sección\s+(\d+):\s*(.+?)\*\*", contenido))
    if not marcas:
        return markdown_a_html(contenido), []
    intro = contenido[: marcas[0].start()].strip()
    secciones = []
    for i, m in enumerate(marcas):
        inicio = m.end()
        fin = marcas[i + 1].start() if i + 1 < len(marcas) else len(contenido)
        cuerpo = contenido[inicio:fin]
        cuerpo = re.sub(r"^(?:<br\s*/?>)+", "", cuerpo, flags=re.I).strip()
        cuerpo = re.sub(r"(?:<br\s*/?>)+$", "", cuerpo, flags=re.I).strip()
        secciones.append((f"Sección {m.group(1)}: {m.group(2).strip()}", markdown_a_html(cuerpo)))
    return markdown_a_html(intro) if intro else "", secciones


# --------------------------------------------------------------------------- cuestionario

INSTRUCCION_QUIZ = ("Selecciona la respuesta correcta para cada pregunta. Hay 20 preguntas y "
                    "necesitas 14 correctas (el 70 %) para superar la evaluación.")
FEEDBACK_OK = "¡Correcto! Has entendido el concepto."
FEEDBACK_KO = "No es correcto. Repasa el contenido del nodo correspondiente e inténtalo de nuevo."


def parse_quiz(contenido: str):
    partes = re.split(r"\*\*Pregunta\s+(\d+):\*\*\s*", contenido)
    preguntas = []
    for i in range(1, len(partes), 2):
        numero = int(partes[i])
        cuerpo = partes[i + 1]
        lineas = [l.strip() for l in re.split(r"<br\s*/?>", cuerpo) if l.strip()]
        enunciado = ""
        opciones, solucion = [], None
        for linea in lineas:
            m = re.match(r"^([a-d])\)\s*(.*)$", linea)
            if m:
                texto = m.group(2).strip()
                if "[CORRECTA]" in texto:
                    texto = texto.replace("[CORRECTA]", "").strip()
                    solucion = len(opciones)
                opciones.append(re.sub(r"\*\*(.+?)\*\*", r"\1", texto))
            elif not opciones:
                enunciado = (enunciado + " " + linea).strip()
        preguntas.append({"n": numero, "enunciado": re.sub(r"\*\*(.+?)\*\*", r"\1", enunciado),
                          "opciones": opciones, "solucion": solucion})
    return preguntas


# --------------------------------------------------- actividades interactivas (revisión VII)
# La página de EJERCICIOS no se monta como texto: sus actividades van con iDevices nativos, que
# es lo que las hace interactivas. El guion las trae en su propia fila, con cuatro bloques:
#
#     **Bloque 1 — Test de práctica: <título>**
#     **Instrucción:** <una frase>
#     **Feedback correcto:** <una frase>
#     **Feedback incorrecto:** <una frase>
#     **Pregunta 1:** <enunciado>
#     a) <opción>
#     b) <opción> [CORRECTA]
#
#     **Bloque 2 — Respuesta abierta: <título>**
#     **Enunciado:** <lo que tiene que hacer el alumno>
#     **Retroalimentación:** <la respuesta modelo, comentada>
#
# «Test de práctica» -> iDevice Test NO evaluativo (se comprueba y explica, no puntúa).
# «Respuesta abierta» -> iDevice Texto con el botón de retroalimentación nativo.
RE_BLOQUE_ACTIVIDAD = re.compile(r"\*\*Bloque (\d+) — ([^:*]+):\s*(.*?)\*\*")
TIPOS_ACTIVIDAD = {"Test de práctica": "test", "Respuesta abierta": "abierta"}
INSTRUCCION_PRACTICA = ("Selecciona la respuesta correcta en cada caso. Puedes repetir la "
                        "actividad tantas veces como quieras: no cuenta para la evaluación.")
INSTRUCCION_RESPUESTA_ABIERTA = "Ver una posible respuesta"


def validar_preguntas(preguntas, maximo_opciones=4):
    """Comprobaciones de un test: opciones suficientes y exactamente una marcada [CORRECTA]."""
    problemas = []
    if not preguntas:
        problemas.append("no se ha detectado ninguna pregunta")
    for p in preguntas:
        if not (2 <= len(p["opciones"]) <= maximo_opciones):
            problemas.append(f"P{p['n']}: {len(p['opciones'])} opciones "
                             f"(se piden entre 2 y {maximo_opciones})")
        if p["solucion"] is None:
            problemas.append(f"P{p['n']}: ninguna opción marcada [CORRECTA]")
    return problemas


def parse_actividades(campo: str):
    """Convierte la fila «Actividades interactivas» en la lista de bloques a montar."""
    if not campo.strip():
        return []
    trozos = RE_BLOQUE_ACTIVIDAD.split(campo)
    if len(trozos) < 5:
        raise ValueError("la fila «Actividades interactivas» no tiene ningún bloque «**Bloque N — …**»")
    bloques = []
    for i in range(1, len(trozos), 4):
        numero, tipo, titulo, cuerpo = (trozos[i], trozos[i + 1].strip(),
                                        trozos[i + 2].strip(), trozos[i + 3])
        clase = TIPOS_ACTIVIDAD.get(tipo)
        if clase is None:
            raise ValueError(f"bloque {numero}: tipo desconocido {tipo!r}; "
                             f"los válidos son {sorted(TIPOS_ACTIVIDAD)}")
        if clase == "test":
            def campo_linea(nombre, defecto="", cuerpo=cuerpo):
                m = re.search(r"\*\*" + nombre + r":\*\*\s*(.*?)(?:<br|$)", cuerpo)
                return m.group(1).strip() if m else defecto

            instruccion = campo_linea("Instrucción", INSTRUCCION_PRACTICA)
            feedback_ok = campo_linea("Feedback correcto", FEEDBACK_OK)
            feedback_ko = campo_linea("Feedback incorrecto", FEEDBACK_KO)
            cuerpo_preguntas = re.sub(r"\*\*(Instrucción|Feedback correcto|Feedback incorrecto):\*\*"
                                      r"\s*(.*?)(?=<br|$)", "", cuerpo)
            preguntas = parse_quiz(cuerpo_preguntas)
            problemas = validar_preguntas(preguntas)
            if problemas:
                raise ValueError(f"bloque {numero} ({titulo}): " + "; ".join(problemas))
            bloques.append({"tipo": "test", "orden": int(numero), "titulo": titulo,
                            "instruccion": instruccion, "feedback_ok": feedback_ok,
                            "feedback_ko": feedback_ko, "preguntas": preguntas})
        else:
            # El enunciado llega hasta «**Retroalimentación:**», con el separador de <br> que use
            # el modelo (uno o dos): exigir un número exacto era una trampa innecesaria.
            m_ret = re.search(r"\*\*Retroalimentación:\*\*\s*(.*)$", cuerpo, re.DOTALL)
            m_env = re.search(r"\*\*Enunciado:\*\*\s*(.*?)\*\*Retroalimentación:\*\*", cuerpo,
                              re.DOTALL)
            if not (m_env and m_ret):
                raise ValueError(f"bloque {numero} ({titulo}): faltan «**Enunciado:**» o "
                                 f"«**Retroalimentación:**»")
            enunciado = re.sub(r"(?:<br\s*/?>|\s)+$", "", m_env.group(1)).strip()
            bloques.append({"tipo": "abierta", "orden": int(numero), "titulo": titulo,
                            "enunciado": enunciado,
                            "retro": m_ret.group(1).strip()})
    return bloques


def xor_encode(texto: str) -> str:
    """escape(XOR 146) de common.js: percent-encoding latin-1 del XOR."""
    xored = "".join(chr(ord(c) ^ XOR_KEY) for c in texto)
    return urllib.parse.quote(xored.encode("latin-1"), safe="")


# El payload del iDevice Test viaja cifrado en el HTML. Este patrón lo localiza para poder
# comprobar su texto en claro (informe de fidelidad) sin abrir el navegador.
RE_PAYLOAD_CIFRADO = re.compile(r'quext-DataGame js-hidden"?>([^<]+)<')


def componente_quiz(ts, usados, preguntas, titulo=None, instruccion=None, evaluativo=True,
                    evaluacion_id=None, feedback_ok=FEEDBACK_OK, feedback_ko=FEEDBACK_KO):
    """iDevice Test (`quick-questions`).

    `evaluativo=True` es la evaluación final: puntúa y lo comunica al LMS (`isScorm=1`).
    `evaluativo=False` es un test de práctica: el alumno se comprueba, pero la actividad no
    reporta nota (no entra en la evaluación del curso). Es el uso que pide la página de
    ejercicios: practicar con corrección inmediata sin que cuente para la calificación.
    """
    tpl = json.loads(JSON_PLANTILLA_QUIZ.read_text(encoding="utf-8"))
    idevice_id = oid(ts, nuevo_sufijo(usados))
    evaluacion_id = evaluacion_id or ("COPILOT10P" if evaluativo else "COPILOTPRACT")
    instruccion = instruccion or INSTRUCCION_QUIZ
    titulo = titulo or "Comprueba lo que has aprendido"

    game = {
        "asignatura": "", "author": "", "authorVideo": "", "typeGame": "QuExt",
        "endVideo": 0, "idVideo": "", "startVideo": 0,
        "instructionsExe": urllib.parse.quote(f"<p>{instruccion}</p>", safe=""),
        "instructions": instruccion,
        "showMinimize": False, "optionsRamdon": False, "answersRamdon": False,
        "showSolution": True, "timeShowSolution": 3,
        "useLives": False, "numberLives": 1,
        "itinerary": {"showClue": False, "clueGame": "", "percentageClue": 0,
                      "showCodeAccess": False, "codeAccess": "", "messageCodeAccess": ""},
        "customMessages": True, "customScore": False,
        "evaluation": evaluativo, "evaluationID": evaluacion_id,
        "feedBack": True, "gameMode": 0, "id": idevice_id, "isScorm": 1 if evaluativo else 0,
        "msgs": tpl["msgs"],
        # percentajeQuestions = % de preguntas que se muestran (100 = las 10 del guion).
        # OJO: no es la nota de corte. La nota de corte la aplica la política SCORM 1.2
        # leyendo cmi.student_data.mastery_score del LMS (por defecto 50 si el LMS no la publica).
        "percentajeFB": 100, "percentajeQuestions": 100, "repeatActivity": True,
        "textAfter": "", "textButtonScorm": "Guardar puntuación", "textFeedBack": "",
        "title": titulo, "useLives": False, "version": 2,
        "weighted": 100,
        "questionsGame": [],
    }
    for p in preguntas:
        game["questionsGame"].append({
            "type": 0, "time": 0, "numberOptions": len(p["opciones"]), "x": 0, "y": 0,
            "author": "", "alt": "", "customScore": 1,
            "url": "", "audio": "", "soundVideo": 1, "imageVideo": 1, "iVideo": 0,
            "fVideo": 0, "silentVideo": 0, "tSilentVideo": 0, "eText": "",
            "quextion": p["enunciado"], "options": p["opciones"], "solution": p["solucion"],
            "msgHit": feedback_ok, "msgError": feedback_ko,
        })

    payload = xor_encode(json.dumps(game, ensure_ascii=False))
    html_view = (tpl["htmlView_tpl"]
                 .replace("__PAYLOAD__", payload)
                 .replace("__INSTR__", instruccion)
                 .replace("__IDEVICEID__", idevice_id)
                 .replace("__EVALUATIONID__", evaluacion_id))
    textarea = (tpl["textTextarea_tpl"]
                .replace("__PAYLOAD__", payload)
                .replace("__INSTR__", instruccion)
                .replace("__IDEVICEID__", idevice_id))
    props = {
        "ideviceId": idevice_id,
        "textInfoDurationInput": "", "textInfoDurationTextInput": "Duración",
        "textInfoParticipantsInput": "", "textInfoParticipantsTextInput": "Agrupamiento",
        "textTextarea": textarea,
        "textFeedbackInput": "Mostrar retroalimentación", "textFeedbackTextarea": "",
    }
    return {"tipo": "quick-questions", "id": idevice_id, "htmlView": html_view,
            "jsonProperties": json.dumps(props, ensure_ascii=False)}


# --------------------------------------------------------------------------- guion

def extraer_nodos():
    texto = GUION.read_text(encoding="utf-8")
    partes = re.split(r"(?m)^### NODO ", texto)
    nodos = []
    for p in partes[1:]:
        cabecera = p.split("\n", 1)[0]
        fila = lambda n: re.search(r"(?m)^\|\s*\*\*" + n + r"\*\*\s*\|(.*?)\|\s*$", p)
        num, _, titulo = cabecera.partition("—")
        m = fila("Contenido en pantalla")
        notas_m = fila("Notas de producción")
        recuadro_m = fila("Recuadro de ideas clave")
        actividades_m = fila("Actividades interactivas")
        notas = notas_m.group(1).strip() if notas_m else ""
        # Nodo 14: el guion dice en las notas qué texto lleva la Nota (mensaje clave entre «»)
        clave = ""
        if "mensaje clave" in notas:
            resto = notas.split("mensaje clave", 1)[1]
            cita = re.search(r"«([^»]{20,})»", resto)
            if cita:
                clave = cita.group(1).strip()
        nodos.append({
            "nodo": int(num.strip()),
            "titulo_guion": titulo.strip(),
            "notas": notas,
            "mensaje_clave": clave,
            "contenido": (m.group(1) if m else "").strip(),
            "recuadro": (recuadro_m.group(1) if recuadro_m else "").strip(),
            "actividades_texto": (actividades_m.group(1) if actividades_m else "").strip(),
        })
    # nombres del sitemap (§2). Dos formas en el guion:
    #   «N. **NOMBRE** — descripción»      (la descripción va fuera del énfasis)
    #   «N. **MÓDULO x — Título**»         (el guion va dentro del énfasis: es parte del nombre)
    sitemap = {}
    sec2 = re.search(r"(?ms)^## 2\. ESTRUCTURA.*?^## 3\.", texto)
    if sec2:
        for m in re.finditer(r"(?m)^(\d{1,2})\.\s+(.+)$", sec2.group(0)):
            linea = m.group(2).strip()
            m_desc = re.match(r"^\*\*(.+?)\*\*\s*—\s*(.*)$", linea)
            m_solo = re.match(r"^\*\*(.+)\*\*$", linea)
            if m_desc:
                nombre = m_desc.group(1).strip()
            elif m_solo:
                nombre = m_solo.group(1).strip()
            else:
                nombre = re.sub(r"\*\*(.+?)\*\*", r"\1", linea).strip()
            sitemap[int(m.group(1))] = nombre
    # «EJERCICIOS» queda fuera del curso (decisión del autor, revisión IV).
    excluidos = {x.strip().upper() for x in NODOS_EXCLUIDOS}
    nodos = [n for n in nodos
             if (sitemap.get(n["nodo"]) or n["titulo_guion"]).strip().upper() not in excluidos]
    for i, n in enumerate(nodos, start=1):
        n["orden"] = i
    for n in nodos:
        nombre = sitemap.get(n["nodo"]) or n["titulo_guion"]
        # el título va sin la etiqueta decorativa «MÓDULO x —»
        n["titulo_pagina"] = re.sub(r"^MÓDULO\s+\d+\s*—\s*", "", nombre).strip()
        # menú lateral: el número de página seguido inmediatamente del título
        n["pageName"] = f'{n["orden"]}. {n["titulo_pagina"]}'
    return nodos


# --------------------------------------------------------------------------- montaje por nodo

# --------------------------------------------------------------------------- claves de página
# El despacho de iDevices es por CLAVE (el título del nodo en el guion), no por número: así se
# pueden insertar o reordenar páginas sin tocar la lógica de montaje. `CLAVES_CONOCIDAS` sirve de
# red de seguridad: si una clave no coincide, main() avisa en vez de montar una página vacía.

C_PORTADA = "PORTADA DEL CURSO"
C_INDICE = "ÍNDICE Y OBJETIVOS"
C_MAPA_IA = "¿QUÉ ES LA IA? DE LA IA AL AGENTE"
C_LIMITES = "QUÉ PUEDE Y QUÉ NO PUEDE HACER LA IA"
C_AGENTE = "¿QUÉ ES UN AGENTE DE IA?"
C_ENTORNOS = "COPILOT WEB Y COPILOT DE TRABAJO"
C_COMPONENTES = "LOS 5 COMPONENTES DEL AGENTE"
C_TIPOS = "LOS TIPOS DE AGENTE DE MICROSOFT"
C_CICLO = "EL CICLO DE TRABAJO DEL AGENTE"
C_WORD = "COPILOT EN WORD, OUTLOOK Y ONENOTE"
C_EXCEL = "COPILOT EN EXCEL, POWERPOINT Y TEAMS"
C_SHAREPOINT = "COPILOT EN SHAREPOINT, LOOP Y PLANIFICACIÓN"
C_AGENT_BUILDER = "CREAR TU PROPIO AGENTE CON AGENT BUILDER"
C_INVENTARIO = "EL INVENTARIO DE IA DE TU EMPRESA"
C_INSTRUCCIONES = "CÓMO ESCRIBIR BUENAS INSTRUCCIONES"
C_PRACTICAS = "BUENAS PRÁCTICAS"
C_RIESGOS = "RIESGOS Y LÍMITES"
C_SOBREEXPOSICION = "PERMISOS, SOBREEXPOSICIÓN Y SHADOW AI"
C_POLITICA = "POLÍTICA DE USO Y PROTOCOLO DE INCIDENTES"
C_AI_ACT = "EL AI ACT EN TÉRMINOS SIMPLES"
C_ART4 = "ARTÍCULO 4: QUÉ TE OBLIGA Y QUÉ DEBES PODER DEMOSTRAR"
C_DATOS = "DATOS PERSONALES, DERECHOS Y SUPERVISIÓN HUMANA"
C_EJERCICIOS = "EJERCICIOS PRÁCTICOS"
C_QUIZ = "EVALUACIÓN FINAL"
C_RESUMEN = "RESUMEN, GLOSARIO Y RECURSOS"

CLAVES_CONOCIDAS = {
    C_PORTADA, C_INDICE, C_MAPA_IA, C_LIMITES, C_AGENTE, C_ENTORNOS, C_COMPONENTES, C_TIPOS,
    C_CICLO, C_WORD, C_EXCEL, C_SHAREPOINT, C_AGENT_BUILDER, C_INVENTARIO, C_INSTRUCCIONES,
    C_PRACTICAS, C_RIESGOS, C_SOBREEXPOSICION, C_POLITICA, C_AI_ACT, C_ART4, C_DATOS,
    C_EJERCICIOS, C_QUIZ, C_RESUMEN,
}

# Textos alternativos de los diagramas (accesibilidad, regla del guion: cada imagen lleva el suyo).
ALT_IA_AL_AGENTE = ("Diagrama en cuatro filas numeradas, de lo más general a lo más concreto: la "
                    "inteligencia artificial, la IA generativa, los modelos de lenguaje y los "
                    "agentes de IA, con una descripción breve en cada fila")
ALT_NIVELES_RIESGO = ("Diagrama de cuatro bandas de color, de más a menos restrictiva: riesgo "
                      "inaceptable o prohibido, alto riesgo, riesgo limitado y riesgo mínimo, con un "
                      "ejemplo en cada banda")
ALT_SOBREEXPOSICION = ("Diagrama comparativo: con permisos abiertos en SharePoint, Copilot muestra "
                       "a cualquier persona documentos confidenciales; con los permisos revisados, "
                       "Copilot solo muestra lo que corresponde a cada persona")


def clave_de_nodo(nodo):
    """Clave de despacho: título del nodo en el guion, normalizado."""
    return (nodo.get("titulo_guion") or "").strip().upper()


def _imagen_centrada(nombre, alt, ancho, alto):
    """Imagen de nodo, centrada en la columna de texto."""
    return imagen(nombre, alt, ancho, alto, "display:block;margin:0 auto;")


def _fragmentos_con_nota(c, marca, icono="icono_nota.png", alt="Nota"):
    """Divide el contenido en dos: hasta `marca` y desde `marca` (este con el icono delante).

    Las notas del guion se escriben con «>» (cita destacada); el icono es el filo de la nota.
    Si la marca no aparece, devuelve la página entera sin nota (no rompe el montaje).
    """
    if marca not in c:
        return [markdown_a_html(c)]
    corte = c.index(marca)
    return [markdown_a_html(c[:corte]),
            f'<p>{imagen(icono, alt, 32, 32)}</p>' + markdown_a_html(c[corte:])]


def componentes_de_nodo(nodo, ts, usados):
    """Devuelve los iDevices del nodo.

    Los fragmentos de texto se acumulan en `textos` y se emiten como UN ÚNICO iDevice Texto
    (un solo bloque por página). `otros` son los iDevices que no son Texto (el cuestionario).
    """
    clave = clave_de_nodo(nodo)
    c = nodo["contenido"]
    textos = []
    otros = []

    def texto(html):
        textos.append(html)

    if clave == C_PORTADA:
        # Portada: la imagen con el título superpuesto (overlay) y, debajo, la introducción.
        i_h2 = c.index("## ")
        i_intro = c.index("Un recorrido práctico")
        i_datos = c.index("**Duración:**")
        titulo = re.sub(r"^#+\s*", "", c[:i_h2].strip())
        subtitulo = re.sub(r"^#+\s*", "", c[i_h2:i_intro].strip())
        texto(portada_con_overlay(
            "portada_curso_copilot.jpg",
            f'<h2 class="portada-titulo">{en_linea(titulo)}</h2>',
            f'<p class="portada-subtitulo">{en_linea(subtitulo)}</p>',
            markdown_a_html(c[i_datos:]).strip(),
        ))
        texto(markdown_a_html(c[i_intro:i_datos]))

    elif clave == C_INDICE:
        corte = c.index("### Objetivos del curso")
        texto(markdown_a_html(c[:corte]))
        texto(markdown_a_html(c[corte:]))

    elif clave == C_MAPA_IA:
        # Página nueva (revisión VI): mapa conceptual IA -> IA generativa -> LLM -> agente.
        texto(_imagen_centrada("diagrama_ia_al_agente.png", ALT_IA_AL_AGENTE, 640, 400))
        texto(markdown_a_html(c))

    elif clave in (C_LIMITES, C_INVENTARIO, C_POLITICA, C_ART4, C_DATOS):
        # Páginas con una Nota destacada al final (marca «> **Nota:**» del guion).
        for frag in _fragmentos_con_nota(c, "> **Nota:**"):
            texto(frag)

    elif clave == C_EJERCICIOS:
        # Página de prácticas (revisión VII). «Contenido en pantalla» trae la introducción; las
        # actividades van en su propia fila y se montan con iDevices nativos e interactivos:
        #   Test de práctica     -> iDevice Test no evaluativo (corrige y explica, no puntúa)
        #   Respuesta abierta    -> iDevice Texto con el botón de retroalimentación nativo
        texto(markdown_a_html(c))
        for activ in parse_actividades(nodo.get("actividades_texto") or ""):
            if activ["tipo"] == "test":
                otros.append(componente_quiz(
                    ts, usados, activ["preguntas"], titulo=activ["titulo"],
                    instruccion=activ["instruccion"], evaluativo=False,
                    evaluacion_id=f"COPILOTPRACT{activ['orden']}",
                    feedback_ok=activ["feedback_ok"], feedback_ko=activ["feedback_ko"]))
            else:
                otros.append(componente_texto(
                    ts, usados,
                    f'<h3>{en_linea(activ["titulo"])}</h3>' + markdown_a_html(activ["enunciado"]),
                    feedback_titulo=INSTRUCCION_RESPUESTA_ABIERTA,
                    feedback_texto=markdown_a_html(activ["retro"])))

    elif clave == C_AGENTE:
        for frag in _fragmentos_con_nota(c, "> **Definición clave:**"):
            texto(frag)

    elif clave == C_ENTORNOS:
        corte = c.index("**Tabla de entornos:**")
        texto(markdown_a_html(c[:corte]))
        texto(markdown_a_html(c[corte:]))

    elif clave in (C_COMPONENTES, C_TIPOS, C_INSTRUCCIONES, C_AI_ACT):
        intro, secciones = partes_acordeon(c)
        if clave == C_COMPONENTES:
            # imagen de entrada del nodo, antes del acordeón (fila «Recurso gráfico»)
            intro = _imagen_centrada(
                "diagrama_5_componentes.png",
                "Diagrama: en el centro el agente de IA y, a su alrededor, numerados, "
                "sus cinco componentes — percepción, razonamiento, herramientas, memoria "
                "y comunicación", 640, 512) + intro
        elif clave == C_AI_ACT:
            intro = _imagen_centrada("diagrama_niveles_riesgo.png", ALT_NIVELES_RIESGO, 640, 400) + intro
        texto(intro)
        if clave == C_INSTRUCCIONES:
            secciones = [(t, _marcar_mal_bien(b)) for t, b in secciones]
        texto(acordeon(secciones))

    elif clave == C_CICLO:
        corte = c.index("**1. Recibir la orden**")
        texto(_imagen_centrada(
            "diagrama_ciclo_5_pasos.png",
            "Diagrama circular con los cinco pasos del ciclo de trabajo, unidos por flechas: "
            "recibir la orden, planificar, ejecutar, verificar y entregar", 640, 640)
            + markdown_a_html(c[:corte]))
        texto(lista_pasos_bold(c[corte:]))

    elif clave == C_AGENT_BUILDER:
        corte1 = c.index("> **Pasos para crear un agente:**")
        corte2 = c.index("> **Nota:**")
        texto(markdown_a_html(c[:corte1]))
        texto(markdown_a_html(c[corte1:corte2]))
        texto(f'<p>{imagen("icono_nota.png", "Nota", 32, 32)}</p>' + markdown_a_html(c[corte2:]))

    elif clave == C_PRACTICAS:
        for frag in _fragmentos_con_nota(c, "**Conoce las políticas de tu empresa**"):
            texto(frag)

    elif clave == C_RIESGOS:
        # El mensaje clave del nodo está en el campo «Notas de producción» del guion, que es donde
        # el guion dice qué lleva la Nota. Se extrae literalmente de ahí.
        texto(markdown_a_html(c))
        mensaje = nodo.get("mensaje_clave") or ""
        texto(f'<p>{imagen("icono_warning.png", "Aviso", 32, 32)}</p>'
              f'<blockquote><p>{en_linea(mensaje)}</p></blockquote>')

    elif clave == C_SOBREEXPOSICION:
        # Página nueva (revisión VI): el riesgo específico de un cliente que solo usa Microsoft 365.
        texto(_imagen_centrada("diagrama_sobreposicion.png", ALT_SOBREEXPOSICION, 640, 400))
        for frag in _fragmentos_con_nota(c, "> **Nota:**", "icono_warning.png", "Aviso"):
            texto(frag)

    elif clave == C_QUIZ:
        otros.append(componente_quiz(ts, usados, parse_quiz(c)))

    elif clave == C_RESUMEN:
        # Crédito obligatorio (regla 6 del guion): al final del bloque «¿Quieres seguir aprendiendo?»,
        # que es el último contenido del nodo.
        html = markdown_a_html(c)
        texto(html + "\n<p><em>Imagen de portada: Jakub Zerdzicki / Pexels</em></p>")

    else:
        # Páginas de texto plano: aplicaciones en Word/Excel/SharePoint, inventario de IA,
        # artículo 4 y ejercicios prácticos.
        texto(markdown_a_html(c))

    # Recuadro de ideas clave (revisión VII): si el guion lo define para esta página, entra en el
    # punto exacto que indica la fila (al final del bloque citado). El texto no se reparte ni se
    # inventa aquí: se inserta tal cual en el flujo del iDevice único.
    campo_recuadro = (nodo.get("recuadro") or "").strip()
    if campo_recuadro and any(t.strip() for t in textos):
        ancla, caja = _caja_html(campo_recuadro)
        textos[:] = [insertar_recuadro("\n".join(textos), ancla, caja)]

    # Un solo iDevice Texto por página: se concatenan todos los fragmentos.
    comps = []
    if any(t.strip() for t in textos):
        comps.append(componente_texto(ts, usados, "\n".join(textos)))
    comps.extend(otros)
    return comps


def _marcar_mal_bien(html: str) -> str:
    """Nodo de instrucciones: marca los ejemplos «Mal» (aspa) y «Bien» (señal correcta)."""
    html = re.sub(r"<p>Mal:", f'<p>{imagen("icono_cross.png", "Incorrecto", 20, 20)} Mal:', html)
    html = re.sub(r"<p>Bien:", f'<p>{imagen("icono_check.png", "Correcto", 20, 20)} Bien:', html)
    return html


# --------------------------------------------------------------------------- content.xml

def bloque(nombre, componente, ts, usados, page_id):
    block_id = oid(ts, nuevo_sufijo(usados))
    return f"""          <odePagStructure>
            <odePageId>{page_id}</odePageId>
            <odeBlockId>{block_id}</odeBlockId>
            <blockName>{xml_escape(nombre)}</blockName>
            <iconName></iconName>
            <odePagStructureOrder>1</odePagStructureOrder>
            <odePagStructureProperties>
              <odePagStructureProperty><key>visibility</key><value>true</value></odePagStructureProperty>
              <odePagStructureProperty><key>teacherOnly</key><value>false</value></odePagStructureProperty>
              <odePagStructureProperty><key>allowToggle</key><value>true</value></odePagStructureProperty>
              <odePagStructureProperty><key>minimized</key><value>false</value></odePagStructureProperty>
            </odePagStructureProperties>
            <odeComponents>
              <odeComponent>
                <odePageId>{page_id}</odePageId>
                <odeBlockId>{block_id}</odeBlockId>
                <odeIdeviceId>{componente['id']}</odeIdeviceId>
                <odeIdeviceTypeName>{componente['tipo']}</odeIdeviceTypeName>
                <htmlView>{cdata(componente['htmlView'])}</htmlView>
                <jsonProperties>{cdata(componente['jsonProperties'])}</jsonProperties>
                <odeComponentsOrder>1</odeComponentsOrder>
                <odeComponentsProperties>
                  <odeComponentsProperty><key>visibility</key><value>true</value></odeComponentsProperty>
                  <odeComponentsProperty><key>teacherOnly</key><value>false</value></odeComponentsProperty>
                  <odeComponentsProperty><key>identifier</key><value></value></odeComponentsProperty>
                  <odeComponentsProperty><key>cssClass</key><value></value></odeComponentsProperty>
                </odeComponentsProperties>
              </odeComponent>
            </odeComponents>
          </odePagStructure>"""


def construir_content_xml(nodos, ts, usados):
    ode_id = oid(ts, nuevo_sufijo(usados))
    ode_version = oid(ts, nuevo_sufijo(usados))
    paginas = []

    for nodo in nodos:
        comps = componentes_de_nodo(nodo, ts, usados)
        page_id = oid(ts, nuevo_sufijo(usados))
        # Bloques SIN nombre: sin la etiqueta «Texto» y sin la caja que la acompaña.
        bloques = "\n".join(bloque("", x, ts, usados, page_id) for x in comps)
        prop_extra = ""
        if nodo["nodo"] == 1:
            prop_extra = ("\n          <odeNavStructureProperty><key>hidePageTitle</key>"
                          "<value>true</value></odeNavStructureProperty>")
        paginas.append(f"""    <odeNavStructure>
      <odePageId>{page_id}</odePageId>
      <odeParentPageId></odeParentPageId>
      <pageName>{xml_escape(nodo['pageName'])}</pageName>
      <odeNavStructureOrder>{nodo['orden']}</odeNavStructureOrder>
      <odeNavStructureProperties>
        <odeNavStructureProperty><key>titlePage</key><value>{xml_escape(nodo['titulo_pagina'])}</value></odeNavStructureProperty>{prop_extra}
      </odeNavStructureProperties>
      <odePagStructures>
{bloques}
      </odePagStructures>
    </odeNavStructure>""")

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE ode SYSTEM "content.dtd">
<ode xmlns="http://www.intef.es/xsd/ode" version="2.0">
  <userPreferences>
    <userPreference>
      <key>theme</key>
      <value>{TEMA}</value>
    </userPreference>
  </userPreferences>
  <odeResources>
    <odeResource><key>odeId</key><value>{ode_id}</value></odeResource>
    <odeResource><key>odeVersionId</key><value>{ode_version}</value></odeResource>
    <odeResource><key>exe_version</key><value>3.0</value></odeResource>
  </odeResources>
  <odeProperties>
    <odeProperty><key>pp_title</key><value>Agentes de IA y Microsoft Copilot para tu día a día</value></odeProperty>
    <odeProperty><key>pp_lang</key><value>es</value></odeProperty>
    <odeProperty><key>pp_author</key><value></value></odeProperty>
    <odeProperty><key>pp_addExeLink</key><value>true</value></odeProperty>
    <odeProperty><key>pp_extraHeadContent</key><value>{xml_escape(ESTILOS_PROPIOS)}</value></odeProperty>
  </odeProperties>
  <odeNavStructures>
{chr(10).join(paginas)}
  </odeNavStructures>
</ode>
"""


# --------------------------------------------------------------------------- fidelidad de textos

def texto_plano(s: str) -> str:
    """Normaliza para comparar: quita etiquetas, marcado y numeración automática."""
    s = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", s)          # enlaces markdown
    s = re.sub(r"<[^>]+>", " ", s)                            # etiquetas HTML
    s = s.replace("{{context_path}}", " ")
    for ch in "*#|>_-":
        s = s.replace(ch, " ")
    s = re.sub(r"\d+", " ", s)                                # cifras (numeración de listas)
    s = re.sub(r"\s+", " ", s)
    return s.strip().lower()


def significativas(s: str):
    return {w for w in re.findall(r"[a-záéíóúüñ]{3,}", texto_plano(s))}


# Etiquetas de la fila «Actividades interactivas»: son instrucciones de montaje, no texto de la
# página (igual que la línea «POSICIÓN:» del recuadro). Se quitan antes de comparar.
ETIQUETAS_ACTIVIDADES = re.compile(
    r"\*\*Bloque \d+ — [^*]*\*\*"                       # **Bloque 2 — Respuesta abierta: <título>**
    r"|\*\*(?:Instrucción|Feedback correcto|Feedback incorrecto|Pregunta \d+|"
    r"Enunciado|Retroalimentación):\*\*"
    r"|\[CORRECTA\]")


def texto_actividades(campo: str) -> str:
    """Texto de las actividades sin sus etiquetas de montaje («**Bloque 2 — Test de práctica:**»,
    «**Retroalimentación:**», «[CORRECTA]»): lo que de verdad tiene que verse en la página."""
    return ETIQUETAS_ACTIVIDADES.sub(" ", campo)


def texto_cifrados(html: str) -> str:
    """Texto en claro que va dentro de los iDevice Test (payload cifrado XOR + urlencode).

    La página de ejercicios monta sus tests con el iDevice nativo, que guarda las preguntas
    cifradas: si la comprobación de fidelidad solo mirara el HTML visible, daría por perdido un
    texto que sí está en la página (y al revés: no vería un texto que se hubiera colado ahí).
    """
    trozos = []
    for m in RE_PAYLOAD_CIFRADO.finditer(html):
        raw = urllib.parse.unquote_to_bytes(m.group(1))
        claro = "".join(chr(b ^ XOR_KEY) for b in raw)
        try:
            trozos.append(_todas_las_cadenas(json.loads(claro)))
        except json.JSONDecodeError:
            trozos.append(claro)
    return " ".join(trozos)


def _todas_las_cadenas(obj) -> str:
    if isinstance(obj, str):
        return obj
    if isinstance(obj, dict):
        return " ".join(_todas_las_cadenas(v) for v in obj.values())
    if isinstance(obj, (list, tuple)):
        return " ".join(_todas_las_cadenas(v) for v in obj)
    return ""


def informe_fidelidad(nodos):
    print("\n=== FIDELIDAD DE TEXTOS (guion -> HTML generado) ===")
    problemas = 0
    for nodo in nodos:
        if clave_de_nodo(nodo) == C_QUIZ:
            continue  # el cuestionario se verifica aparte
        comps = componentes_de_nodo(nodo, "20260912220000", set())
        # Todos los componentes, no solo el iDevice de texto: la página de ejercicios monta sus
        # actividades con iDevices interactivos y su texto también cuenta.
        gen = " ".join(x["htmlView"] for x in comps)
        gen = gen + " " + texto_cifrados(gen)
        # El recuadro de ideas clave también es texto del guion: entra en la comprobación. La
        # línea «POSICIÓN:» no, porque es una instrucción de montaje.
        fuente = (nodo["contenido"] + " " + texto_recuadro(nodo.get("recuadro") or "")
                  + " " + texto_actividades(nodo.get("actividades_texto") or ""))
        faltan = sorted(significativas(fuente) - significativas(gen))
        if faltan:
            problemas += 1
            print(f"  NODO {nodo['nodo']:>2}: FALTAN {len(faltan)} -> {faltan[:15]}")
        else:
            print(f"  NODO {nodo['nodo']:>2}: completo ({len(significativas(nodo['contenido']))} terminos)")
    if not problemas:
        print("  Todos los nodos de texto: el texto del guion aparece completo en el HTML.")


def informe_quiz(nodo):
    print("\n=== CUESTIONARIO (evaluación final) ===")
    preguntas = parse_quiz(nodo["contenido"])
    print(f"  Preguntas detectadas: {len(preguntas)} (el guion pide 20)")
    ok = len(preguntas) == 20
    for p in preguntas:
        cuatro = len(p["opciones"]) == 4
        marcada = p["solucion"] is not None
        if not (cuatro and marcada):
            ok = False
        print(f"    P{p['n']:>2}: {len(p['opciones'])} opciones, correcta -> "
              f"{p['solucion']} ({'ok' if cuatro and marcada else 'REVISAR'})")
    # comprobación del cifrado: nuestro codificador debe poder descifrarse
    comp = componente_quiz("20260912220000", set(), preguntas)
    payload = re.search(r'quext-DataGame js-hidden"?>([^<]+)<', comp["htmlView"]).group(1)
    raw = urllib.parse.unquote_to_bytes(payload)
    claro = "".join(chr(b ^ XOR_KEY) for b in raw)
    datos = json.loads(claro)
    estado_ok = (datos["percentajeQuestions"] == 100 and datos["isScorm"] == 1
                 and datos["evaluation"] is True and len(datos["questionsGame"]) == 20
                 and all(q["customScore"] == 1 for q in datos["questionsGame"]))
    print(f"  Payload cifrado: descifra correctamente -> {estado_ok}")
    print(f"  Nota de corte: {datos['percentajeQuestions']}% | SCORM: {datos['isScorm']} | "
          f"preguntas: {len(datos['questionsGame'])} | msgs: {len(datos['msgs'])}")
    print(f"  Feedback por pregunta: {datos['questionsGame'][0]['msgHit']!r} / "
          f"{datos['questionsGame'][0]['msgError']!r}")
    return ok and estado_ok


# --------------------------------------------------------------------------- main

def main():
    check = "--check" in sys.argv
    ts = datetime.now().strftime("%Y%m%d%H%M%S")
    usados = set()
    random.seed(20260912)

    nodos = extraer_nodos()
    if len(nodos) != NODOS_ESPERADOS:
        print(f"AVISO: se esperaban {NODOS_ESPERADOS} nodos y se han extraido {len(nodos)}")
    # Red de seguridad del despacho por clave: si un título del guion no coincide con ninguna
    # clave conocida, la página caería en el montaje genérico (y el cuestionario, por ejemplo,
    # se perdería en silencio). Mejor avisar.
    desconocidas = sorted({clave_de_nodo(n) for n in nodos} - CLAVES_CONOCIDAS)
    if desconocidas:
        print(f"AVISO: claves de nodo NO reconocidas (se montaran como texto plano): {desconocidas}")
    for n in nodos:
        if not n["contenido"]:
            print(f"AVISO: el nodo {n['nodo']} no tiene contenido extraido")

    try:
        xml = construir_content_xml(nodos, ts, usados)
    except ValueError as exc:
        print(f"FALLO DE MONTAJE: {exc}")
        return 1
    SALIDA.mkdir(parents=True, exist_ok=True)
    (SALIDA / "content.xml").write_text(xml, encoding="utf-8")
    # el CSS propio, en un fichero aparte, para que el post-proceso lo inyecte donde haga falta
    ELPX_MINIMO.parent.mkdir(parents=True, exist_ok=True)
    (ELPX_MINIMO.parent / "estilos_propios.html").write_text(ESTILOS_PROPIOS, encoding="utf-8")

    # DTD y XSD oficiales (desde el contenedor)
    for fichero in ("content.dtd", "ode-content.xsd"):
        destino = SALIDA / fichero
        if not destino.exists():
            subprocess.run(["podman", "cp", f"exelearning:/app/public/app/schemas/ode/{fichero}",
                            str(destino)], check=True)

    # validación
    r1 = subprocess.run(["xmllint", "--noout", "--dtdvalid", str(SALIDA / "content.dtd"),
                         str(SALIDA / "content.xml")], capture_output=True, text=True)
    r2 = subprocess.run(["xmllint", "--noout", "--schema", str(SALIDA / "ode-content.xsd"),
                         str(SALIDA / "content.xml")], capture_output=True, text=True)
    print("Validacion DTD:", "OK" if r1.returncode == 0 else "FALLO\n" + r1.stderr[:2000])
    print("Validacion XSD:", "OK" if r2.returncode == 0 else "FALLO\n" + r2.stderr[:2000])

    # empaquetado (mínimo re-importable: content.xml + content.dtd + recursos)
    elpx = ELPX_MINIMO
    elpx.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(elpx, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(SALIDA / "content.xml", "content.xml")
        z.write(SALIDA / "content.dtd", "content.dtd")
        for img in sorted(IMGS.iterdir()):
            if img.name == "CREDITOS.md":
                continue
            if img.suffix.lower() in (".png", ".jpg") and img.name in IMAGENES_USADAS:
                z.write(img, f"content/resources/{img.name}")
    print(f"\nPaquete intermedio: {elpx} ({elpx.stat().st_size} bytes)")

    with zipfile.ZipFile(elpx) as z:
        print("Contenido:", ", ".join(z.namelist()))

    n_componentes = xml.count("<odeComponent>")
    print(f"\nNodos: {xml.count('<odeNavStructure>')} | Bloques: {xml.count('<odePagStructure>')} "
          f"| Componentes: {n_componentes}")
    print("Tipos:", {t: xml.count(f"<odeIdeviceTypeName>{t}</odeIdeviceTypeName>")
                     for t in ("text", "quick-questions")})

    if check:
        informe_fidelidad(nodos)
        informe_quiz(next(n for n in nodos if clave_de_nodo(n) == C_QUIZ))
    return 0


IMAGENES_USADAS = {
    "portada_curso_copilot.jpg", "diagrama_5_componentes.png", "diagrama_ciclo_5_pasos.png",
    "diagrama_ia_al_agente.png", "diagrama_niveles_riesgo.png", "diagrama_sobreposicion.png",
    "icono_nota.png", "icono_warning.png", "icono_check.png", "icono_cross.png",
}

if __name__ == "__main__":
    raise SystemExit(main())
