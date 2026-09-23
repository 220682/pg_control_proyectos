# 10 — Generación PR

Independiente de importar DP (usa datos del DP, pero es otro flujo). Spec `2026-08-16-pr`, ampliado en PR Fase 1 ([2026-09-21-pr-fase-1-pipeline-rdt.md](../Tareas%20de%20implementacion/2026-09-21-pr-fase-1-pipeline-rdt.md)) y PR Fase 2 ([2026-09-21-pr-fase-2-pipeline-linea-base.md](../Tareas%20de%20implementacion/2026-09-21-pr-fase-2-pipeline-linea-base.md)).

## Qué es el PR

El PR es la tabla que consolida todo lo que alimenta al Dashboard: una sola fila por partida (`pr_partidas`), más una cabecera por proyecto (`proyecto_pr`). No es la fuente original del alcance ni del cronograma — es la capa de consolidación entre plan y real.

Regla de oro: lo que cambia cuando ocurre un hecho (se importa un DP, se aprueba un Plan Maestro, se valida un RDT) **se materializa** (el pipeline lo escribe en una columna); lo que depende de la fecha de corte o es derivación pura (PV, EV, CPI, SPI, PPC…) **se calcula al leer**.

## Tres bloques

```text
A. LÍNEA BASE (CONTRACTUAL — DP)  |  B. ACUMULADO REAL (RDT → PR)  |  C. DERIVADOS (EVM CALCULADO)
```

### A — Línea base contractual

Origen: DP, hoja CD (costo directo, regla 9 de [18-control-avance.md](18-control-avance.md)). Se llena en `reemplazar_dp()` al importar el DP.

- `hh_contractual` = `hh_und_partida × metrado_contractual`.
- `bac` = `metrado_contractual × precio_unitario`, en USD.

### A' — Planificado

Origen: Plan Maestro aprobado y Cronograma. Se recalcula cuando se aprueba una versión nueva del Plan Maestro (la anterior pasa a `REEMPLAZADO`, sin dejar rastro en el PR).

- `metrado_planificado_acum`: suma de `plan_maestro_asignaciones` de la versión `APROBADO`, por partida.
- `fecha_inicio_base` / `fecha_fin_base`: desde `cronograma_actividad_partidas` — inicio es la fecha más temprana de las actividades vinculadas a la partida, fin la más tardía. Se recalculan cuando cambia el vínculo cronograma ↔ partida.

PV **no se almacena** aquí — depende de la fecha de corte y se calcula al leer (bloque C).

### B — Ejecución real

Origen: RDT validado. Toda actividad (D, C y NC) se carga a una partida (regla 12 de negocio) — solo las D generan metrado ejecutado; C y NC aportan horas y costo, no avance.

- `metrado_acumulado`, `hh_reales_acum`, `hh_d_acum`, `hh_c_acum`, `hh_nc_acum`, `hm_reales_acum`, `costo_real_acum`, `actividades_acum`, `actividades_con_cnc_acum`.
- A nivel proyecto (`proyecto_pr`): `hh_mo_indirecta_acum` (MOI, horas sin costo — regla 10 de negocio), y el balde `*_legacy_sin_partida_acum` (solo RDT anteriores a la regla 12, que no se pueden reasignar retroactivamente).

### C — Derivados EVM

No se almacena. Se calcula al leer en `src/lib/pr/evm.ts` — funciones puras sobre las columnas de A/A'/B. Reutiliza lo que ya existe en `src/lib/dashboard/dashboard.ts` (PV al corte, SV, SPI, CPI, EAC, IP) sin modificarlo.

| Indicador | Fórmula |
|---|---|
| BAC | `metrado_contractual × precio_unitario` (partida) · suma (proyecto). Costo directo |
| PV al corte | `Σ metrado_planificado × PU` hasta la fecha de corte. "Pendiente" sin Plan Maestro aprobado |
| % avance físico | `metrado_acumulado / metrado_contractual` |
| EV | `metrado_acumulado × precio_unitario` — no sale del dinero gastado |
| AC | `costo_real_acum` (partida) · suma + balde legacy (proyecto). Costo directo |
| % trabajo productivo | `hh_d_acum / hh_reales_acum` |
| SV / CV | `EV − PV` · `EV − AC` |
| SPI / CPI | `EV / PV` · `EV / AC` |
| HH ganadas | `% avance físico × hh_contractual` |
| IP | `HH ganadas / HH reales` |
| EAC / VAC | `BAC / CPI` · `BAC − EAC` |
| Metrado restante | `contractual − acumulado`, con alerta si sale negativo (sobre-ejecución) |
| HH restantes | `hh_contractual − hh_reales_acum` |
| Rendimiento real vs base | `metrado ejecutado / HH reales` contra `hh_und_partida` |
| PPC | `(actividades_acum − actividades_con_cnc_acum) / actividades_acum × 100`, a nivel proyecto |

Todo indicador se rotula con nombre, fórmula y unidad — nunca solo la sigla. PPC y SPI se muestran separados, nunca mezclados (regla de [18-control-avance.md](18-control-avance.md)). Sin dato suficiente (ej. denominador en 0, sin Plan Maestro aprobado), el indicador muestra "Pendiente", nunca 0 ni un número inventado.

## Pipeline: cuándo se recalcula cada bloque

| Bloque | Se dispara desde | Función |
|---|---|---|
| A | Importar DP | `reemplazar_dp()` (extendida en `db/060`) |
| A' — planificado | Aprobar Plan Maestro | `recalcular_pr_planificado()` (`db/061`) |
| A' — fechas base | Guardar vínculo Cronograma ↔ DP (automático o manual) | `recalcular_pr_fechas_base()` (`db/062`) |
| B | Validar/corregir/rechazar/borrar un RDT, o reimportar un DP | `recalcular_pr_desde_rdt()` (`db/053`) — de recálculo completo, no incremental |

Reimportar un DP borra y reconstruye el PR contractual (`delete from proyecto_pr` + insert); para no perder la ejecución real acumulada, `reemplazar_dp()` llama a `recalcular_pr_desde_rdt()` al final, así el lado real se reconstruye desde los RDT ya validados en la misma transacción.

## Pantalla

`src/app/(workspace)/proyectos/[id]/pr/page.tsx`. Tabla larga con scroll horizontal, columnas de identificación de partida (WBS, descripción, unidad) fijas a la izquierda, encabezado de dos filas (grupo de bloque + columna) sticky en la celda. Fila de total del proyecto al pie — el total físico va como N/A (no se suman unidades físicas incompatibles entre partidas) y la variación global se expresa en valor económico. Fecha de corte siempre visible. Diseño según `docs/visual-companion/design.md`.

## Relación con Dashboard

El Dashboard lee las mismas columnas que este flujo llena — no necesita cambios de código para reflejar datos reales; el semáforo, antes en `PENDIENTE` por falta de dato (AC = 0), toma color real en cuanto el PR se llena.
