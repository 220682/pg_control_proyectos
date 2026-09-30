> Parte de los contratos técnicos compartidos (índice: `00-contratos-tecnicos.md`). Un carril **no cambia** un contrato por su cuenta: si lo necesita, se detiene y devuelve la pregunta al Orquestador. Lo marcado «por confirmar» lo verifica el Worker en el código. Verificado en `main` `45c9e0a`, solo lectura, 2026-09-30.

## C3 · Plan Maestro: líneas y totales (dueño: carril 2)

```ts
type LineaPlanMaestro = {
  id: string; planMaestroId: string;
  dpPartidaId: string; wbs: string; descripcion: string; unidad: string; precioUnitario: number; hhUnidad: number;
  metradoContractual: number;        // de la partida (copia)
  metradoLinea: number;              // porción de esta línea (suma de sus vínculos)
  actividadId: string | null;        // línea = actividad × partida
  paqueteId: string | null; paqueteCodigo: string | null; paqueteNombre: string | null; paqueteOrden: number | null;   // copia
  claveReporte: string;
};
type Asignacion = { lineaId: string; fecha: string /* YYYY-MM-DD */; metradoPlanificado: number };
type RealPorClave = { claveReporte: string; fecha: string; metradoEjecutado: number; hhReales: number };
```
- **Línea = actividad × partida; el Real se muestra por clave de reporte** (paquete × partida), no por línea, porque el RDT declara contra el paquete (C5). Las líneas de una misma clave se suman en su fila «Real».
- Hoy (verificado): `plan_maestro_partidas` tiene `unique (plan_maestro_id, wbs)` (`db/037`) y su `metrado_contractual` se usa para validar la aprobación (`PATCH`); las asignaciones son `unique (plan_maestro_partida_id, fecha)`. Lectores que agregan **por id de línea** y luego por WBS (repetir WBS es seguro si sus entradas se suman): `recalcular_pr_planificado` (`db/061`, `group by wbs`), `curva_s_proyecto` (`db/070`), `pr/page.tsx`, `dashboard/page.tsx`, `api/curva-s/route.ts`. El carril 2 lo **prueba**, no lo asume.
- Migración del carril 2: relajar `unique (plan_maestro_id, wbs)` (**cambio de restricción: requiere la autorización expresa de Victor antes de aplicarse**); añadir `metrado_linea`, `actividad_id`, `clave_reporte`, `paquete_trabajo_id`, `paquete_codigo`, `paquete_nombre`, `paquete_orden`, `hh_und_partida` (sin FK cruzadas a tablas de otros carriles salvo `paquetes_trabajo`, que ya existe).
- API (`src/app/api/plan-maestro/route.ts`; hoy `GET` → `{ plan, partidas, asignaciones, semanas, reales }`, `POST {proyectoId}` → `{ planId, version }`, `PATCH {accion:'GUARDAR_ASIGNACIONES'|'APROBAR', planId, asignaciones:[{partidaId,fecha,metradoPlanificado}]}`):
  - `GET` → `{ plan, lineas: LineaPlanMaestro[], asignaciones: Asignacion[], semanas, reales: RealPorClave[] }`.
  - `POST {proyectoId}`: crea `BORRADOR`; líneas desde vínculos (en paquete o directos) con metrado > 0; si hay versión aprobada, parte de sus asignaciones. **Ya no exige paquetes.**
  - `PATCH`: aprobar exige Σ días por línea = `metradoLinea` **y** Σ líneas por partida = contractual; reemplaza la versión anterior y llama `recalcular_pr_planificado`. Sin cambio de permisos (`puedeGestionarPlanMaestro`; ver = `puedeVerPlanMaestro`, más alcance por OT).
- Totales (lógica pura en `src/lib/plan-maestro/lienzo.ts`), semanas sábado a viernes con `generarSemanasPlanMaestro(min, max)` (`plan-maestro.ts`, existente): avance **físico** (partida: metrado ÷ contractual; paquete y total: ponderado por costo = económico del grupo ÷ BAC del grupo), **económico** (metrado × precio), **HH** (metrado × `hhUnidad`); cada uno semanal y acumulado; igual para lo real. **Caso de prueba obligatorio:** el anexo de 4 semanas del Spec (`…paquetes-y-plan-maestro-grilla.md`, «Anexo»): totales 22,56 / 48,78 / 76,22 / 100 %, económico $ 8 200, HH 172.
