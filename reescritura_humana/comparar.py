#!/usr/bin/env python3
"""Compara el original de un nodo con las versiones reescritas y saca la muestra.

Uso:
    python3 comparar.py nodo_17_riesgos-y-limites.md gemma4b gemma4-12b \
        --salida muestra_nodo_17.md

Genera un markdown con:
  1) la cabecera (modelos, tiempos, longitudes),
  2) el texto bloque a bloque (original / version A / version B),
  3) un recuento de marcas de escritura de IA por version.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
TITULO_BLOQUE = re.compile(r"^\*\*(.+?)\*\*\s*$")

# Marcas de escritura de IA que el detector cuenta (es, no juicio de valor).
MARCAS = {
    "adjetivo de folleto": r"\b(incre[ií]ble|impresionante|revolucionari[oa]|potente|asombros[oa]|espectacular)\b",
    "grandilocuencia": r"\b(es fundamental|es esencial|es crucial|es vital|resulta imprescindible|sin duda)\b",
    "registro acartonado": r"\b(significativ[oa]s?|carece de|en detrimento de|discernir|ostenta|constituye|representa un)\b",
    "paralelismo negativo": r"(no (solo|solamente|únicamente)[^.]{0,60}sino (también )?)|(no (porque|es que)[^.]{0,40}, sino)",
    "personificación": r"(\bmient\w*|\bno sabe si\b|\bsin saber si\b|\bentiend\w+ como (humanos|las personas)\b|\bes consciente\b)",
    "triplete simétrico": r"\b\w+,\s+\w+\s+y\s+\w+\.\s*$",
    "raya larga": r"—",
}


def bloques(texto: str) -> list[tuple[str, str]]:
    """Parte el texto en (titulo, cuerpo) usando las lineas **Titulo**."""
    salida: list[tuple[str, str]] = []
    titulo = "(entrada)"
    cuerpo: list[str] = []
    for linea in texto.splitlines():
        m = TITULO_BLOQUE.match(linea.strip())
        if m:
            if cuerpo:
                salida.append((titulo, "\n".join(cuerpo).strip()))
            titulo, cuerpo = m.group(1), []
        else:
            cuerpo.append(linea)
    if cuerpo:
        salida.append((titulo, "\n".join(cuerpo).strip()))
    return salida


def contar(texto: str) -> dict[str, int]:
    return {nombre: len(re.findall(pat, texto, re.IGNORECASE | re.MULTILINE)) for nombre, pat in MARCAS.items()}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fichero")
    ap.add_argument("sufijos", nargs="+")
    ap.add_argument("--salida", default="")
    args = ap.parse_args()

    original = (RAIZ / "originales" / args.fichero).read_text(encoding="utf-8")
    versiones = {
        s: (RAIZ / "salida" / s / args.fichero).read_text(encoding="utf-8") for s in args.sufijos
    }
    nombres = {"gemma4b": "Gemma 4B", "gemma4-12b": "Gemma 12B", **{s: s for s in args.sufijos}}

    tiempos = {}
    for s in args.sufijos:
        p = RAIZ / "salida" / s / "_tiempos.json"
        if p.exists():
            tiempos[s] = json.loads(p.read_text(encoding="utf-8"))[0]

    L: list[str] = []
    L.append(f"# Muestra de reescritura — {args.fichero}\n")
    L.append("Una sola página del guión, sin tocar el guión original.\n")
    L.append("## Qué se ha usado\n")
    L.append("| Versión | Modelo local (llama-server :8080) | Tiempo | Velocidad | Longitud |")
    L.append("|---|---|---|---|---|")
    L.append(f"| Original | — | — | — | {len(original)} car. |")
    for s in args.sufijos:
        t = tiempos.get(s)
        vel = f"{t['tok_s']} tok/s" if t else "—"
        seg = f"{t['segundos']} s" if t else "—"
        L.append(f"| {nombres.get(s, s)} | `{t['modelo'] if t else s}` | {seg} | {vel} | {len(versiones[s])} car. |")
    L.append("\nPlantilla: `prompts/reescritura.md` · parámetros: los del `command_*.txt` del modelo.\n")

    L.append("## Marcas de escritura de IA detectadas\n")
    L.append("Recuento por versión (menos es mejor; 0 no significa perfecto).\n")
    L.append("| Marca | Original | " + " | ".join(nombres.get(s, s) for s in args.sufijos) + " |")
    L.append("|---|---|" + "---|" * len(args.sufijos))
    c_orig = contar(original)
    c_vers = {s: contar(versiones[s]) for s in args.sufijos}
    for marca in MARCAS:
        fila = [marca, str(c_orig[marca])] + [str(c_vers[s][marca]) for s in args.sufijos]
        L.append("| " + " | ".join(fila) + " |")
    tot_orig = sum(c_orig.values())
    tot = {s: sum(c_vers[s].values()) for s in args.sufijos}
    L.append(
        "| **Total** | **" + str(tot_orig) + "** | "
        + " | ".join(f"**{tot[s]}**" for s in args.sufijos)
        + " |"
    )

    L.append("\n## Texto, bloque a bloque\n")
    b_orig = bloques(original)
    b_vers = {s: bloques(versiones[s]) for s in args.sufijos}
    for i, (titulo, cuerpo_o) in enumerate(b_orig):
        L.append(f"### {titulo}\n")
        L.append(f"**Original.** {cuerpo_o}\n")
        for s in args.sufijos:
            cuerpo_v = b_vers[s][i][1] if i < len(b_vers[s]) else "(bloque ausente)"
            L.append(f"**{nombres.get(s, s)}.** {cuerpo_v}\n")

    L.append("## Versiones completas\n")
    L.append(f"**Original**\n\n```markdown\n{original}\n```\n")
    for s in args.sufijos:
        L.append(f"**{nombres.get(s, s)}**\n\n```markdown\n{versiones[s]}\n```\n")

    texto = "\n".join(L) + "\n"
    destino = RAIZ / args.salida if args.salida else None
    if destino:
        destino.write_text(texto, encoding="utf-8")
        print(f"escrito {destino} ({len(texto)} car.)")
    else:
        print(texto)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
