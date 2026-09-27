# Mejora de trabajo — `SendMessage` no alcanza sesiones creadas con `create_session`; usar la rama de git como punto de retoma

> Origen: sesión `local_1.orquestador_cronograma-import-vinculo`, 2026-09-23. Registrado a pedido explícito de Victor.

## Qué pasó

Se interrumpió (`interrupt_session`) un Worker en nube (`session_01Q8CsGMqPhjmfBAcRfw9XNW`, creado con `create_session` de `Claude_Code_Remote`) para poder corregir el nombre de rama/entorno con calma. Cuando se quiso reanudarlo con una instrucción nueva, `SendMessage` falló dos veces (probando `session_id` y luego el título del chat como destinatario) — `ListAgents` mostraba "no other Claude session is running on this machine right now", es decir, no lo veía como agente alcanzable.

Son dos sistemas de herramientas separados que no están conectados en este entorno:

- `Claude_Code_Remote` (`create_session`, `get_session`, `interrupt_session`, etc.) — administra sesiones en la nube, pero no las registra como "agentes alcanzables".
- `SendMessage`/`ListAgents` — mensajería entre pares (subagentes, otras sesiones de Claude que sí se registran ahí).

Una sesión creada con la primera no aparece en la segunda. Al no poder reanudarla, hubo que archivarla (renombrada `hist_...` primero) y crear una sesión nueva, apoyándose en que la rama de git (`local-worker-1`) sí es un punto de verdad compartido entre ambas sesiones — el trabajo ya pusheado (`ed3feac`) no se perdió por eso.

## Regla nueva

1. **No asumir que una sesión creada con `create_session` se puede redirigir después con `SendMessage`.** Verificado hoy: no funciona. Si hace falta reanudarla, no hay forma de mensajearla directamente desde esta sesión.
2. **Antes de interrumpir un Worker en nube con intención de retomarlo después**, evitarlo si no es estrictamente necesario — no hay garantía de poder reanudar esa sesión exacta.
3. **Si de todas formas hay que interrumpir/redirigir**, esperar a que el Worker haya pusheado su avance real a su rama primero (o confirmar que ya lo hizo) — así, si no se puede reanudar la sesión, retomar significa lanzar una sesión nueva con `source_revision` apuntando a esa misma rama (`local-worker-1`), no perder el trabajo.
4. La rama de git es el punto de verdad compartido entre sesiones de Worker, no el historial de chat de una sesión específica — el plan y el estado real de avance deben poder reconstruirse desde ahí (commits + archivo de tarea en `pg_control_proyectos`), nunca depender de que una sesión de chat particular siga viva.
