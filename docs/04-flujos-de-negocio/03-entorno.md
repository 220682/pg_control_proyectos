# 03 — Entorno por rol
> Lee si: la tarea toca «Mi entorno», sus chips, las herramientas disponibles por rol o el perfil propio (celular, correo y contraseña).


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
| administrador, jefe_de_proyectos | Jefatura (antes «Proyecto») |
| jefe_de_oficina_tecnica, supervisor_oficina_tecnica | Oficina Técnica |
| supervisor_operativo | Supervisión operativa |
| supervisor_ssoma | SSOMA |
| supervisor_logistica | Logística |
| supervisor_administracion, rrhh, asistente | Administración |
| planner | Planificación |
| supervisor_costos, jefe_de_costos | Costos |

El título de la pantalla es «Entorno · {grupo}» (por ejemplo, «Entorno · Jefatura»; antes «Entorno · Proyecto»). Solo administrador y jefe de proyectos ven además el bloque «Equipo» con el acceso a gestionar usuarios.

## Perfil propio (Victor, 2026-10-17)

La tarjeta «Mi perfil» muestra nombre, correo, cargo, área, celular y roles. El chip **«Editar mi perfil» lo ven los 13 roles** (antes solo el administrador y el jefe de proyectos) y abre **tres bloques**, cada uno con su botón y su mensaje:

* **Celular:** se ingresa, se cambia o se borra (déjelo vacío). De 6 a 20 caracteres con dígitos, espacios, `+`, guiones y paréntesis.
* **Correo:** correo nuevo y **contraseña actual**. El correo cambia solo cuando se confirma desde el buzón nuevo; hasta entonces la tarjeta dice «pendiente de confirmar» y vale el correo anterior.
* **Contraseña:** la actual, la nueva (mínimo 8 caracteres) y su confirmación, con el ojo de mostrar/ocultar.

**Nombre, cargo, área y roles no se editan aquí:** los asigna el administrador ([flujo 02](02-usuarios.md)). Permisos en la nota 14 del [flujo 14](14-accesos-y-restricciones.md) y reglas del servidor en el [flujo 07](07-nucleo-auth.md). Los textos están en español claro (contraseña actual incorrecta, nueva muy corta o igual a la actual, confirmación distinta, celular o correo inválido, correo ya usado, error de red y éxito) y los botones se desactivan mientras guarda.

Archivos: `src/lib/notificaciones/grupo-proceso.ts` (`herramientasPorGrupo`), `src/lib/config/registro-accesos.ts`, `src/app/(workspace)/mi-entorno/page.tsx`.

`?accion=` en Mi entorno solo **Crear RQ** (`crear-rq`) y **Subir RDTs** (`subir-rdt`), y solo abre el formulario si el rol tiene el permiso. Notificaciones del panel derecho van a `/notificaciones`.

Panel derecho (compartido con flujo 06): chip **Subir RDTs** en Accesos rápidos; clicable sin servicio, igual que Status RQ y Consolidado RQ (acceso con servicio opcional). Mi entorno no muestra el «Salir a Mi entorno»: es el destino de ese chip (regla 7 del flujo 16).
