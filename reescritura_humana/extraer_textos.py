#!/usr/bin/env python3
"""Extrae el campo «Contenido en pantalla» de cada nodo del guion.

Entrada : ../guión_curso_copilot_exelearning.md
Salida  : originales/nodo_NN_<slug>.md   (texto en markdown, <br> -> salto real)
          originales/indice.json         (numero, titulo, slug, fichero, chars)

No modifica el guion. Es idempotente: volver a ejecutarlo reescribe los mismos ficheros.
"""
from __future__ import annotations

import json
import re
import unicodedata
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
GUION = RAIZ.parent / "guión_curso_copilot_exelearning.md"
DEST = RAIZ / "originales"

CABECERA = re.compile(r"\n### (NODO (\d+) — [^\n]+)\n")
CAMPO = re.compile(r"\|\s*\*\*Contenido en pantalla\*\*\s*\|(.*?)\n\|", re.DOTALL)


def slug(texto: str) -> str:
    s = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "-", s).strip("-").lower()
    return s[:40]


def main() -> int:
    DEST.mkdir(parents=True, exist_ok=True)
    texto = GUION.read_text(encoding="utf-8")

    trozos = CABECERA.split(texto)
    indice = []
    for i in range(1, len(trozos), 3):
        nombre, numero, cuerpo = trozos[i], trozos[i + 1], trozos[i + 2]
        m = CAMPO.search(cuerpo)
        if not m:
            print(f"AVISO: nodo {numero} sin «Contenido en pantalla», se salta")
            continue
        contenido = m.group(1).replace("<br>", "\n").strip()
        # El campo vive en una fila de tabla: puede quedar el «|» de cierre.
        contenido = contenido.rstrip().rstrip("|").rstrip()
        titulo = nombre.split("—", 1)[1].strip()
        fichero = f"nodo_{int(numero):02d}_{slug(titulo)}.md"
        (DEST / fichero).write_text(contenido + "\n", encoding="utf-8")
        indice.append(
            {
                "nodo": int(numero),
                "titulo": titulo,
                "fichero": fichero,
                "chars": len(contenido),
            }
        )

    (DEST / "indice.json").write_text(
        json.dumps(indice, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"{len(indice)} nodos extraidos en {DEST}")
    for e in indice:
        print(f"  {e['nodo']:02d}  {e['chars']:5d}  {e['fichero']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
