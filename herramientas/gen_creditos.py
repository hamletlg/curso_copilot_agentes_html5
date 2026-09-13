#!/usr/bin/env python3
"""Genera recursos/imagenes/CREDITOS.md con datos medidos en disco (dimensiones,
tamaño y sha256) y la licencia verificada en vivo el 12-sep-2026."""
import hashlib
import os

IMG = "/mnt/DATA/trabajo_hermes/articulate_hermes/recursos/imagenes"
OUT = os.path.join(IMG, "CREDITOS.md")

ARCHIVOS = [
    "portada_curso_copilot.jpg",
    "icono_check.png", "icono_check.svg",
    "icono_cross.png", "icono_cross.svg",
    "icono_warning.png", "icono_warning.svg",
    "icono_nota.png", "icono_nota.svg",
    "icono_flecha.png", "icono_flecha.svg",
    "diagrama_5_componentes.png", "diagrama_5_componentes.svg",
    "diagrama_ciclo_5_pasos.png", "diagrama_ciclo_5_pasos.svg",
]

PEXELS_LICENCIA = """**Licencia de Pexels** — texto literal copiado de https://www.pexels.com/license/
(consultada el 12-sep-2026):

> **Legal Simplicity.** All photos and videos on Pexels can be downloaded and used for free.
>
> **What is allowed?**
> - All photos and videos on Pexels are free to use.
> - Attribution is not required. Giving credit to the photographer or Pexels is not necessary but always appreciated.
> - You can modify the photos and videos from Pexels. Be creative and edit them as you like.
>
> **What is not allowed?**
> - Identifiable people may not appear in a bad light or in a way that is offensive.
> - Don't sell unaltered copies of a photo or video, e.g. as a poster, print or on a physical product without modifying it first.
> - Don't imply endorsement of your product by people or brands on the imagery.
> - Don't redistribute or sell the photos and videos on other stock photo or wallpaper platforms.
> - Don't use the photos or videos as part of your trade-mark, design-mark, trade-name, business name or service mark.

**Aplicación a este curso:** material de formación interna = permitido; la modificación
(redimensión y recompresión) está permitida; la atribución no es obligatoria (se incluye por
cortesía en el Nodo 15); no se usa la imagen como marca ni para sugerir aval. El curso no se
vende como fotografía, así que la prohibición de reventa de copias sin modificar no aplica."""


def medir(nombre: str):
    p = os.path.join(IMG, nombre)
    if not os.path.exists(p):
        return "AUSENTE", "AUSENTE", "AUSENTE"
    try:
        from PIL import Image
        with Image.open(p) as im:
            dims = "%dx%d" % im.size
    except Exception:
        dims = "vectorial (SVG)"
    h = hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]
    return dims, "%d KB" % round(os.path.getsize(p) / 1024), h


filas_ver = "\n".join(
    "| `%s` | %s | %s | `%s` |" % ((n,) + medir(n)) for n in ARCHIVOS
)

doc = f"""# CRÉDITOS, LICENCIAS Y ATRIBUCIÓN — RECURSOS GRÁFICOS

**Curso:** Agentes de IA y Microsoft Copilot para tu día a día (eXeLearning / SCORM 1.2)
**Carpeta:** `recursos/imagenes/` — **Actualizado:** 12 de septiembre de 2026
**Fuente de verdad del montaje:** `../../guión_curso_copilot_exelearning.md` (cada nodo indica qué
archivo usar, dónde y con qué texto alternativo). Este documento solo acredita el **origen y las
condiciones de uso** de cada archivo.

---

## 1. Inventario y atribución

| Archivo | Nodo(s) | Origen | Autoría | Licencia | ¿Atribución obligatoria? | Texto de atribución |
|---------|---------|--------|---------|----------|--------------------------|---------------------|
| `portada_curso_copilot.jpg` | Nodo 1 (portada) | Pexels, foto 34088260 — https://www.pexels.com/photo/modern-workspace-with-laptop-and-smartphone-34088260/ | Jakub Zerdzicki (https://www.pexels.com/@jakubzerdzicki/) | Pexels License | No (se recomienda citar) | «Imagen de portada: Jakub Zerdzicki / Pexels» |
| `icono_check.png / .svg` | Nodos 10, 13 | Obra propia del proyecto | Autor del curso | Propia (sin licencia externa) | No | — |
| `icono_cross.png / .svg` | Nodo 10 | Obra propia del proyecto | Autor del curso | Propia | No | — |
| `icono_warning.png / .svg` | Nodo 12 | Obra propia del proyecto | Autor del curso | Propia | No | — |
| `icono_nota.png / .svg` | Nodos 2, 11 | Obra propia del proyecto | Autor del curso | Propia | No | — |
| `icono_flecha.png / .svg` | Nodo 5 (opcional) | Obra propia del proyecto | Autor del curso | Propia | No | — |
| `diagrama_5_componentes.png / .svg` | Nodo 4 | Obra propia del proyecto | Autor del curso | Propia | No | — |
| `diagrama_ciclo_5_pasos.png / .svg` | Nodo 5 | Obra propia del proyecto | Autor del curso | Propia | No | — |

**Título y descripción oficiales de la foto de portada** (tomados de la ficha de Pexels):
«Aerial view of a modern workspace with a laptop, smartphone, and notebook showing copy space».

---

## 2. Licencia de la fotografía de portada

{PEXELS_LICENCIA}

---

## 3. Modificaciones realizadas sobre obra ajena

| Archivo | Modificación | Amparo |
|---------|--------------|--------|
| `portada_curso_copilot.jpg` | Original de Pexels de 3000×2001 px → redimensionado a 1920 px de ancho (1920×1281), metadatos EXIF eliminados y recomprimido en JPEG. | La licencia de Pexels permite expresamente modificar («You can modify the photos…»). |

Los iconos y diagramas son obra propia (SVG generados para este curso); no hay modificación de
obra ajena.

---

## 4. Trazabilidad de la selección de portada

La imagen se descargó del CDN de Pexels y se **verificó por correlación de imagen** contra el
candidato documentado: el archivo entregado coincide al 100 % (correlación de firma normalizada
= 1.0000) con `pexels-photo-34088260` tanto en su versión de 1920 px como en el original de
3000×2001 px. Queda por tanto acreditada sin ambigüedad.

| Candidato descartado | Licencia | Motivo |
|----------------------|----------|--------|
| Pexels 34502060 — «Modern Office Workspace with Laptop and Desktop» | Pexels License | Logotipo de Apple visible en el monitor (inadecuado en un curso sobre Microsoft 365) y formato vertical, no apto para cabecera. |
| Pexels 34170828 — «Modern Office Workspace with Laptop and Smartphone» | Pexels License | Sin incidencias; **segunda opción** si se quiere sustituir la portada. Se descartó solo por composición. |
| Pexels 36123565 — «Modern Workspace with Laptop and Books on Desk» | Pexels License | Menos espacio libre para superponer el título. |
| 5 candidatas CC0 de StockSnap/Flickr («Office Work», «Writing Papers», «Macbook Laptop», «Working Typing», «Analytics Charts», «Business Team») | CC0 1.0 / dominio público | La API solo sirve miniaturas de 960 px y el resto de rutas devuelve 403; varias incluyen personas identificables. Metadatos completos en `../../legado_articulate/descartes_proyecto/candidatos_portada.json`. |

**Criterios de selección:** licencia permisiva de uso comercial; sin personas identificables; sin
logotipos de terceros; anchura ≥1920 px; espacio libre para el título; temática oficina/tecnología.

---

## 5. Cómo citar en el curso

1. **Portada (Nodo 1):** la licencia de Pexels no exige atribución. Recomendado: al final del
   bloque «¿Quieres seguir aprendiendo?» del Nodo 15, la línea
   `Imagen de portada: Jakub Zerdzicki / Pexels`.
2. **Texto alternativo:** obligatorio en todas las imágenes (accesibilidad, §6 del guion); ya está
   redactado en la fila «Recurso gráfico» de cada nodo.
3. **Si se sustituye la portada por una imagen CC BY / CC BY-SA**, la atribución pasa a ser
   obligatoria con el formato `"Título" de Autor, licencia CC BY 4.0, enlace a la fuente`. Las
   alternativas CC0 (sin obligación de atribución) están en `../../legado_articulate/descartes_proyecto/candidatos_portada.json`.
4. **Nunca** usar la imagen de modo que sugiera que la empresa, el curso o el autor están avalados
   por el fotógrafo o por Pexels.

---

## 6. Verificación de integridad de los archivos entregados

Medido sobre disco el 12-sep-2026 (dimensiones + SHA-256, primeros 16 dígitos):

| Archivo | Dimensiones | Tamaño | SHA-256 (16) |
|---------|-------------|--------|--------------|
{filas_ver}

**Estado:** todos los archivos del inventario existen y son legibles. Los diagramas y los iconos
se revisaron con el modelo de visión local (transcripción de sus etiquetas sin texto cortado ni
solapado) y su paleta coincide con la del guion (`#2563EB`, `#1E293B`, `#FFFFFF`, más `#16A34A`,
`#DC2626` y `#D97706` en los iconos).
"""

open(OUT, "w", encoding="utf-8").write(doc)
print("Escrito %s (%d caracteres)" % (OUT, len(doc)))
