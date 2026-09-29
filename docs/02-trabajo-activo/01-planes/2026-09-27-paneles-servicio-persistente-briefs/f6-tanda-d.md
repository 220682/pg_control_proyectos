# F6-D · Regresión: consola, sin servicio, flujos con chips y navegación móvil

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F6 · **Depende de:** F6-C cerrada.
**Punto de commit:** Solo si hay correcciones.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-68 | Recorrido completo (PL-02 a PL-13 con ambas cuentas): sin errores nuevos en la consola del navegador respecto de la línea base | Registro de consola |
| PL-77 | Sin servicio, todas las pantallas se comportan como en la línea base de F0 (mismos destinos y estados) | Comparación con F0 |
| PL-78 | Flujos que usan chips siguen intactos (sin guardar datos): Crear RQ abre desde Mi entorno, filtros de Status de Requerimiento, selector y carga del Consolidado RDTs, Plan Maestro y Cronograma abren con y sin servicio | Capturas |
| PL-80 | Navegación móvil y escritorio: el pie, "Ver como" y los cajones se comportan como en la línea base | Capturas |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- **PL-68:** recorrido de PL-02 a PL-13 con ambas cuentas: sin errores nuevos en la consola del navegador respecto de la línea base (`browser_console_messages` filtrando errores; compara con lo anotado en F0-B).
- **PL-77:** sin servicio, todas las pantallas se comportan como en la línea base LB-03 (mismos destinos y estados).
- **PL-78:** flujos que usan chips intactos, sin guardar datos: Crear RQ abre desde Mi entorno, filtros de Status de Requerimiento, selector y carga del Consolidado RDTs, Plan Maestro y Cronograma abren con y sin servicio.
- **PL-80:** navegación móvil (390 px) y escritorio: el pie, «Ver como» y los cajones se comportan como en la línea base (LB-02).
- Una captura por ítem como máximo; el resto por `browser_snapshot` y `browser_evaluate`.

## Qué NO hacer

- No escribas datos.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
