#!/usr/bin/env python3
"""Comprobaciones de consistencia del guion + patrones de descarga de StockSnap."""
import re
import urllib.request

RUTA = "/mnt/DATA/trabajo_hermes/articulate_hermes/guión_curso_copilot_exelearning.md"
t = open(RUTA, encoding="utf-8").read()

print("=== CONSISTENCIA DEL GUION ===")
print("caracteres:", len(t))
print("nodos (### NODO):", len(re.findall(r"(?m)^### NODO ", t)))
print("filas iDevice(s):", len(re.findall(r"(?m)^\| \*\*iDevice\(s\)\*\* \|", t)))
print("filas Recurso gráfico:", len(re.findall(r"(?m)^\| \*\*Recurso gráfico\*\* \|", t)))
print("menciones de texto alternativo:", t.count("Texto alternativo"))
print("archivos de recursos citados:")
for f in sorted(set(re.findall(r"recursos/imagenes/[A-Za-z0-9_]+\.(?:png|jpg|svg|md)", t))):
    print("   ", f, "->", t.count(f), "veces")
print("referencias a CREDITOS.md:", t.count("CREDITOS.md"))
print("quedan avisos ⚠️:", t.count("⚠️"))
print("puntos de verificación ✅:", t.count("✅"))

print("\n=== PATRONES DE DESCARGA STOCKSNAP (con User-Agent) ===")
hdr = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/120 Safari/537.36"}
for pat in ["https://cdn.stocksnap.io/img-thumbs/960w/DWLWL9USBG.jpg",
            "https://cdn.stocksnap.io/img-thumbs/1920w/DWLWL9USBG.jpg",
            "https://cdn.stocksnap.io/img-thumbs/orig/DWLWL9USBG.jpg",
            "https://cdn.stocksnap.io/img-thumbs/2800w/DWLWL9USBG.jpg"]:
    try:
        req = urllib.request.Request(pat, headers=hdr)
        r = urllib.request.urlopen(req, timeout=25)
        data = r.read()
        from PIL import Image
        import io
        with Image.open(io.BytesIO(data)) as im:
            print(f"  {pat.split('/')[-2]}/{pat.split('/')[-1]}: OK {im.size} {len(data)//1024} KB")
    except Exception as e:
        print(f"  {pat.split('/')[-2]}: FALLO {type(e).__name__} {e}")
