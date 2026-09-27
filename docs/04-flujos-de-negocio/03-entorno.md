# 03 — Entorno por rol

Ruta: `/mi-entorno`. El grupo se elige por el rol de mayor prioridad (`slugEntornoDesdeRoles`).

**Geren** (interno): administrador, jefe de oficina técnica, jefe de proyectos.

## Chips / herramientas por rol (grupo)

Comunes en todos (si el permiso lo permite): Enviar mensaje, Crear RQ, Status RQ, Consolidado RQ (solo quien `puedeVerConsolidadoRq`).

| Rol | Grupo entorno | Extra |
|-----|----------------|-------|
| administrador | Proyecto | Status de RDTs, Consolidado RDTs, Subir RDT, gestionar usuarios |
| jefe_de_proyectos | Proyecto | igual Geren (sin gestionar usuarios si no aplica — sí puede) |
| jefe_de_oficina_tecnica | Oficina Técnica | Status de RDTs, Consolidado RDTs, Subir RDT |
| supervisor_operativo | Supervisión operativa | Subir RDT, Status de RDTs, Consolidado RDTs |
| supervisor_ssoma | SSOMA | Crear RQ; **sin** Subir RDT |
| supervisor_logistica | Logística | Status, Consolidado RQ |
| supervisor_administracion / rrhh / asistente | Administración | Status de RDTs, Consolidado RDTs |
| planner | Planificación | comunes |
| supervisor_costos / jefe_de_costos | Costos | comunes |
| supervisor_oficina_tecnica | Oficina Técnica | Status de RDTs si `puedeVerRdts` (no: solo Geren+Admin+operativo) |

Archivos: `src/lib/notificaciones/grupo-proceso.ts`, `src/app/(workspace)/mi-entorno/page.tsx`.

`?accion=` en Mi entorno solo **Crear RQ** y **Subir RDTs**. Notificaciones del panel derecho van a `/notificaciones`.

Panel derecho (compartido con flujo 06): chip **Subir RDTs** en Accesos rápidos; clicable sin servicio, igual que Status RQ y Consolidado RQ.
