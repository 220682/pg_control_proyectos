# F6-E · Cierre técnico: diff limpio, pruebas, lint contra línea base, build y evidencia completa

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F6 · **Depende de:** F6-A a F6-D cerradas (o sus Observados aceptados por el Orquestador).
**Punto de commit:** Commit final de la fase F6 en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-35 | No hay migraciones ni cambios en `db/` ni en tablas: el diff de `local-worker-1` contra `main` no toca `db/` | `git diff --stat` |
| PL-36 | El diff no toca `src/lib/pr`, `dashboard`, `curva-s`, `plan-maestro` ni `dp` (los cálculos EVM no cambian); en las páginas de PR, Dashboard (servicio y portafolio), DP, Curva S, Plan Maestro y Registro de costos solo cambia la guardia (F5B) | `git diff --stat` + revisión del diff de esas páginas |
| PL-74 | `npm test` completo verde; contadores actualizados con pruebas específicas de ubicación y comportamiento de los ítems nuevos (no solo el número) | Resumen del runner (no un filtro de texto) |
| PL-75 | Lint sin deuda nueva: mismo total que `main` y archivos tocados limpios | Conteo contra `main` |
| PL-76 | `npm run build` correcto (en worktree con `--webpack`) | Salida del build |
| PL-79 | Ningún dato real fue creado, modificado ni borrado durante la verificación | Nota en la evidencia + revisión de las acciones ejecutadas |
| PL-87 | Evidencia completa en `03-evidencia/` con enlace al artifact de checklist visual si se crea, y limitaciones declaradas (SVX si no existe, rol de la cuenta B) | Archivo de evidencia |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- **PL-35:** `git diff --stat main...local-worker-1 -- db/` vacío (sin migraciones). **PL-36:** el diff no toca `src/lib/pr`, `dashboard`, `curva-s`, `plan-maestro` ni `dp`; en las páginas de PR, Dashboard (servicio y portafolio), DP, Curva S, Plan Maestro y Registro de costos solo cambia la guardia (y, para el Dashboard, el permiso del interruptor por C35): revisa el diff de esas páginas.
- **PL-74:** `npm test` completo verde (resumen del runner, no un filtro de texto), con contadores actualizados y pruebas de ubicación y comportamiento. **PL-75:** `npm run lint` sin deuda nueva: mismo total que la línea base LB-01 de F0-A (medida en `main` = HEAD inicial) y archivos tocados limpios. **PL-76:** `npx next build --webpack` correcto en el worktree.
- **PL-79:** ningún dato real fue creado, modificado ni borrado: nota en la evidencia con revisión de las acciones ejecutadas en todas las tandas (a partir de los handoffs).
- **PL-87:** evidencia completa en `02-trabajo-activo/03-evidencia/2026-09-27-paneles-servicio-persistente.md`, con limitaciones declaradas (SVX si no existe, rol de la cuenta B, Observados). Enlace al artefacto de checklist visual si se crea.
- Si quedan Observados corregibles, el Orquestador lanza tandas `F6-R#` (ver `00-indice-de-tandas.md`). Este es el último punto del «loop hasta 100%» antes de F7.

## Qué NO hacer

- No hagas push ni merge. No borres ramas ni worktrees.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
