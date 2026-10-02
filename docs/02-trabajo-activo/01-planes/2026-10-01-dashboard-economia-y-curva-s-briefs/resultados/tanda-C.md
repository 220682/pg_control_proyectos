# Resumen de cierre — Tanda C · Curva S con selector de dos modos

## Tanda, rol y modelo

- Plan: `2026-10-01-dashboard-economia-y-curva-s` · Tanda **C** · Worker 1 (código) · modelo **DeepSeek V4.1 Flash** (`opencode-go/deepseek-v4.1-flash`).
- Carril único `local-worker-5`, worktree `.worktrees/local-worker-5`, puerto 3115. Sin navegador.
- Depende de A (hecha) y B (hecha: `94a5f79`).

## Estado de los ítems

| ID | Estado | Evidencia: comando o pantalla y resultado real | Causa y quién lo resuelve, si no es Conforme |
|---|---|---|---|
| F09 | Conforme (implementación) / Observado (captura por rol) | `PantallaCurvaS.tsx`: selector `role="group"` con «Económica (USD)» y «Avance físico (%)» siempre visible; económica con `aria-disabled` + `title` para rol sin economía. | La captura por rol es de Fase D (navegador). |
| F10 | Conforme (inspección) / Observado (captura) | `GraficoCurvaS.tsx` modo `fisica`: eje «Avance físico (%)», series PV/BAC y EV/BAC, sin AC; tooltip/tarjetas/tabla en `%`. | Captura en D. |
| F11 | Conforme (inspección) / Observado (captura) | Sin PM: `pvPct = null` → «Pendiente» (tarjeta y tabla) y no se dibuja PV; EV se dibuja con los RDT existentes (`calcularSerieFisica`, `route.ts`). | Captura en servicio sin PM en D. |
| D03 | Conforme | `npx vitest run src/lib/curva-s/curva-s.test.ts`: 18/18 verdes (6 nuevas: PV/BAC, EV/BAC, claves sin montos, BAC=0 → `[]`, sin PM → null, recorte al corte, agrupación semanal intacta). | — |
| D04 | Conforme | `git diff --stat`: solo 6 archivos de Curva S; sin cambios en `src/lib/evm.ts`, `src/lib/dashboard/dashboard.ts` ni `db/**`. `calcularSerieFisica` es derivación pura sobre la serie leída. | — |
| U01 | Conforme (inspección DOM) | Selector con `role="group"` y `aria-label="Modo de la Curva S"`; opción no permitida `aria-disabled`, `title`, sigue siendo foco de teclado (no `disabled`), nunca oculta. | — |
| U04 | Conforme (inspección) / Observado (captura) | Un solo eje Y por modo: económico «US$ acumulado (CD)», físico «Avance físico (%)»; `ac` es `null` en físico. | Captura de ambos modos en D. |
| E01 | Conforme (implementación) / Observado (captura) | Sin PM: banner + «Pendiente» en % planificado. Sin RDT (todas EV=0): nota «la serie real (EV/BAC) está vacía» y no se dibuja la línea EV; tabla muestra «—» en real. | Captura en servicio sin PM y sin RDT en D. |
| E03 | Conforme (patrón existente) / Observado (captura) | Carga atenuada con `transition-opacity opacity-50` sobre el render anterior (sin salto de layout); error de API con `setError` y mensaje del cuerpo. | Forzado de error en vivo en D. |
| E04 | Observado — pendiente D | Implementado en `route.ts:50-55`: `modo=economica` sin `puedeVerCurvaSEconomica` → 403 «No tienes acceso a la Curva S económica». La interfaz nunca ofrece el modo (botón `aria-disabled`). | Llamada directa con sesión real, Fase D. |
| V01 | Observado — pendiente D | Implementado en `route.ts:49-56`: sin `modo` deriva `economica` si `puedeVerCurvaSEconomica`, si no `fisica`; `modo` inválido → 400. | Llamada directa con las dos cuentas, Fase D. |
| V02 | Conforme (cuerpo revisado) | `route.ts` bloque `modo === 'fisica'` devuelve `{modo, fechaCorte, hayPlanMaestroAprobado, rangoAplicado, rangoDisponible, bacDisponible, serie:[{fecha,pvPct,evPct}]}`: sin `pvAcum`/`evAcum`/`acAcum` ni `bac`. | — |

## Rama, commits y archivos tocados

- Rama `local-worker-5` (worktree `.worktrees/local-worker-5`), base `94a5f79`.
- Archivos: `src/lib/curva-s/curva-s.ts`, `src/lib/curva-s/curva-s.test.ts`, `src/app/api/curva-s/route.ts`, `src/components/curva-s/GraficoCurvaS.tsx`, `src/components/curva-s/PantallaCurvaS.tsx`, `src/app/(workspace)/proyectos/[id]/curva-s/page.tsx`.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| C-H1 | Observación sobre la política | PD4 dice «opción no permitida con `disabled` + `title`», U01 y `design.md` §254 piden `aria-disabled` y accesible por teclado. Se implementó `aria-disabled` (foco de teclado, `title`, `cursor-not-allowed`, `opacity-40`). | Confirmar PD4 como `aria-disabled` para todo el plan. |
| C-H2 | Regla de negocio (detectada, no editada) | El modo físico necesita el BAC; se tomó `Σ pr_partidas.bac` (flujo 21 §8), leído en servidor y **no** devuelto en `modo=fisica`. | Dejar registrado en flujo 21 al pasar a Fase E. |
| C-H3 | Observación sobre la política | E01 («sin RDT validados: serie real vacía») se interpretó como: si todas las EV del rango son 0, no dibujar la línea EV y mostrar nota; la tabla usa «—». | Confirmar la interpretación en D/cierre. |

## Traspaso

Hecho: selector de dos modos (PD4/U01), contrato `GET /api/curva-s?modo=` con 403 y derivación por permiso (PD2/V01), serie física pura `calcularSerieFisica` con BAC=0 → `[]` (D03), render físico sin USD en eje/tooltip/tarjetas/tabla (F10/U04/V02), «Pendiente» sin PM (F11/E01), carga atenuada y error existentes (E03).
Pendiente (Fase D): capturas por rol (F09/F10/F11/U04/E01), llamada directa con las dos cuentas (E04/V01) y forzado de error (E03). Sin PM ni sin RDT en vivo.
Comandos (worktree): `npx vitest run src/lib/curva-s/curva-s.test.ts` 18/18 · `npm test` 102 archivos / 1063 tests verdes · `npx tsc --noEmit` 0 · `npm run lint` 27 problemas (9E/18W) = baseline `main`, 0 en mis archivos · `npx next build --webpack` exit 0.
Commit en `local-worker-5` (`git add` explícito). Sin push ni merge.

## Llamadas y contexto

≈ 42 llamadas. El Orquestador mide las cifras exactas con el script.

## Skills revisados

- `pg_control_proyectos/.claude/skills/`: `cerrar-tanda`, `seguir-flujo-de-planes`, `trasladar-hallazgos`, `verificar-permisos-por-rol`. Usado: `cerrar-tanda`. `verificar-permisos-por-rol` es de A y D, no de C; `seguir-flujo-de-planes` es del Orquestador; `trasladar-hallazgos` es de la tanda de documentación.
- `py_control_proyectos_web`: **no tiene** carpeta `.claude/skills/` (comprobado). Ninguno aplica.

## Fuentes de verdad revisadas

- Revisadas (solo lectura, sin editar): `docs/04-flujos-de-negocio/21-curva-s.md`, tabla 1 de `docs/04-flujos-de-negocio/14-accesos-y-restricciones.md`, `docs/05-diseno-y-referencias/design.md` (chip deshabilitado §253-254) y las fichas del plan por Grep de ID.
- Pendientes de decisión en Fase E (no editadas aquí): flujo 21 (BAC del modo físico y E01), flujo 14/16/21 con la fila de Curva S física/económica y `planes-futuros.md`.
