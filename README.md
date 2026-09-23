# Curso e-learning: alfabetización en IA con Microsoft Copilot (Microsoft 365)

Curso **SCORM 1.2 / HTML5** de **25 páginas y 3,5 horas** sobre el uso responsable de la IA en una
oficina que trabaja con Microsoft 365, diseñado para responder al **contenido mínimo del Artículo 4
del Reglamento (UE) 2024/1689 (AI Act)** —la obligación de alfabetización en IA de proveedores y
responsables del despliegue— y con el **expediente de evidencia** que convierte el material en una
acción formativa justificable.

> **Demo navegable:** si el repositorio tiene GitHub Pages activado, el curso se puede recorrer en
> línea desde `/docs` (`https://<usuario>.github.io/<repositorio>/`). También se puede abrir en local:
> `python3 -m http.server -d docs` y entrar en `http://127.0.0.1:8000`.

**Estado:** revisión VII · 22-sep-2026 · texto reescrito, 8 recuadros de ideas clave y la página de
ejercicios montada con iDevices interactivos; material terminado y verificado (sin navegador y en
Chrome real). Pendientes menores al final.

> **Revisión VII (22-sep-2026):** los textos de las 25 páginas se reescribieron con un LLM local
> (Gemma 4 12B) para que suenen a persona y no a máquina, sin perder el registro profesional; se
> añadió un **recuadro de ideas clave** a mitad de página en 8 páginas (5, 10, 14, 17, 18, 19, 21 y
> 22); y la página de **ejercicios** dejó de ser texto plano —sus 4 actividades son ahora iDevices
> nativos: 2 test de práctica que corrigen y explican sin puntuar y 2 respuestas abiertas con el
> botón de retroalimentación del iDevice—. El detalle está en
> `reescritura_humana/README.md` y `reescritura_humana/PLAN.md`.

---

## 1. Qué problema resuelve

El Artículo 4 del AI Act obliga desde febrero de 2025 a **adoptar medidas para apoyar el desarrollo de
la alfabetización en IA** del personal (y de terceros que operen los sistemas por cuenta de la
organización). Tras el Reglamento (UE) 2026/1744 es una **obligación de medios**: no exige un nivel
concreto por persona, ni un formato, ni horas mínimas, ni certificación oficial. Lo que exige es
**hacer algo serio, proporcionado al riesgo, y poder demostrarlo**.

El problema práctico de una PYME es doble:

1. **No hay material accesible a su medida.** La formación que existe es o muy técnica (para
   desarrolladores) o marketing de producto. Y para una oficina que solo usa Microsoft 365, el riesgo
   real no son los sistemas de alto riesgo: son las **alucinaciones**, los **datos personales que se
   cuelan en un prompt** y la **sobreexposición de permisos** (Copilot hereda los permisos de
   SharePoint: si estaban mal, aparecen documentos que nadie debía ver).
2. **Formar no es cumplir.** Sin temario, sin política interna, sin registro de participantes y sin
   resultados de evaluación, no hay nada que enseñar en una inspección.

Este repositorio resuelve las dos: **el curso** y **el expediente**.

---

## 2. Qué hay dentro

### El curso (25 páginas, 4 partes, 3,5 h)

| Parte | Páginas | Contenido |
|---|---|---|
| **1. Fundamentos de IA** | 3-9 | Qué es la IA (IA, aprendizaje automático, IA generativa, LLM, agente); qué puede y qué no puede hacer; qué es un agente; Copilot Web y Copilot de Trabajo; los 5 componentes; los tipos de agente de Microsoft; el ciclo de trabajo |
| **2. Copilot en tu día a día** | 10-14 | Casos de uso en Word, Outlook, OneNote, Excel, PowerPoint, Teams, SharePoint y Loop; crear agentes con Agent Builder; **inventario de IA de la empresa** (funciones ya activas y *shadow AI*) |
| **3. Uso responsable** | 15-19 | Instrucciones efectivas; buenas prácticas; riesgos y límites (alucinaciones, sesgos, privacidad, dependencia); **permisos y sobreexposición**; **política de uso, clasificación de datos y protocolo de incidentes** |
| **4. Marco legal y obligaciones** | 20-22 | El AI Act y sus cuatro niveles de riesgo; **Artículo 4** (qué obliga y qué hay que poder demostrar); **datos personales, derechos y supervisión humana** (RGPD + Estatuto de los Trabajadores) |
| **Cierre y evaluación** | 23-25 | Cuatro ejercicios con respuestas comentadas; cuestionario de **20 preguntas** (14 correctas, 70 %); resumen, glosario de 29 términos y recursos |

### El expediente de cumplimiento (`cumplimiento/`)

| Documento | Para qué |
|---|---|
| `01_Matriz_Trazabilidad_Art4.md` | Relaciona los pasos del contenido mínimo (Q&A de la AI Office) con las páginas del curso y sus preguntas |
| `02_Memoria_Justificacion.md` | Memoria de la acción formativa (plantilla, con la matriz como Anexo I) |
| `03_Politica_Uso_IA_Microsoft365.md` | Política interna de uso de IA (plantilla lista para adaptar) |
| `04_Acta_Asistentes_y_Certificado.md` | Relación de participantes y certificado interno (plantillas) |
| `05_Temario_FUNDAE.md` | Temario en formato de justificación de formación (3,5 h) |

### El proceso de producción (`herramientas/`, `00_LEEME_PRIMERO.md`)

Todo el curso se genera **por código**, sin tocar la interfaz de eXeLearning: el guion en markdown se
convierte en `content.xml` (validado contra el DTD y el XSD oficiales), se empaqueta a `.elpx` y se
exporta a SCORM 1.2 y HTML5 con el CLI del contenedor. Después se verifica **sin navegador** y con
**Chrome real** (acordeones, cuestionario, navegación).

```
guion_curso_copilot_exelearning.md      <- documento de producción (25 nodos, texto literal)
contenido_curso_copilot_agentes.md      <- contenido maestro (mismo texto, en prosa)
herramientas/
  revision_vi.py + revision_vi_nodos_nuevos.md   revisión VI: contenido nuevo y reconstrucción
  revision_vii.py                                revisión VII: sincroniza el maestro con el guion
  generar_curso_elpx.py                          guion -> content.xml -> .elpx (valida DTD/XSD)
  exportar.sh                                    -> .elpx + SCORM 1.2 + HTML5 (CLI de eXeLearning)
  verificar_paquete.py                           87 comprobaciones sin navegador
  pruebas_interaccion.py                         pruebas reales en Chrome (CDP)
  capturar_pantallas.py                          capturas del curso
reescritura_humana/                            revisión VII: reescritura, recuadros y actividades
  reescribir.py · escribir_recuadros.py          el LLM local escribe textos y recuadros
  volcar_guion.py                                vuelca al guion (con red de seguridad de estructura)
  verificar_recuadros.py                         el recuadro y su CSS EN los tres entregables
```

---

## 3. Cómo se verifica (evidencia, no promesas)

| Comprobación | Resultado |
|---|---|
| Validación del paquete contra el DTD y el XSD oficiales de eXeLearning | OK |
| **87 comprobaciones** automáticas (`verificar_paquete.py`): 25 páginas, 29 bloques, 4 acordeones y sus enlaces, 10 imágenes referenciadas, 20 preguntas, terminología sin etiquetas de licencia ni precios, el **contenido mínimo del Art. 4 presente en el curso**, los **8 recuadros**, las **2 respuestas abiertas con su respuesta modelo** y la **duración de la portada** (coherente con la ficha: 3,5 h) | Todas OK |
| Fidelidad de textos guion → HTML (25 páginas, incluidas las actividades interactivas) y del cuestionario (20 preguntas) | OK |
| Recuadros: CSS en los tres entregables, uno por página seleccionada, en su sitio y sin intrusos (`verificar_recuadros.py`) | OK |
| Pruebas de interacción en Chrome real: acordeón (desplegar/plegar), cuestionario (puntúa), navegación al pie, portada con *overlay*, recuadro con su estilo y respuesta modelo desplegable | OK |
| Capturas del render final | `entregables/capturas/rev7/` |

Además, el contenido legal se contrastó el 13-sep-2026 con fuentes oficiales: la **Q&A de la AI Office**
sobre alfabetización en IA (`digital-strategy.ec.europa.eu`), el **Reglamento (UE) 2024/1689** y el
**Reglamento (UE) 2026/1744** (EUR-Lex) y el **proyecto de ley orgánica** español (BOCG-15-A-97-1).

---

## 4. Los entregables

| Archivo | Qué es |
|---|---|
| `entregables/curso_copilot_agentes_scorm12.zip` | **Paquete SCORM 1.2** (1,6 MB): el que se sube al LMS |
| `entregables/curso_copilot_agentes_html5.zip` | Export **HTML5** para publicar sin LMS |
| `entregables/curso_copilot_agentes.elpx` | Proyecto completo abrible en eXeLearning (tema Nova, iDevices) |
| `entregables/curso_copilot_agentes_html5/` | El mismo HTML5 **descomprimido** (el paquete que se publica; se reconstruye desde el zip en `exportar.sh`) |
| `entregables/content.xml` | Fuente generada (validada contra DTD/XSD) |
| `docs/` | El HTML5 desplegado, listo para GitHub Pages (lo que sirve el sitio) |

**Nota de implantación:** la **nota de corte (70 %)** se configura en el LMS, no viaja en el paquete
SCORM 1.2 (el estándar lee `cmi.student_data.mastery_score`; por defecto usaría 50).

---

## 5. Cómo reutilizarlo

1. **Usar el curso tal cual:** subir el SCORM al LMS. Está escrito para una oficina genérica con
   Microsoft 365; los ejemplos son de administración, documentación y reuniones.
2. **Adaptarlo a una empresa concreta:** rellenar el inventario (página 14), la política interna
   (página 19, con la plantilla de `cumplimiento/03_…`) y sustituir los ejemplos por documentos
   propios. El contenido vive en **un solo sitio**: el **guion**, del que se derivan el curso
   (`generar_curso_elpx.py`) y el maestro (`herramientas/revision_vii.py`, que comprueba página a
   página que no se pierde ni una palabra).
3. **Regenerar el paquete** tras cualquier cambio:

```
python3 herramientas/revision_vi.py          # solo si hay que reaplicar la revisión VI
python3 herramientas/generar_curso_elpx.py --check
sh herramientas/exportar.sh                  # exporta y APLICA los ajustes del curso a los 3 paquetes
python3 herramientas/verificar_paquete.py
python3 herramientas/pruebas_interaccion.py
sh herramientas/publicar_docs.sh             # actualiza docs/ (demo de GitHub Pages)
```

### Republicar la demo (GitHub Pages)

`publicar_docs.sh` copia el **paquete descomprimido entregable** (`entregables/curso_copilot_agentes_html5/`)
en `docs/`, que es lo que sirve el sitio: <https://hamletlg.github.io/curso_copilot_agentes_html5/>.

```
sh herramientas/publicar_docs.sh --verificar   # ¿docs/ ya es la versión final? (no escribe nada)
sh herramientas/publicar_docs.sh               # copia, verifica y deja los comandos de git
sh herramientas/publicar_docs.sh --push        # copia, verifica, commitea, empuja y espera a Pages
```

Guardas incorporadas (existen porque ya pasó: `docs/` llegó a servir la revisión anterior):

- **Origen único:** siempre el paquete descomprimido entregable, nunca `entregables/html5_preview/`
  (una preview intermedia puede quedarse de una exportación vieja).
- **Aborta si el origen no lleva los ajustes del curso** (busca la marca «ajustes del curso»), que
  es lo que aplica `ajustes_curso.py` — ya integrado en `exportar.sh`, así que una exportación
  completa los lleva siempre.
- **Aborta si el paquete descomprimido y el `.zip` entregable no coinciden** (`index.html`).
- **`docs/` se reemplaza entero** (la versión anterior se archiva en `entregables/historial/docs_*`):
  no sobreviven páginas de revisiones previas.
- **Verificación posterior:** `index.html` idéntico (md5), `.nojekyll` presente, ninguna página
  sobrante y `verificar_enlaces.py` sin referencias rotas. Si algo falla, sale con error.

`--forzar` salta las dos guardas de contenido (para publicar a sabiendas algo sin ajustes).

---

## 6. Decisiones de diseño que conviene conocer

- **Product-agnóstico en lo esencial.** El curso enseña IA y sus riesgos; Copilot es el ejemplo, no el
  objeto. La distinción Copilot Web / Copilot de Trabajo se usa porque es la que determina qué datos se
  pueden escribir en el prompt.
- **Sin capturas de pantalla.** Caducan rápido y Microsoft condiciona su uso; en su lugar hay rutas de
  clic por aplicación.
- **Sin etiquetas de licencia ni precios** en el texto didáctico: el alumno necesita saber **dónde
  opera** el asistente y **qué puede hacer**, no cómo se factura.
- **Una única fuente de contenido:** el guion manda; el maestro se deriva de él con un script, para que
  no vuelvan a divergir.
- **El curso no incluye la política ni la memoria:** las explica y las aprovecha. Son entregables
  aparte, porque son del cliente.

---

## 7. Alcance y límites (honestidad de portafolio)

- **No es asesoramiento jurídico.** El contenido legal es divulgativo y cita fuentes oficiales; la
  organización debe contrastar sus obligaciones cuando su uso de IA cambie de naturaleza.
- **No cubre sistemas de alto riesgo** (selección de personal con IA, scoring, biometría): una oficina
  que redacta, resume y busca información no está ahí. El curso explica cuándo se entraría en ese
  ámbito y por qué.
- **Pendientes declarados:** confirmar el **titular** del curso (autoría) y la licencia del
  repositorio; comprobar en un tenant real la ruta del menú de un agente de Planner (páginas 10-12);
  configurar la nota de corte en el LMS y probar el SCORM en un visor real (Moodle, SCORM Cloud).

---

## 8. Licencia y créditos

- **Contenido del curso** (guion, maestro, documentos, diagramas y paquete exportado): **CC BY-NC-SA
  4.0** — se puede usar, adaptar y compartir sin fines comerciales, citando autoría y compartiendo
  igual. Cualquier uso comercial requiere autorización (ver `LICENSE`).
- **Código** (`herramientas/`): **MIT**.
- **Imagen de portada:** Jakub Zerdzicki / Pexels (licencia Pexels, atribución no obligatoria).
  Licencias, sha256 y trazabilidad de **todos** los recursos: `recursos/imagenes/CREDITOS.md`.
- **Marcas:** Microsoft, Microsoft 365 y Copilot son marcas de Microsoft Corporation. Este curso no
  está patrocinado ni avalado por Microsoft.

---

## English summary

**AI literacy e-learning course (SCORM 1.2 / HTML5), 25 pages / 3.5 hours, built for EU AI Act
Article 4 compliance (Regulation (EU) 2024/1689, as amended by Regulation (EU) 2026/1744).** It covers
AI fundamentals, Copilot in Microsoft 365, responsible use (hallucinations, oversharing, shadow AI,
data classification, incident handling) and the legal module (AI Act, Article 4, GDPR, human
oversight), plus a 20-question assessment. The `cumplimiento/` folder contains the compliance
paperwork (traceability matrix mapped to the AI Office Q&A, justification memo, AI-use policy,
attendance/certificate templates and the course syllabus). The whole course is **generated from a
markdown script by code** (DTD/XSD-validated), and every build is checked by 80 automated assertions
and real-browser interaction tests. Spanish-language course; documentation also in Spanish.
Built with eXeLearning (local container), Python and Chrome DevTools Protocol.
