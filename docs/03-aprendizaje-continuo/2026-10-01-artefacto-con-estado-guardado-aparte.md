# Un artefacto con estado guardado aparte se actualiza en dos sitios

**Fecha:** 2026-10-01
**Origen:** Worker F5-D2 del plan niveles-paquetes-plan-maestro-rdt
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt.md`
**Categoría:** `herramientas/artefactos`

## Hallazgo

El artefacto «Matriz de permisos» guarda su estado en un documento de base de datos (`matriz/actual`) que **pisa los valores por defecto del HTML**. Cambiar solo el HTML no se ve en pantalla. Además, el estado guardado estaba en una versión (v44) distinta de la que citaba el flujo 14 (v42), aunque coincidía fila por fila.

## Qué hacer

1. Al cambiar filas, actualizar **ambos**: el HTML (republicado sobre la misma URL) y el documento `matriz/actual`, con `if_version` para no pisar un cambio ajeno.
2. Si la edición quita la marca «Aprobada», avisar a Victor para que la vuelva a dar.
3. Anotar en el flujo 14 la versión del artefacto solo si se verifica con una lectura previa.

## Destino propuesto

Aprendizaje; se podría incorporar al procedimiento de actualización del artefacto si se vuelve a repetir.
