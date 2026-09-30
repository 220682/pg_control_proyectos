# 01 — Configuración

> **Pendiente de definir/implementar.** Este flujo se llamaba "Interfaz / workspace"; se renombró a "Configuración" pero su contenido específico como flujo de configuración todavía no se ha escrito. Lo que sigue abajo es el contenido original (interfaz/workspace), conservado como referencia hasta que se defina el alcance real de "Configuración" con Victor.

Shell (`WorkspaceShell`), login, adaptación móvil, tablas con scroll.

**Apartado Proyectos** (panel izquierdo): lo ven **todos los roles**; lo que un rol no puede usar se muestra deshabilitado. El pie no se toca (notificaciones, salir, Mi entorno). La regla de los paneles (qué muestra el panel izquierdo con y sin servicio, chips deshabilitados, «Salir a Mi entorno» y el asistente como icono del shell) vive en el flujo 16: ver [`16-paneles.md`](16-paneles.md), secciones «Panel izquierdo», «Reglas de navegación» y «Asistente: elemento del shell fuera de los tres paneles».

Pantallas de listado a pantalla completa (Status RQ, Status RDTs, Consolidado RQ, Consolidado RDTs): chip **Salir a Mi entorno**, que con servicio seleccionado conserva el servicio (`/mi-entorno?proyectoId=…`); ver la regla 7 del flujo 16.

Specs: `2026-08-16-frontend-redesign`, `2026-08-17-workspace-inicio-v2`, nav proyecto.

Pantallas: layout global, `/login`. No es un flujo de negocio.
