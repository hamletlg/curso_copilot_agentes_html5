#!/usr/bin/env python3
"""Vuelca al guion los textos reescritos, los recuadros y las actividades interactivas.

Salvaguarda importante: el generador del curso (generar_curso_elpx.py) localiza los cortes de
cada pagina con literales del texto ("> **Nota:**", "**Sección N:", "**1. Recibir la orden**",
"Un recorrido práctico", "**Pregunta N:**", "[CORRECTA]"...). Si la reescritura se come una de
esas marcas, el montaje revienta o monta otra cosa. Por eso NINGÚN nodo se sustituye sin pasar
antes la comprobación de estructura: el que no la pase se queda como estaba y se avisa.

Uso:
    python3 volcar_guion.py --textos --recuadros --actividades      (lo normal: una sola vez)
    python3 volcar_guion.py --textos --simular                      (no escribe nada, solo informa)

Entradas:
    salida/<sufijo>/nodo_NN_*.md                textos reescritos
    recuadros/salida/nodo_NN.campo.txt          recuadro ya formateado como fila del guion
    ejercicios/salida/nodo_23_intro.md          lo que queda en «Contenido en pantalla»
    ejercicios/salida/nodo_23.campo.txt         la fila «Actividades interactivas»
Salida:
    ../guión_curso_copilot_exelearning.md (con copia de seguridad previa)
    volcado_informe.md
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
GUION = RAIZ.parent / "guión_curso_copilot_exelearning.md"
INDICE = RAIZ / "originales" / "indice.json"
NODO_EJERCICIOS = 23

# Literales que el generador usa con `c.index(...)`: si desaparecen, el montaje lanza ValueError.
LITERALES_CRITICOS = {
    1: ["Un recorrido práctico", "**Duración:**"],
    2: ["### Objetivos del curso"],
    5: ["> **Definición clave:**"],
    6: ["**Tabla de entornos:**"],
    9: ["**1. Recibir la orden**"],
    13: ["> **Pasos para crear un agente:**", "> **Nota:**"],
    16: ["**Conoce las políticas de tu empresa**"],
}

# Estructuras que el generador cuenta o parte: no puede haber menos que en el original.
PATRONES_ESTRUCTURA = [
    r"(?m)^## .+$",
    r"(?m)^### .+$",
    r"\*\*Sección \d+:",
    r"\*\*Pregunta \d+:\*\*",
    r"\[CORRECTA\]",
    r"> \*\*Nota:\*\*",
    r"> \*\*Definición clave:\*\*",
    r"> \*\*Pasos para crear un agente:\*\*",
]

FILA_CONTENIDO = re.compile(r"(?m)^\|\s*\*\*Contenido en pantalla\*\*\s*\|.*\|\s*$")
FILA_RECUADRO = re.compile(r"(?m)^\|\s*\*\*Recuadro de ideas clave\*\*\s*\|.*\|\s*$")
FILA_ACTIVIDADES = re.compile(r"(?m)^\|\s*\*\*Actividades interactivas\*\*\s*\|.*\|\s*$")
CABECERA_NODO = re.compile(r"^### NODO (\d+) — ")

DOC_RECUADRO = (
    "| **Recuadro de ideas clave** | Opcional. Bloque de refuerzo a mitad de página, solo en "
    "algunas páginas. Sintaxis: `**POSICIÓN:** tras «texto de un párrafo o título de la página»"
    "<br><br>**Ideas clave**<br><br>- viñeta<br>- viñeta`. La línea de POSICIÓN no se ve en la "
    "página: es una instrucción de montaje |")
DOC_ACTIVIDADES = (
    "| **Actividades interactivas** | Opcional (página de EJERCICIOS). Bloques que se montan con "
    "iDevices nativos. Cada bloque: `**Bloque N — Test de práctica: <título>**` seguido de "
    "`**Instrucción:**`, `**Feedback correcto:**`, `**Feedback incorrecto:**` y las preguntas "
    "`**Pregunta N:**` con opciones `a)`…`d)` y una sola `[CORRECTA]` (se monta como iDevice Test "
    "no evaluativo); o `**Bloque N — Respuesta abierta: <título>**` con `**Enunciado:**` y "
    "`**Retroalimentación:**` (se monta como iDevice Texto con el botón de retroalimentación) |")

SITEMAP_23_ANTES = ("23. **EJERCICIOS PRÁCTICOS** — 4 ejercicios prácticos con respuestas "
                    "comentadas (autoevaluación).")
SITEMAP_23_DESPUES = ("23. **EJERCICIOS PRÁCTICOS** — 4 ejercicios interactivos: dos test de "
                      "práctica que se corrigen solos (no puntúan para la nota) y dos actividades "
                      "de escritura con respuesta modelo.")
INTERACCION_23_ANTES = ("| **Interacción** | El alumno resuelve los cuatro ejercicios por escrito "
                        "y compara con las respuestas comentadas. Es el nodo de práctica del "
                        "curso. |")
INTERACCION_23_DESPUES = ("| **Interacción** | El alumno resuelve los ejercicios dentro de la "
                          "página: dos test de práctica que corrigen al momento (y no cuentan "
                          "para la evaluación) y dos actividades de escritura con un botón que "
                          "muestra una respuesta modelo. Es el nodo de práctica del curso. |")

REVISION_VII = """> **Revisión del 22-sep-2026 (VII) — reescritura de los textos y refuerzos didácticos:**
> 1. **Los textos de las 25 páginas se reescriben** para que suenen a persona y no a máquina,
>    manteniendo el tono profesional: fuera las frases de folleto, las personificaciones de la
>    tecnología, los paralelismos «no solo… sino también» y los cierres genéricos. Los escribió
>    **Gemma 4 12B** en local (`/mnt/DATA/trabajo_hermes/articulate_hermes/reescritura_humana/`).
>    Se conservan las marcas de estructura que el generador necesita (ver la comprobación de
>    `volcar_guion.py`); la portada conserva el título del curso.
> 2. **Recuadro de ideas clave** (fila nueva, opcional): bloque de refuerzo a mitad de página en
>    **8 de las 25 páginas** (5, 10, 14, 17, 18, 19, 21 y 22), con anclaje por texto y CSS propio
>    coherente con la paleta (`#2563EB` sobre `#F8FAFC`: 4,94:1, AA). No está en todas a propósito:
>    si apareciera en cada página, el alumno dejaría de leerlo.
> 3. **La página de EJERCICIOS deja de ser texto**: los 4 ejercicios se montan con iDevices
>    nativos e interactivos (dos Test de práctica **no evaluativos** y dos respuestas abiertas con
>    el botón de retroalimentación del iDevice Texto). La evaluación final sigue siendo el
>    cuestionario de 20 preguntas con su puntuación y su aviso al LMS.
> 4. Registro de la decisión de fondo (formato intermedio guion → IR en JSON): ver
>    `PROPUESTA_formato_intermedio.md`. Se aborda en la **revisión VIII**.

"""


def campo_desde_markdown(texto: str) -> str:
    """Markdown con saltos reales -> formato del guion (bloques con <br><br>, líneas con <br>)."""
    t = texto.strip()
    t = re.sub(r"[ \t]+\n", "\n", t)
    t = re.sub(r"\n{2,}", "<br><br>", t)
    return t.replace("\n", "<br>")


def comprobar_estructura(nodo: int, original: str, nuevo: str) -> list[str]:
    """Problemas que impedirían montar la página con el texto nuevo."""
    problemas = []
    for literal in LITERALES_CRITICOS.get(nodo, []):
        if literal in original and literal not in nuevo:
            problemas.append(f"ha desaparecido el literal «{literal}» (c.index del generador)")
    for patron in PATRONES_ESTRUCTURA:
        n_orig = len(re.findall(patron, original))
        n_nuevo = len(re.findall(patron, nuevo))
        if n_nuevo < n_orig:
            problemas.append(f"pasan de {n_orig} a {n_nuevo} las coincidencias de {patron}")
    return problemas


def volcar_actividades(parte: str, informe: list[str]) -> tuple[str, int, int]:
    """Página de ejercicios: la intro a «Contenido en pantalla» y los bloques a su fila."""
    intro_f = RAIZ / "ejercicios" / "salida" / "nodo_23_intro.md"
    bloques_f = RAIZ / "ejercicios" / "salida" / "nodo_23.campo.txt"
    if not (intro_f.exists() and bloques_f.exists()):
        informe.append("- NODO 23: SIN ACTIVIDADES reestructuradas, no se toca")
        return parte, 0, 1
    parte = FILA_ACTIVIDADES.sub("", parte).replace("\n\n\n", "\n\n")
    intro = campo_desde_markdown(intro_f.read_text(encoding="utf-8"))
    bloques = bloques_f.read_text(encoding="utf-8").strip()
    if not FILA_CONTENIDO.search(parte):
        informe.append("- NODO 23: sin fila de contenido donde poner la intro")
        return parte, 0, 1
    parte = FILA_CONTENIDO.sub(lambda _: f"| **Contenido en pantalla** | {intro} |", parte, count=1)
    parte = FILA_CONTENIDO.sub(
        lambda m: m.group(0) + f"\n| **Actividades interactivas** | {bloques} |", parte, count=1)
    informe.append(f"- NODO 23: intro de {len(intro)} car. + actividades interactivas "
                   f"({bloques.count('**Bloque ') } bloques)")
    return parte, 1, 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--textos", action="store_true", help="volcar los textos reescritos")
    ap.add_argument("--recuadros", action="store_true", help="volcar los recuadros de ideas clave")
    ap.add_argument("--actividades", action="store_true", help="volcar las actividades del nodo 23")
    ap.add_argument("--sufijo", default="gemma4-12b")
    ap.add_argument("--simular", action="store_true", help="no escribe el guion")
    args = ap.parse_args()
    if not (args.textos or args.recuadros or args.actividades):
        ap.error("indica --textos, --recuadros y/o --actividades")

    indice = json.loads(INDICE.read_text(encoding="utf-8"))
    por_nodo = {e["nodo"]: e["fichero"] for e in indice}
    texto = GUION.read_text(encoding="utf-8")
    partes = re.split(r"(?m)^(?=### NODO )", texto)
    informe: list[str] = []
    aplicados = saltados = 0

    for i, parte in enumerate(partes):
        if i == 0 or not parte.startswith("### NODO "):
            continue
        m_cab = CABECERA_NODO.match(parte)
        if not m_cab:
            continue
        nodo = int(m_cab.group(1))
        fichero = por_nodo.get(nodo)

        if args.textos and fichero:
            original = (RAIZ / "originales" / fichero).read_text(encoding="utf-8")
            reescrito = RAIZ / "salida" / args.sufijo / fichero
            if not reescrito.exists():
                informe.append(f"- NODO {nodo:02d}: SIN REESCRITURA, se queda el texto del guion")
                saltados += 1
            else:
                nuevo = reescrito.read_text(encoding="utf-8")
                problemas = comprobar_estructura(nodo, original, nuevo)
                if problemas:
                    informe.append(f"- NODO {nodo:02d}: NO SE VUELCA — " + "; ".join(problemas))
                    saltados += 1
                else:
                    campo = campo_desde_markdown(nuevo)
                    parte = FILA_CONTENIDO.sub(
                        lambda _, campo=campo: f"| **Contenido en pantalla** | {campo} |",
                        parte, count=1)
                    informe.append(f"- NODO {nodo:02d}: texto volcado "
                                   f"({len(original)} → {len(nuevo)} car.)")
                    aplicados += 1

        if args.recuadros:
            parte = FILA_RECUADRO.sub("", parte).replace("\n\n\n", "\n\n")
            campo_rec = RAIZ / "recuadros" / "salida" / f"nodo_{nodo:02d}.campo.txt"
            if campo_rec.exists():
                campo = campo_rec.read_text(encoding="utf-8").strip()
                if not FILA_CONTENIDO.search(parte):
                    informe.append(f"- NODO {nodo:02d}: recuadro sin fila de contenido donde entrar")
                    saltados += 1
                else:
                    parte = FILA_CONTENIDO.sub(
                        lambda m, campo=campo: m.group(0)
                        + f"\n| **Recuadro de ideas clave** | {campo} |", parte, count=1)
                    ancla_m = re.search(r"«([^»]+)»", campo)
                    informe.append(f"- NODO {nodo:02d}: recuadro añadido "
                                   f"(tras «{ancla_m.group(1) if ancla_m else '?'}»)")
                    aplicados += 1

        if args.actividades and nodo == NODO_EJERCICIOS:
            parte, ok, ko = volcar_actividades(parte, informe)
            aplicados += ok
            saltados += ko

        partes[i] = parte

    nuevo_guion = "".join(partes)

    # §3: documentar los campos nuevos (una sola vez)
    if "**Recuadro de ideas clave**" not in nuevo_guion.split("## 2.")[0] and args.recuadros:
        nuevo_guion = nuevo_guion.replace(
            "| **Contenido en pantalla** | Texto exacto que aparece en el nodo |",
            "| **Contenido en pantalla** | Texto exacto que aparece en el nodo |\n" + DOC_RECUADRO, 1)
        informe.append("- §3: documentado el campo «Recuadro de ideas clave»")
    if "**Actividades interactivas**" not in nuevo_guion.split("## 2.")[0] and args.actividades:
        nuevo_guion = nuevo_guion.replace(DOC_RECUADRO, DOC_RECUADRO + "\n" + DOC_ACTIVIDADES, 1)
        informe.append("- §3: documentado el campo «Actividades interactivas»")

    # cabecera: entrada de la revisión VII
    if args.textos and "Revisión del 22-sep-2026 (VII)" not in nuevo_guion:
        ancla = "> **Revisión del 13-sep-2026 (VI)"
        if ancla in nuevo_guion:
            nuevo_guion = nuevo_guion.replace(ancla, REVISION_VII + ancla, 1)
            informe.append("- cabecera: entrada de la revisión VII")

    # la página de ejercicios ya no es texto: se refleja en el sitemap (§2) y en su fila
    if args.actividades:
        sustituciones = [
            (SITEMAP_23_ANTES, SITEMAP_23_DESPUES),
            (INTERACCION_23_ANTES, INTERACCION_23_DESPUES),
        ]
        for viejo, nuevo in sustituciones:
            if viejo in nuevo_guion:
                nuevo_guion = nuevo_guion.replace(viejo, nuevo, 1)
                informe.append(f"- guion: actualizada una frase de la página 23 ({viejo[:38]}…)")

    if args.simular:
        print("SIMULACIÓN: no se escribe nada\n")
        print("\n".join(informe))
        return 0

    marca = datetime.now(tz=timezone.utc).strftime("%Y%m%d_%H%M%S")
    copia = GUION.parent / "legado_articulate" / "backups_guion" / f"{GUION.name}.bak.{marca}"
    shutil.copy2(GUION, copia)
    GUION.write_text(nuevo_guion, encoding="utf-8")

    (RAIZ / "volcado_informe.md").write_text(
        f"# Volcado al guion ({marca})\n\n"
        f"Fuente de los textos: `salida/{args.sufijo}/`\n\n"
        + "\n".join(informe) + f"\n\nTotal: {aplicados} aplicados, {saltados} saltados.\n",
        encoding="utf-8")
    print("\n".join(informe))
    print(f"\n{aplicados} aplicados, {saltados} saltados")
    print(f"copia de seguridad: {copia}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
