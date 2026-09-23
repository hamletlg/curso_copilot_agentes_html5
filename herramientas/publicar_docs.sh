#!/bin/sh
# Publica la versión FINAL del curso en docs/ — lo que sirve GitHub Pages.
#
# Uso:
#     sh herramientas/exportar.sh                    # 1) regenera .elpx + SCORM 1.2 + HTML5 (con los ajustes)
#     sh herramientas/publicar_docs.sh               # 2) copia el HTML5 final a docs/ (demo navegable)
#     sh herramientas/publicar_docs.sh --verificar   # solo comprueba, sin tocar nada
#     sh herramientas/publicar_docs.sh --push        # además commitea y empuja a GitHub (Pages se reconstruye)
#
# En GitHub: Settings → Pages → Source: «Deploy from a branch», Branch: main, carpeta /docs.
# El curso queda navegable en https://hamletlg.github.io/curso_copilot_agentes_html5/
#
# Guardas (por qué este script no publica una revisión antigua):
#   1. El origen es SIEMPRE el paquete descomprimido entregable
#      (`entregables/curso_copilot_agentes_html5/`), no una vista previa intermedia que pueda
#      quedarse de una exportación anterior.
#   2. Aborta si ese paquete no lleva aplicados los ajustes del curso (menú con memoria, test como
#      evaluación, veredicto del 70 %): busca la marca «ajustes del curso» en las páginas.
#   3. Aborta si el paquete descomprimido y el `.zip` entregable no coinciden (`index.html`):
#      evita publicar una carpeta desincronizada del zip. `--forzar` salta 2 y 3 a sabiendas.
#   4. `docs/` se REEMPLAZA entero (no se fusiona): así no sobreviven páginas de revisiones previas.
#   5. Después de copiar, verifica: md5 origen == md5 docs, 0 referencias locales rotas y ninguna
#      página html en docs/ que no esté en el origen.
set -eu

RAIZ=$(cd "$(dirname "$0")/.." && pwd)
ORIGEN="$RAIZ/entregables/curso_copilot_agentes_html5"
ZIP="$RAIZ/entregables/curso_copilot_agentes_html5.zip"
DESTINO="$RAIZ/docs"
REPO="hamletlg/curso_copilot_agentes_html5"
TOKEN_FILE="$RAIZ/entregables/subir_github/url_y_token.txt"
URL="https://hamletlg.github.io/$REPO/"

VERIFICAR=0
PUSH=0
FORZAR=0
for arg in "$@"; do
    case "$arg" in
        --verificar) VERIFICAR=1 ;;
        --push)      PUSH=1 ;;
        --forzar)    FORZAR=1 ;;
        *) echo "Opción no reconocida: $arg" >&2; exit 2 ;;
    esac
done

md5_de() { md5sum "$1" 2>/dev/null | cut -d' ' -f1; }
paginas_de() { find "$1/html" -maxdepth 1 -name '*.html' -printf '%f\n' 2>/dev/null | sort; }

# ---------------------------------------------------------------- guardas
if [ ! -f "$ORIGEN/index.html" ]; then
    echo "Falta $ORIGEN/index.html." >&2
    echo "Ejecuta antes: python3 herramientas/generar_curso_elpx.py && sh herramientas/exportar.sh" >&2
    exit 1
fi

# G2 — ¿lleva los ajustes del curso?
if ! grep -q "ajustes del curso (inicio)" "$ORIGEN/index.html"; then
    if [ "$FORZAR" = 0 ]; then
        echo "ABORTADO: $ORIGEN no lleva los ajustes del curso (menú con memoria, test como" >&2
        echo "evaluación, veredicto del 70 %). Aplícalos con:" >&2
        echo "    python3 herramientas/ajustes_curso.py $ORIGEN" >&2
        echo "(o repite el flujo completo: generar_curso_elpx.py && exportar.sh, que ya los aplica)" >&2
        exit 1
    fi
    echo "AVISO: se publica SIN los ajustes del curso (--forzar)"
fi

# G3 — ¿coincide el paquete descomprimido con el .zip entregable?
if [ -f "$ZIP" ] && [ "$FORZAR" = 0 ]; then
    M_ORIGEN=$(md5_de "$ORIGEN/index.html")
    M_ZIP=$(unzip -p "$ZIP" index.html | md5sum | cut -d' ' -f1)
    if [ "$M_ORIGEN" != "$M_ZIP" ]; then
        echo "ABORTADO: el paquete descomprimido y el .zip entregable no coinciden." >&2
        echo "  $ORIGEN/index.html              -> $M_ORIGEN" >&2
        echo "  curso_copilot_agentes_html5.zip -> $M_ZIP" >&2
        echo "Reconstruye el paquete desde el zip:" >&2
        echo "    rm -rf $ORIGEN && mkdir -p $ORIGEN && (cd $ORIGEN && unzip -q $ZIP)" >&2
        exit 1
    fi
fi

TMP_O=$(mktemp); TMP_D=$(mktemp)
trap 'rm -f "$TMP_O" "$TMP_D"' EXIT INT TERM
paginas_de "$ORIGEN" > "$TMP_O"

echo "origen : $ORIGEN"
echo "         $(find "$ORIGEN" -type f | wc -l | tr -d ' ') ficheros, $(du -sh "$ORIGEN" | cut -f1), $(wc -l < "$TMP_O" | tr -d ' ') páginas + portada"
echo "         index.html md5 $(md5_de "$ORIGEN/index.html") | content.xml $(stat -c%s "$ORIGEN/content.xml" 2>/dev/null || echo '?') bytes"

if [ "$VERIFICAR" = 1 ]; then
    echo "== comprobación (sin escribir nada) =="
    if [ -f "$DESTINO/index.html" ]; then
        echo "destino: $DESTINO ($(find "$DESTINO" -type f | wc -l | tr -d ' ') ficheros, md5 $(md5_de "$DESTINO/index.html"))"
        if [ "$(md5_de "$ORIGEN/index.html")" = "$(md5_de "$DESTINO/index.html")" ]; then
            echo "ESTADO : docs/ YA es la versión final"
        else
            echo "ESTADO : docs/ está DESACTUALIZADO (hay que publicar)"
        fi
    else
        echo "destino: $DESTINO (no existe)"
    fi
    exit 0
fi

# ---------------------------------------------------------------- copia
echo "== publicando en docs/ =="
if [ -d "$DESTINO" ]; then
    mkdir -p "$RAIZ/entregables/historial"
    cp -a "$DESTINO" "$RAIZ/entregables/historial/docs_$(date +%Y%m%d%H%M%S)"
    echo "   copia de seguridad de docs/ anterior en entregables/historial/"
fi
rm -rf "$DESTINO"
mkdir -p "$DESTINO"
cp -a "$ORIGEN/." "$DESTINO/"
touch "$DESTINO/.nojekyll"      # sin esto Jekyll procesa el sitio (aquí no hace falta)

# ---------------------------------------------------------------- verificación
echo "== verificación =="
FALLO=0
M_O=$(md5_de "$ORIGEN/index.html"); M_D=$(md5_de "$DESTINO/index.html")
if [ "$M_O" = "$M_D" ]; then echo "  ok  index.html de docs/ idéntico al origen ($M_D)"; else echo "  MAL md5 de index.html no coincide"; FALLO=1; fi
if [ -f "$DESTINO/.nojekyll" ]; then echo "  ok  .nojekyll presente"; else echo "  MAL falta .nojekyll"; FALLO=1; fi

paginas_de "$DESTINO" > "$TMP_D"
SOBRAN=$(comm -23 "$TMP_D" "$TMP_O")
if [ -z "$SOBRAN" ]; then
    echo "  ok  sin páginas sobrantes de revisiones anteriores"
else
    echo "  MAL páginas en docs/ que no están en el origen:"
    printf '%s\n' "$SOBRAN" | sed 's/^/      /'
    FALLO=1
fi

if python3 "$RAIZ/herramientas/verificar_enlaces.py" "$DESTINO"; then :; else FALLO=1; fi

if [ "$FALLO" != 0 ]; then
    echo "LA PUBLICACIÓN NO PASA LA VERIFICACIÓN: docs/ queda como está, revisa arriba." >&2
    exit 1
fi
echo "  ok  docs/ listo ($(find "$DESTINO" -type f | wc -l | tr -d ' ') archivos, $(du -sh "$DESTINO" | cut -f1))"

# ---------------------------------------------------------------- git
cd "$RAIZ"
if [ -n "$(git status --porcelain docs)" ]; then
    echo "== git: hay cambios en docs/ ($(git status --porcelain docs | wc -l | tr -d ' ') entradas) =="
else
    echo "== git: docs/ ya coincidía con el repositorio =="
fi

if [ "$PUSH" = 0 ]; then
    echo "    Para publicar:  git add -A && git commit -m 'docs: demo actualizada' && git push"
    echo "    (o repite con --push: commitea, empuja y espera a que Pages reconstruya)"
    echo "    Vista local:    python3 -m http.server -d docs"
    exit 0
fi

echo "== git: commit + push =="
git add -A -- docs
if [ -n "$(git status --porcelain docs)" ]; then
    git commit -q -m "docs: demo sincronizada con el HTML5 final (publicar_docs.sh)"
fi
echo "   commit: $(git log --oneline -1 | cat)"

if [ ! -f "$TOKEN_FILE" ]; then
    echo "AVISO: no hay $TOKEN_FILE; empuja tú con: git push" >&2
    exit 0
fi
TOKEN=$(sed -n 's/.*\(gh[pousr]_[A-Za-z0-9]\{20,\}\).*/\1/p' "$TOKEN_FILE" | head -1)
if [ -z "$TOKEN" ]; then
    echo "AVISO: no encuentro el token en $TOKEN_FILE; empuja tú con: git push" >&2
    exit 0
fi

ASKPASS=$(mktemp /tmp/.askpass.XXXXXX)
printf '#!/bin/sh\ncase "$1" in\n  *[Uu]sername*) echo x-access-token ;;\n  *) echo "%s" ;;\nesac\n' "$TOKEN" > "$ASKPASS"
chmod 700 "$ASKPASS"
trap 'rm -f "$TMP_O" "$TMP_D" "$ASKPASS"' EXIT INT TERM
GIT_ASKPASS="$ASKPASS" GIT_TERMINAL_PROMPT=0 git push origin main 2>&1 | sed "s/$TOKEN/***/g"
echo "   URL: $URL"

echo "== esperando a que GitHub Pages reconstruya =="
i=0
while [ "$i" -lt 24 ]; do
    EST=$(curl -s -H "Authorization: Bearer $TOKEN" -H "Accept: application/vnd.github+json" \
          "https://api.github.com/repos/$REPO/pages" | sed -n 's/.*"status": *"\([a-z]*\)".*/\1/p' | head -1)
    echo "   [$i] status=${EST:-?}"
    [ "$EST" = "built" ] && break
    i=$((i + 1))
    sleep 10
done
curl -s -o /dev/null -w "   raíz publicada: HTTP %{http_code}\n" "$URL"
