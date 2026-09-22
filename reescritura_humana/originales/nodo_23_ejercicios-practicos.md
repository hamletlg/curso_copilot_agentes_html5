## Ejercicios prácticos

Cuatro ejercicios para aplicar lo aprendido. Cada uno lleva su respuesta comentada: la idea es responder **antes** de leerla.

---

### Ejercicio 1: identifica el entorno o el tipo de herramienta

Para cada situación, indica con qué estás trabajando:

**Tabla de claves:**

| Clave | Significa |
|---|---|
| **W** | Herramienta web o asistente general, sin acceso a los datos internos |
| **A** | Agente de Copilot de Trabajo, que actúa sobre datos y herramientas de la organización |

1. Le pides a un asistente web que redacte un correo de presentación para un cliente.
2. Le dices a Copilot de Trabajo que revise tu calendario, busque un hueco libre y envíe la invitación al equipo de marketing.
3. Usas un generador de imágenes web para crear un logotipo a partir de una descripción.
4. Le pides a Copilot de Trabajo que lea las reseñas de clientes en SharePoint, detecte las quejas más frecuentes y te las resuma.
5. Un agente vigila las ventas en Excel y te avisa cuando un producto baja del mínimo de stock.

**Respuestas:** 1-W, 2-A, 3-W, 4-A, 5-A. Criterio: **¿la herramienta toca datos de tu organización?** Si no, es W; si sí, es A. Y en el caso W, la pregunta siguiente es la que importa: ¿está autorizada esa herramienta para el trabajo?

---

### Ejercicio 2: mejora las instrucciones

Reescribe cada instrucción para que sea específica, con contexto, formato y audiencia.

1. «Haz un resumen del informe.»
2. «Analiza los datos de clientes.»
3. «Escribe sobre seguridad.»

**Respuesta comentada (ojo a los cuatro elementos):**

- *«Prepara un resumen de una página del informe de ventas del segundo trimestre, en tres apartados: cifra global, regiones que crecen y riesgos. Audiencia: dirección.»*
- *«Analiza el archivo Ventas_Q2.xlsx y dime qué tres productos crecen más del 10 % respecto al mismo trimestre del año anterior. Devuélvemelo en una tabla con producto, porcentaje y tendencia.»*
- *«Escribe un texto de 150 palabras sobre contraseñas y doble factor dirigido a compañeros no técnicos, con tono cercano y tres recomendaciones prácticas.»*

Lo que cambia en las tres: **objetivo concreto, fuente**, **formato de salida** y **destinatario**. Sin los cuatro, el resultado se parece a lo que querías pero no sirve.

---

### Ejercicio 3: análisis de riesgos

Clasifica cada situación como **ALTO** (no usar sin autorización), **MEDIO** (usar con precaución y revisar) o **BAJO** (uso aceptable).

1. Enviar nombres y teléfonos de clientes a un asistente web para que los ordene.
2. Pedir a Copilot de Trabajo que resuma un artículo interno para la reunión del equipo.
3. Generar ideas para una campaña de marketing.
4. Conectar un agente al sistema de nóminas para que actualice datos de empleados.
5. Redactar con Copilot en Word un borrador de correo para un cliente externo.

**Respuestas comentadas:**

1. **ALTO.** Datos personales de terceros en una herramienta que no controla la empresa.
2. **MEDIO.** El contenido es interno, pero el resumen puede tener imprecisiones: se revisa antes de usarlo.
3. **BAJO.** No hay datos sensibles y el resultado lo valida el equipo.
4. **ALTO.** Nóminas es información especialmente sensible: solo el personal autorizado y en el sistema oficial.
5. **MEDIO.** El borrador sirve, pero se revisa tono, precisión y datos antes de enviarlo.

---

### Ejercicio 4: caso práctico completo

Trabajas en una oficina de diez personas que usa Microsoft 365 para todo: correo, documentos, hojas de cálculo y reuniones. Tu responsable te pide reducir el tiempo que el equipo dedica a tareas repetitivas.

1. **Identifica tres tareas repetitivas** que podrían hacerse mejor con Copilot.
2. **Para cada una, escribe una instrucción** aplicando los cuatro elementos (objetivo, fuente, formato, audiencia).
3. **Señala dos riesgos** y qué harías para reducirlos.
4. **Di qué harías con la información** que aparezca de más (un documento que no deberías haber visto, un dato personal que no hacía falta).

**Respuesta comentada (una posible solución):**

- *Tareas:* preparar el acta de la reunión semanal; resumir el hilo de correos de un cliente antes de responder; pasar las notas de una visita a un documento de seguimiento.
- *Instrucción de ejemplo:* «Resume este hilo de correo en cinco puntos y redacta una respuesta de 80 palabras confirmando la reunión del jueves. Tono profesional. Muéstrame el borrador antes de enviarlo.»
- *Riesgos:* (1) que Copilot muestre documentos con permisos mal puestos —se reduce revisando permisos de lo sensible; (2) que un borrador se envíe sin revisar —se reduce con la regla «nada sale sin leerlo una persona» y con instrucciones que piden el borrador antes del envío.
- *Si aparece información de más:* no usarla, no reenviarla y comunicarlo por el canal de incidentes (Nodo 19). Que se vea algo que no correspondía es precisamente la señal de que hay permisos que hay que corregir.
