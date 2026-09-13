#!/usr/bin/env python3
"""Informe final: mapa nodo -> recurso tal como quedó en el guion."""
import re

RUTA = "/mnt/DATA/trabajo_hermes/articulate_hermes/guión_curso_copilot_exelearning.md"
t = open(RUTA, encoding="utf-8").read()
bloques = re.split(r"(?m)^(?=### NODO \d+ —)", t)[1:]

print("NODO -> RECURSO (resumen del mapa aplicado)")
print("-" * 78)
for b in bloques:
    titulo = b.splitlines()[0].replace("### ", "")
    m = re.search(r"(?m)^\| \*\*Recurso gráfico\*\* \| (.+?) \|$", b)
    fila = m.group(1) if m else "(sin fila)"
    archivos = re.findall(r"`recursos/imagenes/([^`]+)`", fila)
    alt = re.findall(r"Texto alternativo[^«]*«([^»]+)»", fila)
    estado = "ninguno" if fila.startswith("Ninguno") else ", ".join(archivos)
    print(f"{titulo[:46]:<47} | {estado}")
    for a in alt:
        print(f"{'':47} |   alt: {a[:80]}")
print("-" * 78)
print("total nodos:", len(bloques))
