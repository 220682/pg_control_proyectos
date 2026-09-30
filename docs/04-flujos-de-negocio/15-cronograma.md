# 15 — Cronograma

**Fase 1 implementada (en main, 2026-09-16/17).** Importa Excel (plantilla WBS de programación, rotulada EDT si así viene del origen/Nombre de tarea/Duración/Comienzo/Fin/Predecesoras/Sucesoras) o PDF exportado de MS Project, y genera un **informe de extracción** (cuántas actividades se leyeron, cuántas quedaron completas, cuántas se enlazaron al DP). No lee `.mpp` nativo.

Un cronograma por servicio (`proyecto_cronograma`, `proyecto_id` como llave — volver a subir reemplaza el anterior completo). Actividades en `cronograma_actividades`, tipo TAREA/HITO/RESUMEN.

**Terminología:** EDT y WBS son la misma estructura de descomposición. Para evitar ambigüedad, este flujo llama **WBS de programación** al código de la actividad del cronograma, aunque MS Project o el PDF lo rotule como `EDT`; llama **WBS presupuestal** al código contractual de la partida en DP. Pueden coincidir literalmente, pero no se reescriben para forzarlo.

**Enlace de trazabilidad: SOLO contra DP.** El cronograma relaciona cada tarea con la partida `dp_partidas` que ejecuta (WBS presupuestal), **nunca contra PR**. Si WBS de programación y WBS presupuestal coinciden, el enlace se propone automáticamente; si difieren, se registra un vínculo explícito sin cambiar ninguno de los dos códigos.

Predecesoras/sucesoras son informativas: su ausencia no marca la fila como incompleta.

**Quién sube/reemplaza:** administrador, jefe de proyectos y Planner (tabla 2 del [flujo 14](14-accesos-y-restricciones.md)), sobre un servicio a su cargo. **Quién ve:** los 13 roles (el cronograma no lleva datos económicos, tabla 1); sin alcance por OT al leer (R30). **Descargar la plantilla** (.xlsx generada desde el DP): los 13 roles; un usuario sin rol conocido queda rechazado.

Pantalla: `/cronograma` (selector de OT + carga + informe). El chip **Cronograma** se declara una sola vez en el registro único de accesos (flujo 16), grupo Planificación, y aparece en el panel izquierdo (con servicio), en el panel derecho y en Mi entorno. **Sigue exigiendo un servicio elegido** (`requiereServicio: 'si'`): al abrir se preselecciona el servicio de `?proyectoId=`, y Mi entorno lo envía. Ya no hay un chip propio «del entorno del usuario» que dependa del grupo: los diez chips de Mi entorno son los mismos en todos los grupos (flujo 03).

**Duración del servicio:** las tarjetas de Portafolio y el Dashboard de servicio ahora prefieren la duración calculada del Cronograma (fecha de inicio más temprana → fecha de fin más tardía) sobre la fórmula del presupuesto (que hoy siempre da sin dato, ver flujo 11).

## Pendiente (fase 2, no construida)

- Interfaz Gantt: barra base (fija) + barra de avance real (editable, puede quedar antes/después/más corta/más larga).
- Candado de checklist "Cronograma" antes de pasar de "En Planeación" a "Ejecución".
- Restringir el reemplazo a Geren solo mientras el servicio siga "En Planeación" (hoy cualquiera con permiso de subir puede reemplazar en cualquier momento).
- Flujo 17 (Chat agéntico) usaría el informe de extracción como base.

## Hitos del cronograma (PL-1.6, 2026-09-23)

Una actividad de tipo `TAREA` en el cronograma puede marcarse como **hito** (columna `requiere_partidas = false`), indicando que **no requiere estar vinculada a una partida del DP**. Esto evita que esas actividades bloqueen la generación del Plan Maestro por falta de vínculo.

- El marcado se hace desde la pantalla de Cronograma (columna "Hito" con checkbox por tarea, solo visible para quien tiene permiso de carga).
- Una tarea marcada como hito **no participa** en la regla del 100% de metrado asignado por partida.
- La API de hitos (`/api/cronograma/hitos`) expone GET (listado de actividades marcadas) y PATCH (marcar/desmarcar).
- Migración: `db/072_paquetes_trabajo.sql` (columna `cronograma_actividades.requiere_partidas`, default `true`).

## Relación con Paquetes de Trabajo (2026-09-23)

Las fechas de programación diaria de los Paquetes de Trabajo **no modifican ni dependen** de las fechas del cronograma. El cronograma conserva sus fechas intactas (las fechas del archivo original cargado). La reasignación de metrado por día en los paquetes es libre y no altera ninguna columna de `cronograma_actividades`.

Código: `src/lib/cronograma/` (parsers + informe), `src/app/api/cronograma/route.ts`, `src/app/api/cronograma/hitos/route.ts`, `db/036_cronograma.sql`, `db/072_paquetes_trabajo.sql`.
