# 15 — Cronograma
> Lee si: la tarea toca el cronograma, sus hitos o su relación con los Paquetes de Trabajo.


**Fase 1 implementada (en main, 2026-09-16/17).** Importa Excel (plantilla WBS de programación, rotulada EDT si así viene del origen/Nombre de tarea/Duración/Comienzo/Fin/Predecesoras/Sucesoras) o PDF exportado de MS Project, y genera un **informe de extracción** (cuántas actividades se leyeron, cuántas quedaron completas, cuántas se enlazaron al DP). No lee `.mpp` nativo.

**Si la importación falla (RB4, decidido por Victor 2026-10-02):** la pantalla muestra el **motivo específico** del fallo (el texto real del error, sin mensaje genérico) y el error queda **logueado en servidor** con el formato del archivo, su nombre y el mensaje, para trazabilidad. Un fallo de lectura o de parseo no se reporta nunca solo como «error».

Un cronograma por servicio (`proyecto_cronograma`, `proyecto_id` como llave — volver a subir lo reemplaza completo, salvo la «Recarga bloqueada» de más abajo). Actividades en `cronograma_actividades`, tipo TAREA/HITO/RESUMEN.

**Terminología:** EDT y WBS son la misma estructura de descomposición. Para evitar ambigüedad, este flujo llama **WBS de programación** al código de la actividad del cronograma, aunque MS Project o el PDF lo rotule como `EDT`; llama **WBS presupuestal** al código contractual de la partida en DP. Pueden coincidir literalmente, pero no se reescriben para forzarlo. **Tipos de actividad:** TAREA, HITO y ACTIVIDAD (antes "RESUMEN" o "Actividad resumen"; unificado en observación O2 de Victor, 2026-10-02).

**Enlace de trazabilidad: SOLO contra DP.** El cronograma relaciona cada tarea con la partida `dp_partidas` que ejecuta (WBS presupuestal), **nunca contra PR**. Si WBS de programación y WBS presupuestal coinciden, el enlace se propone automáticamente; si difieren, se registra un vínculo explícito sin cambiar ninguno de los dos códigos.

Predecesoras/sucesoras son informativas: su ausencia no marca la fila como incompleta.

**El cronograma solo carga y muestra.** Desde el plan niveles-paquetes-plan-maestro-rdt (2026-09-30) la pantalla del Cronograma ya no edita vínculos con metrado, ni la regla del 100 % por partida, ni hitos, ni lista «partidas incompletas»: la carga, el informe de extracción y la vista de actividades quedan; el **metrado exacto por vínculo y los hitos se declaran en Paquetes** ([flujo 19](19-paquetes-de-trabajo-y-jerarquia-de-control.md)). Se conserva el vínculo simple tarea ↔ partida y el enlace automático por EDT.

**El Plan Maestro es el umbral del cronograma (Enmienda E1, Victor 2026-10-03; deroga la observación O3).** Antes de aprobar el Plan Maestro, el cronograma es un dato de planeación editable junto con el DP, el PR, los paquetes y el propio Plan Maestro. **Aprobado** el Plan Maestro, el cronograma queda **congelado**: no se editan actividades individuales ni se reemplaza el documento (subir un archivo nuevo). Se retira la edición individual de actividades que existía con Plan Maestro aprobado (era de Admin y Jefe de Proyectos). La vía para cambiar el cronograma es crear una **versión nueva del Plan Maestro** con motivo obligatorio; al aprobarla, los RDT se reposicionan a las nuevas fechas y metrados (flujo 06, U4).

**Mapa de niveles.** Igual que el DP ([flujo 09](09-importar-dp.md)), la carga tiene un paso de **confirmación de niveles** antes de guardar: roles propios del cronograma (Servicio, Área, Fase, Actividad resumen, Tarea), un rol por nivel, fila de muestra por grupo de hermanas, columna Duración y filas «para revisar» que **bloquean «Aprobar niveles»** hasta confirmarse. Se guarda en `servicio_niveles` y `servicio_encabezados` con origen `CRONOGRAMA`, y se resume en el informe de extracción.

**Recarga bloqueada.** Con Plan Maestro `APROBADO`, volver a subir el cronograma está **bloqueado**. Sin Plan Maestro aprobado, si hay algo que perder (vínculos, paquetes, borrador del Plan Maestro) se muestra el aviso de lo que se perdería y se pide confirmación; sin nada que perder, la carga es libre (misma regla que el DP, flujo 09).
**Quién sube/reemplaza:** administrador, jefe de proyectos y Planner (tabla 2 del [flujo 14](14-accesos-y-restricciones.md)), sobre un servicio a su cargo. **Quién ve:** los 13 roles (el cronograma no lleva datos económicos, tabla 1); sin alcance por OT al leer (R30). **Descargar la plantilla** (.xlsx generada desde el DP): los 13 roles; un usuario sin rol conocido queda rechazado.

Pantalla: `/cronograma` (selector de OT + carga + informe). El chip **Cronograma** se declara una sola vez en el registro único de accesos (flujo 16), grupo Planificación, y aparece en el panel izquierdo (con servicio), en el panel derecho y en Mi entorno. **Sigue exigiendo un servicio elegido** (`requiereServicio: 'si'`): al abrir se preselecciona el servicio de `?proyectoId=`, y Mi entorno lo envía. Ya no hay un chip propio «del entorno del usuario» que dependa del grupo: los diez chips de Mi entorno son los mismos en todos los grupos (flujo 03).

**Duración del servicio:** las tarjetas de Portafolio y el Dashboard de servicio ahora prefieren la duración calculada del Cronograma (fecha de inicio más temprana → fecha de fin más tardía) sobre la fórmula del presupuesto (que hoy siempre da sin dato, ver flujo 11).

## Pendiente (fase 2, no construida)

- Interfaz Gantt: remitida a [planes-futuros.md](../02-trabajo-activo/01-planes/planes-futuros.md); no está construida ni forma parte del plan vigente.
- Candado de checklist "Cronograma" antes de pasar de "En Planeación" a "Ejecución".
- Restringir el reemplazo a Geren solo mientras el servicio siga "En Planeación" (hoy cualquiera con permiso de subir puede reemplazar en cualquier momento).
- Flujo 17 (Chat agéntico) usaría el informe de extracción como base.

## Hitos del cronograma (PL-1.6, 2026-09-23; declarados en Paquetes desde 2026-09-30)

Una actividad de tipo `TAREA` puede marcarse como **hito** (columna `requiere_partidas = false`), indicando que **no requiere estar vinculada a una partida del DP**. Esto evita que esas actividades bloqueen el Plan Maestro por falta de vínculo.

- **El marcado ya no se hace en la pantalla del Cronograma** (se retiró la columna «Hito»): se declara en la pantalla de Paquetes, donde el hito aparece atenuado con la marca ◆ Hito y sin campo de metrado ([flujo 19](19-paquetes-de-trabajo-y-jerarquia-de-control.md)).
- Una tarea marcada como hito **no participa** en la regla del 100 % de metrado repartido por partida.
- La ruta de hitos (`/api/cronograma/hitos`) y `PATCH /api/cronograma` se conservan en el servidor para uso de Paquetes; el `PUT /api/paquetes-trabajo/vinculos` también marca hitos.
- Migración: `db/072_paquetes_trabajo.sql` (columna `cronograma_actividades.requiere_partidas`, default `true`).

## Relación con Paquetes de Trabajo

Los paquetes **no tienen fechas** (flujo 19): el cronograma conserva siempre las fechas del archivo original cargado y nada de Paquetes las modifica ni depende de ellas. Las fechas de las actividades se usan solo como **guía sombreada** en el lienzo del Plan Maestro ([flujo 20](20-plan-maestro.md)), sin limitar el reparto. Los vínculos tarea ↔ partida con metrado se declaran en Paquetes y alimentan `recalcular_pr_fechas_base` (fechas base del PR).

Código: `src/lib/cronograma/` (parsers, informe y `niveles.ts`), `src/app/api/cronograma/route.ts`, `src/app/api/cronograma/hitos/route.ts`, `db/036_cronograma.sql`, `db/072_paquetes_trabajo.sql`, `db/073_*` y `db/074_*` (niveles).
