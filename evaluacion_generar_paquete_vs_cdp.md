# ¿GENERAR EL PAQUETE O USAR EL CDP? — evaluación con evidencia

> **Nota (revisión VI, 13-sep-2026).** Este documento describe el montaje de la **revisión IV/V
> (16 páginas, cuestionario de 10 preguntas)**. El pipeline no ha cambiado; las cifras sí: el curso
> tiene ahora **25 páginas y 20 preguntas** y el verificador hace **80 comprobaciones**. Los pasos de
> este documento siguen siendo válidos para reproducir el entorno y entender los dos fallos
> encontrados y corregidos.

> **Nota (13-sep-2026):** documento de la **revisión III**. Describe el montaje, los fallos
> encontrados y la decisión técnica, y sigue vigente. Los cambios posteriores sobre el entregable
> (revisión IV: 16 páginas, un bloque por página, bloques sin titular, menú «N. Título», tema Nova,
> `Latidos.gif` y `.elpx` completo; revisión V: terminología del texto —entornos Copilot Web /
> Copilot de Trabajo, tres niveles funcionales, sin etiquetas de licencia— y el arreglo de la fila
> fantasma en las tablas) están en `pendientes_montaje_exelearning.md` §6 y §7 y en
> `00_LEEME_PRIMERO.md`. Con la revisión V el verificador pasa a **70 comprobaciones**, todas en
> verde, y las pruebas de interacción en Chrome siguen OK.

**Fecha:** 12-sep-2026 · **Instancia:** contenedor podman `exelearning` (eXeLearning 4, `0.0.0-alpha`)
**Pregunta a responder:** ¿de verdad se puede generar el paquete del curso por código e importarlo,
o hay que automatizar la interfaz (CDP)?

**VEREDICTO: sí se puede generar el paquete, y además es más barato que el CDP — y ni siquiera hace
falta importarlo para obtener el entregable.** eXeLearning 4 trae un **CLI propio** que convierte y
exporta paquetes **sin navegador**: se puede ir de `content.xml` generado a **SCORM 1.2** por línea
de comandos. Lo he probado de extremo a extremo dentro del contenedor (evidencia en §2).

**Recomendación: vía paquete (A).** El CDP solo como plan B para los dos detalles de §5.

---

## 0. ESTADO: EJECUTADO (12-sep-2026, misma sesión)

Esta evaluación ya no es teórica: **el curso se ha generado y exportado**, y está verificado en
navegador. Entregables en `entregables/`:

| Fichero | Qué es |
|---------|--------|
| `curso_copilot_agentes.elpx` | Proyecto generado (17 nodos, 30 componentes, 7 imágenes) — re-importable en eXeLearning |
| `curso_copilot_agentes_scorm12.zip` | **Entregable principal**: paquete SCORM 1.2 (`schemaversion 1.2`, `adlcp_rootv1p2`) |
| `curso_copilot_agentes_html5.zip` | Export HTML5 (autocontenido, abrible en cualquier navegador) |
| `content.xml` | La fuente generada, validada contra DTD y XSD |
| `html5_preview/` | El HTML5 descomprimido, para inspeccionarlo sin descomprimir nada |

Herramientas nuevas en `herramientas/`: `generar_curso_elpx.py` (el generador),
`verificar_paquete.py` (verificación sin navegador), `pruebas_interaccion.py` (prueba real de
acordeón y cuestionario por CDP), `extraer_componentes_elpx.py` y `plantillas/`.

**Lo que se hizo y salió bien:** `content.xml` válido contra DTD y XSD → `.elpx` → exportación SCORM 1.2
y HTML5 con el CLI → 28 comprobaciones automáticas en verde → y prueba en Chrome: portada, diagrama,
acordeón (despliega y pliega), tabla y cuestionario (10 preguntas, 1 punto por pregunta, feedback por
pregunta, aciertos registrados). Los textos del guion aparecen **completos** en el HTML generado,
nodo por nodo.

**Los dos fallos reales que aparecieron (y se corrigieron) están documentados en §7.** El enfoque
de paquete permitió detectarlos y arreglarlos en minutos, regenerando el curso entero; con el CDP
habrían sido dos sesiones de depuración clic a clic.

---

## 1. Las tres vías, comparadas

| | **A) Generar `.elpx` + CLI** | **B) Importar `.elpx` en la app** | **C) Automatizar la UI por CDP** |
|---|---|---|---|
| Qué es | Escribir `content.xml`, validarlo y exportar con el CLI del contenedor | Generar el `.elpx` y subirlo desde la interfaz (*Archivo → Importar*) | Manejar la SPA de eXeLearning con Chrome/CDP: crear 17 nodos, 30 iDevices, pegar textos… |
| Riesgo de formato | **Resuelto**: formato oficial documentado para agentes LLM + DTD y XSD locales | El mismo `.elpx`; importador documentado y código verificado | Ninguno de formato, pero **todo el riesgo está en la UI**: diálogos, editores TinyMCE, guardado Yjs |
| Verificable | **Sí, todo**: `xmllint` contra DTD/XSD, `unzip -l`, e inspección del SCORM exportado | Sí (contar nodos/iDevices tras importar) | Difícil: hay que creerse el resultado de la UI |
| Coste real | **Cero UI.** Un generador (Python) + 3 comandos | Cero UI para generar; 2 minutos de clic para importar | Alto: ~30 iDevices con editores distintos, cada uno con su diálogo |
| Fragilidad | Baja (todo determinista y re-ejecutable) | Baja | Alta (una clase CSS o un id cambia y se rompe la automatización) |
| Repetible | **Sí**: regenerar el curso entero en segundos | Sí | Casi nunca |
| Entregable | SCORM 1.2 y HTML5 **directos** | Editable en la app | Editable en la app |

Conclusión: **C es la más directa de entender y la más cara de ejecutar.** A es determinista, se
valida sola y produce el entregable final sin abrir el navegador.

---

## 2. LO QUE HE PROBADO (evidencia reproducible)

### 2.1 El CLI de eXeLearning 4 existe y exporta SCORM 1.2

```
$ podman exec exelearning bun dist/cli.js --help
...
ELPX Processing:
  elp:convert <input> <output>            Convert ELP v2.x to v3.0 (elpx)
  elp:export <input> <output> [format]    Export ELP to any format
  export-html5 / export-html5-sp / export-scorm12 / export-scorm2004 / export-ims / export-epub3
```

Formatos disponibles para `elp:export`: `html5`, `html5-sp`, `scorm12`, `scorm2004`, `ims`, `epub3`,
`elpx`. Acepta entrada por **stdin** (`elp:export - salida scorm12 < proyecto.elpx`).

### 2.2 Prueba de extremo a extremo (hecha, no supuesta)

1. Escribí a mano un `content.xml` **mínimo** (1 nodo, 1 iDevice Texto, con un acordeón `exe-fx`
   dentro) siguiendo el ejemplo oficial, y le añadí el `content.dtd` del contenedor.
2. Lo validé contra el esquema oficial **que trae la propia aplicación**:
   `xmllint --noout --dtdvalid content.dtd content.xml` → **válido**;
   `xmllint --noout --schema ode-content.xsd content.xml` → **válido**.
3. Lo empaqueté (`zip`) y lo exporté con el CLI dentro del contenedor:
   `bun dist/cli.js elp:export /tmp/probe.elpx /tmp/out_scorm scorm12` → **SUCCESS**, 290 KB.
4. Comprobé el resultado:

| Comprobación | Resultado |
|--------------|-----------|
| `imsmanifest.xml` | `schemaversion>1.2`, `adlcp_rootv1p2`, `imscp_rootv1p1p2` → **SCORM 1.2 real** |
| `index.html` | carga `exe_effects.js`, `exe_effects.css`, `bootstrap.bundle.min.js`, `jquery.min.js` |
| Acordeón | `exe-fx exe-accordion` y las dos secciones `fx-accordion-title-0/1` presentes en el HTML |
| Paquete | incluye `content.xml`, `content.dtd`, `theme/`, `libs/`, `idevices/`, `content/`, `index.html` |

Es decir: **el camino completo (`content.xml` → validación → SCORM 1.2) está funcionando hoy**, y el
acordeón nativo viaja y funciona en el paquete exportado.

### 2.3 El formato está documentado oficialmente (y pensado para LLM)

`https://exelearning.github.io/exelearning/llms-full.txt` — 416 KB con TODA la referencia del formato
`.elpx` (contenedor, `content.xml`, IDs, metadatos, páginas y bloques, catálogo de iDevices, patrones
de contenido, assets, pipeline de exportación/importación, validación, ejemplos) y un documento
específico **«Generating .elpx with an LLM»** con las 10 reglas no negociables, el pipeline en 4
etapas y la lista de causas de rechazo del importador.

Puntos clave que ya no hay que adivinar:

- Paquete **re-importable mínimo** = ZIP con **`content.xml` + `content.dtd`**. Nada más.
- Prohibido inventar: los tipos de iDevice deben ser los del catálogo (`text`, `casestudy`, …);
  los alias antiguos (`FreeTextIdevice`, `QuizTestIdevice`…) se aceptan al importar pero se normalizan.
- IDs con formato `[0-9]{14}[A-Z0-9]{6}`; IDs redundantes (`<odePageId>`/`<odeBlockId>` dentro de
  bloques y componentes) **deben** coincidir con los de su contenedor, o el componente se rechaza.
- `<htmlView>` y `<jsonProperties>` **siempre** en CDATA; si el contenido lleva `]]>` hay que partirlo.
- Validación obligatoria antes de exportar: `xmllint --noout --dtdvalid content.dtd content.xml`.
- El importador **no lee el HTML pre-renderizado**: reconstruye todo desde `content.xml`.

### 2.4 Hay fixtures oficiales reales para hacer ingeniería inversa (riesgo del quiz: cerrado)

En el repositorio oficial, `test/fixtures/`, hay paquetes reales de ejemplo, entre ellos
**`todos-los-idevices_dos_informes.elpx`** (23 MB) con **todos los tipos de iDevice**, y
`really-simple-test-project.elpx`, `basic-example.elp`, `Manual de eXeLearning 3.0.elpx`.

De ahí he extraído el **estado interno exacto del cuestionario** (`quick-questions`), que era la única
pieza con formato no publicado:

- El estado va en un `<div class="quext-DataGame js-hidden">` **codificado**: XOR de cada carácter con
  la clave `146` y luego `escape()` (percent-encoding). El «cifrado» está en
  `/app/public/app/common/common.js` (`encrypt`) y **el curso exportado ya lleva ese fichero**, así
  que es reproducible en Python en 3 líneas.
- El JSON tiene **36 claves de nivel superior** y cada pregunta **22 claves**. Las que pide el guion
  del Nodo 16 son exactamente estas:

| Requisito del guion | Clave real | Valor |
|---------------------|-----------|-------|
| 10 preguntas de opción múltiple | `questionsGame` (lista) | 10 objetos |
| 1 punto por pregunta | `customScore` (por pregunta) + `weighted` (global) | `1` / `100` |
| Aprobado 7/10 | `percentajeQuestions` | `70` |
| Puntuación al LMS | `isScorm` | `1` |
| Feedback por pregunta | `msgs.msgSuccesses` / `msgs.msgFailures` + `showSolution` | textos del guion |
| Orden fijo | `optionsRamdon` y `answersRamdon` | `false` |
| Actividad evaluativa (no juego) | `evaluation` | `true` |
| Opción correcta | `solution` (índice 0-3) | por pregunta |

Los `msgs` (52 cadenas de interfaz del quiz) se copian tal cual del fixture.

---

## 3. El pipeline que propongo (5 pasos, sin navegador)

```
1. Plan del curso  (ya existe: guion §2, 17 nodos)
2. Generador Python: guion -> content.xml      (IDs [0-9]{14}[A-Z0-9]{6}; texto -> textTextarea;
                                                acordeón -> HTML exe-fx; quiz -> JSON XOR 146)
3. Validación:     xmllint --dtdvalid content.dtd content.xml   (+ XSD)
4. Empaquetado:    zip -> curso.elpx  (content.xml + content.dtd [+ theme/libs/idevices/content])
5. Exportación:    bun dist/cli.js elp:export curso.elpx salida scorm12
                   bun dist/cli.js elp:export curso.elpx salida html5
```

Y, si se quiere el proyecto **editable** dentro de la aplicación: *Archivo → Importar* con ese mismo
`.elpx` (el importador está documentado y su código acepta el paquete mínimo). No hace falta para
entregar el curso: el paso 5 ya da el SCORM 1.2 y el HTML5.

---

## 4. Coste estimado

| Tarea | Vía A (paquete) | Vía C (CDP) |
|-------|-----------------|-------------|
| Generador de `content.xml` (17 nodos, 30 iDevices) | 2-4 h, la mayor parte escribir el generador una vez | — |
| Automatización de la UI (30 iDevices, 17 nodos, imágenes, quiz) | — | 6-12 h y frágil |
| Validación | `xmllint`, segundos | manual, pulsando |
| Regeneración tras un cambio de texto | ~1 min | repetir medio montaje |
| Exportar SCORM 1.2 | 1 comando | clics + descarga por navegador |

El trabajo pesado de la vía A (el generador) es exactamente el mismo que haría falta en cualquier
otra vía para no reescribir 70 KB de textos a mano.

---

## 5. Riesgos residuales (y su mitigación)

| Riesgo | Estado | Mitigación |
|--------|--------|------------|
| Formato de `content.xml` | **Cerrado**: validado contra DTD y XSD oficiales | — |
| Estado interno del cuestionario | **Cerrado**: extraído del fixture oficial, cifrado reproducible | — |
| El acordeón nativo en el paquete exportado | **Cerrado**: verificado en el `index.html` exportado | — |
| `screenshot.png` (1280×720) que pide el paquete «publicable v4» | No probado | Se genera con PIL; el importador no lo exige |
| `index.html`/`html/` pre-renderizados | **Cerrado**: los genera el propio CLI al exportar | — |
| Importar a la app para editarlo | Documentado + código del importador verificado, **no ejercitado** | 2 minutos: *Archivo → Importar* en la UI |
| SCORM 1.2 y nota de corte (7/10) reportando al LMS | Configuración identificada (`isScorm`, `percentajeQuestions`) | Probar una vez en un visor SCORM |
| Estilo/tema | Ninguno instalado con la paleta del guion | Aplazado por decisión del autor |

---

## 6. Fuentes

- Documentación oficial del formato (para LLM): `https://exelearning.github.io/exelearning/llms-full.txt`
  (y `…/llms.txt`). Secciones usadas: `container`, `content-xml`, `ids`, `metadata`, `pages-blocks`,
  `idevices/catalog`, `idevices/patterns`, `idevices/snippets`, `assets`, `export-pipeline`,
  `import-pipeline`, `validation`, `ai-generation`, `examples/minimal-content-xml`.
- Repositorio oficial: `https://github.com/exelearning/exelearning` — `test/fixtures/` (paquetes de
  ejemplo) y `src/shared/export/generators/OdeXmlGenerator.ts` (generador de referencia).
- Esquemas locales de la instancia: `/app/public/app/schemas/ode/content.dtd` y `ode-content.xsd`.
- CLI local: `bun dist/cli.js` dentro del contenedor (`elp:convert`, `elp:export`, `export-scorm12`…).
- Código del importador/exportador local: `/app/public/app/yjs/importers.bundle.js` y
  `exporters.bundle.js`; cifrado del quiz: `/app/public/app/common/common.js`.

**Nota sobre la versión:** la documentación citada corresponde a la línea v3+/v4 y la instancia es
`4.0.0-alpha`. Todo lo verificado en §2 se ha probado **contra la instancia real**, no contra la
documentación; los documentos solo se han usado para saber dónde mirar.

---

## 7. EJECUCIÓN: fallos encontrados, correcciones y pendientes

### 7.1 Los dos fallos reales (los encontró la verificación, no la intuición)

**(a) El acordeón no se desplegaba.** El HTML era válido y el JS viajaba en el paquete, pero al hacer
clic no pasaba nada: el plugin `exeeffects` enlaza cada título con su contenido **por identificador**
(`href="#<id del contenido>"` y un `id` del que deriva el contenedor), no por posición. La prueba de
interacción en Chrome lo detectó en el acto (las cinco secciones seguían con altura 0 tras el clic).
Corregido replicando la nomenclatura exacta del plugin; ahora despliega y vuelve a plegar.

**(b) El cuestionario preguntaba solo 7 de las 10 preguntas.** Yo había puesto `percentajeQuestions: 70`
creyendo que era la nota de corte. No lo es: es el **porcentaje de preguntas que se muestran** (el
editor lo etiqueta «% Questions» y calcula `num = porcentaje * total / 100`). Se vio porque el marcador
del quiz decía «Número de preguntas: 7». Corregido a `100`; ahora dice 10.

Los dos son fallos que **solo** aparecen ejecutando: el XML era válido, el paquete exportaba sin
errores y las comprobaciones estáticas pasaban. De ahí la utilidad de la prueba en navegador.

### 7.2 La nota de corte (7/10) no viaja en el paquete

El curso informa la puntuación real (0-100; con 1 punto por pregunta, 7 aciertos = 70) y `isScorm` está
activo, así que el LMS recibe la nota. Lo que **no** se puede fijar desde el paquete es el umbral de
aprobado:

- La política SCORM 1.2 de eXeLearning lee `cmi.student_data.mastery_score` **del LMS** y, si el LMS no
  la publica, aplica un umbral propio de **50** (`exe-scorm12-policy.js`).
- La propiedad `masteryScore` de eXeLearning existe (categoría *scorm*) y va al manifiesto, pero está
  marcada `excludeFromXml`: **no se lee de `content.xml`** y el CLI no la acepta como opción
  (probado: exportando con `masteryScore=70` en el XML, el manifiesto sale sin ella).

Por tanto, para el «aprobado 7/10» hay dos vías: configurar la nota de corte **70 en el LMS** (lo
habitual en SCORM 1.2) o abrir el proyecto en la aplicación, ponerla en las propiedades y exportar
desde ahí. Queda apuntado como pendiente.

### 7.3 Pendientes que quedan (ninguno bloquea el material)

| # | Pendiente | Quién |
|---|-----------|-------|
| A1 | Titular del curso (licencia de uso interno) — `pp_author` va vacío a propósito | Autor |
| A2 | Ruta del menú del *Planner Agent* en el tenant real (Nodos 8-10) | Autor |
| B1 | Nota de corte 70 en el LMS (o exportar desde la app con `masteryScore`) | Autor / TI |
| B2 | Probar el SCORM en un visor real (Moodle, SCORM Cloud) y ver `lesson_status` | Autor / TI |
| B3 | Tema y paleta: se ha usado el tema `base` por defecto (decisión aplazada) | Autor |
| B4 | Crédito de la portada: el curso lo lleva en el **Nodo 17** (como el guion); `CREDITOS.md` sigue diciendo «Nodo 15» y usa numeración antigua de nodos | Autor/agente |
