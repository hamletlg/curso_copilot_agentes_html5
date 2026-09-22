## Lo que hemos aprendido

**En la parte 1 (fundamentos) hemos descubierto:**

1. La IA no posee conocimiento real; calcula probabilidades basadas en patrones de datos. Debido a este funcionamiento, puede generar datos falsos con apariencia de veracidad.
2. Un agente de IA planifica y ejecuta tareas utilizando las herramientas de tu entorno, además de generar respuestas.
3. Copilot opera en dos entornos: **Copilot Web** (general, sin acceso a los datos de la organización) y **Copilot de Trabajo** o Microsoft 365 Copilot (conectado a los datos internos a través de Microsoft Graph).
4. La IA de Microsoft se organiza en tres niveles: **1) Copilot Asistente** (chatbot estándar, reactivo); **2) agentes especializados** (declarativos, con un rol y una base de conocimiento limitada); **3) agentes avanzados** de Copilot Studio (proactivos, capaces de ejecutar acciones y automatizar flujos).
5. Microsoft ofrece agentes especializados ya preparados (Researcher, Analyst y Facilitator) y agentes avanzados (Cowork). También puedes crear los tuyos con Agent Builder.
6. El funcionamiento de un agente sigue un ciclo de 5 pasos: recibir, planificar, ejecutar, verificar y entregar.

**En la parte 2 (aplicaciones) hemos visto:**

7. Copilot se integra en Word, Excel, PowerPoint, Outlook, Teams, SharePoint y Loop para casos de uso prácticos.
8. Para obtener resultados precisos es necesario escribir instrucciones claras. Especifica el contexto, define el formato y señala a quién va dirigido el contenido.
9. Tu organización utiliza IA en diversos puntos: existen funciones activas en Microsoft 365 y herramientas no autorizadas (shadow AI) que también forman parte de la responsabilidad de la empresa.

**En la parte 3 (uso responsable) hemos aprendido:**

10. Verifica siempre los resultados. Los asistentes pueden generar datos falsos (alucinaciones) y reproducir sesgos.
11. Copilot utiliza los permisos actuales del usuario. La **sobreexposición** de SharePoint es el riesgo de confidencialidad más común en el entorno de oficina.
12. Sigue la política de la empresa y el protocolo de incidentes: para, no borres, avisa, corrige y registra el suceso.

**En la parte 4 (marco legal) hemos entendido:**

13. Tu empresa es **responsable del despliegue** al usar IA en su actividad. El **Artículo 4** del AI Act exige la formación de las personas que la utilizan.
14. Esta obligación es de **medios**: la formación debe ser real, adecuada al riesgo y **demostrable** mediante evidencias conservadas.
15. Al interactuar con un asistente se tratan **datos personales**. Se aplica el RGPD, donde la empresa actúa como responsable y el proveedor como encargado del tratamiento.
16. Las decisiones que afectan a personas requieren **supervisión humana**. Es necesario poder explicar qué acción se realizó y por qué.

**Recuerda:** La IA es una herramienta para mejorar la eficiencia. La responsabilidad sobre el uso y las decisiones derivadas de ella recae en el usuario.

---

## Glosario

**AESIA:** Agencia Española de Supervisión de la Inteligencia Artificial, la autoridad que vigila el cumplimiento del AI Act en España.
**Agent Builder:** herramienta incluida en Copilot de Trabajo para crear agentes especializados sin necesidad de programar.
**Agente de IA:** componente de software que identifica un objetivo, planifica los pasos necesarios, usa herramientas y ejecuta tareas sobre los sistemas conectados, según el grado de autonomía configurado.
**Agentes avanzados (Copilot Studio):** nivel 3. Agentes proactivos: ejecutan acciones, se conectan a servicios y API externos y automatizan flujos mediante disparadores (triggers).
**Agentes especializados (declarativos):** nivel 2. Agentes con un rol concreto y una base de conocimiento acotada. Se crean sin programar con Agent Builder.
**AI Act:** Reglamento (UE) 2024/1689, la norma europea que regula los sistemas de IA por niveles de riesgo. Su Artículo 4 obliga a proveedores y responsables del despliegue a garantizar la alfabetización en IA de su personal.
**Alucinación:** cuando un sistema de IA genera información que parece correcta pero es falsa.
**Analyst:** agente predefinido de Microsoft para análisis de datos y visualización desde Excel.
**Copilot Asistente (chatbot estándar):** nivel 1. Asistente conversacional y reactivo: espera tu instrucción, responde y se detiene; no ejecuta acciones sobre tus sistemas.
**Copilot de Trabajo (Microsoft 365 Copilot):** entorno corporativo de Copilot, conectado a los datos internos de la organización a través de Microsoft Graph. Puede actuar como asistente y como agente.
**Copilot Studio:** plataforma avanzada para crear agentes empresariales con integraciones complejas y flujos de varios pasos.
**Copilot Web (Modo Web):** entorno general de Copilot, basado en búsqueda web y sin acceso a Microsoft Graph; trabaja solo con lo que le aportas y se comporta como asistente conversacional (nivel 1).
**Cowork:** agente avanzado de Copilot que ejecuta tareas complejas de varios pasos en segundo plano, con puntos de aprobación.
**Datos personales:** cualquier información sobre una persona identificada o identificable. Los de salud, ideología, religión, origen étnico u orientación sexual reciben protección especial.
**Encargado del tratamiento:** quien trata datos personales por cuenta de otra organización (por ejemplo, el proveedor del servicio de IA). No decide para qué se tratan.
**Facilitator:** agente predefinido de Microsoft para gestión y resúmenes de reuniones de Teams.
**IA generativa:** IA que crea contenido nuevo (texto, imagen, audio, código) en lugar de limitarse a clasificar o predecir.
**Microsoft Graph:** motor de datos de Microsoft 365 que permite a Copilot acceder a tus correos, archivos, reuniones y chats de forma segura.
**Modelo de lenguaje (LLM):** sistema entrenado con grandes cantidades de texto que calcula qué palabra es más probable a continuación; el motor de la IA generativa de texto.
**Permisos heredados:** Copilot no concede accesos nuevos: muestra lo que los permisos existentes ya permitían ver.
**Prompt:** instrucción que le das a un asistente o agente para que realice una tarea.
**RAG (Retrieval-Augmented Generation):** técnica que permite a Copilot buscar información en tus archivos corporativos para responder con datos actualizados.
**Researcher:** agente predefinido de Microsoft para investigaciones profundas con fuentes citadas.
**Responsable del despliegue (deployer):** la organización o persona que usa un sistema de IA en su actividad profesional. Es quien tiene la obligación de alfabetización del Artículo 4.
**RGPD:** Reglamento (UE) 2016/679, de protección de datos personales, aplicable siempre que en un prompt aparezcan datos de personas.
**Sesgo:** patrón de prejuicio presente en los datos de entrenamiento que el sistema reproduce en sus respuestas.
**Shadow AI:** uso de herramientas de IA por cuenta propia, sin autorización ni conocimiento de la organización.
**Sobreexposición (oversharing):** información accesible a más personas de las que debería. En Microsoft 365, el efecto más visible es que Copilot muestre a alguien un documento que no le correspondía.
**Supervisión humana:** intervención de una persona con capacidad real de revisar, corregir o detener lo que hace el sistema. La exige el AI Act para las decisiones que afectan a personas.

---

## ¿Quieres seguir aprendiendo?

**Recursos recomendados:**
- [Documentación oficial de Microsoft Copilot](https://learn.microsoft.com/es-es/copilot/)
- [Guía de Agent Builder](https://learn.microsoft.com/es-es/microsoft-365-copilot/extensibility/agent-builder)
- [Texto oficial del AI Act (EUR-Lex)](https://eur-lex.europa.eu/legal-content/ES/TXT/?uri=CELEX:32024R1689)
- [AESIA — Agencia Española de Supervisión de la IA](https://aesia.digital.gob.es/)
- [Agencia Española de Protección de Datos](https://www.aepd.es/)

**Preguntas frecuentes:**
- ¿Necesito saber programar para usar Copilot? No. La mayoría de las funcionalidades funcionan mediante lenguaje natural.
- ¿Puede Copilot reemplazarme? No. Es una herramienta para realizar tareas; la decisión y la responsabilidad siguen siendo humanas.
- ¿Qué pasa con mis datos? Copilot de Trabajo se rige por las mismas políticas de seguridad y protección de datos que el resto de Microsoft 365 de tu organización. Además, tú eres el primer filtro: la política de la empresa determina qué se puede escribir y qué no.
- ¿Y si uso una IA que no está autorizada? La responsabilidad recae en la empresa, no solo en ti: solicita autorización o utiliza las herramientas autorizadas.

**Contacto:**
Para dudas sobre este curso, contacta con el equipo de formación de tu organización.
