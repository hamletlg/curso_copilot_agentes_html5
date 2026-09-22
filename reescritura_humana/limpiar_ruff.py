#!/usr/bin/env python3
"""Deja limpios de ruff los scripts de reescritura_humana (arreglos mecánicos, una sola vez)."""
from __future__ import annotations

import stat
from pathlib import Path

RAIZ = Path(__file__).resolve().parent

# 1) shebang -> ficheros ejecutables
for p in RAIZ.glob("*.py"):
    p.chmod(p.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

# 2) alias de re
f = RAIZ / "escribir_recuadros.py"
t = f.read_text(encoding="utf-8")
t = t.replace("recuadro, re.I)", "recuadro, re.IGNORECASE)").replace(
    'recuadro, re.I):', 'recuadro, re.IGNORECASE):')
f.write_text(t, encoding="utf-8")

# 3) noqa inútil
for nombre in ("estructurar_ejercicios.py", "reescribir_quiz.py"):
    f = RAIZ / nombre
    t = f.read_text(encoding="utf-8")
    t = t.replace("import generar_curso_elpx as gen  # noqa: E402",
                  "import generar_curso_elpx as gen")
    f.write_text(t, encoding="utf-8")

# 4) lambdas que capturaban la variable del bucle
f = RAIZ / "volcar_guion.py"
t = f.read_text(encoding="utf-8")
t = t.replace('lambda _: f"| **Contenido en pantalla**',
              'lambda _, campo=campo: f"| **Contenido en pantalla**')
t = t.replace(r'lambda m: m.group(0) + f"\n| **Recuadro de ideas clave**',
              r'lambda m, campo=campo: m.group(0) + f"\n| **Recuadro de ideas clave**')
# 5) datetime con zona horaria
t = t.replace("from datetime import datetime", "from datetime import datetime, timezone")
t = t.replace("marca = datetime.now().strftime", "marca = datetime.now(tz=timezone.utc).strftime")
f.write_text(t, encoding="utf-8")

print("arreglos aplicados")
