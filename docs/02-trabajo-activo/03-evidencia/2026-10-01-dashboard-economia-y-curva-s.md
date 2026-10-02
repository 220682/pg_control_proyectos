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
| F01 | Chip «Dashboard» para 13 roles | tests + inspección | `puedeVerDashboard` = 13 roles (test); chip deriva del registro; D: barrido 13 roles (R03) y sin chips rotos (R05) | Conforme | `resultados/tanda-A.md`, `resultados/tanda-D.md` | Worker 1 · A/D |
| F02 | Chip «Curva S» para 13 roles; económica 5 | tests | `puedeVerCurvaS` = 13; `puedeVerCurvaSEconomica` = 5 (test); D: barrido 13 roles | Conforme | `resultados/tanda-A.md`, `resultados/tanda-D.md` | Worker 1 · A/D |
| P01 | `permisos.ts` 13/13/5; economía intacta | `npm test` | 108/108 módulos; suite 1051/1051 | Conforme | commit `d40cd74` | Worker 1 · A |
| P02 | Registro y matriz coherentes | `matriz-accesos.test.ts` | 0 diferencias vs base (dashboard/curva-s = 13) | Conforme | commit `d40cd74` | Worker 1 · A |
| P03 | Doc↔prueba del flujo 14 coherente (cierra en E) | nota + `npm test` | flujo 14 sin editar; mapa de `permisos.test.ts` 7→5 filas; `npm test` verde | Observado (cierra en E) | `resultados/tanda-A.md` A-H1 | Worker 1 · A/E |
| P04 | Alcance por OT intacto | prueba OT ajena + admin | alcance por OT y bypass admin cubiertos por prueba | Conforme | commit `d40cd74` | Worker 1 · A |
| V03 | Dashboard valida en servidor; PATCH sin cambio | prueba + revisión | D: F03 verifica el forzado de Parcial en servidor (PS-0008 COMPLETO + rol sin economía); PATCH sin cambio (revisión); 403 del PATCH en vivo se intenta en T2 | Conforme parcial | `resultados/tanda-D.md` | Worker 1 · A/D |
| V04 | Sin sesión/alcance: rechazo igual | prueba | D: sin sesión → 307 a `/login`; OT ajena no probada en vivo (guard sin cambios; se intenta en T2) | Conforme (sin sesión) / Observado (OT ajena) | `resultados/tanda-D.md` | Worker 1 · A/D |
| F06 | Interruptor deshabilitado con `title` (A) | DOM/captura | D: toggle visible; sin economía `disabled`+`title`; con economía alterna sin recargar | Conforme | `resultados/tanda-D.md` | Worker 1 · A/B/D |
| U02 | Opciones deshabilitadas visibles con `title` | DOM | D: opciones visibles y deshabilitadas con `title` (no ocultas) | Conforme | `resultados/tanda-D.md` | Worker 1 · D |
| F03 | BD en COMPLETO + rol sin economía → Parcial | prueba | D: PS-0008 `tipo_dashboard=COMPLETO`; con `supervisor_operativo` el servidor fuerza Parcial (sin USD ni «Costo directo»). Captura `F03-F04-F05-U05-*` | Conforme | `resultados/tanda-D.md` | Worker 1 · B/D |
| F04 | Parcial sin ningún dato monetario (PD5) | inspección | ocultos 6 KPI + cabecera/resumen/semáforo/dona/gráfico/columnas/orden; conservados filtros, % físico, matriz sin costo, diagnóstico, PPC/Pareto, enlace | Conforme (captura en D) | commit `94a5f79` | Worker 1 · B |
| F05 | Parcial conserva filtros, % físico, matriz sin costo, diagnóstico, PPC/Pareto y enlace | inspección | conservados | Conforme (captura en D) | commit `94a5f79` | Worker 1 · B |
| F06-B | Interruptor alterna sin recargar (con economía) | revisión | D: admin alterna a Económica sin recargar la URL | Conforme | `resultados/tanda-D.md` | Worker 1 · B/D |
| F07 | Ambos enlazan Curva S; Parcial sin economía `?modo=fisica` | inspección | D: DOM `hrefCurvaS` = `/proyectos/{id}/curva-s?modo=fisica` en Parcial; nav lateral sin `modo` (servidor deriva) | Conforme | `resultados/tanda-D.md` | Worker 1 · B/D |
| F08 | Bloque de costo solo en Completo; Total = AC | prueba/suma | D: captura `U03-F08-F13-*` (Completo admin con bloque); tests D02 | Conforme | `resultados/tanda-D.md` | Worker 1 · B/D |
| D01 | `descripcion` en la query de `pr_recursos` | diff | añadida y usada por el bloque | Conforme | commit `94a5f79` | Worker 1 · B |
| D02 | Reconciliación con tests (`Σ + (AC−Σ) = AC`) | `npm test` | `costo-recursos.test.ts`: 6 pruebas; casos con/sin legacy, diferencia ≠ 0 y = 0 | Conforme | commit `94a5f79` | Worker 1 · B |
| D04 | Dashboard y Curva S leen, no recalculan | diff | sin cambios en `evm.ts`, `dashboard.ts` ni SQL | Conforme | A/B/C | Worker 1 |
| D05 | Total del bloque = KPI AC | revisión | misma fuente del PR | Conforme (captura en D) | commit `94a5f79` | Worker 1 · B |
| U03 | Tabla con scroll horizontal, encabezado fijo, `scope`, sin `max-w-*`; paleta `design.md` | revisión | D: DOM `overflow-x-auto`, `th` con `scope="col"` y `sticky top:0`, `main` sin `max-w-*`; capturas escritorio y móvil | Conforme | `resultados/tanda-D.md`, capturas | Worker 1 · B/D |
| U05 | Ocultado en Parcial sin huecos de layout | revisión | D: 0 secciones vacías en escritorio y móvil 390 px; grid económico omitido entero | Conforme | capturas `F03-*`, `R05-U05-*` | Worker 1 · B/D |
| E02 | Bloque vacío; diferencia = 0 → sin fila «Sin resolver» | prueba | cubierto por `costo-recursos.test.ts` | Conforme | commit `94a5f79` | Worker 1 · B |
| E03 | Carga atenuada y error de API con mensaje | revisión | D: 500 forzado por interceptación → mensaje del cuerpo y «Cargando…» atenuado (`opacity-50`, sin salto de layout) | Conforme | `resultados/tanda-D.md` | Worker 1 · D |
| F09 | Selector visible; «Económica (USD)» deshabilitada con `title` sin economía | inspección | D: `aria-disabled="true"`+`title` sin economía; ambos activos con admin (matiz (a) de C confirmado) | Conforme | capturas `F09-F10-U04-*`, `U04-F09-*` | Worker 1 · C/D |
| F10 | Curva física PV/BAC y EV/BAC sin USD | inspección | D: PS-0004 EV real 12.3 %, eje «Avance físico (%)», sin USD en eje/tooltip/tarjetas/tabla | Conforme | captura `F10-U04-*` | Worker 1 · C/D |
| F11 | Sin PM: «Pendiente»; real con RDT validados | inspección | D: PS-0007 banner «Pendiente» sin curva PV; % real con RDT visto en PS-0004; no existe proyecto sin-PM-con-RDT | Conforme con nota | captura `E01-F11-*` | Worker 1 · C/D |
| F12 | Proyecto de prueba `PRUEBA-DASH-…` de extremo a extremo hasta ~50 % | creación + trayectoria | No creado en D (presupuesto consumido por la verificación en vivo); no se tocó BD ni se borró nada | Observado — pendiente T2 | `resultados/tanda-D.md` | Worker 1 · T2 |
| F13 | Toda la estructura funcionando con el proyecto de prueba | capturas | Sustancia verificada en D con PS-0004/PS-0007/PS-0008 (Parcial, Completo + bloque recursos, Curva S dos modos, 13 roles); se re-verifica en T2 con el `PRUEBA-DASH` | Observado (sustancia verificada) | capturas `F13-R02-*`, `U03-F08-F13-*` | Worker 1 · T2 |
| D03 | Serie física en lógica pura con tests | `npm test` | `curva-s.test.ts` 18/18 (6 nuevas); BAC=0 sin serie | Conforme | commit `5e773c7` | Worker 1 · C |
| U01 | Selector `role="group"`, `aria-label`, `aria-disabled`, `title`, foco de teclado | DOM | implementado | Conforme | commit `5e773c7` | Worker 1 · C |
| U04 | Un eje Y por modo con unidad rotulada | inspección | D: económico «US$ acumulado (CD)» (PV/EV/AC) vs físico «Avance físico (%)» (PV/BAC, EV/BAC); nunca juntos | Conforme | capturas `U04-F09-*`, `F10-U04-*` | Worker 1 · C/D |
| E01 | Sin PM «Pendiente»; sin RDT serie real vacía con nota | inspección | D: PS-0007 «Pendiente»; PS-0008 nota «serie real vacía» y «—» en tabla (matiz (b) confirmado). RB7: con BAC=0 el mensaje es «no tiene BAC» | Conforme | captura `E01-F11-*` | Worker 1 · C/D |
| E04 | `modo=economica` sin permiso → 403 | llamada directa | D: `supervisor_operativo` → 403 `{"error":"No tienes acceso a la Curva S económica"}`; la interfaz nunca ofrece el modo | Conforme | `resultados/tanda-D.md` | Worker 1 · C/D |
| V01 | 403 en económico forzado; sin `modo` determinista | llamada directa | D: sin economía → 403 forzado; sin `modo` → `fisica` sin `ac`; admin → 200 | Conforme | `resultados/tanda-D.md` | Worker 1 · C/D |
| R01 | Suite/tsc/lint/build verdes en el carril | comandos | D: `npm test` 102 archivos/1063 OK; `tsc --noEmit` 0; lint 27 (9E/18W) = baseline `main`; `next build --webpack` 0 | Conforme | `resultados/tanda-D.md` | Worker 1 · D |
| R02 | 5 roles con economía ven Completo + bloque nuevo | barrido DOM | D: los 5 roles ven Completo con `US$` y «Costo real de recursos» | Conforme | `resultados/tanda-D.md` | Worker 1 · D |
| R03 | 13 roles entran a Parcial y Curva S; portafolio sin cambios | barrido DOM | D: 8 sin economía → Parcial; 5 con economía → Completo; portafolio admin OK | Conforme | `resultados/tanda-D.md` | Worker 1 · D |
| R04 | Pruebas del plan niveles siguen verdes | suite | D: `integracion-permisos.test.ts` 5 OK; suite completa verde | Conforme | `resultados/tanda-D.md` | Worker 1 · D |
| R05 | En vivo móvil y escritorio sin roturas | capturas | D: 1440 y 390 px (CDP): sin overflow, sin chips rotos, enlaces correctos | Conforme | capturas `R05-*` | Worker 1 · D |
| R06 | Referencias + índice de planes | verificador | Pendiente Fase E | Pendiente (E) | — | Documentador |
| P05 | Artefacto «Matriz de permisos» | confirmación | Pendiente: lo actualiza Victor (Fase E) | Pendiente (Victor) | — | Victor |
| V02 | `modo=fisica` sin montos USD ni `bac` | JSON | sin `pvAcum`/`evAcum`/`acAcum`/`bac` | Conforme | commit `5e773c7` | Worker 1 · C |

## Enlace al artifact de checklist visual

https://claude.ai/artifact/8yHL1cn8auxbYghuRoiNhd

## Resultados de pruebas técnicas

Tanda D (2026-10-02, worktree `local-worker-5`, HEAD `5e773c7`):

- `npm test` → 102 archivos / **1063 pruebas OK** (`integracion-permisos.test.ts` 5 OK).
- `npx tsc --noEmit` → exit 0.
- `npm run lint` → 27 problemas (9 errores, 18 warnings) = **baseline de `main`**; 0 en archivos del plan.
- `npx next build --webpack` → exit 0.
- `GET /api/curva-s?modo=economica` con rol sin economía → **403**; sin `modo` → `fisica` sin `ac`; sin sesión → **307** a `/login`.
- Barrido DOM: 8 roles sin economía → Parcial sin `US$`; 5 con economía → Completo con `US$` + «Costo real de recursos»; 13 roles entran a Dashboard y Curva S.
- Móvil 390 px (CDP `Emulation.setDeviceMetricsOverride`): sin overflow, sin USD en Parcial, sin secciones vacías.

## Regresiones verificadas

- R01–R05 Conforme (tanda D): suite completa, tipos, lint contra baseline, build, portafolio y resto de economía sin cambios, guard de sesión intacto (307).
- Pruebas del plan niveles (`integracion-permisos.test.ts`) verdes tras A–C.

## Limitaciones o casos no verificables

- **F12/F13:** proyecto `PRUEBA-DASH` no creado en D por presupuesto; pendiente tanda T2. La estructura se verificó con proyectos existentes (PS-0004 con PM+RDT, PS-0007 sin PM, PS-0008 con PM sin RDT). PS-0005 no está vigente.
- **V04 (OT ajena)** y **V03 (PATCH 403 en vivo):** no probados en vivo («Ver como» cambia rol, no alcance; guards sin cambios en este plan). Se intentan en T2.
- **F11:** no existe en los datos un proyecto sin-PM-con-RDT; el «% real» se verificó en PS-0004 (con PM).
- Credenciales para los 13 roles reales: no existen todavía (plan futuro); las dos caras se verificaron con admin + suplantación «Ver como».
- **P03:** coherencia doc↔prueba del flujo 14 cierra en Fase E (+ Worker de código para `permisos.test.ts`).
