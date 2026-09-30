# Contratos técnicos compartidos (fijados antes de empezar)

Su propósito: que los cuatro carriles construyan **a la vez** contra formas acordadas, sin esperar el código de otro carril. Un carril **no cambia** un contrato por su cuenta: si necesita hacerlo, se detiene y devuelve la pregunta al Orquestador. Lo marcado «por confirmar» lo verifica el Worker en el código antes de usarlo. Verificado en el código de la app (`main` `45c9e0a`, solo lectura, 2026-09-30).

Lee solo la sección que tu brief nombre (Grep del título).

## C1 · Niveles (dueño: carril 1)

```ts
type RolNivel = 'SERVICIO' | 'AREA' | 'SUBPRESUPUESTO' | 'PAQUETE_PARTIDAS' | 'PARTIDA';            // DP
type RolNivelCronograma = 'SERVICIO' | 'AREA' | 'FASE' | 'ACTIVIDAD_RESUMEN' | 'TAREA';             // nombres por confirmar (hito = duración 0, como hoy)
type MapaNiveles = { origen: 'DP' | 'CRONOGRAMA'; niveles: { nivel: number; rol: string }[]; confirmado: boolean };
type NodoEstructura = {                                   // lo que consumen las pantallas de todos los carriles
  id: string; codigo: string; nombre: string; nivel: number; rol: string;
  padreId: string | null; tipo: 'ENCABEZADO' | 'PARTIDA' | 'ACTIVIDAD' | 'TAREA' | 'HITO'; orden: number;
};
```
- El orden de roles es fijo: Servicio > Área > Subpresupuesto > Paquete de partidas > Partida. Servicio y Partida obligatorios; Partida siempre el último nivel. El nivel extra de 5 niveles entra en el nivel 2 («Área»).
- Módulo: `src/lib/niveles/` (nuevo, carril 1). Expone `construirArbol(filas, mapa): NodoEstructura[]`. **Hasta la integración**, los carriles 2, 3 y 4 construyen sus pantallas recibiendo `NodoEstructura[]` por props y usan datos simulados o el agrupador actual (`agruparPorSubpresupuesto`, `src/lib/dp/subpresupuestos.ts`); no importan `src/lib/niveles/`.
- Hoy (verificado): subpresupuesto = WBS de 1 segmento (`/^\d+$/`) y paquete de partidas = 2 segmentos (`/^\d+\.\d+$/`) en `src/lib/dp/parser-cd.ts`; tablas `dp_subpresupuestos` (`db/031`) y `dp_paquetes` (`db/034`); `reemplazar_dp` vigente = firma de 13 parámetros en `db/071`. Esas dos tablas se conservan pobladas hasta migrar todos los consumidores.
- Bloqueo de recarga: `src/lib/proyectos/bloqueo-recarga.ts` (carril 1). `evaluarRecarga(admin, proyectoId, origen: 'DP' | 'CRONOGRAMA'): Promise<{ bloqueadoPorPlanAprobado: boolean; perderia: { vinculos: number; paquetes: number; planMaestroBorrador: boolean } }>`. Lee solo tablas que ya existen (`proyecto_plan_maestro`, `paquetes_trabajo`, `cronograma_actividad_partidas`). Con plan `APROBADO` la API responde 409 sin opción de confirmar; sin él, exige `confirmarPerdida: true` tras mostrar el aviso. El borrador no bloquea.

## C2 · Paquetes y vínculos (dueño: carril 3)

- **Vínculo declarado** = fila de `cronograma_actividad_partidas` (PK `(cronograma_actividad_id, dp_partida_id)`, `db/039`, más `metrado` numérico nulo o > 0, `db/071`). Hoy una actividad puede tener varias partidas y una partida varias actividades.
- Tabla nueva `paquete_trabajo_vinculos`:
  `(paquete_id uuid → paquetes_trabajo(id) on delete cascade, cronograma_actividad_id uuid, dp_partida_id uuid, primary key (paquete_id, cronograma_actividad_id, dp_partida_id), foreign key (cronograma_actividad_id, dp_partida_id) → cronograma_actividad_partidas on delete cascade, unique (cronograma_actividad_id, dp_partida_id))`. Un vínculo pertenece a **a lo más un** paquete; una **partida** sí puede estar en varios paquetes (por vínculos distintos).
- `paquetes_trabajo` suma `orden int not null default 0` y `nivel int null` (nivel del árbol donde se muestra). Sin fechas. `paquete_trabajo_partidas` y `paquete_trabajo_programacion` (`db/072`) **se conservan sin uso** (no se borran ni se leen).
- **Clave de reporte** (estable entre versiones del Plan Maestro y usada por RDT): `claveReporte = (paquete_trabajo_id | 'DIRECTA') + ':' + dp_partida_id`. Un paquete con dos actividades sobre la misma partida = **una** clave (se suman sus vínculos).
- API (hoy: `GET` devuelve `{ paquetes, partidasDp }`; `POST` recibe `{ proyectoId, nombre, descripcion, modoMedicion, partidas[] }`; `PATCH` recibe `{ paqueteId, accion: 'ARCHIVAR' }`; `src/app/api/paquetes-trabajo/route.ts`). Forma nueva:
  - `GET ?proyectoId=` → `{ paquetes: { id, codigo, nombre, nivel, orden, modoMedicion, guiaDpPartidaId, estado, vinculos: { actividadId, dpPartidaId, metrado }[] }[], actividades: NodoEstructura[], partidasDp: { id, wbs, descripcion, unidad, metradoContractual, precioUnitario, hhUnidad }[], restantePorPartida: Record<dpPartidaId, number> }`.
  - `PUT /api/paquetes-trabajo/vinculos` (archivo nuevo) `{ proyectoId, vinculos: { actividadId, dpPartidaId, metrado }[], hitos: { actividadId, requierePartidas: boolean }[] }`: fija los vínculos con metrado y la marca de hito (`cronograma_actividades.requiere_partidas`, `db/072`), y llama `recalcular_pr_fechas_base` (RPC existente, `db/062`) como hoy hace `PATCH /api/cronograma`.
  - `POST` `{ proyectoId, nombre, nivel, modoMedicion, guiaDpPartidaId?, vinculos: { actividadId, dpPartidaId }[] }`; `PATCH` `{ paqueteId, accion: 'EDITAR' | 'MOVER' | 'ARCHIVAR', … }`. Edición solo en `BORRADOR`.
- Regla del 100%: Σ metrado declarado por partida = contractual, exigida **para abrir el Plan Maestro** (no para guardar un paquete). Hitos no cuentan. Lógica hoy en `src/lib/cronograma/vinculos.ts` (`sumarMetradoPorPartida`, `partidasConMetradoIncompleto`); carril 3 la **copia** a `src/lib/paquetes-trabajo/`; carril 1 la retira del cronograma (no hay archivo compartido).
- Permisos (sin cambios): ver = `puedeVerPaquetesTrabajo` (13 roles); gestionar = `puedeGestionarPaquetesTrabajo` (= `puedeGestionarPlanMaestro`: administrador, jefe de proyectos, planner), `src/lib/permisos/permisos.ts`.

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

## C4 · Real por clave (dueño: carril 4, consume carril 2)

`realPorClaveReporte(admin, proyectoId): Promise<RealPorClave[]>` en `src/lib/rdts/real-por-clave.ts`. Fuente (verificada): partes `VALIDADO` (`rdt_partes.estado_validacion`, fecha `fecha_lima`); metrado = `rdt_actividades.metrado_ejecutado` solo de `ta = 'D'`; horas = `rdt_tareo_horas (tareo_id, actividad_id, horas)` de `rdt_tareo` con `es_moi = false`; vínculo = `rdt_actividad_partidas` + la columna nueva `paquete_trabajo_id`. El EV se calcula al leer (metrado × precio). Horas de equipos **no** entran (`rdt_equipos_parte` no tiene tabla puente). Mientras no exista, el carril 2 lee `reales: []` detrás de un adaptador.

## C5 · RDT desde el Plan Maestro (dueño: carril 4)

- Columnas nuevas (aditivas): `rdt_actividades.paquete_trabajo_id uuid null → paquetes_trabajo(id)` y `rdt_actividad_partidas.paquete_trabajo_id uuid null` (nulo = partida directa). Se conservan `dp_partida_id`, `rdt_actividades.wbs` (texto) y la PK `(rdt_actividad_id, dp_partida_id)`; el motor del PR (`recalcular_pr_desde_rdt`, `db/053`) y la Curva S (`db/070`) **no se modifican**: suman por partida.
- `GET /api/rdts/catalogos` (hoy devuelve DP y subpresupuestos, `src/app/api/rdts/catalogos/route.ts`) devuelve además `estadoPlanMaestro: 'APROBADO' | 'SIN_PLAN'` y `lineasPlanMaestro: { claveReporte, paqueteId, paqueteCodigo, paqueteNombre, paqueteOrden, modoMedicion, guiaDpPartidaId, dpPartidaId, wbs, descripcion, unidad, metradoClave }[]`. Sin plan aprobado, **no se puede crear RDT** (mensaje claro).
- Hoy la validación (`PATCH` de `src/app/api/rdts/partes/[id]/route.ts`, ~244-294) resuelve `wbs → dp_partidas.id` y reescribe `rdt_actividad_partidas`; con el cambio exige que `(paquete, partida)` esté en el Plan Maestro aprobado y guarda el paquete en el vínculo. Modo «por avance del paquete»: las filas derivadas de las demás partidas son de solo lectura y las recalcula el servidor; **su representación exacta (`declaracion_id`, `es_derivada`) es una pregunta abierta para Victor en el Gate 1**.
- Permisos (vigentes, sin cambio): crear RDT = administrador, jefe de proyectos, jefe de oficina técnica y supervisor operativo; validar o rechazar = administrador, jefe de proyectos y jefe de oficina técnica; rechazar uno ya validado = administrador y jefe de proyectos.

## C6 · Interfaz

- Sin pruebas de componentes (`vitest`: `environment: 'node'`, `include: src/**/*.test.ts`): **toda la lógica de la pantalla vive en módulos puros con prueba**; el componente solo la pinta.
- Ningún chip ni acceso nuevo. La acción «Crear paquete» del panel (`registro-accesos.ts`, id `crear-paquete`, `/paquetes-trabajo?proyectoId=&accion=crear`) **se conserva**; ya llega a la pantalla como `abrirNuevoAlInicio` y debe abrirla en modo «crear» (casillas activas).
- Paneles ocultables: control del shell (`WorkspaceShell.tsx`: asides de escritorio `lg:flex`, izquierdo `w-60` y derecho `w-64`), recordado por usuario; en móvil los paneles ya son un cajón. El icono flotante del asistente (abajo a la derecha, dentro del `main`) no debe tapar columnas del lienzo.
- `design.md` (lectura por secciones: §3, §5, §8, §9, §10, §12) y las maquetas aprobadas de F0 mandan en la interfaz; si falta un componente, se anota como hallazgo, no se inventa.
