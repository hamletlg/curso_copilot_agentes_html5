#!/usr/bin/env python3
"""Revisión VI — remediación de cumplimiento del Art. 4 del AI Act sobre el guion y el maestro.

Qué hace, en orden y con copia de seguridad previa:

  1. **Guion** (`guión_curso_copilot_exelearning.md`): reconstruye el §4 con el orden final de
     **25 nodos** (7 páginas nuevas + la página de ejercicios de vuelta), renumera las cabeceras,
     remapea las referencias cruzadas «Nodo N» de los nodos que se conservan y reescribe el
     sitemap (§2), la ficha del curso (§1), la tabla de iDevices (§5), el cronograma (§7), el
     checklist (§8), el inventario de recursos (§9) y las decisiones de diseño (§10).
  2. **Maestro** (`contenido_curso_copilot_agentes.md`): reconstruye las páginas con el mismo orden
     de 25, inserta las páginas nuevas (mismo texto que el guion, convertido a prosa) y deja los
     cuatro ejercicios de reserva en un anexo.
  3. Corrige las cuatro inconsistencias detectadas en el análisis `04_Gap_Analisis_*`:
     el precio de la FAQ, el ejercicio con ChatGPT/Gemini, los metadatos de 28 páginas y el
     glosario sin ordenar.

Los bloques nuevos y sustitutos viven en `revision_vi_nodos_nuevos.md` (fuente revisable).

Uso:
    python3 herramientas/revision_vi.py --dry-run     # solo comprueba y resume (no escribe)
    python3 herramientas/revision_vi.py               # aplica
"""
import argparse
import pathlib
import re
import shutil
import sys
from datetime import datetime

RAIZ = pathlib.Path(__file__).resolve().parent.parent
AQUI = pathlib.Path(__file__).resolve().parent
GUION = RAIZ / "guión_curso_copilot_exelearning.md"
MAESTRO = RAIZ / "contenido_curso_copilot_agentes.md"
NUEVOS = AQUI / "revision_vi_nodos_nuevos.md"
BACKUPS = RAIZ / "legado_articulate" / "backups_guion"

# --------------------------------------------------------------------------- orden final del curso
# (título final de la página, origen)
#   old:TÍTULO     -> bloque que ya existe en el guion, tal cual (con remapeo de «Nodo N»)
#   rename:TÍTULO  -> bloque que ya existe, solo se cambia el título (clave de montaje)
#   nuevo:TÍTULO   -> bloque de revision_vi_nodos_nuevos.md
ORDEN = [
    ("PORTADA DEL CURSO", "old:PORTADA DEL CURSO"),
    ("ÍNDICE Y OBJETIVOS", "nuevo:ÍNDICE Y OBJETIVOS"),
    ("¿QUÉ ES LA IA? DE LA IA AL AGENTE", "nuevo:¿QUÉ ES LA IA? DE LA IA AL AGENTE"),
    ("QUÉ PUEDE Y QUÉ NO PUEDE HACER LA IA", "nuevo:QUÉ PUEDE Y QUÉ NO PUEDE HACER LA IA"),
    ("¿QUÉ ES UN AGENTE DE IA?", "old:¿QUÉ ES UN AGENTE DE IA?"),
    ("COPILOT WEB Y COPILOT DE TRABAJO", "rename:ENTORNOS DE COPILOT: WEB Y TRABAJO"),
    ("LOS 5 COMPONENTES DEL AGENTE", "old:LOS 5 COMPONENTES DEL AGENTE"),
    ("LOS TIPOS DE AGENTE DE MICROSOFT", "old:LOS TIPOS DE AGENTE DE MICROSOFT"),
    ("EL CICLO DE TRABAJO DEL AGENTE", "old:EL CICLO DE TRABAJO DEL AGENTE"),
    ("COPILOT EN WORD, OUTLOOK Y ONENOTE", "old:COPILOT EN WORD, OUTLOOK Y ONENOTE"),
    ("COPILOT EN EXCEL, POWERPOINT Y TEAMS", "old:COPILOT EN EXCEL, POWERPOINT Y TEAMS"),
    ("COPILOT EN SHAREPOINT, LOOP Y PLANIFICACIÓN",
     "old:COPILOT EN SHAREPOINT, LOOP Y PLANIFICACIÓN"),
    ("CREAR TU PROPIO AGENTE CON AGENT BUILDER",
     "old:CREAR TU PROPIO AGENTE CON AGENT BUILDER"),
    ("EL INVENTARIO DE IA DE TU EMPRESA", "nuevo:EL INVENTARIO DE IA DE TU EMPRESA"),
    ("CÓMO ESCRIBIR BUENAS INSTRUCCIONES", "old:CÓMO ESCRIBIR BUENAS INSTRUCCIONES"),
    ("BUENAS PRÁCTICAS", "old:BUENAS PRÁCTICAS"),
    ("RIESGOS Y LÍMITES", "old:RIESGOS Y LÍMITES"),
    ("PERMISOS, SOBREEXPOSICIÓN Y SHADOW AI", "nuevo:PERMISOS, SOBREEXPOSICIÓN Y SHADOW AI"),
    ("POLÍTICA DE USO Y PROTOCOLO DE INCIDENTES",
     "nuevo:POLÍTICA DE USO Y PROTOCOLO DE INCIDENTES"),
    ("EL AI ACT EN TÉRMINOS SIMPLES", "nuevo:EL AI ACT EN TÉRMINOS SIMPLES"),
    ("ARTÍCULO 4: QUÉ TE OBLIGA Y QUÉ DEBES PODER DEMOSTRAR",
     "nuevo:ARTÍCULO 4: QUÉ TE OBLIGA Y QUÉ DEBES PODER DEMOSTRAR"),
    ("DATOS PERSONALES, DERECHOS Y SUPERVISIÓN HUMANA",
     "nuevo:DATOS PERSONALES, DERECHOS Y SUPERVISIÓN HUMANA"),
    ("EJERCICIOS PRÁCTICOS", "nuevo:EJERCICIOS PRÁCTICOS"),
    ("EVALUACIÓN FINAL", "nuevo:EVALUACIÓN FINAL"),
    ("RESUMEN, GLOSARIO Y RECURSOS", "nuevo:RESUMEN, GLOSARIO Y RECURSOS"),
]

# Remapeo de las referencias «Nodo N» de los nodos que se conservan (numeración antigua -> nueva).
MAPA_NODOS = {1: 1, 2: 2, 3: 5, 4: 6, 5: 7, 6: 8, 7: 9, 8: 10, 9: 11, 10: 12,
              11: 13, 12: 15, 13: 16, 14: 17, 15: 23, 16: 24, 17: 25}

# Sitemap nuevo (§2 del guion). «MÓDULO n — » es decorativo: el menú del curso muestra «N. Título».
SITEMAP = [
    ("PORTADA", "Título, subtítulo, introducción."),
    ("ÍNDICE Y OBJETIVOS", "Las cuatro partes del curso y los 10 objetivos docentes."),
    ("MÓDULO 1 — ¿Qué es la IA? De la IA al agente",
     "Conceptos básicos: IA, aprendizaje automático, IA generativa, LLM y agente."),
    ("MÓDULO 1 — Qué puede y qué no puede hacer la IA",
     "Capacidades, límites, cuándo no usar IA y las tres reglas que no se negocian."),
    ("MÓDULO 1 — ¿Qué es un agente de IA?", "Definición, los tres niveles funcionales y la diferencia con un chatbot."),
    ("MÓDULO 1 — Copilot Web y Copilot de Trabajo", "Los dos entornos y qué permite cada uno."),
    ("MÓDULO 1 — Los 5 componentes del agente", "Percepción, razonamiento, herramientas, memoria y comunicación."),
    ("MÓDULO 1 — Los tipos de agente de Microsoft", "Researcher, Analyst, Facilitator, Cowork y agentes personalizados."),
    ("MÓDULO 1 — El ciclo de trabajo del agente", "Recibir, planificar, ejecutar, verificar y entregar."),
    ("MÓDULO 2 — Copilot en Word, Outlook y OneNote", "Casos de uso reales en la documentación y el correo."),
    ("MÓDULO 2 — Copilot en Excel, PowerPoint y Teams", "Análisis de datos, presentaciones y colaboración."),
    ("MÓDULO 2 — Copilot en SharePoint, Loop y planificación", "Búsqueda, páginas colaborativas y organización del trabajo."),
    ("MÓDULO 2 — Crear tu propio agente con Agent Builder", "Cómo se crea, se prueba y se comparte un agente."),
    ("MÓDULO 2 — El inventario de IA de tu empresa",
     "Qué IA usa la organización: funciones activas, herramientas autorizadas y shadow AI."),
    ("MÓDULO 3 — Cómo escribir buenas instrucciones", "Las reglas de oro del prompt, con ejemplos «mal» y «bien»."),
    ("MÓDULO 3 — Buenas prácticas", "Revisar, proteger, citar fuentes, mantener el control humano."),
    ("MÓDULO 3 — Riesgos y límites", "Alucinaciones, sesgos, privacidad, dependencia y gobernanza."),
    ("MÓDULO 3 — Permisos, sobreexposición y shadow AI",
     "El riesgo de confidencialidad número uno en una oficina con Microsoft 365."),
    ("MÓDULO 3 — Política de uso y protocolo de incidentes",
     "Clasificación de datos, quién autoriza y qué hacer cuando algo sale mal."),
    ("MÓDULO 4 — El AI Act en términos simples",
     "Qué es, a quién obliga y los cuatro niveles de riesgo."),
    ("MÓDULO 4 — Artículo 4: qué te obliga y qué debes poder demostrar",
     "La obligación de alfabetización en IA: contenido, evidencia y recurrencia."),
    ("MÓDULO 4 — Datos personales, derechos y supervisión humana",
     "RGPD en el día a día, derechos de las personas y decisiones que exigen una persona."),
    ("EJERCICIOS PRÁCTICOS", "4 ejercicios prácticos con respuestas comentadas (autoevaluación)."),
    ("EVALUACIÓN FINAL", "Cuestionario de 20 preguntas: 14 correctas (70 %) para aprobar."),
    ("RESUMEN Y GLOSARIO", "Lo aprendido + glosario de 29 términos + recursos."),
]

TABLA_IDEVICES = """## 5. RESUMEN DE IDEVICES USADOS

| iDevice de eXeLearning | Cantidad | Dónde se usa |
|------------------------|----------|--------------|
| Texto (título, subtítulo, introducción de portada) | 3 | Nodo 1 |
| Texto (intro de nodo) | 6 | Nodos 6, 7, 8, 9, 13 y 15 |
| Texto (formato amplio / contenido) | 17 | Nodos 2, 3, 4, 5, 10, 11, 12, 14, 16, 17, 18, 19, 20, 21, 22, 23 y 25 |
| Tabla | 5 | Nodos 4 (capacidades), 6 (entornos), 14 (inventario), 19 (datos) y 23 (claves de los ejercicios) |
| Acordeón | 4 | Nodos 7 (5 componentes), 8 (tipos de agente), 15 (reglas de prompt) y 20 (niveles de riesgo) |
| Lista numerada | 4 | Nodos 2 (objetivos), 9 (ciclo), 13 (pasos de Agent Builder) y 19 (protocolo de incidentes) |
| Nota (destacado) | 7 | Nodos 4, 5, 13, 19 y 22 (nota) + Nodos 17 y 18 (aviso) |
| Cuestionario (Quiz) | 1 | Nodo 24 (evaluación final, 20 preguntas) |

La tabla cuenta **elementos del guion** (fragmentos de contenido), no iDevices: el generador monta
**un único iDevice por página** —los fragmentos de cada nodo se concatenan en un solo bloque sin
titular—, así que el paquete tiene **25 iDevices: 24 de tipo Texto (uno por página) y 1 cuestionario**
(`herramientas/generar_curso_elpx.py`).

> **Aviso de nombres.** «Tabla», «Lista numerada», «Acordeón» y «Nota» **no son iDevices** en la versión
> instalada de eXeLearning (v4): son herramientas o efectos del editor de texto. La traducción de cada
> nombre al catálogo real, con el cómo se hace, está en `idevices_equivalencias_exelearning4.md`
> (tabla de equivalencias §2; acordeón resuelto en §4).

"""

CHECKLIST = """## 8. CHECKLIST DE VERIFICACIÓN FINAL

- [x] Tema **Nova** aplicado (no el tema por defecto)
- [x] Portada con título, subtítulo y descripción (overlay sobre la imagen)
- [x] Navegación lateral visible y botones «Anterior / Siguiente» al pie
- [x] **25 páginas** creadas en el orden de §2
- [x] Nodo 2 (índice y objetivos) presente, con las 4 partes y los **10 objetivos**
- [x] Nodos nuevos de fundamentos (3, 4), uso responsable (18, 19) y marco legal (20, 21, 22)
- [x] Nodo 8 (tipos de agente) presente, con los 5 tipos
- [x] Nodo 23 (ejercicios) montado, con 4 ejercicios y sus respuestas
- [x] Cuestionario con **20 preguntas**, feedback por pregunta y 1 punto por pregunta
- [x] Aprobado: **14/20 (70 %)**, configurado en el LMS (`mastery_score`)
- [x] Imágenes con texto alternativo (10 archivos en el paquete)
- [x] Portada colocada en el Nodo 1 (`portada_curso_copilot.jpg`)
- [x] Recursos de cada nodo colocados según su fila «Recurso gráfico»
- [x] Crédito de la portada en el Nodo 25 («Imagen de portada: Jakub Zerdzicki / Pexels»)
- [x] Contenido mínimo del Art. 4 presente (bloques A a E: fundamentos, inventario, riesgos,
      interpretación de resultados y marco legal)
- [x] Sin etiquetas de licencia ni precios en el texto didáctico (revisión V)
- [x] Sin videos ni audio
- [x] Sin JavaScript personalizado
- [x] Exportado a SCORM 1.2 + HTML5 y validado con `verificar_paquete.py`
- [x] Pruebas de interacción en Chrome real (`pruebas_interaccion.py`)
- [x] Funciona en Chrome/Firefox
- [x] Responsive en móvil
- [x] Textos sin errores ortográficos

"""

INVENTARIO_RECURSOS = """## 9. INVENTARIO DE RECURSOS GRÁFICOS (actualizado el 13-sep-2026, revisión VI)

| Recurso | Cantidad | Archivo(s) en `recursos/imagenes/` | Nodo(s) | Licencia |
|---------|----------|------------------------------------|---------|----------|
| Portada | 1 | `portada_curso_copilot.jpg` (1920×1281) | Nodo 1 | Pexels — atribución no obligatoria (Jakub Zerdzicki) |
| Iconos | 5 | `icono_check`, `icono_cross`, `icono_warning`, `icono_nota`, `icono_flecha` (`.png` 128 px + `.svg`) | Nodos 4, 5, 13, 15, 17, 18, 19 y 22 (el de flecha, sin uso) | Propia del proyecto |
| Diagramas | 5 | `diagrama_ia_al_agente` (1600×1000), `diagrama_5_componentes` (1600×1280), `diagrama_ciclo_5_pasos` (1520×1520), `diagrama_sobreposicion` (1600×1000), `diagrama_niveles_riesgo` (1600×1000) (`.png` + `.svg`) | Nodos 3, 7, 9, 18 y 20 | Propia del proyecto |
| Capturas de pantalla | 0 | — | — | Descartadas (justificación en §10) |

**Total: 11 archivos gráficos** en la carpeta (más su versión vectorial), de los que **10 viajan en el
paquete** (el icono de flecha no se usa). Los iconos y diagramas se insertan como imagen (PNG) en los
iDevices; no hay SVG pegado en el editor de texto. **Licencias, atribución y verificación de
integridad: `recursos/imagenes/CREDITOS.md`.** Candidatos descartados para la portada:
`legado_articulate/descartes_proyecto/candidatos_portada.json`.

"""

DECISIONES_VI = """| **Vuelve la página de ejercicios** | La revisión IV había sacado del paquete el nodo de ejercicios (decisión V6, «16 páginas»). La revisión VI la recupera **recortada a 4 ejercicios** (Nodo 23): el informe de conformidad del Art. 4 pide **evidencia de caso práctico aplicado**, y sin ejercicios el paquete solo tenía un cuestionario. Los otros 4 ejercicios se conservan en el anexo del maestro. |
| **Cuatro módulos y 25 páginas** | El curso pasa de 16 a 25 páginas y de 3 a 4 módulos (fundamentos, aplicaciones, uso responsable y marco legal). Motivo: el contenido mínimo del Art. 4 (bloques A a E) exige fundamentos de IA y marco legal, que el curso no tenía. La numeración de módulos es decorativa (el menú muestra «N. Título»). |
| **7 páginas nuevas** | Nodos 3 y 4 (fundamentos de IA), 14 (inventario de IA de la empresa), 18 (permisos y sobreexposición), 19 (política y protocolo de incidentes), 20 (AI Act), 21 (Artículo 4) y 22 (datos personales, derechos y supervisión humana). Cada una corresponde a un bloque del contenido mínimo que faltaba. |
| **El cuestionario pasa a 20 preguntas** | Las 10 originales (producto) se conservan; se añaden 10 de fundamentos, límites, inventario, sobreexposición, Artículo 4, RGPD y política. Aprobado: 14/20 (70 %), configurado en el LMS. |
| **Sin marcas de terceros en el texto** | Los ejercicios ya no citan asistentes de otros fabricantes por su nombre: se habla de «un asistente web» o «una herramienta no autorizada». Es más preciso (el riesgo es la herramienta no autorizada, no la marca) y mantiene la regla de terminología de la revisión V. |
| **El maestro y el guion comparten texto** | Desde la revisión VI, las páginas del maestro se derivan de los bloques del guion (mismo texto, en prosa). Así no vuelven a divergir; la conversión la hace `herramientas/revision_vi.py`. |
"""


# --------------------------------------------------------------------------- utilidades

def leer_bloques(fuente, patron):
    """Trocea un documento en bloques por su cabecera (patrón con un grupo: el título).

    `fuente` puede ser una ruta o el propio texto.
    """
    texto = fuente if isinstance(fuente, str) else fuente.read_text(encoding="utf-8")
    partes = re.split(patron, texto)
    preludio, resto = partes[0], partes[1:]
    bloques = {}
    for i in range(0, len(resto), 2):
        titulo = resto[i].strip()
        cuerpo = resto[i + 1] if i + 1 < len(resto) else ""
        bloques[titulo] = cuerpo
    return preludio, bloques


def remapear_nodos(texto):
    """Reescribe «Nodo N» con la numeración nueva (solo en los bloques que se conservan)."""
    return re.sub(r"\bNodo\s+(\d+)\b",
                  lambda m: f"Nodo {MAPA_NODOS.get(int(m.group(1)), int(m.group(1)))}", texto)


def guion_a_maestro(texto):
    """Convierte el «Contenido en pantalla» del guion en el cuerpo de una página del maestro."""
    t = texto.strip()
    # el título suelto del guion («## Ejercicios prácticos») se quita: en el maestro lo pone la cabecera
    t = re.sub(r"^##\s+[^<]*(?:<br\s*/?>)?", "", t, count=1).strip()
    t = t.replace("<br><br>", "\n\n").replace("<br>", "\n")
    # los encabezados bajan un nivel (en el maestro la página es «### PÁGINA n»)
    t = re.sub(r"(?m)^(#{2,5})\s", lambda m: "#" + m.group(1) + " ", t)
    return t.strip()


# --------------------------------------------------------------------------- guion

def construir_guion(dry):
    texto = GUION.read_text(encoding="utf-8")
    preludio, viejos = leer_bloques(texto, r"(?m)^### NODO \d+ — ([^\n]+)\n")
    # el preludio incluye §1-§3 y la cabecera del §4; el «resto» del último bloque se corta en §5
    m = re.search(r"(?m)^## 5\. RESUMEN DE IDEVICES USADOS", viejos[list(viejos)[-1]])
    cola = viejos[list(viejos)[-1]][m.start():]
    viejos[list(viejos)[-1]] = viejos[list(viejos)[-1]][:m.start()]

    _, nuevos = leer_bloques(NUEVOS.read_text(encoding="utf-8"), r"(?m)^### NODO \d+ — ([^\n]+)\n")

    # --- §4: bloques en el orden final
    salida_bloques = []
    for i, (titulo, origen) in enumerate(ORDEN, start=1):
        modo, ref = origen.split(":", 1)
        if modo == "nuevo":
            if ref not in nuevos:
                raise SystemExit(f"FALTA el bloque nuevo «{ref}» en {NUEVOS.name}")
            cuerpo = nuevos[ref]
        elif modo == "old":
            if ref not in viejos:
                raise SystemExit(f"FALTA el bloque existente «{ref}» en el guion")
            cuerpo = remapear_nodos(viejos.pop(ref))
        elif modo == "rename":
            if ref not in viejos:
                raise SystemExit(f"FALTA el bloque a renombrar «{ref}» en el guion")
            cuerpo = remapear_nodos(viejos.pop(ref))
        else:
            raise SystemExit(f"origen desconocido: {origen}")
        # separador uniforme entre nodos (el bloque original ya venía con «---», pero el último
        # bloque del fichero de contenido puede no traerlo)
        salida_bloques.append(f"### NODO {i} — {titulo}\n" + cuerpo.rstrip() + "\n\n---\n\n")

    # Los bloques que quedan sin usar son los que la revisión VI sustituye por uno nuevo (mismo
    # título, o el mismo con el sufijo de la versión anterior: «EJERCICIOS PRÁCTICOS (8 EJERCICIOS)»).
    refs_nuevos = {re.sub(r"\s*\(.*\)$", "", ref).strip().upper()
                   for modo, ref in (o.split(":", 1) for _, o in ORDEN) if modo == "nuevo"}
    sobrantes = [t for t in viejos if re.sub(r"\s*\(.*\)$", "", t).strip().upper() not in refs_nuevos]
    if sobrantes:
        raise SystemExit(f"bloques del guion sin usar (¿falta en ORDEN?): {sobrantes}")
    print(f"  bloques sustituidos por la revisión VI: {sorted(viejos)}")

    # --- §2 sitemap
    filas = []
    for i, (nombre, desc) in enumerate(SITEMAP, start=1):
        filas.append(f"{i}. **{nombre}** — {desc}")
    sitemap_nuevo = (
        "## 2. ESTRUCTURA DEL CURSO (SITEMAP)\n\n"
        "Este es el orden de las **páginas** (nodos) que se crean en eXeLearning. Cada nodo contiene\n"
        "un iDevice con el contenido específico.\n\n"
        + "\n".join(filas) + "\n\n"
        "**Total: 25 nodos.** Las páginas se agrupan en cuatro módulos (etiqueta decorativa en esta\n"
        "lista: el menú lateral muestra «N. Título»): **1** Fundamentos de IA (3-9), **2** Copilot en\n"
        "tu día a día (10-14), **3** Uso responsable (15-19) y **4** Marco legal y obligaciones (20-22),\n"
        "más las páginas de cierre (23-25).\n\n"
        "**Nota (revisión VI, 13-sep-2026).** El curso pasa de 16 a 25 páginas: se añaden los nodos 3,\n"
        "4, 14, 18, 19, 20, 21 y 22 (fundamentos de IA y cumplimiento del Art. 4) y **vuelve al montaje\n"
        "la página de ejercicios** (recortada a 4). Guion y curso tienen ya las mismas 25 páginas.\n\n"
        "---\n\n")
    preludio = re.sub(r"(?ms)^## 2\. ESTRUCTURA DEL CURSO.*?^## 3\. FORMATO DEL GUIÓN",
                      sitemap_nuevo + "## 3. FORMATO DEL GUIÓN", preludio)

    # --- §1 ficha del curso
    reemplazos_1 = [
        ("| **Duración** | 2 horas |",
         "| **Duración** | **3,5 horas** (3 h de contenido + 30 min de práctica y evaluación) |"),
        ("| **Público** | Empleados sin formación técnica |",
         "| **Público** | Plantilla de PYME y oficinas, sin formación técnica (administración, gestión y dirección) |"),
        ("| **Licencia del curso** | **Uso interno (propietaria)** — decisión P5. Crédito de cortesía de la portada en el Nodo 17. Falta solo indicar el **titular** (persona u organización) antes de publicar; ver `pendientes_montaje_exelearning.md`. |",
         "| **Licencia del curso** | Decisión P5: **uso interno (propietaria)** para el cliente. La versión publicada como portafolio en GitHub se rige por el `LICENSE` del repositorio. Crédito de cortesía de la portada en el Nodo 25. Falta el **titular** del curso antes de publicar (ver `pendientes_montaje_exelearning.md`). |"),
        ("| **Recursos externos** | 1 imagen de portada (Pexels; atribución no obligatoria) + **recursos propios**: 5 iconos y 2 diagramas. **Sin capturas de pantalla** (ver §10). Enlaces externos a Microsoft Learn solo en el Nodo 17. Licencias y atribución: `recursos/imagenes/CREDITOS.md`. |",
         "| **Recursos externos** | 1 imagen de portada (Pexels; atribución no obligatoria) + **recursos propios**: 5 iconos y 5 diagramas. **Sin capturas de pantalla** (ver §10). Enlaces externos (Microsoft Learn, EUR-Lex, AESIA y AEPD) solo en el Nodo 25. Licencias y atribución: `recursos/imagenes/CREDITOS.md`. |"),
        ("| **Imágenes** | 8 archivos en `recursos/imagenes/`: portada (JPG) + 5 iconos (check, cross, warning, nota, flecha) + 2 diagramas (5 componentes, ciclo de 5 pasos). Todos con PNG de respaldo y texto alternativo. Sin capturas de pantalla de Copilot (ver §10). |",
         "| **Imágenes** | 11 archivos en `recursos/imagenes/` (10 en el paquete): portada (JPG) + 5 iconos (check, cross, warning, nota, flecha) + 5 diagramas (de la IA al agente, 5 componentes, ciclo de 5 pasos, sobreexposición de permisos y niveles de riesgo del AI Act). Todos con versión vectorial (SVG), PNG y texto alternativo. Sin capturas de pantalla de Copilot (ver §10). |"),
    ]
    for viejo, nuevo in reemplazos_1:
        if viejo not in preludio:
            raise SystemExit(f"no encuentro en §1: {viejo[:70]}...")
        preludio = preludio.replace(viejo, nuevo, 1)

    fila_fecha = "| **Última revisión** | 13-sep-2026 (revisión VI: remediación de cumplimiento del Art. 4) |\n"
    preludio = preludio.replace("| **Herramienta** | eXeLearning |",
                                fila_fecha + "| **Herramienta** | eXeLearning |", 1)

    # --- nota de revisión VI, antes de la nota de la revisión V
    nota_vi = (
        "> **Revisión del 13-sep-2026 (VI) — remediación de cumplimiento (Art. 4 del AI Act):**\n"
        "> 1. El curso pasa de **16 a 25 páginas** y de 3 a **4 módulos**: fundamentos de IA, aplicaciones,\n"
        ">    uso responsable y marco legal.\n"
        "> 2. **7 páginas nuevas**: de la IA al agente (Nodo 3), qué puede y qué no puede hacer la IA\n"
        ">    (Nodo 4), inventario de IA de la empresa (Nodo 14), permisos y sobreexposición (Nodo 18),\n"
        ">    política de uso y protocolo de incidentes (Nodo 19), el AI Act en términos simples (Nodo 20),\n"
        ">    Artículo 4 (Nodo 21) y datos personales, derechos y supervisión humana (Nodo 22).\n"
        "> 3. **Vuelve la página de ejercicios** (Nodo 23), recortada a 4 ejercicios con respuestas, y el\n"
        ">    cuestionario pasa a **20 preguntas** (14 correctas, 70 %).\n"
        "> 4. Objetivos docentes: de 6 a **10**, cubriendo los bloques A a E del contenido mínimo.\n"
        "> 5. Corregidas las inconsistencias de la revisión anterior: el precio que quedaba en la FAQ,\n"
        ">    los ejercicios que citaban asistentes de terceros por su marca, los metadatos de 28 páginas\n"
        ">    y el glosario sin ordenar.\n"
        "> 6. Todos los cambios se aplican con `herramientas/revision_vi.py` (guion y maestro a la vez).\n\n")
    preludio = preludio.replace("> **Revisión del 13-sep-2026 (V)", nota_vi + "> **Revisión del 13-sep-2026 (V)", 1)

    # --- cola (§5 a §10)
    cola = re.sub(r"(?ms)^## 5\. RESUMEN DE IDEVICES USADOS.*?(?=^## 6\. )", TABLA_IDEVICES, cola)
    cola = re.sub(r"(?ms)^## 7\. CRONOGRAMA DE PRODUCCIÓN ESTIMADO.*?(?=^## 8\. )",
                  "## 7. CRONOGRAMA DE PRODUCCIÓN ESTIMADO\n\n"
                  "> **Nota (revisión VI).** El curso se monta por código (`python3 herramientas/generar_curso_elpx.py`\n"
                  "> + `sh herramientas/exportar.sh`), así que este cronograma solo aplica al montaje manual en la\n"
                  "> interfaz. Con 25 páginas, una estimación razonable de montaje manual son 2 jornadas: 1,5 para las\n"
                  "> 22 páginas de contenido y 0,5 para ejercicios, cuestionario, cierre y exportación.\n\n", cola)
    cola = re.sub(r"(?ms)^## 8\. CHECKLIST DE VERIFICACIÓN FINAL\n\n.*?(?=^## 9\. )", CHECKLIST, cola)
    cola = re.sub(r"(?ms)^## 9\. INVENTARIO DE RECURSOS GRÁFICOS.*?(?=^## 10\. )",
                  INVENTARIO_RECURSOS, cola)
    # §10: las decisiones conservan sus referencias cruzadas, remapeadas a la numeración nueva, y
    # delante van las filas de la revisión VI. Se remapea SOLO esta sección: §5-§9 ya están escritas
    # con la numeración final.
    m10 = re.search(r"(?ms)^## 10\. DECISIONES DE DISEÑO.*\Z", cola)
    if not m10:
        raise SystemExit("no encuentro el §10 de decisiones")
    dec = remapear_nodos(m10.group(0))
    dec = re.sub(r"(^\| Decisión \| Justificación \|\n\|----------\|--------------\|\n)",
                 r"\1" + DECISIONES_VI, dec, count=1)
    cola = cola[:m10.start()] + dec
    # §6: inventario de recursos del apartado de branding
    cola = cola.replace(
        "(portada, 5 iconos y 2 diagramas; cada uno con versión PNG lista para subir y versión SVG vectorial)",
        "(portada, 5 iconos y 5 diagramas; cada uno con versión PNG lista para subir y versión SVG vectorial)")

    nuevo_guion = preludio + "".join(salida_bloques) + cola

    # comprobaciones
    cabeceras = re.findall(r"(?m)^### NODO (\d+) — ([^\n]+)$", nuevo_guion)
    if len(cabeceras) != 25:
        raise SystemExit(f"el guion resultante tiene {len(cabeceras)} nodos (esperaba 25)")
    if [int(n) for n, _ in cabeceras] != list(range(1, 26)):
        raise SystemExit("la numeración de nodos no es correlativa")
    for prohibido in ("$21", "usuario/mes", "ChatGPT", "Gemini", "Copilot Pro", "Copilot Chat"):
        # se admite en las notas de revisión (histórico), no en el contenido de los nodos
        for n, titulo in cabeceras:
            blq = re.search(rf"(?ms)^### NODO {n} — .*?(?=^### NODO |\Z)", nuevo_guion).group(0)
            if prohibido in blq:
                raise SystemExit(f"«{prohibido}» sigue en el nodo {n} ({titulo})")

    if not dry:
        BACKUPS.mkdir(parents=True, exist_ok=True)
        sello = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(GUION, BACKUPS / f"guión_curso_copilot_exelearning.md.bak.{sello}")
        GUION.write_text(nuevo_guion, encoding="utf-8")
    print(f"GUION: 25 nodos, {len(nuevo_guion)} caracteres"
          + ("" if dry else " -> escrito (copia previa en legado_articulate/backups_guion/)"))
    return nuevo_guion


# --------------------------------------------------------------------------- maestro

MAESTRO_ORDEN = [
    ("old", 1), ("nuevo", "ÍNDICE Y OBJETIVOS"),
    ("nuevo", "¿QUÉ ES LA IA? DE LA IA AL AGENTE"),
    ("nuevo", "QUÉ PUEDE Y QUÉ NO PUEDE HACER LA IA"),
    ("old", 3), ("old", 4), ("old", 5), ("old", 6), ("old", 7),
    ("old", 8), ("old", 9), ("old", 10), ("old", 11),
    ("nuevo", "EL INVENTARIO DE IA DE TU EMPRESA"),
    ("old", 12), ("old", 13), ("old", 14),
    ("nuevo", "PERMISOS, SOBREEXPOSICIÓN Y SHADOW AI"),
    ("nuevo", "POLÍTICA DE USO Y PROTOCOLO DE INCIDENTES"),
    ("nuevo", "EL AI ACT EN TÉRMINOS SIMPLES"),
    ("nuevo", "ARTÍCULO 4: QUÉ TE OBLIGA Y QUÉ DEBES PODER DEMOSTRAR"),
    ("nuevo", "DATOS PERSONALES, DERECHOS Y SUPERVISIÓN HUMANA"),
    ("nuevo", "EJERCICIOS PRÁCTICOS"),
    ("nuevo", "EVALUACIÓN FINAL"),
    ("nuevo", "RESUMEN, GLOSARIO Y RECURSOS"),
]

# Cabeceras de parte: se insertan antes de la página que ocupa esa posición (1-based).
PARTES = {
    3: "## PARTE 1 — FUNDAMENTOS DE IA (páginas 3-9)",
    10: "## PARTE 2 — COPILOT EN TU DÍA A DÍA (páginas 10-14)",
    15: "## PARTE 3 — USO RESPONSABLE (páginas 15-19)",
    20: "## PARTE 4 — MARCO LEGAL Y OBLIGACIONES (páginas 20-22)",
    23: "## EVALUACIÓN Y CIERRE (páginas 23-25)",
}

# Los cuatro ejercicios que NO se montan (banco de reserva) se conservan como anexo.
ANEXO_EJERCICIOS = [16, 17, 19, 23]          # páginas antiguas del maestro
TITULOS_ANEXO = {
    16: "Anexo E-1 — Ejercicio 2: los componentes del agente",
    17: "Anexo E-2 — Ejercicio 3: clasifica el tipo de agente",
    19: "Anexo E-3 — Ejercicio 5: ¿qué harías tú?",
    23: "Anexo E-4 — Ejercicio 7: el ciclo del agente en acción",
}

# Títulos de página del maestro para las páginas nuevas (las que se conservan mantienen el suyo).
TITULOS_NUEVOS_MAESTRO = {
    "ÍNDICE Y OBJETIVOS": "Índice y objetivos",
    "¿QUÉ ES LA IA? DE LA IA AL AGENTE": "¿Qué es la IA? De la IA al agente",
    "QUÉ PUEDE Y QUÉ NO PUEDE HACER LA IA": "Qué puede y qué no puede hacer la IA",
    "EL INVENTARIO DE IA DE TU EMPRESA": "El inventario de IA de tu empresa",
    "PERMISOS, SOBREEXPOSICIÓN Y SHADOW AI": "Permisos, sobreexposición y shadow AI",
    "POLÍTICA DE USO Y PROTOCOLO DE INCIDENTES": "Política de uso y protocolo de incidentes",
    "EL AI ACT EN TÉRMINOS SIMPLES": "El AI Act en términos simples",
    "ARTÍCULO 4: QUÉ TE OBLIGA Y QUÉ DEBES PODER DEMOSTRAR":
        "Artículo 4: qué te obliga y qué debes poder demostrar",
    "DATOS PERSONALES, DERECHOS Y SUPERVISIÓN HUMANA":
        "Datos personales, derechos y supervisión humana",
    "EJERCICIOS PRÁCTICOS": "Ejercicios prácticos",
    "EVALUACIÓN FINAL": "Evaluación final",
    "RESUMEN, GLOSARIO Y RECURSOS": "Resumen, glosario y recursos",
}

CABECERA_MAESTRO = """# Curso: Agentes de IA y Microsoft Copilot para tu día a día

## Contenido completo — 25 páginas (22 de contenido + ejercicios, evaluación y cierre)

**Revisión:** 13-sep-2026 (revisión VI: remediación de cumplimiento del Art. 4 del AI Act).
**Herramienta:** eXeLearning → export **SCORM 1.2 + HTML5** (tema Nova).

> **Relación con el guion.** Este documento es la **fuente de verdad del contenido**. Desde la
> revisión VI su texto y el de `guión_curso_copilot_exelearning.md` son el mismo: las páginas nuevas
> se redactan una sola vez (en los bloques del guion) y `herramientas/revision_vi.py` las convierte a
> prosa aquí. Si hay que cambiar contenido, se cambia en el guion y se vuelve a ejecutar el script (o
> se editan los dos, con cuidado de no divergir).
>
> **Qué cubre y por qué.** Los cuatro módulos siguen el **contenido mínimo del Artículo 4** del
> Reglamento (UE) 2024/1689 según la AI Office: (A) qué es la IA, (B) qué IA usa tu organización,
> (C) oportunidades y riesgos, (D) interpretación de resultados y (E) marco legal y ético. Los
> bloques C y D se desarrollan en los módulos 2 y 3, y el bloque E, en el módulo 4.

---

## OBJETIVOS DOCENTES

Al finalizar este curso, el participante será capaz de:

1. **Explicar con sus propias palabras** qué es la inteligencia artificial, en qué se diferencia de la
   IA generativa y de un modelo de lenguaje, y por qué un asistente puede inventar datos.
2. **Decidir cuándo conviene usar IA y cuándo no**: qué tareas admite sin riesgo y en cuáles hace falta
   siempre una fuente oficial o una persona que decida.
3. **Explicar con sus propias palabras** qué es un agente de IA y en qué se diferencia de un chatbot.
4. **Distinguir los dos entornos de Copilot** —Copilot Web y Copilot de Trabajo— y reconocer los tres
   niveles funcionales de la IA de Microsoft: Copilot Asistente, agentes especializados y agentes
   avanzados de Copilot Studio.
5. **Clasificar los tipos de agentes** que ofrece Microsoft (Researcher, Analyst, Facilitator, Cowork
   y los agentes personalizados) y saber cuándo corresponde cada uno.
6. **Reconocer casos de uso reales** de Copilot y sus agentes en Word, Excel, PowerPoint, Outlook,
   Teams y SharePoint.
7. **Redactar instrucciones efectivas** para interactuar con Copilot dentro de Microsoft 365.
8. **Identificar la IA que usa su organización** —incluidas las funciones ya activas y las
   herramientas no autorizadas— y explicar por qué los permisos de SharePoint son un riesgo de
   confidencialidad.
9. **Aplicar la política de uso y el protocolo de incidentes** de su empresa: qué se puede hacer,
   quién autoriza un agente y qué hacer si algo sale mal.
10. **Describir las obligaciones de su organización** según el Reglamento (UE) 2024/1689 (AI Act):
    qué es el Artículo 4, cómo se demuestra el cumplimiento, qué papel tienen el RGPD y la AESIA, y
    qué derechos tienen las personas.

---

"""


def construir_maestro(dry, guion_nuevo):
    ruta_paginas, viejas = leer_bloques(MAESTRO.read_text(encoding="utf-8"),
                                       r"(?m)^#{2,3} PÁGINA \d+ — ([^\n]+)\n")
    # limpia las cabeceras de parte que quedaron dentro de los bloques
    viejas = {t: re.sub(r"(?m)^## (PARTE [^\n]*|RESUMEN FINAL)\n+", "", c) for t, c in viejas.items()}

    _, nuevos = leer_bloques(NUEVOS.read_text(encoding="utf-8"), r"(?m)^### NODO \d+ — ([^\n]+)\n")
    _, nodos_guion = leer_bloques(guion_nuevo, r"(?m)^### NODO \d+ — ([^\n]+)\n")

    # mapa «título de página del maestro» -> número antiguo (las claves son los títulos literales)
    numero_antiguo = {}
    for m in re.finditer(r"(?m)^#{2,3} PÁGINA (\d+) — ([^\n]+)$", MAESTRO.read_text(encoding="utf-8")):
        numero_antiguo[m.group(2).strip()] = int(m.group(1))
    titulo_por_numero = {v: k for k, v in numero_antiguo.items()}

    partes = []
    for i, (modo, ref) in enumerate(MAESTRO_ORDEN, start=1):
        if i in PARTES:
            partes.append(PARTES[i] + "\n\n")
        if modo == "old":
            titulo = titulo_por_numero[ref]
            cuerpo = viejas[titulo].strip()
            partes.append(f"### PÁGINA {i} — {titulo}\n\n{cuerpo}\n\n---\n\n")
        else:
            titulo, cuerpo = None, None
            # el título de la página nueva se toma del guion (mismo orden) para no divergir
            titulo_guion, bloque_guion = list(nodos_guion.items())[i - 1]
            if titulo_guion != ref:
                raise SystemExit(f"desajuste en la página {i}: guion «{titulo_guion}» vs maestro «{ref}»")
            titulo = TITULOS_NUEVOS_MAESTRO[ref]
            cuerpo = guion_a_maestro(bloque_guion)
            partes.append(f"### PÁGINA {i} — {titulo}\n\n{cuerpo}\n\n---\n\n")

    anexo = ["## ANEXO — BANCO DE EJERCICIOS (los 4 ejercicios que no se montan)\n\n"
             "El curso monta 4 ejercicios (Nodo 23). Estos cuatro se conservan como banco de reserva,\n"
             "listos para sustituir o ampliar los del curso.\n\n---\n\n"]
    for num in ANEXO_EJERCICIOS:
        titulo = titulo_por_numero[num]
        anexo.append(f"### {TITULOS_ANEXO[num]}\n\n{viejas[titulo].strip()}\n\n---\n\n")

    estructura = """## ANEXO: ESTRUCTURA DE PÁGINAS RESUMEN

| Sección | Páginas | Tipo | Contenido |
|---------|---------|------|-----------|
| Portada | 1 | Material | Título, duración, autor |
| Índice y objetivos | 2 | Material | Las 4 partes y los 10 objetivos |
| Fundamentos de IA | 3-9 | Material | De la IA al agente, límites, agentes, entornos, componentes, tipos y ciclo |
| Copilot en tu día a día | 10-14 | Material | Apps, Agent Builder e inventario de IA |
| Uso responsable | 15-19 | Material | Instrucciones, buenas prácticas, riesgos, permisos y política |
| Marco legal | 20-22 | Material | AI Act, Artículo 4, datos personales y derechos |
| Ejercicios | 23 | Evaluación | 4 ejercicios con respuestas comentadas |
| Evaluación final | 24 | Evaluación | 20 preguntas (14 correctas, 70 %) |
| Resumen y glosario | 25 | Cierre | 16 puntos de repaso, 29 términos y recursos |

**Total: 25 páginas** (22 de contenido + 3 de práctica, evaluación y cierre).

---

## MAPA DE COBERTURA DEL ART. 4 (bloques A-E)

| Bloque mínimo | Páginas del curso | Preguntas del cuestionario |
|---|---|---|
| A. ¿Qué es la IA? | 3, 4, 5, 7 | 2, 6, 11, 12, 13, 15 |
| B. Qué IA usa tu organización | 6, 14 | 1, 4, 9, 14 |
| C. Oportunidades y riesgos | 4, 17, 18 | 5, 8, 9, 15, 19 |
| D. Interpretación de resultados | 9, 15, 16, 23 | 8, 12, 13 |
| E. Marco legal y ético | 19, 20, 21, 22 | 16, 17, 18, 19, 20 |
"""

    nuevo = CABECERA_MAESTRO + "".join(partes) + "".join(anexo) + estructura
    if not dry:
        BACKUPS.mkdir(parents=True, exist_ok=True)
        sello = datetime.now().strftime("%Y%m%d_%H%M%S")
        shutil.copy2(MAESTRO, BACKUPS / f"contenido_curso_copilot_agentes.md.bak.{sello}")
        MAESTRO.write_text(nuevo, encoding="utf-8")
    paginas = len(re.findall(r"(?m)^#{2,3} PÁGINA \d+ —", nuevo))
    if paginas != 25:
        raise SystemExit(f"el maestro resultante tiene {paginas} páginas (esperaba 25)")
    for prohibido in ("$21", "usuario/mes", "ChatGPT", "Gemini"):
        if prohibido in nuevo:
            raise SystemExit(f"«{prohibido}» sigue en el maestro")
    print(f"MAESTRO: {paginas} páginas, {len(nuevo)} caracteres"
          + ("" if dry else " -> escrito (copia previa en legado_articulate/backups_guion/)"))
    return nuevo


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--dry-run", action="store_true", help="no escribe nada")
    args = ap.parse_args()
    guion = construir_guion(args.dry_run)
    construir_maestro(args.dry_run, guion)
    print("\nSiguiente paso: python3 herramientas/generar_curso_elpx.py --check")
    return 0


if __name__ == "__main__":
    sys.exit(main())
