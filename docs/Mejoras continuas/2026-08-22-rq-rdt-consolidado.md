# Lote 2026-08-22 — RQ, RDT, consolidado y gobernanza

## Pedido

1. Código RQ visible al crear (preview automático).
2. PDF PROM-GP-008: quién aprobó, después de aprobar.
3. Fechas `22-08-2026` (ceros, guiones) en UI y PDF.
4. Imágenes del RQ en hojas siguientes (máx. 6 por hoja, ítem + descripción).
5. Quitar eco de notificación al aprobar (Geren/Admin); colores de estado distintos entre sí e **iguales** en Status, consolidado y notificaciones.
6. Borrar RQ: solo Status, solo admin (columna visible). No en consolidado.
7. Pasar responsabilidades a: **pendiente**, no se programa.
8–9. Consolidado RQ: filtros desplegable + orden.
10. Geren puede subir RDT.
11. Consolidado RDTs con las mismas mejoras de filtro/orden/fecha.
12. Gobernanza: carpetas Flujos de trabajo + Mejoras continuas.

Pantallas: crear RQ, PDF RQ, Status RQ, consolidado RQ, Mi entorno (inbox), Subir RDT, consolidado/listado RDT.

Cambio compartido: helper de fecha y `claseBadgeEstado` (flujos 05, 06, 04).

## Resultados

- Gobernanza: `docs/Flujos de trabajo/` (01–13) + `docs/Mejoras continuas/` con esta ficha.
- Crear RQ muestra el código previsto (`GET …/siguiente-codigo`) al elegir OT.
- PROM-GP-008: caja Aprobado con `revisado_por` (nombre/cargo) si el RQ ya no está Solicitado; imágenes jpg/png/webp en hojas 2+ (máx. 6, ítem + descripción).
- Fechas documento `dd-mm-yyyy` (RDT con hora `dd-mm-yyyy HH:mm`) en Status, panel, consolidado, PDF 008/004/0006.
- Inbox de Mi entorno: solo recibidas (sin eco al aprobar). Paleta única `claseBadgeEstado` (Recepcionado naranja, no celeste).
- Eliminar RQ: solo Status, solo admin, columna fija a la derecha. No en consolidado.
- Consolidado RQ: filtros `<select>` + orden por columna; PROM-GP-004 usa el mismo recorte/orden.
- Geren puede Subir RDT. Nuevo `/rdts/consolidado` (mismos filtros/orden/ZIP/0006).
- Pendiente de producto: “Pasar responsabilidades a”. Pendiente de probar en prod (no de programar): adjunto por ítem, 5 estados, PDF 004, borrado admin.
