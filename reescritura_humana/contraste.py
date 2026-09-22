#!/usr/bin/env python3
"""Comprueba el contraste WCAG 2.1 de los colores del recuadro de ideas clave.

Uso: python3 contraste.py
Sin dependencias. Fórmula de luminancia relativa de WCAG 2.1 (sRGB).
"""
from __future__ import annotations


def luminancia(color: str) -> float:
    h = color.lstrip("#")
    canales = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    lineales = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in canales]
    return 0.2126 * lineales[0] + 0.7152 * lineales[1] + 0.0722 * lineales[2]


def contraste(a: str, b: str) -> float:
    la, lb = luminancia(a), luminancia(b)
    alto, bajo = max(la, lb), min(la, lb)
    return (alto + 0.05) / (bajo + 0.05)


FONDOS = ["#FFFFFF", "#F8FAFC", "#F1F5F9"]
TEXTOS = ["#1E293B", "#2563EB", "#1D4ED8", "#1E40AF", "#334155"]


def veredicto(r: float) -> str:
    if r >= 4.5:
        return "AA texto normal"
    if r >= 3:
        return "AA solo texto grande"
    return "NO cumple"


def main() -> int:
    for fondo in FONDOS:
        print(f"-- sobre {fondo}:")
        for texto in TEXTOS:
            r = contraste(texto, fondo)
            print(f"   {texto}: {r:.2f}:1  {veredicto(r)}")
    print(f"-- acento #2563EB sobre blanco: {contraste('#2563EB', '#FFFFFF'):.2f}:1")
    print(f"-- blanco sobre #2563EB:        {contraste('#FFFFFF', '#2563EB'):.2f}:1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
