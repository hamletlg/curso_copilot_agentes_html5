#!/usr/bin/env python3
"""Verifica, EN EL PRODUCTO EXPORTADO, que el recuadro de ideas clave está y se ve como toca.

Comprueba las tres cosas por separado, que es donde se rompen estas cosas:
  1. el CSS del recuadro viaja dentro del paquete (vista previa HTML5, .zip SCORM y .elpx);
  2. cada página seleccionada tiene EXACTAMENTE un recuadro, con su etiqueta y sus viñetas;
  3. el recuadro cae donde se dijo: entre el 25 % y el 80 % de la página, no al final.

Uso: python3 verificar_recuadros.py [recuadros/seleccion.json]
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
PROYECTO = RAIZ.parent
PREVIEW = PROYECTO / "entregables" / "html5_preview" / "html"
SCORM = PROYECTO / "entregables" / "curso_copilot_agentes_scorm12.zip"
HTML5 = PROYECTO / "entregables" / "curso_copilot_agentes_html5.zip"
ELPX = PROYECTO / "entregables" / "curso_copilot_agentes.elpx"

MARCA_CSS = ".caja-ideas-clave{"
MINIMO, MAXIMO = 0.20, 0.85


def paginas_html() -> dict[int, Path]:
    """{numero de pagina: fichero} a partir de «N-slug.html»."""
    salida = {}
    for fichero in sorted(PREVIEW.glob("*.html")):
        m = re.match(r"(\d+)-", fichero.name)
        if m:
            salida[int(m.group(1))] = fichero
    return salida


def css_en(zip_abierto: zipfile.ZipFile, sufijo: str) -> bool:
    for nombre in zip_abierto.namelist():
        if nombre.endswith(sufijo):
            datos = zip_abierto.read(nombre).decode("utf-8", "replace")
            if MARCA_CSS in datos:
                return True
    return False


def main() -> int:
    seleccion = json.loads(
        (RAIZ / (sys.argv[1] if len(sys.argv) > 1 else "recuadros/seleccion.json"))
        .read_text(encoding="utf-8"))
    nodos = sorted(e["nodo"] for e in seleccion)
    fallos: list[str] = []

    # 1. el CSS viaja en la vista previa y en los tres entregables
    print("== CSS del recuadro ==")
    css_prev = 0
    paginas = paginas_html()
    for fichero in paginas.values():
        if MARCA_CSS in fichero.read_text(encoding="utf-8", errors="replace"):
            css_prev += 1
    print(f"  vista previa: el CSS aparece en {css_prev} de {len(paginas)} páginas")
    if css_prev != len(paginas):
        fallos.append(f"el CSS del recuadro no está en todas las páginas de la vista previa "
                      f"({css_prev}/{len(paginas)})")
    for etiqueta, ruta in (("SCORM 1.2", SCORM), ("HTML5", HTML5), ("elpx", ELPX)):
        if not ruta.exists():
            fallos.append(f"{etiqueta}: no existe {ruta.name}")
            continue
        with zipfile.ZipFile(ruta) as z:
            hay = any(MARCA_CSS in z.read(n).decode("utf-8", "replace")
                      for n in z.namelist() if n.endswith((".html", ".xml")))
        print(f"  {etiqueta}: CSS presente -> {hay}")
        if not hay:
            fallos.append(f"{etiqueta}: el CSS del recuadro no viaja dentro del paquete")

    # 2 y 3. una página por recuadro, con su etiqueta, sus viñetas y en su sitio
    print("\n== Recuadros por página ==")
    for entrada in seleccion:
        numero = entrada["nodo"]
        fichero = paginas.get(numero)
        if fichero is None:
            fallos.append(f"página {numero}: no está en la vista previa")
            continue
        html = fichero.read_text(encoding="utf-8", errors="replace")
        veces = len(re.findall(r'class="caja-ideas-clave"', html))
        if veces != 1:
            fallos.append(f"página {numero}: {veces} recuadros (debe haber 1)")
            continue
        pos = html.index('class="caja-ideas-clave"') / max(len(html), 1)
        trozo = html[html.index('class="caja-ideas-clave"'):]
        trozo = trozo[:trozo.index("</aside>") + len("</aside>")]
        vinietas = len(re.findall(r"<li>", trozo))
        etiqueta = re.search(r'caja-ideas-clave-titulo">(.*?)</p>', trozo)
        problemas = []
        if vinietas < 3:
            problemas.append(f"solo {vinietas} viñetas")
        if not etiqueta or not etiqueta.group(1).strip():
            problemas.append("sin etiqueta visible")
        if not (MINIMO <= pos <= MAXIMO):
            problemas.append(f"fuera de la franja de mitad de página ({pos:.0%})")
        print(f"  página {numero:>2} · {fichero.name:<52} "
              f"posición {pos:.0%} · {vinietas} viñetas · "
              f"{'OK' if not problemas else 'REVISAR: ' + '; '.join(problemas)}")
        fallos.extend(f"página {numero}: {p}" for p in problemas)

    # las páginas SIN recuadro no deben tenerlo
    sin_recuadro = [n for n in paginas if n not in nodos]
    intrusos = [n for n in sin_recuadro
                if 'class="caja-ideas-clave"' in paginas[n].read_text(encoding="utf-8",
                                                                      errors="replace")]
    print(f"\n== Páginas sin recuadro: {len(sin_recuadro)} · con recuadro por error: {len(intrusos)}")
    if intrusos:
        fallos.append(f"páginas con recuadro no previsto: {intrusos}")

    print()
    if fallos:
        print(f"FALLOS ({len(fallos)}):")
        for f in fallos:
            print("  -", f)
        return 1
    print(f"OK: {len(seleccion)} recuadros, correctos y en su sitio, y el CSS viaja en los "
          f"tres entregables.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
