Herramientas del proyecto (revisión VI, 13-sep-2026)

AVISO: ninguna de estas herramientas es contenido del curso.

=== PRODUCCIÓN Y VERIFICACIÓN DEL CURSO ===

generar_curso_elpx.py   GENERADOR. Lee el guion y recursos/imagenes/ y produce:
                          - entregables/content.xml (validado contra el DTD y el XSD oficiales)
                          - entregables/_trabajo/curso_copilot_agentes_minimo.elpx (paquete mínimo,
                            INTERMEDIO: el .elpx entregable lo genera el CLI, ver exportar.sh)
                          - entregables/_trabajo/estilos_propios.html (el CSS del proyecto, que el
                            post-proceso inyecta donde el exportador no lo ponga)
                        Decisiones de la revisión IV: 16 páginas (sin EJERCICIOS), UN iDevice Texto
                        por página, bloques sin titular, menú «N. Título», tema Nova y sin el ancla
                        colgante a Latidos.gif en la plantilla del cuestionario.
                        Revisión V: la ancla del Nodo 4 pasa a «**Tabla de entornos:**» y en
                        markdown_a_html los separadores «---» solo se sustituyen cuando van sueltos
                        (antes troceaban las filas de separación de las tablas: fila fantasma de
                        guiones).
                        Revisión VI: el curso pasa a 25 páginas (sin exclusiones) y el despacho de
                        iDevices es POR CLAVE —el título del nodo en el guion (C_*), no su número—,
                        así que añadir o reordenar páginas no exige tocar el montaje: basta editar la
                        lista ORDEN de revision_vi.py. Si una clave no coincide con ninguna conocida,
                        avisa en vez de montar la página en silencio.
                        Uso: python3 herramientas/generar_curso_elpx.py [--check]
                        --check añade el informe de fidelidad de textos nodo a nodo y el del quiz.

exportar.sh             Exporta con el CLI de eXeLearning (sin navegador) y publica los entregables:
                        .elpx completo (formato `elpx`: tema, html/ e iDevices ya dentro), SCORM 1.2
                        y HTML5; les pasa el post-proceso (CSS del proyecto + navegación al pie) y
                        reconstruye entregables/html5_preview/ (la vista previa anterior se archiva
                        en entregables/historial/).
                        Uso: sh herramientas/exportar.sh   (antes: generar_curso_elpx.py)

postproceso_export.py   Retoca las páginas HTML de un paquete exportado (`.elpx`, SCORM o HTML5).
                        Hace dos cosas, ambas idempotentes:
                          1) inyecta el CSS del proyecto: el exportador SCORM 1.2 de eXeLearning 4
                             ignora `pp_extraHeadContent` (el export HTML5 y el .elpx sí lo aplican);
                          2) lleva la navegación «Anterior / Siguiente» al pie: mueve el div
                             `.nav-buttons` (que el exportador deja justo tras `</main>`) dentro de
                             `<main>`, para que herede la maquetación del tema; el CSS del proyecto
                             lo saca del `position: fixed` de Nova.
                        Uso: python3 herramientas/postproceso_export.py <zip|elpx> [<más> ...]
                        Lo llama exportar.sh; no hace falta ejecutarlo a mano.

verificar_paquete.py    Verifica sin navegador el .elpx y sus exportaciones (SCORM 1.2 y HTML5):
                        las 25 páginas, bloques (uno por página y sin titular), menú lateral numerado,
                        imágenes referenciadas, acordeones (4) y sus enlaces título->contenido, texto
                        alternativo, crédito, tema Nova, ausencia de Latidos.gif, y el cuestionario
                        (descifra su estado XOR 146 y comprueba las 20 preguntas, la puntuación SCORM
                        y el feedback). Incluye las comprobaciones de TERMINOLOGÍA de la revisión V
                        (sin etiquetas de licencia, precios ni nombres antiguos; entornos «Copilot
                        Web» / «Copilot de Trabajo» presentes; sin filas fantasma de guiones) y el
                        bloque de CUMPLIMIENTO de la revisión VI: el curso y el cuestionario tienen
                        que contener el contenido mínimo del Art. 4 (AI Act, Reglamento (UE)
                        2024/1689, Artículo 4, responsable del despliegue, RGPD, AESIA,
                        sobreexposición, shadow AI…). 80 comprobaciones.
                        Uso: python3 herramientas/verificar_paquete.py

revision_terminologia.py  REVISIÓN V: aplica al guion la terminología acordada (fuera etiquetas de
                        licencia y precios; entornos Copilot Web / Copilot de Trabajo; tres niveles
                        funcionales; corrección conceptual chatbot vs. agente). Reescribe los campos
                        «Contenido en pantalla» de los nodos 2, 3, 4, 5, 6, 16 y 17 y hace
                        sustituciones puntuales en el resto. Idempotente y con comprobación previa:
                        si un patrón no aparece las veces esperadas, aborta sin escribir. Antes de
                        nada guarda copia en legado_articulate/backups_guion/.
                        Uso: python3 herramientas/revision_terminologia.py   (ya aplicado)

revision_terminologia_maestro.py  Lo mismo sobre contenido_curso_copilot_agentes.md (el documento
                        maestro). Edita por número de línea comprobando el contenido esperado y
                        regenera la PÁGINA 4 (entornos en vez de niveles de facturación).
                        Uso: python3 herramientas/revision_terminologia_maestro.py  (ya aplicado)

revision_vi.py          REVISIÓN VI (remediación de cumplimiento del Art. 4). Reconstruye el §4 del
                        guion con el orden final de 25 nodos (7 páginas nuevas + la de ejercicios de
                        vuelta), renumera, remapea las referencias «Nodo N» de los nodos conservados y
                        reescribe el sitemap (§2), la ficha (§1), la tabla de iDevices (§5), el
                        cronograma (§7), el checklist (§8), el inventario de recursos (§9) y las
                        decisiones (§10). Regenera además el maestro con el mismo texto (en prosa) y
                        deja los 4 ejercicios de reserva en un anexo. Corrige de paso las
                        inconsistencias C1-C5 (precio en la FAQ, ejercicio con ChatGPT/Gemini,
                        metadatos de 28 páginas, glosario sin ordenar y título del nodo 4).
                        Comprueba antes de escribir y guarda copia en legado_articulate/backups_guion/.
                        Uso: python3 herramientas/revision_vi.py [--dry-run]   (ya aplicado)

revision_vi_nodos_nuevos.md  FUENTE del contenido de la revisión VI: los bloques «### NODO» que se
                        insertan o sustituyen (fundamentos de IA, inventario, sobreexposición,
                        política y protocolo, AI Act, Artículo 4, datos personales y derechos,
                        ejercicios, cuestionario de 20 preguntas y cierre). Es el único sitio donde se
                        redacta el contenido nuevo: el script lo reparte entre guion y maestro.

pruebas_interaccion.py  Prueba REAL en navegador (Chrome headless por CDP): que cada página tenga UN
                        bloque y ningún titular «Texto», la navegación «Anterior/Siguiente» al pie
                        (posición, alineación con el texto, visible al final), la portada (modo
                        overlay en columna ancha y apilado en estrecha, sombra y texto alternativo),
                        el acordeón (desplegar y plegar) y el cuestionario (iniciar, leer la pregunta,
                        responder y comprobar el feedback y el marcador). Necesita el HTML5
                        descomprimido en entregables/html5_preview/; no hace falta servidor: usa file://.
                        Uso: python3 herramientas/pruebas_interaccion.py

capturar_pantallas.py   Capturas de página completa del HTML5 exportado (portada, fundamentos, uso
                        responsable, ejercicios y evaluación, más una en móvil) para el README y el
                        historial: entregables/capturas/rev6/. Despliega el primer acordeón en las
                        páginas que lo tienen, para que se vea la interacción.
                        Uso: python3 herramientas/capturar_pantallas.py

extraer_componentes_elpx.py  Extrae componentes de un content.xml real (fixture oficial) y muestra su
                        estructura; descifra los iDevices de juego (XOR 146 + percent-encoding).
                        Uso: python3 herramientas/extraer_componentes_elpx.py <content.xml> [tipos]

plantillas/             plantillas/quiz_quick-questions.json — esqueleto real del iDevice
                        quick-questions (htmlView, textTextarea y las 52 cadenas de interfaz),
                        extraído de test/fixtures/todos-los-idevices_dos_informes.elpx del repo
                        oficial. Lo usa el generador para no inventar el estado del quiz.

=== MANTENIMIENTO DEL GUION (revisión III y anteriores) ===

check_guion.py       -> verifica la consistencia del guion (nodos, filas de recursos, alt texts,
                        recursos citados) y comprueba los patrones de descarga de StockSnap.
informe_final.py     -> imprime el mapa nodo -> recurso del guion.
verificar_guion.py   -> verifica el guion tras la revision III: titulos de los 17 nodos, secciones,
                        referencias cruzadas dentro de rango, sitemap vs titulos, iDevices por nodo.
tail_check.py        -> comprueba la cola del nodo de ejercicios (8 ejercicios) y la seccion 9.
gen_creditos.py      -> REGENERA recursos/imagenes/CREDITOS.md midiendo los archivos en disco.
vis_desc.py          -> describe una imagen con el modelo de vision local (llama.cpp :8081).
ver_paginas.py       -> muestra los nombres de página y títulos H1 que produce el generador.
aplicar_decisiones.py -> script que aplico las decisiones P1-P9 al guion el 12-sep-2026 (revision III).
                        Idempotente; los backups los escribe en legado_articulate/backups_guion/.

Los backups del guion son guión_curso_copilot_exelearning.md.bak.<AAAAMMDD_HHMMSS> y desde el
12-sep-2026 se guardan en legado_articulate/backups_guion/ (fuera de la raíz, para no hacer ruido).
