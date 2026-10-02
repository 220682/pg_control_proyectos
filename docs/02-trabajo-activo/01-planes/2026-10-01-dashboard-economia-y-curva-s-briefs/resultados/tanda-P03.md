# Resumen de cierre — Tanda P03 (Worker de código, cierre del ítem P03)

## Tanda, rol y modelo

- Plan `2026-10-01-dashboard-economia-y-curva-s` · Tanda **P03** (Worker de código) · worktree `py_control_proyectos_web/.worktrees/local-worker-5`, rama `local-worker-5`.
- Insumo: brief de la tarea (restaurar en `permisos.test.ts` las filas del flujo 14 separadas en Fase E) y tabla 1 del flujo 14 (commit `d262395`).
- Único archivo tocado: `src/lib/permisos/permisos.test.ts`.

## Qué cambió en el test

El mapa `FUNCIONES` (que compara fila por fila la tabla 1 del flujo 14 leída por ruta absoluta) pasó de 5 a **9 filas** al recuperar las cuatro que la Fase E separó:

| Fila en el mapa (nombre exacto del flujo 14) | Permiso mapeado | Roles |
|---|---|---|
| `Dashboard del servicio — Parcial` | `puedeVerDashboard` | 13 |
| `Dashboard del servicio — Completo` | `(r) => puedeVerDashboard(r) && puedeVerEconomia(r)` | 5 |
| `Curva S — avance físico (%)` | `puedeVerCurvaS` | 13 |
| `Curva S — económica (USD)` | `puedeVerCurvaSEconomica` | 5 |

Las otras cinco filas (`Dashboard del portafolio`, `PR`, `DP`, `Plan Maestro`, `Registro de costos`) se conservan sin cambio. `expect(comparadas)` pasa de `5 * 13` a **`9 * 13`**.

Como `puedeVerDashboard` y `puedeVerCurvaS` ahora dan `true` a los 13 roles, las dos aserciones de semántica económica que iteraban todo `FUNCIONES` (excepciones planner/SOT y «asistente no ve ninguna interfaz con economía») quedaron acotadas a las filas con datos económicos mediante la lista `FILAS_TODOS_LOS_ROLES` (`Dashboard del servicio — Parcial`, `Curva S — avance físico (%)`), que no rompe el objetivo de esas pruebas y las mantiene verdes.

## Comandos y resultado

- `npx vitest run src/lib/permisos/permisos.test.ts` → **1 archivo / 93 tests pasados**.
- `npm test` (suite completa) → **102 archivos / 1063 tests pasados**.
- `npx tsc --noEmit` → **sin errores**.

## Commit

- `98df43c` en `local-worker-5`: `tanda P03: permisos.test.ts vuelve a comparar las filas Dashboard Parcial/Completo y Curva S fisica/economica contra el flujo 14`.
- `git add src/lib/permisos/permisos.test.ts` explícito · 1 archivo, +22/−8 · sin push ni merge · árbol limpio.
