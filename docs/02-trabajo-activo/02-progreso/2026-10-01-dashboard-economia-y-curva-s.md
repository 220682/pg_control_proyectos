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

## Tabla de roles / Workers y estado

| Rol | Estado |
|---|---|
| Orquestador | Activo (esta sesión) |
| Planner | Plan entregado (2026-10-02) |
| Worker 1 (código, DeepSeek V4.1 Flash) | Tanda A en curso |
| Documentador | Pendiente (tanda E) |
| Worker git | Pendiente (merge tras Gate 2) |
| Auditor | Pendiente (tras E) |

## Skills revisados

Skills de `.claude/skills/` de `pg_control_proyectos`: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`, `trasladar-hallazgos`. Repo de la app: sin carpeta de Skills (verificado). El Orquestador usó `seguir-flujo-de-planes` al lanzar la Fase A.

## Avances terminados

- Plan, Punch List, briefs (índice, reglas de contexto, brief A), progreso y evidencia; worktree `local-worker-5` creado desde `main` (`5e8420b`) con `.env.local` y `node_modules` enlazado.
- **Tanda A:** `puedeVerDashboard` y `puedeVerCurvaS` a 13 roles; nueva `puedeVerCurvaSEconomica` (los 5 con economía); `puedeVerEconomia` intacta; `matriz-base-flujo14.ts` con `dashboard`/`curva-s` a 13 roles (0 diferencias); Dashboard fuerza Parcial en servidor; `ToggleTipoDashboard` visible y deshabilitado con `title`. Commit `d40cd74`.
- **Tanda B:** Parcial sin dinero (PD5), Bloque E y enlace a Curva S en ambos (PD6, `?modo=fisica` sin economía), bloque «Costo real de recursos» (PD1) con reconciliación `Σ + (AC−Σ) = AC` y legacy no sumable; `descripcion` añadida a la query. Nuevos `CostoRealRecursos.tsx` y `lib/dashboard/costo-recursos.ts`. Commit `94a5f79`.
- **Tanda C:** selector «Económica (USD)»/«Avance físico (%)»; serie física PV/BAC y EV/BAC sin USD; `GET /api/curva-s?modo=` con 403 en `economica` sin permiso y sin `bac` en `fisica`; sin PM → «Pendiente». Commit `5e773c7`.

## Trabajo actual

Tandas A, B y C cerradas. Siguiente: Fase T (proyecto de prueba de extremo a extremo) + Fase D (verificación en vivo con navegador, 13 roles, dos caras, móvil).

## Pendientes

1. Tanda A: resultados y commit en `local-worker-5`.
2. T, B, C, D, E, Auditoría y Gate 2.

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
| Orquestador (A–C) | `ses_f02cf10c6ffe84DXAbOkjj4uBZ` | — | — | — | sesión en curso |

## Operaciones de git

Pendientes (Worker git tras Gate 2).

## Hallazgos y preguntas de negocio

Sin preguntas devueltas todavía. El libro de hallazgos vive en el plan.

## Bloqueos, riesgos y decisiones requeridas

- R1 (coordinación con el plan niveles) **cerrado**: aquel plan quedó Cerrado el 2026-10-02.
- R2 (doc↔prueba del flujo 14): la Fase A no edita el flujo 14; la coherencia se cierra en E (ítem P03).

## Próximo paso verificable

Consolidar el resultado de la tanda A, medir la sesión y, si A cierra, lanzar T y B.

## Última actualización y responsable

2026-10-02, Orquestador.

## Handoffs

Sin handoffs todavía.
