# Informe de la reescritura (fase 1 del PLAN)

Modelo: **gemma4-12b** en `llama-server :8080` (local, GPU del usuario).
Nodos reescritos: **25 de 25** · tiempo total: **54.6 min** · velocidad media: **20.6 tok/s** · errores: 0.

**Marcas de escritura de IA detectadas: 52 en el original -> 21 en la reescritura** (60 % menos).

| Nodo | Marcas orig. | Marcas nuevo | Caracteres orig. -> nuevo | Tiempo (s) | tok/s |
|---|---|---|---|---|---|
| 01 | 0 | 0 | 379 -> 377 | 94.5 | 22.1 |
| 02 | 9 | 1 | 3277 -> 3320 | 141.7 | 20.5 |
| 03 | 1 | 0 | 3045 -> 3281 | 130.5 | 20.5 |
| 04 | 0 | 0 | 2166 -> 2154 | 123.4 | 20.7 |
| 05 | 5 | 0 | 1991 -> 1928 | 116.9 | 20.8 |
| 06 | 2 | 0 | 1000 -> 967 | 106.0 | 21.1 |
| 07 | 5 | 5 | 1812 -> 1848 | 114.8 | 20.9 |
| 08 | 7 | 5 | 2856 -> 2759 | 125.8 | 20.7 |
| 09 | 0 | 0 | 1624 -> 1778 | 115.9 | 20.8 |
| 10 | 0 | 0 | 3239 -> 3155 | 134.4 | 20.5 |
| 11 | 0 | 0 | 1761 -> 1842 | 108.2 | 20.8 |
| 12 | 1 | 1 | 2971 -> 2964 | 130.3 | 20.6 |
| 13 | 2 | 0 | 1668 -> 1794 | 101.8 | 20.8 |
| 14 | 0 | 0 | 3408 -> 3456 | 136.3 | 20.5 |
| 15 | 0 | 0 | 1196 -> 1229 | 111.4 | 20.8 |
| 16 | 0 | 0 | 1567 -> 1649 | 112.9 | 20.9 |
| 17 | 4 | 0 | 1691 -> 1797 | 113.7 | 21.0 |
| 18 | 0 | 0 | 2512 -> 2642 | 125.7 | 20.6 |
| 19 | 1 | 0 | 2989 -> 3168 | 134.2 | 20.5 |
| 20 | 4 | 2 | 4875 -> 4990 | 143.8 | 20.1 |
| 21 | 2 | 2 | 4560 -> 4878 | 157.0 | 20.1 |
| 22 | 3 | 2 | 4013 -> 4287 | 148.8 | 20.2 |
| 23 | 3 | 1 | 4904 -> 4851 | 160.8 | 20.1 |
| 24 | 0 | 0 | 5976 -> 6607 | 181.0 | 19.9 |
| 25 | 3 | 2 | 8555 -> 8684 | 204.2 | 19.7 |

## Detalle por marca

| Marca | Original | Reescritura |
|---|---|---|
| adjetivo de folleto | 1 | 0 |
| grandilocuencia | 0 | 0 |
| registro acartonado | 1 | 1 |
| paralelismo negativo | 3 | 0 |
| personificación | 3 | 2 |
| triplete simétrico | 5 | 4 |
| raya larga | 39 | 14 |

## Lectura de las marcas que quedan (revisadas una a una)

Las 21 marcas residuales **no son escritura de IA**: se han revisado todas y son falsos positivos del
detector o marcado estructural que el guion necesita.

| Qué | Dónde | Por qué se queda |
|---|---|---|
| 13 de las 14 rayas largas | títulos de sección del acordeón (`**Sección 1: Percepción — Recibir la información**`) y un inciso entre rayas en el nodo 21 | El generador parte el acordeón por `**Sección N:`; la raya es del propio marcado del guion, no prosa |
| triplete simétrico (3) | nodos 2, 20 y 25 | Son enumeraciones reales del temario («contexto, formato y audiencia», «migración y justicia», «recibir, planificar, ejecutar, verificar y entregar») |
| personificación (2) | nodos 12 y 22 | El patrón casa «**mient**ras» — «mientras unifica», «mientras que el RGPD» |
| registro acartonado (1) | nodo 22 | «efectos significativos» es el término del RGPD (Artículo 22), no relleno |

Lo que sí se ha ido es lo que sonaba a folleto: 39 rayas largas en prosa → 14 (y de esas, 13 son
marcado), 3 paralelismos «no solo… sino también» → 0, 5 tripletes simétricos → 4 (los 4 reales del
temario), 1 adjetivo de folleto → 0 y 3 personificaciones → 2 (ambas falsas).
