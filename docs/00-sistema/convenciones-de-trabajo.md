# Convenciones de trabajo

> Origen: aprobado por Victor en Fase 1 de `docs/Tareas de implementacion/2026-09-22-plan-unico-orquestador-sesiones-worktrees-Claude-y-local.md`. Estas convenciones se reutilizan en tareas futuras salvo cambio explícito de Victor.

## Entorno por defecto

- Modo: híbrido — local o nube, según disponibilidad y necesidad de cada tarea.
- Ejecución del flujo: Claude (app de escritorio o web).
- VS Code: revisión de archivos, no gestión de chats/sesiones.
- App/web de Claude: visualización de chats, historial y cambio manual de nombre.

## Pool de ramas

- Rama integrada: `main`.
- Ramas de trabajo persistentes: `work-1`, `work-2`.
- Las ramas `work-N` no se borran por rutina; se reutilizan después de sincronizarlas con `main` y verificar que no contengan trabajo pendiente.
- Los Workers trabajan siempre en su rama `work-N` propia. El resto de roles (Orquestador, Planner, Auditor) trabaja directo en `main`, salvo que Victor pida lo contrario para una tarea puntual.

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
- La nomenclatura completa de chats (distinción local/nube, jerarquía de roles) se define en `docs/00-sistema/gestion-de-sesiones-y-contexto.md`.
