# Matriz de trazabilidad — curso «Agentes de IA y Microsoft Copilot» frente al Artículo 4 del AI Act

> **Qué es.** El documento que convierte un curso en **evidencia de cumplimiento**: relaciona, uno a
> uno, lo que exige el Artículo 4 del Reglamento (UE) 2024/1689 (en su redacción tras el
> Reglamento (UE) 2026/1744) con las páginas del curso, las preguntas que lo evalúan y la evidencia
> que queda archivada.
>
> **Cómo se usa.** Se adjunta como **Anexo I de la memoria de justificación**. Es lo primero que
> permite responder a la pregunta «¿y esto cómo cumple?» sin tener que abrir el paquete SCORM.
>
> **Versión:** 13-sep-2026 · Curso de 25 páginas, 3,5 horas, cuestionario de 20 preguntas.

---

## 1. Los pasos mínimos de la AI Office, cubiertos por el curso

La Oficina Europea de IA publica en su Q&A sobre alfabetización (`digital-strategy.ec.europa.eu`)
los pasos que debe considerar un programa conforme al Artículo 4. Esta es la correspondencia con el
curso:

| Paso (AI Office) | Qué exige | Páginas del curso | Preguntas del cuestionario | Ejercicios |
|---|---|---|---|---|
| **a)** Comprensión general de la IA | Qué es la IA, cómo funciona, qué IA se usa en la organización, oportunidades y peligros | 3 (de la IA al agente) · 4 (qué puede y qué no) · 5 (agente) · 7 (componentes) · 14 (inventario) | 2, 6, 11, 12, 13 | 1, 3 |
| **b)** El papel de la organización | ¿Desarrollamos sistemas de IA o solo los usamos? (proveedor / **responsable del despliegue**) | 20 (AI Act) · 21 (Artículo 4) | 16 | — |
| **c)** El riesgo de los sistemas | Qué hay que saber al usarlos, qué riesgos existen y cómo mitigarlos | 17 (riesgos y límites) · 18 (permisos y sobreexposición) · 19 (política y protocolo) · 20 (niveles de riesgo) | 5, 8, 9, 15, 19 | 3, 4 |
| **d)** Adaptación al público y al contexto | Ajustar al conocimiento previo y al contexto de uso (oficina, Microsoft 365) | Todo el curso está escrito para una oficina que solo usa Microsoft 365; el diagnóstico previo (entregable 1 del pack) completa este paso por empresa | — | 4 (caso práctico) |

Además, la Q&A señala que los pasos **a) a d) incluyen aspectos legales y éticos**: eso es lo que
cubren las páginas 19 (política y protocolo), 21 (Artículo 4) y 22 (datos personales, derechos y
supervisión humana), evaluadas en las preguntas **17, 18, 20** y **16, 19** respectivamente.

---

## 2. Correspondencia con los bloques A-E del informe interno

| Bloque (informe `01_Reporte_Normativa_IA_Art4.md` §3.1) | Páginas del curso |
|---|---|
| **A.** ¿Qué es la IA? (conceptos, capacidades y limitaciones) | 3, 4, 5, 7 |
| **B.** Qué IA usa tu organización (inventario) | 6 (entornos), 14 (inventario y shadow AI) |
| **C.** Oportunidades y riesgos (alucinaciones, sesgos, privacidad) | 4, 17, 18 |
| **D.** Interpretación de resultados | 9 (ciclo: verificar), 15 (instrucciones), 16 (buenas prácticas), 23 (ejercicio de caso práctico) |
| **E.** Marco legal y ético | 19, 20, 21, 22 |

**Ningún bloque queda sin página.** Las páginas 1, 2, 8, 10, 11, 12, 13 y 24-25 son portada,
orientación, aplicaciones de producto, evaluación y cierre.

---

## 3. Evidencia que genera la acción formativa

| Evidencia | Dónde queda | Para qué sirve |
|---|---|---|
| Paquete SCORM 1.2 con las 25 páginas y el cuestionario de 20 preguntas | `entregables/curso_copilot_agentes_scorm12.zip` | Demostrar **qué contenido** se impartió y que es verificable (sha256 en el historial de entregas) |
| Registro de puntuación del cuestionario | `cmi.core.score.raw` y `lesson_status` en el LMS (o el CSV de la plantilla de acta) | Demostrar **que se evaluó** y con qué resultado |
| Relación de participantes con fechas y horas | `cumplimiento/04_Acta_Asistentes_y_Certificado.md` | Demostrar **a quién** se formó y **cuándo** |
| Temario de la acción formativa | `cumplimiento/05_Temario_FUNDAE.md` | Demostrar que el contenido era **adecuado y estructurado** |
| Política de uso de IA vigente y fechada | `cumplimiento/03_Politica_Uso_IA_Microsoft365.md` | Demostrar que la formación se apoya en una **regla interna** |
| Esta matriz de trazabilidad | `cumplimiento/01_Matriz_Trazabilidad_Art4.md` (Anexo I de la memoria) | Demostrar que **el contenido responde a la obligación** |
| Memoria de justificación | `cumplimiento/02_Memoria_Justificacion.md` | Documento de cabecera que reúne todo lo anterior |

**Conservación:** cuatro años (plazo de custodia habitual de la formación bonificada y estándar
práctico más seguro).

---

## 4. Qué NO exige el Artículo 4 (para no sobredimensionar el proyecto)

Verificado en la Q&A de la AI Office el 13-sep-2026:

- **No** exige garantizar un nivel concreto de alfabetización de ninguna persona (Reglamento (UE)
  2026/1744, que sustituye el Artículo 4).
- **No** exige medir los conocimientos de cada persona.
- **No** existe un examen oficial, un certificado obligatorio, un formato obligatorio ni un mínimo
  de horas.
- **No** hay requisitos específicos por sector.

Lo que sí exige: **adoptar medidas** para apoyar el desarrollo de la alfabetización, proporcionadas
al riesgo y al papel de la organización, y **poder demostrarlo**. Es una obligación de medios, y este
curso —con su memoria, su política y su registro— es la evidencia de esos medios.

---

## 5. Avisos de uso

1. **La obligación es de la empresa, no del curso.** El curso es el medio, no el cumplimiento. Sin
   diagnóstico previo, sin política propia y sin registro de participantes, la memoria no se sostiene.
2. **El umbral de aprobación (14/20 = 70 %) se configura en el LMS**, no viaja en el paquete SCORM
   1.2 (comportamiento del estándar: lee `cmi.student_data.mastery_score`). Verificar en el LMS antes
   de la primera convocatoria.
3. **Adaptación por empresa.** El curso es genérico por diseño (misma oficina, Microsoft 365). Lo que
   debe personalizarse en cada implantación: inventario de herramientas (página 14), política interna
   (página 19), ejemplos con documentos reales del cliente y el protocolo de incidentes.
4. **Revisión anual.** El contenido cita productos y normas que cambian. Está previsto revisarlo una
   vez al año; la fecha de última revisión figura en la ficha del guion (§1) y en el cierre del curso.
5. Este documento es de diseño instruccional y organización interna; no es asesoramiento jurídico.
