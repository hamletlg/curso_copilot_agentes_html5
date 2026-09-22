### El riesgo principal en una oficina con Microsoft 365

Copilot de Trabajo no añade permisos nuevos: **usa los que ya existen**. Si un documento está al alcance de todo el equipo, Copilot lo mostrará a todos los usuarios. Si el documento está mal compartido, el asistente facilita que alguien acceda a la información **sin saber que no tenía autorización**.

Este fenómeno se denomina **sobreexposición** (oversharing). Se produce cuando la información es más accesible de lo que la organización prevé. No se trata de un ataque externo, sino del resultado de compartir carpetas de forma apresurada durante años.

### Cómo se produce, en la vida real

- Un sitio de SharePoint con el permiso por defecto **«Todos excepto usuarios externos»**: cualquier persona interna puede ver todo el contenido, incluso información de dirección.
- Un **enlace de uso compartido** creado para una urgencia que sigue activo y sin fecha de caducidad.
- Documentos sensibles en la carpeta general de un equipo: nóminas, tarifas de proveedores, ofertas, expedientes de clientes o borradores de despidos.
- Un sitio antiguo de un proyecto finalizado que permanece con los permisos abiertos.

Con Copilot, cualquier usuario puede escribir *«resume los datos de personal del último trimestre»* y obtener información que antes solo era accesible si alguien buscaba el archivo exacto.

### Qué se hace con esto

- **Revisar los permisos de los datos sensibles.** No guardes nóminas, datos de clientes, precios o contratos en carpetas abiertas por comodidad.
- **Verificar los enlaces compartidos.** Asegúrate de que lo que compartiste "temporalmente" tenga una fecha de caducidad o esté cerrado.
- **Usar las etiquetas de confidencialidad** de la organización: estas marcan el documento y se mantienen durante su uso.
- **Consultar antes de crear un agente.** Un agente hereda los permisos de las fuentes conectadas. Si le das acceso a una carpeta abierta, el agente mostrará esa información a cualquier usuario.
- **Identificar a quién avisar.** Un documento expuesto no es un problema técnico: es un incidente que debe comunicarse (Nodo 19).

### Y de nuevo el shadow AI

La sobreexposición es un problema interno, pero comparte origen con el *shadow AI*: **información que circula más de lo previsto**. En ambos casos, la regla es la misma: antes de pegar, subir o compartir contenido, piensa si esa información debería estar disponible para quien la reciba.

> **Aviso:** Copilot no decide qué mostrar. El sistema reproduce lo que los permisos permiten. Si aparece información que no deberías ver, el problema es el permiso y no el asistente. Debes reportarlo.
