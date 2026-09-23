# 06 — RDT (Registro diario de trabajo)

Archivo (foto/PDF) ligado a una OT vigente. Fecha Lima `dd-mm-yyyy HH:mm`.

Quien sube: Supervisión operativa **y Geren**. SSOMA no sube (v1).

Quien ve carpeta/listado/consolidado: Geren + Administración + **Supervisión operativa**.

Notificación al subir: solo Administración.

Pantallas: Subir RDT, `/rdts`, `/rdts/listado` (**Status de RDTs**), `/rdts/consolidado`. Nav del apartado Supervisión operativa: Subir RDTs, Status de RDTs y Consolidado RDTs. Chip **Subir RDTs** en Accesos rápidos. Chips de descarga: **Descargar RDTs (según filtro)** (ZIP) y **Descargar listado RDTs (según filtro)** (PDF PROM-GP-0006). Encabezado PDF: **Fecha y hora** (sin “(Lima)”). Chip **Salir a Mi entorno**.

**Borrar RDT:** solo admin (listado/consolidado).

No es el flujo OT: solo se vinculan por N° OT.

**RDT validado alimenta el PR.** Toda actividad registrada (D, C y NC) se carga a una partida — solo las D generan metrado ejecutado; C y NC aportan horas y costo, sin avance (regla 12 de negocio, ver [18-control-avance.md](18-control-avance.md)). El metrado programado del RDT es informativo, no oficial. El CNC (causa de no cumplimiento) se registra contra un catálogo mantenible y es obligatorio para actividades NC.

Spec: `docs/superpowers/specs/2026-08-20-rdt-design.md`.
