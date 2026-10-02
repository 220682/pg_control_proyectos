# Progreso — Dashboard por economía, Curva S con selector y costo real de recursos

## Referencia al plan

- Plan: `docs/02-trabajo-activo/01-planes/2026-10-01-dashboard-economia-y-curva-s.md` (fases A, T, B, C, D, E).
- Briefs: `docs/02-trabajo-activo/01-planes/2026-10-01-dashboard-economia-y-curva-s-briefs/` (índice, reglas de contexto y un brief por tanda; los resultados en `resultados/<tanda>.md`).
- Evidencia: `docs/02-trabajo-activo/03-evidencia/2026-10-01-dashboard-economia-y-curva-s.md`.
- Auditoría: `docs/02-trabajo-activo/04-auditoria/2026-10-01-dashboard-economia-y-curva-s.md` (la escribe el Auditor tras E).

## Estado general y fase actual

- Gate Spec y Gate 1: **aprobados por Victor (2026-10-02)**. Gate 2: pendiente.
- Precondición de arranque (cierre del plan `2026-09-30-niveles-paquetes-plan-maestro-rdt`, Q4): **cumplida el 2026-10-02** (aquel plan quedó Cerrado). Victor autorizó proceder.
- **Fase A lanzada (2026-10-02):** Worker 1 en `local-worker-5` + `.worktrees/local-worker-5`, puerto 3115.
- **Tanda A cerrada (2026-10-02):** commit `d40cd74` en `local-worker-5` (padre `5e8420b`), árbol limpio. `P01`, `P02`, `P04` Conforme; `F01`, `F02`, `V03`, `V04` y la parte A de `F06`/`U02` Observado (verificación en vivo pendiente de la Fase D); `P03` Observado (el flujo 14 se edita en E). Detalle en `…-briefs/resultados/tanda-A.md`.
- **Tanda B cerrada (2026-10-02):** commit `94a5f79`. Parcial sin datos económicos (PD5), Bloque E y enlace a Curva S en ambos (PD6), bloque «Costo real de recursos» con reconciliación = AC (PD1), `descripcion` en la query de `pr_recursos`. 14 ítems: los de lógica/diff Conforme; los visuales Observado por D. Detalle en `…-briefs/resultados/tanda-B.md`.
- **Tanda C cerrada (2026-10-02):** commit `5e773c7`. Selector de dos modos, serie física PV/BAC y EV/BAC, contrato `GET /api/curva-s?modo=` con 403 (PD2/PD4/D03). `D03`, `D04`, `U01`, `V02` Conforme; el resto Observado por D. Dos matices devueltos (PD4 `aria-disabled`; semántica de E01) para confirmar en D. Detalle en `…-briefs/resultados/tanda-C.md`.
- **Sesión congelada y retomada (2026-10-02):** la sesión anterior del Orquestador quedó congelada tras C. Al retomar se encontró un **merge en progreso `local-worker-5` → `main` en la app sin Gate 2** (17 archivos staged); se abortó (`git merge --abort`), `main` restaurado a `35ac5dd` (0/0 con origin). Registrado como OP6 en el libro de hallazgos del plan.
- **Tanda D cerrada (2026-10-02, ~108 llamadas):** verificación en vivo con admin + «Ver como» (Chrome, Playwright), escritorio y móvil 390 px. 21 ítems **Conforme** (F03–F11, U02–U05, E01/E03/E04, V01, R01–R05); matices (a) y (b) de C confirmados. **F12/F13 Observado**: el proyecto `PRUEBA-DASH` no se creó (presupuesto); la sustancia se verificó con PS-0004/0007/0008. V03/V04 parciales (PATCH 403 y OT ajena en vivo pendientes). Sin cambios de código (HEAD sigue `5e773c7`). 9 capturas en `03-evidencia/capturas/dashboard-economia-y-curva-s/`. Detalle en `…-briefs/resultados/tanda-D.md`.
- **Tanda T2 cerrada (2026-10-02, ~71 llamadas):** creado el servicio de prueba **PS-0009** `PRUEBA-DASH Servicio T2` (id `da33f1fa-…`) con DP (BAC US$ 4.482,54; 9 partidas HH/HM) y cronograma (14 act.). **V03 Conforme** (PATCH tipo-dashboard con «Ver como» sin economía → 403) y **V04 Conforme** (López con OT ajena → 403 API y pantallas). F12 parcial (~80 %): faltaban Paquetes → PM → RDTs. Sin código. Detalle en `resultados/tanda-T2.md`.
- **Tanda E cerrada (Documentador, ~55 llamadas):** flujos 11/14/16/21 editados según tabla (iii) (commit `d262395`); M1–M3 → `03-aprendizaje-continuo/` (`2ec79de`); índices + `planes-futuros.md` (`0e757f3`); resumen + **RB8** (B-H2 no estaba volcada al libro) (`ffeeb74`); `verificar-referencias.py` 0/0 (R06 Conforme). Push hecho, `0 0`. Detalle en `resultados/tanda-E.md`.
- **Tanda T3 cerrada (2026-10-02, ~68 llamadas):** **F12/F13 Completados**. PS-0009: paquete `PT-001` (9 partidas), PM v2 APROBADO (22 asignaciones), 2 RDTs VALIDADOS → **50 % de avance**; AC 297,76 = Total del bloque = Σ MO+HM (reconciliación exacta); Curva S económica y física con datos reales; 4 capturas `T3-F13-*`. **Bug fuera de alcance (OP8):** `PATCH /api/plan-maestro` APROBAR con asignaciones inline no las persiste. Sin código. Detalle en `resultados/tanda-T3.md`.
- **Tanda P03 cerrada (~26 llamadas):** `permisos.test.ts` vuelve a comparar las filas Dashboard Parcial/Completo y Curva S física/económica contra el flujo 14 editado (mapa 5→9 × 13 = 117 celdas); suite 1063 verde, tsc 0. Commit **`98df43c`** en `local-worker-5`.

## Tabla de roles / Workers y estado

| Rol | Estado |
|---|---|
| Orquestador | Activo (sesión retomada 2026-10-02) |
| Planner | Plan entregado (2026-10-02) |
| Worker 1 (código, DeepSeek V4.1 Flash) | Tandas A–D cerradas; tanda T2 en lanzamiento (F12/F13) |
| Documentador | En lanzamiento (tanda E) |
| Worker git | Pendiente (merge tras Gate 2) |
| Auditor | Pendiente (tras E y T2) |

## Skills revisados

Skills de `.claude/skills/` de `pg_control_proyectos`: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`, `trasladar-hallazgos`. Repo de la app: sin carpeta de Skills (verificado). El Orquestador usó `seguir-flujo-de-planes` al lanzar la Fase A.

## Avances terminados

- Plan, Punch List, briefs (índice, reglas de contexto, brief A), progreso y evidencia; worktree `local-worker-5` creado desde `main` (`5e8420b`) con `.env.local` y `node_modules` enlazado.
- **Tanda A:** `puedeVerDashboard` y `puedeVerCurvaS` a 13 roles; nueva `puedeVerCurvaSEconomica` (los 5 con economía); `puedeVerEconomia` intacta; `matriz-base-flujo14.ts` con `dashboard`/`curva-s` a 13 roles (0 diferencias); Dashboard fuerza Parcial en servidor; `ToggleTipoDashboard` visible y deshabilitado con `title`. Commit `d40cd74`.
- **Tanda B:** Parcial sin dinero (PD5), Bloque E y enlace a Curva S en ambos (PD6, `?modo=fisica` sin economía), bloque «Costo real de recursos» (PD1) con reconciliación `Σ + (AC−Σ) = AC` y legacy no sumable; `descripcion` añadida a la query. Nuevos `CostoRealRecursos.tsx` y `lib/dashboard/costo-recursos.ts`. Commit `94a5f79`.
- **Tanda C:** selector «Económica (USD)»/«Avance físico (%)»; serie física PV/BAC y EV/BAC sin USD; `GET /api/curva-s?modo=` con 403 en `economica` sin permiso y sin `bac` en `fisica`; sin PM → «Pendiente». Commit `5e773c7`.

## Trabajo actual

Implementación completada: tandas A, B, C, D, T2, T3, E y P03 cerradas. Punch List: todo Conforme salvo **P05** (artefacto «Matriz de permisos» — Victor). Siguiente: ronda documental **E2** (traslado de M4–M9 y cierre de filas nuevas del libro), **Auditoría** y **Gate 2**.

## Pendientes

1. E2: trasladar M4–M9 a `03-aprendizaje-continuo/` y marcar las filas del libro.
2. Auditoría (informe en `04-auditoria/`), con la clasificación de OP1–OP9.
3. Gate 2: aprobación de Victor + autorización explícita del merge/push del código; P05 (artefacto) y decisión sobre el bug OP8; borrado de PS-0009 por Victor (lista de ids en `resultados/tanda-T2.md`/`tanda-T3.md`).
4. Tras Gate 2: merge `local-worker-5` → `main` (Worker git) y mensaje de cierre.

## Commits, ramas y worktrees usados

- `py_control_proyectos_web`: rama `local-worker-5`, worktree `.worktrees/local-worker-5`, desde `main` = `origin/main` = `5e8420b`. Sin push ni merge todavía.
- `pg_control_proyectos`: `main` (documentación), directo.

## Medición

Una fila por sesión medida (plantilla `10-medicion-y-eficiencia.md`).

| Tanda | Sesión | Llamadas | Contexto máx. | ¿Cumple? | Nota |
|---|---|---|---|---|---|
| A | `ses_f029eed31ffeWFI3pCwQvfa79V` | ~52 | no medido directo por opencode (entrada total 107k, caché leída 4,52M) | Sí | commit `d40cd74`; modelo `opencode-go/deepseek-v4.1-flash` |
| B | `ses_f028df363ffeuHsUgvXJJMEeJx` | ~58 | no medido directo por opencode | Sí | commit `94a5f79`; 14/14 ítems |
| C | `ses_f02830508ffern02eppm9wuhSI` | ~42 | no medido directo por opencode | Sí | commit `5e773c7`; dos matices para D |
| Orquestador (A–C) | `ses_f02cf10c6ffe84DXAbOkjj4uBZ` | — | — | — | sesión congelada tras C; dejó un merge en progreso abortado al retomar (OP6) |
| D (con Fase T parcial) | `ses_f01caf7f8ffeIW1ELNrFcYbzq1` | ~108 | no medido directo por opencode | No (excede ~80; OP5) | 21 ítems Conforme; F12 pendiente T2; sin código tocado |
| T2 | `ses_f01a4905effecWEVWhatyP1yqv` | ~71 | no medido directo | No (objetivo ~60; OP7) | PS-0009 + DP/crono; V03/V04 cerrados; F12 parcial |
| E (Documentador) | `ses_f01a42166ffeCJGLNpd1KA4RgY` | ~55 | no medido directo | Sí | flujos 11/14/16/21 + traslados; 4 commits pusheados |
| T3 | `ses_f018dff20ffeZrNUE7YR3RlnO6` | ~68 | no medido directo | Sí | F12/F13 completados; bug OP8 detectado |
| P03 | `ses_f018dba81ffe1Rz0C83usApsBl` | ~26 | no medido directo | Sí | commit `98df43c`; suite 1063 verde |
| Orquestador (retoma, D→cierre) | sesión actual | — | — | — | consolidación A–P03, lanzamiento T2/E/T3/P03 |

## Operaciones de git

Pendientes (Worker git tras Gate 2).

## Hallazgos y preguntas de negocio

Libro de hallazgos del plan consolidado por el Orquestador (2026-10-02): mejoras M1–M3, reglas RB1–RB7, observaciones sobre la política OP1–OP6 (incluye el merge abortado), huérfanos ninguno. Sin conflictos de negocio sin resolver; los matices (a) y (b) de C quedaron confirmados en D.

## Bloqueos, riesgos y decisiones requeridas

- R1 (coordinación con el plan niveles) **cerrado**: aquel plan quedó Cerrado el 2026-10-02.
- R2 (doc↔prueba del flujo 14): la Fase A no edita el flujo 14; la coherencia se cierra en E (ítem P03).

## Próximo paso verificable

Cerrar T2 (F12/F13) y E (flujos + traslados); luego P03 (Worker de código), Auditoría y Gate 2.

## Última actualización y responsable

2026-10-02, Orquestador (sesión retomada).

## Handoffs

Sin handoffs todavía.
