# Sesiones, contexto y handoff

## Regla de contexto

- Una sesión = una tarea o una etapa clara de una tarea.
- No mezclar tareas distintas en la misma sesión.
- Al cerrar una tarea, sus sesiones dejan de ser contexto activo y quedan como historial.
- Para una tarea nueva se abre una sesión nueva con contexto limpio. Una sesión histórica no se reutiliza como contexto activo de una tarea nueva.

## Identificar las sesiones

El estándar no depende de nombres de chat ni de una aplicación concreta. El Orquestador lanza cada subagente (Planner, Worker, Auditor, Analista del flujo) y lo identifica por **rol, tarea y tanda** en la descripción con que lo lanza (por ejemplo «Worker F2-A»), de modo que el registro de sesión permita medirlo después. **Lanzar un subagente es autónomo del Orquestador:** no es «crear infraestructura» en el sentido que requiere autorización, es abrir el espacio de trabajo que el plan ya aprobado definió.

## Inicio de cada sesión

El primer mensaje (el brief) debe contener solo:

- Rol.
- Objetivo o subalcance.
- Rama y worktree, si aplica.
- Documentos que debe leer (ver `00-indice.md`).
- Criterios de salida.
- Restricciones.
- Skills que debe usar, si el Orquestador los nombra (ver `04-flujo-sdd-y-planes.md`).

**Skills, antes de empezar.** El brief **nombra** los Skills de la tanda (ver `04-flujo-sdd-y-planes.md`, paso 8) y el agente abre el `SKILL.md` de esos. **No vuelve a listar el contenido de `.claude/skills/`**: la herramienta ya publica en su bloque de Skills la lista disponible, y repetirla son dos llamadas y una lista duplicada por agente, sin valor. Si entre los Skills disponibles hay uno que aplica y el brief no nombró, el agente lo usa y lo anota. Si ninguno aplica, anota en el progreso del plan «Skills revisados: ninguno aplica» con una frase de motivo. Ese es todo el trabajo de Skills que se pide antes de empezar.

## Cierre de cada sesión

Al cerrar una tarea, sus sesiones quedan como historial: no se reutilizan para una tarea nueva y no se borran sin autorización explícita (la misma que exige borrar una rama o un worktree).

## Compactar contexto y relevo del Orquestador

Comprimir o resumir el contexto de una sesión se usa solo si una tarea larga llena demasiado el contexto disponible; no convierte una sesión vieja en contexto válido para una tarea nueva. El Orquestador de un plan largo mide su contexto al terminar cada ola y, si pasa del umbral, hace el relevo con los pasos de `08-medicion-y-relevo.md`. Referencia: los Workers apuntan a 200k o menos; el Orquestador del plan de paneles llegó a 552k y el del plan de niveles y paquetes a 564k. El relevo se hace entre olas, nunca a mitad de una.

**Prompt para el siguiente Orquestador (política desde 2026-09-30, indicada por Victor).** En **cada** cambio de sesión del Orquestador, el saliente termina su último mensaje entregando a Victor el **prompt completo para el Orquestador siguiente**, listo para pegar: cómo trabajar (qué leer, en qué orden y qué no leer), dónde estamos, la primera tarea, las políticas vigentes, cómo hablarle a Victor, qué no hacer y los pendientes con él. El handoff del archivo de progreso es el respaldo; el prompt es la entrega. Un relevo sin prompt no está terminado.

## Handoff obligatorio

Ante cualquier cambio de sesión, LLM o entorno a mitad de una tarea, se escribe un handoff como **sección fechada al final del archivo de progreso** del plan, con la plantilla `06-plantillas/07-handoff.md`: objetivo y estado, plan/progreso/evidencia relacionados, rama/worktree y último commit, terminado y no terminado, pruebas ejecutadas, bloqueos y riesgos, qué debe leer el siguiente agente, y el próximo paso concreto.

## Planes grandes en tandas

Un plan de más de unos 15 ítems, o de una fase completa, se reparte en tandas de 4 a 8 ítems:

- Un Worker nuevo por tanda, con un brief de 8 KB como máximo y un tope de unas 80 llamadas.
- El Worker lee solo lo que el brief nombra (busca por ID en vez de leer el plan completo).
- Cada tanda se marca en el índice de tandas como **paralelizable** (documentación o código puro, sin navegador) o **usa el navegador** (se ejecutan una a una: dos tandas con navegador nunca corren a la vez).
- Se mide cada sesión (llamadas, contexto máximo, caché leída) y se guarda en un archivo de medición.
- Antes de declarar terminada su tanda, cada Worker entrega al Orquestador su resumen de cierre en un archivo propio por tanda (plantilla `06-plantillas/12-resumen-de-cierre-de-tanda.md`: estado de sus ítems, evidencia y hallazgos) y no edita los archivos compartidos del plan. El Orquestador pasa los hallazgos al **libro de hallazgos del plan** (los cuatro apartados de `02-plan.md`) a medida que llegan; al terminar la última fase, el Documentador traslada cada fila a su destino final (flujos de negocio, aprendizaje continuo, evidencia) según `02-roles-y-delegacion.md`.
- **Manejo de los hallazgos de cada Worker.** El resumen de cierre tiene secciones fijas: estado de los ítems de la tanda con su evidencia; hallazgos clasificados en cinco grupos (mejora de trabajo, regla de negocio acordada, observación sobre la política, archivo o carpeta huérfano, conflicto con un flujo o pregunta para el Responsable humano); traspaso; llamadas y contexto usado; y «Skills revisados». Una pregunta de negocio o un conflicto con un flujo **no espera al cierre**: el Worker se detiene, se la devuelve al Orquestador en el momento y la registra con la respuesta. Ningún Worker borra nada por su cuenta.

## Límite conocido: mensajería entre sesiones

> Aprendizaje promovido: una sesión de Worker se interrumpió pensando en retomarla más tarde con una herramienta de mensajería entre sesiones, y esa herramienta no pudo alcanzarla — la sesión había sido creada con otro mecanismo (de administración de sesiones en la nube) que no la registra como "agente alcanzable" por la mensajería entre pares.

1. No asumir que una sesión creada con una herramienta de administración de sesiones remotas se puede redirigir después con una herramienta de mensajería entre agentes — son sistemas distintos y una sesión creada con la primera puede no aparecer en la segunda. Verificar con la herramienta de listado de agentes antes de asumir que se puede retomar.
2. Antes de interrumpir un Worker con intención de retomarlo después, evitarlo si no es estrictamente necesario — no hay garantía de poder reanudar esa sesión exacta.
3. Si de todas formas hay que interrumpir o redirigir, esperar a que el Worker haya pusheado su avance real a su rama primero (o confirmar que ya lo hizo): así, si la sesión no se puede reanudar, retomar significa lanzar una sesión nueva apuntando a esa misma rama, sin perder el trabajo.
4. **La rama de git (o el sistema de control de versiones que use el repositorio de código) es el punto de verdad compartido entre sesiones de Worker, no el historial de conversación de una sesión específica.** El plan y el estado real de avance deben poder reconstruirse desde ahí (commits + archivo de plan en el repositorio de documentación), nunca depender de que una sesión de chat particular siga viva.
