# Planes

## Qué vive acá

Un plan real por archivo (`YYYY-MM-DD-<tema>.md`), basado en la plantilla `02-plan.md`: contiene SDD, plan, Punch List, roles, decisiones y cierre — todo en un único archivo. El informe de auditoría de los planes nuevos (desde 2026-09-30) vive aparte en `../04-auditoria/`; los planes anteriores conservan el suyo dentro del archivo.

Las tareas ya cerradas migradas desde `docs/Tareas de implementacion/` (reestructuración documental, 2026-09-27) viven acá tal cual, como archivo histórico único (no se re-descomponen en plan/progreso/evidencia). Sus rutas internas antiguas no se corrigen — quedan como enlaces históricos.

`planes-futuros.md` es el último archivo fijo de esta carpeta: cola de pendientes que el Responsable humano decidió postergar explícitamente. No es un plan aprobado — no tiene progreso, evidencia ni Worker asignado.

## Índice

### En ejecución

| Plan | Estado |
|---|---|
| [`2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md`](2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md) | En ejecución (Worker, Fases 2–9 del plan) |
| [`2026-09-23-paquetes-de-trabajo.md`](2026-09-23-paquetes-de-trabajo.md) | Abierta — Fase 1 terminada; progreso y evidencia se crean al retomarla (D9, Gate 1 del 2026-09-27) |
| [`2026-09-22-plan-unico-orquestador-sesiones-worktrees-Claude-y-local.md`](2026-09-22-plan-unico-orquestador-sesiones-worktrees-Claude-y-local.md) | Ejecutado; pendiente de cierre 100% |

### Cerrados (históricos)

| Plan | Estado |
|---|---|
| [`2026-09-20-control-avance-plan-maestro.md`](2026-09-20-control-avance-plan-maestro.md) | Cerrada |
| [`2026-09-20-evm-fase-0-catalogo-unico.md`](2026-09-20-evm-fase-0-catalogo-unico.md) | Cerrada |
| [`2026-09-20-sub-lote-2-alcance-proyecto.md`](2026-09-20-sub-lote-2-alcance-proyecto.md) | Cerrada — evidencia externa: artifact [Sub-lote 2 — Checklist F0-F7](https://claude.ai/artifact/Xv6wSxUA2fbXaFX8ACe1rh) |
| [`2026-09-21-evm-fase-1-congelar-tarifa.md`](2026-09-21-evm-fase-1-congelar-tarifa.md) | Cerrada |
| [`2026-09-21-fix-reemplazar-dp.md`](2026-09-21-fix-reemplazar-dp.md) | Cerrada |
| [`2026-09-21-pr-fase-1-pipeline-rdt.md`](2026-09-21-pr-fase-1-pipeline-rdt.md) | Completa, verificada y mergeada (PR #13) |
| [`2026-09-21-pr-fase-2-pipeline-linea-base.md`](2026-09-21-pr-fase-2-pipeline-linea-base.md) | Completa, verificada y mergeada (PR #14) |
| [`2026-09-21-dashboard-fase-3-agente-c.md`](2026-09-21-dashboard-fase-3-agente-c.md) | Implementada y verificada (Punch List 25/25) — evidencia externa: artifact [Dashboards y Curva S — Fase 3](https://claude.ai/artifact/CdUMm5cdoxGjYPUsMHM85q) |
| [`2026-09-21-curva-s-fase-3-agente-d.md`](2026-09-21-curva-s-fase-3-agente-d.md) | CERRADO (Punch List 20/20, PR #16 mergeado) — misma evidencia externa que Dashboard Fase 3 |
| [`2026-09-23-reordenamiento-y-actualizacion-fuentes-de-verdad.md`](2026-09-23-reordenamiento-y-actualizacion-fuentes-de-verdad.md) | Ejecutado |
| [`2026-09-27-paneles-servicio-persistente.md`](2026-09-27-paneles-servicio-persistente.md) | Cerrada (Gate 2 aprobado por Victor, 2026-09-30) — Punch List 181 ítems: 173 Conforme, 7 Observado por causas externas o pasos de Victor, 1 No aplica; código mergeado a `main` de la app (`45c9e0a`); Informe de Auditoría «Apto para Gate 2» |

### En preparación

| Plan | Estado |
|---|---|
| [`2026-09-30-niveles-presupuesto-y-cronograma.md`](2026-09-30-niveles-presupuesto-y-cronograma.md) | Spec aprobado (Gate Spec 2026-09-30); plan conjunto entregado |
| [`2026-09-30-paquetes-y-plan-maestro-grilla.md`](2026-09-30-paquetes-y-plan-maestro-grilla.md) | Spec aprobado (Gate Spec 2026-09-30); plan conjunto entregado |
| [`2026-09-30-rdt-desde-plan-maestro.md`](2026-09-30-rdt-desde-plan-maestro.md) | Spec aprobado (Gate Spec 2026-09-30); plan conjunto entregado |
| [`2026-09-30-niveles-paquetes-plan-maestro-rdt.md`](2026-09-30-niveles-paquetes-plan-maestro-rdt.md) | **Planificando** — plan conjunto de los tres Specs (19 tandas, 4 carriles, 109 ítems); pendiente del Gate 1 de Victor |

Ver [`planes-futuros.md`](planes-futuros.md) para ideas pendientes de Spec/SDD.

### Eliminado (no migrado)

`2026-09-23-cronograma-import-y-versatilidad-vinculo.md` — eliminado con `git rm` por decisión de Victor en el Gate 1 del plan de reestructuración documental (2026-09-27, §4.5 de ese plan). No se migró.

### Evidencia externa sin dueño único

La **Matriz de Accesos y Restricciones** (artifact de evidencia externa) no tiene un dueño único claro entre `04-flujos-de-negocio/14-accesos-y-restricciones.md` y `2026-09-20-sub-lote-2-alcance-proyecto.md` — queda reportada en §14 del plan de reestructuración documental para que el Responsable humano decida.

## Qué no vive acá

Nada se borra. Un plan cerrado permanece íntegro, indefinidamente.

## Qué leer después

El propio archivo de plan del tema activo, más su `02-progreso/`, `03-evidencia/` y `04-auditoria/` homónimos si existen.
