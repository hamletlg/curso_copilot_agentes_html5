# Propuesta: formato intermedio (guion → IR determinista → generador)

**Pregunta del autor:** ¿conviene un documento intermedio entre el guion técnico y la generación
real, en un formato estable, revisable y determinista (JSON/YAML), que sea lo que tome el script
generador?

**Respuesta corta:** sí, y los dos roces de hoy lo demuestran. Abajo está el porqué medido, la
forma concreta y cómo migrar sin romper nada.

---

## 1. Los problemas que tiene hoy el paseador del guion (con evidencia de esta sesión)

El generador (`herramientas/generar_curso_elpx.py`) lee el guion en markdown y **corta el texto por
literales**, porque el «Contenido en pantalla» es una sola celda de tabla con el texto, el marcado y
las instrucciones de montaje mezclados.

| Problema | Evidencia de hoy |
|---|---|
| **El montaje depende de literales dentro del texto** | `c.index("Un recorrido práctico")`, `c.index("> **Nota:**")`, `c.index("**1. Recibir la orden**")`, `c.index("**Tabla de entornos:**")`, `c.index("**Conoce las políticas de tu empresa**")`, `partes_acordeon()` buscando `**Sección N:` y `parse_quiz()` buscando `**Pregunta N:**` + `[CORRECTA]` |
| **Reescribir el texto puede romper el montaje** | El nodo 1 perdió «Un recorrido práctico» al reescribirlo: el generador habría lanzado `ValueError`. Hubo que añadir una red de seguridad (`volcar_guion.py`) que **rechaza** el nodo — o sea, el texto es rehén del montaje |
| **El guion no es revisable** | Cada nodo es una línea de hasta 9.000 caracteres (nodo 25). Un `git diff` de eso no lo lee nadie |
| **La decisión de montaje vive en el código** | `componentes_de_nodo()` + las 25 constantes `C_*`: qué iDevice, qué icono, dónde va la imagen y dónde la nota está en Python, no en el documento. Añadir una página obliga a tocar el generador |
| **Posición por texto, no por estructura** | El recuadro de ideas clave (hoy) y las notas (siempre) se colocan citando un fragmento literal del texto |
| **Sin esquema** | Nada valida el guion antes de generar: el cuestionario con 19 preguntas, una imagen que no existe o un `###` perdido se descubren al final, y hay respaldos silenciosos (clave desconocida → texto plano) |

Ninguno de los seis es un fallo del generador: es lo que pasa cuando el documento de trabajo y el
documento de montaje son el mismo fichero.

---

## 2. La forma concreta: `curso.json` como fuente de verdad del montaje

Un fichero JSON (biblioteca estándar: no añade dependencias) donde cada página es una lista de
**bloques tipados** y **no hay ni una instrucción de montaje dentro del texto**.

```jsonc
{
  "version": 1,
  "curso": {
    "titulo": "Agentes de IA y Microsoft Copilot para tu día a día",
    "duracion": "3,5 horas", "tema": "Nova", "idioma": "es-ES"
  },
  "paginas": [
    {
      "id": "p05",
      "orden": 5,
      "titulo_menu": "5. ¿Qué es un agente de IA?",
      "titulo_pagina": "¿Qué es un agente de IA?",
      "tipo": "texto",
      "bloques": [
        { "tipo": "parrafo", "texto": "Considera el siguiente caso." },
        { "tipo": "parrafo", "texto": "Pides a Copilot de Trabajo que prepare un resumen…" },
        { "tipo": "nota", "icono": "icono_nota.png", "etiqueta": "Definición clave",
          "texto": "Un agente de IA en Microsoft 365 es un asistente que planifica acciones…" },
        { "tipo": "parrafo", "texto": "La diferencia entre un chatbot y un agente…" },
        { "tipo": "lista", "ordenada": false, "items": [
          "**Nivel 1. Copilot Asistente (chatbot estándar)** Es una herramienta conversacional…",
          "**Nivel 2. Agentes especializados (o declarativos)** Tienen un rol concreto…",
          "**Nivel 3. Agentes avanzados (agentes de Copilot Studio)** Son proactivos…" ] },
        { "tipo": "recuadro", "tras": "bloque:3", "etiqueta": "Ideas clave", "items": [
          "Un chatbot responde y se detiene; un agente planifica y ejecuta.",
          "En Microsoft 365 hay tres niveles: asistente, especializado y avanzado.",
          "El mismo asistente cambia de nivel según el entorno y las herramientas." ] }
      ]
    }
  ],
  "recursos": { "imagenes": [ { "fichero": "diagrama_ia_al_agente.png", "alt": "…" } ] }
}
```

### Lo que arregla, problema por problema

| Problema de hoy | Con el IR |
|---|---|
| Cortes por literales en el texto | El bloque `nota` **es** una nota. No hay nada que buscar en el texto |
| Reescribir rompe el montaje | El texto es texto: la posición va en `"tras": "bloque:3"`, así que reescribir no puede mover nada |
| Guion ilegible en el `diff` | Un `git diff` de `curso.json` es un diff por líneas de bloques concretos |
| Montaje en el código | El generador pasa a ser un render genérico de bloques tipados; las 25 constantes `C_*` y sus casos especiales desaparecen |
| Posición por texto | Posición por **índice de bloque**: determinista y comprobable |
| Sin esquema | Esquema validado antes de generar: 25 páginas, cuestionario con 20 preguntas y una correcta cada una, toda imagen existe, todo `alt` presente, ningún `<br>` |

### Validaciones que se pueden hacer y hoy no

- 25 páginas y órdenes 1..25 sin huecos.
- Cuestionario: 20 preguntas, 4 opciones cada una, exactamente una correcta.
- Toda imagen citada existe en `recursos/imagenes/` y tiene texto alternativo.
- Todo bloque `recuadro` entre 3 y 4 viñetas y con `tras` apuntando a un bloque existente de su
  propia página.
- Toda página termina en un bloque de cierre si el guion lo pide.
- Terminología: sin «con licencia», «gratis», precios (hoy ya hay comprobaciones sueltas).

---

## 3. Cómo migrar sin riesgo

1. **Escribir el esquema** (`curso.schema.json`) y el **conversor** `guion → curso.json`
   (`herramientas/guion_a_ir.py`), determinista, solo biblioteca estándar.
2. **Prueba de equivalencia** (la clave de todo): `generar_curso_elpx.py --ir curso.json` y el
   generador actual deben producir **el mismo `content.xml`**, ignorando los identificadores
   aleatorios y las marcas de tiempo. Si coincide, la migración no cambia el curso ni un carácter.
   Es una prueba que se puede dejar en el repositorio y repetir.
3. **Cambiar el generador** para leer el IR (y borrar los casos especiales por clave de nodo).
4. **Mantener una sola fuente de verdad.** Dos opciones:
   - **(a) El guion manda** (mínimo cambio): el autor sigue escribiendo el guion markdown; el
     conversor produce `curso.json`; el generador consume el JSON. Se guarda la huella (hash) del
     guion dentro del JSON, como ya hace tu motor `plan` con los pasos, y el verificador avisa si el
     JSON se ha quedado atrás.
   - **(b) El IR manda** (más limpio a la larga): `curso.json` es la fuente; el guion markdown se
     **genera** desde él (`ir_a_guion.py`) para que el autor y el cliente lo revisen. Deja de haber
     dos documentos que puedan contradecirse.
   - **Recomendación:** (a) ahora, (b) cuando el IR esté probado. Empezar por (b) obliga al autor a
     escribir prosa en JSON el primer día, y eso no aporta nada.

---

## 4. Lo que cuesta, sin adornos

- Definir el esquema y el conversor: es trabajo de una sesión larga, no de un rato.
- Mientras conviven, hay que mantener el paseador actual **y** el conversor.
- El guion markdown sigue existiendo como documento del autor; si se elige (a), hay que recordar que
  el JSON es un derivado y se regenera.
- Riesgo real: si el conversor tiene un fallo, el curso se monta distinto. Por eso la prueba de
  equivalencia del punto 2 no es opcional.

## 5. Por qué creo que merece la pena

Los dos problemas que han aparecido hoy (el nodo 1 rechazado y tener que inventar una red de
seguridad para no perder texto) no son mala suerte: son la consecuencia directa de que el texto y
las órdenes de montaje vivan en la misma celda. El IR corta esa clase de fallo de raíz, y de paso
hace revisable, validable y diffeable lo que hoy es una línea de 9.000 caracteres.

Lo que **no** resuelve: la calidad del texto. Eso es el trabajo del modelo y de la plantilla.

## 6. Encaje con lo que se está haciendo hoy

- El recuadro de ideas clave ya está implementado con anclaje por texto (`POSICIÓN: tras «…»`).
  Funciona y está verificado, así que la entrega de hoy sale adelante.
- Cuando exista el IR, esos 8 recuadros pasan a ser `"tipo": "recuadro", "tras": "bloque:N"` y el
  anclaje por texto desaparece. La migración de los recuadros es mecánica.
- **Decisión:** esto es una **revisión VIII**, no algo que meter a mitad del lote de reescritura.
  Se hace con el curso ya regenerado y verificado, para que la prueba de equivalencia compare dos
  cosas buenas.

---

## 7. Decisiones tomadas (22-sep-2026)

| Decisión | Elegido |
|---|---|
| **Cuándo** | **Después.** Primero se cierra la reescritura (25 textos), los 8 recuadros y el CSS verificado en el producto. El IR es la **revisión VIII** |
| **Formato** | **JSON** canónico (solo biblioteca estándar, determinista, con esquema). El **guion markdown se genera** desde el IR (`ir_a_guion.py`) para que el autor y el cliente lo revisen |
| **Fuente de verdad** | **(a) El guion manda por ahora:** el autor sigue escribiendo el guion; el conversor produce `curso.json`; dentro del JSON se guarda la **huella (hash) del guion** y el verificador avisa si el JSON se ha quedado atrás. Se reevaluará el paso a (b) cuando el IR esté probado |

Orden de trabajo de la revisión VIII: esquema → `guion_a_ir.py` → **prueba de equivalencia de
`content.xml`** contra el generador actual → generador leyendo el IR → `ir_a_guion.py` → migrar los
recuadros a `"tras": "bloque:N"` y retirar el anclaje por texto.

