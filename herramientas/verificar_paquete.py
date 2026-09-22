#!/usr/bin/env python3
"""Verifica el paquete generado y sus exportaciones (.elpx, SCORM 1.2 y HTML5).

Uso:
    python3 herramientas/verificar_paquete.py

Comprueba, sin abrir el navegador:
  - el .elpx: nodos, bloques, componentes, imágenes y tipos de iDevice de content.xml
  - las decisiones de las revisiones IV, V y VI: un solo bloque por página, bloques sin nombre,
    menú lateral «N. Título», tema Nova, 25 páginas (la de EJERCICIOS vuelve al curso) y
    terminología sin etiquetas de licencia ni precios
  - el bloque de cumplimiento (revisión VI): los conceptos legales que el Art. 4 exige están
    presentes en el curso y en el cuestionario
  - el cuestionario: descifra su estado (XOR 146) y valida nota de corte, SCORM y las 20 preguntas
  - la revisión VII: los recuadros de ideas clave (8 páginas) y las actividades interactivas de la
    página de ejercicios (2 test de práctica + 2 respuestas abiertas con su respuesta modelo)
  - el SCORM 1.2: manifiesto (schemaversion, adlcp), páginas, recursos e interacciones
  - el HTML5: páginas, recursos e interacciones
"""
import json
import pathlib
import re
import sys
import urllib.parse
import zipfile

RAIZ = pathlib.Path(__file__).resolve().parent.parent
ENT = RAIZ / "entregables"
ELPX = ENT / "curso_copilot_agentes.elpx"
SCORM = ENT / "curso_copilot_agentes_scorm12.zip"
HTML5 = ENT / "curso_copilot_agentes_html5.zip"
XOR_KEY = 146

# 25 páginas: guion y curso coinciden (revisión VI). 24 de contenido + el cuestionario.
# Revisión VII: la página de EJERCICIOS deja de ser un iDevice Texto único y monta sus actividades
# con iDevices nativos (2 test de práctica + 2 respuestas abiertas), así que esa página lleva
# 5 bloques y el total sube a 29 bloques y 29 componentes (26 Texto + 3 Cuestionario).
N_PAGINAS = 25
N_BLOQUES = 29
N_COMPONENTES = 29
N_TEXTOS = 26
N_QUIZ = 3
N_BLOQUES_EJERCICIOS = 5
N_PAGINA_EJERCICIOS = 23
N_RECUADROS = 8
N_TEST_PRACTICA = 2
N_RESPUESTAS_ABIERTAS = 2
N_IMAGENES = 10
N_ACORDEONES = 4
N_PREGUNTAS = 20
TITULOS_MENU = [
    "1. PORTADA", "2. ÍNDICE Y OBJETIVOS", "3. ¿Qué es la IA? De la IA al agente",
    "4. Qué puede y qué no puede hacer la IA", "5. ¿Qué es un agente de IA?",
    "6. Copilot Web y Copilot de Trabajo",
    "7. Los 5 componentes del agente", "8. Los tipos de agente de Microsoft",
    "9. El ciclo de trabajo del agente", "10. Copilot en Word, Outlook y OneNote",
    "11. Copilot en Excel, PowerPoint y Teams", "12. Copilot en SharePoint, Loop y planificación",
    "13. Crear tu propio agente con Agent Builder", "14. El inventario de IA de tu empresa",
    "15. Cómo escribir buenas instrucciones", "16. Buenas prácticas", "17. Riesgos y límites",
    "18. Permisos, sobreexposición y shadow AI", "19. Política de uso y protocolo de incidentes",
    "20. El AI Act en términos simples",
    "21. Artículo 4: qué te obliga y qué debes poder demostrar",
    "22. Datos personales, derechos y supervisión humana", "23. EJERCICIOS PRÁCTICOS",
    "24. EVALUACIÓN FINAL", "25. RESUMEN Y GLOSARIO",
]

# Contenido mínimo del Art. 4 (bloques A-E del informe): tiene que estar EN el curso, no solo en la
# documentación. Si desaparece de una página, esta comprobación lo caza.
LEGAL = [
    "Reglamento (UE) 2024/1689", "AI Act", "Artículo 4", "responsable del despliegue",
    "RGPD", "datos personales", "supervisión humana", "AESIA", "sobreexposición",
    "shadow AI", "sesgo", "alucinación",
]


def sin_acentos(texto: str) -> str:
    """Normaliza para comparar: sin acentos y en minúsculas (evita falsos negativos)."""
    import unicodedata
    n = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in n if not unicodedata.combining(c))

fallos = []


def check(nombre, condicion, detalle=""):
    print(f"  [{'OK  ' if condicion else 'FALLO'}] {nombre}" + (f" -> {detalle}" if detalle else ""))
    if not condicion:
        fallos.append(nombre)
    return condicion


def descifrar(payload: str) -> str:
    raw = urllib.parse.unquote_to_bytes(payload)
    return "".join(chr(b ^ XOR_KEY) for b in raw)


print("=== PAQUETE .elpx (entregable, producido por el CLI) ===")
with zipfile.ZipFile(ELPX) as z:
    nombres = z.namelist()
    xml = z.read("content.xml").decode("utf-8")

    check("content.xml en la raiz", "content.xml" in nombres)
    check("content.dtd incluido", "content.dtd" in nombres)
    check(f"{N_PAGINAS} nodos", xml.count("<odeNavStructure>") == N_PAGINAS,
          f"{xml.count('<odeNavStructure>')}")
    check(f"{N_BLOQUES} bloques / {N_COMPONENTES} componentes",
          xml.count("<odePagStructure>") == N_BLOQUES
          and xml.count("<odeComponent>") == N_COMPONENTES,
          f"{xml.count('<odePagStructure>')} / {xml.count('<odeComponent>')}")
    check(f"{N_TEXTOS} iDevices Texto",
          xml.count("<odeIdeviceTypeName>text</odeIdeviceTypeName>") == N_TEXTOS,
          f"{xml.count('<odeIdeviceTypeName>text</odeIdeviceTypeName>')}")
    check(f"{N_QUIZ} iDevices Cuestionario (evaluación + 2 test de práctica)",
          xml.count("<odeIdeviceTypeName>quick-questions</odeIdeviceTypeName>") == N_QUIZ,
          f"{xml.count('<odeIdeviceTypeName>quick-questions</odeIdeviceTypeName>')}")

    # revisión IV: un bloque por página, sin nombre de bloque. Excepción: la página de ejercicios,
    # que necesita un bloque por actividad (revisión VII).
    paginas = re.findall(r"<odeNavStructure>(.*?)</odeNavStructure>", xml, re.S)
    bloques_por_pagina = {i + 1: p.count("<odePagStructure>") for i, p in enumerate(paginas)}
    esperado = {n: (N_BLOQUES_EJERCICIOS if n == N_PAGINA_EJERCICIOS else 1) for n in bloques_por_pagina}
    check("un bloque por pagina (5 en la de ejercicios)",
          bloques_por_pagina == esperado,
          f"distintas: {[n for n in bloques_por_pagina if bloques_por_pagina[n] != esperado[n]]}")
    check("bloques sin nombre (nada de la etiqueta «Texto»)",
          "<blockName>Texto</blockName>" not in xml
          and xml.count("<blockName></blockName>") == N_BLOQUES,
          f"con nombre: {len(re.findall(r'<blockName>(.+?)</blockName>', xml))}")

    # revisión IV: menú lateral numerado y sin la etiqueta decorativa «MÓDULO x —»
    titulos = re.findall(r"<pageName>(.*?)</pageName>", xml)
    check(f"{N_PAGINAS} nombres de pagina", len(titulos) == N_PAGINAS)
    check("menu lateral «N. Titulo»", titulos == TITULOS_MENU,
          f"distintos: {[t for t in titulos if t not in TITULOS_MENU][:3]}")
    check("sin la etiqueta «MODULO» en el menu",
          not any("MÓDULO" in t.upper() for t in titulos))
    check("pagina «EJERCICIOS PRACTICOS» montada (revisión VI)",
          any(t.upper().endswith("EJERCICIOS PRÁCTICOS") for t in titulos))

    # revisión IV: tema Nova y sin referencias colgantes al recurso Latidos.gif
    check("tema Nova en userPreferences",
          re.search(r"<key>theme</key>\s*<value>nova</value>", xml) is not None)
    check("sin referencias a Latidos.gif", "Latidos" not in xml)

    # el .elpx entregable es el paquete completo (tema + html renderizado), no el mínimo
    check("el .elpx incluye el tema", any(n.startswith("theme/") for n in nombres))
    check("el .elpx incluye index.html y html/",
          "index.html" in nombres and len([n for n in nombres if re.match(r"html/.*\.html$", n)]) == N_PAGINAS - 1)

    # acordeones: componentes cuyo htmlView lleva el efecto exeeffects. El número de enlaces
    # título->contenido depende de las secciones, así que se cuenta de forma dinámica.
    comps = re.findall(r"<odeComponent>(.*?)</odeComponent>", xml, re.S)
    acordeones = [c for c in comps if "exe-fx exe-accordion" in c]
    check(f"{N_ACORDEONES} acordeones", len(acordeones) == N_ACORDEONES, f"{len(acordeones)}")
    # cada sección aparece dos veces por componente (htmlView + jsonProperties), y cada título
    # contiene la clase tres veces: se cuenta por los divs de contenido y se divide entre dos.
    secciones = sum(c.count("fx-accordion-content") for c in acordeones) // 2
    n_enlaces = len(re.findall(r'href=\\?\"#exe-accordion-', xml))
    check(f"acordeones con enlaces titulo->contenido ({secciones} secciones x2)",
          n_enlaces == 2 * secciones, f"{n_enlaces} en xml (htmlView + jsonProperties)")

    # imagenes: cada PNG/JPG del paquete debe estar referenciado en content.xml
    recursos = sorted(n for n in nombres if n.startswith("content/resources/"))
    check(f"{N_IMAGENES} imagenes en el paquete", len(recursos) == N_IMAGENES, f"{len(recursos)}")
    sin_ref = [r for r in recursos if pathlib.Path(r).name not in xml]
    check("todas las imagenes referenciadas", not sin_ref, f"sin referencia: {sin_ref}")
    n_alt = xml.count('alt="')
    check("textos alternativos en las imagenes", n_alt >= N_IMAGENES + 1, f"{n_alt}")

    check("credito de portada (ultima pagina)", "Jakub Zerdzicki" in xml)
    # la portada y la ficha del curso tienen que decir la misma duración (la del curso: 3,5 horas)
    check("portada: duracion coherente con la ficha del curso",
          "3,5 horas" in xml and "2 horas" not in xml,
          "la portada no dice 3,5 horas" if "2 horas" in xml or "3,5 horas" not in xml else "")
    check("enlaces externos con target", xml.count('target="_blank"') >= 3)

    # cuestionario: descifrar el estado y comprobar los requisitos del guion. Desde la revisión VII
    # la página de ejercicios trae además dos test de práctica (no evaluativos), así que la
    # evaluación final se identifica por isScorm=1 y no por ser el primer quick-questions.
    quices = []
    for c in comps:
        if "<odeIdeviceTypeName>quick-questions</odeIdeviceTypeName>" not in c:
            continue
        payload = re.search(r'quext-DataGame js-hidden"?>([^<]+)<', c).group(1)
        quices.append({"id": re.search(r'data-evaluationid="([^"]+)"', c).group(1),
                       "html": c, "estado": json.loads(descifrar(payload))})
    finales = [x for x in quices if x["estado"]["isScorm"] == 1]
    check("una sola evaluación final (isScorm=1)", len(finales) == 1,
          f"{[x['id'] for x in finales]}")
    estado = (finales or quices)[0]["estado"]
    check(f"cuestionario: {N_PREGUNTAS} preguntas", len(estado["questionsGame"]) == N_PREGUNTAS,
          f"{len(estado['questionsGame'])}")
    check("cuestionario: muestra las 20 preguntas (percentajeQuestions=100)",
          estado["percentajeQuestions"] == 100, f"{estado['percentajeQuestions']}")
    check("cuestionario: puntuacion SCORM activa", estado["isScorm"] == 1)
    check("cuestionario: 1 punto por pregunta",
          all(p["customScore"] == 1 for p in estado["questionsGame"]))
    check("cuestionario: orden fijo",
          estado["optionsRamdon"] is False and estado["answersRamdon"] is False)
    check("cuestionario: feedback por pregunta",
          all(p["msgHit"] and p["msgError"] for p in estado["questionsGame"]))
    check("cuestionario: 4 opciones en todas",
          all(len(p["options"]) == 4 for p in estado["questionsGame"]))
    check("cuestionario: respuesta marcada en todas",
          all(p["solution"] is not None for p in estado["questionsGame"]))
    check("cuestionario: textos de interfaz (msgs)", len(estado["msgs"]) >= 40, f"{len(estado['msgs'])}")
    check("cuestionario: instrucción con el 70 %",
          "70" in estado["instructions"], estado["instructions"][:80])

    # terminología (revisión V): ni etiquetas de licencia ni nombres comerciales antiguos, y los
    # términos funcionales nuevos presentes. Se revisa el contenido del curso y el del cuestionario.
    PROHIBIDOS = ["(con licencia)", "(sin licencia)", "(versión de pago)", "(versión free)",
                  "Copilot Chat", "Copilot Pro", "ChatGPT", "Gemini", "Gratis (incluido)",
                  "usuario/mes", "Copilot Business", "$21", "20 $"]
    cuerpo = "\n".join(re.findall(r"<htmlView><!\[CDATA\[(.*?)\]\]></htmlView>", xml, re.S))
    quiz_texto = json.dumps(estado, ensure_ascii=False)
    sobra = {p: cuerpo.count(p) + quiz_texto.count(p) for p in PROHIBIDOS
             if cuerpo.count(p) or quiz_texto.count(p)}
    check("terminologia: sin etiquetas de licencia ni nombres antiguos", not sobra, f"{sobra}")
    faltan_terminos = [t for t in ("Copilot Web", "Copilot de Trabajo", "Copilot Asistente",
                                   "agentes especializados", "Copilot Studio")
                       if t not in cuerpo]
    check("terminologia: entornos y niveles funcionales en el curso", not faltan_terminos,
          f"faltan: {faltan_terminos}")
    check("terminologia: el cuestionario usa Copilot Web / Copilot de Trabajo",
          "Copilot Web" in quiz_texto and "Copilot de Trabajo" in quiz_texto)

    # revisión VII: los test de práctica de la página de ejercicios se corrigen y explican, pero no
    # puntúan (no son la evaluación del curso).
    practica = [x for x in quices if x["estado"]["isScorm"] == 0]
    check(f"{N_TEST_PRACTICA} test de practica no evaluativos", len(practica) == N_TEST_PRACTICA,
          f"{[x['id'] for x in practica]}")
    check("test de practica: corrigen, explican y no puntuan",
          all(x["estado"].get("evaluation") is not True
              and all(p["msgHit"] and p["msgError"] and p["solution"] is not None
                      for p in x["estado"]["questionsGame"]) for x in practica))
    check("test de practica: cada pregunta con opciones",
          all(len(p["options"]) >= 2 for x in practica for p in x["estado"]["questionsGame"]))

    # revisión VII: recuadros de ideas clave (uno por página seleccionada, con su etiqueta y viñetas)
    recuadros = [c for c in comps if '<aside class="caja-ideas-clave"' in c]
    check(f"{N_RECUADROS} recuadros de ideas clave", len(recuadros) == N_RECUADROS,
          f"{len(recuadros)}")
    check("recuadros: role=note, etiqueta visible y 3+ viñetas",
          all('role="note"' in c and "caja-ideas-clave-titulo" in c and c.count("<li>") >= 3
              for c in recuadros),
          f"viñetas: {[c.count('<li>') for c in recuadros]}")
    check("recuadros: la línea «POSICIÓN:» no llega a la página",
          "POSICIÓN" not in xml and "POSICI&#211;N" not in xml)

    # revisión VII: las respuestas abiertas llevan su respuesta modelo EN el HTML. El exportador
    # solo copia `ideviceId` al json-data del iDevice, así que dejar la retroalimentación en
    # `textFeedbackTextarea` la hacía desaparecer del curso entregado (el ejercicio quedaba sin
    # respuesta y sin botón).
    abiertas = [c for c in comps if "feedbacktooglebutton" in c]
    check(f"{N_RESPUESTAS_ABIERTAS} respuestas abiertas con su boton", len(abiertas) == N_RESPUESTAS_ABIERTAS,
          f"{len(abiertas)}")
    respuestas = [re.search(r'class="feedback js-feedback js-hidden">(.*?)</div>', c, re.S)
                  for c in abiertas]
    check("respuestas abiertas: la respuesta modelo viaja en el HTML",
          all(m and len(m.group(1)) > 80 for m in respuestas),
          f"longitudes: {[len(m.group(1)) if m else 0 for m in respuestas]}")

    # bloque de cumplimiento (revisión VI): el contenido mínimo del Art. 4 tiene que estar dentro
    todo = cuerpo + "\n" + quiz_texto
    faltan_legal = [t for t in LEGAL if sin_acentos(t) not in sin_acentos(todo)]
    check("cumplimiento: contenido mínimo del Art. 4 en el curso", not faltan_legal,
          f"faltan: {faltan_legal}")
    check("cumplimiento: el cuestionario incluye preguntas legales",
          sum(1 for p in estado["questionsGame"]
              if any(t in sin_acentos(json.dumps(p, ensure_ascii=False))
                     for t in ("ai act", "rgpd", "articulo 4", "responsable del despliegue",
                               "supervision humana", "datos personales", "sobreexposicion",
                               "politica de uso"))) >= 5,
          "preguntas legales detectadas")


def revisar_export(ruta, etiqueta, scorm=False):
    print(f"\n=== EXPORT {etiqueta} ===")
    if not ruta.exists():
        check(f"{etiqueta}: existe el fichero", False, str(ruta))
        return
    with zipfile.ZipFile(ruta) as z:
        nombres = z.namelist()
        paginas = [n for n in nombres if re.match(r"html/.*\.html$", n)]
        check(f"{etiqueta}: index.html + {N_PAGINAS - 1} paginas = {N_PAGINAS} nodos",
              "index.html" in nombres and len(paginas) == N_PAGINAS - 1, f"html/={len(paginas)}")
        html = "\n".join(z.read(n).decode("utf-8", "ignore") for n in nombres
                         if n.endswith(".html") and "libs/" not in n and "idevices/" not in n)
        check(f"{etiqueta}: {N_ACORDEONES} acordeones renderizados",
              html.count("exe-fx exe-accordion") == N_ACORDEONES,
              f"{html.count('exe-fx exe-accordion')}")
        check(f"{etiqueta}: JS de efectos", "exe_effects.js" in html)
        check(f"{etiqueta}: jquery + bootstrap", "jquery.min.js" in html and "bootstrap.bundle.min.js" in html)
        check(f"{etiqueta}: cuestionario presente", "quext-DataGame" in html)
        check(f"{etiqueta}: tabla del nodo de entornos", "exe-table" in html)
        # la fila de separación del markdown no debe llegar al HTML como fila fantasma de guiones
        fantasma = re.search(r"<tr>(?:\s*<td>-+\s*</td>)+\s*</tr>", html)
        check(f"{etiqueta}: sin fila fantasma de guiones en las tablas", not fantasma,
              (fantasma.group(0)[:60] if fantasma else ""))
        check(f"{etiqueta}: {N_IMAGENES} imagenes copiadas",
              len([n for n in nombres if n.startswith("content/resources/")]) == N_IMAGENES)
        check(f"{etiqueta}: tema incluido", any(n.startswith("theme/") for n in nombres))
        check(f"{etiqueta}: tema Nova (config.xml)",
              "nova" in z.read("theme/config.xml").decode("utf-8", "ignore"))
        check(f"{etiqueta}: sin referencia a Latidos.gif", "Latidos" not in html)
        check(f"{etiqueta}: sin cajas tituladas «Texto»",
              'class="box-title"' not in html and ">Texto<" not in html)
        # terminología (revisiones V y VI) en las páginas exportadas
        sobra_exp = [p for p in ("(con licencia)", "(sin licencia)", "Copilot Chat", "Copilot Pro",
                                "usuario/mes", "Copilot Business") if p in html]
        check(f"{etiqueta}: sin etiquetas de licencia, precios ni nombres antiguos", not sobra_exp,
              f"{sobra_exp}")
        check(f"{etiqueta}: entornos con nombre funcional (Web / Trabajo)",
              "Copilot Web" in html and "Copilot de Trabajo" in html)
        faltan_legal_exp = [t for t in ("AI Act", "Reglamento (UE) 2024/1689", "RGPD",
                                        "sobreexposición", "supervisión humana")
                            if sin_acentos(t) not in sin_acentos(html)]
        check(f"{etiqueta}: contenido legal del Art. 4 en las páginas", not faltan_legal_exp,
              f"faltan: {faltan_legal_exp}")
        # titulos: los 25 nombres de pagina aparecen en la navegacion
        norm = lambda s: re.sub(r"[\s—–-]+", "", s)
        html_norm = norm(html)
        faltan = [t for t in TITULOS_MENU if norm(t) not in html_norm]
        check(f"{etiqueta}: {N_PAGINAS} titulos del menu en la navegacion", not faltan,
              f"faltan: {faltan}")
        check(f"{etiqueta}: pagina de ejercicios montada",
              any("ejercicios-practicos" in n for n in nombres))
        # revisión VII: las respuestas modelo de las actividades abiertas tienen que llegar al
        # HTML exportado. Dejarlas solo en las propiedades del iDevice las hacía desaparecer del
        # curso (el exportador solo copia `ideviceId` al json-data).
        check(f"{etiqueta}: respuestas abiertas con su boton de retroalimentacion",
              html.count("feedbacktooglebutton") >= N_RESPUESTAS_ABIERTAS,
              f"{html.count('feedbacktooglebutton')}")
        if scorm:
            man = z.read("imsmanifest.xml").decode("utf-8", "ignore")
            check("SCORM 1.2 (schemaversion)", "schemaversion>1.2" in man.replace(" ", ""))
            check("SCORM 1.2 (adlcp_rootv1p2)", "adlcp_rootv1p2" in man)
            check("SCORM: recurso sco declarado", 'scormtype="sco"' in man)


revisar_export(SCORM, "SCORM 1.2", scorm=True)
revisar_export(HTML5, "HTML5")

print("\n" + ("TODAS LAS COMPROBACIONES OK" if not fallos else f"FALLOS ({len(fallos)}): {fallos}"))
sys.exit(1 if fallos else 0)
