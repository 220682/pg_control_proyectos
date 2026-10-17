# 08 — Programa / portafolio / proyecto
> Lee si: la tarea crea, adjudica, archiva o elimina un proyecto, programa o portafolio. Quién puede cada acción está en el flujo 14, tabla 2; no se repite aquí.


Ciclo de vida de contenedores. Spec `2026-08-16-programa-portafolio-proyecto`. Quién puede cada acción: tabla 2 del [flujo 14](14-accesos-y-restricciones.md) (no se repite aquí).

**Adjudicar y crear:** adjudicar un proyecto y crear un programa o un portafolio: administrador, jefe de proyectos y jefe de oficina técnica.

**Borrado administrador:** archivar y eliminar un proyecto, y eliminar un contenedor (programa o portafolio): administrador y jefe de proyectos. El jefe de oficina técnica **no** archiva ni elimina proyectos (regla transversal «Borrado administrador» del [índice](README.md)). Cascada en `borrado-cascada.ts` (RDT + storage primero).

**Transición `EN_PLANEACION` → `EJECUCION`:** restrictiva desde PR Fase 2 (regla 8, ver [20-plan-maestro.md](20-plan-maestro.md)) — exige un Plan Maestro en estado `APROBADO` para el proyecto **y, desde el plan Informes de supervisión y Dashboard (Victor, 2026-10-15), un supervisor operativo a cargo asignado** (ver abajo). Sin eso, `POST /api/proyectos/[id]/confirmar-transicion` la rechaza con un mensaje explicando qué falta, validado en servidor (también por URL directa). Quien confirma la transición: administrador, jefe de proyectos y jefe de oficina técnica.

**Estructura de niveles y paso a ejecución:** la carga del DP de un servicio pasa por la **aprobación de sus niveles** en la pantalla de Importar DP (flujo 09): mientras haya filas «para revisar» sin confirmar, «Aprobar niveles» queda bloqueado y la pantalla no deja importar. Como el checklist del servicio exige el DP importado, esas filas frenan en la práctica la transición `EN_PLANEACION` → `EJECUCION`; la transición en sí valida en servidor el Plan Maestro `APROBADO`, el checklist completo y el supervisor operativo a cargo (los documentos de fase CIERRE no cuentan desde O7, ver [flujo 12](12-checklist.md); el bloqueo por filas «para revisar» es de la pantalla, no de la API).

**Supervisor operativo a cargo (Victor, 2026-10-15):** cada servicio tiene **uno solo**, guardado en una columna propia del servicio (`proyectos.supervisor_operativo_id`, migración `099`) que se asigna en **Editar servicio** («Supervisor operativo a cargo»); ya no se deduce del último miembro con rol. Toda pantalla que muestre al responsable operativo (Dashboard, informes) lo toma de ahí. Debe tener el rol supervisor operativo, y el servidor lo valida.

* **Sin supervisor a cargo no hay ejecución:** `POST /api/proyectos/[id]/confirmar-transicion` rechaza `EN_PLANEACION` → `EJECUCION` con «No se puede pasar a Ejecución: el servicio no tiene supervisor operativo a cargo. Asígnalo en Editar servicio»; el botón de confirmar lista lo que falta (Plan Maestro, checklist, supervisor a cargo).
* **En ejecución se puede cambiar, no vaciar:** «vaciar» es quitar un supervisor que estaba asignado; se rechaza pasar de un supervisor a ninguno. Un servicio que ya estaba en ejecución **sin** supervisor (la migración no encontró a nadie al rellenar) no retrocede de estado y se puede seguir editando; el Dashboard muestra «Sin supervisor a cargo» como aviso.
* **Al crear el servicio desde la adjudicación** se guarda el supervisor a cargo.
