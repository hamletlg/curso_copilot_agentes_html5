#!/bin/sh
# Publica la vista previa del curso en docs/ — lo que sirve GitHub Pages.
#
# Uso:
#     sh herramientas/exportar.sh        # 1) genera .elpx + SCORM 1.2 + HTML5 + entregables/html5_preview/
#     sh herramientas/publicar_docs.sh   # 2) copia esa vista previa a docs/ (demo navegable)
#
# En GitHub: Settings → Pages → Source: «Deploy from a branch», Branch: main, carpeta /docs.
# El curso queda navegable en https://<usuario>.github.io/<repositorio>/
set -e

RAIZ=$(cd "$(dirname "$0")/.." && pwd)
ORIGEN="$RAIZ/entregables/html5_preview"
DESTINO="$RAIZ/docs"

if [ ! -f "$ORIGEN/index.html" ]; then
    echo "Falta $ORIGEN/index.html." >&2
    echo "Ejecuta antes: sh herramientas/exportar.sh" >&2
    exit 1
fi

rm -rf "$DESTINO"
mkdir -p "$DESTINO"
cp -a "$ORIGEN/." "$DESTINO/"

echo "OK: demo actualizada en docs/ ($(find "$DESTINO" -type f | wc -l | tr -d ' ') archivos, $(du -sh "$DESTINO" | cut -f1))"
echo "    Navegable en local con: python3 -m http.server -d docs"
