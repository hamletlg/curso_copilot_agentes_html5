#!/usr/bin/env python3
"""Muestra los nombres de pagina y titulos que el generador está produciendo."""
import re
import pathlib

xml = pathlib.Path('/mnt/DATA/trabajo_hermes/articulate_hermes/entregables/content.xml').read_text(encoding='utf-8')
paginas = re.findall(r"<odeNavStructure>(.*?)</odeNavStructure>", xml, re.S)
print(f"{'#':>3}  {'pageName (arbol)':<52} titlePage (H1)")
for p in paginas:
    nombre = re.search(r"<pageName>(.*?)</pageName>", p).group(1)
    titulo = re.search(r"<key>titlePage</key><value>(.*?)</value>", p).group(1)
    print(f"{len(nombre):>3}  {nombre:<52} {titulo}")
