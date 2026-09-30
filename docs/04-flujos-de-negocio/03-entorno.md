# 03 — Entorno por rol

Ruta: `/mi-entorno`. El grupo se elige por el rol de mayor prioridad (`slugEntornoDesdeRoles`) y solo decide el título y los accesos de Notificaciones; **no decide qué chips salen**.

**Geren** (interno): administrador, jefe de oficina técnica, jefe de proyectos.

## Chips / herramientas de Mi entorno

Los chips de Mi entorno salen del registro único de accesos (flujo 16; los accesos con presencia en el panel central) y son **los mismos diez en los ocho grupos**, en este orden: Enviar mensaje, Crear RQ, Status RQ, Consolidado RQ, Cronograma, Plan Maestro, Status de RDTs, Consolidado RDTs, Crear RDTs y Subir RDTs. Lo que el rol no puede usar **se muestra deshabilitado** con título explicativo (regla 2 del flujo 16); el chip deshabilitado es la señal de «no tienes acceso». Con servicio elegido, los chips de pantallas de servicio envían `?proyectoId=` (Cronograma y Plan Maestro también); sin servicio abren la pantalla sin él.

Quién puede usar cada chip lo deciden las tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md); este flujo no las repite. En resumen, para orientarse:

- **Status RQ, Consolidado RQ, Status de RDTs, Consolidado RDTs y Cronograma:** los 13 roles (interfaces sin datos económicos, tabla 1). Enviar mensaje también.
- **Crear RQ:** los 13 roles (incluido el administrador).
- **Crear RDTs y Subir RDTs:** administrador, jefe de proyectos, jefe de oficina técnica y supervisor operativo (tabla 2); el resto los ve deshabilitados.
- **Plan Maestro:** roles con datos económicos y planner (tabla 1); el resto lo ve deshabilitado.

Además, el grupo determina el resto de la pantalla:

| Rol | Grupo entorno |
|-----|----------------|
| administrador, jefe_de_proyectos | Proyecto |
| jefe_de_oficina_tecnica, supervisor_oficina_tecnica | Oficina Técnica |
| supervisor_operativo | Supervisión operativa |
| supervisor_ssoma | SSOMA |
| supervisor_logistica | Logística |
| supervisor_administracion, rrhh, asistente | Administración |
| planner | Planificación |
| supervisor_costos, jefe_de_costos | Costos |

Solo administrador y jefe de proyectos ven además el bloque «Equipo» con el acceso a gestionar usuarios.

Archivos: `src/lib/notificaciones/grupo-proceso.ts` (`herramientasPorGrupo`), `src/lib/config/registro-accesos.ts`, `src/app/(workspace)/mi-entorno/page.tsx`.

`?accion=` en Mi entorno solo **Crear RQ** (`crear-rq`) y **Subir RDTs** (`subir-rdt`), y solo abre el formulario si el rol tiene el permiso. Notificaciones del panel derecho van a `/notificaciones`.

Panel derecho (compartido con flujo 06): chip **Subir RDTs** en Accesos rápidos; clicable sin servicio, igual que Status RQ y Consolidado RQ (acceso con servicio opcional). Mi entorno no muestra el «Salir a Mi entorno»: es el destino de ese chip (regla 7 del flujo 16).
