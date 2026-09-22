# Dónde lleva recuadro de ideas clave cada página

Análisis de las 25 páginas del guión, hecho sobre el texto ya reescrito. El recuadro es un bloque
de refuerzo que va **a mitad de página**: recuerda lo que el alumno no debería perder y rompe la
monotonía de una página solo de prosa.

## Criterios

1. **Densidad de prosa.** Si la página ya es una lista o una tabla, el recuadro sobra: repite lo
   que el alumno acaba de leer en el mismo formato.
2. **Información crítica.** Entra donde equivocarse tiene consecuencias: el concepto central del
   curso, los riesgos reales, las obligaciones legales, el protocolo de incidentes.
3. **Reparto, no barrido.** 8 de 25 páginas. Si el recuadro apareciera en todas, el alumno dejaría
   de leerlo: es justo lo contrario de lo que se busca.
4. **Variedad de posición.** El anclaje se elige en cada página en un punto distinto (entre el 30 %
   y el 70 % del texto), para que no caiga siempre en el mismo sitio.
5. **Sin duplicar un resumen propio.** La página que ya tiene un bloque de cierre del tipo «Lo que
   tienes que recordar» se queda sin recuadro.

## Selección

| Nodo | Página | Anclaje (se coloca tras…) | Posición aprox. | Por qué |
|---|---|---|---|---|
| 5 | ¿Qué es un agente de IA? | el bloque de la definición clave | ~45 % | Es el concepto central del curso; el recuadro fija la diferencia entre chatbot y agente antes de entrar en los tres niveles |
| 10 | Copilot en Word, Outlook y OneNote | la sección de correo en Outlook | ~30 % | Recapitula qué aporta Copilot en cada aplicación, que es lo que el alumno va a recordar cuando lo abra |
| 14 | El inventario de IA de tu empresa | la sección de la IA que ya está en Microsoft 365 | ~55 % | Deja claro qué IA corre ya en la casa sin que nadie la haya apuntado en ningún sitio |
| 17 | Riesgos y límites | el bloque de los agentes y el lenguaje | ~55 % | Los riesgos que de verdad ocurren en una oficina, condensados |
| 18 | Permisos, sobreexposición y shadow AI | la sección de cómo se produce el problema | ~50 % | El riesgo de confidencialidad número uno: merece el alto en el camino |
| 19 | Política de uso y protocolo de incidentes | la regla práctica de la clasificación de datos | ~51 % | Qué hacer cuando algo sale mal: no se puede depender de haber leído toda |
| 21 | Artículo 4 | la sección de qué debe cubrir la formación | ~60 % | Los bloques que la formación tiene que tocar sí o sí |
| 22 | Datos personales, derechos y supervisión humana | la sección de supervisión humana | ~55 % | Qué significa supervisión humana de verdad, que es el punto que más se malinterpreta |

**8 páginas con recuadro (32 %).** Reparto por módulo: 1 en fundamentos, 2 en aplicaciones,
3 en uso responsable y 2 en marco legal. Es coherente con el peso informativo de cada módulo.

## Páginas descartadas, y por qué

| Página | Motivo |
|---|---|
| 1 Portada | Es el título del curso y una línea de introducción: no hay ideas que reforzar |
| 2 Índice y objetivos | Página de orientación; el recuadro competiría con la lista de objetivos |
| 3 De la IA al agente | **Ya tiene** un bloque de cierre propio («Lo que tienes que recordar de esta página»): dos resúmenes en la misma página se anulan |
| 4 Qué puede y qué no | Ya estructura la información en tabla y en «tres reglas» |
| 6 Copilot Web y de Trabajo | Corta (1.000 car.) y con tabla propia |
| 7 Los 5 componentes · 8 Tipos de agente · 15 Buenas instrucciones · 20 El AI Act | Acordeón: el alumno ya despliega lo que le interesa, el recuadro sería un bloque más que abrir |
| 9 El ciclo del agente | Es una lista de cinco pasos: el recuadro repetiría la lista |
| 11 · 12 · 13 Aplicaciones y Agent Builder | Misma estructura que la 10, que ya lleva recuadro; no conviene encadenar recuadros en páginas seguidas |
| 16 Buenas prácticas | Es ya una lista de siete prácticas: el recuadro sobra |
| 23 Ejercicios · 24 Evaluación | Son actividades: el recuadro no aporta y estorba |
| 25 Resumen, glosario y recursos | Es la página de cierre del curso: ya es, entera, un resumen |

## Cómo se colocan (mecánica)

En el guión, cada recuadro es una fila nueva del nodo:

```
| **Recuadro de ideas clave** | **POSICIÓN:** tras «<texto de un párrafo o título>»<br><br>**Ideas clave**<br><br>- …<br>- … |
```

El generador busca ese texto en el HTML ya montado de la página y deja el recuadro **detrás del
elemento que lo contiene**: si el anclaje es un encabezado, el recuadro cierra la sección entera;
si es un párrafo o una etiqueta en negrita, entra justo detrás; si cae dentro de una lista, espera
a que la lista termine. Si el texto no existe o aparece más de una vez, **el generador falla en
voz alta** en vez de montar la página sin el recuadro.
