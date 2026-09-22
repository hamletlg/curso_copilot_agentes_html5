#!/usr/bin/env python3
"""Reescribe el cuestionario final preservando el formato que el generador sabe leer.

El cuestionario no se puede reescribir «a lo libre»: el generador lo parte con `parse_quiz()`, que
busca `**Pregunta N:**`, opciones `a)`…`d)` y la marca `[CORRECTA]`. Por eso aquí:

  1. el modelo reescribe el texto con la estructura congelada;
  2. se valida con el parser REAL del generador: 20 preguntas, 4 opciones cada una, exactamente una
     correcta, numeración 1..20 sin huecos;
  3. si falla, se reintenta una vez con los errores delante;
  4. si vuelve a fallar, NO se sustituye nada: se conserva el cuestionario que ya estaba.

El cuestionario original y el intento fallido se guardan siempre, para poder compararlos.

Uso:
    python3 reescribir_quiz.py --sufijo gemma4-12b
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
GEN = RAIZ.parent / "herramientas"
sys.path.insert(0, str(GEN))
import generar_curso_elpx as gen

PLANTILLA = RAIZ / "prompts" / "quiz_formato.md"
INDICE = RAIZ / "originales" / "indice.json"
DEST = RAIZ / "quiz" / "salida"
BASE = "http://127.0.0.1:8080"
MAX_TOKENS = 9000
N_PREGUNTAS = 20
N_OPCIONES = 4


def pedir(prompt: str, modelo: str, timeout: int = 900) -> dict:
    cuerpo = {"messages": [{"role": "user", "content": prompt}], "max_tokens": MAX_TOKENS,
              "stream": False}
    if modelo:
        cuerpo["model"] = modelo
    pet = urllib.request.Request(BASE + "/v1/chat/completions",
                                 data=json.dumps(cuerpo).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
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
    m = re.search(r"\*\*Título del quiz:\*\*", t)
    if m:
        t = t[m.start():]
    # una línea por elemento (el parser del generador parte por <br>)
    lineas = [l.strip() for l in t.splitlines() if l.strip()]
    t = "<br>".join(lineas)
    # las opciones sueltas quedan pegadas a la pregunta anterior por comas: se separan igual
    return re.sub(r"(?<=[^\s])\s*(?=[a-d]\)\s)", "<br>", t)


def validar(texto: str) -> list[str]:
    """Valida con el parser real del generador."""
    problemas = []
    if "**Título del quiz:**" not in texto:
        problemas.append("falta la línea «Título del quiz»")
    if "**Instrucción:**" not in texto:
        problemas.append("falta la línea «Instrucción»")
    preguntas = gen.parse_quiz(texto)
    if len(preguntas) != N_PREGUNTAS:
        problemas.append(f"{len(preguntas)} preguntas detectadas (se esperan {N_PREGUNTAS})")
    numeros = [p["n"] for p in preguntas]
    if numeros != list(range(1, N_PREGUNTAS + 1)):
        problemas.append(f"numeración irregular: {numeros[:25]}")
    for p in preguntas:
        if len(p["opciones"]) != N_OPCIONES:
            problemas.append(f"P{p['n']}: {len(p['opciones'])} opciones (se esperan {N_OPCIONES})")
        if p["solucion"] is None:
            problemas.append(f"P{p['n']}: sin opción [CORRECTA]")
        if not p["enunciado"].strip():
            problemas.append(f"P{p['n']}: sin enunciado")
        for opcion in p["opciones"]:
            if not opcion.strip():
                problemas.append(f"P{p['n']}: opción vacía")
    return problemas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sufijo", default="gemma4-12b")
    ap.add_argument("--modelo", default="gemma4-12b")
    ap.add_argument("--max-intentos", type=int, default=2)
    args = ap.parse_args()

    indice = json.loads(INDICE.read_text(encoding="utf-8"))
    fichero = next(e["fichero"] for e in indice if e["nodo"] == 24)
    original = (RAIZ / "originales" / fichero).read_text(encoding="utf-8")
    previo = RAIZ / "salida" / args.sufijo / fichero
    base_texto = previo.read_text(encoding="utf-8") if previo.exists() else original
    DEST.mkdir(parents=True, exist_ok=True)
    (DEST / "nodo_24_original.md").write_text(original, encoding="utf-8")

    # el original ya está en formato válido: se comprueba para tener la referencia
    original_br = re.sub(r"(?<=\S)\s*(?=[a-d]\)\s)", "<br>", "<br>".join(
        l.strip() for l in original.splitlines() if l.strip()))
    print("cuestionario original:", "válido" if not validar(original_br) else validar(original_br))

    plantilla = PLANTILLA.read_text(encoding="utf-8")
    informe = {"modelo": args.modelo, "intentos": []}
    texto, problemas = "", ["no se ha intentado nada"]
    for intento in range(1, args.max_intentos + 1):
        prompt = (plantilla.replace("{QUIZ}", base_texto) if intento == 1 else
                  plantilla.replace("{QUIZ}", base_texto)
                  + "\n\nATENCIÓN: tu respuesta anterior no servía por esto. Corrígelo y devuelve "
                    "otra vez SOLO el cuestionario completo:\n- " + "\n- ".join(problemas))
        t0 = time.monotonic()
        try:
            resp = pedir(prompt, args.modelo)
        except urllib.error.HTTPError as e:
            print(f"  intento {intento}: FALLO HTTP {e.code} {e.read()[:200]!r}")
            informe["intentos"].append({"intento": intento, "error": f"HTTP {e.code}"})
            break
        segundos = time.monotonic() - t0
        texto = limpiar(resp["choices"][0]["message"].get("content") or "")
        problemas = validar(texto)
        informe["intentos"].append({"intento": intento, "segundos": round(segundos, 1),
                                    "problemas": problemas})
        print(f"  intento {intento}: {segundos:.0f}s · "
              f"{'VÁLIDO' if not problemas else 'INVÁLIDO: ' + '; '.join(problemas[:6])}")
        if not problemas:
            break

    (DEST / "informe.json").write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n",
                                       encoding="utf-8")
    if problemas:
        (DEST / "nodo_24.invalido.txt").write_text(texto + "\n", encoding="utf-8")
        print("\nEl cuestionario NO se sustituye: se conserva el que ya estaba. "
              "Intento fallido en quiz/salida/nodo_24.invalido.txt")
        return 1

    previo.parent.mkdir(parents=True, exist_ok=True)
    crudo = previo.with_suffix(".modelo-raw.md")
    if previo.exists() and not crudo.exists():
        crudo.write_text(previo.read_text(encoding="utf-8"), encoding="utf-8")
    previo.write_text(texto + "\n", encoding="utf-8")
    (DEST / "nodo_24_valido.md").write_text(texto + "\n", encoding="utf-8")
    print(f"\nOK: cuestionario válido (20 preguntas) escrito en salida/{args.sufijo}/{fichero}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
