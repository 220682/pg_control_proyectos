# Brief Tanda G — Worker 1 (`qwen3.8-flash`, esfuerzo medio)

**Plan:** `2026-10-02-observaciones-victor-lote-3-plan.md` · **Carril:** rama `local-worker-4`, worktree `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-4` (ya tiene los 9 commits del Lote 3; NO crear ramas ni worktrees, NO tocar `main`).

## Qué hacer (solo esto)

1. **Integrar el modal `NotificacionImpacto`** (componente ya commiteado en `d985d33`, con endpoint `GET /api/cronograma/actividades/[id]/impacto`) en la pantalla del Cronograma: antes de editar una actividad individual cuando el Plan Maestro está aprobado, traer el impacto y mostrar el modal; si el usuario confirma, continuar con el `PATCH` (endpoint ya existe, `77c3ab2`). Respetar el permiso `puedeEditarActividadCronograma` (solo Admin/Jefe de Proyectos).
2. **Verificar el botón "Recalcular PR"** (creado en `7f755df`, endpoint `POST /api/proyectos/[id]/pr/recalcular`): confirmar que aparece en la pantalla del PR y que la llamada responde; si falta el wiring en la pantalla, conectarlo.

## Reglas

- No tocar permisos nuevos ni `middleware.ts`; no aplicar migraciones.
- Archivos esperados: los de la pantalla del Cronograma, el PR, y `NotificacionImpacto` si hace falta adaptarlo. Si necesitas tocar algo del Lienzo del Plan Maestro o RDT, **te detienes y reportas** (eso es Tanda E/F).
- Evidence mínima: `npx tsc --noEmit` exit 0 + `npx vitest run` de las suites que toquen lo afectado + verificación real de las dos funciones contra `npm run dev` local (puerto 3114 del worktree; técnica SSR/API sin navegador del aprendizaje `2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md`, sin secretos en la salida).
- Commit(s) en `local-worker-4` al terminar con mensajes claros. NO merge, NO push a `main`, NO pushear `local-worker-4`.
- Escribe tu cierre en `resultados/G.md` (misma carpeta de briefs): qué hiciste, comandos con salida, capturas/texto de la verificación, hallazgos (mejoras de trabajo / reglas de negocio / observaciones / huérfanos) y pendientes.
