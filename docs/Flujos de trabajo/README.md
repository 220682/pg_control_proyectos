# Flujos de trabajo

Fuente de verdad de cada flujo: pantallas, roles, subflujos, archivos. Al desplegar una mejora, actualizar el MD del flujo.

**Interfaz:** al crear una pantalla nueva o modificar una existente en `py_control_proyectos_web`, la convención obligatoria de diseño/UI es [`visual-companion/design.md`](../visual-companion/design.md) — layout, tokens, componentes, columnas, accesibilidad. Leerlo antes de tocar cualquier interfaz.

| # | Flujo | Archivo |
|---|--------|---------|
| 01 | Interfaz / workspace | [01-interfaz.md](01-interfaz.md) |
| 02 | Usuarios | [02-usuarios.md](02-usuarios.md) |
| 03 | Entorno por rol | [03-entorno.md](03-entorno.md) |
| 04 | Notificaciones | [04-notificaciones.md](04-notificaciones.md) |
| 05 | Requerimiento de servicios (RQ) | [05-rq.md](05-rq.md) |
| 06 | RDT | [06-rdt.md](06-rdt.md) |
| 07 | Núcleo / auth | [07-nucleo-auth.md](07-nucleo-auth.md) |
| 08 | Programa / portafolio / proyecto | [08-programa-portafolio-proyecto.md](08-programa-portafolio-proyecto.md) |
| 09 | Importar DP | [09-importar-dp.md](09-importar-dp.md) |
| 10 | Generación PR | [10-generacion-pr.md](10-generacion-pr.md) |
| 11 | Dashboard | [11-dashboard.md](11-dashboard.md) |
| 12 | Checklist editable | [12-checklist.md](12-checklist.md) |
| 13 | Orden de trabajo (OT) | [13-orden-de-trabajo.md](13-orden-de-trabajo.md) |
| 14 | Accesos y restricciones | [14-accesos-y-restricciones.md](14-accesos-y-restricciones.md) |
| 15 | Cronograma | [15-cronograma.md](15-cronograma.md) |
| 16 | Paneles | [16-paneles.md](16-paneles.md) |
| 17 | Chat agéntico | [17-chat-agentico.md](17-chat-agentico.md) |
| 18 | Control de avance | [18-control-avance.md](18-control-avance.md) |
| 19 | Paquetes de trabajo y jerarquía de control | [19-paquetes de trabajo y jerarquia de control.md](19-paquetes%20de%20trabajo%20y%20jerarquia%20de%20control.md) |
| 20 | Plan Maestro | [20-plan-maestro.md](20-plan-maestro.md) |

**Borrado administrador** no es un flujo: es una regla transversal (solo admin destruye RQ / RDT / proyecto / programa / portafolio). Está citada en 05, 06 y 08.

Mejoras: ver [../README.md](../README.md) (orquestador de `docs/`, ciclo de vida de un archivo de Mejoras continuas).

**Checklists de verificación:** cada mejora o fase implementada tiene su checklist en la Punch List de Mejoras (ver `docs/README.md`), así la implementación se haya seccionado en varias fases o sub-lotes — cada una con su propio checklist. El registro cronológico de todos los checklists (cuántos ítems, cuántos Conforme, Observado o Sin verificar) vive en [../Mejoras continuas/resumen-checklists.md](../Mejoras%20continuas/resumen-checklists.md).
