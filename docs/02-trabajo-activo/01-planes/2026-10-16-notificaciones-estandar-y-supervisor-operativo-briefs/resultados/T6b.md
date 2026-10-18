# Resumen de cierre — T6b Ajuste de avisos de servicio asignado y retirado

Worker 7 (código) · Sonnet 5.5 · rama `local-worker-7` (verificada) · commit `04739ec` sobre `e3c4dfa`. Sin navegador, sin servidor, sin push ni merge. Aplica las decisiones de Victor del 2026-10-18 sobre T6-H1 y T6-H2.

## Qué cambió

1. **Cambio de responsable** (`api/proyectos/[id]/datos`): avisa al anterior con `servicio.retirado` y al nuevo con `servicio.asignado`. Nadie se avisa a sí mismo (si quien edita es el anterior o el nuevo, no se le avisa). Sin cambio no avisa; si antes no había responsable solo avisa al nuevo; si se quita sin poner otro solo avisa al anterior. Al cambiar, se cierra el aviso `servicio.asignado` pendiente del anterior para ese servicio.
2. **Cierre por referencia**: `servicio.asignado` ahora lleva `referencia_id = {servicio}:{persona}`, para cerrar solo el de esa persona (no los de otras personas del mismo servicio). El cierre también se hace al retirar la OT desde Usuarios (misma vía de «dejar de estar a cargo»).
3. **Usuarios** (`api/admin/usuarios/[id]`, `asignarProyectos` y `quitarProyectos`): los avisos de asignación y retiro solo se envían si la persona tiene el rol supervisor operativo (`tieneRolSupervisorOperativo`). Los demás roles no reciben aviso; el cambio de membresía se guarda igual. Se mantiene: solo a los nuevos y solo a quienes realmente se retiran.
4. **Catálogo**: descripción de `servicio.asignado` y `servicio.retirado` actualizada; `servicio.asignado` pasa a cierre automático por referencia. `SITIOS` en `cobertura-avisos.test.ts` no cambió (no hay llamadas nuevas a creadores de avisos; la cobertura pasa).

## Archivos

- `src/lib/servicios/avisos-servicio.ts` (nuevos `avisarCambioDeResponsable` y `cerrarAvisoServicioAsignado`; referencia en `servicio.asignado`).
- `src/app/api/proyectos/[id]/datos/route.ts`, `src/app/api/admin/usuarios/[id]/route.ts`.
- `src/lib/notificaciones/catalogo.ts`.
- `src/lib/requerimientos/doble-base-test.ts` (el doble ahora acepta `upsert` por lotes y resuelve `roles(clave)` también por `rol_id`; solo agrega).
- `src/app/api/proyectos/servicio-asignado-api.test.ts` (pruebas con doble de base, ninguna contra la base real).

No se tocó: pantallas, `permisos.ts`, migraciones, flujos.

## Pruebas nuevas o ajustadas

Vía 2: cambio de A a B avisa a ambos (retirado a A, asignado a B); cierra el «asignado» pendiente de A y no el de otra persona; quitar el responsable avisa solo al anterior; sin responsable previo avisa solo al nuevo; quien cambia no se avisa a sí mismo (como anterior ni como nuevo); mismo responsable o sin tocarlo no avisa. Vía 3: persona con rol de otro tipo o sin rol no recibe aviso pero el cambio se guarda; retirar cierra el «asignado» pendiente; supervisor operativo sigue recibiendo solo por los nuevos y los que de verdad tenía.

## Comandos y resultado

- `npm test`: 178 archivos pasan (1 omitido), 1889 pruebas pasan (6 más que en T6), 1 omitida.
- `npm run lint`: 9 errores, los mismos previos y ajenos; ninguno nuevo.
- `npx tsc --noEmit`: limpio.
- `npx next build --webpack`: compila sin errores.
- Commit `04739ec` con `GIT_LITERAL_PATHSPECS=1` y `git add` explícito.

## Dudas y observaciones

- **Avisos «asignado» anteriores a T6b** no tienen referencia, así que no se cierran al cambiar de responsable; solo los nuevos. Si Victor quiere cerrar también los viejos, hace falta una regla por texto (no hecho).
- Depende de la migración 108 (columna `referencia_id`) para el cierre por referencia; sin ella `cerrarAvisos` devuelve error que se registra en el log y no frena el cambio (mismo caso que T6-H4).
- La vía 1 (crear el servicio) no cambia: el supervisor elegido recibe `servicio.asignado` salvo que sea quien crea.
- Flujos por actualizar por el Documentador: el aviso al responsable anterior y la regla de «solo supervisores operativos» en Usuarios (notificaciones y orden de trabajo/usuarios). No tocados aquí.

Unas 20 llamadas a herramientas.
