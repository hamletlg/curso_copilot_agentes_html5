# Muestra de reescritura — nodo_17_riesgos-y-limites.md

Una sola página del guión, sin tocar el guión original.

## Qué se ha usado

| Versión | Modelo local (llama-server :8080) | Tiempo | Velocidad | Longitud |
|---|---|---|---|---|
| Original | — | — | — | 1691 car. |
| gemma4b | `/mnt/DATA/INSTALADORES/LLM-MODELS/lmstudio-community/GEMMA_4/gemma-4-E4B-it-Q5_K_S.gguf` | 34.2 s | 67.4 tok/s | 2096 car. |
| gemma4-12b | `/mnt/DATA/INSTALADORES/LLM-MODELS/lmstudio-community/GEMMA_4/gemma-4-12B-it-qat-UD-Q4_K_XL.gguf` | 113.9 s | 20.9 tok/s | 1771 car. |

Plantilla: `prompts/reescritura.md` · parámetros: los del `command_*.txt` del modelo.

## Marcas de escritura de IA detectadas

Recuento por versión (menos es mejor; 0 no significa perfecto).

| Marca | Original | gemma4b | gemma4-12b |
|---|---|---|---|
| adjetivo de folleto | 1 | 0 | 0 |
| grandilocuencia | 0 | 1 | 0 |
| registro acartonado | 0 | 3 | 0 |
| paralelismo negativo | 1 | 0 | 0 |
| personificación | 2 | 1 | 0 |
| triplete simétrico | 0 | 0 | 0 |
| raya larga | 0 | 0 | 0 |
| **Total** | **4** | **5** | **0** |

## Texto, bloque a bloque

### (entrada)

**Original.** Copilot es una herramienta increíble, pero tiene límites importantes que todo usuario debe conocer:

**gemma4b.** Copilot es una herramienta, pero existen limitaciones importantes que todo usuario debe conocer:

**gemma4-12b.** Copilot tiene límites importantes que debes conocer como usuario:

### Las alucinaciones existen

**Original.** Copilot puede inventar datos, citas o hechos con total seguridad. No porque mienta, sino porque el modelo de IA a veces genera información plausible pero falsa. Siempre verifica los datos concretos.

**gemma4b.** Copilot puede generar datos, citas o hechos que parecen ciertos. Esto no significa que esté mintiendo. El modelo de IA a veces genera información que es plausible, pero que carece de fundamento. Siempre verifica los datos concretos que te proporciona.

**gemma4-12b.** Copilot puede generar datos, citas o hechos incorrectos. Esto sucede porque el modelo de IA produce información basada en patrones estadísticos que pueden parecer plausibles pero no son ciertos. Verifica siempre los datos concretos.

### Los sesgos se transmiten

**Original.** Si los datos en los que se entrena el modelo tienen sesgos (de género, culturales, económicos), Copilot los repetirá. Un agente que resume noticias puede priorizar ciertos puntos de vista sobre otros.

**gemma4b.** Los sesgos presentes en los datos de entrenamiento del modelo serán reproducidos por Copilot. Por ejemplo, un agente que resume noticias puede priorizar sistemáticamente ciertos puntos de vista en detrimento de otros.

**gemma4-12b.** El modelo puede repetir sesgos de género, culturales o económicos presentes en sus datos de entrenamiento. Un agente que resume noticias puede priorizar ciertos puntos de vista sobre otros.

### La privacidad depende de tu empresa

**Original.** Copilot de Trabajo se rige por las mismas políticas de seguridad y protección de datos que el resto de Microsoft 365. Tus datos no se usan para entrenar modelos. Pero debes respetar las políticas de tu organización: no compartas información que no debas.

**gemma4b.** Copilot de Trabajo sigue las mismas políticas de seguridad y protección de datos que el resto de Microsoft 365. Tus datos no se utilizan para entrenar modelos. Sin embargo, debes respetar las políticas internas de tu organización y no compartir información confidencial.

**gemma4-12b.** Copilot de Trabajo sigue las políticas de seguridad y protección de datos de Microsoft 365. Tus datos no se usan para entrenar modelos. Debes respetar las políticas de tu organización y no compartir información que no debas.

### Los agentes no entienden como humanos

**Original.** Copilot puede procesar la palabra "banco" y no saber si te refieres a un banco financiero o a un banco de río. El contexto ayuda, pero no es infalible.

**gemma4b.** Copilot procesa la información basándose en patrones, no en la comprensión humana. Por ejemplo, puede procesar la palabra "banco" sin discernir si te refieres a una institución financiera o a un asiento de río. El contexto ayuda, pero no elimina la posibilidad de error.

**gemma4-12b.** Copilot procesa palabras como "banco" basándose en probabilidades. El contexto ayuda a identificar si te refieres a una entidad financiera o a una orilla de río, pero el sistema no es infalible.

### Depender demasiado es peligroso

**Original.** Si delegas todo a Copilot, pierdes habilidades propias. Si un sistema falla, ¿sabrás seguir trabajando? Usa Copilot para potenciar tu trabajo, no para reemplazarlo.

**gemma4b.** La delegación excesiva de tareas a Copilot puede provocar la pérdida de habilidades profesionales propias. Si el sistema falla, debes tener la capacidad de continuar trabajando. Utiliza Copilot como un complemento para potenciar tu rendimiento, no como un sustituto.

**gemma4-12b.** Delegar todas las tareas a Copilot puede reducir tus habilidades propias. Si el sistema falla, debes saber trabajar sin él. Usa Copilot para mejorar tu trabajo, no para sustituirlo.

### Los agentes no son éticos por defecto

**Original.** Copilot no tiene conciencia moral. Si le pides algo incorrecto, puede hacerlo sin cuestionarlo. Tú eres el responsable final de lo que Copilot hace.

**gemma4b.** Copilot no posee conciencia moral. Si le solicitas una acción incorrecta o inapropiada, la ejecutará sin cuestionarla. La responsabilidad final de las acciones de Copilot es siempre tuya.

**gemma4-12b.** Copilot no tiene conciencia moral. Si le pides realizar una acción incorrecta, la ejecutará siguiendo tus instrucciones. Eres el responsable final de los resultados que genere la herramienta.

### Gobernanza corporativa

**Original.** Si tu empresa usa Agent Builder o Copilot Studio para crear agentes, hay controles de TI que determinan qué agentes se pueden publicar, a quién se pueden compartir y qué datos pueden acceder. Respeta estos controles.

**gemma4b.** Cuando tu empresa utiliza Agent Builder o Copilot Studio para desarrollar agentes, existen controles de TI específicos. Estos controles definen qué agentes se pueden publicar, con quién se pueden compartir y a qué datos pueden acceder. Es fundamental que respetes estos límites.

**gemma4-12b.** Si tu empresa utiliza Agent Builder o Copilot Studio para crear agentes, existen controles de TI que determinan qué agentes se pueden publicar, a quién se pueden compartir y a qué datos pueden acceder. Respeta estos controles.

## Versiones completas

**Original**

```markdown
Copilot es una herramienta increíble, pero tiene límites importantes que todo usuario debe conocer:

**Las alucinaciones existen**
Copilot puede inventar datos, citas o hechos con total seguridad. No porque mienta, sino porque el modelo de IA a veces genera información plausible pero falsa. Siempre verifica los datos concretos.

**Los sesgos se transmiten**
Si los datos en los que se entrena el modelo tienen sesgos (de género, culturales, económicos), Copilot los repetirá. Un agente que resume noticias puede priorizar ciertos puntos de vista sobre otros.

**La privacidad depende de tu empresa**
Copilot de Trabajo se rige por las mismas políticas de seguridad y protección de datos que el resto de Microsoft 365. Tus datos no se usan para entrenar modelos. Pero debes respetar las políticas de tu organización: no compartas información que no debas.

**Los agentes no entienden como humanos**
Copilot puede procesar la palabra "banco" y no saber si te refieres a un banco financiero o a un banco de río. El contexto ayuda, pero no es infalible.

**Depender demasiado es peligroso**
Si delegas todo a Copilot, pierdes habilidades propias. Si un sistema falla, ¿sabrás seguir trabajando? Usa Copilot para potenciar tu trabajo, no para reemplazarlo.

**Los agentes no son éticos por defecto**
Copilot no tiene conciencia moral. Si le pides algo incorrecto, puede hacerlo sin cuestionarlo. Tú eres el responsable final de lo que Copilot hace.

**Gobernanza corporativa**
Si tu empresa usa Agent Builder o Copilot Studio para crear agentes, hay controles de TI que determinan qué agentes se pueden publicar, a quién se pueden compartir y qué datos pueden acceder. Respeta estos controles.

```

**gemma4b**

```markdown
Copilot es una herramienta, pero existen limitaciones importantes que todo usuario debe conocer:

**Las alucinaciones existen**
Copilot puede generar datos, citas o hechos que parecen ciertos. Esto no significa que esté mintiendo. El modelo de IA a veces genera información que es plausible, pero que carece de fundamento. Siempre verifica los datos concretos que te proporciona.

**Los sesgos se transmiten**
Los sesgos presentes en los datos de entrenamiento del modelo serán reproducidos por Copilot. Por ejemplo, un agente que resume noticias puede priorizar sistemáticamente ciertos puntos de vista en detrimento de otros.

**La privacidad depende de tu empresa**
Copilot de Trabajo sigue las mismas políticas de seguridad y protección de datos que el resto de Microsoft 365. Tus datos no se utilizan para entrenar modelos. Sin embargo, debes respetar las políticas internas de tu organización y no compartir información confidencial.

**Los agentes no entienden como humanos**
Copilot procesa la información basándose en patrones, no en la comprensión humana. Por ejemplo, puede procesar la palabra "banco" sin discernir si te refieres a una institución financiera o a un asiento de río. El contexto ayuda, pero no elimina la posibilidad de error.

**Depender demasiado es peligroso**
La delegación excesiva de tareas a Copilot puede provocar la pérdida de habilidades profesionales propias. Si el sistema falla, debes tener la capacidad de continuar trabajando. Utiliza Copilot como un complemento para potenciar tu rendimiento, no como un sustituto.

**Los agentes no son éticos por defecto**
Copilot no posee conciencia moral. Si le solicitas una acción incorrecta o inapropiada, la ejecutará sin cuestionarla. La responsabilidad final de las acciones de Copilot es siempre tuya.

**Gobernanza corporativa**
Cuando tu empresa utiliza Agent Builder o Copilot Studio para desarrollar agentes, existen controles de TI específicos. Estos controles definen qué agentes se pueden publicar, con quién se pueden compartir y a qué datos pueden acceder. Es fundamental que respetes estos límites.

```

**gemma4-12b**

```markdown
Copilot tiene límites importantes que debes conocer como usuario:

**Las alucinaciones existen**
Copilot puede generar datos, citas o hechos incorrectos. Esto sucede porque el modelo de IA produce información basada en patrones estadísticos que pueden parecer plausibles pero no son ciertos. Verifica siempre los datos concretos.

**Los sesgos se transmiten**
El modelo puede repetir sesgos de género, culturales o económicos presentes en sus datos de entrenamiento. Un agente que resume noticias puede priorizar ciertos puntos de vista sobre otros.

**La privacidad depende de tu empresa**
Copilot de Trabajo sigue las políticas de seguridad y protección de datos de Microsoft 365. Tus datos no se usan para entrenar modelos. Debes respetar las políticas de tu organización y no compartir información que no debas.

**Los agentes no procesan información como humanos**
Copilot procesa palabras como "banco" basándose en probabilidades. El contexto ayuda a identificar si te refieres a una entidad financiera o a una orilla de río, pero el sistema no es infalible.

**Depender demasiado es peligroso**
Delegar todas las tareas a Copilot puede reducir tus habilidades propias. Si el sistema falla, debes saber trabajar sin él. Usa Copilot para mejorar tu trabajo, no para sustituirlo.

**Los agentes no tienen ética propia**
Copilot no tiene conciencia moral. Si le pides realizar una acción incorrecta, la ejecutará siguiendo tus instrucciones. Eres el responsable final de los resultados que genere la herramienta.

**Gobernanza corporativa**
Si tu empresa utiliza Agent Builder o Copilot Studio para crear agentes, existen controles de TI que determinan qué agentes se pueden publicar, a quién se pueden compartir y a qué datos pueden acceder. Respeta estos controles.

```

