# Plan — Reescritura humana del guión + recuadros de ideas clave

**Objetivo:** los 25 textos del guión suenan a persona (no a LLM) y sin perder registro
profesional; y las páginas donde la información es crítica llevan un **recuadro de ideas
clave** a mitad de página, definido en el guión, con CSS propio y verificado en el producto.

**Estado: COMPLETADO** (22-sep-2026). Las fases 1 a 6 están hechas y verificadas; abajo queda el
resultado real de cada una y los dos hallazgos que aparecieron al verificar (uno de ellos, una pérdida
de contenido que no se habría visto sin la comprobación de fidelidad). Lo que sigue pendiente es la
decisión del autor sobre el maestro (§ «Riesgos») y la revisión VIII (formato intermedio).

**Modelo:** `gemma4-12b` en `llama-server :8080` (conmutador `LLAMACPP_MODEL_SWITCH`).

---

## Contexto verificado

| Qué | Dónde | Dato |
|---|---|---|
| Textos a reescribir | `guión_curso_copilot_exelearning.md` | campo **«Contenido en pantalla»** de 25 nodos, markdown |
| CSS propio del proyecto | `herramientas/generar_curso_elpx.py:77` (`ESTILOS_PROPIOS`) | se inyecta vía `pp_extraHeadContent` |
| Punto de montaje | `componentes_de_nodo()` en `generar_curso_elpx.py:619` | 1 iDevice Texto por página, bloques sin titular |
| Comprobación de fidelidad | `informe_fidelidad()` (`:860`) | verifica que el texto del guión aparece en el HTML |
| Exportación | `herramientas/exportar.sh` (CLI del contenedor `exelearning`) | `.elpx` + SCORM 1.2 + HTML5 + vista previa |
| Verificación sin navegador | `herramientas/verificar_paquete.py` | 80 comprobaciones |
| Verificación real | `herramientas/pruebas_interaccion.py` (Chrome CDP 9222) | acordeón y cuestionario |
| Paleta oficial | `legado_articulate/pautas_diseno/PAUTAS_DE_DISEÑO.md` | primario `#2563EB`, texto `#1E293B`, fondo 2º `#F8FAFC`, bordes `#E2E8F0` |

**Carpeta de trabajo de la reescritura:** `reescritura_humana/` (extractor, plantilla,
cliente del servidor, comparador). El guión original nunca se tocó hasta este plan.

---

## Fase 1 — Reescritura de los 25 textos con Gemma 12B

| # | Tarea | Salida | Verificación |
|---|---|---|---|
| 1.1 | Lote completo con el modelo 12B | `reescritura_humana/salida/gemma4-12b/nodo_NN_*.md` | 25 ficheros, `_tiempos.json` sin errores |
| 1.2 | Informe de conjunto (marcas de IA por nodo, longitudes, tiempos) | `reescritura_humana/informe_reescritura.md` | suma de marcas < original en todos los nodos |
| 1.3 | Copia de seguridad del guión | `legado_articulate/backups_guion/guión_...bak.<fecha>-pre-rec7` | fichero con el mismo sha256 que el guión de partida |
| 1.4 | Volcado de los 25 textos nuevos al campo «Contenido en pantalla» | guión revisado | `git diff` solo en ese campo; 25 nodos, ningún `<br>` perdido |
| 1.5 | Entrada de revisión **VII** en la cabecera del guión (§ revisiones) | guión revisado | texto nuevo, sin tocar las revisiones anteriores |

## Fase 2 — Recuadros de ideas clave: dónde y por qué

| # | Tarea | Salida | Verificación |
|---|---|---|---|
| 2.1 | Análisis didáctico página a página sobre el texto ya reescrito (criterio: densidad + información crítica + variedad) | `reescritura_humana/recuadros/seleccion.md` | 7–9 páginas objetivo de 25; ninguna página de cierre ni el cuestionario |
| 2.2 | Reparto de **posiciones** (tras qué bloque va cada recuadro), sin patrón fijo | misma tabla | ningún recuadro en el primer ni en el último bloque |
| 2.3 | Título normalizado del recuadro y reglas de redacción (3–5 viñetas, sin repetir enlaces ni cifras nuevas) | `reescritura_humana/prompts/recuadro.md` | — |

## Fase 3 — Los recuadros los escribe Gemma 12B

| # | Tarea | Salida | Verificación |
|---|---|---|---|
| 3.1 | Generar un recuadro por página seleccionada | `reescritura_humana/salida/recuadros/nodo_NN.md` | uno por página de la lista, sin error del servidor |
| 3.2 | Revisión de las reglas duras (3–5 viñetas, sin datos nuevos, sin marcas de IA) | `comparar.py` sobre los recuadros | 0 marcas de folleto/grandilocuencia |
| 3.3 | Ajuste manual de lo que el modelo deje flojo | ficheros finales | ninguno queda con viñetas de relleno |

## Fase 4 — Guión técnico y montaje

| # | Tarea | Salida | Verificación |
|---|---|---|---|
| 4.1 | Nueva fila de nodo **«Recuadro de ideas clave»** (`POSICIÓN:` + texto) documentada en §3 «Formato del guión» | guión | §3 lista el campo y su sintaxis |
| 4.2 | Recuadros volcados en la fila nueva de su nodo | guión | un recuadro por página de la lista de la fase 2 |
| 4.3 | `generar_curso_elpx.py`: leer la fila, buscar el `<h3>` ancla y **fallar en voz alta** si no lo encuentra | generador | sin `--check`: no rompe; con ancla falsa: mensaje claro |
| 4.4 | Recuadro en HTML accesible: `<aside class="caja-ideas-clave" aria-label="Ideas clave">` con etiqueta + lista | generador | aparece en `content.xml` |
| 4.5 | Extender `informe_fidelidad()` para que cubra también el texto del recuadro | generador | nodo con recuadro: «completo» |

## Fase 5 — CSS del recuadro

| # | Tarea | Salida | Verificación |
|---|---|---|---|
| 5.1 | Regla `.caja-ideas-clave` en `ESTILOS_PROPIOS` | `generar_curso_elpx.py` | coherente con la paleta (borde de acento azul + fondo claro) |
| 5.2 | Contraste WCAG AA calculado, no estimado (etiqueta pequeña + cuerpo) | `reescribir.py`/script de verificación | ≥ 4.5:1 en las dos combinaciones |
| 5.3 | Responsive (contenedor estrecho) y sin `!important` innecesario | CSS | a 400 px el recuadro no desborda |

## Fase 6 — Verificación en el producto final

| # | Tarea | Comando | Criterio |
|---|---|---|---|
| 6.1 | Regenerar `content.xml` y `.elpx` | `python3 herramientas/generar_curso_elpx.py --check` | fidelidad completa en los 25 nodos |
| 6.2 | Exportar `.elpx`, SCORM 1.2 y HTML5 | `sh herramientas/exportar.sh` | los tres ficheros se actualizan |
| 6.3 | Verificación sin navegador | `python3 herramientas/verificar_paquete.py` | 80/80 |
| 6.4 | **Estilo aplicado de verdad**: captura de una página con recuadro en Chrome | `capturar_pantallas.py` + inspección visual | el recuadro se ve como el CSS manda (borde, fondo, etiqueta) |
| 6.5 | Interacciones intactas | `python3 herramientas/pruebas_interaccion.py` | acordeón y cuestionario siguen funcionando |
| 6.6 | `git status` del guión y del generador | `git diff --stat` | sin ficheros colaterales tocados |

## Resultado (lo que ha pasado de verdad)

| Fase | Resultado |
|---|---|
| 1. Reescritura | **25/25 nodos** con `gemma4-12b`, **54,6 min**, 20,6 tok/s, 0 errores. Marcas de IA en el detector: **52 → 21**; las 21 restantes se revisaron una a una y son marcado estructural o falsos positivos (ver `informe_reescritura.md`). Volcado al guion: 34 cambios, 0 saltos |
| 2-3. Recuadros | **8 recuadros** (5, 10, 14, 17, 18, 19, 21, 22), 3-4 viñetas, sin datos nuevos. Posición medida **en el navegador** (nodo 19: 47 %; `verificar_recuadros.py` mide sobre el fichero y da 73-83 %, porque cuenta el marco de la página: para la posición real vale la medida del navegador) |
| 4-5. Guión y CSS | Fila `**Recuadro de ideas clave**` documentada en §3; `<aside class="caja-ideas-clave" role="note">`; CSS `#2563EB` sobre `#F8FAFC` (contraste 13,98:1 y 4,94:1, AA) |
| 6. Verificación | `verificar_paquete.py`: **86/86 OK**. `verificar_recuadros.py`: 8 recuadros correctos y CSS en los tres entregables. `pruebas_interaccion.py` en Chrome real: recuadro con su estilo aplicado (fondo y borde medidos por píxel) y respuesta modelo que se despliega. Capturas en `entregables/capturas/rev7/` |

### Dos hallazgos de la verificación (los dos, arreglados)

1. **Ancla duplicada en el nodo 19.** El ancla «El protocolo de incidentes» aparecía **dos veces** en
   la página montada (en el título y dentro de una viñeta anterior) y el generador se negaba a montar,
   con razón: montar el recuadro en el sitio equivocado en silencio es peor. Ancla nueva:
   **«Regla práctica: si tienes dudas»**, que cierra el bloque de clasificación de datos a mitad de
   página. Toda ancla nueva se comprueba antes de gastar el turno del modelo (`escribir_recuadros.py`).
2. **Las respuestas modelo de los ejercicios no llegaban al curso.** El exportador solo copia
   `ideviceId` al atributo `data-idevice-json-data`, así que el `text.js` del iDevice nunca recibía
   `textFeedbackTextarea`: los dos ejercicios de respuesta abierta salían **sin respuesta y sin
   botón**. La comprobación de fidelidad lo destapó al incluir por fin el texto de las actividades
   interactivas. Arreglado en `generar_curso_elpx.py`: la retroalimentación se monta dentro del
   `htmlView`, con el marcado nativo del iDevice, y hay comprobaciones nuevas (paquete y navegador)
   para que no vuelva a escaparse.

## Riesgos y decisiones abiertas

- **El maestro no lo toca este plan.** `contenido_curso_copilot_agentes.md` (fuente de verdad
  del contenido) comparte texto con el guión desde la revisión VI. Si no se sincroniza, quedan
  desalineados. → Decisión del autor al final (puede hacerse con el mismo volcado).
- **Regla 1 del montaje** («el guion manda, no inventar texto») sigue vigente: los recuadros se
  añaden al guión antes de montar, así que el generador no inventa nada.
- **Balance de los recuadros:** pocos y bien repartidos. Si una página ya es una lista o una
  tabla, el recuadro sobra; el valor está en las páginas de prosa densa.
- **Coste:** ~45 min el lote de reescritura + ~5 min los recuadros, con la GPU del usuario.
