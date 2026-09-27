# Histórico de aprendizajes

Aprendizajes ya promovidos, rechazados, reemplazados o cerrados, con su destino final y fecha. Un archivo migrado y promovido **no se borra**: queda en esta carpeta y su estado pasa a "promovido" acá.

| Fecha | Archivo | Clasificación | Destino final |
|---|---|---|---|
| 2026-09-21 | [`2026-09-21-acceso-postgres-sin-ipv6.md`](2026-09-21-acceso-postgres-sin-ipv6.md) | Histórico (excepción cerrada) | Queda como registro histórico de una excepción puntual ya cerrada (acceso IPv6 resuelto); no se integró a ninguna fuente de verdad permanente. |
| 2026-09-21 | [`2026-09-21-verificacion-playwright-falsos-negativos.md`](2026-09-21-verificacion-playwright-falsos-negativos.md) | Promovido | `docs/01-contexto-repositorio/04-pruebas-y-evidencia.md` § Falsos negativos conocidos. |
| 2026-09-23 | [`2026-09-23-eslint-baseline-vs-cero.md`](2026-09-23-eslint-baseline-vs-cero.md) | Promovido | `docs/01-contexto-repositorio/04-pruebas-y-evidencia.md` § Lint: contra `main`, no contra cero. |
| 2026-09-23 | [`2026-09-23-orquestador-salta-flujo-de-roles-sin-auditoria.md`](2026-09-23-orquestador-salta-flujo-de-roles-sin-auditoria.md) | Histórico (ya promovido a roles) | El incidente y sus tres rondas de seguimiento ya están integrados en `docs/00-estandar-agentes/02-roles-y-delegacion.md` (límites del Orquestador, primer chequeo del Auditor, los dos únicos puntos de parada, la separación commit/push/merge de código vs. documentación). Este archivo queda como el registro completo del incidente que originó esas reglas. |
| 2026-09-23 | [`2026-09-23-preguntas-frecuentes-flujo-orquestador.md`](2026-09-23-preguntas-frecuentes-flujo-orquestador.md) | Histórico con rastro visible | FAQ en lenguaje llano del flujo de roles; varias de sus preguntas motivaron correcciones ya integradas en `docs/00-estandar-agentes/02-roles-y-delegacion.md` y `04-flujo-sdd-y-planes.md`. Se referencia desde ambos documentos. |
| 2026-09-23 | [`2026-09-23-sendmessage-no-alcanza-sesiones-create-session.md`](2026-09-23-sendmessage-no-alcanza-sesiones-create-session.md) | Promovido | `docs/00-estandar-agentes/03-sesiones-contexto-y-handoff.md` § Límite conocido: mensajería entre sesiones. |
| 2026-09-23 | [`2026-09-23-tests-contadores-congelados.md`](2026-09-23-tests-contadores-congelados.md) | Promovido | `docs/01-contexto-repositorio/04-pruebas-y-evidencia.md` § Tests: contadores congelados y atribución de fallos. |
| 2026-09-23 | [`2026-09-23-turbopack-worktree-junction.md`](2026-09-23-turbopack-worktree-junction.md) | Promovido | `docs/01-contexto-repositorio/03-entorno-git-y-worktrees.md` § Worktrees y bundler. |
| 2026-09-23 | [`2026-09-23-verificar-antes-de-afirmar.md`](2026-09-23-verificar-antes-de-afirmar.md) | Promovido (principio universal) | `docs/00-estandar-agentes/01-principios-y-seguridad.md` § Verificar antes de afirmar, o preguntar. |

## No promovidos (se quedan solo como aprendizaje, sin cambiar ninguna fuente de verdad)

| Archivo | Motivo |
|---|---|
| [`2026-09-21-migraciones-sql-sobrecargas-huerfanas.md`](2026-09-21-migraciones-sql-sobrecargas-huerfanas.md) | Aprendizaje técnico puntual sobre `CREATE OR REPLACE FUNCTION` en Postgres; útil como referencia pero no se integró a un documento permanente en esta reestructuración — queda disponible por su etiqueta (`migraciones-sql`) en el índice. |
