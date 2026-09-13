#!/usr/bin/env python3
"""Revisión V (13-sep-2026): terminología del curso.

Reglas aplicadas (petición del autor):
  1. Fuera las etiquetas de licencia/facturación del texto didáctico:
     «(con licencia)», «(sin licencia)», «(gratis)», «(de pago)», «Copilot Pro», precios.
  2. Entornos con nombre funcional: «Copilot Web» (o «Modo Web») y «Copilot de Trabajo»
     (Microsoft 365 Copilot).
  3. Jerarquía explícita: Nivel 1 «Copilot Asistente» / chatbot estándar; Nivel 2 «agentes
     especializados» (declarativos); Nivel 3 «agentes avanzados» / de Copilot Studio.
  4. Descripción chatbot vs. agente técnicamente correcta (alcance, herramientas, autonomía).

Idempotente: aborta si algún patrón no aparece exactamente las veces esperadas.
"""
import pathlib
import shutil
import sys

RAIZ = pathlib.Path(__file__).resolve().parent.parent
GUION = RAIZ / "guión_curso_copilot_exelearning.md"
BACKUPS = RAIZ / "legado_articulate" / "backups_guion"
import re

t = GUION.read_text(encoding="utf-8")
original = t
# copia de seguridad (convención del proyecto: legado_articulate/backups_guion/)
BACKUPS.mkdir(parents=True, exist_ok=True)
from datetime import datetime as _dt
_bak = BACKUPS / (GUION.name + ".bak." + _dt.now().strftime("%Y%m%d_%H%M%S"))
if not _bak.exists():
    shutil.copy2(GUION, _bak)
    print("Backup:", _bak.relative_to(RAIZ))

# --------------------------------------------------------------------- 1) campos completos
NEW = {}

NEW[2] = (
    "### ¿Qué vas a encontrar en este curso?<br><br>"
    "**Parte 1 — Fundamentos**<br>"
    "- ¿Qué es un agente de IA en Microsoft 365? (Nodo 3)<br>"
    "- Copilot Web y Copilot de Trabajo: dónde opera cada uno (Nodo 4)<br>"
    "- Los 5 componentes del agente (Nodo 5)<br>"
    "- Los tipos de agente de Microsoft (Nodo 6)<br>"
    "- El ciclo de trabajo del agente (Nodo 7)<br><br>"
    "**Parte 2 — Aplicaciones prácticas**<br>"
    "- Copilot en Word, Outlook y OneNote (Nodo 8)<br>"
    "- Copilot en Excel, PowerPoint y Teams (Nodo 9)<br>"
    "- Copilot en SharePoint, Loop y planificación (Nodo 10)<br>"
    "- Crear tu propio agente con Agent Builder (Nodo 11)<br>"
    "- Cómo escribir buenas instrucciones (Nodo 12)<br>"
    "- Buenas prácticas (Nodo 13)<br>"
    "- Riesgos y límites (Nodo 14)<br><br>"
    "**Parte 3 — Práctica y cierre**<br>"
    "- Ejercicios prácticos: 8 ejercicios (Nodo 15)<br>"
    "- Evaluación final: cuestionario de 10 preguntas (Nodo 16)<br>"
    "- Resumen, glosario y recursos (Nodo 17)<br><br>"
    "### Objetivos del curso<br><br>"
    "Al terminar el curso serás capaz de:<br><br>"
    "1. **Explicar con tus propias palabras** qué es un agente de IA y en qué se diferencia de un "
    "chatbot estándar.<br>"
    "2. **Distinguir los dos entornos de Copilot** —Copilot Web y Copilot de Trabajo— y "
    "**reconocer los tres niveles funcionales** de la IA de Microsoft: Copilot Asistente (chatbot "
    "estándar), agentes especializados o declarativos, y agentes avanzados de Copilot Studio.<br>"
    "3. **Clasificar los tipos de agentes** de Microsoft (Researcher, Analyst, Facilitator, Cowork "
    "y los agentes personalizados que crees tú mismo) y saber cuándo corresponde cada uno.<br>"
    "4. **Reconocer casos de uso reales** de Copilot y sus agentes en Word, Excel, PowerPoint, "
    "Outlook, Teams y SharePoint.<br>"
    "5. **Redactar instrucciones efectivas** para interactuar con Copilot dentro de Microsoft 365.<br>"
    "6. **Aplicar buenas prácticas y detectar riesgos** al usar Copilot: protección de datos, "
    "gobernanza corporativa, verificación de resultados y límites éticos."
)

NEW[3] = (
    "Imagina esto:<br><br>"
    "Le dices a Copilot de Trabajo: *\"Prepara un resumen de las reuniones que tuve esta semana con "
    "el equipo de ventas y envía un correo con los puntos clave a los asistentes.\"*<br><br>"
    "Un chatbot estándar —como Copilot Web— te devolvería un texto que después tendrías que llevar "
    "tú al calendario, a Teams y a Outlook. **Copilot de Trabajo** hace algo más: consulta tu "
    "calendario, lee los resúmenes de las reuniones de Teams, redacta el resumen y envía el correo, "
    "todo dentro del entorno seguro de tu organización.<br><br>"
    "> **Definición clave:** Un agente de IA en Microsoft 365 es un asistente que no se limita a "
    "generar respuestas: PLANIFICA ACCIONES y las EJECUTA con las herramientas conectadas a tu "
    "ecosistema Microsoft.<br><br>"
    "La diferencia entre un chatbot y un agente no está en lo que sabe, sino en lo que puede hacer. "
    "En Microsoft 365 conviven tres niveles:<br>"
    "- **Nivel 1 — Copilot Asistente (chatbot estándar).** Es conversacional y reactivo: espera tu "
    "instrucción, responde y se detiene. Responde preguntas generales, redacta textos o resume el "
    "documento que tú le entregas, pero no actúa por su cuenta ni toca tus sistemas.<br>"
    "- **Nivel 2 — Agentes especializados (o declarativos).** Tienen un rol concreto y una base de "
    "conocimiento acotada: por ejemplo, un agente de Recursos Humanos que responde sobre las "
    "políticas de la empresa a partir de los documentos de SharePoint.<br>"
    "- **Nivel 3 — Agentes avanzados (agentes de Copilot Studio).** Son proactivos: no esperan a "
    "que les preguntes. Ejecutan acciones, se conectan a servicios y API externos y automatizan "
    "flujos completos a partir de disparadores (triggers).<br><br>"
    "Y una idea que conviene retener: un mismo asistente puede comportarse como chatbot o como "
    "agente según el entorno y las herramientas que tenga habilitadas. En una frase, un agente de "
    "IA es un asistente digital que entiende un objetivo, decide qué pasos necesita dar, usa las "
    "herramientas de tu entorno (correo, calendario, documentos, Teams) y te devuelve un resultado "
    "completo."
)

NEW[4] = (
    "Copilot no es una sola cosa: es el mismo asistente disponible en dos entornos distintos y "
    "conviene saber en cuál estás trabajando en cada momento.<br><br>"
    "**Tabla de entornos:**<br><br>"
    "| Entorno | Nombre | ¿Se conecta a los datos de tu organización? | ¿Qué permite? |<br>"
    "|-------|--------|--------|--------|<br>"
    "| **Web** | Copilot Web (o «Modo Web») | **No** — responde con información pública de la web y "
    "con lo que tú le aportas | Buscar en internet, redactar textos generales, resumir los "
    "documentos que tú subes |<br>"
    "| **Trabajo** | Copilot de Trabajo (Microsoft 365 Copilot) | **Sí** — accede a tus correos, "
    "archivos, reuniones y chats a través de Microsoft Graph | Todo lo del entorno web + "
    "integración en Word, Excel, PowerPoint, Outlook, Teams y SharePoint + agentes especializados "
    "y avanzados |<br><br>"
    "**La clave:** el entorno de trabajo es el que conoce tu organización. Solo él puede apoyarse "
    "en los datos internos y, por eso, es también en el que se aplican las políticas de seguridad y "
    "de gobernanza de tu empresa."
)

NEW[5] = (
    "Todo agente de IA en Microsoft 365 tiene cinco partes que trabajan juntas. Piensa en ellas "
    "como las habilidades de un buen asistente. Haz clic en cada componente para descubrirlo.<br><br>"
    "**Sección 1: Percepción — Recibir la información**<br>"
    "Copilot recibe tu instrucción en lenguaje natural y, además, atiende al contexto en el que "
    "trabajas: los correos, los archivos, los participantes de una reunión de Teams o los datos de "
    "una hoja de Excel a los que tiene acceso. Cuanto más rico es ese contexto, mejor entiende lo "
    "que necesitas.<br><br>"
    "**Sección 2: Razonamiento — Pensar y planificar**<br>"
    "Copilot analiza tu objetivo, decide qué pasos necesita dar y en qué orden. Si le pides que "
    "prepare un informe, primero pensará: necesito los datos de Excel, después los organizaré, "
    "luego lo escribiré en Word.<br><br>"
    "**Sección 3: Herramientas — Tener manos para actuar**<br>"
    "Copilot usa las herramientas de Microsoft 365: puede acceder a tu correo (Outlook), consultar "
    "tus archivos (SharePoint, OneDrive), consultar bases de datos (Excel), buscar en internet, "
    "generar gráficos o interactuar con cualquier aplicación conectada. Sin herramientas, un "
    "agente solo puede conversar; con ellas, puede actuar.<br><br>"
    "**Sección 4: Memoria — Mantener el hilo y el conocimiento**<br>"
    "Copilot conserva el hilo de la conversación durante la sesión, de modo que no tienes que "
    "repetirle el contexto en cada mensaje. En los agentes, la memoria se amplía con las fuentes "
    "de conocimiento conectadas: el agente consulta los documentos y los datos de la organización "
    "que le hayas autorizado.<br><br>"
    "**Sección 5: Comunicación — Hablar y entregar resultados**<br>"
    "Copilot te informa de lo que ha hecho, te muestra el resultado y puede preguntar si necesitas "
    "ajustes. Los resultados aparecen directamente en las apps que ya usas: un texto en Word, un "
    "gráfico en Excel, un resumen en Teams."
)

NEW[6] = (
    "Todos los agentes de Microsoft comparten la misma base, pero no todos tienen el mismo alcance. "
    "Conviene saber a qué nivel pertenece cada uno y cuándo corresponde usarlo. Haz clic en cada "
    "tipo para descubrirlo.<br><br>"
    "**Sección 1: Researcher — el investigador profundo (nivel 2)**<br>"
    "Es un agente especializado: tiene un rol muy definido —investigar— y una base de conocimiento "
    "acotada a las fuentes que se le indiquen. Se toma su tiempo: realiza investigaciones complejas "
    "de varios pasos, consulta tus archivos de trabajo y fuentes externas, y te entrega un informe "
    "estructurado con citas y fuentes.<br><br>"
    "*Ejemplo:* *\"Investiga las tendencias del mercado de logística en Europa del Sur y compáralas "
    "con nuestros datos de ventas del último trimestre.\"* Researcher buscará en internet, "
    "consultará tus hojas de Excel y te entregará un informe con gráficos y referencias.<br><br>"
    "**Sección 2: Analyst — el analista de datos (nivel 2)**<br>"
    "Otro agente especializado, en este caso dentro de Copilot de Trabajo: transforma datos "
    "complejos en conclusiones claras y visualizaciones, y se conecta directamente a tus archivos "
    "de Excel.<br><br>"
    "*Ejemplo:* *\"Analiza las ventas del último trimestre en este archivo de Excel y dime qué "
    "productos tienen mayor margen.\"* Analyst lee la hoja, crea gráficos y te explica qué "
    "significan.<br><br>"
    "**Sección 3: Facilitator — el organizador de reuniones (nivel 2)**<br>"
    "Agente especializado en reuniones de Teams: toma notas, obtiene respuestas rápidas durante la "
    "llamada y genera un resumen con acuerdos y tareas asignadas.<br><br>"
    "*Ejemplo:* Durante una reunión de Teams, Facilitator transcribe en directo, detecta los "
    "acuerdos y al final te entrega un resumen con quién debe hacer qué.<br><br>"
    "**Sección 4: Cowork — el ejecutor de tareas complejas (nivel 3)**<br>"
    "Es un agente avanzado: no se limita a responder, ejecuta tareas de varios pasos en segundo "
    "plano. Tú describes el resultado que quieres, Cowork crea un plan, lo ejecuta paso a paso y te "
    "va informando. Puedes interrumpirlo, corregirlo o pausarlo en cualquier momento. (Es el mismo "
    "Cowork que reaparece en el Nodo 7 al explicar el ciclo de trabajo.)<br><br>"
    "*Ejemplo:* *\"Prepara una presentación con los resultados del último trimestre, envía un "
    "correo al equipo directivo con un resumen y agenda una reunión para discutirlos.\"* Cowork "
    "crea la presentación en PowerPoint, redacta el correo en Outlook y crea el evento en tu "
    "calendario, con puntos de aprobación para ti.<br><br>"
    "**Sección 5: Agentes personalizados — los que creas tú (nivel 2)**<br>"
    "Si necesitas un agente para una tarea concreta de tu empresa, puedes crearlo sin saber "
    "programar con Agent Builder. Son agentes especializados: un rol concreto y una base de "
    "conocimiento acotada. Por ejemplo, un agente que responde preguntas frecuentes sobre las "
    "políticas de vacaciones a partir del documento de Recursos Humanos de SharePoint. (Los pasos "
    "para crearlo están en el Nodo 11.)"
)

NEW[16] = (
    "**Título del quiz:** Comprueba lo que has aprendido<br>"
    "**Instrucción:** Selecciona la respuesta correcta para cada pregunta. Necesitas 7 de 10 para "
    "aprobar.<br><br>"
    "**Pregunta 1:** ¿Cuál es la diferencia principal entre Copilot Web y Copilot de Trabajo?<br>"
    "a) Copilot Web es más rápido<br>"
    "b) Copilot de Trabajo se conecta a los datos internos de la organización (correo, archivos, "
    "reuniones) **[CORRECTA]**<br>"
    "c) No hay diferencia, son lo mismo<br>"
    "d) Copilot Web solo funciona en inglés<br><br>"
    "**Pregunta 2:** ¿Cuál NO es un componente de un agente de IA?<br>"
    "a) Percepción<br>b) Memoria<br>c) Programación **[CORRECTA]**<br>d) Comunicación<br><br>"
    "**Pregunta 3:** ¿Qué agente de Microsoft se especializa en análisis de datos y gráficos desde "
    "Excel?<br>"
    "a) Researcher<br>b) Analyst **[CORRECTA]**<br>c) Facilitator<br>d) Cowork<br><br>"
    "**Pregunta 4:** ¿Qué es Cowork en Microsoft Copilot?<br>"
    "a) Un chatbot de preguntas frecuentes<br>"
    "b) Un agente avanzado que ejecuta tareas complejas de varios pasos en segundo plano "
    "**[CORRECTA]**<br>"
    "c) Una herramienta para editar documentos<br>d) Un sistema de correo electrónico<br><br>"
    "**Pregunta 5:** ¿Qué es una \"alucinación\" en el contexto de Copilot?<br>"
    "a) Cuando Copilot se apaga inesperadamente<br>"
    "b) Cuando Copilot genera información que parece correcta pero es falsa **[CORRECTA]**<br>"
    "c) Cuando Copilot se conecta a internet<br>d) Cuando Copilot pide ayuda a otro agente<br><br>"
    "**Pregunta 6:** ¿Cuántos componentes tiene un agente de IA?<br>"
    "a) 3<br>b) 5 **[CORRECTA]**<br>c) 7<br>d) 10<br><br>"
    "**Pregunta 7:** Con Agent Builder creas agentes especializados sin programar. ¿Qué herramienta "
    "necesitas cuando el agente debe ejecutar acciones y conectarse a sistemas externos mediante "
    "disparadores?<br>"
    "a) Agent Builder, igual que para los agentes especializados<br>"
    "b) Copilot Studio **[CORRECTA]**<br>c) PowerPoint<br>d) Excel<br><br>"
    "**Pregunta 8:** ¿Qué deberías hacer SIEMPRE antes de enviar un resultado generado por "
    "Copilot?<br>"
    "a) Nada, Copilot siempre acierta<br>b) Revisar y verificar el resultado **[CORRECTA]**<br>"
    "c) Compartirlo directamente con tu jefe<br>d) Pedirle a Copilot que lo guarde<br><br>"
    "**Pregunta 9:** ¿Qué dato NO deberías compartir con Copilot?<br>"
    "a) Un texto para traducir<br>b) Contraseñas o datos personales confidenciales **[CORRECTA]**<br>"
    "c) Un documento para resumir<br>d) Una lista de tareas<br><br>"
    "**Pregunta 10:** ¿Cuál es la mejor forma de empezar a usar Copilot en el trabajo?<br>"
    "a) Delegando todas las tareas importantes<br>"
    "b) Empezando con tareas pequeñas y verificando los resultados **[CORRECTA]**<br>"
    "c) Esperando a que la tecnología sea perfecta<br>d) Usándolo solo para entretenimiento"
)

NEW[17] = (
    "## Lo que hemos aprendido<br><br>"
    "**En el Módulo 1 (fundamentos) hemos descubierto:**<br><br>"
    "1. Un agente de IA en Microsoft 365 no solo genera respuestas: PLANIFICA y EJECUTA tareas "
    "completas.<br>"
    "2. Copilot funciona en dos entornos: **Copilot Web** (general, sin acceso a los datos de la "
    "organización) y **Copilot de Trabajo** o Microsoft 365 Copilot (conectado a los datos "
    "internos a través de Microsoft Graph).<br>"
    "3. La IA de Microsoft se organiza en tres niveles: **1) Copilot Asistente** o chatbot "
    "estándar, reactivo; **2) agentes especializados** o declarativos, con un rol y una base de "
    "conocimiento acotada; **3) agentes avanzados** o de Copilot Studio, proactivos, capaces de "
    "ejecutar acciones y automatizar flujos.<br>"
    "4. Todo agente tiene 5 componentes: percepción, razonamiento, herramientas, memoria y "
    "comunicación.<br>"
    "5. Microsoft ofrece agentes especializados ya preparados (Researcher, Analyst y Facilitator) "
    "y agentes avanzados (Cowork), además de los que creas tú mismo con Agent Builder.<br>"
    "6. Un agente trabaja en un ciclo de 5 pasos: recibir, planificar, ejecutar, verificar y "
    "entregar.<br><br>"
    "**En los Módulos 2 y 3 (aplicaciones prácticas y buenas prácticas) hemos descubierto:**<br><br>"
    "7. Copilot se integra en Word, Excel, PowerPoint, Outlook, Teams, SharePoint y Loop para "
    "casos de uso reales.<br>"
    "8. La clave para obtener buenos resultados es escribir buenas instrucciones: sé específico, da "
    "contexto, define formato.<br>"
    "9. Siempre verifica los resultados: Copilot puede inventar datos (alucinaciones).<br>"
    "10. Protege la información sensible y consulta con tu equipo de seguridad antes de dar acceso "
    "a agentes.<br>"
    "11. Copilot es una herramienta para potenciar tu trabajo, no para reemplazar tu juicio.<br><br>"
    "**Recuerda:** La tecnología avanza rápido, pero el criterio humano sigue siendo insustituible. "
    "Copilot te hace más eficiente; tú decides cómo usarlo.<br><br>---<br><br>"
    "## Glosario<br><br>"
    "**Agente de IA:** Componente de software que entiende un objetivo, planifica los pasos "
    "necesarios, usa herramientas y ejecuta tareas sobre los sistemas conectados, con el grado de "
    "autonomía que se le haya configurado.<br><br>"
    "**Copilot Web (Modo Web):** Entorno general de Copilot, basado en búsqueda web y sin acceso a "
    "Microsoft Graph. Trabaja solo con lo que tú le aportas y se comporta como asistente "
    "conversacional (nivel 1).<br><br>"
    "**Copilot de Trabajo (Microsoft 365 Copilot):** Entorno corporativo de Copilot, conectado a "
    "los datos internos de la organización (SharePoint, Teams, correo y archivos) a través de "
    "Microsoft Graph. Puede actuar como asistente y como agente.<br><br>"
    "**Copilot Asistente (chatbot estándar):** Nivel 1. Asistente conversacional y reactivo: "
    "espera tu instrucción, responde y se detiene; no ejecuta acciones sobre tus sistemas.<br><br>"
    "**Agentes especializados (declarativos):** Nivel 2. Agentes con un rol concreto y una base de "
    "conocimiento acotada, como un agente de Recursos Humanos que responde a partir de los "
    "documentos de SharePoint. Se crean sin programar con Agent Builder.<br><br>"
    "**Agentes avanzados (Copilot Studio):** Nivel 3. Agentes proactivos: ejecutan acciones, se "
    "conectan a servicios y API externos y automatizan flujos mediante disparadores (triggers).<br><br>"
    "**Agent Builder:** Herramienta incluida en Copilot de Trabajo para crear agentes "
    "especializados sin necesidad de programar.<br><br>"
    "**Copilot Studio:** Plataforma avanzada para crear agentes con acciones, conectores a "
    "sistemas externos y flujos de varios pasos.<br><br>"
    "**Cowork:** Agente avanzado de Copilot que ejecuta tareas complejas de varios pasos en "
    "segundo plano, con puntos de aprobación.<br><br>"
    "**Researcher:** Agente especializado de Microsoft para investigaciones profundas con fuentes "
    "citadas.<br><br>"
    "**Analyst:** Agente especializado de Microsoft para análisis de datos y visualización desde "
    "Excel.<br><br>"
    "**Facilitator:** Agente especializado de Microsoft para la gestión y el resumen de reuniones "
    "de Teams.<br><br>"
    "**Microsoft Graph:** Motor de datos de Microsoft 365 que permite a Copilot acceder a tus "
    "correos, archivos, reuniones y chats de forma segura.<br><br>"
    "**Prompt:** Instrucción que le das a Copilot para que realice una tarea.<br><br>"
    "**Alucinación:** Cuando Copilot genera información que parece correcta pero es falsa.<br><br>"
    "**RAG (Retrieval-Augmented Generation):** Técnica que permite a Copilot buscar información en "
    "tus archivos corporativos para responder con datos actualizados.<br><br>---<br><br>"
    "## ¿Quieres seguir aprendiendo?<br><br>"
    "- [Documentación oficial de Microsoft Copilot](https://learn.microsoft.com/en-us/microsoft-365/copilot/)<br>"
    "- [Guía de Agent Builder](https://learn.microsoft.com/en-us/microsoft-365/copilot/extensibility/agent-builder)<br>"
    "- [Centro de ayuda de Copilot para tu empresa](https://support.microsoft.com/en-us/microsoft-365-copilot)<br>"
    "- El Agent Store de Microsoft para explorar agentes predefinidos<br>"
    "- Cursos en línea sobre inteligencia artificial para no técnicos"
)


def reemplaza_campo(texto, num, nuevo):
    """Sustituye el campo «Contenido en pantalla» del nodo `num`."""
    pat = re.compile(r"(?ms)^### NODO %d —.*?(?=^### NODO |^## 5\.)" % num)
    m = pat.search(texto)
    if not m:
        raise SystemExit("No encuentro el nodo %d" % num)
    seg = m.group(0)
    nuevo_seg, n = re.subn(
        r"(?m)(\|\s*\*\*Contenido en pantalla\*\*\s*\|)(.*?)(\|\s*)$",
        lambda mm: mm.group(1) + nuevo + mm.group(3),
        seg, count=1,
    )
    if n != 1:
        raise SystemExit("Campo «Contenido en pantalla» del nodo %d: %d coincidencias" % (num, n))
    return texto[: m.start()] + nuevo_seg + texto[m.end():]


for num in sorted(NEW):
    t = reemplaza_campo(t, num, NEW[num])

# --------------------------------------------------------------------- 2) sustituciones puntuales
SUST = [
    # nota de revisión al principio del documento
    ("## Documento de producción — eXeLearning\n\n",
     "## Documento de producción — eXeLearning\n\n"
     "> **Revisión del 13-sep-2026 (V) — revisión de terminología:**\n"
     "> 1. Fuera del texto didáctico las etiquetas de licencia y facturación («(con licencia)», "
     "«(sin licencia)», «(gratis)», «(de pago)», «Copilot Pro», precios): el alumno debe entender "
     "**dónde opera** Copilot y **qué puede hacer**, no cómo se factura.\n"
     "> 2. Estandarizados los entornos: **Copilot Web** («Modo Web») para el asistente general sin "
     "acceso a Microsoft Graph, y **Copilot de Trabajo** (Microsoft 365 Copilot) para el asistente "
     "conectado a los datos internos de la organización. El Nodo 4 pasa a llamarse «Copilot Web y "
     "Copilot de Trabajo».\n"
     "> 3. Explicitada la jerarquía funcional en tres niveles (Nodos 3 y 6, resumen y glosario): "
     "**Nivel 1 — Copilot Asistente / chatbot estándar** (reactivo), **Nivel 2 — agentes "
     "especializados o declarativos** (rol y base de conocimiento acotada) y **Nivel 3 — agentes "
     "avanzados / de Copilot Studio** (proactivos: acciones, API externas y disparadores).\n"
     "> 4. Corregida la descripción conceptual chatbot frente a agente (Nodos 3 y 5): la diferencia "
     "no está en «escuchar el entorno» ni en el precio, sino en el alcance, las herramientas y la "
     "autonomía.\n"
     "> 5. Ajustados a los nuevos términos el índice, los objetivos, el cuestionario (preguntas 1, "
     "4 y 7), los ejercicios, el resumen y el glosario.\n\n", 1),
    # sitemap y encabezado del nodo 4
    ("4. **MÓDULO 1 — Niveles de Copilot**",
     "4. **MÓDULO 1 — Copilot Web y Copilot de Trabajo**", 1),
    ("### NODO 4 — NIVELES DE COPILOT", "### NODO 4 — ENTORNOS DE COPILOT: WEB Y TRABAJO", 1),
    ("| Tabla | 1 | Nodo 4 (niveles de Copilot) |", "| Tabla | 1 | Nodo 4 (entornos de Copilot) |", 1),
    ("Fundamentos (qué es un agente y niveles de Copilot)",
     "Fundamentos (qué es un agente y entornos de Copilot)", 1),
    # recursos propios del proyecto: sin la coletilla de licencia
    ("(generado para este curso; sin licencia externa)", "(generado para este curso)", 7),
    # nodo 8: nota de producción
    ("la interfaz puede variar según licencia y canal de actualización",
     "la interfaz puede variar según el entorno y el canal de actualización", 1),
    # nodo 10: Planner
    ("está disponible en los planes de grupo para usuarios con licencia de Microsoft 365 Copilot",
     "está disponible en los planes de grupo para quienes cuentan con Copilot de Trabajo", 1),
    # nodo 11: nota (Agent Builder frente a Copilot Studio)
    ("> **Nota:** Agent Builder es ideal para agentes simples de uso individual o de equipo pequeño. "
     "Si necesitas algo más complejo (flujos de varios pasos, integración con sistemas externos), "
     "se usa Copilot Studio.",
     "> **Nota:** Agent Builder sirve para crear **agentes especializados (nivel 2)**: sencillos, "
     "con un rol y una base de conocimiento acotada, ideales para uso individual o de equipo "
     "pequeño. Cuando necesitas un **agente avanzado (nivel 3)** —flujos de varios pasos, acciones "
     "sobre sistemas externos y disparadores—, la herramienta es Copilot Studio.", 1),
    # nodo 13
    ("en herramientas que no sean Copilot de tu empresa. Copilot de empresa respeta las políticas "
     "de seguridad de tu organización",
     "en herramientas que no sean Copilot de Trabajo. Copilot de Trabajo respeta las políticas de "
     "seguridad de tu organización", 1),
    # nodo 14
    ("Copilot de empresa respeta las mismas políticas de seguridad y protección de datos",
     "Copilot de Trabajo se rige por las mismas políticas de seguridad y protección de datos", 1),
    # nodo 15 (ejercicios, no se monta pero se mantiene coherente)
    ("### Ejercicio 1: Identifica el tipo de IA", "### Ejercicio 1: Identifica el entorno o el agente", 1),
    ("Para cada situación, indica si se trata de Copilot Chat (G) o de Copilot con licencia de "
     "agente (A).",
     "Para cada situación, indica si se trata de Copilot Web (W), que solo trabaja con lo que le "
     "das, o de un agente de Copilot de Trabajo (A), que actúa sobre los datos y las herramientas "
     "de la organización.", 1),
    ("→ Respuesta: G", "→ Respuesta: W", 3),
    ("Le dices a Copilot con licencia que revise tu calendario",
     "Le dices a Copilot de Trabajo que revise tu calendario", 1),
    ("Le pides a Copilot con licencia que lea las reseñas",
     "Le pides a Copilot de Trabajo que lea las reseñas", 1),
    ("Enviar nombres y teléfonos de clientes a Copilot Chat (gratis) para que los organice.",
     "Enviar nombres y teléfonos de clientes a Copilot Web para que los organice.", 1),
    ("y Copilot Chat gratis no está conectado a las políticas de seguridad corporativa.",
     "y Copilot Web no está conectado a las políticas de seguridad de la empresa.", 1),
    ("Pedir a Copilot con licencia que resuma un artículo de noticias interno",
     "Pedir a Copilot de Trabajo que resuma un artículo de noticias interno", 1),
    # §10
    ("quien no tiene licencia no puede replicar nada",
     "quien no tiene Copilot de Trabajo no puede replicar nada", 1),
]

fallos = []
for viejo, nuevo, veces in SUST:
    n = t.count(viejo)
    if n != veces:
        fallos.append((viejo[:70], n, veces))
        continue
    t = t.replace(viejo, nuevo)

if fallos:
    print("FALLOS (patrón, encontradas, esperadas):")
    for f in fallos:
        print("  ", f)
    raise SystemExit(1)

# --------------------------------------------------------------------- 3) anclas del generador
ANCLAS = {
    "nodo 1": ["## Cómo entenderlos", "Un recorrido práctico", "**Duración:**"],
    "nodo 2": ["### Objetivos del curso"],
    "nodo 3": ["> **Definición clave:**"],
    "nodo 4": ["**Tabla de entornos:**"],
    "nodo 5": ["**Sección 1: ", "**Sección 5: "],
    "nodo 6": ["**Sección 1: ", "**Sección 5: "],
    "nodo 7": ["**1. Recibir la orden**"],
    "nodo 11": ["> **Pasos para crear un agente:**", "> **Nota:**"],
    "nodo 12": ["**Sección 1: ", "**Sección 5: "],
    "nodo 13": ["**Conoce las políticas de tu empresa**"],
    "nodo 14": ["mensaje clave"],
    "nodo 16": ["**Pregunta 1:**", "**Pregunta 10:**"],
}
for nodo, anclas in ANCLAS.items():
    for a in anclas:
        if a not in t:
            print(f"ANCLA PERDIDA en {nodo}: {a!r}")
            raise SystemExit(1)

# --------------------------------------------------------------------- 4) residuos
RESIDUOS = ["(con licencia)", "(sin licencia)", "(versión de pago)", "(versión free)",
            "Copilot Chat", "Copilot Pro", "de pago", "sin licencia externa"]
res = {r: t.count(r) for r in RESIDUOS if t.count(r)}
print("Residuos:", res if res else "ninguno")

GUION.write_text(t, encoding="utf-8")
print(f"OK: guion actualizado ({len(original)} -> {len(t)} caracteres)")
