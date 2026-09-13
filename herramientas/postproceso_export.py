#!/usr/bin/env python3
"""Post-proceso de las exportaciones: CSS del proyecto y navegación al pie.

Hace dos cosas sobre las páginas HTML de un paquete exportado (`.elpx`, SCORM, HTML5):

 1. **Inyecta el CSS del proyecto** si no está. Hace falta porque el exportador SCORM 1.2 de
    eXeLearning 4 ignora `pp_extraHeadContent` (el export HTML5 y el `.elpx` sí lo aplican).
 2. **Mueve la navegación «Anterior / Siguiente» al pie**: el div `.nav-buttons` que el exportador
    coloca justo después de `</main>` se mete dentro de `<main>` (al final), para que herede el
    hueco del menú lateral y los puntos de ruptura del tema. Nova lo posiciona `fixed` arriba a la
    derecha; el CSS del proyecto lo devuelve al flujo. Los JS del tema (style.js, libs/exe_export.js)
    seleccionan `.nav-buttons a` de forma global, así que la ubicación del contenedor les es igual.

Es idempotente (si ya está hecho, no toca nada), conserva el orden de los ficheros y normaliza los
permisos del zip a 644/755 (Python los dejaría en 600: un paquete descomprimido en un servidor no se
podría leer).

Uso:
    python3 herramientas/postproceso_export.py <zip|elpx> [<más> ...]
"""
import pathlib
import re
import shutil
import sys
import tempfile
import zipfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ESTILOS = RAIZ / "entregables" / "_trabajo" / "estilos_propios.html"
MARCA = "box.no-header"          # aparece en el CSS del proyecto
RE_NAV = re.compile(r'<div class="nav-buttons">[\s\S]*?</div>\s*')


def es_pagina(nombre: str) -> bool:
    return nombre == "index.html" or (nombre.startswith("html/") and nombre.endswith(".html"))


def tocar_pagina(texto: str, estilos: str):
    """Devuelve (texto, cambios), con cambios la lista de lo aplicado: 'css', 'nav'."""
    cambios = []

    if MARCA not in texto and "</head>" in texto:
        texto = texto.replace("</head>", estilos + "\n</head>", 1)
        cambios.append("css")

    if "</main>" in texto:
        m = RE_NAV.search(texto)
        i_main = texto.rindex("</main>")
        if m and m.start() > i_main:          # todavía está fuera de <main> (aún sin mover)
            bloque = m.group(0).strip()
            resto = texto[:m.start()] + texto[m.end():]
            j = resto.rindex("</main>")
            texto = resto[:j] + bloque + "\n" + resto[j:]
            cambios.append("nav")

    return texto, cambios


def procesar(ruta: pathlib.Path, estilos: str):
    with zipfile.ZipFile(ruta) as z:
        entradas = [(i, z.read(i.filename)) for i in z.infolist()]

    resumen = {"css": 0, "nav": 0}
    nuevo = []
    for info, datos in entradas:
        if es_pagina(info.filename):
            texto, cambios = tocar_pagina(datos.decode("utf-8"), estilos)
            for c in cambios:
                resumen[c] += 1
            if cambios:
                datos = texto.encode("utf-8")
        nuevo.append((info, datos))

    if resumen["css"] or resumen["nav"]:
        modo = ruta.stat().st_mode
        with tempfile.NamedTemporaryFile(dir=ruta.parent, suffix=".zip", delete=False) as tmp:
            tmp_ruta = pathlib.Path(tmp.name)
        with zipfile.ZipFile(tmp_ruta, "w", zipfile.ZIP_DEFLATED) as z:
            for info, datos in nuevo:
                # `writestr` fija los permisos en 600 si el ZipInfo no los trae: se normalizan a
                # 644/755 para que el paquete se pueda descomprimir y servir desde un servidor.
                info.external_attr = ((info.external_attr & 0xFFFF)
                                      | ((0o755 if info.filename.endswith("/") else 0o644) << 16))
                z.writestr(info, datos)
        tmp_ruta.chmod(modo)  # el fichero temporal nace 600: se conservan los permisos originales
        shutil.move(str(tmp_ruta), str(ruta))
    return resumen


def main():
    if not ESTILOS.exists():
        raise SystemExit(f"Falta {ESTILOS}. Ejecuta antes herramientas/generar_curso_elpx.py")
    estilos = ESTILOS.read_text(encoding="utf-8").strip()
    for arg in sys.argv[1:]:
        ruta = pathlib.Path(arg)
        r = procesar(ruta, estilos)
        if r["css"] or r["nav"]:
            print(f"  {ruta.name}: CSS en {r['css']} páginas, navegación al pie en {r['nav']}")
        else:
            print(f"  {ruta.name}: ya estaba al día (sin cambios)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    raise SystemExit(main())
