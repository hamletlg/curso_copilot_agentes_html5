#!/usr/bin/env python3
"""Revisión V de terminología aplicada al documento maestro (fuente de verdad del contenido).

Mismo criterio que `revision_terminologia.py` (guion): fuera etiquetas de licencia y nombres
antiguos; entornos «Copilot Web» / «Copilot de Trabajo»; tres niveles funcionales.
Edita por número de línea, comprobando antes que la línea esperada es la que se cree.
"""
import pathlib
import re
import shutil
from datetime import datetime

RAIZ = pathlib.Path(__file__).resolve().parent.parent
DOC = RAIZ / "contenido_curso_copilot_agentes.md"
BACKUPS = RAIZ / "legado_articulate" / "backups_guion"

texto = DOC.read_text(encoding="utf-8")
lin = texto.split("\n")
original = list(lin)

BACKUPS.mkdir(parents=True, exist_ok=True)
bak = BACKUPS / (DOC.name + ".bak." + datetime.now().strftime("%Y%m%d_%H%M%S"))
if not bak.exists():
    shutil.copy2(DOC, bak)
    print("Backup:", bak.relative_to(RAIZ))

# (línea 1-based, fragmento que debe contener, texto nuevo — None = borrar la línea)
EDICIONES = [
    (10, "en qué se diferencia de ChatGPT",
     "1. **Explicar con sus propias palabras** qué es un agente de IA y en qué se diferencia de un "
     "chatbot estándar (Copilot Asistente)."),
    (11, "Identificar los niveles de Copilot",
     "2. **Distinguir los dos entornos de Copilot** —Copilot Web y Copilot de Trabajo— y "
     "**reconocer los tres niveles funcionales** de la IA de Microsoft: Copilot Asistente (chatbot "
     "estándar), agentes especializados o declarativos, y agentes avanzados de Copilot Studio."),
    (37, "Copilot Chat (gratis) vs. Copilot con licencia (de pago)",
     "- Página 4: Copilot Web y Copilot de Trabajo: dónde opera cada uno"),
    (60, "Le dices a Copilot en Microsoft 365",
     "Le dices a Copilot de Trabajo: *\"Prepara un resumen de las reuniones que tuve esta semana con "
     "el equipo de ventas y envía un correo con los puntos clave a los asistentes.\"*"),
    (62, "Un chatbot libre (como ChatGPT sin licencia empresarial)",
     "Un chatbot estándar —como Copilot Web— te devolvería un texto. Pero **Copilot de Trabajo** "
     "hace algo más: consulta tu calendario, lee los resúmenes de las reuniones de Teams, redacta "
     "el resumen y envía el correo, todo dentro del entorno seguro de tu organización."),
    (64, "PLANIFICA ACCIONES",
     "**Un agente de IA en Microsoft 365 es un asistente que no solo genera respuestas, sino que "
     "PLANIFICA ACCIONES y las EJECUTA con las herramientas conectadas a tu ecosistema "
     "Microsoft.**"),
    (66, "Piensa en la diferencia así:", None),
    (67, "Copilot Chat (gratis)** es como un **secretario",
     "La diferencia entre un chatbot y un agente no está en lo que sabe, sino en lo que puede "
     "hacer. En Microsoft 365 conviven tres niveles:"),
    (68, "Microsoft 365 Copilot (con licencia)** es como un **asistente",
     "- **Nivel 1 — Copilot Asistente (chatbot estándar).** Conversacional y reactivo: espera tu "
     "instrucción, responde y se detiene; no actúa por su cuenta ni toca tus sistemas."),
    # la línea 69 (en blanco) y la 70 («En una frase: …») se conservan tal cual; los niveles 2 y 3
    # se insertan más abajo, detrás de la línea del nivel 1.
    (145, "Trabaja dentro de Copilot Chat",
     "Trabaja dentro de Copilot de Trabajo para transformar datos complejos en conclusiones claras "
     "y visualizaciones. Se conecta directamente a tus archivos de Excel."),
    (426, "Ejercicio 1: Identifica el tipo de IA",
     "### PÁGINA 15 — Ejercicio 1: Identifica el entorno o el agente"),
    (428, "Diferenciar entre Copilot Chat (gratis)",
     "**Objetivo:** Diferenciar entre Copilot Web (que solo trabaja con lo que le das) y un agente "
     "de Copilot de Trabajo (que actúa sobre los datos y las herramientas de la organización)."),
    (430, "indica si se trata de Copilot Chat (G)",
     "**Instrucción:** Para cada situación, indica si se trata de Copilot Web (W) o de un agente de "
     "Copilot de Trabajo (A)."),
    (433, "Respuesta: G", "   Respuesta: W"),
    (435, "Le dices a Copilot con licencia",
     "2. Le dices a Copilot de Trabajo que revise tu calendario, encuentre un hueco libre y envíe "
     "una invitación de reunión al equipo de marketing."),
    (439, "Respuesta: G", "   Respuesta: W"),
    (441, "Le pides a Copilot con licencia",
     "4. Le pides a Copilot de Trabajo que lea las reseñas de tus clientes en SharePoint, detecte "
     "las quejas más frecuentes y te las resuma en un informe."),
    (445, "Respuesta: G", "   Respuesta: W"),
    (595, "diferencia principal entre Copilot Chat (gratis)",
     "**1. ¿Cuál es la diferencia principal entre Copilot Web y Copilot de Trabajo?**"),
    (596, "a) Copilot Chat es más rápido", "   a) Copilot Web es más rápido"),
    (597, "b) Copilot con licencia accede",
     "   b) Copilot de Trabajo se conecta a los datos internos de la organización (correo, "
     "archivos, reuniones) [CORRECTA]"),
    (599, "d) Copilot Chat solo funciona en inglés", "   d) Copilot Web solo funciona en inglés"),
    (615, "b) Un agente que ejecuta tareas complejas",
     "   b) Un agente avanzado que ejecuta tareas complejas de varios pasos en segundo plano "
     "[CORRECTA]"),
    (637, "crear un agente personalizado sin saber programar",
     "**7. Con Agent Builder creas agentes especializados sin programar. ¿Qué herramienta "
     "necesitas cuando el agente debe ejecutar acciones y conectarse a sistemas externos mediante "
     "disparadores?**"),
    (638, "a) Copilot Studio (solo para expertos)",
     "   a) Agent Builder, igual que para los agentes especializados"),
    (639, "b) Agent Builder [CORRECTA]", "   b) Copilot Studio [CORRECTA]"),
    (708, "Enviar nombres y teléfonos de clientes a Copilot Chat (gratis)",
     "**Riesgo 1:** Enviar nombres y teléfonos de clientes a Copilot Web para que los organice."),
    (710, "Copilot Chat gratis no está conectado",
     "Justificación: Los datos personales de clientes son información protegida por la normativa de "
     "protección de datos. Copilot Web no está conectado a las políticas de seguridad de la "
     "empresa."),
    (712, "Pedir a Copilot con licencia que resuma",
     "**Riesgo 2:** Pedir a Copilot de Trabajo que resuma un artículo de noticias interno para la "
     "reunión del equipo."),
    (737, "Copilot Chat (gratis) es un chatbot",
     "2. Copilot funciona en dos entornos: **Copilot Web** (general, sin acceso a los datos de la "
     "organización) y **Copilot de Trabajo** o Microsoft 365 Copilot (conectado a los datos "
     "internos a través de Microsoft Graph)."),
    (739, "Microsoft ofrece agentes especializados",
     "4. Microsoft organiza sus agentes en tres niveles: Copilot Asistente (nivel 1), agentes "
     "especializados o declarativos (nivel 2: Researcher, Analyst, Facilitator y los que creas con "
     "Agent Builder) y agentes avanzados (nivel 3: Cowork y Copilot Studio)."),
    (760, "**Agente de IA:** Programa que entiende un objetivo",
     "**Agente de IA:** Componente de software que entiende un objetivo, planifica los pasos "
     "necesarios, usa herramientas y ejecuta tareas sobre los sistemas conectados, con el grado de "
     "autonomía que se le haya configurado."),
    (762, "**Copilot Chat:** Versión gratuita",
     "**Copilot Web (Modo Web):** Entorno general de Copilot, basado en búsqueda web y sin acceso a "
     "Microsoft Graph; trabaja solo con lo que le aportas y se comporta como asistente "
     "conversacional (nivel 1)."),
    (764, "**Microsoft 365 Copilot (Business/Enterprise):**",
     "**Copilot de Trabajo (Microsoft 365 Copilot):** Entorno corporativo de Copilot, conectado a "
     "los datos internos de la organización a través de Microsoft Graph. Puede actuar como "
     "asistente y como agente."),
    (766, "**Agent Builder:** Herramienta incluida",
     "**Agent Builder:** Herramienta incluida en Copilot de Trabajo para crear agentes "
     "especializados sin necesidad de programar."),
    (770, "**Cowork:**", "**Cowork:** Agente avanzado de Copilot que ejecuta tareas complejas de "
     "varios pasos en segundo plano, con puntos de aprobación."),
]

fallos = []
for n, frag, nuevo in EDICIONES:
    linea = lin[n - 1]
    if frag not in linea:
        fallos.append((n, frag, linea[:80]))
if fallos:
    print("FALLOS (linea, fragmento esperado, encontrado):")
    for f in fallos:
        print("  ", f)
    raise SystemExit(1)

# de abajo hacia arriba, para que los índices no se muevan
for n, frag, nuevo in sorted(EDICIONES, reverse=True):
    if nuevo is None:
        del lin[n - 1]
    else:
        lin[n - 1] = nuevo

# notas de los niveles 2 y 3, justo detrás de la línea del nivel 1
i_nivel1 = next(i for i, l in enumerate(lin) if l.startswith("- **Nivel 1 — Copilot Asistente"))
lin[i_nivel1 + 1:i_nivel1 + 1] = [
    "- **Nivel 2 — Agentes especializados (o declarativos).** Con un rol concreto y una base de "
    "conocimiento acotada (por ejemplo, un agente de Recursos Humanos que responde sobre las "
    "políticas de la empresa a partir de los documentos de SharePoint).",
    "- **Nivel 3 — Agentes avanzados (agentes de Copilot Studio).** Proactivos: ejecutan acciones, "
    "se conectan a servicios y API externos y automatizan flujos completos a partir de "
    "disparadores (triggers).",
]

# entradas de glosario de los tres niveles, detrás de la de Copilot de Trabajo
i_glos = next(i for i, l in enumerate(lin) if l.startswith("**Copilot de Trabajo (Microsoft 365"))
fin = i_glos
while lin[fin] != "":
    fin += 1
lin[fin:fin] = [
    "",
    "**Copilot Asistente (chatbot estándar):** Nivel 1. Asistente conversacional y reactivo: "
    "espera tu instrucción, responde y se detiene; no ejecuta acciones sobre tus sistemas.",
    "",
    "**Agentes especializados (declarativos):** Nivel 2. Agentes con un rol concreto y una base de "
    "conocimiento acotada. Se crean sin programar con Agent Builder.",
    "",
    "**Agentes avanzados (Copilot Studio):** Nivel 3. Agentes proactivos: ejecutan acciones, se "
    "conectan a servicios y API externos y automatizan flujos mediante disparadores (triggers).",
]

# sección PÁGINA 4 completa: entornos en lugar de niveles de facturación
i_p4 = next(i for i, l in enumerate(lin) if l.startswith("### PÁGINA 4 — Copilot Chat"))
j_p4 = next(i for i, l in enumerate(lin) if l.startswith("### PÁGINA 5 —"))
nuevo_p4 = """### PÁGINA 4 — Copilot Web y Copilot de Trabajo

**Copilot no es una sola cosa: es el mismo asistente en dos entornos distintos.**

**Copilot Web (o «Modo Web»)** — entorno general, basado en búsqueda web y sin acceso a Microsoft Graph:

- Buscar información en internet
- Redactar textos generales
- Resumir documentos que tú subes manualmente

**Lo que NO puede hacer:** no accede automáticamente a tus correos, reuniones de Teams, archivos de SharePoint ni a tu calendario. Solo trabaja con lo que tú le das.

**Copilot de Trabajo (Microsoft 365 Copilot)** — entorno corporativo, conectado a los datos internos de la organización:

- **Copilot integrado en Word, Excel, PowerPoint, Outlook, OneNote y Teams** — no tienes que salir de la app
- **Acceso a Microsoft Graph** — Copilot "ve" tus correos, reuniones, chats de Teams, archivos de SharePoint y documentos con los que tienes permiso
- **Agentes especializados:** Researcher (investigación profunda), Analyst (análisis de datos) y Facilitator (resúmenes de reuniones); y, por función, Sales, Service y Finance (conectados a tu CRM y datos de negocio)
- **Agentes avanzados:** Cowork y los que se crean con Copilot Studio
- **Agent Builder:** puedes crear tus propios agentes especializados con lenguaje natural

**Lo que cambia:** en el entorno de trabajo, Copilot no solo responde — actúa sobre tus datos reales respetando las políticas de seguridad y gobernanza de tu organización.

**La clave:** el entorno de trabajo es el que conoce tu organización; solo él puede apoyarse en los datos internos. Los **niveles funcionales** (asistente, agentes especializados y agentes avanzados) son otra clasificación: describen qué puede hacer cada uno, no dónde se ejecuta.

---

"""
lin[i_p4:j_p4] = nuevo_p4.split("\n")

DOC.write_text("\n".join(lin), encoding="utf-8")

# residuos
RESIDUOS = ["(con licencia)", "(sin licencia)", "Copilot Chat", "Copilot Pro", "de pago", "gratis",
            "gratuita", "Business/Enterprise", "ChatGPT", "Gemini"]
texto_final = "\n".join(lin)
res = {r: texto_final.count(r) for r in RESIDUOS if texto_final.count(r)}
for pat in res:
    for m in re.finditer(re.escape(pat), texto_final):
        print(f"  RESIDUO [{pat}]: ...{texto_final[max(0, m.start()-70):m.end()+70]}...")
print("Residuos:", res if res else "ninguno")
print(f"OK: maestro actualizado ({len(original)} -> {len(lin)} lineas)")
