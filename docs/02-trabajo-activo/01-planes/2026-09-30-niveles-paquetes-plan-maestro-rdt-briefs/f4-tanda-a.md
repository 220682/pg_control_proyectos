# F4-A · RDT: datos, catálogo desde el Plan Maestro y real por clave

Lee primero `00-reglas-de-contexto.md`. Carril **4 · RDT** · rama `local-worker-4` (worktree `.worktrees/local-worker-4`, puerto 3114).
Fase F4 · **Depende de:** nada · No depende de la maqueta. Contratos: `00-contratos-tecnicos.md` § C3 (líneas), § C4 (real por clave) y § C5.
**Migraciones reservadas: `db/082`–`084`** (se escriben, **no se aplican**).
**Punto de commit:** al cerrar la tanda, en `local-worker-4`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F4A-1 | Migraciones 082–084: `paquete_trabajo_id uuid null → paquetes_trabajo(id)` en `rdt_actividades` y en `rdt_actividad_partidas` (nulo = partida directa); campos para las filas **derivadas** del modo por avance del paquete (`declaracion_id`, `es_derivada`; nombres **por confirmar con Victor** en el Gate 1). Se conservan `dp_partida_id`, `wbs` y la PK. Idempotentes | Archivos SQL + lectura crítica (sin aplicar) |
| F4A-2 | Lógica pura: **reparto del % del paquete** a sus partidas (reutiliza `repartirAvanceDelPaquete` de `src/lib/paquetes-trabajo/`, que es del carril 3: **lo importas, no lo editas**) y validaciones de la declaración por paquete | Pruebas |
| F4A-3 | `GET /api/rdts/catalogos` devuelve `estadoPlanMaestro` y `lineasPlanMaestro` por **clave de reporte** (C5) desde el Plan Maestro aprobado, en vez de `dp_partidas`/`dp_subpresupuestos`; sin plan aprobado → estado claro | Prueba con datos simulados |
| F4A-4 | `src/lib/rdts/real-por-clave.ts`: `realPorClaveReporte(admin, proyectoId)` (C4): metrado de actividades `D` de partes `VALIDADO`, horas de `rdt_tareo_horas` sin MOI y fecha `fecha_lima`, agregados por clave y día | Prueba con datos simulados |
| F4A-5 | **Clave estable entre versiones** del Plan Maestro: prueba de que un RDT validado contra el paquete P y la partida X se sigue atribuyendo a `P:X` aunque haya una versión nueva (con otro id de línea) | Prueba |

## Contrato técnico verificado (2026-09-30, `45c9e0a`)

- Catálogo hoy: `src/app/api/rdts/catalogos/route.ts` (GET ~15) consulta `dp_partidas` y `dp_subpresupuestos`; si no hay DP, el supervisor escribe a mano (~121). Con el cambio, **sin Plan Maestro aprobado no se puede crear RDT**.
- Vínculo oficial: `rdt_actividad_partidas (rdt_actividad_id, dp_partida_id)` PK compuesta (`db/040`); lo leen `db/052`, `db/053` (`recalcular_pr_desde_rdt`: suma por partida), `db/070` (Curva S), `api/plan-maestro/route.ts` y `partes/[id]/route.ts`. **Ninguno cambia**: la columna nueva es nula y aditiva.
- Horas por actividad: `rdt_tareo_horas (tareo_id, actividad_id, horas)` con `rdt_tareo.es_moi` (`db/026`); las horas de equipos (`rdt_equipos_parte`) no tienen tabla puente y **no entran** al real por clave.
- C/NC: solo las `D` generan metrado; C y NC aportan horas y costo (regla 12, flujos 06 y 18).
- No modifiques `db/053`, `db/061`, `db/070` ni `src/lib/pr`: el PR suma por partida.

## Qué NO hacer

- No apliques migraciones; no edites `db/README.md`. No edites `src/lib/paquetes-trabajo/**`, `plan-maestro/**` ni `niveles/**`. No toques `permisos.ts`.
- No cambies quién crea o valida RDT. Sin push.
- Ante contradicción con un flujo, cambio de contrato o duda de negocio: detente y devuelve la pregunta.

## Cierre

`resultados/F4-A.md` (estado de F4A-1 a F4A-5, handoff con migraciones, llamadas). Commit en `local-worker-4`, `git add` explícito.
