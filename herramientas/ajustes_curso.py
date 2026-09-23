#!/usr/bin/env python3
"""Ajustes del curso exportado (menú lateral con memoria, test como evaluación y avisos).

Se aplica sobre los HTML **ya exportados** (un directorio descomprimido o un zip: `.elpx`, SCORM
1.2 o HTML5) sin regenerar nada y sin abrir el navegador. Es idempotente: si ya está hecho, no
toca nada.

Qué cambia

 1. **Menú lateral con memoria.** Cada página del export es un documento nuevo, así que el panel
    de navegación (`#siteNav > ul`, que es el que scrollea) vuelve al principio al clicar una
    entrada de abajo y se pierde el punto de lectura. Un script pequeño guarda la posición en
    `sessionStorage` y la restaura; si no hay posición guardada (primera visita o enlace directo),
    deja visible la página activa.

 2. **El test se comporta como evaluación, no como juego.** El iDevice `quick-questions` viene
    configurado en el modo «arcade» (`gameMode: 0`): cada acierto vale 1000 puntos + 10 por cada
    segundo que quede en el cronómetro, y cada fallo resta 330. Eso hace que la «Puntuación» que ve
    el alumno (p. ej. 17040) dependa de la velocidad de respuesta y no guarde relación con la nota.
    Aquí se reescribe, dentro del payload cifrado de cada actividad:
      - `gameMode: 1`  -> cada acierto vale 10/total (con 20 preguntas, 0,50), así que la
        «Puntuación» que se muestra es la nota sobre 10: la misma que ya se guarda en el informe
        del curso y la que usa el veredicto del 70 %. No depende del reloj, y los fallos no restan
        (con `gameMode: 2` tampoco dependían, pero el iDevice esconde los valores del marcador y
        quedan las etiquetas «Aciertos: · Errores:» vacías);
      - `percentajeFB: 0` -> se desactiva el aviso «Necesita al menos un 100 % de respuestas
        correctas para conseguir la información. Vuelva a intentarlo.», que en este curso no
        aplica (el umbral real, el 70 %, lo dice el enunciado de la evaluación);
      - `time: 5` -> 600 s por pregunta (índice 5 de la tabla de tiempos del iDevice). Con los 15 s
        originales, si el tiempo se agotaba la pregunta se saltaba EN SILENCIO: no contaba como
        acierto ni como error, así que la puntuación se calculaba sobre preguntas no respondidas.

 3. **CSS de los avisos.** El bloque de retroalimentación del test viaja vacío en este curso (el
    feedback va dentro de cada respuesta), y el aviso «La puntuación no se puede guardar porque
    esta página no forma parte de un paquete SCORM» solo tiene sentido en el paquete SCORM. Se
    ocultan en la web autocontenida y en el `.elpx` (en el paquete SCORM el `body` lleva la clase
    `exe-scorm` y el aviso se conserva).

 4. **Veredicto del curso (70 %).** El marcador del curso da la actividad por superada a partir de
    5 sobre 10, mientras el curso pide un 70 % (14 de 20). El script de la página reescribe ese
    veredicto con el criterio del curso, y mientras la actividad está en marcha (el iDevice guarda
    la nota parcial después de cada pregunta) no adelanta ningún veredicto: informa de la
    puntuación acumulada.

 5. **El menú no tapa la página en vista estrecha.** En ≤750 px el tema deja de poner el índice
    como barra lateral (`#siteNav{float:none}`) y lo despliega como un panel a pantalla completa
    que, además, viaja abierto a la página siguiente (el estado va en `sessionStorage`). Aquí: al
    llegar sin preferencia guardada el menú empieza cerrado, y al clicar una entrada se cierra,
    para que la página elegida se vea sin tener que cerrarlo a mano. En escritorio no cambia nada
    (el menú es la barra lateral y se queda abierto).

Uso:
    python3 herramientas/ajustes_curso.py <ruta> [<ruta> ...]
    (cada <ruta> puede ser un directorio con las páginas en la raíz, un zip o un .elpx)
"""
import json
import pathlib
import re
import shutil
import sys
import tempfile
import urllib.parse
import zipfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent
XOR_KEY = 146

# Marca de los bloques que inyecta: permite reemplazarlos (y no duplicarlos) al volver a ejecutar.
MARCA_CSS = "/* ajustes del curso (inicio) */"
MARCA_JS = "<!-- ajustes del curso (inicio) -->"
RE_BLOQUE_CSS = re.compile(re.escape(MARCA_CSS) + r"[\s\S]*?/\* ajustes del curso \(fin\) \*/")
RE_BLOQUE_JS = re.compile(re.escape(MARCA_JS) + r"[\s\S]*?<!-- ajustes del curso \(fin\) -->")

RE_PAYLOAD = re.compile(r'(quext-DataGame js-hidden"?>)([^<]+)(<)')
RE_CIERRE = re.compile(r"</head>", re.IGNORECASE)

AJUSTES_CSS = """
/* ajustes del curso (inicio) */
/* Ajustes del proyecto: el test se lee como evaluación y no como juego.
   - El iDevice del test deja al terminar un bloque de retroalimentación vacío (con su botón
     «Cerrar»): en este curso la retroalimentación va dentro de cada respuesta.
   - El aviso de que la puntuación no se puede guardar solo tiene sentido en el paquete SCORM;
     aquí (body.exe-web-site) se oculta. */
body.exe-export .QXTP-DivFeedBack{display:none !important}
body.exe-web-site .Games-RepeatActivity{display:none !important}
/* ajustes del curso (fin) */
"""

AJUSTES_JS = r"""
<!-- ajustes del curso (inicio) -->
<script>
/* ajustes del curso: menú lateral con memoria, título de la pestaña y veredicto de la evaluación.
   Va en todas las páginas del export (HTML5, SCORM y .elpx) y no toca ni el iDevice ni sus datos:
   solo envuelve su interfaz. */
(function () {
    'use strict';
    var CLAVE = 'exe-menu-scroll';
    var TITULO = document.title; // el título real, antes de que el iDevice del test lo pise
    var fijado = false;          // posición decidida (clic en una entrada): no la pisar después
    // La posición se lee UNA vez, aquí (el script va en el <head>, antes de que el tema re-maquete
    // el menú y de que nada pueda sobrescribirla): si se leyera más tarde ya valdría 0.
    var GUARDADO = 0;
    try {
        GUARDADO = parseInt(sessionStorage.getItem(CLAVE) || '', 10) || 0;
    } catch (e) {}

    /* 5) Vista estrecha (≤750 px: es donde theme/style.css deja de poner el índice como barra
       lateral, `#siteNav{float:none}`, y lo despliega a pantalla completa). El estado «menú
       abierto» viaja en sessionStorage a la página siguiente, así que el panel tapa la página que
       el alumno acaba de elegir. Aquí: al llegar sin preferencia guardada el menú empieza cerrado,
       y al clicar una entrada se cierra antes de navegar. */
    var CORTE_ESTRECHO = '(max-width: 750px)';
    function esVistaEstrecha() {
        // Señal real del tema (su propio isLowRes()): en estrecho #siteNav deja de flotar.
        var n = document.getElementById('siteNav');
        return !!n && getComputedStyle(n).float === 'none';
    }
    function cerrarMenu() {
        document.documentElement.classList.add('siteNav-off');
        if (document.body) document.body.classList.add('siteNav-off');
        try {
            sessionStorage.setItem('siteNav-off', '1');
        } catch (e) {}
    }
    // Antes de pintar (este script va en el <head>): primera visita en el móvil -> cerrado.
    try {
        if (sessionStorage.getItem('siteNav-off') === null &&
            window.matchMedia && window.matchMedia(CORTE_ESTRECHO).matches) {
            sessionStorage.setItem('siteNav-off', '1');
            document.documentElement.classList.add('siteNav-off');
        }
    } catch (e) {}

    function menu() {
        return document.querySelector('#siteNav > ul');
    }

    /* 1) El menú lateral recuerda dónde estaba: sin esto, al clicar una entrada de abajo el panel
       vuelve al principio (cada página es un documento nuevo) y se pierde el punto de lectura. */
    function guardarMenu() {
        var c = menu();
        if (!c || fijado) return;
        try {
            sessionStorage.setItem(CLAVE, String(c.scrollTop));
        } catch (e) {}
    }

    function guardarYFijar() {
        guardarMenu();
        fijado = true; // al clicar, el navegador puede desplazar el panel para enfocar el enlace:
                       // la posición que vale es la de antes de clicar
    }

    function restaurarMenu() {
        var c = menu();
        if (!c) return;
        if (GUARDADO > 0) {
            c.scrollTop = GUARDADO;
            return;
        }
        // Sin posición guardada (primera visita o enlace directo): deja visible la página actual.
        var activo = c.querySelector('li.active > a');
        if (activo) {
            var r = activo.getBoundingClientRect();
            var n = c.getBoundingClientRect();
            if (r.top < n.top || r.bottom > n.bottom) {
                activo.scrollIntoView({ block: 'nearest' });
            }
        }
    }

    /* 2) El resultado se lee con el criterio del curso: 70 % (14 de 20). El marcador del iDevice da
       la actividad por superada a partir de 5 sobre 10. Mientras la actividad está en marcha no se
       adelanta veredicto (el iDevice guarda la nota parcial tras cada pregunta): se informa de la
       puntuación acumulada. */
    function revisarVeredicto() {
        Array.prototype.forEach.call(
            document.querySelectorAll('.Games-ReportIconDiv span'),
            function (span) {
                var m = /([0-9]+[.,]?[0-9]*)\s*$/.exec((span.textContent || '').trim());
                if (!m) return;
                var nota = parseFloat(m[1].replace(',', '.'));
                if (isNaN(nota)) return;
                // ¿Ha terminado esa actividad? El botón de arranque (que al terminar pasa a ser
                // «Repetir la actividad») está a la vista; durante la partida, oculto.
                var caja = span.closest('.idevice_node') || span.closest('article') || document;
                var boton = caja.querySelector('.QXTP-StartGame');
                var terminada = !boton || boton.offsetParent !== null;
                var texto = terminada
                    ? (nota >= 7 ? 'Actividad superada' : 'Actividad no superada') +
                      '. Puntuación: ' + nota.toFixed(2) + ' (mínimo 70 %)'
                    : 'Puntuación acumulada: ' + nota.toFixed(2) + ' (mínimo 70 %)';
                // Solo se toca si cambia: así el observador no se realimenta.
                if (span.textContent !== texto) span.textContent = texto;
            }
        );
    }

    document.addEventListener('DOMContentLoaded', function () {
        var c = menu();
        if (c) {
            restaurarMenu();
            setTimeout(restaurarMenu, 400); // el tema fija el menú en checkNav(): insistir una vez
            var t = null;
            c.addEventListener('scroll', function () {
                if (t) clearTimeout(t);
                t = setTimeout(guardarMenu, 150);
            });
            window.addEventListener('pagehide', guardarMenu);
            Array.prototype.forEach.call(
                document.querySelectorAll('#siteNav a[href]'),
                function (a) {
                    a.addEventListener('click', function (ev) {
                        guardarYFijar();
                        // En vista estrecha, elegir página cierra el menú: la página debe verse al
                        // llegar. Se descartan los botones de desplegable del propio menú y los
                        // enlaces que no navegan (anclas) o que abren otra pestaña.
                        var href = a.getAttribute('href') || '';
                        if (!href || href.charAt(0) === '#' || a.target === '_blank') return;
                        if (ev.target && ev.target.closest && ev.target.closest('button')) return;
                        if (esVistaEstrecha()) cerrarMenu();
                    });
                }
            );
        }
        // Título de la pestaña: el iDevice del test lo sustituye por el suyo (y en la evaluación lo
        // deja vacío), así que se recupera el de la página.
        var fijaTitulo = function () {
            if (document.title !== TITULO) document.title = TITULO;
        };
        fijaTitulo();
        setTimeout(fijaTitulo, 600);
        var tEl = document.querySelector('title');
        if (tEl) {
            new MutationObserver(fijaTitulo).observe(tEl, {
                childList: true,
                characterData: true,
                subtree: true,
            });
        }
        // Veredicto del curso (el marcador aparece al terminar y al volver a cargar la página).
        revisarVeredicto();
        setTimeout(revisarVeredicto, 700);
        new MutationObserver(revisarVeredicto).observe(document.body, {
            childList: true,
            subtree: true,
            characterData: true,
            attributes: true,
            attributeFilter: ['style'],
        });
    });
})();
</script>
<!-- ajustes del curso (fin) -->
"""


# --------------------------------------------------------------------------- payload cifrado

def descifra(cifrado: str) -> str:
    """escape() + XOR 146 en sentido inverso (common.js: encrypt)."""
    return "".join(chr(b ^ XOR_KEY) for b in urllib.parse.unquote_to_bytes(cifrado))


def cifra(claro: str) -> str:
    """Reproduce escape() del XOR 146 byte a byte (igual que el generador)."""
    xored = "".join(chr(ord(c) ^ XOR_KEY) for c in claro)
    return urllib.parse.quote(xored.encode("latin-1"), safe="")


def ajustar_payload(texto: str):
    """Reescribe el estado del iDevice Test en el payload cifrado. Devuelve (texto, n)."""
    cambios = [0]

    def sub(m):
        cifrado = m.group(2)
        claro = descifra(cifrado)
        if cifra(claro) != cifrado:                      # red de seguridad: la clave debe ser exacta
            raise SystemExit("el payload no se recodifica igual: no toco nada")
        nuevo = clave_a_valor(claro, "gameMode", 1)
        nuevo = clave_a_valor(nuevo, "percentajeFB", 0)
        nuevo = clave_a_valor(nuevo, "time", 5)
        if nuevo == claro:
            return m.group(0)
        json.loads(nuevo)                                # que siga siendo JSON válido
        cambios[0] += 1
        return m.group(1) + cifra(nuevo) + m.group(3)

    return RE_PAYLOAD.sub(sub, texto), cambios[0]


def clave_a_valor(claro: str, clave: str, valor: int) -> str:
    """Cambia "clave": N por el valor nuevo, solo si existe con un valor distinto."""
    return re.sub(r'"%s"\s*:\s*-?\d+' % re.escape(clave),
                  '"%s": %d' % (clave, valor), claro)


# --------------------------------------------------------------------------- páginas

# Bloques de la PRIMERA versión del script (sin marcas de inicio/fin): se retiran para poder
# actualizarlos, en vez de quedar duplicados.
RE_V1_CSS = re.compile(r"\n/\* Ajustes del proyecto: el test se lee como evaluación y no como juego\."
                       r"[\s\S]*?body\.exe-web-site \.Games-RepeatActivity\{display:none !important\}\n")
RE_V1_JS = re.compile(r"<script>\n/\* ajustes del curso: menú lateral con memoria[\s\S]*?</script>\n")


def quita_bloques_v1(texto: str) -> str:
    """Elimina los bloques inyectados por la primera versión (se reinyectan ya con marcas).

    Solo se aplica si la página no lleva ya las marcas nuevas: si no, el patrón de la v1 (que
    empieza por `<script>` y un comentario idéntico) también casaría con el bloque nuevo.
    """
    if MARCA_JS in texto or MARCA_CSS in texto:
        return texto
    return RE_V1_JS.sub("", RE_V1_CSS.sub("", texto))


def tocar_pagina(texto: str):
    """Devuelve (texto, lista de cambios aplicados)."""
    texto = quita_bloques_v1(texto)
    cambios = []
    texto, n = ajustar_payload(texto)
    if n:
        cambios.append(f"{n} payload(s)")

    cierre_head = RE_CIERRE.search(texto)
    if cierre_head:
        # OJO con el orden: cada inserción mueve los índices, así que los puntos de corte se
        # recalculan antes de cada una (si no, el script acabaría dentro del <style>).
        # Los bloques propios se reemplazan (no se duplican) si ya estaban: así una revisión
        # posterior del script actualiza las páginas ya retocadas.
        m_css = RE_BLOQUE_CSS.search(texto)
        if m_css:
            if m_css.group(0) != AJUSTES_CSS.strip():
                texto = texto[:m_css.start()] + AJUSTES_CSS.strip() + texto[m_css.end():]
                cambios.append("css actualizado")
        else:
            fin_css = texto.rfind("</style>", 0, cierre_head.start())
            if fin_css != -1:
                texto = texto[:fin_css] + AJUSTES_CSS + texto[fin_css:]
                cambios.append("css")
        m_js = RE_BLOQUE_JS.search(texto)
        if m_js:
            if m_js.group(0) != AJUSTES_JS.strip():
                texto = texto[:m_js.start()] + AJUSTES_JS.strip() + texto[m_js.end():]
                cambios.append("js actualizado")
        else:
            cierre = RE_CIERRE.search(texto)
            if cierre:
                texto = texto[:cierre.start()] + AJUSTES_JS + texto[cierre.start():]
                cambios.append("js")
    return texto, cambios


def es_pagina(nombre: str) -> bool:
    return nombre == "index.html" or (nombre.startswith("html/") and nombre.endswith(".html"))


# --------------------------------------------------------------------------- directorios y zips

def procesar_directorio(ruta: pathlib.Path):
    resumen = {}
    for f in [ruta / "index.html", *sorted((ruta / "html").glob("*.html"))]:
        if not f.exists():
            continue
        texto, cambios = tocar_pagina(f.read_text(encoding="utf-8"))
        if cambios:
            f.write_text(texto, encoding="utf-8")
        resumen[f.name] = cambios
    xml = ruta / "content.xml"
    if xml.exists():
        texto, n = ajustar_payload(xml.read_text(encoding="utf-8"))
        if n:
            xml.write_text(texto, encoding="utf-8")
        resumen["content.xml"] = [f"{n} payload(s)"] if n else []
    return resumen


def procesar_zip(ruta: pathlib.Path):
    with zipfile.ZipFile(ruta) as z:
        entradas = [(i, z.read(i.filename)) for i in z.infolist()]

    resumen = {}
    nuevas = []
    for info, datos in entradas:
        texto = datos.decode("utf-8", "surrogateescape")
        cambios = []
        if es_pagina(info.filename):
            texto, cambios = tocar_pagina(texto)
        elif info.filename == "content.xml":
            texto, n = ajustar_payload(texto)
            if n:
                cambios = [f"{n} payload(s)"]
        if cambios:
            datos = texto.encode("utf-8", "surrogateescape")
        if cambios:
            resumen[info.filename] = cambios
        nuevas.append((info, datos))

    if resumen:
        modo = ruta.stat().st_mode
        with tempfile.NamedTemporaryFile(dir=ruta.parent, suffix=".zip", delete=False) as tmp:
            tmp_ruta = pathlib.Path(tmp.name)
        with zipfile.ZipFile(tmp_ruta, "w", zipfile.ZIP_DEFLATED) as z:
            for info, datos in nuevas:
                info.external_attr = ((info.external_attr & 0xFFFF)
                                      | ((0o755 if info.filename.endswith("/") else 0o644) << 16))
                z.writestr(info, datos)
        tmp_ruta.chmod(modo)
        shutil.move(str(tmp_ruta), str(ruta))
    return resumen


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    for arg in sys.argv[1:]:
        ruta = pathlib.Path(arg)
        if not ruta.exists():
            raise SystemExit(f"no existe: {ruta}")
        resumen = procesar_directorio(ruta) if ruta.is_dir() else procesar_zip(ruta)
        tocados = {k: v for k, v in resumen.items() if v}
        if tocados:
            print(f"  {ruta.name}:")
            for k, v in tocados.items():
                print(f"      {k}: {', '.join(v)}")
        else:
            print(f"  {ruta.name}: ya estaba al día (sin cambios)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
