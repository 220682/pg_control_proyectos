# Resumen de checklists

Registro cronológico de todos los checklists de verificación en vivo (Punch List de Mejoras) creados desde el 21-sep-2026 en adelante. Un checklist = una fase o sub-lote de una implementación, aunque la implementación completa de un flujo haya quedado seccionada en varias fases o sub-lotes con su propio checklist cada una.

**Regla:** toda implementación debe tener su checklist en la Punch List, así se haya seccionado en varias fases — cada fase/sub-lote es su propio checklist, no se mezclan puntos de dos fases distintas en un mismo checklist.

No incluye checklists anteriores al 21-sep-2026 (por ejemplo "Lote 24-ago" o "UI unificada"), que siguen viviendo solo en la Punch List sin registrar aquí.

Los datos de ítems/estado se toman de la Punch List de Mejoras (artifact `8yHL1cn8auxbYghuRoiNhd`) al momento de actualizar esta tabla — no se mantienen en vivo, así que pueden quedar desactualizados entre sesiones; para el estado exacto actual, revisar la Punch List directamente.

## Flujo 020 — Plan Maestro

| # | Fecha | Fase / sub-lote | Checklist (Punch List) | Documentado en Mejoras continuas | Ítems | Conforme | Observado | Sin verificar | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-09-20/21 | Sub-lote 1 — RDT rechazo + historial | "RDT: rechazo visible con motivo + historial de corrección" | [2026-09-20-control-avance-plan-maestro.md](2026-09-20-control-avance-plan-maestro.md) | 30 | 29 | 1 | 0 | **Cerrado 100%** — verificación visual completa y migraciones 041-044 aplicadas en Supabase (2026-09-21). Ítem 14 sigue Observado en la Punch List pero sin impacto: la regla "cada partida jala su WBS" se cumple automáticamente, la validación de bloqueo quedó sin efecto por diseño |
| 2 | 2026-09-20 | Sub-lote 2 — Alcance por OT sobre permisos por rol | "Sub-lote 2: Alcance por OT sobre permisos por rol" | [2026-09-20-sub-lote-2-alcance-proyecto.md](2026-09-20-sub-lote-2-alcance-proyecto.md) | 7 | 7 | 0 | 0 | **Cerrado 100%** |
| 3 | 2026-09-20/21 | EVM Fase 0 — Catálogo único de cargos/equipos | "EVM Plan Maestro — Fase 0: catálogo único de cargos/equipos" | [2026-09-20-evm-fase-0-catalogo-unico.md](2026-09-20-evm-fase-0-catalogo-unico.md) | 11 | 11 | 0 | 0 | **Cerrado 100%** |
| 4 | 2026-09-21 | EVM Fase 1 — Congelar tarifa al validar RDT | "EVM Plan Maestro — Fase 1: congelar tarifa al Validar RDT" | [2026-09-21-evm-fase-1-congelar-tarifa.md](2026-09-21-evm-fase-1-congelar-tarifa.md) | 5 | 5 | 0 | 0 | **Cerrado 100%** |
| 5 | 2026-09-21 | Fix — reemplazar_dp no borraba partidas/recursos viejos | *(sin checklist propio en Punch List — fix puntual)* | [2026-09-21-fix-reemplazar-dp.md](2026-09-21-fix-reemplazar-dp.md) | — | — | — | — | **Cerrado 100%** — verificado en vivo por Victor |

**Totales flujo 020 (al 21-sep-2026):** 4 checklists con Punch List · 53 ítems · 53 Conforme · 1 Observado (sin impacto) · 0 Sin verificar · **Todos los sub-lotes/fases abiertos quedaron Cerrados 100%.**

## Flujo 010 — Generación PR

| # | Fecha | Fase / sub-lote | Checklist (Punch List) | Documentado en Mejoras continuas | Ítems | Conforme | Observado | Sin verificar | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-09-21 | PR Fase 1 (Agente A) — pipeline RDT → PR | "PR enriquecido — Fase 1: pipeline RDT → PR" | [2026-09-21-pr-fase-1-pipeline-rdt.md](2026-09-21-pr-fase-1-pipeline-rdt.md) | 19 | 19 | 0 | 0 | **Cerrado 100%** — verificado con Playwright + login real contra Supabase real. Mergeado en `py_control_proyectos_web` [PR #13](https://github.com/220682/py_control_proyectos_web/pull/13) (2026-09-21 16:20) |
| 2 | 2026-09-21 | PR Fase 2 (Agente B) — línea base, planificado y derivados EVM | "PR Fase 2 — línea base, planificado y derivados EVM" | [2026-09-21-pr-fase-2-pipeline-linea-base.md](2026-09-21-pr-fase-2-pipeline-linea-base.md) | 15 | 15 | 0 | 0 | **Cerrado 100%** — verificado con Playwright + login real contra Supabase real. Mergeado en `py_control_proyectos_web` [PR #14](https://github.com/220682/py_control_proyectos_web/pull/14) (2026-09-21 18:05), después de A |

**Totales flujo 010 (al 21-sep-2026):** 2 checklists con Punch List · 34 ítems · 34 Conforme · 0 Observado · 0 Sin verificar · **Ambas fases cerradas 100% y mergeadas a main en `py_control_proyectos_web`.** Efecto conjunto: la cadena RDT → PR → Dashboard queda cerrada en código — el Dashboard ya muestra indicadores reales en vez de "Pendiente".

**Pendiente de decisión de Victor** (no bloqueante, anotado en el cierre de PR Fase 1): tarifa retroactiva para los RDT que ya estaban validados antes de esta sesión — quedan con `costo_real_acum = 0` en el motor nuevo porque no se quiso re-resolver la tarifa de hoy sobre RDT validados hace semanas sin una decisión explícita.

## Flujo 011 — Dashboard

| # | Fecha | Fase / sub-lote | Checklist (Punch List) | Documentado en Mejoras continuas | Ítems | Conforme | Observado | Sin verificar | Estado |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-09-21 | Dashboard Fase 3 (Agente C) — los dos Dashboards: Parcial mejorado y Completo construido | "Dashboard Fase 3 — los dos Dashboards" | [2026-09-21-dashboard-fase-3-agente-c.md](2026-09-21-dashboard-fase-3-agente-c.md) | 25 | — | — | — | **Plan inicial — pendiente de aprobación de Victor.** Punch List todavía no cargada; la implementación no arranca sin ella |
| 2 | 2026-09-21 | Curva S Fase 3 (Agente D) — serie temporal PV/EV/AC en pantalla propia | "Curva S Fase 3 — serie temporal PV/EV/AC" | [2026-09-21-curva-s-fase-3-agente-d.md](2026-09-21-curva-s-fase-3-agente-d.md) | 20 | — | — | — | **Plan inicial — pendiente de aprobación de Victor.** Incluye una decisión previa (D0: ubicación y nombre del chip) que Victor confirma antes de que el agente escriba código de navegación |

**Nota:** estas dos filas se agregan con la Punch List **propuesta**, no cargada. Al aprobarlas, se cargan en la Punch List de Mejoras y esta tabla se actualiza con los conteos reales, igual que las fases anteriores.

## Cómo se actualiza esta tabla

Al cerrar cada sesión (o al menos al cerrar un checklist), agregar o actualizar la fila correspondiente con el conteo real leído de la Punch List. Un checklist nuevo (nueva fase, nuevo sub-lote, nueva mejora) siempre se agrega como fila nueva, nunca se reemplaza una fila existente salvo para actualizar sus conteos.
