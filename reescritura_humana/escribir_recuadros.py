#!/usr/bin/env python3
"""Pide al modelo local el recuadro de ideas clave de las páginas seleccionadas.

Uso:
    python3 escribir_recuadros.py recuadros/seleccion.json
    python3 escribir_recuadros.py recuadros/seleccion.json --modelo gemma4-12b

Entrada : recuadros/seleccion.json  -> [{nodo, fichero, ancla, motivo}, ...]
          salida/<sufijo>/<fichero>  (la página YA reescrita: el recuadro va sobre el texto final)
Plantilla: prompts/recuadro.md
Salida  : recuadros/salida/nodo_NN.md            (solo el recuadro: etiqueta + viñetas)
          recuadros/salida/nodo_NN.campo.txt     (la fila lista para pegar en el guion)

Solo biblioteca estandar.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
PLANTILLA = RAIZ / "prompts" / "recuadro.md"
BASE = "http://127.0.0.1:8080"
MAX_TOKENS = 3000  # el modelo razona antes de escribir: con 1200 se quedaba sin presupuesto
                    # y devolvía la respuesta vacía (medido: 8 de 8 vacíos)
MIN_VINETAS, MAX_VINETAS = 3, 4


def pedir(prompt: str, modelo: str, timeout: int = 600) -> dict:
    cuerpo = {
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": MAX_TOKENS,
        "stream": False,
    }
    if modelo:
        cuerpo["model"] = modelo
    pet = urllib.request.Request(
        BASE + "/v1/chat/completions",
        data=json.dumps(cuerpo).encode("utf-8"),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(pet, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def limpiar(txt: str) -> str:
    t = (txt or "").strip()
    if t.startswith("```"):
        lineas = t.splitlines()[1:]
        if lineas and lineas[-1].strip() == "```":
            lineas = lineas[:-1]
        t = "\n".join(lineas).strip()
    t = t.replace("... reasoning budget exceeded, need to answer.", "").strip()
    # el modelo a veces deja el razonamiento en prosa antes de las viñetas: nos quedamos desde
    # la etiqueta hacia abajo
    m = re.search(r"(?m)^\*\*[^*\n]{3,40}\*\*\s*$", t)
    if m:
        t = t[m.start():]
    return t


def revisar(recuadro: str) -> list[str]:
    """Reglas duras comprobables sin criterio humano."""
    avisos = []
    lineas = [l.strip() for l in recuadro.splitlines() if l.strip()]
    vinietas = [l for l in lineas if l.startswith("- ")]
    if not (MIN_VINETAS <= len(vinietas) <= MAX_VINETAS):
        avisos.append(f"{len(vinietas)} viñetas (se piden {MIN_VINETAS} o {MAX_VINETAS})")
    if not lineas or not lineas[0].startswith("**"):
        avisos.append("sin etiqueta en negrita en la primera línea")
    for v in vinietas:
        palabras = len(v[2:].split())
        if not (8 <= palabras <= 26):
            avisos.append(f"viñeta de {palabras} palabras: {v[:60]}")
        if "**" in v or "[" in v:
            avisos.append(f"viñeta con negrita o enlace: {v[:60]}")
        inicio = v[2:].lower()
        for muletilla in ("recuerda que", "es importante", "ten en cuenta", "no olvides"):
            if inicio.startswith(muletilla):
                avisos.append(f"viñeta con muletilla «{muletilla}»: {v[:60]}")
    folleto = re.findall(r"\b(increíble|esencial|crucial|fundamental|potente|revolucionari\w+)\b",
                         recuadro, re.IGNORECASE)
    if folleto:
        avisos.append(f"palabras de folleto: {sorted(set(folleto))}")
    if re.search(r"\b(usted|su empresa|debe)\b", recuadro, re.IGNORECASE):
        avisos.append("mezcla de tratamiento (usted/debe)")
    return avisos


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("seleccion")
    ap.add_argument("--modelo", default="gemma4-12b")
    ap.add_argument("--sufijo", default="gemma4-12b", help="subcarpeta de salida de la reescritura")
    args = ap.parse_args()

    seleccion = json.loads(Path(args.seleccion).read_text(encoding="utf-8"))
    plantilla = PLANTILLA.read_text(encoding="utf-8")
    destino = RAIZ / "recuadros" / "salida"
    destino.mkdir(parents=True, exist_ok=True)
    informe = []

    for entrada in seleccion:
        pagina = (RAIZ / "salida" / args.sufijo / entrada["fichero"]).read_text(encoding="utf-8")
        # Si ya hay recuadro escrito y con viñetas, no se vuelve a pedir (el script es reanudable).
        destino_md = destino / f"nodo_{entrada['nodo']:02d}.md"
        if destino_md.exists():
            previo = destino_md.read_text(encoding="utf-8")
            if len([l for l in previo.splitlines() if l.startswith("- ")]) >= MIN_VINETAS:
                print(f"  NODO {entrada['nodo']:02d}: ya hecho, se salta")
                informe.append({**entrada, "saltado": True})
                continue
        # El anclaje tiene que existir y ser único en el TEXTO FINAL: si no, el generador se
        # negaría a montar la página (y con razón). Mejor descubrirlo antes de gastar el turno.
        plano = pagina.replace("<br>", "\n")
        repeticiones = plano.count(entrada["ancla"])
        if repeticiones != 1:
            print(f"  NODO {entrada['nodo']:02d}: ANCLA NO VÁLIDA — «{entrada['ancla']}» aparece "
                  f"{repeticiones} veces en el texto final")
            informe.append({**entrada, "error": f"ancla aparece {repeticiones} veces"})
            continue
        prompt = plantilla.replace("{PAGINA}", pagina)
        t0 = time.monotonic()
        try:
            resp = pedir(prompt, args.modelo)
        except urllib.error.HTTPError as e:
            print(f"  NODO {entrada['nodo']:02d}: FALLO HTTP {e.code} {e.read()[:200]!r}")
            informe.append({**entrada, "error": f"HTTP {e.code}"})
            continue
        segundos = time.monotonic() - t0
        bruto = resp["choices"][0]["message"].get("content") or ""
        (destino / f"nodo_{entrada['nodo']:02d}.raw.txt").write_text(bruto, encoding="utf-8")
        recuadro = limpiar(bruto)
        if not recuadro.strip():
            print(f"  NODO {entrada['nodo']:02d}: RESPUESTA VACÍA — el modelo gastó el presupuesto "
                  f"de razonamiento sin escribir (mira el .raw.txt)")
            informe.append({**entrada, "error": "respuesta vacía"})
            continue
        (destino / f"nodo_{entrada['nodo']:02d}.md").write_text(recuadro + "\n", encoding="utf-8")
        # fila del guion: POSICIÓN + texto con <br>
        cuerpo_html = recuadro.replace("\n\n", "<br><br>").replace("\n", "<br>")
        campo = f"**POSICIÓN:** tras «{entrada['ancla']}»<br><br>{cuerpo_html}"
        (destino / f"nodo_{entrada['nodo']:02d}.campo.txt").write_text(campo + "\n", encoding="utf-8")
        avisos = revisar(recuadro)
        informe.append({**entrada, "segundos": round(segundos, 1), "avisos": avisos,
                        "vinietas": len([l for l in recuadro.splitlines() if l.startswith("- ")])})
        print(f"  NODO {entrada['nodo']:02d}: {segundos:.0f}s · "
              f"{'OK' if not avisos else 'REVISAR: ' + '; '.join(avisos)}")

    (destino / "informe.json").write_text(
        json.dumps(informe, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    con_avisos = [i for i in informe if i.get("avisos")]
    print(f"\n{len(informe) - len(con_avisos)}/{len(informe)} recuadros sin avisos automáticos")
    return 0


if __name__ == "__main__":
    sys.exit(main())
