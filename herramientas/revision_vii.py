#!/usr/bin/env python3
"""Revisión VII — sincroniza el maestro con el texto reescrito del guion.

Qué hace, en orden y con copia de seguridad previa:

  1. Lee los 25 nodos del guion con **el mismo analizador que usa el generador del curso**
     (`generar_curso_elpx.extraer_nodos`): contenido en pantalla, recuadro de ideas clave y
     actividades interactivas. Así el maestro no puede divergir de lo que se monta.
  2. Reescribe el cuerpo de cada «### PÁGINA n — …» del maestro con ese texto, convertido a prosa
     con la misma función que usó la revisión VI (`revision_vi.guion_a_maestro`).
  3. Añade el recuadro de ideas clave como bloque propio de su página (con la posición de montaje) y,
     en la página 23, las cuatro actividades interactivas con su respuesta modelo.
  4. Actualiza la cabecera: la línea **Revisión:** y la nota de relación con el guion.
  5. No toca nada más: los anexos, la estructura resumida, el mapa del Art. 4 y las secciones §5-§10
     se conservan tal cual (se comprueba que salen byte a byte iguales).

Uso:
    python3 herramientas/revision_vii.py --dry-run     # comprueba y resume, sin escribir
    python3 herramientas/revision_vii.py               # aplica
"""
from __future__ import annotations

import argparse
import pathlib
import re
import shutil
import sys
from datetime import datetime

AQUI = pathlib.Path(__file__).resolve().parent
RAIZ = AQUI.parent
sys.path.insert(0, str(AQUI))

import generar_curso_elpx as gen
from revision_vi import (
    guion_a_maestro,
)

MAESTRO = RAIZ / "contenido_curso_copilot_agentes.md"
BACKUPS = RAIZ / "legado_articulate" / "backups_guion"
RE_PAGINA = re.compile(r"(?m)^### PÁGINA (\d+) — ([^\n]+)\n")
# Donde empieza la cola técnica del documento (dentro del cuerpo de la última página).
MARCA_COLA = "### 5. RESUMEN DE IDEVICES USADOS"
N_PAGINAS = 25

CABECERA_REVISION = (
    "**Revisión:** 22-sep-2026 (revisión VII: textos reescritos, recuadros de ideas clave y\n"
    "ejercicios interactivos).\n"
)
CABECERA_REVISION_VIEJA = (
    "**Revisión:** 13-sep-2026 (revisión VI: remediación de cumplimiento del Art. 4 del AI Act).\n"
)

NOTA_RELACION = """> **Relación con el guion.** Este documento es la **fuente de verdad del contenido**. Desde la
> revisión VI su texto y el de `guión_curso_copilot_exelearning.md` son el mismo: el maestro se
> deriva del guion con `herramientas/revision_vi.py` (revisión VI) y `herramientas/revision_vii.py`
> (revisión VII, que añade los recuadros de ideas clave y las actividades interactivas). Si hay que
> cambiar contenido, se cambia en el guion y se vuelve a ejecutar el script de la revisión; el
> verificador de esta última comprueba página a página que no se ha perdido ni una palabra.
>"""


def bloques_del_maestro(texto: str):
    """(cabecera, {n: (titulo, cuerpo)}, cola) del maestro, sin tocar nada."""
    i_cola = texto.index(MARCA_COLA)
    cabecera_y_paginas, cola = texto[:i_cola], texto[i_cola:]
    m = RE_PAGINA.search(cabecera_y_paginas)
    if not m:
        raise SystemExit("el maestro no tiene ninguna página «### PÁGINA n — …»")
    cabecera = cabecera_y_paginas[: m.start()]
    trozos = RE_PAGINA.split(cabecera_y_paginas[m.start():])
    paginas = {}
    for i in range(1, len(trozos), 3):
        numero, titulo, cuerpo = int(trozos[i]), trozos[i + 1].strip(), trozos[i + 2]
        paginas[numero] = (titulo, cuerpo.strip().rstrip("-").strip())
    return cabecera, paginas, cola


def bloque_recuadro(campo: str) -> str:
    """El recuadro del guion como bloque del maestro, con su posición de montaje."""
    ancla = gen.ANCLA_RECUADRO.search(campo.split("**")[0] or campo)
    cuerpo = gen.texto_recuadro(campo).strip()
    cuerpo = re.sub(r"^(\*\*.+?\*\*)\s*(?:<br\s*/?>)?\s*", r"", cuerpo, count=1)
    vinietas = [l.strip() for l in cuerpo.replace("<br><br>", "\n").replace("<br>", "\n").splitlines()
                if l.strip()]
    salida = ["**Ideas clave** — *recuadro de refuerzo que se monta a mitad de página*", ""]
    if ancla:
        salida.append(f"*Posición:* tras «{ancla.group(1).strip()}».")
        salida.append("")
    salida.extend(vinietas)
    return "\n".join(salida) + "\n"


def bloque_actividades(campo: str) -> str:
    """Las actividades de la página de ejercicios, legibles y con su respuesta modelo."""
    texto = campo.strip().replace("<br><br>", "\n\n").replace("<br>", "\n")
    texto = texto.replace("[CORRECTA]", "  ← **correcta**")
    # el guion separa cada línea con <br>: aquí se respira un poco más (blanco antes de cada bloque
    # y de cada pregunta) para que el maestro se pueda leer de un tirón
    lineas = []
    for linea in texto.splitlines():
        if re.match(r"^\*\*(Bloque \d+|Pregunta \d+)", linea):
            lineas.append("")
        lineas.append(linea)
    texto = re.sub(r"\n{3,}", "\n\n", "\n".join(lineas)).strip()
    return ("### Actividades interactivas\n\n"
            "Las cuatro actividades se montan como iDevices nativos: los dos test de práctica se\n"
            "corrigen y explican solos (no puntúan) y las dos respuestas abiertas llevan su\n"
            "respuesta modelo en un botón de retroalimentación.\n\n"
            + texto.strip() + "\n")


def construir_maestro(dry: bool) -> str:
    nodos = gen.extraer_nodos()
    if len(nodos) != N_PAGINAS:
        raise SystemExit(f"el guion tiene {len(nodos)} nodos (se esperaban {N_PAGINAS})")
    original = MAESTRO.read_text(encoding="utf-8")
    cabecera, paginas, cola = bloques_del_maestro(original)
    if sorted(paginas) != list(range(1, N_PAGINAS + 1)):
        raise SystemExit(f"el maestro no tiene las páginas 1..{N_PAGINAS}: {sorted(paginas)}")

    # idempotente: la primera vez cambia la línea de revisión, las siguientes la deja como está
    if CABECERA_REVISION_VIEJA in cabecera:
        cabecera = cabecera.replace(CABECERA_REVISION_VIEJA, CABECERA_REVISION, 1)
    elif CABECERA_REVISION not in cabecera:
        raise SystemExit("no encuentro la línea «**Revisión:**» en la cabecera del maestro")
    cabeza_nota = re.search(r"(?ms)^> \*\*Relación con el guion\.\*\*.*?(?=\n> \*\*Qué cubre)", cabecera)
    if not cabeza_nota:
        raise SystemExit("no encuentro la nota «Relación con el guion» en la cabecera")
    cabecera = cabecera[: cabeza_nota.start()] + NOTA_RELACION + cabecera[cabeza_nota.end():]

    partes, informe = [], []
    for nodo in nodos:
        n = nodo["nodo"]
        titulo, _ = paginas[n]
        cuerpo = guion_a_maestro(nodo["contenido"])
        if nodo.get("recuadro"):
            cuerpo += "\n\n" + bloque_recuadro(nodo["recuadro"]).rstrip()
        if nodo.get("actividades_texto"):
            cuerpo += "\n\n" + bloque_actividades(nodo["actividades_texto"]).rstrip()
        partes.append(f"### PÁGINA {n} — {titulo}\n\n{cuerpo}\n\n---\n\n")
        informe.append((n, titulo, len(cuerpo)))

    nuevo = cabecera + "".join(partes) + cola

    # --- comprobaciones
    _, paginas_nuevas, cola_nueva = bloques_del_maestro(nuevo)
    if len(paginas_nuevas) != N_PAGINAS:
        raise SystemExit(f"el maestro resultante tiene {len(paginas_nuevas)} páginas")
    if cola_nueva != cola:
        raise SystemExit("la cola técnica (§5-§10) ha cambiado: no debe tocarse")
    problemas = []
    for nodo in nodos:
        n = nodo["nodo"]
        fuente = (nodo["contenido"] + " " + gen.texto_recuadro(nodo.get("recuadro") or "")
                  + " " + gen.texto_actividades(nodo.get("actividades_texto") or ""))
        # se compara contra el título de la página y su cuerpo: el guion quita el título suelto
        # del campo («## Ejercicios prácticos») porque en el maestro lo pone la cabecera.
        destino = paginas_nuevas[n][0] + " " + paginas_nuevas[n][1]
        faltan = sorted(gen.significativas(fuente) - gen.significativas(destino))
        if faltan:
            problemas.append((n, faltan[:8]))
    if problemas:
        raise SystemExit("texto del guion que no llega al maestro: " + str(problemas))
    for prohibido in ("2 horas", "$21", "usuario/mes", "Copilot Pro", "Copilot Chat"):
        if prohibido in nuevo:
            raise SystemExit(f"«{prohibido}» sigue en el maestro")

    if not dry:
        BACKUPS.mkdir(parents=True, exist_ok=True)
        sello = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(MAESTRO, BACKUPS / f"contenido_curso_copilot_agentes.md.bak.{sello}")
        MAESTRO.write_text(nuevo, encoding="utf-8")

    for n, titulo, largo in informe:
        extra = []
        nodo = next(x for x in nodos if x["nodo"] == n)
        if nodo.get("recuadro"):
            extra.append("recuadro")
        if nodo.get("actividades_texto"):
            extra.append("actividades")
        print(f"  PÁGINA {n:>2} — {titulo[:46]:<46} {largo:>6} car."
              + (f"  [{', '.join(extra)}]" if extra else ""))
    print(f"\nMAESTRO: {N_PAGINAS} páginas, {len(nuevo)} caracteres, cola técnica intacta"
          + ("" if dry else " -> escrito (copia previa en legado_articulate/backups_guion/)"))
    return nuevo


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="no escribe nada")
    args = ap.parse_args()
    construir_maestro(args.dry_run)
    return 0


if __name__ == "__main__":
    sys.exit(main())
