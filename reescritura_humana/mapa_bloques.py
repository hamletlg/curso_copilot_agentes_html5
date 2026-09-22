#!/usr/bin/env python3
"""Mapa de bloques de cada página, para decidir dónde va un recuadro de ideas clave.

Imprime, por nodo: longitud, lista de encabezados ### con su posición relativa dentro de la
página (para elegir un ancla de mitad de página) y el número de bloques.

Uso: python3 mapa_bloques.py [carpeta]      (por defecto, originales/)
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent


def main() -> int:
    carpeta = RAIZ / (sys.argv[1] if len(sys.argv) > 1 else "originales")
    indice = json.loads((carpeta / "indice.json").read_text(encoding="utf-8"))
    for entrada in indice:
        texto = (carpeta / entrada["fichero"]).read_text(encoding="utf-8")
        encabezados = [(m.start(), m.group(2).strip())
                       for m in re.finditer(r"(?m)^(#{2,4})\s+(.*)$", texto)]
        total = len(texto)
        print(f"\n=== NODO {entrada['nodo']:02d} · {entrada['titulo']}  ({total} car.)")
        if not encabezados:
            print("   (sin encabezados)")
            continue
        for pos, titulo in encabezados:
            print(f"   {pos * 100 // total:>3}%  {titulo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
