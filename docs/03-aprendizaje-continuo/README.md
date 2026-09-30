# Aprendizaje continuo

## Qué vive acá

Aprendizajes que nacen de la ejecución de planes: cada uno con origen, evidencia, clasificación y destino propuesto (basado en `08-aprendizaje.md`). El índice de abajo etiqueta cada mejora por categoría, para que cualquier rol escanee rápido y abra solo la que aplica a lo que está por hacer — nunca la carpeta completa por defecto.

`pendientes-de-promocion.md` lista lo que espera aprobación. `historico.md` registra lo ya promovido, rechazado, reemplazado o cerrado.

Cuando un procedimiento reusable **se repite**, el Auditor puede proponer convertirlo en un Skill real de Claude Code (`.claude/skills/`), redactado de forma agnóstica para ser copiable a otros repositorios.

## Qué no vive acá

Ni planes futuros ni tareas operativas completas — eso vive en `../02-trabajo-activo/`.

## Índice por categoría

Rehecho en la Fase 5 de la reestructuración documental (2026-09-27), una fila por archivo, con su etiqueta y su estado final (ver clasificación completa en `historico.md` y `pendientes-de-promocion.md`).

| Etiqueta | Archivo | Estado |
|---|---|---|
| `roles/orquestador` | [`2026-09-23-orquestador-salta-flujo-de-roles-sin-auditoria.md`](2026-09-23-orquestador-salta-flujo-de-roles-sin-auditoria.md) | Histórico — ya promovido a `00-estandar-agentes/02-roles-y-delegacion.md` |
| `roles/orquestador` | [`2026-09-23-preguntas-frecuentes-flujo-orquestador.md`](2026-09-23-preguntas-frecuentes-flujo-orquestador.md) | Histórico con rastro visible en el estándar |
| `sesiones/chat` | [`2026-09-23-sendmessage-no-alcanza-sesiones-create-session.md`](2026-09-23-sendmessage-no-alcanza-sesiones-create-session.md) | Promovido a `00-estandar-agentes/03-sesiones-contexto-y-handoff.md` |
| `entorno/infra` | [`2026-09-21-acceso-postgres-sin-ipv6.md`](2026-09-21-acceso-postgres-sin-ipv6.md) | Histórico (excepción cerrada) |
| `entorno/infra` | [`2026-09-23-red-bloqueada-impide-autonomia-real.md`](2026-09-23-red-bloqueada-impide-autonomia-real.md) | Pendiente de promoción — ver `pendientes-de-promocion.md` |
| `migraciones-sql` | [`2026-09-21-migraciones-sql-sobrecargas-huerfanas.md`](2026-09-21-migraciones-sql-sobrecargas-huerfanas.md) | No promovido — se queda como aprendizaje |
| `playwright` | [`2026-09-21-verificacion-playwright-falsos-negativos.md`](2026-09-21-verificacion-playwright-falsos-negativos.md) | Promovido a `01-contexto-repositorio/04-pruebas-y-evidencia.md` |
| `lint` | [`2026-09-23-eslint-baseline-vs-cero.md`](2026-09-23-eslint-baseline-vs-cero.md) | Promovido a `01-contexto-repositorio/04-pruebas-y-evidencia.md` |
| `tests` | [`2026-09-23-tests-contadores-congelados.md`](2026-09-23-tests-contadores-congelados.md) | Promovido a `01-contexto-repositorio/04-pruebas-y-evidencia.md` |
| `worktrees/turbopack` | [`2026-09-23-turbopack-worktree-junction.md`](2026-09-23-turbopack-worktree-junction.md) | Promovido a `01-contexto-repositorio/03-entorno-git-y-worktrees.md` |
| `principios` | [`2026-09-23-verificar-antes-de-afirmar.md`](2026-09-23-verificar-antes-de-afirmar.md) | Promovido (principio universal) a `00-estandar-agentes/01-principios-y-seguridad.md` |
| `sesiones/contexto` | [`2026-09-30-plan-paneles-servicio-persistente-tandas.md`](2026-09-30-plan-paneles-servicio-persistente-tandas.md) | Promovido (2026-09-30) a `00-estandar-agentes/` 01, 02, 03 y 04 y a `01-contexto-repositorio/` 03 y 04; pendiente: informes de Worker de formato fijo, hasta medir |
| `skills` | Revisar y usar los Skills disponibles: vacío detectado por Victor (2026-09-30); no tiene archivo propio, la regla quedó directo en el estándar | Promovido (2026-09-30) a `00-estandar-agentes/` 02, 03 y 04 y a las plantillas de plan y progreso |
| `roles/orquestador` | Por qué se olvida el flujo: `AGENTS.md` no nombraba el documento de los 18 pasos; sin archivo propio, la regla quedó directo en `AGENTS.md` y en un Skill | Promovido (2026-09-30) a `AGENTS.md` (primera lectura obligatoria) y al Skill `seguir-flujo-de-planes` |
