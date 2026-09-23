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

## Mejoras (de trabajo)

> **Se escribe en el momento en que ocurre**, no al cerrar la tarea — es un registro en vivo, igual que el Registro de decisiones. Aprendizajes sobre **cómo trabajamos** (método, herramientas, workarounds) encontrados durante la ejecución — no reglas del sistema. Al cerrar, cada entrada ya escrita aquí se traslada a `docs/Mejoras continuas/` (no se redacta recién al final). "Ninguna identificada" si no aplica.

- <Fecha/momento> — <Aprendizaje> → trasladado a `docs/Mejoras continuas/<archivo>.md`.

## Reglas de negocio acordadas en esta tarea

> **Se escribe en el momento en que ocurre.** Reglas del sistema (cómo se calcula/valida/comporta algo) encontradas o confirmadas durante la ejecución — van **directo al Flujo de trabajo correspondiente** al cerrar, integradas en su estructura (no como nota aparte). "Ninguna nueva" si no aplica.
>
> **Si la regla nueva contradice una ya escrita en un flujo** (conflicto detectado durante la ejecución, no anticipado por el Planner al armar el plan):
> 1. El agente **pregunta a Victor en el momento** — no sigue implementando con el conflicto sin resolver ni espera al cierre.
> 2. Victor responde.
> 3. El agente **valida** la respuesta (¿resuelve el conflicto de forma coherente?).
> 4. Si valida: **primero escribe la decisión aquí** (en este apartado, en el momento), **luego continúa** con la implementación.
> 5. Si no valida: repite el ciclo (vuelve a preguntar a Victor) hasta que quede resuelto — no se avanza con una regla contradictoria sin resolver.

- <Fecha/momento> — <Regla> → aplicada en `docs/Flujos de trabajo/NN-*.md`. (Si hubo conflicto: <regla anterior> vs <regla nueva> → resuelto con Victor: <decisión>.)

## Carpetas/archivos huérfanos

> **Se escribe en el momento en que se detecta**, con búsqueda real (Grep/referencias — nunca por memoria, ver AGENTS.md), en **ambos repositorios** (`pg_control_proyectos` y `py_control_proyectos_web`). Con fin de limpieza — el agente no borra nada por su cuenta, solo reporta; Victor decide. "Ninguno encontrado" si no aplica.

- <Fecha/momento> — <Archivo/carpeta> (`<repositorio>`) → por qué se sospecha huérfano, verificado con `grep`/búsqueda de referencias → **Acción:** reportado a Victor, pendiente de decisión / autorizado a eliminar / se conserva.

## Cierre

- Documentación promovida:
- Pendientes:
- Autorización de cierre:
