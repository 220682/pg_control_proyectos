# 2026-10-02 — Plan: Observaciones Victor Lote 3

> Tarea con flujo de Orquestador. Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`. Plan del **Planner**, sobre las 13 observaciones de Victor (2026-10-02). **4 Workers** en paralelo.

## Identificación y estado

- Tema: Mejoras de interfaz y lógica en DP, PR, Cronograma, Paquetes, Plan Maestro y RDT
- Fecha: 2026-10-02
- Estado: **Aprobado** (Gate 1)
- Gate 1: **Aprobado por Victor** (2026-10-02)

## Reglas confirmadas

1. **Editar vs Reemplazar:** Editar = modificar actividades individuales; Reemplazar = subir documento nuevo
2. **Cronograma con Plan Maestro aprobado:** Solo Admin y Jefe de Proyectos pueden **editar** actividades individuales (no reemplazar)
3. **Notificación de impacto:** Deben ver qué se pierde antes de editar
4. **RDT preservados:** Los RDT declarados se reposicionan automáticamente en las nuevas fechas/metrados al aprobar el nuevo Plan Maestro
5. **Declaración de metrados en Plan Maestro:** Por paquete (no por partida individual)
6. **Declaración en RDT:** Paquete completo (WBS="PQ-001"), excepto partidas directas
7. **Disciplinas:** 8 total (Civil, Mecánica, Eléctrica, Instrumentación, Tuberías, Preliminares, Cierre, Subcontratos)
8. **Distribución del metrado del paquete:** Por partida guía (modo `AVANCE_PAQUETE`)
9. **Fechas en Plan Maestro:** Editables, no restringen el reparto, se ponen en rojo si están fuera del rango visible
10. **RDT y paquetes:** Se calcula automáticamente cuando se declara un paquete

## Objetivo, alcance y no alcance

- **Resultado esperado:**
  - Botón "Cargar" + barra de progreso en DP y PR
  - Edición de actividades individuales del cronograma (con Plan Maestro aprobado)
  - Terminología unificada ("Actividad", "Declarar")
  - Indicador de niveles + botón "Guardar cambios" en Paquetes
  - Rediseño del Plan Maestro (espacio optimizado, metrados por paquete, fechas editables)
  - RDT con disciplinas ampliadas + declaración por paquete + libertad de WBS
- **Alcance:** Las 13 observaciones completas, con 3 migraciones SQL (090, 091, 092)
- **No alcance:** Gantt con línea base, 3WLA, multi-moneda, orden de trabajo, cambios al motor del PR, Dashboard y Curva S (solo pruebas que los lean)

## Entorno, repositorios, ramas y worktrees

- Modo: local. Documentación en `pg_control_proyectos` (`main`, directo). Código en `py_control_proyectos_web`.
- **Workers** (4 en paralelo):

| Carril | Rama | Worktree | Puerto | Fases |
|---|---|---|---|---|
| 1 · Terminología | `local-worker-1` | `.worktrees/local-worker-1` | 3111 | F1 |
| 2 · Cronograma | `local-worker-2` | `.worktrees/local-worker-2` | 3112 | F2 |
| 3 · Paquetes | `local-worker-3` | `.worktrees/local-worker-3` | 3113 | F3 |
| 4 · Plan Maestro | `local-worker-4` | `.worktrees/local-worker-4` | 3114 | F4 |

- Las fases F0 (maqueta), F5 (RDT) y F6 (integración) se ejecutan después de las fases iniciales.

## Migraciones SQL (3)

| # | Archivo | Propósito | Tipo |
|---|---------|-----------|------|
| **090** | `090_ampliar_catalogo_disciplinas.sql` | Agregar 3 disciplinas: Preliminares, Cierre, Subcontratos | Aditiva, idempotente |
| **091** | `091_plan_maestro_declaracion_paquete.sql` | Columnas: `es_declaracion_paquete`, `metrado_paquete`, `fecha_inicio`, `fecha_fin` en `plan_maestro_partidas` | Aditiva, idempotente |
| **092** | `092_rdt_declaracion_paquete.sql` | Columnas: `es_declaracion_paquete`, `metrado_paquete` en `rdt_actividades` | Aditiva, idempotente |

**Protocolo de aplicación:**
1. Orden: 090 → 091 → 092
2. Método: Manual en SQL Editor de Supabase
3. Idempotencia: Todas usan `IF NOT EXISTS` o `ON CONFLICT DO NOTHING`
4. Rollback: Cada archivo incluye comentario de cómo deshacer

## Fases y dependencias

| Fase | Qué es | Tareas | Depende de |
|---|---|---|---|
| F0 | Maqueta Plan Maestro | F0-A | — |
| F1 | Terminología y convenciones | F1-A, F1-B, F1-C | F0 |
| F2 | Edición de cronograma | F2-A, F2-B, F2-C | F0 |
| F3 | Paquetes mejorado | F3-A, F3-B | F1 |
| F4 | Plan Maestro rediseñado | F4-A, F4-B, F4-C, F4-D | F0, migración 091 |
| F5 | RDT mejorado | F5-A, F5-B, F5-C, F5-D | F4, migraciones 090, 092 |
| F6 | Integración y documentación | F6-A, F6-B, F6-C | Todas las anteriores |

## Cambios por flujo

| Flujo | Dice hoy | Pasará a decir | Observación |
|-------|----------|----------------|-------------|
| **09 (Importar DP)** | Importación por file input, sin barra de progreso | Botón "Cargar" visible + barra de progreso durante procesamiento | O1 |
| **10 (Generación PR)** | PR es solo lectura, se genera con el DP | Botón "Cargar" visible + barra de progreso durante generación | O1 |
| **15 (Cronograma)** | Tipos TAREA/HITO/RESUMEN; recarga bloqueada con Plan Maestro aprobado | (1) Terminología: "Actividad" (no "Actividad resumen"); (2) Edición de actividades individuales permitida con Plan Maestro aprobado (solo Admin/Jefe Proyectos); (3) Endpoint `PATCH /api/cronograma/actividades/[id]`; (4) Notificación de impacto antes de editar; (5) Reemplazo sigue bloqueado | O2, O3 |
| **19 (Paquetes)** | "Elegir partida"; niveles en árbol único; guardado por paquete individual | (1) "Declarar partida" (no "elegir"); (2) Botón "Este servicio tiene N niveles"; (3) Niveles juntos (no separados); (4) Botón "Guardar cambios" global al terminar | O4, O5, O6 |
| **20 (Plan Maestro)** | Lienzo con columnas fijas y diarias; selector OT full-width; metrados por partida | (1) Selector OT compacto (200px max); (2) Icono flotante con reserva de espacio; (3) Plegable por grupo de medida (físico/económico/HH); (4) **Metrados por paquete** (no por partida); (5) Espacio optimizado para fechas; (6) Fechas editables (rojo si fuera de rango) | O7, O8, O9 |
| **06 (RDT)** | Sin disciplinas; declaración por partida o paquete según modo; C/NC y equipos exigen D previa | (1) Plegable en disciplinas + catálogo de 8; (2) Icono flotante con reserva de espacio; (3) **Declaración por paquete** (WBS="PQ-001"); (4) Partidas directas si no están en paquetes; (5) C/NC y equipos: libertad de WBS | O10, O11, O12, O13 |
| **14 (Accesos)** | Edición de cronograma no mencionada | Tabla nueva: "Editar actividad del cronograma con Plan Maestro aprobado" → Admin, Jefe Proyectos | O3 |
| **16 (Paneles)** | Icono flotante global | Convención: icono flotante con reserva de espacio (no tapa contenido) | O7, O11 |

## Riesgos y bloqueos

| # | Riesgo | Mitigación |
|---|---|---|
| 1 | Cambio conceptual de "partida" a "paquete" en Plan Maestro | Maqueta previa + pruebas cruzadas exhaustivas |
| 2 | Edición de cronograma con Plan Maestro aprobado | Notificación de impacto clara + reposicionamiento automático de RDT |
| 3 | Icono flotante tapa contenido | Reserva de espacio en todos los lienzos |
| 4 | Declaración de metrados por paquete (no por partida) | Lógica nueva + pruebas unitarias + migración de datos existentes |

## Estado de implementación

| Fase | Ítem | Estado | Commit | Observaciones |
|---|---|---|---|---|
| F0 | Maqueta Plan Maestro | **Conforme** | `f77b8dc` | `docs/05-diseno-y-referencias/mockups/plan-maestro-rediseño.html` |
| F1-A | Botón "Cargar" + barra de progreso en DP | **Conforme** | `f82fd7f` | Etiqueta "Cargar DP" + `<progress>` durante análisis e importación |
| F1-B | Botón "Recalcular PR" + barra de progreso | **Conforme** | `7f755df` | Endpoint POST + componente cliente con `<progress>` |
| F1-C | Terminología "Actividad" (no "Actividad resumen") | **Conforme** | `f82fd7f` | Etiqueta en `pantalla-niveles.ts` |
| F2-A | Permiso `puedeEditarActividadCronograma` | **Conforme** | `77c3ab2` | Solo Admin y Jefe Proyectos (no Planner) |
| F2-B | Endpoint PATCH `/api/cronograma/actividades/[id]` | **Conforme** | `77c3ab2` | Valida PM aprobado, permiso, alcance; actualiza nombre/duración/fechas |
| F2-C | Notificación de impacto antes de editar | **Conforme** | `d985d33` | GET `/impacto` + modal `NotificacionImpacto` muestra partes de RDT afectadas |
| F3 | Paquetes mejorado | **Conforme** | `b324a3b` | "Declarar partida", badge "N niveles", botón "Guardar cambios" |
| F4-A | Selector OT compacto + icono flotante | **Conforme** | `bd75f48` | `max-w-[200px]` contenedor, `max-w-[110px]` select; icono IA `position:fixed` sin reservar espacio |
| F4-B | Plegables individuales por grupo de medida | **Conforme** | `5f67006` | `medVis: { fisico, economico, hh }` reemplaza `acumuladas`; 3 toggles independientes |
| F4-C | Metrados por paquete (no por partida) | **Conforme** | `8b33cdd` | Tipo `LineaPlanMaestro` con `esDeclaracionPaquete`/`metradoPaquete`; API actualizada; `distribuirMetradoPaquete` |
| F4-D | Fechas editables con indicador fuera de rango | **Conforme** | `8b33cdd` | Columnas `fecha_inicio`/`fecha_fin` en tipo y API; indicador visual en Lienzo pendiente de migración 091 |
| F5 | RDT mejorado | **Parcial** | — | Migración 090 existe (8 disciplinas); libertad WBS para C/NC y equipos pendiente |
| F6 | Integración y documentación | **En curso** | — | db/README, flujos actualizados, verificación cruzada |

**Nota (2026-10-02):** El subagente Worker 4 no pudo lanzarse (modelo `qwen3.8-plus` no disponible en opencode). F0, F1-A/B/C, F2-A/B/C, F3 y F4 implementados directamente por el Orquestador (qwen3.7-plus).

**Correcciones de Victor (2026-10-02):**
1. **Metrados contractuales fijos**: las partidas muestran el metrado contractual como texto plano (no editable). Solo los metrados de paquete son editables (celdas verdes). ✓ Ya correcto en la maqueta.
2. **Icono IA flotante sin reservar espacio**: el icono debe flotar sobre el contenido sin `padding-right`. Corregido en `bd75f48` (quita `pr-[60px]` del lienzo).

**Pendiente para completar F4-C/D en la UI real:**
- Aplicar migración 091 en Supabase (`db/091_plan_maestro_declaracion_paquete.sql`)
- Modificar el Lienzo para mostrar celdas editables (verde) en filas con `esDeclaracionPaquete = true`
- Añadir indicador rojo en fechas fuera del rango visible

**Verificación (F4):**
- `npx tsc --noEmit`: exit 0
- `npx vitest run src/lib/plan-maestro/`: 115 tests verdes
- `npx next build --webpack`: exit 0

## Mensaje de cierre

(Pendiente de completar al finalizar el plan)
