#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Comprueba el final del nodo de ejercicios y la seccion 9 tras la revision III."""
import re

P = "/mnt/DATA/trabajo_hermes/articulate_hermes/guión_curso_copilot_exelearning.md"
t = open(P, encoding="utf-8").read()

b = [x for x in re.split(r"(?m)^(?=### NODO \d+ — )", t)[1:] if "8 EJERCICIOS" in x.splitlines()[0]][0]
print("=== COLA DEL NODO 15 (ultimos 700 caracteres) ===")
print(b[-700:])
print()
print("=== COLUMNAS DE LA FILA DE CONTENIDO DEL NODO 15 ===")
fila = [l for l in b.splitlines() if l.startswith("| **Contenido en pantalla**")][0]
print("celda empieza:", fila[:60])
print("celda termina:", fila[-60:])
print("<br> en la celda:", fila.count("<br>"))
print()
print("=== SECCION 9 ===")
i = t.index("## 9. INVENTARIO");
j = t.index("## 10. DECISIONES")
print(t[i:j])
print("=== ULTIMAS 3 LINEAS DEL §10 ===")
print("\n".join(t[i:].splitlines()[-3:]))
