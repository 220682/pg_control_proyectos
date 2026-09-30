# 06 — RDT (Registro diario de trabajo)

Archivo (foto/PDF) ligado a una OT vigente. Fecha Lima `dd-mm-yyyy HH:mm`.

**Quién puede qué** (fuente única: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md); no se repiten aquí):

* **Ver** Status de RDTs, Archivo de RDTs subidos y Consolidado RDTs: los 13 roles (no llevan datos económicos). Sin alcance por OT al leer (R30): el servicio de la URL solo preselecciona el filtro N° OT.
* **Subir RDT** (PDF o foto) y **crear RDT estructurado** (PROM-GP-002): administrador, jefe de proyectos, jefe de oficina técnica y supervisor operativo. SSOMA no sube (v1).
* **Validar o rechazar RDT:** administrador, jefe de proyectos y jefe de oficina técnica. **Rechazar un RDT ya validado** (destraba para corregir y dispara el recálculo del PR): solo administrador y jefe de proyectos. Corregir un RDT rechazado: administrador, jefe de proyectos y supervisor operativo.
* **Descargas:** RDTs según filtro (ZIP), listado de RDTs (PDF PROM-GP-0006), PDF de un RDT estructurado y archivo de un RDT subido: los 13 roles; un usuario sin rol conocido queda rechazado.
* **Borrar RDT:** administrador y jefe de proyectos (regla transversal «Borrado administrador» del [índice](README.md)); ver más abajo.

Notificación al subir: solo Administración.

## Pantallas

| Pantalla | Ruta | Contenido |
|---|---|---|
| Subir RDT | Mi entorno `?accion=subir-rdt` | Formulario de subida (solo si el rol puede subir) |
| Crear RDT | `/rdts/crear` | RDT estructurado (PROM-GP-002) |
| **Status de RDTs** | `/rdts/status` | Tabla de RDTs con su estado; aquí se valida, rechaza y corrige según el rol |
| **Archivo de RDTs subidos** | `/rdts/listado` | Los PDF y fotos que llegaron en papel; **aquí se borra un RDT** (columna de borrado solo para quien puede) |
| Consolidado RDTs | `/rdts/consolidado` | Consolidado por filtros |
| Carpeta | `/rdts` | Carpeta de RDTs |

Nav del apartado Supervisión operativa: Crear RDTs, Subir RDTs, Status de RDTs, Archivo de RDTs subidos y Consolidado RDTs. Chip **Subir RDTs** en Accesos rápidos. Las pantallas reciben el servicio con `?proyectoId=` y lo preselecciona en el filtro N° OT. Chips de descarga: **Descargar RDTs (según filtro)** (ZIP) y **Descargar listado RDTs (según filtro)** (PDF PROM-GP-0006). Encabezado PDF: **Fecha y hora** (sin “(Lima)”). Chip **Salir a Mi entorno** (con servicio elegido conserva `?proyectoId=`, flujo 16 regla 7).

**Borrar RDT:** solo en el Archivo de RDTs subidos (`/rdts/listado`); administrador y jefe de proyectos. Es un borrado definitivo: cubre el archivo y el parte estructurado y dispara el recálculo del PR.

No es el flujo OT: solo se vinculan por N° OT.

**RDT validado alimenta el PR.** Toda actividad registrada (D, C y NC) se carga a una partida — solo las D generan metrado ejecutado; C y NC aportan horas y costo, sin avance (regla 12 de negocio, ver [18-control-avance.md](18-control-avance.md)). El metrado programado del RDT es informativo, no oficial. El CNC (causa de no cumplimiento) se registra contra un catálogo mantenible y es obligatorio para actividades NC.

Spec: `docs/superpowers/specs/2026-08-20-rdt-design.md`.
