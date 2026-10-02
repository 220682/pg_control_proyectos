# Resumen de cierre — Tanda B

## Tanda, rol y modelo

Worker 1 (código) · `opencode-go/deepseek-v4.1-flash` · tanda **B** · carril único `local-worker-5` (worktree `py_control_proyectos_web\.worktrees\local-worker-5`). Depende de A (hecha, commit `d40cd74`).

## Estado de los ítems

| ID | Estado | Evidencia: comando o pantalla y resultado real | Causa y quién lo resuelve, si no es Conforme |
|---|---|---|---|
| F03 | Conforme | Servidor ya forzaba Parcial a rol sin economía (A, `page.tsx:112-113`); en B se completó el ocultado por `puedeEditarTipo`. `npx tsc --noEmit` = 0 | Prueba en vivo con BD en COMPLETO y rol sin economía: `Observado — pendiente de D` (navegador) |
| F04 | Conforme | Inspección ítem por ítem de `page.tsx` y componentes: cabecera USD, resumen, chip semáforo, dona, desempeño por partida, columnas PV/EV/AC/SPI/CPI y orden «mayor desviación» detrás de `puedeEditarTipo` | Captura: `Observado — pendiente de D` |
| F05 | Conforme | Parcial conserva filtros (`FiltrosDashboard`), % avance físico (TarjetaKpi siempre visible), matriz sin costo (`mostrarCosto={false}`), diagnóstico (`PanelDiagnostico`), Bloque E y enlace a Curva S | Captura: `Observado — pendiente de D` |
| F06 (B) | Conforme | `ToggleTipoDashboard` sigue renderizándose en ambos modos con `puedeEditar={puedeEditarTipo}`; `router.refresh()` ya existía (A). Alternancia en vivo: `Observado — pendiente de D` | — |
| F07 | Conforme | `hrefCurvaS = puedeEditarTipo ? '/curva-s' : '/curva-s?modo=fisica'`; Bloque E lo recibe y enlaza (mismo componente en ambos modos) | URL real verificable en D |
| F08 | Conforme | `CostoRealRecursos` solo si `puedeEditarTipo` (Completo): filas MO+HM con `descripcion`, fila «Sin resolver» si `≠ 0`, nota legacy no sumable, Total = AC | Suma manual en vivo: `Observado — pendiente de D` |
| D01 | Conforme | Query `pr_recursos` ahora selecciona `descripcion` y ordena por ella (`page.tsx:102-107`); el bloque la usa | — |
| D02 | Conforme | `npx vitest run src/lib/dashboard` → 4 files, 66 tests passed (6 nuevos en `costo-recursos.test.ts`: con/sin legacy, diferencia 0 y ≠ 0, corrida ≠ 0, vacío) | — |
| D04 | Conforme | Diff: no se tocó `evm.ts`, `dashboard.ts` (motor) ni SQL. Solo lectura desde `page.tsx` | — |
| D05 | Conforme | `reconciliarCostoRecursos({ ac: indicadoresProyecto.ac })`: mismo `AC` del KPI y del Total del bloque | Captura comparando: `Observado — pendiente de D` |
| U03 | Conforme | `CostoRealRecursos`: `tablaWrapClase` (scroll-x), `sticky top-0` por celda, `scope="col"` en cada `th`, `tabular-nums`, sin `max-w-*`; paleta de tokens | Captura: `Observado — pendiente de D` |
| U05 | Conforme | Ocultado por condicionales por bloque (sin placeholders): en Parcial no quedan huecos ni secciones vacías; el grid de gráficos se omite entero | Captura: `Observado — pendiente de D` |
| E02 | Conforme | `costo-recursos.test.ts`: sin filas y AC 0 → `mostrarDiferencia=false`; `CostoRealRecursos` devuelve estado vacío | Captura: `Observado — pendiente de D` |
| E03 | Conforme | Patrón existente: `FiltrosDashboard` atenúa con `opacity-50 transition-opacity` sin salto de layout; `ToggleTipoDashboard` ya maneja error de API con mensaje claro | Forzado de error en vivo: `Observado — pendiente de D` |

## Rama, commits y archivos tocados

- Rama `local-worker-5`, commit `94a5f79` (padre `d40cd74`, tanda A). Comprobado con `git branch --contains HEAD` → `* local-worker-5`. Sin push ni merge.
- Archivos: `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx`; `src/components/dashboard/BloqueE.tsx`, `FiltrosDashboard.tsx`, `MatrizPartidasDashboard.tsx`, `CostoRealRecursos.tsx` (nuevo); `src/lib/dashboard/costo-recursos.ts` (nuevo), `costo-recursos.test.ts` (nuevo).

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| B-H1 | regla de negocio acordada | En Parcial, el orden «mayor desviación de costo» se fuerza a `WBS` en el servidor aunque la URL traiga otro orden (es dinero derivado). La matriz igual llega en orden contractual. | Flujo 11 (Fase E del plan) |
| B-H2 | regla de negocio acordada | El `?modo=fisica` de la URL del enlace se pone en B; la API/lectura real del parámetro es Fase C. En B el enlace es solo navegación. | Flujo 21 / Fase C |
| B-H3 | observación sobre la política | El plan indexa PD5 como «los 10 KPI» (auditoría, L187) pero la lista cerrada oculta 6 KPI, no 10. El brief manda; implementé la lista del brief. | Auditor clasifica / Victor decide en Gate 2 |

## Traspaso

Tanda B cerrada. Dashboard Parcial sin ningún dato económico de la lista PD5 (conserva filtros, % avance físico, matriz sin costo, diagnóstico, PPC/Pareto y enlace a Curva S); Completo con `CostoRealRecursos` (Total = AC, reconciliación con legacy y «Sin resolver»). Bloque E y enlace a Curva S en ambos dashboards; desde Parcial sin economía `?modo=fisica`. `descripcion` añadida a la query de `pr_recursos`. Todo lo visual/URL queda `Observado — pendiente de D`.
Verificación: `npx tsc --noEmit` = 0; `npm test` = 102 files / 1057 tests passed; `npm run lint` = 27 problems (9 errors, 18 warnings), igual al baseline medido en `main`. Commit `94a5f79` en `local-worker-5`.
Pendiente: Fase C (lectura real del `?modo=`), Fase D (navegador), Fase E (flujos 11/21).

## Llamadas y contexto

~58 llamadas aproximadas (meta ~80). Las cifras exactas las mide el Orquestador.

## Skills revisados

- `pg_control_proyectos\.claude\skills\`: `cerrar-tanda` (usada), `verificar-permisos-por-rol` (no aplica: A/D; en B se conserva el permiso cerrado en A), `seguir-flujo-de-planes` (Orquestador), `trasladar-hallazgos` (Documentador).
- Repo de la app `py_control_proyectos_web`: no tiene carpeta `.claude/skills` (comprobado). Ninguno aplica.

## Fuentes de verdad revisadas

- Revisadas (no editadas): flujo `04-flujos-de-negocio/11-dashboard.md` y `21-curva-s.md`; `design.md` §4.1/§5/§8/§10/§11.
- Pendientes de decisión (Fase E): añadir a flujo 11 la lista cerrada PD5, Bloque E en ambos dashboards y el bloque «Costo real de recursos»; a flujo 21, el `?modo=fisica` en el enlace desde Parcial. El Worker de código no las edita.
