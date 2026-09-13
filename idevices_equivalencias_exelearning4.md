# EQUIVALENCIAS DE iDEVICES — guion → eXeLearning 4 (instalado)

**Curso:** Agentes de IA y Microsoft Copilot para tu día a día
**Fecha:** 12-sep-2026
**Versión instalada:** eXeLearning 4 (`package.json` del contenedor: *«eXeLearning 4 is an AGPL-licensed
free/libre tool to create and publish open educational resources»*, versión `0.0.0-alpha`, sobre Bun/Elysia).
Contenedor podman `exelearning` → http://127.0.0.1:8090
**Para qué sirve este documento:** el guion (`guión_curso_copilot_exelearning.md`, §4 y §5) nombra
iDevices de una generación anterior de eXeLearning. Aquí está el mapeo verificado contra el catálogo
real de la versión instalada. **Donde dice «iDevice X», esto es lo que hay que poner.**

Todas las comprobaciones de este documento están hechas sobre el contenedor en ejecución
(`podman exec exelearning …`), no sobre documentación de terceros.

---

## 1. LO QUE NO EXISTE EN ESTA VERSIÓN

El catálogo real tiene **52 iDevices**. De los que pide el guion, **solo «Texto» y «Cuestionario»
existen con ese nombre**. Estos cuatro NO existen ni como iDevice ni con otro nombre:

| Guion pide | ¿Existe? | Evidencia |
|------------|----------|-----------|
| **Tabla** | No | No hay iDevice `table` en `/app/public/files/perm/idevices/base/`. La tabla es una **herramienta del editor de texto** (plugin TinyMCE `table`, ver §3). |
| **Acordeón** | No como iDevice | Ningún iDevice de acordeón. Pero **sí existe como Efecto nativo**, ver §4 (resuelto). |
| **Lista numerada** | No | No hay iDevice de lista. La lista ordenada es una **herramienta del editor de texto** (botones `bullist`/`numlist`). |
| **Nota** | No | No hay iDevice «Nota». Equivalentes posibles en §5. |
| «Proceso» (Nodo 7, condicional) | No | No existe. Alternativa en §4.3. |
| «Lista de definiciones» (Nodo 17, condicional) | No como iDevice | El editor TinyMCE **sí** trae el plugin `definitionlist` (§3). |

---

## 2. TABLA DE EQUIVALENCIAS (los 30 iDevices del guion)

> **Nota (revisión IV):** esta tabla describe el catálogo real de eXeLearning y sigue vigente. Lo que
> cambió es el agrupamiento al montar: **cada página es ahora UN único iDevice Texto** (un bloque sin
> titular), con los fragmentos que antes iban en iDevices separados. El recuento «30 iDevices» es el
> del guion; el montaje produce **16 componentes** (15 Texto + 1 Test). Ver
> `pendientes_montaje_exelearning.md` §6.

Recuento del guion (§4 y §5): **17 nodos, 30 iDevices**. Mapeo uno a uno:

| Nodo | Guion §4 (iDevice) | Real en eXeLearning 4 | Cómo se hace exactamente |
|------|--------------------|------------------------|--------------------------|
| 1 | Texto (título) + Texto (subtítulo) + Texto (introducción) ×3 | **Texto** (`text`) | 1:1. Tres iDevices Texto. |
| 2 | Texto (formato amplio) | **Texto** | 1:1. |
| 2 | Lista numerada (objetivos) | *no existe* → **Texto** | Lista ordenada con el botón `numlist` dentro del iDevice Texto. |
| 3 | Texto (formato amplio) | **Texto** | 1:1. |
| 3 | Nota (definición clave) | *no existe* → ver §5 | Opción recomendada: cita (`blockquote`) o caja «Ejemplo». |
| 4 | Texto (intro) | **Texto** | 1:1. |
| 4 | Tabla (entornos de Copilot: Web / Trabajo) | *no existe* → **Texto** | Tabla insertada con el botón Tabla del editor (plugin `table`). |
| 5 | Texto (intro) | **Texto** | 1:1. |
| 5 | Acordeón (5 secciones) | *no existe como iDevice* → **Efecto «Acordeón»** | Plugin `exeeffects`: botón «Efectos (acordeón, pestañas, paginación…)» del editor. Ver §4. |
| 6 | Texto (intro) | **Texto** | 1:1. |
| 6 | Acordeón (5 secciones) | **Efecto «Acordeón»** | Igual que el Nodo 5. |
| 7 | Texto (intro) | **Texto** | 1:1. |
| 7 | Lista numerada (o «Proceso») | *no existe* → **Texto** (+ opción **Efecto «Pagination»**) | Lista ordenada; si se quiere paso a paso, efecto Pagination (§4.3). |
| 8 | Texto (formato amplio) | **Texto** | 1:1. |
| 9 | Texto (formato amplio) | **Texto** | 1:1. |
| 10 | Texto (formato amplio) | **Texto** | 1:1. |
| 11 | Texto (intro) | **Texto** | 1:1. |
| 11 | Lista numerada (5 pasos) | *no existe* → **Texto** | Lista ordenada. |
| 11 | Nota (Copilot Studio) | *no existe* → ver §5 | |
| 12 | Texto (intro) | **Texto** | 1:1. |
| 12 | Acordeón (5 reglas) | **Efecto «Acordeón»** | Igual que los Nodos 5 y 6. |
| 13 | Texto (formato amplio) | **Texto** | 1:1. |
| 13 | Nota (políticas de la empresa) | *no existe* → ver §5 | |
| 14 | Texto (contenido) | **Texto** | 1:1. |
| 14 | Nota (mensaje clave) | *no existe* → ver §5 | |
| 15 | Texto (formato amplio) ×1 | **Texto** | 1:1 (8 ejercicios como texto). |
| 16 | Cuestionario (Quiz) | **Test** (`quick-questions`) | Ver §6. |
| 17 | Texto (formato amplio) | **Texto** | 1:1. Glosario: lista de descripciones dentro del Texto (plugin `definitionlist`). |

**Resultado:** de los 30 iDevices del guion, **21 son iDevice «Texto» puro**, **1 es el iDevice «Test»**,
**3 son el efecto «Acordeón»** (Nodos 5, 6 y 12) y **5 se resuelven con herramientas del editor de texto
dentro de un iDevice Texto** (2 listas numeradas, 1 tabla, 4 «Notas» que además pueden ir como caja).
Es decir: **la estructura del guion se sostiene entera**; solo hay que cambiar *cómo se llama la cosa*.

---

## 3. LO QUE SÍ TIENE EL EDITOR DE TEXTO (iDevice «Texto»)

El iDevice Texto es **TinyMCE 5**. Configuración verificada en `/app/public/app/editor/tinymce_5_settings.js`:

| Necesidad del guion | Herramienta real | Evidencia |
|---------------------|------------------|-----------|
| Tablas (Nodo 4) | Plugin TinyMCE `table` (botón Tabla) | `/app/public/libs/tinymce_5/js/tinymce/plugins/table/` |
| Listas numeradas y con viñetas (Nodos 2, 7, 11) | Plugins `lists`, `advlist` (botones `bullist`, `numlist`) | toolbar del editor (`tinymce_5_settings.js`) |
| Citas / destacados | Plugin `blockquoteandcite` | `…/plugins/blockquoteandcite/` |
| Lista de definiciones (glosario, Nodo 17) | Plugin `definitionlist` | `…/plugins/definitionlist/` |
| Negrita, cursiva, títulos h1-h6 | `style_formats` del editor | `tinymce_5_settings.js` líneas 500-600 |
| Imágenes (los 8 recursos del proyecto) | Plugin `exeimage` (y `exemermaid`, `exemindmap`, `template`) | toolbar del editor |
| **Efectos: acordeón, pestañas, paginación, carrusel, línea de tiempo** | **Plugin `exeeffects`** | toolbar del editor (`exeeffects`) + `/app/public/libs/tinymce_5/js/tinymce/plugins/exeeffects/` |

Dato clave para no perder tiempo: **el editor acepta cualquier marcado**. En `tinymce_5_settings.js`:

```js
getValidElements: function () { var e = '*[*]'; return e; }   // línea 817
```

`*[*]` = **cualquier etiqueta con cualquier atributo**. No va a borrar clases, estilos ni atributos
`data-*`. Y el editor carga el CSS del tema y el de Bootstrap (`getContentCSS`, línea 799), así que lo
que se ve editando es lo que se verá publicado.

---

## 4. EL ACORDEÓN: RESUELTO (no hace falta inventar nada)

### 4.1 La solución: el efecto «Acordeón» del plugin de Efectos

eXeLearning 4 incluye el plugin TinyMCE **`exeeffects`** («Efectos»), cuya etiqueta en la interfaz es
literalmente **«Efectos (acordeón, pestañas, paginación…)»** (traducción en
`/app/translations/messages.es.xlf`, línea 9501). Incluye **Accordion, Tabs, Pagination, Carousel y
Timeline**.

Cómo se aplica: dentro de un iDevice **Texto**, se escribe el contenido en secciones (un encabezado por
sección) y se aplica el efecto desde el botón «Efectos». El HTML resultante es este (definido por el
propio plugin en `…/exeeffects/readme.txt`):

```html
<div class="exe-fx exe-accordion">
  <div>
    <div class="fx-accordion-section">
      <a class="fx-accordion-title fx-accordion-title-0 fx-C1" href="#"><h2>Título A</h2></a>
      <div class="fx-accordion-content"><p>…</p></div>
      <a class="fx-accordion-title fx-accordion-title-1 fx-C1" href="#"><h2>Título B</h2></a>
      <div class="fx-accordion-content"><p>…</p></div>
    </div>
  </div>
</div>
```

Es **exactamente la interacción que pide el guion** («haz clic en cada componente para descubrirlo»,
«puede abrir y cerrar secciones libremente») y **no requiere JavaScript propio**: el efecto se resuelve
con los ficheros que ya viajan en el curso exportado:

- `/app/public/app/common/exe_effects/exe_effects.css` y `…/exe_effects.js` — **referenciados en el
  exportador** (`/app/public/app/yjs/exporters.bundle.js`), es decir, se copian al paquete exportado.
- El CSS del acordeón (`.fx-accordion-title`, `.fx-accordion-content`…) está en `exe_effects.css`.

**Trampa verificada (importante si se genera el HTML por código):** el JS del plugin enlaza cada título
con su contenido **por identificador**, no por posición. El marcado tiene que reproducir su
nomenclatura exacta o el clic no despliega nada (el contenido se queda en `display:none`):

```html
<div class="exe-fx exe-accordion">
  <div id="exe-accordion-0">
    <div class="fx-accordion-section">
      <a class="fx-accordion-title fx-accordion-title-0 fx-C1" href="#exe-accordion-0-0"
         id="exe_accordion_0-0-trigger"><h2>Título A</h2></a>
      <div class="fx-accordion-content" id="exe-accordion-0-0">…</div>
      …
```

Reglas (sacadas del propio `exe_effects.js`): el `href` del título apunta al **id del div de contenido**;
el `id` del título es el del contenido con los **dos primeros guiones como guion bajo** más `-trigger`
(de ahí el script deriva el contenedor a cerrar). El título va en `<h2>` (el plugin lo usa para el
comportamiento de abrir/cerrar). Comprobado en navegador: despliega y vuelve a plegar al segundo clic.

**Coste: cero.** No hay que crear iDevices nuevos ni tocar el tema. Y cumple la regla 7 del guion
(«Sin JavaScript propio»): el JS lo pone eXeLearning.

### 4.2 Aplicación a los tres nodos

| Nodo | Contenido del guion | Cómo montarlo |
|------|---------------------|---------------|
| 5 | 5 componentes (Percepción, Razonamiento, Herramientas, Memoria, Comunicación) | 1 iDevice Texto: intro + 5 secciones con encabezado + efecto **Acordeón** |
| 6 | 5 tipos de agente (Researcher, Analyst, Facilitator, Cowork, personalizados) | Igual |
| 12 | 5 reglas de instrucciones (con ejemplos «Mal» / «Bien») | Igual. Los ejemplos «Mal» en cursiva, «Bien» en negrita (como pide el guion); el icono `icono_check.png` / `icono_cross.png` se puede insertar como imagen dentro de cada sección |

### 4.3 Alternativas (documentadas, no recomendadas salvo el Nodo 7)

| Alternativa | Qué es | Coste | Cuándo usarla |
|-------------|--------|-------|----------------|
| **Efecto «Acordeón»** | Desplegable por clic | Nulo | **Recomendado** (Nodos 5, 6, 12) |
| Efecto «Tabs» (pestañas) | Pestañas horizontales, una visible | Nulo | Si se prefiere no mostrar todas las cabeceras |
| Efecto «Pagination» / «Carousel» | Contenido paginado con botones ◄ ► | Nulo | **Candidato para el Nodo 7** (el guion quería un «Proceso» paso a paso) |
| Efecto «Timeline» | Línea de tiempo desplegable | Nulo | Si el Nodo 7 se quiere como secuencia temporal |
| Tarjetas de memoria (`flipcards`) | Tarjetas que giran al clic (anverso/reverso) | Bajo, pero reescribe el contenido | Solo si se acepta partir el texto en tarjetas |
| Texto con encabezados (sin efecto) | 5 secciones normales | Nulo | Si se prioriza la máxima accesibilidad y cero dependencias |
| **Acordeón de Bootstrap a mano** | HTML `<div class="accordion">` pegado en el Texto | Redundante | **No usar**: `bootstrap.bundle.min.js` y `bootstrap.min.css` sí viajan en el export (verificado en `exporters.bundle.js`), pero el efecto nativo ya hace lo mismo mejor |

### 4.4 Lo que NO sirve

- **`slide` (Slide)** — aunque su nombre engaña, es un «Visual slide editor (canvas-based)» con Fabric.js:
  un lienzo de dibujo, no un carrusel de secciones de texto. **Descartado.**
- **`hidden-image` (Imagen oculta)** — revela zonas de una imagen; obligaría a meter imágenes dentro del
  acordeón, cosa que el guion prohíbe expresamente.

---

## 5. LA «NOTA» DESTACADA (Nodos 3, 11, 13 y 14) — decisión tomada

No hay iDevice «Nota» ni un estilo «Nota» en el editor (los `style_formats` del editor son: encabezados,
inline, bloques —párrafo/cita/div/pre— y alineación; `tinymce_5_settings.js` líneas 500-600).

**Decisión del montaje: cita destacada (`<blockquote>`) dentro del iDevice Texto, con el icono del
guion encima.** Es lo más fiel, no depende de componentes con semántica distinta y encaja con que el
propio guion ya escriba estas notas como citas (`> **Definición clave:** …`). Se aplica a los 4 casos:

| Nodo | Icono (fila «Recurso gráfico») | Contenido de la Nota |
|------|-------------------------------|----------------------|
| 3 | `icono_nota.png` | Definición clave (está en el contenido del nodo) |
| 11 | `icono_nota.png` | Aviso sobre Copilot Studio (está en el contenido) |
| 13 | `icono_nota.png` | «Conoce las políticas de tu empresa» (último párrafo del contenido) |
| 14 | `icono_warning.png` | Mensaje clave (está en las **notas de producción** del guion, que es donde el guion dice qué lleva la Nota) |

Descartado tras verificarlo en el contenedor:

- **`example` («Ejemplo») NO sirve como caja de texto**: no es un iDevice de contenido, es la
  **implementación de referencia** del patrón Standard JSON de la api-version 3.0 (sus campos son
  `text`, `dataList`, `number`, `color`, `switch`, `radio`, es decir, un formulario de demostración).
  Es el único iDevice del catálogo marcado `downloadable=1`.
- **`casestudy` («Caso práctico»)**: sí es una caja real, pero su estado es «historia + actividades»
  (`history`, `activities[]` con feedback) y su etiqueta visible es «Caso práctico»: no encaja como
  «Nota» ni semántica ni visualmente.
- **`<div class="alert alert-info">` de Bootstrap**: funciona (Bootstrap viaja en el export), pero
  introduce marcado manual sin ventaja sobre la cita.

---

## 6. EL CUESTIONARIO (Nodo 16) — iDevice «Test», configuración verificada

El iDevice se llama **«Test»** en la interfaz (slug `quick-questions`; su código es el clásico `quext`
de eXeLearning). El estado real que guarda (descifrado del fixture oficial y comprobado en el curso
generado) es este:

| Requisito del guion | Clave real del estado | Valor aplicado |
|---------------------|----------------------|----------------|
| 10 preguntas de opción múltiple | `questionsGame[]` (22 claves por pregunta) | 10 objetos, 4 opciones cada uno |
| 1 punto por pregunta | `customScore` (por pregunta) + `weighted` (total) | `1` / `100` |
| Que se muestren **las 10** preguntas | `percentajeQuestions` | `100` |
| Feedback por pregunta | `msgHit` y `msgError` (por pregunta) + `msgs` (52 textos de interfaz) | textos del guion |
| Orden fijo (no aleatorio) | `optionsRamdon`, `answersRamdon` | `false` |
| Actividad evaluativa | `evaluation` (+ `evaluationID`) | `true` |
| Puntuación al LMS | `isScorm` | `1` |
| Opción correcta | `solution` (índice 0-3) | marcada en el guion con `[CORRECTA]` |

**Aviso importante sobre dos claves que se confunden con facilidad:**

- `percentajeQuestions` **no es la nota de corte**: es el **porcentaje de preguntas que se muestran**
  (el editor lo etiqueta «% Questions» y calcula `num = porcentaje * total / 100`). Poner 70 hacía que
  el cuestionario preguntara solo 7 de las 10. Con `100` se muestran todas.
- `percentajeFB` es el «% de aciertos para ver el feedback», no la nota de corte.

**Nota de corte (7/10):** no viaja en el paquete. La política SCORM 1.2 de eXeLearning
(`/app/public/app/common/scorm/scorm12/exe-scorm12-policy.js`) lee la nota de corte del LMS
(`cmi.student_data.mastery_score`) y solo si el LMS no la publica aplica su umbral por defecto, que es
**50**. Es decir: el curso informa la puntuación real (0-100; con 1 punto por pregunta, 7 aciertos = 70),
y el «aprobado 7/10» se cierra **configurando la nota de corte 70 en el LMS**. Existe una propiedad
`masteryScore` en eXeLearning (categoría *scorm*) que va al manifiesto, pero está marcada
`excludeFromXml`, así que **no se puede fijar desde `content.xml`**: habría que abrir el proyecto en la
aplicación, ponerla y exportar desde ahí. Ver `evaluacion_generar_paquete_vs_cdp.md` §5.

---

## 7. CONSECUENCIAS SOBRE EL GUION (qué hay que retocar)

El guion **no necesita reescribirse**: su contenido (los textos) es válido tal cual. Solo hay que
corregir las filas «iDevice(s)» y las notas de producción que nombran aparatos que no existen:

| Nodo | Cambio en el guion |
|------|--------------------|
| 2 | «iDevice *Lista numerada*» → «lista ordenada dentro del iDevice Texto» |
| 3, 11, 13, 14 | «iDevice *Nota*» → caja «Ejemplo»/«Caso práctico» (11, 13, 14) o cita (3) |
| 4 | «iDevice *Tabla*» → «tabla dentro del iDevice Texto» |
| 5, 6, 12 | «iDevice *Acordeón*» → «efecto **Acordeón** (`exeeffects`) en un iDevice Texto» |
| 7 | «*Lista numerada* o *Proceso*» → lista ordenada, u opcionalmente efecto Pagination |
| 17 | «*Lista de definiciones* si está disponible» → lista de descripciones en el iDevice Texto |
| §5 | El recuento «30 iDevices» sigue siendo correcto **en intención**, pero el desglose real es: 21 Texto + 1 Test + 3 efectos Acordeón + 5 formatos dentro de Texto |
| §10 | La fila «Acordeón en vez de múltiples bloques de texto» sigue siendo válida, pero conviene citar el efecto `exeeffects` en lugar del «iDevice Acordeón» |

**Recuento real de objetos a crear en el editor: 22 iDevices** (21 Texto + 1 Test) **+ 3 efectos
Acordeón** aplicados dentro de iDevices Texto.

---

## 8. VERIFICACIÓN PENDIENTE (5 minutos, ya en la interfaz)

Estas dos comprobaciones necesitan el editor abierto y no se pueden hacer desde el contenedor. Son las
únicas cosas que dejo marcadas:

1. **Botón «Efectos»**: que aparezca en la barra del editor de texto y que el diálogo del efecto
   «Acordeón» parta el contenido por encabezados como se espera.
2. **iDevice «Test»**: que la nota de corte (7/10) y el feedback por pregunta se guarden y se exporten a
   SCORM 1.2 con `cmi.core.score.raw` y `lesson_status` (aprobado/suspendido).

---

## 9. FUENTES DE ESTE DOCUMENTO

Todo lo anterior está comprobado sobre el contenedor `exelearning` en ejecución. Rutas concretas:

- Catálogo y nombres ES: `/app/public/files/perm/idevices/base/*/config.xml` y `/app/translations/messages.es.xlf`
- Editor: `/app/public/app/editor/tinymce_5_settings.js` (líneas 500-600, 799-830)
- Plugins del editor: `/app/public/libs/tinymce_5/js/tinymce/plugins/`
- Efectos: `/app/public/libs/tinymce_5/js/tinymce/plugins/exeeffects/readme.txt` y
  `/app/public/app/common/exe_effects/exe_effects.{css,js}`
- Exportación: `/app/public/app/yjs/exporters.bundle.js`
- Cuestionario: `/app/public/files/perm/idevices/base/quick-questions/edition/quick-questions.js`
