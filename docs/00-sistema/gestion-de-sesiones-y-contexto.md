# Gestión de sesiones y contexto

> Origen: aprobado por Victor en Fase 3 de `docs/Mejoras continuas/2026-09-22-plan-unico-orquestador-sesiones-worktrees-Claude-y-local.md`.

## Dónde se trabaja

- Claude (app de escritorio o web): ejecución del flujo completo, tanto local como nube.
- VS Code: revisión de planes y documentos; no administración de chats/sesiones.
- App/web de Claude: visualización de chats, historial y renombrado manual de chats.

## Regla de contexto

- Un chat = una tarea o etapa clara de una tarea.
- No mezclar tareas distintas en el mismo chat.
- Al cerrar una tarea, sus chats dejan de ser contexto activo y quedan como historial.
- Para una tarea nueva se abre un chat nuevo con contexto limpio.

## Nombres de chats

Los chats locales y los de la nube conviven en el mismo apartado de la app (se agrupan por repositorio), por lo que el nombre debe distinguir entorno y ordenar los roles por jerarquía.

Patrón:

```text
<entorno>_<jerarquía>.<rol>_<tarea>
```

- `entorno`: `local` o `nube`.
- `jerarquía`: número fijo por rol, para que el listado de chats quede ordenado.
  - `1` → Orquestador
  - `2` → Planner
  - `3` → Worker
  - `4` → Auditor
- `tarea`: slug corto de la tarea (ej. `dashboard-fase4`, `curva-s`).
- Orquestador, Planner y Auditor llevan solo el nombre de la tarea.
- Si hay más de un Worker en la misma tarea, se diferencian por fase de esa tarea, no por número de worker:

```text
<tarea>-fase1
<tarea>-fase2
```

Ejemplo completo:

```text
local_1.orquestador_dashboard-fase4
local_2.planner_dashboard-fase4
local_3.worker_dashboard-fase4-fase1
local_3.worker_dashboard-fase4-fase2
local_4.auditor_dashboard-fase4

nube_1.orquestador_curva-s-fase3
```

## Inicio de cada chat

El primer mensaje debe contener solo:

- Rol.
- Objetivo/subalcance.
- Rama y worktree, si aplica.
- Documentos que debe leer.
- Criterios de salida.
- Restricciones.

## Cierre de cada chat

Al cerrar una tarea, se antepone el prefijo `hist_` al nombre del chat: señala que la tarea terminó y que el rol/entorno queda libre para la siguiente.

```text
hist_local_1.orquestador_dashboard-fase4
```

No se reutiliza un chat histórico (`hist_...`) para una tarea nueva.

## /compact

Puede usarse solo si una tarea larga llena demasiado el contexto. No convierte un chat viejo en contexto válido para una tarea nueva.
