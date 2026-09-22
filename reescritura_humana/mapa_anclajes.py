#!/usr/bin/env python3
"""Lista los ANCLAJES disponibles de cada página (encabezados y etiquetas en negrita).

Es la lista de puntos donde el guion puede decir «tras «...»» para colocar un recuadro de ideas
clave. Imprime también la posición relativa de cada anclaje en la página, para elegir uno de
mitad de página.

Uso: python3 mapa_anclajes.py [carpeta]      (por defecto, originales/)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
RE_ENCABEZADO = re.compile(r"(?m)^(#{2,4})\s+(.*)$")
RE_NEGRITA = re.compile(r"\*\*(.+?)\*\*")


def anclajes(texto: str):
    """Encabezados y etiquetas en negrita que abren bloque (el texto usa <br> o saltos reales)."""
    normalizado = texto.replace("<br>", "\n").replace("<br/>", "\n").replace("<br />", "\n")
    encontrados = []
    desplazamiento = 0
    for linea in normalizado.split("\n"):
        limpia = linea.strip()
        m_h = RE_ENCABEZADO.match(limpia)
        m_n = RE_NEGRITA.match(limpia)
        if m_h:
            encontrados.append((desplazamiento, m_h.group(2).strip(), "encabezado"))
        elif m_n and len(m_n.group(1).strip()) > 3:
            encontrados.append((desplazamiento, m_n.group(1).strip(), "etiqueta"))
        desplazamiento += len(linea) + 1
    # quita duplicados exactos conservando el primero
    vistos, salida = set(), []
    for pos, titulo, tipo in encontrados:
        if titulo.lower() not in vistos:
            vistos.add(titulo.lower())
            salida.append((pos, titulo, tipo))
    return salida


def entradas(carpeta: Path):
    """Lista de (nodo, titulo, fichero). Usa indice.json si está; si no, deduce de los nombres."""
    indice_json = carpeta / "indice.json"
    if indice_json.exists():
        return json.loads(indice_json.read_text(encoding="utf-8"))
    salida = []
    for fichero in sorted(carpeta.glob("nodo_*.md")):
        m = re.match(r"nodo_(\d+)_(.*)\.md$", fichero.name)
        if m:
            salida.append({"nodo": int(m.group(1)), "titulo": m.group(2).replace("-", " "),
                           "fichero": fichero.name})
    return salida


def main() -> int:
    carpeta = RAIZ / (sys.argv[1] if len(sys.argv) > 1 else "originales")
    indice = entradas(carpeta)
    for entrada in indice:
        texto = (carpeta / entrada["fichero"]).read_text(encoding="utf-8")
        total = len(texto) or 1
        lista = anclajes(texto)
        print(f"\n=== NODO {entrada['nodo']:02d} · {entrada['titulo']} ({total} car.)")
        if not lista:
            print("   (sin anclajes)")
        for pos, titulo, tipo in lista:
            repeticiones = texto.count(titulo)
            aviso = "" if repeticiones == 1 else f"  <-- OJO: aparece {repeticiones} veces"
            print(f"   {pos * 100 // total:>3}%  [{tipo}] {titulo}{aviso}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
