#!/usr/bin/env python3
"""Reescribe los textos del guion con el modelo local servido en llama-server.

Uso:
    python3 reescribir.py nodo_17_riesgos-y-limites.md
    python3 reescribir.py --todos
    python3 reescribir.py --todos --modelo gemma4-e4b-mtp --sufijo gemma4b

Entrada : originales/<fichero>            (lo extrae extraer_textos.py)
Plantilla: prompts/reescritura.md         (con el marcador {TEXTO})
Salida  : salida/<sufijo>/<fichero>  +  salida/<sufijo>/_tiempos.json

Solo biblioteca estandar. Cliente OpenAI (/v1/chat/completions), sin dependencias.
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
ORIGINALES = RAIZ / "originales"
PLANTILLA = RAIZ / "prompts" / "reescritura.md"
BASE = "http://127.0.0.1:8080"
MAX_TOKENS = 6000


def pedir(prompt: str, modelo: str = "", timeout: int = 900) -> dict:
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
    """Quita vallas de codigo y el mensaje del presupuesto de razonamiento."""
    t = txt.strip()
    if t.startswith("```"):
        lineas = t.splitlines()
        if lineas and lineas[0].startswith("```"):
            lineas = lineas[1:]
        if lineas and lineas[-1].strip() == "```":
            lineas = lineas[:-1]
        t = "\n".join(lineas).strip()
    t = t.replace("... reasoning budget exceeded, need to answer.", "").strip()
    # El «|» de cierre del campo del guion no forma parte del texto de la pagina.
    t = t.rstrip().rstrip("|").rstrip()
    return t + "\n"


def reescribir(fichero: str, sufijo: str, modelo: str) -> dict:
    original = (ORIGINALES / fichero).read_text(encoding="utf-8")
    prompt = PLANTILLA.read_text(encoding="utf-8").replace("{TEXTO}", original)
    destino = RAIZ / "salida" / sufijo
    destino.mkdir(parents=True, exist_ok=True)
    salida = destino / fichero

    t0 = time.monotonic()
    try:
        resp = pedir(prompt, modelo)
    except urllib.error.HTTPError as e:
        detalle = e.read().decode("utf-8", "replace")[:500]
        print(f"  FALLO HTTP {e.code} en {fichero}: {detalle}")
        return {"fichero": fichero, "error": f"HTTP {e.code}"}
    except Exception as e:  # noqa: BLE001
        print(f"  FALLO en {fichero}: {e}")
        return {"fichero": fichero, "error": str(e)}
    segundos = time.monotonic() - t0

    msg = resp["choices"][0]["message"]
    reescrito = limpiar(msg.get("content") or "")
    salida.write_text(reescrito, encoding="utf-8")

    uso = resp.get("usage", {})
    gen = uso.get("completion_tokens", 0)
    dato = {
        "fichero": fichero,
        "modelo": resp.get("model", modelo),
        "segundos": round(segundos, 1),
        "tokens_entrada": uso.get("prompt_tokens", 0),
        "tokens_salida": gen,
        "tok_s": round(gen / segundos, 1) if segundos else 0,
        "chars_original": len(original),
        "chars_reescrito": len(reescrito),
        "razonamiento_chars": len(msg.get("reasoning_content") or ""),
    }
    print(
        f"  {fichero}: {dato['segundos']}s  {gen} tok  {dato['tok_s']} tok/s  "
        f"{dato['chars_original']}→{dato['chars_reescrito']} chars"
    )
    return dato


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("ficheros", nargs="*", help="ficheros de originales/")
    ap.add_argument("--todos", action="store_true", help="todos los nodos, en orden")
    ap.add_argument("--modelo", default="", help="campo model de la peticion")
    ap.add_argument("--sufijo", default="gemma4b", help="subcarpeta de salida")
    args = ap.parse_args()

    ficheros = args.ficheros
    if args.todos:
        indice = json.loads((ORIGINALES / "indice.json").read_text(encoding="utf-8"))
        ficheros = [e["fichero"] for e in indice]
    if not ficheros:
        ap.error("indica al menos un fichero o --todos")

    tiempos = [reescribir(f, args.sufijo, args.modelo) for f in ficheros]

    destino = RAIZ / "salida" / args.sufijo
    (destino / "_tiempos.json").write_text(
        json.dumps(tiempos, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    ok = [t for t in tiempos if "error" not in t]
    if ok:
        print(
            f"\n{len(ok)}/{len(tiempos)} nodos · "
            f"total {sum(t['segundos'] for t in ok):.0f}s · "
            f"media {statistics.mean(t['segundos'] for t in ok):.1f}s · "
            f"{statistics.mean(t['tok_s'] for t in ok):.1f} tok/s"
        )
    return 0 if len(ok) == len(tiempos) else 1


if __name__ == "__main__":
    sys.exit(main())
