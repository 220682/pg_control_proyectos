# Aprendizaje continuo

## Qué vive acá

Aprendizajes que nacen de la ejecución de planes: cada uno con origen, evidencia, clasificación y destino propuesto (basado en `08-aprendizaje.md`). El índice de abajo etiqueta cada mejora por categoría, para que cualquier rol escanee rápido y abra solo la que aplica a lo que está por hacer — nunca la carpeta completa por defecto.

`pendientes-de-promocion.md` lista lo que espera aprobación. `historico.md` registra lo ya promovido, rechazado, reemplazado o cerrado.

Cuando un procedimiento reusable **se repite**, el Auditor puede proponer convertirlo en un Skill real de Claude Code (`.claude/skills/`), redactado de forma agnóstica para ser copiable a otros repositorios.

## Qué no vive acá

Ni planes futuros ni tareas operativas completas — eso vive en `../02-trabajo-activo/`.

## Índice por categoría

| Etiqueta | Mejoras |
|---|---|
| `roles/orquestador` | incidente del Orquestador saltando el flujo de roles + FAQ del flujo — ver `historico.md` |
| `sesiones/chat` | `SendMessage` no alcanza sesiones de `create_session` |
| `git/ramas` | acceso directo a Postgres sin IPv6; red bloqueada impide autonomía real (pendiente) |
| `migraciones-sql` | `CREATE OR REPLACE FUNCTION` deja sobrecargas huérfanas |
| `playwright` | falsos negativos en verificación (uppercase, timeout fijo) |
| `lint` | verificar contra `main` y por archivo tocado, no contra cero |
| `tests` | contadores congelados y atribución errónea de fallos en vitest |
| `worktrees/turbopack` | Turbopack no corre en worktrees con `node_modules` en Junction |
| `principios` | verificar antes de afirmar, o preguntar; nunca asumir |
