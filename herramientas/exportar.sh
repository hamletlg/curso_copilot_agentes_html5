#!/bin/sh
# Exporta el curso con el CLI de eXeLearning (sin navegador) y reconstruye la vista previa.
#
# Uso:
#     python3 herramientas/generar_curso_elpx.py     # 1) guion -> content.xml (+ .elpx mínimo)
#     sh herramientas/exportar.sh                    # 2) -> .elpx completo + SCORM 1.2 + HTML5
#     python3 herramientas/verificar_paquete.py      # 3) comprobaciones
#
# El `.elpx` entregable se produce aquí (formato `elpx` del CLI): es el paquete completo, con tema
# Nova, html renderizado e iDevices, y se puede abrir directamente en eXeLearning.
set -e

CONT=exelearning
RAIZ=$(cd "$(dirname "$0")/.." && pwd)
ENT="$RAIZ/entregables"
MIN="$ENT/_trabajo/curso_copilot_agentes_minimo.elpx"

if [ ! -f "$MIN" ]; then
    echo "Falta $MIN" >&2
    echo "Ejecuta antes: python3 herramientas/generar_curso_elpx.py" >&2
    exit 1
fi

podman cp "$MIN" "$CONT:/tmp/curso_entrada.elpx"
for f in elpx scorm12 html5; do
    podman exec "$CONT" sh -c "cd /app && bun dist/cli.js elp:export /tmp/curso_entrada.elpx /tmp/curso_out_$f $f" >/dev/null
    echo "export $f: OK"
done

podman cp "$CONT:/tmp/curso_out_elpx.elpx" "$ENT/curso_copilot_agentes.elpx"
podman cp "$CONT:/tmp/curso_out_scorm12.zip" "$ENT/curso_copilot_agentes_scorm12.zip"
podman cp "$CONT:/tmp/curso_out_html5.zip" "$ENT/curso_copilot_agentes_html5.zip"

# post-proceso (idempotente): el exportador SCORM 1.2 ignora pp_extraHeadContent y Nova fija la
# navegación arriba a la derecha; aquí se inyecta el CSS del proyecto y se lleva el «Anterior /
# Siguiente» al pie en las tres salidas (también en el .elpx, para que la app lo vea igual).
python3 "$RAIZ/herramientas/postproceso_export.py" \
    "$ENT/curso_copilot_agentes.elpx" \
    "$ENT/curso_copilot_agentes_scorm12.zip" \
    "$ENT/curso_copilot_agentes_html5.zip"

# vista previa HTML5 descomprimida (para inspeccionar y para las pruebas de interacción)
# La anterior no se borra: se archiva en entregables/historial/.
if [ -d "$ENT/html5_preview" ]; then
    mkdir -p "$ENT/historial"
    mv "$ENT/html5_preview" "$ENT/historial/html5_preview_$(date +%Y%m%d%H%M%S)"
fi
mkdir -p "$ENT/html5_preview"
cd "$ENT/html5_preview" && unzip -q "$ENT/curso_copilot_agentes_html5.zip"

echo "OK: .elpx + SCORM 1.2 + HTML5 en entregables/ y vista previa reconstruida"
