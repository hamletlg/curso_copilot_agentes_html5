#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Aplica las decisiones P1-P9 (opciones recomendadas) al guion del curso Copilot.

Cambios:
  P2 -> nodo nuevo "INDICE Y OBJETIVOS" tras la portada.
  P4 -> nodo nuevo "TIPOS DE AGENTE DE MICROSOFT" tras los 5 componentes.
  P3 -> el nodo de ejercicios pasa de 4 a 8 ejercicios (se recuperan los del maestro).
  Renumeracion de todos los nodos (2..17) + referencias cruzadas, sitemap, iDevices,
  cronograma, checklist e inventario de recursos.
Idempotente por comprobacion: si el nodo nuevo ya existe, aborta sin escribir.
"""
import os
import re
import shutil
import sys
from datetime import datetime

P = "/mnt/DATA/trabajo_hermes/articulate_hermes/guión_curso_copilot_exelearning.md"
t = open(P, encoding="utf-8").read()

if "LOS TIPOS DE AGENTE DE MICROSOFT" in t:
    sys.exit("ABORTA: el guion ya parece tener aplicada la revision III.")

# ---------------------------------------------------------------- mapa de nodos
MAP = {1: 1, 2: 3, 3: 4, 4: 5, 5: 7, 6: 8, 7: 9, 8: 10, 9: 11, 10: 12, 11: 13, 12: 14, 13: 15, 14: 16, 15: 17}


def remap_refs(texto):
    """Renumera las referencias 'Nodo(s) X' del texto segun MAP (una sola pasada)."""
    def _rn(m):
        nums = re.sub(r"\d+", lambda x: str(MAP.get(int(x.group(0)), x.group(0))), m.group(2))
        return m.group(1) + nums
    return re.sub(
        r"(?i)\b(nodos?)((?:\s+\d+(?:\s*[\u2013-]\s*\d+)?)(?:\s*(?:,|y)\s*\d+(?:\s*[\u2013-]\s*\d+)?)*)",
        _rn, texto)


t = remap_refs(t)

# ------------------------------------------------- nodos nuevos (numeracion final)
NODO_2 = '''### NODO 2 — ÍNDICE Y OBJETIVOS

| Campo | Detalle |
|-------|---------|
| **iDevice(s)** | Texto (formato amplio) + iDevice "Lista numerada" (objetivos) |
| **Recurso gráfico** | Ninguno. Nodo de orientación: no lleva imágenes (mismo criterio que el Nodo 4). |
| **Contenido en pantalla** | ### ¿Qué vas a encontrar en este curso?<br><br>**Parte 1 — Fundamentos**<br>- ¿Qué es un agente de IA en Microsoft 365? (Nodo 3)<br>- Copilot Chat (gratis) vs. Copilot con licencia (Nodo 4)<br>- Los 5 componentes del agente (Nodo 5)<br>- Los tipos de agente de Microsoft (Nodo 6)<br>- El ciclo de trabajo del agente (Nodo 7)<br><br>**Parte 2 — Aplicaciones prácticas**<br>- Copilot en Word, Outlook y OneNote (Nodo 8)<br>- Copilot en Excel, PowerPoint y Teams (Nodo 9)<br>- Copilot en SharePoint, Loop y planificación (Nodo 10)<br>- Crear tu propio agente con Agent Builder (Nodo 11)<br>- Cómo escribir buenas instrucciones (Nodo 12)<br>- Buenas prácticas (Nodo 13)<br>- Riesgos y límites (Nodo 14)<br><br>**Parte 3 — Práctica y cierre**<br>- Ejercicios prácticos: 8 ejercicios (Nodo 15)<br>- Evaluación final: cuestionario de 10 preguntas (Nodo 16)<br>- Resumen, glosario y recursos (Nodo 17)<br><br>### Objetivos del curso<br><br>Al terminar el curso serás capaz de:<br><br>1. **Explicar con tus propias palabras** qué es un agente de IA y en qué se diferencia de un chatbot.<br>2. **Identificar los niveles de Copilot** disponibles en Microsoft 365: Copilot Chat (gratis), Copilot Business/Enterprise (de pago) y Copilot Pro (personal).<br>3. **Clasificar los tipos de agentes** de Microsoft (Researcher, Analyst, Facilitator, Cowork y agentes personalizados) y saber cuándo corresponde cada uno.<br>4. **Reconocer casos de uso reales** de Copilot y sus agentes en Word, Excel, PowerPoint, Outlook, Teams y SharePoint.<br>5. **Redactar instrucciones efectivas** para interactuar con Copilot dentro de Microsoft 365.<br>6. **Aplicar buenas prácticas y detectar riesgos** al usar Copilot: protección de datos, gobernanza corporativa, verificación de resultados y límites éticos. |
| **Interacción** | El alumno lee el índice y los objetivos y continúa con la navegación secuencial. Es un nodo de orientación: no tiene actividad. |
| **Notas de producción** | Nodo añadido en la revisión III (decisión P2). Los objetivos son los del documento maestro (`contenido_curso_copilot_agentes.md`, bloque OBJETIVOS DOCENTES) y justifican la evaluación final: cada objetivo tiene al menos una pregunta del cuestionario que lo comprueba. Van en el iDevice «Lista numerada»; el índice, en un «Texto (formato amplio)». Si en el montaje se reordena algún nodo, actualizar esta lista, que es la vista previa del árbol. |

---

'''

NODO_6 = '''### NODO 6 — LOS TIPOS DE AGENTE DE MICROSOFT

| Campo | Detalle |
|-------|---------|
| **iDevice(s)** | Texto (intro) + iDevice "Acordeón" (5 secciones) |
| **Recurso gráfico** | Ninguno. Los cinco tipos se explican dentro del acordeón (mismo criterio que los Nodos 5 y 12: sin imágenes dentro del acordeón). |
| **Contenido en pantalla** | No todos los agentes de Microsoft son iguales. Microsoft ofrece varios tipos y conviene saber cuál corresponde a cada tarea. Haz clic en cada uno para descubrirlo.<br><br>**Sección 1: Researcher — el investigador profundo**<br>Piensa en él como un analista que se toma su tiempo. Researcher realiza investigaciones complejas de varios pasos, consultando tus archivos de trabajo y fuentes externas, y te entrega un informe estructurado con citas y fuentes.<br><br>*Ejemplo:* *"Investiga las tendencias del mercado de logística en Europa del Sur y compáralas con nuestros datos de ventas del último trimestre."* Researcher buscará en internet, consultará tus hojas de Excel y te entregará un informe con gráficos y referencias.<br><br>**Sección 2: Analyst — el analista de datos**<br>Trabaja dentro de Copilot Chat para transformar datos complejos en conclusiones claras y visualizaciones. Se conecta directamente a tus archivos de Excel.<br><br>*Ejemplo:* *"Analiza las ventas del último trimestre en este archivo de Excel y dime qué productos tienen mayor margen."* Analyst lee la hoja, crea gráficos y te explica qué significan.<br><br>**Sección 3: Facilitator — el organizador de reuniones**<br>Te ayuda a gestionar reuniones de Teams: toma notas, obtiene respuestas rápidas durante la llamada y genera un resumen con acuerdos y tareas asignadas.<br><br>*Ejemplo:* Durante una reunión de Teams, Facilitator transcribe en directo, detecta los acuerdos y al final te entrega un resumen con quién debe hacer qué.<br><br>**Sección 4: Cowork — el ejecutor de tareas complejas**<br>Es el más potente: no solo responde, ejecuta tareas de varios pasos en segundo plano. Tú describes el resultado que quieres, Cowork crea un plan, lo ejecuta paso a paso y te va informando. Puedes interrumpirlo, corregirlo o pausarlo en cualquier momento. (Es el mismo Cowork que reaparece en el Nodo 7 al explicar el ciclo de trabajo.)<br><br>*Ejemplo:* *"Prepara una presentación con los resultados del último trimestre, envía un correo al equipo directivo con un resumen y agenda una reunión para discutirlos."* Cowork crea la presentación en PowerPoint, redacta el correo en Outlook y crea el evento en tu calendario, con puntos de aprobación para ti.<br><br>**Sección 5: Agentes personalizados (Agent Builder)**<br>Si necesitas un agente para una tarea concreta de tu empresa, puedes crearlo sin saber programar con Agent Builder. Por ejemplo, un agente que responda preguntas frecuentes sobre las políticas de vacaciones a partir del documento de Recursos Humanos de SharePoint. (Los pasos para crearlo están en el Nodo 11.) |
| **Interacción** | El alumno abre y cierra las cinco secciones del acordeón. |
| **Notas de producción** | Nodo añadido en la revisión III (decisión P4), redactado a partir de la PÁGINA 6 del documento maestro. Motivo: el cuestionario evalúa Analyst (pregunta 3) y Cowork (pregunta 4) y los objetivos docentes incluyen «clasificar los tipos de agente»; sin este nodo, Researcher y Facilitator solo aparecían en el resumen y el glosario. El ejercicio 3 del Nodo 15 evalúa exactamente estos cinco tipos: mantener la correspondencia de nombres (Researcher, Analyst, Facilitator, Cowork, agentes personalizados). |

---

'''

# --------------------------------------------------- ejercicios nuevos (P3)
EJ_3 = '''### Ejercicio 3: Clasifica el tipo de agente de Microsoft<br><br>Para cada caso, indica si es **Researcher (R)**, **Analyst (A)**, **Facilitator (F)**, **Cowork (C)** o un **agente personalizado (P)**.<br><br>1. Copilot busca información en internet y en los archivos de la empresa para entregarte un informe detallado con citas y fuentes sobre el mercado de logística en España. → Respuesta: R<br>2. Copilot analiza una tabla de Excel con las ventas de los últimos 12 meses y te genera un gráfico con los productos de mayor margen. → Respuesta: A<br>3. Durante una reunión de Teams, Copilot toma notas en directo y al final te entrega un resumen con acuerdos y tareas asignadas. → Respuesta: F<br>4. Le dices a Copilot: *"Prepara una presentación con los resultados del trimestre, envía un correo al equipo y agenda una reunión."* Copilot lo hace todo paso a paso. → Respuesta: C<br>5. Creas un agente con Agent Builder que responde preguntas sobre las políticas de vacaciones de la empresa consultando el documento de RRHH en SharePoint. → Respuesta: P<br><br>---<br><br>'''

EJ_678 = '''### Ejercicio 6: Caso práctico completo<br><br>**Contexto:** Trabajas en una empresa de distribución con 200 empleados. Tu jefe te pide que investigues si Copilot puede ayudar a reducir el tiempo que el equipo de administración pierde en tareas repetitivas.<br><br>**Tu misión:**<br><br>1. **Identifica 3 tareas repetitivas** del equipo administrativo que podrían automatizarse con Copilot:<br>a) ____________________________________________<br>b) ____________________________________________<br>c) ____________________________________________<br><br>2. **Para cada tarea, describe brevemente** qué haría Copilot:<br>a) ____________________________________________<br>b) ____________________________________________<br>c) ____________________________________________<br><br>3. **Señala 2 riesgos** que deberías considerar antes de implementar:<br>a) ____________________________________________<br>b) ____________________________________________<br><br>4. **Escribe una instrucción de prueba** (prompt) para una de las tareas, aplicando las reglas vistas:<br>____________________________________________<br>____________________________________________<br><br>---<br><br>### Ejercicio 7: El ciclo del agente en acción<br><br>Situación: tu jefe te ha pedido que uses Copilot para preparar un informe de tendencias del sector. **Completa el ciclo:**<br><br>**Paso 1 — Recibir la orden:** ¿qué le dirías exactamente a Copilot?<br>____________________________________________<br><br>**Paso 2 — Planificar:** ¿qué pasos crees que Copilot seguirá? (al menos 3)<br>1. ______________________________________<br>2. ______________________________________<br>3. ______________________________________<br><br>**Paso 3 — Ejecutar:** ¿qué herramientas podría usar Copilot? (al menos 2)<br>1. ______________________________________<br>2. ______________________________________<br><br>**Paso 4 — Verificar:** ¿qué comprobarías antes de entregar el informe a tu jefe?<br>____________________________________________<br><br>**Paso 5 — Entregar y aprender:** ¿qué feedback le darías a Copilot para mejorar su próximo informe?<br>____________________________________________<br><br>---<br><br>### Ejercicio 8: Análisis de riesgos con Copilot<br><br>Lee cada situación y clasifícala como **ALTO** (no usar sin autorización), **MEDIO** (usar con precaución) o **BAJO** (uso aceptable con revisión). Las respuestas y su justificación están debajo de cada caso.<br><br>**Riesgo 1:** Enviar nombres y teléfonos de clientes a Copilot Chat (gratis) para que los organice.<br>Clasificación: ALTO. Los datos personales de clientes están protegidos por la normativa de protección de datos y Copilot Chat gratis no está conectado a las políticas de seguridad corporativa.<br><br>**Riesgo 2:** Pedir a Copilot con licencia que resuma un artículo de noticias interno para la reunión del equipo.<br>Clasificación: MEDIO. El contenido no es confidencial, pero el resumen podría contener imprecisiones.<br><br>**Riesgo 3:** Usar Copilot para generar una lista de ideas creativas para una campaña de marketing.<br>Clasificación: BAJO. Las ideas no son datos sensibles y siempre pasarán por la revisión del equipo creativo.<br><br>**Riesgo 4:** Conectar un agente personalizado al sistema de nóminas de la empresa para que actualice los datos de los empleados.<br>Clasificación: ALTO. Las nóminas contienen información financiera sensible y solo el personal autorizado con acceso directo debe gestionarla.<br><br>**Riesgo 5:** Pedir a Copilot en Word que redacte un borrador de correo para un cliente externo.<br>Clasificación: MEDIO. El borrador es útil, pero debe revisarse antes de enviarlo para asegurar tono, precisión y datos correctos.'''


def sub1(texto, viejo, nuevo, etiqueta):
    n = texto.count(viejo)
    if n != 1:
        sys.exit(f"ABORTA [{etiqueta}]: {n} coincidencias (se esperaba 1) para {viejo[:70]!r}")
    return texto.replace(viejo, nuevo)


# ------------------------------------------------------------- nodos y ensamblado
corte = t.index("## 5. RESUMEN DE IDEVICES USADOS")
head, tail = t[:corte], t[corte:]
partes = re.split(r"(?m)^(?=### NODO \d+ — )", head)
pre, bloques = partes[0], partes[1:]
if len(bloques) != 15:
    sys.exit(f"ABORTA: se esperaban 15 nodos, hay {len(bloques)}")
titulos = [b.splitlines()[0] for b in bloques]

# --- nodo de ejercicios (antiguo 13 -> nuevo 15): 4 -> 8 ejercicios
i_ej = next(i for i, b in enumerate(bloques) if "EJERCICIOS PRÁCTICOS" in titulos[i])
b = bloques[i_ej]
b = sub1(b, "### NODO 15 — EJERCICIOS PRÁCTICOS\n", "### NODO 15 — EJERCICIOS PRÁCTICOS (8 EJERCICIOS)\n", "titulo ejercicios")
b = sub1(b, "### Ejercicio 3: Mejora las instrucciones", "### Ejercicio 4: Mejora las instrucciones", "renum ej3->4")
b = sub1(b, "### Ejercicio 4: ¿Qué harías tú?", "### Ejercicio 5: ¿Qué harías tú?", "renum ej4->5")
b = sub1(b, "### Ejercicio 4: Mejora las instrucciones", EJ_3 + "### Ejercicio 4: Mejora las instrucciones", "inserta ej3")
b = sub1(b, "una página para una revisión rápida. |", "una página para una revisión rápida.<br><br>" + EJ_678 + " |", "inserta ej6-8")
b = sub1(b, "| **iDevice(s)** | Texto (formato amplio) — los ejercicios se presentan como texto",
         "| **iDevice(s)** | Texto (formato amplio) — los 8 ejercicios se presentan como texto", "idevice ejercicios")
b = sub1(b, "Las respuestas están incluidas para autoevaluación. |",
         "Las respuestas están incluidas para autoevaluación. **Revisión III:** el nodo pasa de 4 a 8 ejercicios (decisión P3); los ejercicios 3, 6, 7 y 8 proceden del documento maestro `contenido_curso_copilot_agentes.md`. |",
         "notas ejercicios")
bloques[i_ej] = b

# --- ensamblado con los dos nodos nuevos
orden = [bloques[0], NODO_2, bloques[1], bloques[2], bloques[3], NODO_6] + bloques[4:]
nuevo = pre + "".join(orden) + tail

# -------------------------------------------------------------- §1 (licencia)
nuevo = sub1(
    nuevo,
    "| **Licencia del curso** | Pendiente de decidir por el autor (ver `pendientes_montaje_exelearning.md`) |",
    "| **Licencia del curso** | **Uso interno (propietaria)** — decisión P5. Crédito de cortesía de la portada en el Nodo 17. Falta solo indicar el **titular** (persona u organización) antes de publicar; ver `pendientes_montaje_exelearning.md`. |",
    "licencia")

# ----------------------------------------------------- nota de revision (II)
nuevo = sub1(nuevo, "Añadida la fila **«Recurso gráfico»** a los 15 nodos",
             "Añadida la fila **«Recurso gráfico»** a todos los nodos", "nota II item 1")
nota3 = """> **Revisión del 12-sep-2026 (III) — cambios de esta versión:**
> 1. Aplicadas las decisiones del autor recogidas en `pendientes_montaje_exelearning.md`: árbol de **17 nodos** (P1, P2 y P4), **8 ejercicios** en el nodo de prácticas (P3), licencia de uso interno (P5), portada mantenida (P8) y material legado apartado en `legado_articulate/` (P7).
> 2. **Nodo 2 nuevo, «Índice y objetivos»** (P2), a partir de la PÁGINA 2 y del bloque OBJETIVOS DOCENTES del documento maestro.
> 3. **Nodo 6 nuevo, «Los tipos de agente de Microsoft»** (P4), a partir de la PÁGINA 6 del maestro: cubre Researcher, Analyst, Facilitator, Cowork y los agentes personalizados, que el cuestionario evalúa en las preguntas 3 y 4.
> 4. **Nodo 15 (ejercicios) ampliado de 4 a 8** (P3): se recuperan los ejercicios del maestro que faltaban (clasificar el tipo de agente, caso práctico completo, el ciclo en acción y análisis de riesgos) y se renumera el resto.
> 5. Renumerados todos los nodos posteriores al 1 (del 2 al 17) y actualizadas las referencias cruzadas, el sitemap (§2), la tabla de iDevices (§5), el cronograma (§7), el checklist (§8) y el inventario de recursos (§9).
> 6. Queda solo lo que no puedo hacer yo: indicar el titular/autoría del curso (P5) y comprobar en el tenant real la ruta del menú del Planner Agent (P6). Ver `pendientes_montaje_exelearning.md`.

"""
nuevo = sub1(nuevo, "> **Revisión del 12-sep-2026 (II) — cambios de esta versión:**",
             nota3 + "> **Revisión del 12-sep-2026 (II) — cambios de esta versión:**", "nota III")


# --------------------------------------------------- reemplazo de secciones §
def seccion(texto, ini, fin, cuerpo, etiqueta):
    i = texto.index(ini)
    j = texto.index(fin, i + 1)
    return texto[:i] + cuerpo + texto[j:]


S2 = '''## 2. ESTRUCTURA DEL CURSO (SITEMAP)

Este es el orden de los **nodos** (páginas) que se crearán en eXeLearning. Cada nodo contiene uno o más **iDevices** con el contenido específico.

1. **PORTADA** — Título, subtítulo, introducción.
2. **ÍNDICE Y OBJETIVOS** — Qué contiene el curso y qué sabrá hacer el alumno al terminarlo.
3. **MÓDULO 1 — ¿Qué es un agente de IA?**
4. **MÓDULO 1 — Niveles de Copilot**
5. **MÓDULO 1 — Los 5 componentes del agente**
6. **MÓDULO 1 — Los tipos de agente de Microsoft**
7. **MÓDULO 1 — El ciclo de trabajo del agente**
8. **MÓDULO 2 — Copilot en Word, Outlook y OneNote**
9. **MÓDULO 2 — Copilot en Excel, PowerPoint y Teams**
10. **MÓDULO 2 — Copilot en SharePoint, Loop y planificación**
11. **MÓDULO 2 — Crear tu propio agente con Agent Builder**
12. **MÓDULO 3 — Cómo escribir buenas instrucciones**
13. **MÓDULO 3 — Buenas prácticas**
14. **MÓDULO 3 — Riesgos y límites**
15. **EJERCICIOS** — 8 ejercicios prácticos con respuestas de autoevaluación
16. **EVALUACIÓN FINAL** — Cuestionario de 10 preguntas (aprobado 7/10)
17. **RESUMEN Y GLOSARIO** — Lo aprendido + glosario + recursos

**Total: 17 nodos.** Los nodos 2 y 6 se añadieron en la revisión III (decisiones P2 y P4); el resto conserva el orden del guion original.

---

'''

S5 = '''## 5. RESUMEN DE IDEVICES USADOS

| iDevice de eXeLearning | Cantidad | Dónde se usa |
|------------------------|----------|--------------|
| Texto (título, subtítulo, introducción de portada) | 3 | Nodo 1 |
| Texto (intro de nodo) | 6 | Nodos 4, 5, 6, 7, 11, 12 |
| Texto (formato amplio / contenido) | 9 | Nodos 2, 3, 8, 9, 10, 13, 14, 15, 17 |
| Tabla | 1 | Nodo 4 (niveles de Copilot) |
| Acordeón | 3 | Nodo 5 (5 componentes), Nodo 6 (tipos de agente), Nodo 12 (5 reglas de prompt) |
| Lista numerada | 3 | Nodo 2 (objetivos), Nodo 7 (ciclo), Nodo 11 (pasos de Agent Builder) |
| Nota (destacado) | 4 | Nodos 3 (definición clave), 11 (Copilot Studio), 13 (políticas de la empresa), 14 (mensaje clave) |
| Cuestionario (Quiz) | 1 | Nodo 16 (evaluación final) |

**Total: 17 nodos, 30 iDevices** (recuento por instancia de iDevice, incluidos los textos de portada e intro de nodo y los iDevices añadidos en los Nodos 2 y 6).

---

'''

S7 = '''## 7. CRONOGRAMA DE PRODUCCIÓN ESTIMADO

> Estimación para montaje manual en la interfaz de eXeLearning (decisión P9a). Si el montaje se hace contra la instancia local por CDP, este cronograma se sustituye por el plan de montaje automatizado.

### DÍA 1 — Montaje en eXeLearning (08:00 - 18:00)

| Hora | Tarea | Nodos |
|------|-------|-------|
| 08:00-09:00 | Configurar proyecto eXeLearning: tema, colores, navegación | Nodo 1 (portada) |
| 09:00-10:00 | Índice y objetivos | Nodo 2 |
| 10:00-11:30 | Fundamentos (qué es un agente y niveles de Copilot) | Nodos 3, 4 |
| 11:30-13:00 | Componentes y tipos de agente | Nodos 5, 6 |
| 13:00-14:00 | Almuerzo | — |
| 14:00-15:30 | Ciclo de trabajo y apps de Office | Nodos 7, 8 |
| 15:30-16:30 | Excel, PowerPoint, Teams y SharePoint | Nodos 9, 10 |
| 16:30-17:30 | Agent Builder e instrucciones | Nodos 11, 12 |
| 17:30-18:00 | Buenas prácticas y riesgos | Nodos 13, 14 |

### DÍA 2 — Evaluación, cierre y exportación (08:00 - 18:00)

| Hora | Tarea | Nodos |
|------|-------|-------|
| 08:00-10:30 | Ejercicios prácticos (8 ejercicios, texto con líneas en blanco) | Nodo 15 |
| 10:30-11:30 | Cuestionario de 10 preguntas con feedback | Nodo 16 |
| 11:30-12:30 | Resumen, glosario y recursos | Nodo 17 |
| 12:30-13:00 | Revisión general: textos, navegación, accesibilidad | — |
| 13:00-14:00 | Almuerzo | — |
| 14:00-15:00 | Imágenes, iconos y textos alternativos (según §9) | Nodos 1, 3, 5, 7, 12, 13, 14, 15 |
| 15:00-16:00 | Exportar: SCORM 1.2 + HTML descargable | — |
| 16:00-18:00 | Verificación en navegador, prueba del cuestionario y ajustes finales | — |

---

'''

S8 = '''## 8. CHECKLIST DE VERIFICACIÓN FINAL

- [ ] Tema personalizado (no tema por defecto)
- [ ] Portada con título, subtítulo y descripción
- [ ] Navegación lateral visible
- [ ] 17 nodos creados en el orden de §2
- [ ] Nodo 2 (índice y objetivos) presente y con los 6 objetivos
- [ ] Nodo 6 (tipos de agente) presente, con los 5 tipos
- [ ] Nodo 15 con los 8 ejercicios y sus respuestas
- [ ] Cuestionario con 10 preguntas y feedback por pregunta
- [ ] Aprobado: 7/10
- [ ] Imágenes con texto alternativo
- [ ] Portada colocada en el Nodo 1 (`portada_curso_copilot.jpg`)
- [ ] Recursos de cada nodo colocados según su fila «Recurso gráfico»
- [ ] Crédito de la portada en el Nodo 17 («Imagen de portada: Jakub Zerdzicki / Pexels»)
- [ ] Sin videos ni audio
- [ ] Sin JavaScript personalizado
- [ ] Exportado a SCORM 1.2 + HTML
- [ ] Funciona en Chrome/Firefox
- [ ] Responsive en móvil
- [ ] Textos sin errores ortográficos

---

'''

nuevo = seccion(nuevo, "## 2. ESTRUCTURA", "## 3. FORMATO", S2, "S2")
nuevo = seccion(nuevo, "## 5. RESUMEN", "## 6. NOTAS", S5, "S5")
nuevo = seccion(nuevo, "## 7. CRONOGRAMA", "## 8. CHECKLIST", S7, "S7")
nuevo = seccion(nuevo, "## 8. CHECKLIST", "## 9. INVENTARIO", S8, "S8")

# §9: actualizar la fila de nodos de los iconos y diagramas (ya remapeada)
nuevo = sub1(nuevo, "`icono_nota`, `icono_flecha` (`.png` 128 px + `.svg`) | Nodos 8, 7, 12, 13, 14, 15 |",
             "`icono_nota`, `icono_flecha` (`.png` 128 px + `.svg`) | Nodos 3, 7, 12, 13, 14, 15 |",
             "§9 iconos") if "| Nodos 8, 7, 12, 13, 14, 15 |" in nuevo else nuevo

# §10: filas nuevas al final de la tabla de decisiones
ancla10 = remap_refs("| **Sin evaluación intermedia** | Solo hay una evaluación final (Nodo 14). Se eliminan los cuestionarios intermedios del contenido original para mantener la simplicidad. |")
filas10 = ancla10 + "\n" + "\n".join([
    "| **Nodo «Índice y objetivos»** | Añadido (decisión P2) con contenido ya redactado en el maestro: mejora la orientación del alumno y hace explícitos los seis objetivos que evalúa el cuestionario. |",
    "| **Nodo «Tipos de agente de Microsoft»** | Añadido (decisión P4) para cubrir la PÁGINA 6 del maestro: el cuestionario evalúa Analyst y Cowork, y hasta ahora Researcher y Facilitator solo aparecían en el glosario, sin haberse explicado. |",
    "| **8 ejercicios en lugar de 4** | Recuperados (decisión P3) los cuatro ejercicios del maestro que faltaban; refuerzan precisamente lo que mide el cuestionario (clasificar tipos de agente y priorizar riesgos). |",
])
nuevo = sub1(nuevo, ancla10, filas10, "§10 nuevas filas")

# ------------------------------------------------------------------- escritura
ts = datetime.now().strftime("%Y%m%d_%H%M%S")
# Los backups viven fuera de la raiz del proyecto (limpieza del 12-sep-2026):
# legado_articulate/backups_guion/
_bdir = os.path.join(os.path.dirname(os.path.abspath(P)), "legado_articulate", "backups_guion")
os.makedirs(_bdir, exist_ok=True)
_bak = os.path.join(_bdir, os.path.basename(P) + f".bak.{ts}")
shutil.copy2(P, _bak)
open(P, "w", encoding="utf-8").write(nuevo)

print("GUION ACTUALIZADO")
print("backup:", _bak)
print("nodos:", len(re.findall(r"(?m)^### NODO ", nuevo)))
print("iDevices declarados:", len(re.findall(r"(?m)^\| \*\*iDevice\(s\)\*\* \|", nuevo)))
print("filas Recurso grafico:", len(re.findall(r"(?m)^\| \*\*Recurso gráfico\*\* \|", nuevo)))
print("ejercicios:", len(re.findall(r"### Ejercicio \d+:", nuevo)))
print("caracteres:", len(nuevo))
print("\nTITULOS DE NODOS:")
for h in re.findall(r"(?m)^### NODO .+$", nuevo):
    print("  ", h)
