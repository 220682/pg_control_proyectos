# 2026-10-02 — Plan: Observaciones Victor Lote 3

> Tarea con flujo de Orquestador. Estándar: `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`. Plan del **Planner**, sobre las 13 observaciones de Victor (2026-10-02).
>
> **Corrección de alcance (2026-10-03, Orquestador):** el plan se escribió para 4 Workers en paralelo, pero la realidad es **un solo carril** (`local-worker-4`, worktree `.worktrees/local-worker-4`) con tandas **secuenciales**, porque F0–F4 y F6 los implementó el Orquestador anterior sin Workers y las fases que quedan (E y F) comparten worktree y migraciones. La tabla de carriles de § «Entorno» describe el diseño original, no el estado real.

## Identificación y estado

- Tema: Mejoras de interfaz y lógica en DP, PR, Cronograma, Paquetes, Plan Maestro y RDT
- Fecha: 2026-10-02
- Estado: **CERRADO** (Gate 2 de Victor, 2026-10-04)
- Puertas (las lee `scripts/verificar.ps1`):
  - Gate Spec: no consta — el Lote 3 no tiene Spec/SDD propio; el Gate 1 se aprobó sobre este mismo plan, que contiene las 13 observaciones y las 10 reglas confirmadas. Queda registrado como observación sobre la política (OP2) para el Auditor: no se inventa un Spec retroactivo.
  - Gate 1: aprobado por Victor (2026-10-02)
  - Gate 2: **aprobado por Victor (2026-10-04)**

## Reglas confirmadas

> **Enmienda E1 (Victor, 2026-10-03):** las reglas **2**, **3** y **4** de esta lista quedaron **derogadas** y reemplazadas por las reglas del **umbral** (ver § Enmienda E1). La regla 4 era correcta en el fondo pero decía el disparador equivocado: el reposicionamiento ocurre **al aprobar un Plan Maestro nuevo**, no al editar una actividad.

1. **Editar vs Reemplazar:** Editar = modificar actividades individuales; Reemplazar = subir documento nuevo — **regla derogada por E1** (con Plan Maestro aprobado no se edita el cronograma en absoluto).
2. ~~**Cronograma con Plan Maestro aprobado:** Solo Admin y Jefe de Productos pueden editar actividades individuales~~ — **DEROGADA (E1)**, con su regla 3.
3. ~~**Notificación de impacto:** Deben ver qué se pierde antes de editar~~ — **DEROGADA (E1)**: el endpoint de impacto se elimina.
4. ~~**RDT preservados: se reposicionan al aprobar el nuevo Plan Maestro**~~ — **SUSTITUIDA (E1) por la regla del umbral U4**, que además alcanza a los RDT **validados**.
5. **Declaración de metrados en Plan Maestro:** Por paquete (no por partida individual)
6. **Declaración en RDT:** Paquete completo (WBS="PQ-001"), excepto partidas directas
7. **Disciplinas:** 8 total (Civil, Mecánica, Eléctrica, Instrumentación, Tuberías, Preliminares, Cierre, Subcontratos)
8. **Distribución del metrado del paquete:** Por partida guía (modo `AVANCE_PAQUETE`)
9. **Fechas en Plan Maestro:** Editables, no restringen el reparto, se ponen en rojo si están fuera del rango visible
10. **RDT y paquetes:** Se calcula automáticamente cuando se declara un paquete

## Enmienda E1 — «El Plan Maestro es el umbral» (Victor, 2026-10-03)

> Redactada por el **Orquestador**: en este harness no hay subagente `Planner`, y las reglas las dictó Victor en conversación, no en un Spec previo. Se presenta como **Gate 1 Complementario** antes de implementar. Contexto: el ítem 5 de la Tanda F quedó detenido (OP8) porque el reposicionamiento aparecía con dos disparadores; al confirmar el de Victor, la falta de coherencia resultó ser más ancha que ese ítem.

### Las cinco reglas del umbral

| ID | Regla |
|---|---|
| **U1** | El RDT se genera **solo** cuando el Plan Maestro está **aprobado** y el servicio está en **Ejecución**. Las dos condiciones, no una |
| **U2** | **Antes** de aprobar el Plan Maestro se pueden editar: DP, PR, cronogramas, paquetes y el propio Plan Maestro |
| **U3** | **Aprobado** el Plan Maestro, **lo único editable es el Plan Maestro** (mediante versión nueva con motivo obligatorio). Quedan **congelados** DP, PR, cronogramas y paquetes. Lo **administrativo** (checklist, notificaciones y datos del servicio) sigue funcionando normal |
| **U4** | El **reposicionamiento** de los RDT en **fechas y metrados** ocurre **solo** al aprobar un Plan Maestro nuevo, y alcanza a **todos** los RDT, **incluidos los validados** |
| **U5** | El Plan Maestro **no puede dejar de contemplar ninguna partida**: al modificarlo solo se **mueven partidas** y se **crean o desagrupan paquetes**. Nunca se elimina una partida del plan — por eso no puede quedar un RDT sin partida |
| **U6** | Al aprobar un Plan Maestro nuevo, **antes** de confirmar se muestra **qué RDT van a cambiar** (cuántos, y con qué fechas y metrados). Es el aviso de impacto que R1 retira del cronograma, trasladado al momento correcto |
| **U7** | El reposicionamiento **deja rastro**: cada RDT afectado registra en su historial el plan anterior, el plan nuevo y su versión, el diff de claves y quién aprobó el Plan Maestro. **La fecha y el metrado no se guardan** (precisión del 2026-10-04): el `snapshot` no los tiene como dato consultable. U4 modifica datos validados, así que sin historial sería un cambio invisible |
| **U8** | El orden al aprobar es **Plan Maestro → reposicionamiento de RDT → recálculo del PR**, y es **todo o nada**: si algo falla, no queda aprobado nada |
| **U9** | U3 congela los datos de **planeación** (DP, PR, cronogramas, paquetes, Plan Maestro), **no el registro de ejecución**. Por tanto: **cualquier vía de creación de un RDT** —incluida la carga por archivo— exige las dos condiciones de U1. Una vez que el RDT **existe**, las acciones sobre él —reasignarle el paquete, corregirlo, validarlo o rechazarlo— siguen exigiendo **solo Plan Maestro aprobado** (precisión del 2026-10-04): la segunda condición, servicio en Ejecución, es de **creación**, no de operación |
| **U10** | El congelamiento de U3 alcanza también **reordenar** paquetes (`MOVER`): con Plan Maestro aprobado no se crean, editan, archivan **ni reordenan** paquetes, ni se declaran vínculos. Deroga la lectura de que `MOVER` era solo orden de presentación (decisión de Victor, 2026-10-04) |

### Aclaración de U4 (Victor, 2026-10-04)

> «Cargo los datos que se extrajeron del RDT para reposicionarlos en el nuevo Plan Maestro. Pero lo que no se está entendiendo hasta ahora es que, aunque se cambie el Plan Maestro, **el PR sigue conservando los datos de todos los RDTs porque estos no se han cambiado**. Lo que se cambia es **la forma en que se muestran en el Plan Maestro**; no cambia la forma en que están declarados en el PR (consolidado).»

Consecuencia implementable: el reposicionamiento **re-vincula** cada RDT a las líneas del plan vigente por la clave de reporte `paquete × partida`. **Lo que no cambia:** el `metrado_ejecutado`, los metrados derivados, las horas, el estado de validación, los archivos y el historial de ejecución (el reposicionamiento solo **agrega** su fila), y **las cifras del PR consolidado**. **Lo que sí cambia es la asociación de paquete** del RDT (`rdt_actividades.paquete_trabajo_id` y `rdt_actividad_partidas.paquete_trabajo_id`), que es justamente la clave de reporte: por eso un RDT ya registrado puede verse con otro paquete en su propio formulario y en la pantalla Status, no solo en el Plan Maestro (corrección del Auditor, 2026-10-04: la frase anterior —«no cambia los datos del RDT»— era más fuerte que lo que el código garantiza).


### Qué deroga

| ID | Deroga |
|---|---|
| **E1-D1** | La observación **O3** del Lote 3, en su parte de «editar actividades individuales del cronograma con Plan Maestro aprobado» |
| **E1-D2** | Las **reglas confirmadas 1, 2 y 3** de este plan (editar con PM aprobado · solo Admin y JP · aviso de impacto previo) |
| **E1-D3** | **G-R1** y **V-R1** (conteo de partes por el endpoint de impacto): el endpoint desaparece con la función |
| **E1-D4** | La fila de la matriz del **flujo 14** + su nota 11 + el permiso `puedeEditarActividadCronograma` |

### Trabajo pendiente (R1–R5), mismo carril `local-worker-4`

| ID | Qué | Archivos (verificados en el carril) |
|---|---|---|
| **R1** | **Quitar** la edición de actividades del cronograma con PM aprobado | borrar `src/app/api/cronograma/actividades/[id]/route.ts` y `.../impacto/route.ts`, `src/components/cronograma/EditarActividadCronograma.tsx`, `NotificacionImpacto.tsx`; quitar `puedeEditarActividadCronograma` de `src/lib/permisos/permisos.ts` y de sus tests; quitar el uso en `src/app/(workspace)/cronograma/page.tsx`, `FormularioCronograma.tsx` (columna «Editar», modal, `planMaestroAprobado`) y el campo en `src/app/api/cronograma/route.ts` |
| **R2** | **Congelar paquetes** con PM aprobado (DP y cronograma ya están congelados por los flujos 09 y 15) | `src/app/api/paquetes-trabajo/route.ts`, `.../vinculos/route.ts`, su test y la pantalla |
| **R3** | **RDT exige PM aprobado + servicio `EJECUCION`**, validado en servidor | `src/app/api/rdts/route.ts`, `src/app/api/rdts/partes/route.ts`, `src/components/ui/FormularioCrearRdt.tsx` |
| **R4** | **Reposicionar** los RDT (fechas + metrados) al aprobar un Plan Maestro nuevo, todos, incluidos los validados | `src/app/api/plan-maestro/route.ts` (acción de aprobación) y lógica nueva en `src/lib/rdts/` con su test |
| **R5** | **Flujos** | `06-rdt.md` (U1), `14-accesos-y-restricciones.md` (E1-D4), `15-cronograma.md` (U2/U3), `19-paquetes…md` (U3), `20-plan-maestro.md` (U3/U4/U5) + índice |
| **R6** | **Guardia de U1 en las otras dos vías de ejecución** (hueco detectado por el Worker de R2-R3): carga de RDT **por archivo** y acción **MOVER** | `src/app/api/rdts/route.ts` y la ruta/acción que implemente MOVER, con sus tests |

| Tanda posterior | Qué | Estado | Commit / evidencia |
|---|---|---|---|
| **R4c** | Determinismo del reposicionamiento, `sinLinea` en la respuesta, aviso de dependencia de la `093` | **Cerrada** | `ae476f1` · tsc 0 · **1115 tests** · [`resultados/R4c.md`](2026-10-02-observaciones-victor-lote-3-briefs/resultados/R4c.md) |
| **U6** | Aviso de impacto antes de aprobar | **Cerrada** | `f19c801` · tsc 0 · **1136 tests** · [`resultados/U6.md`](2026-10-02-observaciones-victor-lote-3-briefs/resultados/U6.md) |
| **DOCS-L3** | Olas 1, 2 y 4: los 7 puntos de «APLICAR AHORA», las tres decisiones y el libro de hallazgos (39 → **56 filas**) | **Cerrada** | [`resultados/DOCS-L3.md`](2026-10-02-observaciones-victor-lote-3-briefs/resultados/DOCS-L3.md) · verificador 0/0 exit 0 |

### Estado real de las tareas de la Enmienda E1 (2026-10-04)

| Tanda | Qué | Estado | Commit / evidencia |
|---|---|---|---|
| R1 | Quitar la edición de actividades del cronograma con PM aprobado | **Cerrada** | `ceb269e` (8 archivos, +4/−608) |
| R2 | Congelar paquetes con PM aprobado | **Cerrada** | `d916716` |
| R3 | RDT exige PM aprobado + servicio `EJECUCION` | **Cerrada** | `74734d7` |
| R4a | Código, módulo, pruebas y migración `093` del reposicionamiento | **Cerrada** | `11804b6`, `56c66e0`, `d7d96fd` · tsc 0 · **106 archivos / 1094 tests** |
| R4b | Aplicar la migración `093` con el protocolo | **Cerrada** | Aplicada 2026-10-04 08:41, vía directa; conteos idénticos en 8 tablas; CHECK con `REPOSICIONAMIENTO`; función `aprobar_plan_maestro_con_reposicionamiento` creada |
| R5 | Escribir U1–U8 en los flujos 06, 14, 15, 19, 20 y índice | **Cerrada** | `resultados/R5.md` |
| R5b | Precisiones de las tres respuestas de Victor (U4 aclarada, U10, U9, U8 transaccional) | **Cerrada** | U10 quedó escrita **solo en el flujo 19** (no en el 06 ni en el 20, como decía esta fila); el §6 del flujo 20 se completó después, en la Ola 1 del 2026-10-04. U4, U9 y U8 sí quedaron en los flujos 06, 19 y 20. Verificador 0/0 exit 0 |
| R6a | Guardia de U1 en la **carga de RDT por archivo** | **Cerrada** | `26288bf` · tsc 0 · 1082 tests |
| R6b | Congelar **MOVER** con PM aprobado (U10) | **Cerrada** | `9d033e3` · 2 archivos, +17/−12 |
| R4c | Reposicionamiento **determinista**: migración `094`, `sinLinea` que vuelve en la respuesta y aviso de dependencia de la `093` | **Cerrada en código** | `ae476f1` · tsc 0 · 107 archivos / 1115 tests · `resultados/R4c.md`. **La `094` no se aplicó**: la base sigue con la `093`, que es la versión no determinista |

**Sin verificar:** el reposicionamiento y el aviso U6 **no se han probado en vivo** (ningún servicio de prueba sirve para una aprobación real; antecedente OP9). Lo verificado es `tsc`, la suite completa y la aplicación verificada de la migración.


### Riesgos

| # | Riesgo | Mitigación |
|---|---|---|
| E1-R1 | **R4 toca RDT validados**, y de ellos sale el «Real» del Dashboard y de la Curva S | Registrar el reposicionamiento en el **historial del RDT** (append-only) para que sea auditable y reversible; el PR se recalcula después, en el mismo paso de aprobación |
| E1-R2 | Congelar paquetes puede romper un flujo de trabajo si algún rol los usaba después de aprobar | Se valida en **servidor** con mensaje claro, igual que el DP y el cronograma; verificar en vivo que el bloqueo es solo de escritura |
| E1-R3 | Quitar R1 deja código muerto o referencias colgantes en la pantalla del cronograma | `tsc` + suite completa en verde y `grep` de los símbolos eliminados antes de commitear |

### Preguntas del Gate 1 Complementario — **respondidas por Victor (2026-10-03)**

| # | Pregunta | Respuesta | Queda como |
|---|---|---|---|
| E1-Q1 | ¿Aviso de impacto antes de aprobar? | **Sí, mostrar el impacto** | U6 |
| E1-Q2 | ¿Rastro del reposicionamiento? | **Sí, con historial** | U7 |
| E1-Q3 | ¿Orden al aprobar? | **PM → RDT → PR, todo o nada** | U8 |

**Gate 1 Complementario aprobado por Victor (2026-10-03):** las reglas U1–U8 y el trabajo R1–R5 quedan autorizados para implementación, sin aprobaciones intermedias hasta el Gate 2.

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
| F6 | Integración y documentación | **Conforme** | `0aa8196` | Flujos 06, 09, 10, 14, 15, 19, 20 actualizados; db/README ya documentaba 090-092 |

**Nota (2026-10-02):** El subagente Worker 4 no pudo lanzarse (modelo `qwen3.8-plus` no disponible en opencode). F0, F1-A/B/C, F2-A/B/C, F3, F4 y F6 implementados directamente por el Orquestador (qwen3.7-plus).

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

## Continuation del plan (2026-10-02 — Orquestador nuevo)

**Deuda del orquestador anterior (registrada, no ocultada):** implementó F0–F4 y F6 él mismo (sin Workers ni tandas), sin informe de Auditor, sin progreso/evidencia homónimos, solo 1 brief suelto, sin fila en el índice, y dejó 10 commits de docs sin pushear y un cambio sucio en el repo raíz de código.

**Decisiones de Victor (2026-10-02, continuación):**
1. Completar todo el alcance pendiente con Workers antes del Gate 2 (no postergar F5/Lienzo).
2. Descartar el cambio sucio de `FormularioPlanMaestro.tsx` en el árbol de `main` (reintroducía `pr-[60px]` ya corregido en `bd75f48`) — **hecho**.
3. Las migraciones `091` y `092` las aplica **Victor** (SQL Editor de Supabase, orden 090→091→092).
4. Asignación por complejidad según `docs/00-estandar-agentes/09-orquestacion-y-modelos.md` (Flash para simples; no usar Plus en todo).
5. Push de docs: sin autorización expresa → se hace en el cierre, tras el Gate 2.

## Tandas pendientes (carril único `local-worker-4` de código, secuenciales; merge solo tras Gate 2)

| Tanda | Qué | Worker | Modelo | Esfuerzo | Depende de | Estado |
|---|---|---|---|---|---|---|
| G | Integrar modal `NotificacionImpacto` en la pantalla del Cronograma + verificar en vivo el botón "Recalcular PR" (commits previos `d985d33`, `7f755df`) | Worker 1 | `qwen3.8-flash` | Medio | — | **Cerrada (2026-10-02)** |
| V | Corregir los dos defectos de `scripts/verificar.ps1` que impiden el Gate 2: (a) la ruta del informe espera el nombre del plan **con** `-plan` y la convención lo usa **sin**; (b) el conteo de filas `Registrada` no reconoce los acentos graves con que las escribe el libro de hallazgos. Documentación, `main`, sin código de la app | Worker flash | `qwen3.8-flash` | Medio | — | **Cerrada (2026-10-03)** — commit `53dbee9` |
| M | Aplicar las migraciones `090` → `091` → `092` con el protocolo de migraciones (candado, transacción, conteos antes/después, verificación en `information_schema`); hasta esta corrección las aplicaba cada Worker en su propia tanda | Worker plus | `deepseek-v4-pro` (high) | Medio | Credenciales en `D:\1 Nueva carpeta\todo\DIARIO` (ruta movida el 2026-10-03) | **Cerrada (2026-10-03)** — 3/3 aplicadas y verificadas; `disciplinas` 5→8; 6/6 columnas; conteos 267/104 sin cambio |
| E | UI del Lienzo del Plan Maestro: celdas editables verdes para `esDeclaracionPaquete`, indicador rojo de fechas fuera del rango visible | Worker plus | `qwen3.7-plus` (el cambio de config aún no aplicaba) | Medio | Tanda M aplicó `091` | **Cerrada (2026-10-03)** — commit `39408cb`; tsc 0 · vitest 124 (9 nuevos) · **en vivo: GET Conforme** (200 JSON, los 4 campos nuevos presentes, una fila de paquete y otra no) · **PATCH sin verificar**: ningún servicio de prueba tiene Plan Maestro en BORRADOR |
| F | F5 restante: declaración por paquete en RDT (WBS `PQ-001`, partidas directas) + libertad de WBS para C/NC y equipos + plegable de 8 disciplinas + V-R1 (impacto solo validados) + ítem 5 | Worker plus | `qwen3.7-plus` | Medio | M aplicó `090`+`092`; E cerrada | **Cerrada (2026-10-03)** — commit `abe1ebd`; tsc 0 · vitest 166/166 · worktree limpio · **en vivo: parcial** (cookie de sesión) · **ítem 5 pendiente de diseño de Victor** |

Después: **Documentador** (progreso/evidencia homónimos, briefs, libro de hallazgos, índice) → **Auditor** (informe propio en `04-auditoria/`, clasifica hallazgos) → **Gate 2** de Victor (merge `local-worker-4` → `main`, push de ambos repos). Ningún uso de Max ni esfuerzo alto.

> **Corrección (2026-10-03, Orquestador):** esta línea decía «Auditor → Documentador», al revés de lo que manda el estándar (`02-roles-y-delegacion.md` § Documentador: el Documentador **termina antes de la auditoría**; `04-flujo-sdd-y-planes.md` paso 11). Orden correcto: Documentador → Auditor.

### Cierre de la Tanda G (Worker 1, flash) — 2026-10-02

- `871b238`: `NotificacionImpacto` integrado en la pantalla del Cronograma (columna «Editar» solo con `puedeEditarActividadCronograma` + PM aprobado; campo nuevo `planMaestroAprobado` en el GET; formulario nuevo `EditarActividadCronograma.tsx` → PATCH existente, re-validado en servidor).
- `b59a82b`: **fix obligatorio** — los endpoints F2-B/F2-C ya marcados «Conforme» por el orquestador anterior fallaban 100 % contra la base real (`GET impacto` consultaba una columna inexistente; `PATCH` escribía con cliente de usuario sobre tabla con RLS de solo lectura). Corregidos con el patrón admin+validación del repo. Evidencia: la F2-C real exigía esta corrección — «Conforme» sin llamada viva no era cierre (G-O1).
- Ítem 2 (Recalcular PR): wiring ya completo (`7f755df`) — verificado en vivo, sin cambios.
- Validación: `tsc` exit 0 · vitest 174/174 (12 archivos) · verificación en vivo 12/12 + cadena de impacto contada a mano en PS-0009. Detalle en [`briefs/resultados/G.md`](2026-10-02-observaciones-victor-lote-3-briefs/resultados/G.md).
- **Pendiente que pasa a la Tanda F:** el aviso anticipa el reposicionamiento automático de RDT (regla confirmada 4) y el PATCH hoy no lo implementa.

### Ajustes operativos de la continuación (registro de política/modelos)

- Victor: «continúa hasta cerrar» (2026-10-02) — autoriza seguir E, F, Auditor, Documentador y cierre sin aprobaciones intermedias, salvo Gate 2 (merge) y lo que bloquea la política (Max, esfuerzo alto, destructivos).
- **Modelos:** `qwen3.8-plus` **no existe en opencode** (solo `qwen3.7-plus`, `qwen3.8-flash`, `qwen3.8-max`; verificado al intentar lanzar el Worker G — error del harness, mismo que frenó al orquestador anterior). Los Workers de E y F correrán en **`qwen3.8-flash`** (default de Worker en la política). No se usa Max (requiere aprobación y Victor no la pidió). Si flash no basta en alguna tanda, el Orquestador suspende y escala.
- **Migraciones `090`/`091`/`092`:** las aplica un Worker con el protocolo de migraciones autorizado por Victor (2026-09-30), en una sola tanda previa (**M**, orden `090`→`091`→`092`) para que E y F no compitan por el candado ni arranquen sin su precondición. (Antes de este registro estaba previsto que las aplicara Victor; no las había aplicado al retomar.)
- Briefs actualizados: `briefs/E.md`, `briefs/F.md`.

## Libro de hallazgos
## Plan de las tandas que faltan (2026-10-04, escrito tras el informe del Auditor)

El Auditor recomendó **requiere corrección mayor**. Lo que sigue son seis olas, con el nivel de cada una. Ninguna cuesta un nivel alto salvo la Ola 3, y esa depends de una decisión tuya que ya está escrita en el plan (U6).

| Ola | Tarea | Nivel | Quién | Depende de |
|---|---|---|---|---|
| **0** | **Terminar R4c**: el Worker escribió la migración `094` y sus pruebas y se cortó sin commit, sin validación y sin resultado | **1** | Worker `n1` | — |
| **0b** | Aplicar la `094` con el protocolo de migraciones | — | Orquestador | Ola 0 |
| **1** | Los **7 puntos de «APLICAR AHORA»** del informe: todos de documentación, ninguno con decisión de negocio | **0** | `n0` | Ola 0b |
| **2** | Las **tres decisiones de negocio** (U6, U7, segunda mitad de U9), escritas en los flujos | **0** | `n0` | Ola 1 |
| **3** | **U6 en código**: el aviso de qué RDT van a cambiar, antes de aprobar | **3** | Worker `n3` | Ola 2 |
| **4** | **Libro de hallazgos**: pasar las 12 filas que faltaron y aplicar la clasificación del Auditor a las 39 — **hecha el 2026-10-04**: 16 filas nuevas (12 + las 4 de R4c) y clasificación de las 39 | **0** | `n0` | Ola 1 |
| **5** | **Verificación en vivo**: crear un servicio de prueba con Plan Maestro en BORRADOR (desbloquea OP9) y probar la aprobación de punta a punta | **1** + Orquestador | `n1` | Ola 3 |
| **6** | **Gate 2 y cierre**: las 4 reglas de R4a, OP1, OP3, OP4, el artefacto «Matriz de permisos», merge, push y mensaje de cierre | — | Victor + Orquestador | Olas 1 a 5 |

**Estado de las olas (2026-10-04):** la **0** está **cerrada** (`ae476f1`, resultado en [`resultados/R4c.md`](2026-10-02-observaciones-victor-lote-3-briefs/resultados/R4c.md)); la **0b** sigue **pendiente** (la `094` no se aplicó). Las olas **1**, **2** y **4** —las tres de documentación— están **cerradas** ([`resultados/DOCS-L3.md`](2026-10-02-observaciones-victor-lote-3-briefs/resultados/DOCS-L3.md)). La **3** corre en paralelo. Las **5** y **6** quedan para después.

### Ola 0 — Cerrar R4c (lo que quedó a medias) — **cerrada el 2026-10-04**

El Worker de R4c **escribió** `db/094_aprobar_plan_maestro_reposicion_determinista.sql`, `src/lib/rdts/reposicionamiento-sql-094.test.ts` y modificó `reposicionamiento.ts`, `reposicionamiento-servidor.ts`, `api/plan-maestro/route.ts`, `plan-maestro-api.test.ts` y `db/README.md`. Se cortó antes de validar y de commitear. Lo que faltaba, en orden:

1. `n1` revisa el diff de los seis archivos, corrige lo que esté mal, corre `npx tsc --noEmit` y `npx vitest run`, y commitea con mensaje `R4c:`. Escribe `resultados/R4c.md`. → **Hecho**: `ae476f1`, `tsc` 0, 107 archivos y 1115 tests en verde.
2. El Orquestador aplica la `094` con el protocolo (candado, una transacción, conteos antes/después, verificación en `information_schema`) y borra script y candado. → **Pendiente (Ola 0b)**: el archivo de credenciales quedó inalcanzable durante la tanda y no se buscó otra vía. **La base tiene la `093`, que es la versión no determinista.**
3. Se comprueba en la base que la función viva es la `094` y que `db/README.md` tiene su fila. → **Pendiente**, depende del punto 2.

### Ola 1 — Los 7 puntos de «APLICAR AHORA» (nivel 0)

| # | Qué |
|---|---|
| 1 | Corregir el lenguaje de U4 en el flujo 20, el flujo 06 y el progreso: lo que **no** cambia es el metrado ejecutado, los derivados, las horas y el estado de validación; lo que **sí** cambia es la **asociación de paquete** del RDT, que se ve en su propio formulario y en Status |
| 2 | Eliminar la fila duplicada malformada que rompó la tabla del libro de hallazgos |
| 3 | Corregir la fila de R5b: U10 quedó en el flujo 19, no en 06, 19 y 20 |
| 4 | Añadir el congelamiento de `MOVER` al §6 del flujo 20 |
| 5 | Añadir la advertencia de dependencia de la `093` en `db/README.md` y en la cabecera de `db/093`: **la acción de aprobación falla por completo si la `093` no está aplicada** en ese entorno |
| 6 | Registrar el riesgo de la actualización no determinista de `rdt_actividades` en el libro **y en el código**, como comentario junto a la sentencia |
| 7 | **`sinLinea`**: se calculaba y se descartaba en silencio. **Resuelto en R4c** (`ae476f1`): la función SQL lo devuelve en su `jsonb` y la ruta lo expone en la respuesta de la aprobación, así que se muestra **como aviso al aprobar**. Lo que **no** se hizo (de las tres salidas que daba el Auditor) es registrarlo en el historial del RDT: esos vínculos no se reasocian ni se tocan |

> **Olas 1, 2 y 4 ejecutadas el 2026-10-04** (las tres son solo documentación; ninguna toca el repositorio de código). Lo que dice cada una está en `briefs/resultados/DOCS-L3.md`, con los archivos tocados y la salida del verificador. La Ola 3 (U6 en código) corre en paralelo.

### Ola 2 — Las tres decisiones de negocio, por escrito (nivel 0)

| Regla | Se asume | Alternatives que dejó abiertas |
|---|---|---|
| **U6** (aviso de impacto antes de aprobar) | **Se implementa** (Ola 3), porque está aprobada y escrita como vigente | Si no la quieres: se borra el texto del flujo 20 y la regla queda como trabajo futuro |
| **U7** (historial con fecha y metrado) | **Se corrige el flujo 06** para que prometa solo lo que el historial guarda: plan, versión, diff de claves y quién aprobó | La otra vía es ampliar el `snapshot` con fecha y metrado nuevo de cada línea |
| **U9**, segunda mitad | **Se deja como está**: la segunda condición (servicio en Ejecución) aplica a la **creación** del RDT; registrar, reasignar, validar y rechazar siguen exigiendo solo Plan Maestro aprobado | Añadir la segunda condición en `rdts/partes/[id]` sería una tanda nueva |

### Ola 3 — U6 en código (nivel 3, la única que sube de nivel)

Endpoint de consulta del impacto **antes** de confirmar la aprobación (cuántos RDT, con qué fechas y metrados), el modal que lo muestra en la pantalla del Plan Maestro, y el aviso de los que quedan `sinLinea`. Valida: `tsc` 0, suite en verde, y una llamada en vivo que cuente los RDT afectados de un servicio de prueba.

### Ola 5 — Verificación en vivo (desbloquea OP9)

Hoy no hay ningún servicio de prueba con Plan Maestro en BORRADOR, y por eso el reposicionamiento está verificado por pruebas y por la migración, **nunca en la app**. La tanda crea ese servicio de prueba (con su `.env.local` si hace falta, según `03-entorno-git-y-worktrees.md`) y aprueba un plan de verdad, comprobando tres cosas: que **las cifras del PR no cambian**, que el historial tiene la fila, y que un RDT con varios vínculos en paquetes distintos **no** queda descolocado.

### Ola 6 — Gate 2

Cierra con: las cuatro reglas de R4a (un RDT sin línea, partida en dos líneas, filas derivadas, porcentaje viejo), OP1 y OP3/OP4 (estándar), el artefacto «Matriz de permisos» (que solo editas tú), el merge de `local-worker-4` a `main`, el push de los dos repositorios y el mensaje de cierre que sustituye al borrador anticipado.

**Costo esperado:** las olas 0, 1, 2, 4 y 5 en nivel 0 o 1 (centavos de dólar). Solo la Ola 3 es nivel 3.

## Niveles de modelos y benchmark (2026-10-04)

Aplica `docs/00-estandar-agentes/10-niveles-de-modelos.md` (política aprobada por Victor el 2026-10-04). Las tareas de hoy se asignaron por **nivel de consumo medido**, no por nombre de modelo.

### Benchmark de R4 (tarea con resultado conocido: diseño del reposicionamiento)

| Nivel | Modelo | USD de la corrida | Tokens | Min | Resultado |
|---|---|---|---|---|---|
| **1** | `deepseek-v4.1-flash` | **0,0369** | 1 467 458 | 2,8 | 8/8 — el más completo: detectó el CHECK del historial, el snapshot en `jsonb`, el riesgo de `metrado_ejecutado` |
| **2** | `deepseek-v4-pro` (variante `high`) | 0,0858 | 809 909 | 2,2 | 7/8 — correcto; dice que el metrado ejecutado no se toca |
| **3** | `qwen3.7-plus` | 0,0477 | 325 972 | 2,3 | 7/8 — correcto; añade la regla de resolución de mapeo |

Los tres diseños coincidieron en lo importante: hoy la aprobación son llamadas HTTP sueltas a Supabase y **no es una transacción**; por eso hace falta la función SQL. **El nivel 1 salió bien y más barato: 2,3 veces más barato que el nivel 3 y 4,4 veces que el nivel 2.** Es la regla de seguridad de la política en práctica: el precio por token no predice el costo por tarea.

### Asignación por nivel de las tareas de hoy

| Tanda | Tipo de tarea | Nivel | Quién la ejecutó | Modelo |
|---|---|---|---|---|
| R5 (flujos) | Documentación acotada | 1 | Worker | `deepseek-v4.1-flash` |
| R6a (carga por archivo) | Código con brief cerrado: un archivo + test | 1 | Worker | `deepseek-v4.1-flash` |
| R6b (congelar MOVER) | Código con brief cerrado: un archivo + test | 1 | Worker | `deepseek-v4.1-flash` |
| R4a (reposicionamiento) | Tanda con análisis y varios archivos | 1, justificado por el benchmark | Worker | `deepseek-v4.1-flash` |
| R4b (migración `093`) | Migración con candado sobre datos reales | — | **Orquestador** | — |
| R5b (precisiones) | Cuatro frases en tres flujos | 1 | **Orquestador** (el Worker se cayó por un comando suyo) | — |

**Cómo se lanzó:** `opencode run --agent build --model opencode-go/deepseek-v4.1-flash --dir <worktree>`, sin tocar ningún archivo de configuración (hecho 4 de la política). El Worker 4 del Lote 3 quedó bloqueado antes por el motivo opuesto, y la Tanda R4 original se detuvo en el mismo permiso cuando intentó leer las credenciales.


Formato de fila: `| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |`. Estados: `Registrada` → `Trasladada` (con enlace y commit) · `Descartada` (con motivo) · `Pendiente de decisión` (con quién decide). Los Workers de código no editan este archivo: dejan sus hallazgos en su resumen de cierre y el Orquestador los pasa aquí, fila por fila.

> **Clasificación aplicada el 2026-10-04 (Ola 4):** el estado de las 39 filas que ya existían es el del [informe del Auditor](../04-auditoria/2026-10-02-observaciones-victor-lote-3.md) § «Clasificación de hallazgos», resumido fila por fila. Además entraron las **12 filas** que nunca se habían pasado (R1-M1, R1-M2, R2-R3-M1, R4a-M4, R5-M1, R4a-O1, R4a-O2, R5-R2, R5-R3, R5-O1, R5-O2, R6a-R1) y las **4 de R4c**. El libro queda con **24 mejoras, 13 reglas y 19 observaciones** (56 filas): las 39 del Auditor más 17 nuevas.

### Mejoras (de trabajo)

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| G-M1 | 2026-10-02 | Worker 1 (G) | Fijar en el brief la ruta de la memoria de cuentas y el puerto del carril para no re-buscarlos al usar evidencia sin navegador | `03-aprendizaje-continuo/` | Registrada | — |
| G-M2 | 2026-10-02 | Worker 1 (G) | Antes de integrar endpoints ajenos ya commiteados, una llamada viva mínima (GET/PATCH neutro) — tsc/vitest con mock de Supabase no ven errores de esquema | `03-aprendizaje-continuo/` | Registrada | — |
| V-M1 | 2026-10-03 | Orquestador (Fase 0) | Con `PLAN_ACTIVO`, `scripts/verificar.ps1` decide el cierre con dos defectos que lo dejaban pasar siempre: nombre del informe de Auditoría con sufijo `-plan` (la convención no lo lleva) y regex de `Registrada` que no reconoce los acentos graves con que las escribe el libro de hallazgos. Un control que no vigila es peor que no tenerlo | `03-aprendizaje-continuo/` | Registrada | — |
| V-M2 | 2026-10-03 | Orquestador (Fase 0) | Benchmark de modelos con tarea de resultado conocido (10 modelos, 11 corridas): los 10 acertaron las 4 preguntas, así que la calidad no discriminó; decidirse por costo y latencia. La latencia tiene varianza alta (18,3 s y 61,8 s para el mismo modelo en dos corridas) → con n=1 no se puede ordenar por latencia. Instrumento reutilizable | `03-aprendizaje-continuo/` | **Trasladada** | [2026-10-04-opencode-run-modelo-por-invocacion-y-niveles.md](../../03-aprendizaje-continuo/2026-10-04-opencode-run-modelo-por-invocacion-y-niveles.md) §5, con la conclusión de que con n=1 no se ordena por latencia |
| V-M3 | 2026-10-03 | Worker flash (V) | Para probar el verificador con fixtures, la carpeta de prueba debe replicar la **derivación exacta** de rutas del script (dos `Split-Path -Parent` desde el archivo de plan), no la ruta visible del repo | `03-aprendizaje-continuo/` | Registrada | — |
| V-M4 | 2026-10-03 | Worker flash (V) | En PowerShell 5.1 el acento grave es carácter de escape: para escribir `` `Registrada` `` en un fixture hay que usar cadena de comilla simple | `03-aprendizaje-continuo/` (se une a `2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md` § 3) | Registrada | — |
| V-M5 | 2026-10-03 | Orquestador | El almacén de sesiones de opencode (`%USERPROFILE%\.local\share\opencode\opencode.db`, tabla `session`) trae costo y tokens por sesión, incluidos los subagentes: es la fuente real para medir, y funciona donde `scripts/medir.py` no ve (opencode no escribe en `~/.claude/projects`) | `scripts/medir.py` (extender) o nuevo script | **Trasladada** | [niveles-modelos.py](../../../scripts/niveles-modelos.py) y [10-niveles-de-modelos.md](../../00-estandar-agentes/10-niveles-de-modelos.md). Falta en el destino la ruta y el nombre de la tabla, que solo están en la evidencia |
| M-M1 | 2026-10-03 | Worker (M) | El nombre real de la tabla es `disciplinas` (creada en la migración `085`), no `catalogo_disciplinas`: un brief que la llame así hace dudar al Worker. Los briefs deben copiar el nombre real de la tabla, no el del README | `03-aprendizaje-continuo/` | Registrada | — |
| E-M1 | 2026-10-03 | Worker (E) | El login sin navegador funciona si el propio `@supabase/ssr` construye la cookie (`createServerClient` + `cookieStore` tipo `Map` con `getAll`/`setAll`, `signInWithPassword`) y se reutilizan las cookies que devuelve: serializa la **sesión completa** en base64url con prefijo `base64-` y trocea a 3180. Construirla a mano con solo `{access_token, refresh_token}` hace que el middleware devuelva HTML | `03-aprendizaje-continuo/2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md` § 2 (ampliar) | Registrada | — |
| E-M2 | 2026-10-03 | Worker (E) | En un worktree el dev server solo levanta con `npm run dev -- --webpack -p <puerto>`; y hay que arrancar **el propio**, no reutilizar el de otra sesión de opencode, que puede estar sirviendo otro código | `03-aprendizaje-continuo/` | Registrada | — |
| E-M3 | 2026-10-03 | Worker (E) | Una llamada que devuelve HTML en vez de JSON es **fallo de sesión**, no del endpoint: contarla como resultado del endpoint produce un falso negativo | `03-aprendizaje-continuo/` | **Trasladada** | [2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md](../../03-aprendizaje-continuo/2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md) §2, párrafo «Trampa». El Auditor anota que el texto es anterior a este hallazgo: la fila se cerró por duplicado, no por aporte nuevo |
| F-M1 | 2026-10-03 | Worker (F) | El patrón de login sin navegador no estaba documentado en aprendizaje continuo, así que cada Worker lo redescubre: el hallazgo E-M1 debe promoverse **antes** de la siguiente tanda que necesite verificación en vivo | `03-aprendizaje-continuo/` | Registrada | — |
| R4a-M1 | 2026-10-04 | Worker (R4a) | El reposicionamiento re-vincula por **clave de reporte** `paquete × partida` porque no existe FK entre RDT y línea del plan; quien lo lea esperará una tabla de unión y no la hay | `03-aprendizaje-continuo/` | **Trasladada** | No llegó al destino propuesto, pero el contenido está donde un lector lo encuentra: cabecera de `db/093` (código), `reposicionamiento.ts` y los flujos [06](../../04-flujos-de-negocio/06-rdt.md) y [20](../../04-flujos-de-negocio/20-plan-maestro.md) |
| R4a-M2 | 2026-10-04 | Worker (R4a) | El cálculo del diff está en TS y la aplicación en SQL: la regla vive en dos sitios, con el payload jsonb de unión | `03-aprendizaje-continuo/` | **Trasladada** | Cabecera de `db/093` y `reposicionamiento-servidor.ts` (código). Mismo matiz: no llegó a `03-aprendizaje-continuo/` |
| R4a-M3 | 2026-10-04 | Worker (R4a) | `FilaHistorialRdt.accion` en TS no incluye `BORRADO`, que sí existe en el CHECK de la base: unión desalineada | Deuda técnica (tipos) | Registrada | El Auditor lo verificó y lo clasificó **NO PROMOVER**: deuda técnica de tipos, va al backlog del código, no a la política |
| R6a-M1 | 2026-10-04 | Worker (R6a) | El brief citaba `src/app/api/rdts/partes/partes-paquetes.test.ts`, que no existe; la suite real está en `src/lib/rdts/partes-paquetes.test.ts` | Corregir el brief (Documentador) | Registrada | El Auditor verificó que `briefs/R6a.md` **sigue citando** la ruta que no existe: corrección de una línea, pendiente |
| R6a-M2 | 2026-10-04 | Worker (R6a) | Dos helpers comprueban lo mismo con distinta forma: `planMaestroAprobado` (booleano) y `cargarPlanAprobado` (aprobado + líneas) | Backlog de refactor menor | Registrada | Los dos siguen existiendo y duplicando el criterio; no hay nota que diga cuál usar |
| R1-M1 | 2026-10-04 | Worker (R1) | Para confirmar que una columna o un botón **desapareció** de una tabla que se arma en el cliente, el SSR no basta: la tabla se construye tras el `fetch` en `useEffect`. Hace falta API + SSR + **Playwright** con la sesión ya iniciada | `03-aprendizaje-continuo/` | Registrada | — |
| R1-M2 | 2026-10-04 | Worker (R1) | `planMaestroAprobado` es **subcadena** de `hayPlanMaestroAprobado`: un grep por el primero da falsos positivos sobre un símbolo ajeno a la tarea. Buscar por símbolo exacto o delimitar | `03-aprendizaje-continuo/` | Registrada | — |
| R2-R3-M1 | 2026-10-04 | Worker (R2-R3) | El criterio «Plan Maestro aprobado» ya vivía en **tres** módulos distintos; conviene un único helper compartido para que el criterio no se abra en un cuarto | `03-aprendizaje-continuo/` | Registrada | — |
| R4a-M4 | 2026-10-04 | Worker (R4a) | En cada aprobación el servidor **relee todos los RDT del servicio** (lotes de 200) solo para calcular el diff: el costo crece con el historial del servicio. Conviene mover el cálculo a la función SQL o filtrar por vínculos. **El Auditor lo llamó «R4a-M1 (rendimiento)», pero ese ID ya lo tenía el hallazgo de la clave de reporte**; se numera M4 para no pisarlo | Plan de mejoras / rendimiento del código | Registrada | — |
| R5-M1 | 2026-10-04 | Worker (R5) | Buscar una regla derogada por **palabra suelta** (`impacto`) produce falsos positivos en cuanto la regla sucesora reutiliza el término —U6 se llama «aviso de impacto»—. El patrón de búsqueda debe ser por **símbolo o ruta** (endpoint, componente, permiso) | `03-aprendizaje-continuo/` | Registrada | — |
| R4c-M1 | 2026-10-04 | Worker (R4c) | Una tanda que **aplica una migración** no puede ejecutarse en un Worker lanzado con `opencode run` (permiso de directorio externo), y además depende de un archivo de credenciales que puede quedar inalcanzable sin aviso. El brief debería abrir con «verifica que la credencial se lee, antes de escribir una línea de código» | `03-aprendizaje-continuo/` | Registrada | — |
| R4c-M2 | 2026-10-04 | Worker (R4c) | Un corte del Worker a mitad de tanda no deja ni commit ni archivo de resultado: el brief debería exigir el **commit y el resultado antes** que cualquier refinamiento opcional | `03-aprendizaje-continuo/` | Registrada | — |

### Reglas de negocio acordadas en esta tarea

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| G-R1 | 2026-10-02 | Worker 1 (G) | Impacto de editar actividad = nº de partes RDT distintos vía `cronograma_actividad_partidas`/`dp_partida_id` → `rdt_actividad_partidas` → `parte_id` | `04-flujos-de-negocio/15-cronograma.md` | **Descartada** | E1-D3: el conteo desaparece con la función; el endpoint está borrado del código (verificado por el Auditor) |
| R4a-R1 | 2026-10-04 | Worker (R4a) | Un RDT que apunta a una `dp_partida` que ya no está en el plan queda **sin línea** y no se reasocia por WBS | `06-rdt.md` / `20-plan-maestro.md` | **Pendiente de decisión (Victor)** | Verificado en código, sin regla escrita. Desde R4c el caso vuelve en la respuesta de la aprobación como aviso |
| R4a-R2 | 2026-10-04 | Worker (R4a) | Una partida presente en dos líneas del plan con paquetes distintos es **ambigua**: no se reposiciona y falta el desempate | `20-plan-maestro.md` | **Pendiente de decisión (Victor)** | Verificado; falta el desempate |
| R4a-R3 | 2026-10-04 | Worker (R4a) | Las filas derivadas cambian de paquete pero no recalculan su metrado (recalcularlo cambiaría el PR): si el plan reagrupa partidas, el conjunto derivado puede quedar inconsistente | `19-paquetes-de-trabajo-y-jerarquia-de-control.md` | **Pendiente de decisión (Victor)** | Verificado: no hay código que recalcule el metrado derivado |
| R4a-R4 | 2026-10-04 | Worker (R4a) | El porcentaje de avance de una partida pudo quedar calculado sobre el plan viejo | `20-plan-maestro.md` | **Pendiente de decisión (Victor)** | Verificado: ningún punto del código lo recalcula tras reposicionar |
| G-R2 | 2026-10-02 | Worker 1 (G) | Edición individual: UI solo con permiso + PM APROBADO; servidor re-valida (403/409/404); aviso de impacto antes de editar; anotar en flujo 15 el campo `planMaestroAprobado` | `04-flujos-de-negocio/15-cronograma.md` | **Descartada** | Superada por U2/U3: la acción ya no existe en el código (verificado) |
| V-R1 | 2026-10-03 | **Victor** (decisión del Orquestador) | El aviso de impacto de editar una actividad del cronograma cuenta **solo partes de RDT validados**; los borradores no se cuentan. Antes (G-R1) contaba ambos | `04-flujos-de-negocio/15-cronograma.md` | **Descartada** | Mismo motivo que G-R1 (E1-D3): el aviso que contar solo los validados ya no existe |
| F-R1 | 2026-10-03 | Victor (reglas confirmadas 6 y 13 del plan, 2026-10-02) | Al declarar en el RDT, el **paquete completo** figura como `WBS="PQ-001"` y las partidas directas sueltas; las actividades **C y NC, los equipos y los materiales** tienen **libertad de WBS** (pueden elegir cualquier partida del Plan Maestro sin depender de una actividad D previa del mismo día) | `04-flujos-de-negocio/06-rdt.md` | **Trasladada** | [06-rdt.md](../../04-flujos-de-negocio/06-rdt.md) § «Crear RDT con el Plan Maestro», párrafo «Qué elige el supervisor». La fila nunca se cerró |
| F-R2 | 2026-10-03 | Worker (F) | El catálogo de disciplinas queda en **8**: Civil, Mecánica, Eléctrica, Instrumentación, Tuberías, Preliminares, Cierre y Subcontratos | `04-flujos-de-negocio/06-rdt.md` | **Trasladada** | [06-rdt.md](../../04-flujos-de-negocio/06-rdt.md) § «Disciplinas», con la referencia a la migración `090`. Fila nunca cerrada |
| R5-R2 | 2026-10-04 | Worker (R5) | **G-R2 y V-R1 quedan superadas por U2/U3 y deben pasar a «Descartada»**: con Plan Maestro aprobado el cronograma no se edita, así que no corresponde trasladarlas al flujo 15 | Libro de hallazgos de este plan | **Trasladada** | Aplicada el 2026-10-04: G-R2 y V-R1 de esta tabla quedaron en **Descartada**, con su motivo |
| R5-R3 | 2026-10-04 | Worker (R5) | **U9 no estaba en el mapeo de R5**: la carga de RDT por archivo —vía de creación que el flujo 06 no mencionaba— y la acción `MOVER` | `04-flujos-de-negocio/06-rdt.md` | **Trasladada** | [06-rdt.md](../../04-flujos-de-negocio/06-rdt.md) nombra las vías de creación (el RDT estructurado, la carga por archivo y las que se creen después) y precisa que las dos condiciones son de **creación**. `MOVER` quedó en el flujo 19 (U10) y en el §6 del flujo 20 |
| R6a-R1 | 2026-10-04 | Worker (R6a) | Los **RDT ya existentes por archivo** en servicios que están fuera de `EJECUCION` no se migran ni se ocultan: la guarda de U1 es de creación y no borra ni esconde nada de lo anterior | `04-flujos-de-negocio/06-rdt.md` (nota de datos) | Registrada | Destino sin escribir: es regla de negocio y el flujo 06 todavía no la dice |
| R4c-R1 | 2026-10-04 | Worker (R4c) | Una actividad con **varios vínculos** que el plan nuevo reparte en paquetes distintos **no se reposiciona**, y se reporta en `actividadesAmbiguas` con los paquetes en conflicto. El código ya lo aplica (migración `094`) y no está escrito en ningún flujo | `06-rdt.md` / `20-plan-maestro.md` | **Pendiente de decisión (Victor)** | Decidir si se documenta como regla o si se cambia el comportamiento. No se escribe en los flujos mientras Victor no decida |

### Observaciones sobre la política

| ID | Fecha | Quién (rol, tanda) | Qué | Destino propuesto | Estado | Enlace al destino |
|---|---|---|---|---|---|---|
| G-O1 | 2026-10-02 | Worker 1 (G) | «Conforme» declarado sin ninguna llamada real a endpoints (fallaban 100 %); el criterio de cierre de un endpoint debería exigir al menos una llamada viva | Clasificación del Auditor; Victor decide en el Gate 2 | **Pendiente de decisión (Victor, Gate 2)** | El Auditor: se repetiría —R4a, R6a y R6b se cerraron sin verificación en vivo; la regla solo se aplicó a R1 y R3. Recomienda que el criterio sea explícito en el estándar |
| R4b-O1 | 2026-10-04 | Orquestador | Una Tanda que solo escribe en un worktree puede ir por `opencode run`; una que necesita credenciales, no: el permiso se rechaza sin humano. El brief de R4 debió prever el corte desde el inicio | `10-niveles-de-modelos.md` § Política 3 | **Trasladada** | [2026-10-04-opencode-run-modelo-por-invocacion-y-niveles.md](../../03-aprendizaje-continuo/2026-10-04-opencode-run-modelo-por-invocacion-y-niveles.md) §4, con el workaround del brief y la regla de que las credenciales las aplica el Orquestador. Falta recogerlo en `10-niveles-de-modelos.md` § Política 3 (destino propuesto) |
| R5b-O1 | 2026-10-04 | Worker (R5b) | El Worker de R5b se cayó por un comando propio (`rg`, que no existe en esta máquina) y no dejó nada: la tarea la hizo el Orquestador. Un Worker que falla en el primer comando debe reportar, no desaparecer | Clasificación del Auditor | Registrada | No hay ninguna regla escrita sobre qué hacer cuando un Worker falla en su primer comando |
| G-O2 | 2026-10-02 | Worker 1 (G) | `crearClienteServidor` escribe sobre tablas con RLS de solo lectura y PostgREST devuelve `message` vacío (difícil de diagnosticar) | Clasificación del Auditor; Victor decide en el Gate 2 | Registrada | El Auditor lo clasifica **NO PROMOVER**: es útil pero no es una regla de política; basta una línea en el checklist de endpoints de escritura |
| OP1 | 2026-10-03 | Orquestador (Fase 0) | `.opencode/config.json` commiteado apunta **6 roles** a `opencode-go/qwen3.8-plus`, que **no existe** en el proveedor (verificado con `opencode models`: 28 modelos). Eso impidió lanzar al Worker 4 del Lote 3. El estándar `09-orquestacion-y-modelos.md` publica esa misma tabla de modelos, así que el error está en dos sitios | `docs/00-estandar-agentes/09-orquestacion-y-modelos.md` + `.opencode/config.json` | **Pendiente de decisión (Victor)** | El Auditor verificó que `qwen3.8-plus` **sigue** en `09-orquestacion-y-modelos.md`, `10-niveles-de-modelos.md` y `01-contexto-repositorio/09-medicion-y-modelos.md`: son tres sitios y el propio plan dice que no los edita un agente |
| OP2 | 2026-10-03 | Orquestador (Fase 0) | El Lote 3 se implementó sin Spec/SDD ni Gate Spec (el flujo los exige en los pasos 3 y 4) y con un «Mensaje de cierre» escrito antes del Auditor y del Gate 2. El estándar no dice qué hacer con un plan ya aprobado sin Spec: no se inventó un Spec retroactivo | Clasificación del Auditor | **Pendiente de decisión (Victor, Gate 2)** | El plan ya marca el mensaje de cierre como borrador anticipado; el estándar sigue sin decir qué hacer con un plan aprobado sin Spec |
| OP3 | 2026-10-03 | Orquestador (Fase 0) | El merge a `main` del código (paso 16a) tiene dueño ambiguo en el estándar: `04-flujo-sdd-y-planes.md:76` lo asigna al Orquestador, `02-roles-y-delegacion.md:66` se lo prohíbe al Orquestador y `:172` se lo da al Worker git, y `09-orquestacion-y-modelos.md:187` lo declara sin aprobación de Victor | Clasificación del Auditor | **Pendiente de decisión (Victor, Gate 2)** | El Auditor verificó que el conflicto sigue: cuatro enunciados, tres dueños |
| OP4 | 2026-10-03 | Orquestador (Fase 0) | `09-orquestacion-y-modelos.md` trata al verificador como control obligatorio de acciones críticas, mientras `07-verificador-de-acciones.md` dice que sin el hook registrado la regla no es obligatoria | Clasificación del Auditor | Registrada | La contradicción sigue |
| OP5 | 2026-10-03 | Worker flash (V) | El estándar nombra el informe del Auditor «el mismo nombre base sin `-plan`» y el script nació contradiciéndolo: la política no exige probar con un fixture las rutinas que leen el árbol de `docs/` cuando se escribe un script nuevo de `scripts/` | Clasificación del Auditor | Registrada | Agrupar con V-M3 y resolver en el mismo Gate |
| OP6 | 2026-10-03 | Worker flash (V) | `verificar.ps1` deriva `04-auditoria/` con dos `Split-Path -Parent` sin validar que el plan viva bajo `01-planes/`: un plan fuera de esa estructura produce el fallback `no existe` en silencio | Clasificación del Auditor | Registrada | El Auditor verificó que no se corrigió en la Tanda V (que corrigió otros dos defectos) |
| OP7 | 2026-10-03 | Orquestador | Hay **tres** fuentes de verdad para el modelo de cada rol y no coinciden: el config global `~/.config/opencode/opencode.jsonc` (modificado el 2026-10-03 00:00, ya con `worker-flash` = `glm-5.3-flash` y su nota de benchmark), el `.opencode/config.json` del repo (6 roles apuntan a `qwen3.8-plus`, que no existe) y el harness que realmente lanza los subagentes (en la Tanda V ejecutó `qwen3.8-flash`). Con más de un proceso opencode vivo, un cambio de config puede no aplicarse a las sesiones ya abiertas | Clasificación del Auditor; Victor decide | Registrada (la fila decía «Resuelta» y no del todo) | El Auditor verificó que el config del repo ya no define modelos (esa mitad está resuelta), pero las tablas del estándar y el pendiente 5 del progreso lo siguen nombrando. **Corregido el estado de la fila** (2026-10-04): no es Resuelta |
| OP8 | 2026-10-03 | Worker (F) | El ítem «reposicionamiento automático de los RDT» aparece en **dos sitios con disparadores distintos**: la regla 4 del plan dice «al aprobar el nuevo Plan Maestro» y el brief de la tanda G lo puso «al confirmar la edición de una actividad». Sin mecanismo especificado no se implementa: el plan debe fixarlo antes | Clasificación del Auditor; **Victor decide el diseño** | **Descartada** | Resuelta por la Enmienda E1: el disparador único es la aprobación de un Plan Maestro nuevo (U4), escrito en el plan, en el flujo 06 y en el flujo 20 |
| OP9 | 2026-10-03 | Worker (E, F) | El brief exige «una llamada viva» pero el repositorio **no tiene un servicio de prueba con Plan Maestro en BORRADOR**, y el estado que exige el PATCH es justo ese: la verificación en vivo del guardado queda bloqueada por datos, no por código | Clasificación del Auditor; Victor decide | Registrada | Sigue vigente: es la razón de que el reposicionamiento no se haya probado en vivo. **No la resuelve este plan** (la resuelve la Ola 5) |
| R4a-O1 | 2026-10-04 | Worker (R4a) | El protocolo de migraciones dice que el Worker aplica las migraciones de su rango y el brief de R4a se lo prohíbe: **el protocolo y el brief se contradicen** | Protocolo de migraciones / checklist de revisión | Registrada | — |
| R4a-O2 | 2026-10-04 | Worker (R4a) | U8 exige «todo o nada» y la aprobación **no era** transaccional: conviene un ítem de revisión que prohíba llamadas sueltas en flujos de aprobación | Checklist de revisión (repositorio de código) | Registrada | — |
| R4a-O3 | 2026-10-04 | Orquestador (tras el Auditor) | Un `UPDATE` alimentado por un payload **una fila por vínculo** no es determinista cuando una actividad tiene varios vínculos y el plan nuevo los reparte en paquetes distintos: PostgreSQL elige una fila arbitrariamente y el RDT queda con un paquete arbitrario (la `093`, tal como se aplicó). Lo detectó la revisión, no el brief: **un brief que escribe SQL debe exigir comprobar el determinismo de todo `UPDATE` alimentado por un payload por fila**, y el checklist de revisión debe incluirlo. El código ya lo corrige con la `094` (`ae476f1`) | Checklist de revisión de endpoints y funciones SQL / `03-aprendizaje-continuo/` | Registrada | El Auditor lo señala como el riesgo más grave de su punto 1; el código ya está corregido (`094`), lo que queda es el aprendizaje de revisión |
| R5-O1 | 2026-10-04 | Worker (R5) | La política no dice si un registro histórico de cambio se conserva o se reescribe al derogarse una regla; R5 lo reescribió, por coherencia | Clasificación del Auditor | Registrada | — |
| R5-O2 | 2026-10-04 | Worker (R5) | El término `impacto` figura como **prohibido** en la verificación del brief y a la vez se conserva en U6 («aviso de impacto»): la política debería distinguir «símbolo derogado» de «concepto vigente con el mismo nombre» | Clasificación del Auditor | Registrada | — |
| R4c-O1 | 2026-10-04 | Worker (R4c) | Un archivo puede estar **listado** por el sistema de archivos y a la vez ser **inaccesible** a toda API. El protocolo de migraciones asume que la credencial está o no está; falta el caso intermedio | Protocolo de migraciones | Registrada | — |

### Carpetas/archivos huérfanos

Ninguno detectado en la revisión de inicio del 2026-10-03. Se reporta sin borrar nada.En la revisión de inicio del 2026-10-03: ninguno. En la del 2026-10-04 (tandas R1, R2-R3, R4a, R5, R6a, R6b): **ninguno**. Se reporta sin borrar nada.

Cuatro archivos temporales que el Orquestador movió a `resultados/` y borró del worktree: `R6a-resultado.md`, `R4a-resultado.md`, `R6b-resultado.md` y una copia de `_protocolo-migraciones.md` (para que el Worker no dependiera de un directorio externo). Ninguno quedó en el repositorio de código.

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-02 | Gate 1 aprobado: las 13 observaciones, las 10 reglas confirmadas, 4 carriles, 3 migraciones | Victor |
| 2026-10-02 | F0, F1, F2, F3, F4 y F6 implementados por el Orquestador anterior, sin Workers ni verificación viva — **deuda registrada** (OP2) | Orquestador (deuda) |
| 2026-10-02 | «Continúa hasta cerrar»: seguir E, F, Documentador, Auditor y cierre sin aprobaciones intermedias, salvo Gate 2 | Victor |
| 2026-10-02 | Push de docs solo en el cierre, tras el Gate 2 | Victor |
| 2026-10-03 | **Se continúa el Lote 3** (el Lote 2 está cerrado) y el trabajo a medias del worktree **lo termina y verifica un Worker**, no se descarta ni se rehace | Victor |
| 2026-10-03 | F0–F4 y F6 quedan como **deuda registrada**: el Auditor la clasifica, no se reimplementa | Victor |
| 2026-10-03 | **V-R1:** el aviso de impacto cuenta **solo partes de RDT validados** | Victor |
| 2026-10-03 | Se agrega la **Tanda V** (arreglar `scripts/verificar.ps1`) porque sus dos defectos bloquean el Gate 2, y la **Tanda M** (migraciones `090`→`091`→`092`) como precondición común de E y F | Orquestador |
| 2026-10-03 | Cambio de modelos **pendiente de evidencia**: el benchmark de 10 modelos no diferenció calidad; la Tanda V se usa como benchmark real (agéntico) antes de tocar `.opencode/config.json` | Orquestador |
| 2026-10-03 | **Enmienda E1 (reglas del umbral):** Victor fija que el Plan Maestro es el umbral del servicio (U1–U5) y **deroga** O3, las reglas confirmadas 1-3, G-R1/V-R1 y la fila de la matriz del flujo 14. Trabajo autorizado: **R1–R5** | Victor |
| 2026-10-03 | **Gate 1 Complementario aprobado:** aviso de impacto antes de aprobar (U6), reposicionamiento con historial (U7) y orden **PM → RDT → PR, todo o nada** (U8). Implementación autorizada sin aprobaciones intermedias hasta el Gate 2 | Victor |
| 2026-10-03 | **Tanda V cerrada** (arreglo del verificador, `53dbee9`) y **Tanda C cerrada** (config del repo alineada al global, `ba7e371`) | Orquestador (consolidación) |
| 2026-10-03 | **Tanda M cerrada:** migraciones `090`/`091`/`092` aplicadas y verificadas por un Worker con las credenciales de la **ruta nueva** (`D:\1 Nueva carpeta\todo\DIARIO`) | Orquestador (consolidación) |
| 2026-10-03 | **Tandas E y F cerradas** (`39408cb`, `abe1ebd`); el ítem 5 quedó detenido por OP8 y quedó resuelto por la Enmienda E1 (R4) | Orquestador (consolidación) |
| 2026-10-04 | **U4 aclarada:** el reposicionamiento re-vincula el RDT a las líneas del plan vigente; **no** toca `metrado_ejecutado` **ni las cifras del PR consolidado** | Victor |
| 2026-10-04 | **Atomicidad de U8:** función SQL nueva (migración `093`), aplicada por un Worker con el protocolo de migraciones | Victor |
| 2026-10-04 | **U10:** con Plan Maestro aprobado también se congela **MOVER** (reordenar paquetes); deroga la lectura R2-R3-R1 | Victor |
| 2026-10-04 | **R4 se parte en dos:** R4a (código y pruebas, sin base) la hace un Worker; R4b (aplicar la `093`) la hace el Orquestador, porque el Worker se detuvo en el permiso de credenciales | Orquestador |
| 2026-10-04 | **Niveles de modelos:** cinco niveles por consumo medido, benchmark antes de asignar y `opencode run --model` para no depender de la configuración. Política en `docs/00-estandar-agentes/10-niveles-de-modelos.md`; las tareas de hoy salen todas en **nivel 1** | Victor (política) / Orquestador (asignación) |
| 2026-10-03 | **Tanda N bloqueada:** no se pudo crear el servicio de prueba con Plan Maestro en BORRADOR por un bloqueo de sesión en la UI; el PATCH del Plan Maestro sigue sin verificar en vivo (OP9). El Worker dejó opciones por escrito | Orquestador |

## Enlaces a progreso y evidencia homónimos

- Progreso: `docs/02-trabajo-activo/02-progreso/2026-10-02-observaciones-victor-lote-3.md` (lo crea el Documentador)
- Evidencia: `docs/02-trabajo-activo/03-evidencia/2026-10-02-observaciones-victor-lote-3.md` (lo crea el Documentador)
- Auditoría: `docs/02-trabajo-activo/04-auditoria/2026-10-02-observaciones-victor-lote-3.md` (la emite el Auditor; **sin** sufijo `-plan`, que es la convención)

## Gate 2 — aprobado por Victor (2026-10-04)

**Estado: las tres olas del Auditor están cerradas.** C commits en `local-worker-4`, **sin mergear**: `ceb269e`, `d916716`, `74734d7`, `26288bf`, `9d033e3`, `11804b6`, `56c66e0`, `d7d96fd` (R4), `ae476f1` (R4c), `f19c801` (U6).

### Lo que se pide

1. **Aprobar el cierre** de las 13 observaciones del Lote 3 con la Enmienda E1 (U1 a U10) y las tres decisiones de hoy.
2. **Autorizar el merge** de `local-worker-4` → `main` en el repositorio de código y el **push de los dos repositorios**.

### Lo que queda dentro, con una salvedad

| # | Salvedad | Por qué |
|---|---|---|
| 1 | ~~La `094` sin aplicar~~ **CERRADA**: aplicada por el responsable humano el 2026-10-04 en los dos proyectos (control y control web) y verificada en la base (`es_la_094 = true`, que en el mismo cuerpo lleva el guard `having count(distinct`, o sea determinista) | El Orquestador no pudo aplicarla porque el archivo de credenciales quedó inalcanzable; la aplicó el responsable humano por el SQL Editor |
| 2 | **El reposicionamiento no se probó en vivo** | Ningún servicio de prueba tiene Plan Maestro en BORRADOR (OP9) |
| 3 | **U6 sin verificación en vivo** | El Worker se agotó antes; validado por `tsc` y por 1136 tests |

### Las cuatro reglas de R4a y las demás que no bloquean el cierre

`R4a-R1` (RDT cuya partida ya no está en el plan), `R4a-R2` (partida en dos líneas con paquetes distintos), `R4a-R3` (filas derivadas que cambian de paquete sin recalcular metrado), `R4a-R4` (porcentaje de avance sobre el plan viejo), `R4c-R1` (actividad con vínculos en paquetes distintos: no se reposiciona y se reporta), `U6-R1` (si el impacto no se puede calcular, se avisa y se deja aprobar), más OP1, OP3 y OP4. **Ninguna impide el cierre**: quedan written en el libro de hallazgos con su estado y se resuelven en un plan siguiente o en estándar. El artefacto «Matriz de permisos» lo editas tú.

### Lo que este plan deja escrito para el siguiente

La Enmienda E1, el orden de las olas, los niveles de modelo por tipo de tarea y el mecanismo de lanzar un Worker por invocación. El aprendizaje nuevo está en `docs/03-aprendizaje-continuo/2026-10-04-opencode-run-modelo-por-invocacion-y-niveles.md` y la política en `docs/00-estandar-agentes/10-niveles-de-modelos.md`.

## Mensaje de cierre

> **Este es el cierre real** (paso 17 del estándar), escrito después del informe del Auditor y del Gate 2 de Victor del 2026-10-04. Sustituye al borrador anticipado que estaba antes en este lugar, que se conservó solo por trazabilidad.

### Lo que se completó

Las **13 observaciones** del Lote 3, con la Enmienda E1 («el Plan Maestro es el umbral del servicio», reglas U1 a U10) y las tres decisiones que tomó el responsable humano el 2026-10-04.

- **El Plan Maestro es el umbral.** Aprobado, lo único editable es el Plan Maestro; DP, PR, cronogramas y paquetes quedan congelados, incluido **reordenar** paquetes (U10). El registro de ejecución sigue funcionando: el congelamiento es de la planeación.
- **Ninguna vía de creación de un RDT se salta las dos condiciones** (U1, U9): Plan Maestro aprobado **y** servicio en Ejecución, en las tres vías (RDT estructurado, carga por archivo y las posteriores), validadas en servidor.
- **El reposicionamiento de los RDT al aprobar un plan nuevo** (U4), con **rastro en el historial** (U7) y **todo o nada** (U8) en una sola transacción. No reescribe el metrado ejecutado, los derivados, las horas ni el estado de validación, y **las cifras del PR consolidado no cambian**: lo que cambia es la asociación de paquete del RDT, que es la clave de reporte.
- **El aviso de impacto antes de aprobar** (U6): cuántos RDT cambian, con qué fecha y qué metrado.
- **Correcciones de las 7 observaciones anteriores** (F1 a F4) y de la Tanda F: botones con barra de progreso, terminología, permisos por rol, mejora de Paquetes y del Plan Maestro, declaración por paquete en RDT y el plegable de 8 disciplinas.

### Evidencia

- **Código:** 10 commits de la Enmienda E1 en `main` (`ceb269e` a `f19c801`), **mergeado y pusheado**: `main` = `origin/main` = `f19c801`.
- **Validación final:** `npx tsc --noEmit` exit 0 y `npx vitest run` **109 archivos / 1136 tests en verde**.
- **Migraciones:** `093` aplicada y verificada (conteos idénticos en 8 tablas). `094` escrita y validada, **pendiente de aplicar**.
- **Documentación:** flujos 06, 09, 10, 14, 15, 19 y 20actualizados; verificador de referencias **0 huérfanos, 0 enlaces rotos, exit 0**.
- **Auditoría:** informe propio en `04-auditoria/2026-10-02-observaciones-victor-lote-3.md`, recomendación **requiere corrección mayor**; sus tres hallazgo se cerraron con las olas R4c, U6 y DOCS-L3.

### Lo que NO quedó hecho, y por qué

1. **La migración `094` quedó aplicada y verificada el 2026-10-04**, en los dos proyectos (control y control web). El Orquestador no pudo aplicarla porque el archivo de credenciales quedó inalcanzable; la aplicó el responsable humano por el SQL Editor, y la verificación en la base dio `es_la_094 = true`, que en el mismo cuerpo de la función lleva el guard `having count(distinct`: **el reposicionamiento es determinista**.
2. **El reposicionamiento y el aviso U6 no se probaron en vivo** (OP9): ningún servicio de prueba tiene Plan Maestro en BORRADOR. Es lo único que queda abierto de este plan, y no es un defecto: es una prueba que no se pudo hacer.
3. **F5 quedó parcial**: la libertad de WBS para actividades C y NC, equipos y materiales quedó fuera.

### Reglas que quedan pendientes de decisión

`R4a-R1` a `R4a-R4`, `R4c-R1`, `U6-R1`, más OP1, OP3 y OP4: están en el libro de hallazgos con su estado y van a un plan siguiente. El artefacto «Matriz de permisos» lo edita el responsable humano.

### Lo que este plan deja instalado para los siguientes

- **Política de niveles de modelo** (`docs/00-estandar-agentes/10-niveles-de-modelos.md`) con seis agentes (`n0` a `n5`) en el `opencode.json` de la raíz, que no pisan el config global, y el instrumento `scripts/niveles-modelos.py`.
- **Aprendizaje nuevo** en `docs/03-aprendizaje-continuo/2026-10-04-opencode-run-modelo-por-invocacion-y-niveles.md`: lanzar cualquier modelo por invocación, dónde sí manda un override, y el corte del permiso de directorio externo.
- **El orden de las olas** que funciona: dos carriles en paralelo (código y documentación, con archivos separados), brief copiado dentro del worktree, y **commit antes que refinamiento**.

### Git

- `py_control_proyectos_web`: merge `--ff-only` de `local-worker-4` a `main`, `cd10882..f19c801`, **pusheado**. `main` = `origin/main`, `0/0`.
- `pg_control_proyectos`: commit de cierre en `main` y push.
- Las dos Policies y el aprendizaje viven en este repositorio; el código, en el hermano.

## Elementos postergados propuestos para planes futuros

- Aplicar migración 091 en Supabase y completar la UI del Lienzo (celdas editables verdes + fechas rojas fuera de rango).
- Libertad de WBS para C/NC y equipos en RDT (F5).
- Integración del modal `NotificacionImpacto` en la pantalla del Cronograma.
- Integración del botón "Recalcular PR" en la pantalla del PR (ya creado, pendiente de verificar en vivo).
