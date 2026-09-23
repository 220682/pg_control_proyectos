# Plantilla mínima de tarea con Orquestador

> Copiar este archivo como `YYYY-MM-DD-<tema>.md` dentro de `docs/Tareas de implementacion/` al iniciar una tarea nueva con el flujo de Orquestador. Ver `docs/00-sistema/roles-y-flujo.md` y `docs/00-sistema/gestion-de-sesiones-y-contexto.md`.

# <Fecha> — <Título de tarea>

## Estado

Propuesta / Planificando / Implementando / En auditoría / Pendiente de Victor / Cerrada.

## Objetivo

- Resultado esperado:
- Alcance:
- No alcance:
- Validación esperada:

## Entorno

- Modo: local / nube / híbrido.
- Orquestador: chat `<entorno>_1.orquestador_<tarea>`.
- Planner: chat `<entorno>_2.planner_<tarea>`.
- Auditor: chat `<entorno>_4.auditor_<tarea>`.

## Asignaciones

| Rol | Chat | Rama | Worktree | Estado |
| --- | --- | --- | --- | --- |
| Orquestador | `<entorno>_1.orquestador_<tarea>` | `main` | N/A | Activo |
| Planner | `<entorno>_2.planner_<tarea>` | `main` | N/A | Pendiente |
| Worker (fase 1) | `<entorno>_3.worker_<tarea>-fase1` | `work-1` | `.worktrees/work-1` | Pendiente |
| Auditor | `<entorno>_4.auditor_<tarea>` | `main` | N/A | Pendiente |

## Plan aprobado

- [ ] Pendiente de Planner.

## Punch List

- [ ] Pendiente de Planner.

## Registro de decisiones

| # | Fecha | Decisión | Origen | Destino | Estado |
| --- | --- | --- | --- | --- | --- |

## Resultados de Workers

- Rama:
- Commits:
- Pruebas:
- Bloqueos:

## Informe de Auditoría

### Aplicar ahora

### Proponer a Victor

### No promover

## Cierre

- Documentación promovida:
- Pendientes:
- Autorización de cierre:
