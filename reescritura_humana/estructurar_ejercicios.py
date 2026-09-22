#!/usr/bin/env python3
"""Convierte la página de EJERCICIOS PRÁCTICOS en actividades interactivas con el modelo local.

El modelo reestructura los 4 ejercicios al formato de la fila «Actividades interactivas» del guion
(Test de práctica + Respuesta abierta). El resultado NO se da por bueno porque el modelo lo diga:
se valida con el parser REAL del generador (`generar_curso_elpx.parse_actividades`), que es el que
va a montar la página. Si no parsea, se reintenta una vez con el error delante y, si vuelve a
fallar, no se escribe nada.

Uso:
    python3 estructurar_ejercicios.py --sufijo gemma4-12b
    python3 estructurar_ejercicios.py --sufijo gemma4-12b --modelo gemma4-12b --max-intentos 2

Entrada : salida/<sufijo>/nodo_23_*.md          (el texto reescrito de la página)
Salida  : ejercicios/salida/nodo_23_intro.md    (lo que queda en «Contenido en pantalla»)
          ejercicios/salida/nodo_23_bloques.md  (la fila «Actividades interactivas»)
          ejercicios/salida/nodo_23.campo.txt   (la fila lista para pegar en el guion)
          ejercicios/salida/informe.json
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

PLANTILLA = RAIZ / "prompts" / "ejercicios_interactivos.md"
DEST = RAIZ / "ejercicios" / "salida"
BASE = "http://127.0.0.1:8080"
MAX_TOKENS = 4000
CABECERA_EJERCICIO = re.compile(r"(?m)^#{2,4}\s+Ejercicio\s+1\b")


def extraer_intro(pagina: str) -> str:
    """La introducción es lo que va antes del primer «### Ejercicio 1»: no la toca el modelo."""
    m = CABECERA_EJERCICIO.search(pagina)
    intro = (pagina[:m.start()] if m else pagina).strip()
    intro = re.sub(r"(?m)^-{3,}\s*$", "", intro).strip()
    return intro


def pedir(prompt: str, modelo: str, timeout: int = 600) -> dict:
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
    m = re.search(r"\*\*Bloque 1 ", t)
    if m:
        t = t[m.start():]
    # cada bloque es un párrafo con <br> dentro: los saltos reales pasan a <br>
    bloques = re.split(r"\n(?=\*\*Bloque \d+ )", t)
    return "<br><br>".join(b.strip().replace("\n", "<br>") for b in bloques if b.strip())


def validar(campo: str) -> tuple[list[dict], list[str]]:
    """Valida con el parser real del generador, que es el que va a montar la página."""
    try:
        bloques = gen.parse_actividades(campo)
    except ValueError as exc:
        return [], [str(exc)]
    problemas = []
    esperado = {1: ("test", 5), 2: ("abierta", None), 3: ("test", 5), 4: ("abierta", None)}
    if len(bloques) != 4:
        problemas.append(f"{len(bloques)} bloques (se esperan 4)")
    for b in bloques:
        tipo, n = esperado.get(b["orden"], (None, None))
        if tipo and b["tipo"] != tipo:
            problemas.append(f"bloque {b['orden']}: es «{b['tipo']}» y debería ser «{tipo}»")
        if n and len(b.get("preguntas", [])) != n:
            problemas.append(f"bloque {b['orden']}: {len(b.get('preguntas', []))} preguntas "
                             f"(se esperan {n})")
        if b["tipo"] == "abierta":
            if len(b["enunciado"]) < 40:
                problemas.append(f"bloque {b['orden']}: enunciado demasiado corto")
            if len(b["retro"]) < 120:
                problemas.append(f"bloque {b['orden']}: retroalimentación demasiado corta")
    return bloques, problemas


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sufijo", default="gemma4-12b")
    ap.add_argument("--modelo", default="gemma4-12b")
    ap.add_argument("--max-intentos", type=int, default=2)
    ap.add_argument("--reusar-invalido", action="store_true",
                    help="valida el fichero nodo_23.invalido.txt en vez de volver a preguntar")
    args = ap.parse_args()

    fichero = next(iter(sorted((RAIZ / "salida" / args.sufijo).glob("nodo_23_*.md"))), None)
    if fichero is None:
        print(f"no encuentro la página 23 en salida/{args.sufijo}/")
        return 1
    pagina = fichero.read_text(encoding="utf-8")
    intro = extraer_intro(pagina)
    plantilla = PLANTILLA.read_text(encoding="utf-8")
    DEST.mkdir(parents=True, exist_ok=True)

    base = plantilla.replace("{PAGINA}", pagina)
    informe = {"fichero": fichero.name, "modelo": args.modelo, "intentos": []}
    campo, problemas = "", []

    if args.reusar_invalido:
        previo = DEST / "nodo_23.invalido.txt"
        if not previo.exists():
            print("no hay nodo_23.invalido.txt que reutilizar")
            return 1
        campo = previo.read_text(encoding="utf-8").strip()
        _, problemas = validar(campo)
        informe["intentos"].append({"intento": 0, "reutilizado": previo.name,
                                    "problemas": problemas})
        print(f"  reutilizando {previo.name}: {'VÁLIDO' if not problemas else 'INVÁLIDO: ' + '; '.join(problemas)}")

    for intento in range(1, args.max_intentos + 1) if problemas else []:
        prompt = base if intento == 1 else (
            base + "\n\nATENCIÓN: tu respuesta anterior no servía por estos motivos. "
                   "Corrígelos y devuelve otra vez SOLO los bloques:\n- " + "\n- ".join(problemas))
        t0 = time.monotonic()
        try:
            resp = pedir(prompt, args.modelo)
        except urllib.error.HTTPError as e:
            print(f"  intento {intento}: FALLO HTTP {e.code} {e.read()[:200]!r}")
            informe["intentos"].append({"intento": intento, "error": f"HTTP {e.code}"})
            break
        segundos = time.monotonic() - t0
        bruto = resp["choices"][0]["message"].get("content") or ""
        campo = limpiar(bruto)
        bloques, problemas = validar(campo)
        informe["intentos"].append({"intento": intento, "segundos": round(segundos, 1),
                                    "problemas": problemas,
                                    "bloques": [{"orden": b["orden"], "tipo": b["tipo"],
                                                 "titulo": b["titulo"],
                                                 "preguntas": len(b.get("preguntas", []))}
                                                for b in bloques]})
        print(f"  intento {intento}: {segundos:.0f}s · "
              f"{'VÁLIDO' if not problemas else 'INVÁLIDO: ' + '; '.join(problemas)}")
        if not problemas:
            break

    if problemas:
        (DEST / "nodo_23.invalido.txt").write_text(campo + "\n", encoding="utf-8")
        (DEST / "informe.json").write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n",
                                           encoding="utf-8")
        print("\nLa página de ejercicios NO se ha reestructurado. Respuesta inválida guardada en "
              "ejercicios/salida/nodo_23.invalido.txt")
        return 1

    (DEST / "nodo_23_intro.md").write_text(intro + "\n", encoding="utf-8")
    (DEST / "nodo_23_bloques.md").write_text(campo + "\n", encoding="utf-8")
    (DEST / "nodo_23.campo.txt").write_text(campo + "\n", encoding="utf-8")
    (DEST / "informe.json").write_text(json.dumps(informe, ensure_ascii=False, indent=2) + "\n",
                                       encoding="utf-8")
    print(f"\nOK: 4 bloques válidos. Intro de {len(intro)} car., bloques de {len(campo)} car.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
