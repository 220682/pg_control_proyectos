# Evidencia — Dashboard por economía, Curva S con selector y costo real de recursos

## Referencia al plan

- Plan: `docs/02-trabajo-activo/01-planes/2026-10-01-dashboard-economia-y-curva-s.md`.
- Progreso: `docs/02-trabajo-activo/02-progreso/2026-10-01-dashboard-economia-y-curva-s.md`.
- Checklist visual interactivo (artifact de verificación en vivo): https://claude.ai/artifact/8yHL1cn8auxbYghuRoiNhd

## Entorno y fecha

- `py_control_proyectos_web`, rama `local-worker-5`, worktree `.worktrees/local-worker-5`, puerto 3115. Fecha de arranque: 2026-10-02.

## Rol / usuario y datos autorizados

- Cuentas de prueba: en memoria del agente, sin secretos.
- Proyecto de prueba (Fase T): se crea marcado y desactivable; lo borra Victor.

## Punch List ejecutada

| ID | Esperado | Método | Observado | Estado | Evidencia/ruta/enlace | Responsable |
|---|---|---|---|---|---|---|
| F01 | Chip «Dashboard» para 13 roles | tests + inspección | `puedeVerDashboard` = 13 roles (test); chip deriva del registro | Observado (falta captura en D) | `resultados/tanda-A.md` | Worker 1 · A |
| F02 | Chip «Curva S» para 13 roles; económica 5 | tests | `puedeVerCurvaS` = 13; `puedeVerCurvaSEconomica` = 5 (test) | Observado (falta captura en D) | `resultados/tanda-A.md` | Worker 1 · A |
| P01 | `permisos.ts` 13/13/5; economía intacta | `npm test` | 108/108 módulos; suite 1051/1051 | Conforme | commit `d40cd74` | Worker 1 · A |
| P02 | Registro y matriz coherentes | `matriz-accesos.test.ts` | 0 diferencias vs base (dashboard/curva-s = 13) | Conforme | commit `d40cd74` | Worker 1 · A |
| P03 | Doc↔prueba del flujo 14 coherente (cierra en E) | nota + `npm test` | flujo 14 sin editar; mapa de `permisos.test.ts` 7→5 filas; `npm test` verde | Observado (cierra en E) | `resultados/tanda-A.md` A-H1 | Worker 1 · A/E |
| P04 | Alcance por OT intacto | prueba OT ajena + admin | alcance por OT y bypass admin cubiertos por prueba | Conforme | commit `d40cd74` | Worker 1 · A |
| V03 | Dashboard valida en servidor; PATCH sin cambio | prueba + revisión | PATCH sigue exigiendo `puedeVerEconomia`; página fuerza Parcial en servidor | Observado (prueba en vivo en D) | `resultados/tanda-A.md` | Worker 1 · A |
| V04 | Sin sesión/alcance: rechazo igual | prueba | guards intactos (revisión); prueba en vivo pendiente de D | Observado (D) | `resultados/tanda-A.md` | Worker 1 · A |
| F06 | Interruptor deshabilitado con `title` (A) | DOM/captura | toggle visible; opciones `disabled` con `title` | Observado (DOM en D) | `resultados/tanda-A.md` | Worker 1 · A/B |
| U02 | Opciones deshabilitadas visibles con `title` | DOM | opciones visibles y deshabilitadas con `title` | Observado (DOM en D) | `resultados/tanda-A.md` | Worker 1 · A/B |
| F03 | BD en COMPLETO + rol sin economía → Parcial | prueba | servidor fuerza Parcial (revisión de código) | Observado (D) | `resultados/tanda-B.md` | Worker 1 · B |
| F04 | Parcial sin ningún dato monetario (PD5) | inspección | ocultos 6 KPI + cabecera/resumen/semáforo/dona/gráfico/columnas/orden; conservados filtros, % físico, matriz sin costo, diagnóstico, PPC/Pareto, enlace | Conforme (captura en D) | commit `94a5f79` | Worker 1 · B |
| F05 | Parcial conserva filtros, % físico, matriz sin costo, diagnóstico, PPC/Pareto y enlace | inspección | conservados | Conforme (captura en D) | commit `94a5f79` | Worker 1 · B |
| F06-B | Interruptor alterna sin recargar (con economía) | revisión | `router.refresh()` | Observado (D) | `resultados/tanda-B.md` | Worker 1 · B |
| F07 | Ambos enlazan Curva S; Parcial sin economía `?modo=fisica` | inspección | implementado | Conforme (URL en D) | commit `94a5f79` | Worker 1 · B |
| F08 | Bloque de costo solo en Completo; Total = AC | prueba/suma | bloque nuevo + reconciliación probada; legacy como nota | Conforme (captura en D) | commit `94a5f79` | Worker 1 · B |
| D01 | `descripcion` en la query de `pr_recursos` | diff | añadida y usada por el bloque | Conforme | commit `94a5f79` | Worker 1 · B |
| D02 | Reconciliación con tests (`Σ + (AC−Σ) = AC`) | `npm test` | `costo-recursos.test.ts`: 6 pruebas; casos con/sin legacy, diferencia ≠ 0 y = 0 | Conforme | commit `94a5f79` | Worker 1 · B |
| D04 | Dashboard y Curva S leen, no recalculan | diff | sin cambios en `evm.ts`, `dashboard.ts` ni SQL | Conforme | A/B/C | Worker 1 |
| D05 | Total del bloque = KPI AC | revisión | misma fuente del PR | Conforme (captura en D) | commit `94a5f79` | Worker 1 · B |
| U03 | Tabla con scroll horizontal, encabezado fijo, `scope`, sin `max-w-*`; paleta `design.md` | revisión | implementado | Observado (captura en D) | `resultados/tanda-B.md` | Worker 1 · B |
| U05 | Ocultado en Parcial sin huecos de layout | revisión | implementado | Observado (captura en D) | `resultados/tanda-B.md` | Worker 1 · B |
| E02 | Bloque vacío; diferencia = 0 → sin fila «Sin resolver» | prueba | cubierto por `costo-recursos.test.ts` | Conforme | commit `94a5f79` | Worker 1 · B |
| E03 | Carga atenuada y error de API con mensaje | revisión | patrón existente conservado | Observado (D) | B/C | Worker 1 |
| F09 | Selector visible; «Económica (USD)» deshabilitada con `title` sin economía | inspección | implementado (`aria-disabled` + `title`, ver matiz) | Conforme (captura en D) | commit `5e773c7` | Worker 1 · C |
| F10 | Curva física PV/BAC y EV/BAC sin USD | inspección | implementado; tabla con «—» en celdas sin dato | Conforme (captura en D) | commit `5e773c7` | Worker 1 · C |
| F11 | Sin PM: «Pendiente»; real con RDT validados | inspección | implementado | Conforme (captura en D) | commit `5e773c7` | Worker 1 · C |
| D03 | Serie física en lógica pura con tests | `npm test` | `curva-s.test.ts` 18/18 (6 nuevas); BAC=0 sin serie | Conforme | commit `5e773c7` | Worker 1 · C |
| U01 | Selector `role="group"`, `aria-label`, `aria-disabled`, `title`, foco de teclado | DOM | implementado | Conforme | commit `5e773c7` | Worker 1 · C |
| U04 | Un eje Y por modo con unidad rotulada | inspección | implementado | Conforme (captura en D) | commit `5e773c7` | Worker 1 · C |
| E01 | Sin PM «Pendiente»; sin RDT serie real vacía con nota | inspección | implementado | Conforme (semántica a confirmar en D) | `resultados/tanda-C.md` | Worker 1 · C |
| E04 | `modo=economica` sin permiso → 403 | llamada directa | lógica en `route.ts`; llamada con cuenta en D | Observado (D) | `resultados/tanda-C.md` | Worker 1 · C |
| V01 | 403 en económico forzado; sin `modo` determinista | llamada directa | lógica implementada; llamada con las dos cuentas en D | Observado (D) | `resultados/tanda-C.md` | Worker 1 · C |
| V02 | `modo=fisica` sin montos USD ni `bac` | JSON | sin `pvAcum`/`evAcum`/`acAcum`/`bac` | Conforme | commit `5e773c7` | Worker 1 · C |

## Enlace al artifact de checklist visual

https://claude.ai/artifact/8yHL1cn8auxbYghuRoiNhd

## Resultados de pruebas técnicas

Pendientes: se llenan con la evidencia de cada tanda (`resultados/<tanda>.md`).

## Regresiones verificadas

Pendiente (Fase D).

## Limitaciones o casos no verificables

- Verificación en vivo sin navegador en A–C; queda para D.
