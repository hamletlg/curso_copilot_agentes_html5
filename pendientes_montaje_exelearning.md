# DECISIONES Y PENDIENTES DEL PROYECTO

**Curso:** Agentes de IA y Microsoft Copilot para tu día a día (eXeLearning → SCORM / HTML)
**Estado:** **revisión VI del montaje, 13-sep-2026** — decisiones P1-P9 aplicadas, los ajustes sobre el entregable (§6), la revisión de terminología (§7) y la **remediación de cumplimiento del Art. 4** (§8: 25 páginas, 3,5 h, cuestionario de 20 preguntas). Quedan 2 cosas que solo puede hacer el autor (§3).
**Documentación vigente:** `00_LEEME_PRIMERO.md` (guía maestra) · `guión_curso_copilot_exelearning.md` (producción) · `contenido_curso_copilot_agentes.md` (maestro) · `recursos/imagenes/CREDITOS.md` (licencias).

---

## 1. DECISIONES DEL AUTOR — APLICADAS (P1-P9)

| # | Decisión | Opción aplicada | Qué se hizo exactamente |
|---|----------|-----------------|-------------------------|
| **P1** | Estructura del árbol | **Nodos planos, sin módulos padre** | El guion §2 mantiene los 17 nodos planos (con la etiqueta decorativa «MÓDULO x»). `plan_diseño_exelearning_copilot.md` queda descartado y archivado en `legado_articulate/`. |
| **P2** | Nodo «Índice + objetivos» | **Sí, añadido** | **Nodo 2 nuevo** («Índice y objetivos»), redactado desde la PÁGINA 2 y el bloque OBJETIVOS DOCENTES del maestro. iDevices: Texto (formato amplio) + Lista numerada. |
| **P3** | Ejercicios: 4 u 8 | **8** | **Nodo 15** pasa de 4 a 8 ejercicios, en el orden del maestro: 1 identifica el tipo de IA · 2 componentes · **3 clasifica el tipo de agente (nuevo)** · 4 mejora las instrucciones · 5 ¿qué harías tú? · **6 caso práctico completo (nuevo)** · **7 el ciclo en acción (nuevo)** · **8 análisis de riesgos (nuevo)**. Los ejercicios 1-5 solo se renumeraron. |
| **P4** | Tipos de agente | **Nodo propio** | **Nodo 6 nuevo** («Los tipos de agente de Microsoft»): acordeón de 5 secciones (Researcher, Analyst, Facilitator, Cowork, agentes personalizados), redactado desde la PÁGINA 6 del maestro. Cierra el hueco que el cuestionario evaluaba (preguntas 3 y 4) y que solo aparecía en el glosario. |
| **P5** | Licencia y autoría | **Uso interno + crédito de cortesía** | §1: «Licencia del curso: uso interno (propietaria)». Crédito de la portada en el Nodo 17. **Falta solo el titular** (ver §3). |
| **P6** | Verificación en el tenant real | **La hace el autor** | No aplicable desde aquí (no hay tenant). El guion deja marcado exactamente qué comprobar (ver §3). |
| **P7** | Ruido legado | **Mover a carpeta propia** | 8 documentos y la carpeta `pautas_diseno/` movidos a **`legado_articulate/`**, con un `README.md` que explica qué es cada cosa y advierte de que su cuestionario es distinto. Nada borrado. |
| **P8** | Portada | **Mantener la actual** | Sin cambios: `portada_curso_copilot.jpg`, acreditada en `recursos/imagenes/CREDITOS.md` (Pexels, Jakub Zerdzicki). La segunda opción verificada (Pexels 34170828) queda documentada por si algún día se cambia. |
| **P9** | §7 y §8 | **Mantenerlos como checklist** | Se conservan como cronograma de montaje manual y checklist de verificación, **actualizados a 17 nodos y 8 ejercicios**. |

### Además (renumeración y coherencia)
- Todos los nodos posteriores al 1 se renumeraron (del 2 al 17) y se actualizaron **todas** las referencias cruzadas: sitemap (§2), tabla de iDevices (§5: 17 nodos / 30 iDevices), cronograma (§7), checklist (§8), inventario de recursos (§9: iconos en Nodos 3, 7, 12, 13, 14, 15; diagramas en 5 y 7) y decisiones de diseño (§10, con 3 filas nuevas).
- Verificación automática: 17 nodos, 17 filas «Recurso gráfico», 8 ejercicios, ninguna referencia a nodos fuera del rango 1-17 y sitemap coincidente con los títulos. Script: `herramientas/verificar_guion.py`.
- Copia de seguridad previa a esta revisión: `legado_articulate/backups_guion/guión_curso_copilot_exelearning.md.bak.20260912_210125` (y las dos anteriores del 12-sep, en la misma carpeta).

---

## 2. LO RESUELTO EN LA REVISIÓN II (contexto, no requiere acción)

R1 mapa recurso → nodo en los 17 nodos · R2 los 8 textos alternativos · R3 portada identificada
(Pexels 34088260, Jakub Zerdzicki; correlación 1.0000 con el original) y ficha legal en
`recursos/imagenes/CREDITOS.md` · R4 los 2 diagramas asignados a los Nodos 5 y 7 · R5 los 5 iconos
asignados y verificados con el modelo de visión local (:8081) · R6 «SVG inline» corregido (se
inserta PNG; el SVG es respaldo) · R7 rutas de clic de los Nodos 8-10 contrastadas con la
documentación de Microsoft (corregidos OneNote y Loop) · R8 Cowork definido antes de evaluarse
(ahora en el Nodo 6) · R9 el botón «Comenzar» del Nodo 1 reformulado como la navegación
«Siguiente» · R10 metadatos (idioma es-ES) · R11 trazabilidad: cada sección remite a la fuente
correcta y el material legado está identificado y apartado.

---

## 3. LO ÚNICO QUE QUEDA (no lo puede hacer el agente)

| # | Qué falta | Por qué | Cómo cerrarlo |
|---|-----------|---------|---------------|
| **A1** | **Titular del curso** (persona u organización) para la licencia de uso interno | Es un dato legal/de autoría que no está en ningún documento | Decir el nombre y se escribe en §1 del guion y en el Nodo 17 (créditos). 2 minutos. |
| **A2** | **Comprobación en el tenant de Microsoft 365** | Único dato no verificable por documentación: la ruta del menú del *Planner Agent* y la posición visual exacta de los botones (varían con licencia y canal de actualización) | 10 minutos con la app delante. El guion marca qué mirar en los Nodos 8, 9 y 10 (bloques «¿Dónde está Copilot? (ruta de clic)»). Si algo no cuadra, se corrige el texto del bloque. |

Ninguna de las dos bloquea el montaje: se puede montar el curso entero y aplicar A1/A2 al final.

---

## 4. ESTADO DEL MONTAJE (12-sep-2026): HECHO

**El curso está generado y exportado.** No quedó en un plan: hay paquete y exportaciones verificadas
en `entregables/` (`.elpx`, SCORM 1.2, HTML5, `content.xml`, vista previa). Se montó **sin tocar la
interfaz**, con el generador `herramientas/generar_curso_elpx.py` y el CLI interno de eXeLearning;
el detalle está en `evaluacion_generar_paquete_vs_cdp.md`.

- **Material:** `guión_curso_copilot_exelearning.md` — 17 nodos con texto literal, iDevice asignado, recurso gráfico y texto alternativo por nodo; cuestionario de 10 preguntas (aprobado 7/10); 8 ejercicios con respuestas.
- **Imágenes:** `recursos/imagenes/` — portada (JPG) + 5 iconos (PNG) + 2 diagramas (PNG); licencias en `CREDITOS.md`.
- **Entorno ya levantado:** contenedor `exelearning` (podman) en `http://127.0.0.1:8090` y Chrome con CDP en `127.0.0.1:9222`.
- **Herramientas de apoyo:** `herramientas/` — generador (`generar_curso_elpx.py`), verificador del paquete (`verificar_paquete.py`), prueba de interacción (`pruebas_interaccion.py`) y las de mantenimiento del guion. Descripción completa en `herramientas/README.txt`.
- **No leer para montar:** `legado_articulate/` (curso anterior en Articulate y documentos descartados).

---

## 5. PENDIENTES TRAS EL MONTAJE (12-sep-2026)

Ninguno bloquea el material: el curso está exportado y probado. Son ajustes de cierre.

| # | Pendiente | Detalle | Quién |
|---|-----------|---------|-------|
| A1 | Titular del curso | Falta el nombre para la licencia de uso interno; `pp_author` va vacío a propósito. Al ponerlo: editar `content.xml` o el generador y regenerar | Autor |
| A2 | Ruta del *Planner Agent* | Comprobar en el tenant real el bloque «¿Dónde está Copilot?» de los Nodos 8-10 | Autor |
| B1 | Nota de corte 7/10 | El paquete informa la puntuación correcta (0-100), pero el umbral de aprobado lo pone el LMS (`cmi.student_data.mastery_score`; por defecto la política SCORM 1.2 usa 50). Configurar 70 en el LMS, o abrir el proyecto en la app, poner `masteryScore` y exportar desde ahí | Autor / TI |
| B2 | Probar en un visor SCORM real | Moodle o SCORM Cloud: ver que se registra `cmi.core.score.raw` y el `lesson_status` | Autor / TI |
| B3 | ~~Tema y paleta~~ | **Resuelto en la revisión IV**: tema **Nova** aplicado y verificado en el `.elpx`, el SCORM 1.2 y el HTML5 | — |
| B4 | ~~`CREDITOS.md` desactualizado~~ | **Resuelto en la revisión IV**: corregidas las dos referencias al «Nodo 15» (ahora «RESUMEN Y GLOSARIO», página 16) | — |

---

## 6. REVISIÓN IV (13-sep-2026): ajustes sobre el curso exportado

El autor revisó el entregable y pidió seis cambios (más uno de navegación al final). Todos aplicados
regenerando el curso con el generador y el CLI (nada a mano en el `.elpx`) y verificados con
`verificar_paquete.py` (todas las comprobaciones en verde) y `pruebas_interaccion.py` (acordeón,
cuestionario y navegación al pie, reales, en Chrome).

| # | Petición | Qué se hizo |
|---|----------|-------------|
| V1 | **Un solo bloque de texto por página** (antes había 2-3 y obligaba a hacer scroll) | El generador acumula los fragmentos de cada nodo y emite **un único iDevice Texto por página**. Se conserva el texto literal del guion. |
| V2 | Quitar la etiqueta **«Texto»** de cada bloque | Los bloques van con `blockName` vacío: el export no dibuja titular ni caja de título (`article.box.no-header`). |
| V3 | Menú lateral: **«N. Título»** en vez de «MÓDULO n — Título» | `pageName` = número de página + título (16 páginas numeradas). Fuera la etiqueta decorativa «MÓDULO x —» y el `odeNavStructureOrder` se renumera. |
| V4 | Aplicar el **tema Nova** | `userPreferences/theme = nova`. Verificado: el `style.css` exportado coincide (sha256) con el `nova` del contenedor. |
| V5 | Faltaba **`Latidos.gif`** | No era un recurso del curso: era un ancla colgante (`.quext-LinkImages`) que la plantilla del cuestionario **heredó del fixture oficial** de eXeLearning; el JS la usaba como imagen de la pregunta 1. Nuestro cuestionario no usa imágenes → **se eliminó el ancla**. El paquete ya no referencia `Latidos.gif` y el cuestionario sigue resolviendo bien. |
| V6 | **Eliminar la página «EJERCICIOS»** | `NODOS_EXCLUIDOS = {"EJERCICIOS"}` en el generador. El curso queda en **16 páginas** (15 de contenido + el cuestionario). El guion conserva el nodo como documentación. |
| V7 | **Navegación «Anterior / Siguiente» al pie** en vez de arriba a la derecha | Nova la fija arriba (`position: fixed`) desde un `div.nav-buttons` que en el HTML ya está justo después de `</main>`. El post-proceso lo mete **dentro de `<main>`** (último hijo), para que herede el hueco del menú lateral y los puntos de ruptura del tema, y el CSS del proyecto lo devuelve al flujo: queda al pie, alineado con la columna de texto y visible justo al terminar de leer (40 px por debajo del contenido). Extra: por debajo de 1024 px se recuperan las etiquetas de los botones (Nova las ocultaba porque arriba compartían barra). **Ojo:** el export SCORM 1.2 no lleva estos botones (`hideNavButtons`), la navegación la da el índice del LMS; el cambio se ve en el HTML5 y en el `.elpx`. |
| V8 | **Portada con el texto sobre la imagen** (overlay), formateado y con sombra | El título, el subtítulo y la línea «Duración · Nivel» van superpuestos sobre la foto; la introducción queda debajo, sobre el fondo claro. La foto es clara por zonas (contraste medio del blanco: 4,96:1 en la franja baja, 2,87:1 en la esquina inferior derecha), así que no basta la sombra: el texto va sobre un **degradado oscuro** y además lleva sombra propia. Medido sobre el render real: contraste del blanco **17:1 de media y 9,6:1 en el percentil 95** (la peor zona). Es **responsive por contenedor**: si la columna de contenido no da de sí (menos de 520 px: móvil, o tablet con el menú abierto), el texto pasa automáticamente **debajo** de la imagen y en color oscuro. |

**Efecto colateral corregido:** sin titular, la cabecera vacía del bloque reservaba **60 px** y dejaba
suelto el botón de plegado de Nova. Se añadió el CSS del proyecto (`pp_extraHeadContent`) para anular
los dos. El exportador **SCORM 1.2** de eXeLearning 4 ignora esa propiedad, así que
`herramientas/postproceso_export.py` la inyecta en las páginas del zip SCORM (paso idempotente dentro
de `herramientas/exportar.sh`).

**Entregables regenerados:** `.elpx` (ahora paquete completo con tema y html renderizado, producido por
el CLI en formato `elpx`), SCORM 1.2 y HTML5 en `entregables/`; la vista previa de
`entregables/html5_preview/` se reconstruye desde el HTML5. La versión anterior (revisión III, con el
tema puesto desde la app) queda en `entregables/historial/`.

---

## 7. REVISIÓN V (13-sep-2026): revisión de terminología del texto

Petición del autor: limpiar y estandarizar los textos del curso. Sobraban **etiquetas de licencia y de
facturación** («con licencia», «gratis», «de pago», «Copilot Pro», precios) que entorpecían la lectura
pedagógica, y faltaba una distinción clara entre **dónde opera** Copilot y **qué puede hacer**.

| # | Cambio | Qué se hizo |
|---|--------|-------------|
| T1 | **Fuera las etiquetas de licencia y los precios** | Eliminadas del texto didáctico las expresiones «(con licencia)», «(sin licencia)», «(versión de pago/free)», «Copilot Chat (gratis)», «Copilot Pro» y la tabla de precios (~$21-30/usuario/mes). En las fichas de recursos se quita también «sin licencia externa». |
| T2 | **Entornos con nombre funcional** | **Copilot Web** (o «Modo Web») = asistente general, basado en búsqueda web y sin acceso a Microsoft Graph; **Copilot de Trabajo** (Microsoft 365 Copilot) = asistente conectado a los datos internos (SharePoint, Teams, correo, archivos). El Nodo 4 pasa de «Niveles de Copilot» a **«Copilot Web y Copilot de Trabajo»** (menú, sitemap y encabezado) y su tabla deja de ser de precios para ser de entornos. |
| T3 | **Tres niveles funcionales explícitos** | **Nivel 1 — Copilot Asistente / chatbot estándar** (reactivo), **Nivel 2 — agentes especializados o declarativos** (rol y base de conocimiento acotada; Agent Builder) y **Nivel 3 — agentes avanzados / de Copilot Studio** (proactivos: acciones, API externas y disparadores). Se explican en el Nodo 3, se etiquetan en el acordeón del Nodo 6 (cada tipo de agente con su nivel), en la nota del Nodo 11, en el resumen y en el glosario. |
| T4 | **Corrección conceptual chatbot vs. agente** | El texto ya no dice que un chatbot «solo da texto» frente a Copilot «con licencia», ni que un agente se distinga por «escuchar el entorno» (Nodo 5, sección Percepción). La diferencia se explica por **alcance, herramientas y autonomía**: el agente planifica y ejecuta acciones sobre los sistemas conectados. |
| T5 | **Índice, objetivos, cuestionario, ejercicios y glosario** | Actualizados a los términos nuevos. En el cuestionario: P1 pasa a comparar Copilot Web y Copilot de Trabajo, P4 dice «agente avanzado» y P7 evalúa el salto de Agent Builder (nivel 2) a Copilot Studio (nivel 3: acciones y disparadores). Ejercicio 1 distingue **Web (W)** frente a **agente de Trabajo (A)**. Glosario con entradas nuevas de los dos entornos y de los tres niveles. |

**Artefactos y verificación de esta revisión**

- Guion y maestro actualizados por script, con copia previa en `legado_articulate/backups_guion/`:
  `herramientas/revision_terminologia.py` (guion: nodos 2, 3, 4, 5, 6, 16, 17 y sustituciones
  puntuales) y `herramientas/revision_terminologia_maestro.py` (documento maestro). Ambos comprueban
  antes de escribir y abortan si un patrón no coincide.
- El generador necesitó dos ajustes: la ancla del Nodo 4 pasa a `**Tabla de entornos:**` y se corrigió
  `markdown_a_html` (**bug heredado**: el reemplazo de «---» troceaba las filas de separación de las
  tablas y dejaba una fila fantasma de guiones; ahora solo se sustituyen los «---» sueltos).
- `herramientas/verificar_paquete.py` incorpora 8 comprobaciones nuevas de terminología y de tablas:
  sin etiquetas de licencia ni nombres antiguos en el paquete y en los dos exports, entornos con
  nombre funcional presentes, y ausencia de filas fantasma. **70 comprobaciones, todas en verde.**
- `herramientas/pruebas_interaccion.py` en Chrome real: acordeón (desplegar/plegar), cuestionario
  (la P1 nueva se carga, se responde y puntúa) y navegación al pie. **Todo OK.**
---

## 8. REVISIÓN VI (13-sep-2026): remediación de cumplimiento del Art. 4

Origen: el análisis `../normativa_IA_EU/04_Gap_Analisis_Curso_Copilot_vs_Art4.md` (auditoría del curso
frente al contenido mínimo del Artículo 4). El curso cubría los bloques C y D, pero **no tenía bloque E
(marco legal) ni el bloque A completo (fundamentos de IA)**, y el paquete no incluía ejercicios.

### Qué se cambió

| # | Cambio | Detalle |
|---|--------|---------|
| R1 | **El curso pasa de 16 a 25 páginas** y de 3 a **4 módulos**: fundamentos de IA, Copilot en tu día a día, uso responsable y marco legal | El menú sigue mostrando «N. Título»; la etiqueta de módulo solo vive en el sitemap (§2) |
| R2 | **7 páginas nuevas** | Fundamentos de IA (Nodos 3 y 4), inventario de IA de la empresa (14), permisos y sobreexposición (18), política de uso y protocolo de incidentes (19), el AI Act (20), Artículo 4 (21) y datos personales, derechos y supervisión humana (22) |
| R3 | **Vuelve la página de EJERCICIOS** (decisión que revoca la V6) | Nodo 23, recortado a **4 ejercicios** con respuestas comentadas: entornos, instrucciones, análisis de riesgos y caso práctico. Los otros 4 quedan como banco de reserva en el anexo del maestro. Motivo: el expediente de conformidad pide evidencia de **caso práctico aplicado** |
| R4 | **Cuestionario de 10 a 20 preguntas** | Se conservan las 10 de producto y se añaden 10 de fundamentos, límites, inventario, sobreexposición, Artículo 4, RGPD y política. Aprobado: **14/20 (70 %)** |
| R5 | **Objetivos docentes de 6 a 10** | Los cinco nuevos cubren los bloques A, B, C, D y E del contenido mínimo |
| R6 | **Tres diagramas nuevos** | `diagrama_ia_al_agente` (Nodo 3), `diagrama_sobreposicion` (Nodo 18) y `diagrama_niveles_riesgo` (Nodo 20); SVG propios exportados a PNG 1600×1000 y verificados con visión |
| R7 | **Generador por clave** | `componentes_de_nodo()` despacha por **título del nodo** (`C_*`), no por número: añadir o reordenar páginas ya no exige tocar la lógica. `NODOS_EXCLUIDOS` queda vacío y `NODOS_ESPERADOS = 25` |
| R8 | **Verificador ampliado** | 80 comprobaciones: 25 páginas, 4 acordeones y sus enlaces, 10 imágenes, 20 preguntas, **terminología sin precios** y un bloque nuevo de **cumplimiento** (el curso contiene «AI Act», «Reglamento (UE) 2024/1689», «responsable del despliegue», «RGPD», «AESIA», «sobreexposición», «shadow AI»…) |
| R9 | **Expediente de cumplimiento** | Carpeta `cumplimiento/`: matriz de trazabilidad, memoria de justificación, política de uso de IA, acta y certificado, y temario (3,5 h) |

### Inconsistencias corregidas de paso

| # | Inconsistencia detectada | Corrección |
|---|--------------------------|------------|
| C1 | El maestro seguía citando un precio en la FAQ («Copilot Business desde ~$21/usuario/mes»), contra la decisión T1 | Eliminado: el maestro se reconstruye desde los bloques del guion, sin precios, y el verificador prohíbe «usuario/mes» y «Copilot Business» |
| C2 | El Ejercicio 1 del maestro marcaba ChatGPT y Gemini como «Copilot Web» (conceptualmente falso) | Reescrito: el curso ya no cita asistentes de terceros por su marca; habla de «un asistente web» y de «herramientas no autorizadas» (que es lo que importa en compliance) |
| C3 | Metadatos del maestro obsoletos (28 páginas, 12 términos de glosario, resumen en dos horas) y «## PARTE 2» duplicado | Maestro y anexo de estructura regenerados: 25 páginas, glosario de 29 términos, cuatro partes + cierre |
| C4 | El glosario no estaba ordenado | Reordenado alfabéticamente (29 entradas) y ampliado con los términos legales y de uso responsable |
| C5 | El nodo 4 del guion seguía titulándose «Entornos de Copilot: Web y Trabajo», contra lo documentado en la revisión V | Renombrado a «Copilot Web y Copilot de Trabajo» (menú, sitemap y encabezado) |

### Cómo se aplicó

- **Fuente única:** el contenido nuevo se redactó una sola vez en
  `herramientas/revision_vi_nodos_nuevos.md`; `herramientas/revision_vi.py` reconstruyó el §4 del guion
  con el orden final de 25 nodos, remapeó las referencias «Nodo N» de los bloques conservados y
  regeneró el maestro a partir del mismo texto (en prosa), con copias previas en
  `legado_articulate/backups_guion/`.
- **Verificación:** `generar_curso_elpx.py --check` (fidelidad de los 24 nodos de texto y de las 20
  preguntas), `verificar_paquete.py` (**80 comprobaciones, todas en verde**),
  `pruebas_interaccion.py` en Chrome real (acordeón, cuestionario de 20 preguntas, navegación al pie,
  portada con overlay) y `capturar_pantallas.py` (7 capturas en `entregables/capturas/rev6/`).
- **Fuentes del contenido legal** (verificadas el 13-sep-2026): Q&A de la AI Office sobre alfabetización
  en IA (`digital-strategy.ec.europa.eu`), Reglamento (UE) 2024/1689 y Reglamento (UE) 2026/1744
  (EUR-Lex), y el proyecto de ley orgánica español (BOCG-15-A-97-1, 12-jun-2026, en tramitación).
  La AI Office estructura el contenido mínimo en los pasos **a) a d)**, que es la matriz que usa
  `cumplimiento/01_Matriz_Trazabilidad_Art4.md`.
