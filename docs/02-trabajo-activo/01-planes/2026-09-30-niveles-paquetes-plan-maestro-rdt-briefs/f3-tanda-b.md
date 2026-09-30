# F3-B · Plan Maestro: datos y API (líneas, borrador, aprobar)

Lee primero `00-reglas-de-contexto.md`. Carril **2 · Plan Maestro** · rama `local-worker-2`, puerto 3112.
Fase F3 · **Depende de:** F3-A cerrada. No depende de la maqueta. Contratos que lees: `contrato-c3-plan-maestro.md` y `contrato-c4-real-por-clave.md`.
**Migraciones reservadas: `db/076`–`078`** (se escriben y **las aplicas tú**, según `00-protocolo-migraciones.md`; cuarto lugar en el orden).
**Punto de commit:** al cerrar la tanda, en `local-worker-2`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F3B-1 | Migraciones 076–078: relajar `unique (plan_maestro_id, wbs)`; agregar `metrado_linea`, `actividad_id`, `clave_reporte`, `paquete_trabajo_id`, `paquete_codigo`, `paquete_nombre`, `paquete_orden`, `hh_und_partida` a `plan_maestro_partidas`, y `motivo_version text` a `proyecto_plan_maestro`. **Cambio de restricción: el handoff lo marca «requiere autorización expresa de Victor»**; nada se borra | Archivos SQL + lectura crítica (sin aplicar) |
| F3B-2 | `POST /api/plan-maestro`: crea `BORRADOR` **sin exigir paquetes** ni leer `paquete_trabajo_programacion`; líneas desde vínculos (en paquete o directos) con metrado > 0; si hay versión aprobada, parte de sus asignaciones y **exige `motivo`** (se guarda en `motivo_version`); sin copia de programación | Prueba con datos simulados |
| F3B-3 | `GET /api/plan-maestro` → `{ plan, lineas, asignaciones, semanas, reales }` (C3); `reales` viene de un **adaptador** que lee `realPorClaveReporte` (C4, carril 4) y mientras no exista devuelve `[]` | Prueba |
| F3B-4 | `PATCH` guardar y aprobar: valida Σ días = `metradoLinea` por línea **y** Σ líneas = contractual por partida; reemplaza la versión aprobada anterior y llama `recalcular_pr_planificado` (RPC existente); mensajes que dicen qué líneas o partidas faltan | Prueba |
| F3B-5 | **Partida repetida sin romper nada**: prueba unitaria de que el PV, el planificado del PR y la Curva S **suman** las líneas repetidas de un mismo WBS (lectura de `pr/page.tsx`, `dashboard/page.tsx`, `api/curva-s/route.ts` y del SQL de `db/061` y `db/070`; si algo no suma, se reporta, no se edita) | Prueba + nota |
| F3B-6 | Guardias: ver = `puedeVerPlanMaestro` **y alcance por OT**; gestionar = `puedeGestionarPlanMaestro` (administrador, jefe de proyectos, planner); **crear una versión nueva cuando ya hay una aprobada = `puedeCrearVersionPlanMaestro` (administrador y jefe de proyectos; función nueva en `permisos.ts` con su prueba para los 13 roles; es una restricción más estricta que la de gestionar y se registra en el handoff para la tabla del flujo 14)**; 403 por rol, 400/404 por servicio; `npx tsc --noEmit`, suite y lint comparado con `main` | Salida de comandos |

## Contrato técnico verificado (2026-09-30, `45c9e0a`)

- `src/app/api/plan-maestro/route.ts`: `GET` (~29) devuelve `{ plan, partidas, asignaciones, semanas, reales }` y lee los RDT validados por `rdt_actividad_partidas` (con `hhReales` y `costoReal` en 0 como marcador); `POST` (~125) hoy exige paquetes y partidas completas en paquetes y **copia** desde `paquete_trabajo_programacion` a `plan_maestro_asignaciones`; `PATCH` (~295) valida Σ días = `metrado_contractual` de la línea y al aprobar reemplaza la versión anterior y llama `recalcular_pr_planificado`.
- Esquema (`db/037`): `proyecto_plan_maestro (estado BORRADOR|APROBADO|REEMPLAZADO, unique (proyecto_id, version))`, índice único de un solo aprobado por servicio; `plan_maestro_partidas`; `plan_maestro_asignaciones` `unique (plan_maestro_partida_id, fecha)`.
- Lectores de las tablas (todos agregan por **id de línea** y luego por WBS): `db/061` (`group by wbs`), `db/070`, `pr/page.tsx` (~204-208 mapea cada asignación a `{ wbs, fecha, metradoPlanificado, precioUnitario }`), `dashboard/page.tsx`, `api/curva-s/route.ts`. Esos archivos **no son tuyos**: solo los lees para la prueba F3B-5.
- Sin Plan Maestro aprobado no hay PV (los indicadores muestran «Pendiente»); transición `EN_PLANEACION → EJECUCION` exige uno aprobado (flujo 20, regla 8): **no cambia**.
- Permisos (flujo 14): gestionar = administrador, jefe de proyectos y planner; ver = roles con economía + planner, con alcance por OT al leer. **Nuevo** (aprobado en el Spec): versión nueva tras una aprobada = administrador y jefe de proyectos.

## Qué NO hacer

- Aplica solo tus migraciones (076–078), según el protocolo; no edites `db/README.md`. No edites `pr/page.tsx`, `dashboard/page.tsx`, `curva-s/**`, `src/lib/pr/**`, `src/lib/dashboard/**`. No edites `paquetes-trabajo/**` ni `rdts/**`.
- No cambies otros permisos que el indicado. No quites el bloqueo de transición a ejecución. Sin push.
- Ante contradicción con un flujo, acción destructiva o duda de negocio: detente y devuelve la pregunta.

## Cierre

**Skills:** al empezar, lista `.claude/skills/` de `pg_control_proyectos` (hoy: `cerrar-tanda`, `verificar-permisos-por-rol`, `seguir-flujo-de-planes`) y del repositorio de la app (hoy sin carpeta de Skills) y anota «Skills revisados» en tu `resultados/F3-B.md`. **Usa `cerrar-tanda` al terminar** (adaptación de este plan: sus pasos de estados, evidencia y traspaso van en tu `resultados/F3-B.md`, no en el plan ni en el progreso compartidos). **Usa también `verificar-permisos-por-rol`**: añades `puedeCrearVersionPlanMaestro` a `permisos.ts`; verifica los 13 roles contra las tablas 1 y 2 del flujo 14 (función y API, llamadas sin efecto).

`resultados/F3-B.md` (estado de F3B-1 a F3B-6, handoff con migraciones aplicadas y verificadas (la relajación de WBS único ya la autorizó Victor), llamadas). Commit en `local-worker-2`, `git add` explícito.
