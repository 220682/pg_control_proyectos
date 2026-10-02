# Resultados — Tanda T3 · Worker 1 · carril `local-worker-5`

Worker 1 · DeepSeek V4.1 Flash · rama `local-worker-5`, worktree `py_control_proyectos_web/.worktrees/local-worker-5`, HEAD `5e773c7`, árbol **limpio** al cerrar (sin cambios de código). Dev levantado por este Worker en **3115** y **detenido al cerrar**. Navegador Chrome vía Playwright, un solo navegador. Cuentas leídas con **Read**, nunca impresas. **No se borró nada, sin SQL directo, sin migraciones** (el borrado lo hará Victor).

Método: sesión real (Victor, admin) y llamadas a las APIs de la app con sesión desde la propia página (`fetch` con cookie). «Ver como» por `POST /api/ver-como` + recarga, restaurado con `DELETE /api/ver-como`.

## Registros creados en PS-0009 (lo que Victor debe borrar)

| Pieza | Identificador exacto |
|---|---|
| **Paquete de trabajo** | `PT-001` · id `4bd2dd7c-7e41-4d59-a893-72b90f14f895` · nombre `PRUEBA-DASH Paquete T3` · disciplina Tuberías · modo `POR_PARTIDAS` · 9 vínculos |
| **Vínculo nuevo** (cronograma_actividad_partidas) | partida `a0f8062c-8ffd-4049-9f31-691544fcb963` (WBS 01.01) × actividad `a73dc3aa-b306-48fb-918b-e111a0d982d6`, metrado 1.0 (antes restaba 1) |
| **Plan Maestro v1** | id `3e7e030a-9ffd-4f1a-8fcd-d8a40093ec0b` · version 1 · estado `REEMPLAZADO` (se aprobó **sin** asignaciones persistidas — ver «Posible bug») |
| **Plan Maestro v2 (vigente)** | id `7074c8ad-01ce-4b01-b0c2-c729210e69e2` · version 2 · `APROBADO` · 22 asignaciones (`plan_maestro_asignaciones`) |
| Líneas de v2 (`plan_maestro_partidas`) | `3205310c-7c3b-4366-a38c-6b56dec88c02` (01.01), `7afce8b9-63f8-4751-9ee7-1eea0a1441e0` (02.01), `5b1997db-75d2-4577-af8e-c4b97c71e5e7` (02.02), `b08c7666-9d95-4708-9447-da2965255475` (02.03), `02a77982-903a-405f-9e4f-41242f88b639` (02.04), `8d103217-b723-4c2d-b2f5-b348f81a9380` (02.05), `efeecd05-d69b-4f10-a7bf-bdc0e47d9759` (02.06), `aac3c640-a65f-40e5-94e9-35e1b7a10fcd` (03.01), `00c6705c-cec8-4364-b8c1-8f962383c212` (04.01) |
| **RDT 1** | id `92a97e60-e3df-4fba-89f6-060d5c5df38d` · 2026-08-11 Día · `VALIDADO` · 9 actividades · 16 HH + 8 HM |
| **RDT 2** | id `4fc8d898-53b9-4acb-b167-c4c9940e83c4` · 2026-08-14 Día · `VALIDADO` · 9 actividades · 16 HH + 8 HM |

Derivados recalculados por el motor del PR (no requieren borrado aparte; caen con el proyecto/plan): `plan_maestro_asignaciones` (22 filas), `plan_maestro_partidas` (9 por versión), `rdt_actividades`/`rdt_tareo`/`rdt_equipos_parte`, `pr_partidas`, `pr_recursos`, `rdt_actividad_partidas`.

## Estados

| Ítem | Estado | Evidencia / causa |
|---|---|---|
| **F12** | **Completado** | Bloqueo destrabado: 1 paquete con las 9 partidas del DP, Plan Maestro creado, repartido y **APROBADO** (v2), 2 RDTs estructurados **VALIDADO** que suman **50 %** de avance. Sin SQL, sin migraciones, sin borrar. |
| **F13** | **Completado** | Curva S **económica** (PV/EV/AC USD) y **física** (% PV/BAC y EV/BAC) dibujan con datos reales. Dashboard **Completo** con bloque «Costo real de recursos» con AC > 0 por recurso y Total = AC. Dashboard **Parcial** («Ver como» `supervisor_operativo`) sin USD ni economía, con Bloque E y enlace Curva S. |

### Números reales verificados (fecha de corte 02-10-2026)

- **% avance físico: 50 %** · **BAC US$ 4.482,54** · **PV US$ 4.482,54** · **EV US$ 2.241,27** · **AC US$ 297,76** · SPI 0,50 · CPI 7,53.
- Bloque «Costo real de recursos» (solo Completo): `CAPATAZ` MO 123,04 · `OPERARIO SOLDADOR` MO 111,52 · `MAQUINA DE SOLDAR` HM 52,00 · `ESMERIL ANGULAR 7"` HM 11,20 · resto en 0,00. **Σ recursos MO+HM = US$ 297,76 = Total (AC) = KPI AC** (reconcilia, sin fila «Sin resolver»).
- Curva S económica: serie con `pvAcum`/`evAcum`/`acAcum` > 0 (p. ej. 2026-08-11 pv 2.789,01 / ev 1.120,64 / ac 52,00). Física: `pvPct`/`evPct` (p. ej. 2026-08-11 pv 62,22 % / ev 25 %; cierre ev 50 %).

## Capturas (nuevas, prefijo `T3-`)

- `T3-F13-dashboard-completo-PS-0009.png` — Completo: KPIs económicos (BAC/PV/EV/AC/SPI/CPI), 50 %, bloque «Costo real de recursos» con Total (AC).
- `T3-F13-curva-s-economica-PS-0009.png` — Curva S económica USD con PV/EV/AC reales.
- `T3-F13-curva-s-fisica-PS-0009.png` — Curva S física % con PV/BAC y EV/BAC reales.
- `T3-F13-dashboard-parcial-sin-economia-PS-0009.png` — Dashboard Parcial con «Ver como» `supervisor_operativo`, sin `US$`, con Bloque E y enlace Curva S.

## Posible bug detectado (no se tocó código)

**`PATCH /api/plan-maestro` con `accion:'APROBAR'` acepta `asignaciones` inline, las usa solo para validar y aprueba, pero NO las persiste** (`src/app/api/plan-maestro/route.ts` §APROBAR: solo inserta en la rama `GUARDAR_ASIGNACIONES`). Números exactos: en PS-0009 se aprobó la v1 enviando **22 asignaciones** en el mismo APROBAR; respuesta `200 {ok:true}` y el plan quedó `APROBADO` con **`plan_maestro_asignaciones` = 0 filas** → el Dashboard mostró **PV US$ 0,00** (SPI «Pendiente») hasta que se reaprobó por la vía correcta. Se resolvió **por interfaz/API sin tocar código**: crear versión nueva (v2) → `GUARDAR_ASIGNACIONES` (22 filas) → `APROBAR`; con eso **PV pasó a US$ 4.482,54**. Latente para cualquier caller que asuma que APROBAR con `asignaciones` persiste.

## Handoff (≤15 líneas)

1. F12 **cerrado**: paquete `PT-001` (id `4bd2dd7c-…`) + Plan Maestro v2 APROBADO (id `7074c8ad-…`) + 2 RDTs VALIDADOS; **50 %** de avance.
2. F13 **cerrado**: Curva S económica y física con datos reales; Completo con «Costo real de recursos» AC>0 y Total=AC; Parcial sin economía.
3. AC = US$ 297,76; Total (AC) del bloque = US$ 297,76 (Σ recursos MO+HM = mismo valor); PV US$ 4.482,54 · EV US$ 2.241,27 · BAC US$ 4.482,54.
4. **Bug**: APROBAR con `asignaciones` inline no persiste → PV 0 con plan APROBADO. Se destrabó con versión nueva + GUARDAR_ASIGNACIONES. Verificado, no se tocó código.
5. Capturas `T3-F13-*` (4) en `03-evidencia/capturas/dashboard-economia-y-curva-s/`.
6. «Ver como» restaurado (`DELETE /api/ver-como` → 200); dev 3115 detenido; worktree de la app **limpio**; sin commits.
7. Pendiente Victor: borrar PS-0009 y sus filas/archivos por `proyecto_id` (incluye los registros de la tabla de arriba).
8. **Llamadas: ~68** (dentro del límite ~80).

## Mejoras (de trabajo)

- Para un caller de API: `APROBAR` **no** reemplaza a `GUARDAR_ASIGNACIONES`; hay que guardar el reparto antes de aprobar (o la versión queda sin PV). Ahorra la iteración que costó destrabarlo.
- `window.*` de `browser_evaluate` se pierde entre llamadas tras ciertos renders: conviene re-`fetch` los catálogos/plan dentro de cada evaluate de escritura en vez de depender de estado guardado.
- RDT con varias actividades: `metradoProgramado`/`metradoEjecutado` por orden y personas con `horas:[{ordenActividad,horas}]` bastan; el `wbs` y el paquete los fija el servidor desde el Plan.

## Reglas de negocio detectadas

- Ninguna nueva que editar. Confirmado en vivo: sin partidas declaradas en Paquetes no se crea Plan Maestro (flujo 20); toda partida del DP con metrado contractual necesita al menos una línea para aprobar (validado: 01.01 exigió su vínculo); el RDT exige Plan Maestro APROBADO y clave `paquete|partida` existente. No se editó ningún flujo.

## Observaciones sobre la política

- El bloqueo de T2 («PM sin paquetes») sí era destrabable por interfaz/API en una sola tanda: declarar vínculo faltante, crear 1 paquete, PM, repartir y aprobar consumió ~14 llamadas. El presupuesto de ~80 fue holgado. Queda para clasificación del Auditor.

## Carpetas/archivos huérfanos

- Ninguno detectado. El worktree de la app quedó limpio; no se dejaron archivos temporales en `pg_control_proyectos` (solo capturas y este resultado).

## Fuentes de verdad revisadas

Flujos 19 y 20 (y 06 para RDT); código del worktree (solo lectura): `src/app/api/paquetes-trabajo/route.ts`, `.../vinculos/route.ts`, `src/app/api/plan-maestro/route.ts`, `src/lib/plan-maestro/{lineas,lienzo}.ts`, `src/app/api/rdts/partes/route.ts`, `.../[id]/route.ts`, `src/lib/rdts/{declaracion-paquete,partes-paquetes,partes-paquetes-servidor,catalogo-plan-maestro}.ts`, `src/lib/dp/tarifas-servidor.ts`, `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx`. **Fase E no tocada.**

## Número de llamadas

**~68**.
