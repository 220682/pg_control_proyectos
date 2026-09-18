# Lote 2026-08-24 — Status estándar, acciones Mi entorno, apartado Proyectos

## Pedido (Victor)

Una interfaz por acción; dos puertas (chip de Mi entorno + panel derecho). El rol habilita o corta.

1. **Status de RDTs** (antes Listado RDTs) es el estándar de pantallas de listado. Replicar a **Status de requerimiento**. Las cuatro pantallas completas (Status RQ, Status RDTs, Consolidado RQ, Consolidado RDTs) llevan chip **Salir a Mi entorno**. Chips de descarga RDT: **Descargar RDTs (según filtro)** y **Descargar listado RDTs (según filtro)**. PDF 0006: columna **Fecha y hora**, sin “(Lima)”.
2. En Mi entorno, `?accion=` solo **Crear RQ** y **Subir RDTs**. Notificaciones del panel derecho no abren Mi entorno; van a `/notificaciones`.
3. **Apartado Proyectos** (panel izquierdo, dentro de un servicio): solo **administrador** y **jefe de proyectos**. No se toca el pie (notificaciones, salir, Mi entorno). Jefe de OT no entra a ese apartado.

Pantallas: `/rdts/listado`, `/rdts/consolidado`, `/requerimientos`, `/logistica/consolidado-rq`, Mi entorno, panel derecho (Notificaciones), sidebar izquierdo con servicio abierto.

Compartido: `nav-proyecto.ts`, `grupo-proceso.ts`, `permisos.ts`, `WorkspaceShell.tsx`, `CabeceraPagina.tsx` (flujos 01, 03, 05, 06).

## Resultados

Código local (24–26 ago), **sin commit/push**. HEAD de prod sigue `bb3f751`.

- Status de RDTs (antes Listado) es el estándar. Status RQ abre `/requerimientos` con la **misma forma de tabla** (filtros y orden en columnas, N° OT dentro de la tabla, sin selector aparte ni chips de estado). Chip **Salir a Mi entorno** en Status RQ, Status RDTs, Consolidado RQ y Consolidado RDTs.
- Chips descarga RDT: **Descargar RDTs (según filtro)** y **Descargar listado RDTs (según filtro)**. PDF 0006: **Fecha y hora**. Status RQ: **Descargar listado RQ (según filtro)**.
- Notificaciones del panel derecho → `/notificaciones`. `?accion=` solo Crear RQ y Subir RDTs.
- Apartado Proyectos (panel izquierdo): solo admin y jefe de proyectos.
- Compartido: `nav-proyecto.ts`, `grupo-proceso.ts`, `permisos.ts`, `WorkspaceShell.tsx`, `CabeceraPagina.tsx` (flujos 01, 03, 05, 06). Status RQ: `filtros-listado.ts`.
- Victor empezó revisión local 24 ago (dev server + fix import `formatearFechaLima` + tabla Status RQ alineada). **No confirmó el lote.** El 26 ago pidió guardar memoria y abrir chat nuevo.

Pendiente: que Victor pruebe en local y, si está bien, commit/push a `main` (no incluir borrados de `docs/Flujos de trabajo/` ni `.cursor/` del repo web).
