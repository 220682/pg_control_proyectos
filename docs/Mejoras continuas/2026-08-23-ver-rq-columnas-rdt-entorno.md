# Lote 2026-08-23 — Ver RQ, columnas consolidado, RDTs en Sup. operativa

**Estado: CERRADO 100 %.** Victor comprobó los 3 puntos en producción (23 ago).

## Pedido (Victor, checklist 23 ago aprobado)

Los 14 puntos del check de prod del lote 22 ago **pasaron**. Este lote es lo siguiente.

1. **Panel Ver RQ:** campo **Aprobado por:**. En el PDF PROM-GP-008, al crear (Solicitado) **no** figura el nombre de logística. Cuando Logística recepciona, ahí sí: nombre de **quien recepcionó**.
2. **Consolidado RQ (entorno Logística):** columna **Comentarios** y, al final, **Acción** (Recepcionado / En almacen / Atendido). No juntas.
3. **Supervisión operativa:** chips Listado RDTs y Consolidado RDTs (igual que en Geren). Geren accede a ese entorno (igual que entra a Logística por los RQ). Geren y supervisor operativo **suben** RDTs.

Pantallas: panel Ver RQ (Status), PDF 008, `/logistica/consolidado-rq`, Mi entorno · Supervisión operativa, panel derecho (Accesos rápidos + acordeón), `/rdts/listado`, `/rdts/consolidado`.

Cambio compartido: `puedeVerRdts`, `puedeSubirRdt`, `herramientasPorGrupo`, `hrefItemPanel` (flujos 03, 06).

## Resultados (prod, 23 ago)

| # | Punto | Pantalla | Prod |
|---|--------|----------|------|
| 1 | Aprobado por + logística en PDF solo al recepcionar | Status → Ver · PDF PROM-GP-008 | OK |
| 2 | Comentarios y Acción en columnas distintas | `/logistica/consolidado-rq` | OK |
| 3 | Listado, Consolidado y Subir RDTs (Geren + sup. operativa) | Panel derecho · Accesos rápidos · Supervisión operativa | OK |

- Panel Ver RQ (Status): campo **Aprobado por** (`revisadoPor`). Vacío en Solicitado.
- PDF PROM-GP-008: Personal Logístico vacío hasta Recepcionado; entonces nombre/celular de **quien recepcionó** (`recepcionado_por`).
- Consolidado RQ: columna **Comentarios** (botón Comentar) y, al final, **Acción**.
- Supervisión operativa: Listado RDTs + Consolidado RDTs. `puedeVerRdts` incluye `supervisor_operativo`. Geren entra igual que a Logística.
- Subir RDTs: `puedeSubirRdt` = supervisor operativo + Geren (admin, jefe OT, jefe de proyectos). SSOMA no. Chip en Accesos rápidos; abre sin servicio (`/mi-entorno?accion=subir-rdt`).
- Compartido: `permisos.ts`, `grupo-proceso.ts`, `nav-proyecto.ts` (flujos 03, 06).

Commits en `main`: `d980ed6` (Aprobado por, columnas, RDTs en nav), `bb3f751` (chip Subir RDTs clicable sin servicio).

## Fuera de este lote

“Pasar responsabilidades a” sigue **fuera** (ya lo era en el lote 22 ago).
