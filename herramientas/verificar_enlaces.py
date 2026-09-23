#!/usr/bin/env python3
"""Comprueba que todos los recursos locales de un export HTML5 existen.

Recorre las páginas, hojas de estilo y scripts del paquete y resuelve cada `src`/`href` relativo
contra el directorio del fichero que lo referencia (las páginas viven en `html/` y apuntan a
`../content/...`, así que resolverlo todo desde la raíz daría falsos positivos). Ignora URLs
externas, anclas, `data:` y las plantillas JS (`${path}...` del iDevice quick-questions).

Uso:
    python3 herramientas/verificar_enlaces.py <directorio>
Salida: una línea de resumen; sale con 1 si hay alguna referencia rota.
"""
import pathlib
import re
import sys

PATRON = re.compile(r'(?:src|href)\s*=\s*["\']([^"\']+)["\']')
EXTERNOS = ("http", "//", "data:", "mailto:", "#", "javascript:")
SUFIJOS = (".html", ".htm", ".css", ".js")


def verificar(raiz: pathlib.Path) -> tuple[int, list[tuple[str, str]]]:
    total = 0
    rotas: list[tuple[str, str]] = []
    for fichero in sorted(raiz.rglob("*")):
        if not fichero.is_file() or fichero.suffix.lower() not in SUFIJOS:
            continue
        texto = fichero.read_text(encoding="utf-8", errors="replace")
        for m in PATRON.finditer(texto):
            url = m.group(1).strip()
            if not url or url.startswith(EXTERNOS) or "${" in url:
                continue
            url = url.split("#")[0].split("?")[0]
            if not url:
                continue
            total += 1
            if not (fichero.parent / url).resolve().exists():
                rotas.append((str(fichero.relative_to(raiz)), url))
    return total, rotas


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    raiz = pathlib.Path(sys.argv[1])
    if not raiz.is_dir():
        raise SystemExit(f"no es un directorio: {raiz}")
    total, rotas = verificar(raiz)
    if rotas:
        print(f"  MAL {len(rotas)} referencia(s) local(es) rota(s) de {total}:")
        for fichero, url in rotas[:20]:
            print(f"      {fichero} -> {url}")
        return 1
    print(f"  ok  {total} referencias locales, 0 rotas")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
