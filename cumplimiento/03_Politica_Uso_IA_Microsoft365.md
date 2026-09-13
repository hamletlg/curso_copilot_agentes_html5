# Política de uso de inteligencia artificial en Microsoft 365

> **Qué es.** Plantilla de política interna (entregable 5 del pack), redactada para una organización
> pequeña que trabaja **solo con Microsoft 365** y usa Copilot en tareas de oficina. El curso la
> explica en la página 19 («Política de uso y protocolo de incidentes»): la política es la regla, el
> curso es la formación.
>
> **Cómo se usa.** Se rellenan los campos entre corchetes, se aprueba y se comunica. **Debe estar
> vigente antes de la formación** (el curso pide a los participantes que la usen). Se revisa una vez
> al año y cuando cambie una herramienta.
>
> **Versión:** `[n]` · **Fecha:** `[dd/mm/aaaa]` · **Responsable:** `[nombre y cargo]`

---

## 1. Objetivo y ámbito de aplicación

Esta política regula el uso de herramientas de inteligencia artificial (IA) en `[la organización]`.
Se aplica a **toda la plantilla**, a las personas en prácticas y a **cualquier tercero** (contratista,
proveedor o colaborador externo) que use sistemas de IA por cuenta de la organización.

Objetivo: que la IA se use para mejorar el trabajo, **sin comprometer la confidencialidad, la
protección de datos ni la responsabilidad** de la organización sobre lo que se hace con ella.

---

## 2. Qué herramientas están autorizadas

| Herramienta o función | Autorizada | Condiciones |
|---|---|---|
| Copilot de Trabajo (Word, Excel, PowerPoint, Outlook, Teams, SharePoint, OneNote) | Sí | Solo con la cuenta corporativa `[@dominio]` |
| Agentes creados con Agent Builder | Sí, con autorización (§5) | Solo sobre fuentes con permisos revisados |
| Copilot Web / asistentes web en general | `[Sí / No]` | `[Solo sin datos de la organización / No autorizado]` |
| Otras herramientas de IA (asistentes personales, extensiones, webs de resumen, traductores) | **No** | Solo si se solicitan y se aprueban por escrito (§8) |
| Uso de IA con **cuenta personal** para asuntos de trabajo | **No** | — |

**Regla:** si una herramienta no está en esta tabla, **no se usa con información de la organización**.
No importa que sea gratuita o que venga instalada en el navegador.

**Solicitar una herramienta nueva:** formulario del Anexo A. La valoración la hace
`[persona o departamento responsable]` y se resuelve en `[plazo]`.

---

## 3. Qué datos se pueden usar (clasificación)

| Nivel | Ejemplos | Regla |
|---|---|---|
| **Público** | Información ya publicada, catálogos abiertos | Se puede usar en cualquier herramienta autorizada |
| **Interno** | Procesos, manuales, borradores sin datos de terceros | Se puede usar en las herramientas autorizadas |
| **Confidencial** | Datos de clientes, precios, contratos, información financiera, datos de personal | **Solo en Copilot de Trabajo**, y solo si la tarea lo requiere |
| **Especialmente protegido** | Salud, datos de menores, ideología, religión, sindicación, datos biométricos | **No se escriben en prompt**. Requiere base jurídica específica y autorización expresa de `[responsable de protección de datos]` |

Reglas prácticas obligatorias:

1. **Minimizar:** se escribe solo el dato necesario. Para resumir no hacen falta nombres completos.
2. **No mezclar:** no se pegan listados de clientes ni de personal en herramientas sin autorización.
3. **Verificar:** ningún resultado generado se envía, firma o publica sin revisión humana.
4. **Datos personales:** quien detecte que se han tratado datos indebidamente lo comunica según §6.

---

## 4. Permisos y confidencialidad (sobreexposición)

- Copilot de Trabajo **no crea accesos nuevos**: muestra lo que los permisos existentes permiten.
  Por tanto, la organización se compromete a:
  - Revisar los **permisos de las carpetas y sitios sensibles** (nóminas, datos de clientes, precios,
    contratos) y restringirlos al personal que los necesita.
  - Revisar los **enlaces de uso compartido** activos y aplicar caducidad a los temporales.
  - Usar **etiquetas de confidencialidad** en los documentos sensibles.
- Si alguien **ve información que no debería**, no la usa ni la reenvía: la comunica según §6.
- Responsable de esta revisión: `[persona o proveedor informático]`, con periodicidad
  `[semestral / anual]`.

---

## 5. Agentes de IA: quién crea y quién publica

| Acción | Quién puede |
|---|---|
| Crear un agente para uso **propio** | Cualquier persona, sobre datos a los que ya tiene acceso |
| Crear un agente para **su equipo** | Con el visto bueno de su responsable |
| **Publicar** un agente para toda la organización | Solo `[TI / dirección]`, tras revisar las fuentes y los permisos |
| Conectar un agente a **sistemas de negocio** (nóminas, facturación, expedientes, CRM) | **Prohibido** sin autorización escrita de `[dirección]` y valoración de `[protección de datos]` |

Todo agente publicado debe indicar **quién es su responsable**, **qué fuentes usa** y **cada cuánto se
revisa**.

---

## 6. Protocolo de incidentes

Ante cualquier uso indebido o resultado con datos que no correspondían:

1. **Detener.** No seguir usando el resultado ni la herramienta y no compartirlo.
2. **No borrar.** Conservar la información del incidente: qué herramienta, qué datos, cuándo y quién
   lo vio.
3. **Avisar** a `[responsable de protección de datos / TI]` en `[canal y plazo]`.
4. **Corregir** lo que esté en la mano: retirar el documento compartido, corregir el permiso, retirar
   el agente.
5. **Registrar** el incidente en el registro interno (Anexo B).

Los incidentes con datos personales se valoran para su notificación a la autoridad de control
(AEPD) en los plazos legalmente previstos, si procede.

---

## 7. Formación y revisión

- **Formación obligatoria:** todo el personal que use sistemas de IA realiza la acción formativa en
  alfabetización en IA (3,5 horas), conforme al Artículo 4 del Reglamento (UE) 2024/1689. Se repite
  **una vez al año** o cuando cambie el inventario de herramientas.
- **Personal de nueva incorporación:** la realiza en `[plazo desde la incorporación]`.
- **Terceros** que operen IA por cuenta de la organización: se les exige formación equivalente
  (cláusula en `[contrato / pedido]`).
- **Registro:** se conserva la relación de participantes, el temario, la política vigente y los
  resultados de la evaluación durante **cuatro años**.

---

## 8. Responsabilidades

| Papel | Quién | Responsabilidad |
|---|---|---|
| Titular de la política | `[dirección]` | Aprobarla, revisarla y dotarla de medios |
| Responsable de IA / protección de datos | `[nombre]` | Inventario, incidentes, evaluación de nuevas herramientas |
| Administración de Microsoft 365 | `[nombre o proveedor]` | Permisos, etiquetas, enlaces, publicación de agentes |
| Todo el personal | — | Cumplir la política, verificar resultados, comunicar incidentes |

---

## 9. Consecuencias del incumplimiento

El incumplimiento de esta política se considera `[falta leve / grave / muy grave]` conforme al
régimen disciplinario de aplicación, sin perjuicio de la responsabilidad de la organización frente a
terceros y de las obligaciones del Reglamento (UE) 2024/1689.

---

## Anexo A — Solicitud de alta de herramienta o agente de IA

| Campo | Contenido |
|---|---|
| Solicitante y unidad | |
| Herramienta o agente | |
| Finalidad | |
| Datos que tratará (nivel de §3) | |
| Fuentes o sistemas conectados | |
| Proveedor y condiciones (¿entrena con los datos? ¿dónde se alojan?) | |
| Alternativa autorizada evaluada | |
| Decisión y condiciones | |
| Responsable del agente | |

## Anexo B — Registro de incidentes

| Fecha | Quién lo detectó | Descripción | Datos afectados | Medidas adoptadas | ¿Notificado? |
|---|---|---|---|---|---|
| | | | | | |
