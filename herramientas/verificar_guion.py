#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifica el guion tras aplicar las decisiones: estructura, referencias y coherencia."""
import re

P = "/mnt/DATA/trabajo_hermes/articulate_hermes/guión_curso_copilot_exelearning.md"
t = open(P, encoding="utf-8").read()

nodos = re.findall(r"(?m)^### NODO (\d+) — (.+)$", t)
print("NODOS:", len(nodos))
for n, tt in nodos:
    print(f"  {n:>2}  {tt}")

print("\nSECCIONES:", re.findall(r"(?m)^## .+$", t))

# referencias cruzadas
refs = {}
for m in re.finditer(r"(?i)\bNodos?\s+(\d+(?:\s*[–-]\s*\d+)?(?:\s*(?:,|y)\s*\d+(?:\s*[–-]\s*\d+)?)*)", t):
    for num in re.findall(r"\d+", m.group(1)):
        refs.setdefault(int(num), 0)
        refs[int(num)] += 1
fuera = {k: v for k, v in refs.items() if not (1 <= k <= 17)}
print("\nREFERENCIAS a nodos 1-17:", dict(sorted(refs.items())))
print("REFERENCIAS FUERA DE RANGO:", fuera if fuera else "ninguna")

# coherencia de las referencias contextuales clave
checks = [
    ("tipos de agente (P4)", "Nodo 6 (tipos de agente)", "Nodo 6 (tipos de agente)"),
    ("evaluacion final", "Nodo 16 (evaluación final)", "Nodo 16 (evaluación final)"),
    ("resumen/glosario", "Nodo 17", "Nodo 17"),
]
print("\nCOMPROBACIONES DE CONTEXTO:")
for etiqueta, aguja, esperado in checks:
    print(f"  {etiqueta:28} '{aguja}' -> {'OK' if esperado in t else 'FALTA'}")

# el mapa recurso -> nodo
print("\nMAPA NODO -> RECURSO")
for b in re.split(r"(?m)^(?=### NODO \d+ — )", t)[1:]:
    titulo = b.splitlines()[0].replace("### ", "")
    m = re.search(r"(?m)^\| \*\*Recurso gráfico\*\* \| (.+?) \|$", b)
    fila = m.group(1) if m else "(SIN FILA)"
    arch = re.findall(r"`recursos/imagenes/([^`]+)`", fila)
    print(f"  {titulo[:48]:<49} | {'ninguno' if fila.startswith('Ninguno') else ', '.join(arch)}")

# iDevices declarados por nodo
print("\nIDEVICES POR NODO")
total = 0
for b in re.split(r"(?m)^(?=### NODO \d+ — )", t)[1:]:
    titulo = b.splitlines()[0].replace("### ", "")
    m = re.search(r"(?m)^\| \*\*iDevice\(s\)\*\* \| (.+?) \|$", b)
    if not m:
        print(f"  {titulo[:48]:<49} | FALTA FILA")
        continue
    print(f"  {titulo[:48]:<49} | {m.group(1)[:90]}")

# el sitemap cuadra con los titulos
print("\nSITEMAP vs TITULOS")
sitemap = t[t.index("## 2. ESTRUCTURA"):t.index("## 3. FORMATO")]
lines = re.findall(r"(?m)^\s*(\d+)\. \*\*(.+?)\*\*(.*)$", sitemap)
for i, (num, nombre, resto) in enumerate(lines, 1):
    titulo = nodos[i - 1][1] if i <= len(nodos) else "?"
    ok = "OK" if nombre.split("—")[-1].strip().lower()[:12] in titulo.lower() or titulo.lower()[:12] in nombre.lower() else "REVISAR"
    print(f"  {num:>2} {nombre[:46]:<47} | guion: {titulo[:40]:<41} | {ok}")

# ejercicios
print("\nEJERCICIOS:", re.findall(r"### (Ejercicio \d+):? ([^<]*)", t))

# restos de numeracion antigua sospechosa
print("\nAVISOS:")
for pat in ["15 nodos", "26 iDevices", "Nodo 13 —", "NODO 13", "NODO 14", "NODO 15 —", "4 ejercicios", "nodos 6 y 7"]:
    c = t.count(pat)
    if c:
        print(f"  {pat!r}: {c}")
print("  marcadores <br>:", t.count("<br>"), " | ⚠️:", t.count("⚠️"))
print("  filas Recurso gráfico:", t.count("| **Recurso gráfico** |"))
print("  caracteres:", len(t), " lineas:", t.count("\n") + 1)
