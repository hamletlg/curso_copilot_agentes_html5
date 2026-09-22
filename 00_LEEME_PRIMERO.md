# 00 — LEE ESTO PRIMERO

**Proyecto:** curso e-learning «Agentes de IA y Microsoft Copilot para tu día a día»
**Herramienta:** eXeLearning (local) → export **SCORM 1.2 + HTML5** (tema **Nova**)
**Estado:** **revisión VII (22-sep-2026)**: sobre la base de la revisión VI (25 páginas y 3,5 horas,
remediación del Artículo 4 y expediente de `cumplimiento/`), esta revisión **reescribe los textos de
las 25 páginas** con un LLM local (Gemma 4 12B) para que suenen a persona y no a máquina, sin perder
el registro profesional; añade un **recuadro de ideas clave** a mitad de página en 8 páginas (5, 10,
14, 17, 18, 19, 21 y 22); y **monta la página de ejercicios con iDevices interactivos** (2 test de
práctica que corrigen y explican sin puntuar + 2 respuestas abiertas con el botón de
retroalimentación). Se mantienen los ajustes de las revisiones IV, V y VI (un bloque por página, tema
**Nova**, terminología sin etiquetas de licencia ni precios). Todo se aplica por código (guion y
maestro → `content.xml` → CLI de eXeLearning) y se verifica sin navegador (87 comprobaciones) y en
Chrome real.
**Objetivo del proyecto:** montar el curso y exportarlo → **conseguido**; queda la revisión del autor.

Este documento existe para que quien retome el trabajo (persona o agente) no tenga que leer
todos los ficheros de la carpeta. Con estos **cinco** y este resumen, es suficiente.

---

## 1. QUÉ LEER, EN ESTE ORDEN

| Orden | Fichero | Para qué |
|-------|---------|----------|
| 1 | **Este documento** (`00_LEEME_PRIMERO.md`) | Estado, mapa de la carpeta, entorno y reglas |
| 2 | `guión_curso_copilot_exelearning.md` | **Documento de trabajo**: 25 nodos con texto literal, iDevice, recurso gráfico y texto alternativo; cuestionario de 20 preguntas; 4 ejercicios montados (y 4 de reserva en el maestro). Al final: §5 iDevices, §6 tema y accesibilidad, §7 cronograma, §8 checklist, §9 recursos, §10 decisiones |
| 3 | `idevices_equivalencias_exelearning4.md` | **Traducción de los iDevices del guion al catálogo real** (eXeLearning 4): tabla de equivalencias, el «acordeón» resuelto con el efecto nativo `exeeffects` (con la trampa de los identificadores) y la configuración verificada del cuestionario |
| 4 | `evaluacion_generar_paquete_vs_cdp.md` | **Cómo se montó y con qué evidencia**: pipeline `.elpx` → SCORM 1.2 con el CLI del contenedor, ejecución paso a paso, los 2 fallos encontrados y corregidos, y los pendientes |
| 5 | `contenido_curso_copilot_agentes.md` | **Fuente de verdad del contenido** (25 páginas del maestro). Desde la revisión VI su texto es el mismo que el del guion: se redacta una vez y `revision_vi.py` lo pasa a prosa |
| — | `entregables/` | **El resultado**: `.elpx`, SCORM 1.2, HTML5, `content.xml` y la vista previa |
| — | `recursos/imagenes/CREDITOS.md` | Licencias, atribución y sha256 de las 11 imágenes (10 en el paquete) |
| — | `pendientes_montaje_exelearning.md` | Historial de decisiones (P1-P9, revisiones IV, V y VI) y lo que queda |
| — | `cumplimiento/00_LEEME.md` | **Expediente de cumplimiento**: matriz de trazabilidad (Anexo I), memoria de justificación, política de uso de IA, acta y certificado, y temario |

### Qué NO hay que leer (y por qué)

- **`legado_articulate/`** — material del curso **anterior** («Agentes de IA Generativa», hecho en Articulate Rise/Storyline) y documentos intermedios descartados. Su contenido y su cuestionario son **distintos**: si se confunden, se monta el curso equivocado. Tiene su propio `README.md`. Lo único reutilizable ahí dentro es `pautas_diseno/PAUTAS_DE_DISEÑO.md` (paleta de color con contrastes WCAG).
- **`herramientas/`** — scripts de producción y mantenimiento (generador, verificadores), no documentación de contenido. Están descritos en `herramientas/README.txt`.
- Los `*.bak.<fecha>` del guion, el catálogo de portadas descartadas y la auditoría de capturas se movieron el 12-sep-2026 a `legado_articulate/` (`backups_guion/` y `descartes_proyecto/`).

---

## 2. ESTADO EN UNA LÍNEA

**Hecho:** **25 páginas** (22 de contenido + ejercicios + cuestionario + cierre), **29 componentes**
(**26 iDevices Texto** + **3 Cuestionario**: la evaluación final y los 2 test de práctica de la página
de ejercicios) repartidos en 29 bloques, 10 imágenes, 4 acordeones nativos, **8 recuadros de ideas
clave**, cuestionario de **20 preguntas** (14 correctas, 70 %) con 1 punto por pregunta y feedback por
pregunta, tema **Nova** y el CSS propio del proyecto. `content.xml` validado contra el DTD y el XSD
oficiales, y exportado a **`.elpx`**, **SCORM 1.2** y **HTML5** con el CLI de eXeLearning, sin tocar la
interfaz. Verificado sin navegador (**87 comprobaciones**, incluidas las de terminología, las de
cumplimiento del Art. 4, los recuadros, las respuestas abiertas y la coherencia de la portada) y en Chrome real: portada con
overlay, diagramas, acordeón (despliega y pliega), tablas, navegación al pie, cuestionario (20
preguntas, aciertos registrados), el recuadro con su estilo aplicado y la respuesta modelo que se
despliega al pulsar el botón. Capturas en `entregables/capturas/rev7/`.

**Pendiente (nada bloquea el material):**

| # | Qué | Quién |
|---|-----|-------|
| A1 | **Titular del curso** (`pp_author` va vacío a propósito) y licencia del repositorio | Autor |
| A2 | Ruta del menú del *Planner Agent* en el tenant real (Nodos 10-12) | Autor |
| B1 | Nota de corte **70** en el LMS: el paquete informa la nota (0-100), pero el umbral lo aplica el LMS (`cmi.student_data.mastery_score`; por defecto, la política SCORM 1.2 usa 50) | Autor / TI |
| B2 | Probar el SCORM en un visor real (Moodle, SCORM Cloud) y ver `lesson_status` | Autor / TI |
| C1 | **Completar el expediente realizado** con la memoria, la política y el acta del cliente (plantillas en `cumplimiento/`) | Autor |

*(B3 —tema— y B4 —`CREDITOS.md`— quedaron resueltos en la revisión IV; ver §6 de
`pendientes_montaje_exelearning.md`. La revisión VI está documentada en §8 del mismo fichero.)*

---

## 3. MAPA DE LA CARPETA

```
/mnt/DATA/trabajo_hermes/articulate_hermes/
├── 00_LEEME_PRIMERO.md                     <- este documento
├── guión_curso_copilot_exelearning.md      <- documento de PRODUCCIÓN (fuente del montaje)
├── idevices_equivalencias_exelearning4.md  <- iDevices del guion → catálogo real de eXeLearning 4
├── evaluacion_generar_paquete_vs_cdp.md    <- cómo se montó, con evidencia y pendientes
├── contenido_curso_copilot_agentes.md      <- contenido MAESTRO (fuente de verdad)
├── pendientes_montaje_exelearning.md       <- decisiones aplicadas + lo que queda
├── cumplimiento/                           <- EXPEDIENTE de la acción formativa (Art. 4)
│   ├── 00_LEEME.md                            índice del expediente y orden de uso
│   ├── 01_Matriz_Trazabilidad_Art4.md         contenido mínimo (Q&A de la AI Office) -> páginas y preguntas
│   ├── 02_Memoria_Justificacion.md            memoria (plantilla, Anexo I = matriz)
│   ├── 03_Politica_Uso_IA_Microsoft365.md     política interna de uso de IA (plantilla)
│   ├── 04_Acta_Asistentes_y_Certificado.md    acta de participantes y certificado (plantillas)
│   └── 05_Temario_FUNDAE.md                   temario en formato de justificación (3,5 h)
├── entregables/                            <- RESULTADO
│   ├── curso_copilot_agentes.elpx             proyecto COMPLETO (25 páginas, tema Nova, html/ ya
│   │                                          renderizado): abrible en eXeLearning y previsualizable
│   ├── curso_copilot_agentes_scorm12.zip      ENTREGABLE: SCORM 1.2
│   ├── curso_copilot_agentes_html5.zip        export HTML5
│   ├── content.xml (+ content.dtd, ode-content.xsd)  fuente generada y los esquemas
│   ├── html5_preview/                         HTML5 descomprimido para inspeccionar
│   ├── historial/                             revisiones anteriores (preview rev. III y el .elpx
│   │                                          revisión III guardado desde la app; los borradores
│   │                                          intermedios de la rev. IV en _borradores_rev4/). Nada se borra
│   └── _trabajo/                              intermedios: .elpx mínimo y estilos_propios.html
├── recursos/
│   └── imagenes/    portada_curso_copilot.jpg + 5 iconos (PNG/SVG) + 2 diagramas (PNG/SVG) + CREDITOS.md
├── herramientas/
│   ├── generar_curso_elpx.py      GENERADOR: guion -> content.xml -> .elpx (valida DTD/XSD)
│   ├── verificar_paquete.py       verifica .elpx + SCORM + HTML5 sin navegador (87 comprobaciones,
│   │                              incluidas las de terminología: sin etiquetas de licencia)
│   ├── pruebas_interaccion.py     prueba real de acordeón y cuestionario en Chrome headless (CDP)
│   ├── extraer_componentes_elpx.py  extrae/descifra componentes reales de un content.xml
│   ├── plantillas/                plantilla del cuestionario extraída del fixture oficial
│   └── (mantenimiento: revision_terminologia.py y revision_terminologia_maestro.py —revisión V,
│       de terminología, sobre el guion y el maestro—, verificar_guion.py, informe_final.py,
│       check_guion.py, gen_creditos.py, vis_desc.py, aplicar_decisiones.py, tail_check.py,
│       ver_paginas.py) + README.txt
└── legado_articulate/   NO USAR para montar: curso anterior y documentos descartados, más
                         backups_guion/ (copias .bak del guion) y descartes_proyecto/
                         (portadas descartadas y auditoría de capturas) (+ su README)
```

---

## 4. ENTORNO LOCAL (ya levantado)

| Qué | Detalle |
|-----|---------|
| eXeLearning | Contenedor podman `exelearning`, imagen local `localhost/exelearning:local` (**v4**) |
| URL | http://127.0.0.1:8090 |
| Usuario | administrador local `admin@local`; la contraseña está en `/mnt/DATA/INSTALADORES/exelearning-podman/state/exelearning.env` (`ADMIN_PASSWORD`) |
| Datos | base SQLite y ficheros en `/mnt/DATA/INSTALADORES/exelearning-podman/data` y `.../files` |
| Chrome para CDP | `google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/remote-profile` (ya escuchando en 127.0.0.1:9222) |

Comandos del contenedor (script del instalador):

```
cd /mnt/DATA/INSTALADORES/exelearning-podman
./exelearning-podman.sh status     # estado, puerto, URL y healthcheck
./exelearning-podman.sh up         # arrancar (construye solo si hace falta)
./exelearning-podman.sh logs       # últimas líneas de log (FOLLOW=1 para seguirlo)
./exelearning-podman.sh stop
```

Exportación sin navegador (lo que hace `herramientas/exportar.sh`):

```
podman cp entregables/_trabajo/curso_copilot_agentes_minimo.elpx exelearning:/tmp/curso_entrada.elpx
for f in elpx scorm12 html5; do
  podman exec exelearning sh -c "cd /app && bun dist/cli.js elp:export /tmp/curso_entrada.elpx /tmp/curso_out_$f $f"
  podman cp exelearning:/tmp/curso_out_$f.* entregables/     # .elpx | .zip | .zip
done
```

---

## 5. CÓMO REGENERAR EL CURSO

```
python3 herramientas/revision_vi.py                # 0) solo si hay que reaplicar la revisión VI (guion y maestro)
python3 herramientas/revision_vii.py               # 0b) solo si hay que reaplicar la revisión VII (maestro)
python3 herramientas/generar_curso_elpx.py        # 1) guion -> content.xml (+ .elpx mínimo; valida DTD/XSD)
python3 herramientas/generar_curso_elpx.py --check  #    opcional: informe de fidelidad de textos y del quiz
sh herramientas/exportar.sh                       # 2) -> .elpx completo + SCORM 1.2 + HTML5 + vista previa
python3 herramientas/verificar_paquete.py         # 3) comprueba los tres entregables sin navegador
python3 herramientas/pruebas_interaccion.py       # 4) acordeón y cuestionario reales en Chrome (CDP)
python3 herramientas/capturar_pantallas.py        # 5) capturas de página completa -> entregables/capturas/rev6/
```

`exportar.sh` lanza los tres exports con el CLI del contenedor y pasa `postproceso_export.py` sobre
los tres (`.elpx`, SCORM y HTML5), que inyecta el CSS del proyecto donde hace falta (el exportador
SCORM 1.2 ignora `pp_extraHeadContent`) y lleva la navegación «Anterior / Siguiente» al pie de las
páginas. Después reconstruye `entregables/html5_preview/` (la vista previa anterior se archiva en
`historial/`, no se borra).

---

## 6. REGLAS DEL MONTAJE (siguen vigentes si se retoca algo)

1. **El guion manda.** No inventar texto: si falta contenido, está en `contenido_curso_copilot_agentes.md`.
   La página de **EJERCICIOS** ya se monta (revisión VII): su introducción como texto y sus 4
   actividades con iDevices nativos, tal como las trae su fila «Actividades interactivas».
2. **Un iDevice Texto por página** (desde la revisión VII, con dos excepciones). Los fragmentos del
   guion de cada nodo se concatenan en un único iDevice Texto, en un bloque sin titular; el
   cuestionario es aparte. Excepciones de la página de EJERCICIOS: lleva 5 bloques (introducción,
   2 test de práctica y 2 respuestas abiertas) y sus respuestas abiertas usan el botón de
   retroalimentación del iDevice Texto. Ojo: esa retroalimentación tiene que viajar **en el
   `htmlView`**, no solo en las propiedades del iDevice — el exportador solo copia `ideviceId` al
   `data-idevice-json-data`, así que dejarla en `textFeedbackTextarea` la hace desaparecer del curso
   (pasó, y lo caza la comprobación de fidelidad). El recuento de iDevices del guion y su traducción
   al catálogo real están en `idevices_equivalencias_exelearning4.md`.
3. **Recursos:** cada nodo usa exactamente el archivo de su fila «Recurso gráfico» y su texto
   alternativo, como imagen PNG.
4. **Tema:** **Nova** (`userPreferences/theme`). El CSS propio del proyecto viaja en
   `pp_extraHeadContent` (ver §6, regla 9).
5. **Cuestionario:** 1 punto por pregunta, feedback por pregunta, orden fijo y las **20 preguntas**
   visibles (`percentajeQuestions = 100`, que NO es la nota de corte: la corte se pone en el LMS a 70).
6. **Crédito obligatorio en la última página («RESUMEN Y GLOSARIO»):** «Imagen de portada: Jakub
   Zerdzicki / Pexels».
7. **Sin JavaScript propio**: las interacciones son las nativas de eXeLearning (efecto `exeeffects`).
8. **No tocar `legado_articulate/`** ni reabrir decisiones cerradas (`pendientes_montaje_exelearning.md`).
9. **Bloques sin titular.** Los bloques van con `blockName` vacío (nada de «Texto»): el export los
   marca `article.box.no-header`. Como el tema Nova reserva 60 px de cabecera y deja suelto el botón
   de plegado, el CSS propio del proyecto los anula.
10. **Nada se borra.** Al regenerar, la vista previa anterior se archiva en `entregables/historial/`.
11. **Navegación al pie.** Los botones «Anterior / Siguiente» van al final de cada página, alineados
    con la columna de texto (el post-proceso mete `div.nav-buttons` dentro de `<main>` y el CSS del
    proyecto lo saca del `position: fixed` de Nova). En el export SCORM 1.2 no existen: ahí navega el
    índice del LMS.
12. **Portada con overlay.** El título, el subtítulo y «Duración · Nivel» van sobre la foto, con
    degradado oscuro + sombra (la imagen es clara por zonas: la sombra sola no basta). Es responsive
    por contenedor (`@container`): si la columna baja de 520 px, el texto pasa debajo de la imagen en
    color oscuro. La introducción queda siempre debajo. Nada de esto necesita JS.
13. **Terminología (revisión V).** El texto didáctico **no lleva etiquetas de licencia ni de
    facturación** («con licencia», «gratis», «de pago», precios): lo que se explica es **dónde opera**
    Copilot —**Copilot Web** (o «Modo Web») y **Copilot de Trabajo** (Microsoft 365 Copilot)— y **qué
    puede hacer**, en tres niveles: **Copilot Asistente** (o chatbot estándar), **agentes
    especializados** (o declarativos) y **agentes avanzados** (o de Copilot Studio). Los cambios se
    aplican al guion y al maestro con `herramientas/revision_terminologia*.py`; el verificador
    (`verificar_paquete.py`) tiene comprobaciones específicas para que no vuelvan a colarse.
14. **Revisión VI: el curso cumple el mínimo del Art. 4.** 25 páginas y 3,5 h: el contenido se
    redacta **una sola vez** en `herramientas/revision_vi_nodos_nuevos.md` y `herramientas/revision_vi.py`
    reconstruye con él el guion y el maestro (mismo texto, uno en formato guion y otro en prosa). El
    despacho de iDevices del generador es **por clave (título del nodo)**, no por número: para añadir o
    mover páginas no hay que tocar la lógica de montaje, solo la lista `ORDEN` del script.
15. **Revisión VII: texto reescrito, recuadros y actividades interactivas.** Los 25 textos se
    reescriben con un LLM local (`reescritura_humana/`) y al guion le crecen dos cosas: la fila
    **«Recuadro de ideas clave»** (bloque de refuerzo a mitad de página, con anclaje por texto: el
    ancla tiene que ser **única** en la página montada y el generador falla en voz alta si no lo es)
    y la fila **«Actividades interactivas»** del nodo 23. Todo el trabajo y sus verificadores viven en
    `reescritura_humana/`; el guion guarda copia de seguridad previa en
    `legado_articulate/backups_guion/`.
16. **El expediente de cumplimiento va aparte.** Lo que hace que el curso sea evidencia de una acción
    formativa (memoria, matriz de trazabilidad, política, acta y temario) vive en `cumplimiento/`; el
    curso no incluye esos documentos, los explica y los aprovecha (página 19 y página 21).
