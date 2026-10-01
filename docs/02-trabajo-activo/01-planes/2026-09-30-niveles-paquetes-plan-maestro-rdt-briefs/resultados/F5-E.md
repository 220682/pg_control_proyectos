# F5-E — Aprobar versión nueva del Plan Maestro (corrección corta)

## Estado
- Ítem único: **Conforme**. `PATCH /api/plan-maestro` con `accion: APROBAR`, cuando existe otra versión APROBADA del mismo proyecto, exige `puedeCrearVersionPlanMaestro` (administrador y jefe de proyectos); si no, 403 «No autorizado: solo el administrador y el jefe de proyectos aprueban una versión nueva que reemplaza una aprobada». La comprobación va justo tras el alcance del plan y antes de cualquier escritura (también antes de guardar disciplinas). La primera aprobación y GUARDAR_ASIGNACIONES siguen con `puedeGestionarPlanMaestro`.
- Commit en `local-worker-1`: `caab04f` (route.ts y plan-maestro-api.test.ts). Sin push, sin migraciones, sin navegador.

## Evidencia
- `npx vitest run src/lib/plan-maestro src/app/api/plan-maestro src/lib/permisos`: 12 archivos, 244 pruebas verdes.
- `npx tsc --noEmit`: sin errores. `npx eslint src/app/api/plan-maestro`: sin problemas.
- Pruebas nuevas (describe «aprobar una versión nueva»): planner 403 sin ninguna escritura; administrador y jefe de proyectos 200 y reemplaza la anterior; guardar asignaciones sigue permitido al planner; primera aprobación del planner sin cambio. Las pruebas existentes del PATCH con una aprobada (pm0) ahora usan administrador.

## Handoff
- Pendiente para el Orquestador/F5-D: reflejar la regla en flujo 20 (Plan Maestro), flujo 14 y la Matriz de permisos (aprobar versión nueva = solo administrador y jefe de proyectos; planner solo la primera aprobación). No lo edité (no es mío).
- Posible ajuste de interfaz: el botón Aprobar del planner con una aprobada vigente devolverá 403; la UI no se tocó.

## Mejoras de trabajo / reglas de negocio / huérfanos
- Regla de negocio (decidida por Victor): aprobar un borrador que reemplaza una aprobada es solo administrador y jefe de proyectos, igual que crearlo.
- Mejoras: ninguna. Huérfanos: ninguno.

## Skills revisados
- `cerrar-tanda` aplicado (adaptado). El repositorio de la app no tiene carpeta `.claude/skills`; `verificar-permisos-por-rol` no aplica (sin navegador; cubierto por pruebas de rol).

## Llamadas
- ~10.
