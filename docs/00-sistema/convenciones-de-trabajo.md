# Convenciones de trabajo

> Origen: aprobado por Victor en Fase 1 de `docs/Tareas de implementacion/2026-09-22-plan-unico-orquestador-sesiones-worktrees-Claude-y-local.md`. Estas convenciones se reutilizan en tareas futuras salvo cambio explícito de Victor.

## Entorno por defecto

- Modo: híbrido — local o nube, según disponibilidad y necesidad de cada tarea.
- Ejecución del flujo: Claude (app de escritorio o web).
- VS Code: revisión de archivos, no gestión de chats/sesiones.
- App/web de Claude: visualización de chats, historial y cambio manual de nombre.

## Pool de ramas

- Rama integrada: `main`.
- **Nomenclatura (corregida 2026-09-23):** `<entorno>-worker-<N>` — el mismo criterio que los nombres de chat: entorno seguido de quién la usa. `entorno` es `local` o `nube` (según qué entorno de Victor esté corriendo la sesión — verificar con `list_environments`, no asumir). Ejemplo: `local-worker-1`, `local-worker-2`, `nube-worker-1`.
- Ramas de trabajo persistentes: `local-worker-1`, `local-worker-2` (pool de hoy; se agregan `nube-worker-N` si se trabaja desde el entorno `nube`).
- Las ramas `<entorno>-worker-N` no se borran por rutina; se reutilizan después de sincronizarlas con `main` y verificar que no contengan trabajo pendiente.
- Los Workers trabajan siempre en su rama `<entorno>-worker-N` propia. El resto de roles (Orquestador, Planner, Auditor) trabaja directo en `main`, salvo que Victor pida lo contrario para una tarea puntual.

## Worktrees

- Ubicación aprobada: `.worktrees/` dentro del repositorio (excluida de Git vía `.gitignore`).
- Cada worktree corresponde a una rama `work-N`.
- No se crea ni elimina un worktree sin autorización explícita de Victor.

## Estado actual del pool (creado 2026-09-23)

| Rama | Worktree | Estado |
| --- | --- | --- |
| `work-1` | `.worktrees/work-1` | Libre |
| `work-2` | `.worktrees/work-2` | Libre |

## Commits durante la implementación

> Corregido el 2026-09-23 (Victor) — la práctica anterior era un commit por cada ítem de la Punch List; eso no va.

- **No** un commit por cada ítem de la Punch List.
- Commitear aproximadamente **cada 35% de avance acumulado** de la Punch List de la tarea.
- El commit se hace **solo al terminar completo** el ítem de checklist en curso — nunca a medias de un ítem, aunque eso implique pasar el 35% antes de commitear.
- Aplica tanto en `pg_control_proyectos` (documentación) como en `py_control_proyectos_web` (código), salvo que Victor indique otra cosa para una tarea puntual.

## Chats

- Un chat corresponde a una tarea o etapa clara.
- No se reutiliza un chat de una tarea cerrada para una tarea nueva.
- Al cerrar una tarea, se antepone el prefijo `hist_` al nombre del chat: señala que la tarea terminó y que el rol/entorno queda libre para la siguiente.
- **Los chats no se borran, se renombran.** Ningún agente elimina un chat/sesión por su cuenta — un chat cerrado queda como historial (`hist_...`) indefinidamente, igual que una tarea cerrada en `Tareas de implementacion/` no se borra. Eliminar un chat requiere la misma autorización explícita que eliminar una rama o un worktree.
- Crear un chat nuevo (Worker, Planner, Auditor) sí es autónomo del Orquestador — no es "crear infraestructura" en el sentido que requiere preguntar, es abrir el espacio de trabajo que el plan aprobado ya definió.
- La nomenclatura completa de chats (distinción local/nube, jerarquía de roles) se define en `docs/00-sistema/gestion-de-sesiones-y-contexto.md`.
