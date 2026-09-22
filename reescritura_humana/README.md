# reescritura_humana

Reescribir los textos del guión (`../guión_curso_copilot_exelearning.md`) con un LLM local para que
suenen escritos por una persona y no por una máquina, sin perder el tono profesional del curso, y
añadir **recuadros de ideas clave** en las páginas donde la información lo merece.

**El guión original se toca solo al final y con copia de seguridad.** Todo el trabajo previo ocurre
en esta carpeta. Plan de la tarea: `PLAN.md`. Selección de los recuadros: `recuadros/seleccion.md`.

## Tubería completa

```
guión (markdown)
   │  extraer_textos.py            → originales/nodo_NN_*.md            (25 páginas, campo «Contenido en pantalla»)
   │  reescribir.py                → salida/<modelo>/nodo_NN_*.md       (texto humanizado, LLM local)
   │  volcar_guion.py --textos     → guión actualizado                  (con comprobación de estructura por nodo)
   │
   │  mapa_bloques.py / mapa_anclajes.py   → qué anclajes tiene cada página (para elegir dónde va el recuadro)
   │  escribir_recuadros.py        → recuadros/salida/nodo_NN.md        (el recuadro, escrito por el mismo LLM)
   │                                  recuadros/salida/nodo_NN.campo.txt (la fila lista para el guión)
   │  volcar_guion.py --recuadros  → guión actualizado                  (fila «Recuadro de ideas clave»)
   │
   │  herramientas/generar_curso_elpx.py  → content.xml + .elpx mínimo   (monta el recuadro en su sitio)
   │  herramientas/exportar.sh            → .elpx + SCORM 1.2 + HTML5
   └  verificar_recuadros.py       → comprueba el estilo EN el producto exportado
```

## Ficheros

| Fichero | Qué hace |
|---|---|
| `PLAN.md` | El plan de la tarea, con las fases y sus criterios de verificación |
| `extraer_textos.py` | Saca el campo «Contenido en pantalla» de los 25 nodos a `originales/` |
| `prompts/reescritura.md` | Instrucciones de estilo de la reescritura (marcador `{TEXTO}`) |
| `reescribir.py` | Llama al `llama-server` de :8080 y guarda en `salida/<sufijo>/` |
| `comparar.py` | Muestra comparativa original / versiones + detector de marcas de escritura de IA |
| `mapa_bloques.py` · `mapa_anclajes.py` | Mapa de encabezados y etiquetas de cada página |
| `prompts/recuadro.md` | Instrucciones del recuadro de ideas clave (marcador `{PAGINA}`) |
| `escribir_recuadros.py` | Pide el recuadro al modelo y lo deja listo como fila del guión |
| `volcar_guion.py` | Vuelca textos y recuadros al guión (con copia de seguridad y red de seguridad) |
| `contraste.py` | Contraste WCAG 2.1 de los colores del recuadro |
| `verificar_recuadros.py` | Comprueba el recuadro y su CSS en la vista previa, el SCORM y el HTML5 |
| `muestra_nodo_17_riesgos.md` | La muestra: nodo 17 en original, Gemma 4B y Gemma 12B |
| `informe_reescritura.md` | Las 25 páginas, una a una: marcas de IA antes y después, longitudes y tiempos |
| `reescribir_quiz.py` · `quiz/` | Reescritura de las 20 preguntas del cuestionario (se comprueba que sigue siendo parseable) |
| `estructurar_ejercicios.py` · `ejercicios/` | Convierte los 4 ejercicios en la fila «Actividades interactivas» del guion |
| `PROPUESTA_formato_intermedio.md` (en la raíz del proyecto) | La decisión de fondo: pasar de guion markdown a un IR en JSON (revisión VIII) |

## Uso

```bash
cd /mnt/DATA/trabajo_hermes/articulate_hermes/reescritura_humana

python3 extraer_textos.py                                              # 25 nodos -> originales/
python3 reescribir.py --todos --modelo gemma4-12b --sufijo gemma4-12b  # las 25 páginas (~45 min)
python3 volcar_guion.py --textos --simular                             # ver qué se volcaría
python3 volcar_guion.py --textos                                       # volcar de verdad

python3 mapa_anclajes.py salida/gemma4-12b                             # anclajes del texto final
python3 escribir_recuadros.py recuadros/seleccion.json                 # los 8 recuadros
python3 volcar_guion.py --recuadros                                    # al guión

python3 contraste.py
python3 verificar_recuadros.py
```

## Servidor

El modelo lo sirve el conmutador del usuario, no este proyecto:

```bash
cd /mnt/datos/PROGRAMACION/PYTHON/LLAMACPP_MODEL_SWITCH
python3 llama_server_switch.py switch gemma4-12b   # puerto 8080
python3 llama_server_switch.py status
python3 llama_server_switch.py stop
```

Los parámetros de generación son los del `command_*.txt` del modelo (temperatura, top-k,
`--reasoning on`). Los scripts de aquí no los pisan: solo mandan `max_tokens` y el campo `model`.

## La red de seguridad del volcado (importante)

El generador del curso corta el texto de cada página por **literales**: `c.index("Un recorrido
práctico")`, `c.index("> **Nota:**")`, `c.index("**1. Recibir la orden**")`, `partes_acordeon()`
buscando `**Sección N:` y `parse_quiz()` buscando `**Pregunta N:**` + `[CORRECTA]`. Si la
reescritura se come una de esas marcas, el montaje falla o monta otra cosa.

Por eso `volcar_guion.py` no sustituye ningún nodo sin comprobar antes que conserva todas las
marcas que tenía: el nodo que no pasa **se queda como estaba** y sale en `volcado_informe.md`.
Es lo que pasó con el nodo 1 (portada): el modelo cambió el título del curso y se comió un literal.

## Rendimiento medido (RTX 4060 8 GB)

| Modelo | Arranque | Velocidad | Una página | Las 25 |
|---|---|---|---|---|
| `gemma4-e4b-mtp` (4B) | 15,1 s | 67 tok/s | ~34 s | ~5 min |
| `gemma4-12b` | 16,0 s | 21 tok/s | ~2 min | ~45 min |

## Resultado (22-sep-2026)

- **Textos:** 25/25 reescritos con `gemma4-12b` (54,6 min, 20,6 tok/s, 0 errores); marcas de IA del
  detector 52 → 21, y las 21 restantes son marcado estructural o falsos positivos (ver
  `informe_reescritura.md`).
- **Recuadros:** 8 (5, 10, 14, 17, 18, 19, 21 y 22), con `verificar_recuadros.py` en verde.
- **Dos cosas que solo se vieron al verificar:** el ancla del nodo 19 aparecía dos veces en la página
  (ancla nueva: «Regla práctica: si tienes dudas») y **las respuestas modelo de los ejercicios no
  llegaban al curso** —el exportador solo copia `ideviceId` al `data-idevice-json-data`, así que
  `textFeedbackTextarea` se perdía—; ahora la retroalimentación viaja en el `htmlView` del iDevice.
  Detalle en `PLAN.md`.

## Verificación

```bash
ruff check .
python3 -c "import ast,sys;[ast.parse(open(f).read()) for f in sys.argv[1:]]" *.py
python3 /tmp/hermes-verify-recuadro/probar_recuadro.py   # el montaje del recuadro, con casos límite
```
