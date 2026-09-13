# Memoria de justificación de la acción formativa en alfabetización en IA

> **Qué es.** El documento de cabecera del expediente: reúne en una sola pieza qué se hizo, con
> quién, cuándo y con qué resultado, y remite a las pruebas. Es la plantilla que se entrega al
> cliente (entregable 4 del pack) y la que se conserva **cuatro años**.
>
> **Cómo se usa.** Se rellenan los campos entre corchetes. Los apartados 4, 5 y 6 no dependen del
> cliente (el contenido del curso es el mismo); lo que cambia es el 1, el 2, el 3 y el 7.
>
> **Versión de la plantilla:** 13-sep-2026.

---

## 1. Datos de la acción formativa

| Campo | Valor |
|---|---|
| Organización | `[Razón social y CIF]` |
| Acción formativa | Alfabetización en inteligencia artificial para el uso responsable de Copilot (Microsoft 365) |
| Modalidad | Teleformación (e-learning auto-guiado con tutor) |
| Duración | 3,5 horas |
| Fechas de impartición | `[fechas]` |
| Plataforma / LMS | `[Moodle, o el LMS del cliente]` |
| Tutor / monitor | `[nombre y contacto]` |
| Participantes | `[número]` (ver Anexo II: relación de participantes) |
| Personas que operan IA por cuenta de la empresa | `[contratistas, proveedores o servicios externos que usan los sistemas, si los hay]` |

---

## 2. Por qué se hace (obligación y encaje)

- **Norma:** Artículo 4 del Reglamento (UE) 2024/1689 (AI Act), en su redacción tras el Reglamento
  (UE) 2026/1744 (Ómnibus digital sobre IA, en vigor desde el 27 de julio de 2026).
- **Obligación:** adoptar medidas para **apoyar el desarrollo de la alfabetización en IA** del
  personal y de otras personas que operen los sistemas por cuenta de la organización, sin obligación
  de garantizar un nivel concreto por persona.
- **Posición de la organización:** **responsable del despliegue** (Artículo 3.4 del AI Act), por el
  uso de sistemas de IA en su actividad profesional (Microsoft 365 Copilot).
- **Encuadre interno:** esta acción formativa forma parte del `[plan de formación anual / plan de
  compliance]` de la organización.

---

## 3. Inventario de sistemas de IA de la organización (punto de partida)

| Herramienta o función | Quién la usa | Para qué | Datos que trata | Autorizada |
|---|---|---|---|---|
| `[Copilot de Trabajo en Word, Excel, Outlook, Teams]` | `[perfiles]` | `[tareas]` | `[documentos y correo corporativo]` | Sí |
| `[Funciones de IA activas en Microsoft 365: transcripción, respuestas sugeridas…]` | `[perfiles]` | `[tareas]` | `[datos]` | Sí |
| `[Agentes creados con Agent Builder]` | `[perfiles]` | `[tareas]` | `[fuentes conectadas]` | Sí |
| `[Herramientas no autorizadas detectadas]` | `[—]` | `[—]` | `[—]` | **No** |

`[Nota: este inventario procede del diagnóstico previo (sesión de 60-90 min) y se actualiza al menos
una vez al año.]`

---

## 4. Contenido impartido y trazabilidad

**Temario:** cuatro partes y 25 páginas (ver `cumplimiento/05_Temario_FUNDAE.md`).

1. Fundamentos de IA (páginas 3-9): qué es la IA, qué puede y qué no puede hacer, agentes, entornos
   de Copilot, componentes, tipos y ciclo de trabajo.
2. Copilot en tu día a día (páginas 10-14): casos de uso, creación de agentes e inventario de IA.
3. Uso responsable (páginas 15-19): instrucciones, buenas prácticas, riesgos, permisos y
   sobreexposición, política de uso y protocolo de incidentes.
4. Marco legal y obligaciones (páginas 20-22): AI Act, Artículo 4, datos personales, derechos y
   supervisión humana.

**Correspondencia con el contenido mínimo** (pasos a) a d) de la Q&A de la AI Office): ver
`01_Matriz_Trazabilidad_Art4.md`, que se adjunta como **Anexo I**.

---

## 5. Metodología

- Teleformación auto-guiada: páginas con texto, tablas, tres acordeones interactivos, diagramas
  propios y cuatro ejercicios con respuestas comentadas.
- Material entregado: paquete **SCORM 1.2** (y versión HTML5) con 25 páginas y cuestionario final.
- Accesibilidad: textos alternativos en todas las imágenes, contraste WCAG 2.1 AA y navegación por
  teclado.
- Tutoría: `[canal y horario de consultas]`.

---

## 6. Evaluación y resultados

| Elemento | Detalle |
|---|---|
| Instrumento | Cuestionario final de 20 preguntas de opción múltiple (una sola respuesta correcta) |
| Puntuación | 1 punto por pregunta, sobre 100 |
| Criterio de superación | 14 correctas (70 %), configurado en el LMS (`mastery_score`) |
| Registro | `cmi.core.score.raw` y `lesson_status` del paquete SCORM (o el CSV de resultados del LMS) |
| Resultados de esta convocatoria | `[n]` participantes · `[n]` aptos · `[n]` no aptos · media `[x]`/100 |
| Reintentos | Permitidos, con nuevas preguntas del mismo banco temático; si no supera, sesión de refuerzo de 30 min |
| Certificación | Certificado interno de finalización (Anexo III), sin validez oficial: el Artículo 4 no exige certificación homologada |

---

## 7. Política y medidas complementarias

- **Política de uso de IA vigente:** `03_Politica_Uso_IA_Microsoft365.md`, versión `[n]`, fecha
  `[dd/mm/aaaa]`, difundida a `[toda la plantilla]`.
- **Protocolo de incidentes:** definido en la política (parar, no borrar, avisar, corregir, anotar) y
  explicado en la página 19 del curso.
- **Medidas técnicas en curso:** `[revisión de permisos de SharePoint, etiquetas de confidencialidad,
  gestión de enlaces compartidos, controles de publicación de agentes]`.
- **Persona responsable de IA / protección de datos:** `[nombre y contacto]`.

---

## 8. Evidencia custodiada

| Documento | Ubicación | Conservación |
|---|---|---|
| Esta memoria + Anexo I (matriz de trazabilidad) | `[carpeta / repositorio]` | 4 años |
| Anexo II: relación de participantes | `04_Acta_Asistentes_y_Certificado.md` | 4 años |
| Anexo III: certificados emitidos | `[carpeta]` | 4 años |
| Temario | `05_Temario_FUNDAE.md` | 4 años |
| Política de uso de IA | `03_Politica_Uso_IA_Microsoft365.md` | 4 años |
| Paquete SCORM y resultados del LMS | `[carpeta / LMS]` | 4 años |

---

## 9. Revisión y mejora

| Fecha | Qué se revisó | Cambios | Responsable |
|---|---|---|---|
| `[dd/mm/aaaa]` | Contenido del curso, política e inventario | `[—]` | `[—]` |
| `[dd/mm/aaaa]` | `[—]` | `[—]` | `[—]` |

**Compromiso de revisión:** anual, y siempre que cambie una herramienta de IA, una norma aplicable o
el inventario de sistemas.

---

## 10. Declaración

`[La organización]` declara que la acción formativa descrita se ha impartido en las fechas indicadas,
al personal y a las personas relacionadas en el Anexo II, con el contenido y la evaluación
documentados en esta memoria y sus anexos, como medida de apoyo a la alfabetización en IA prevista en
el Artículo 4 del Reglamento (UE) 2024/1689.

En `[lugar]`, a `[fecha]`.

Firma: `[nombre, cargo]`

---

> **Nota de uso.** Este documento acredita **medidas** (obligación de medios), no un nivel de
> alfabetización por persona. No es asesoramiento jurídico: la organización debe contrastar sus
> obligaciones concretas con su asesoría cuando su uso de IA cambie de naturaleza (por ejemplo, si
> pasa a tomar decisiones sobre personas, lo que la sitúa en el ámbito de alto riesgo).
