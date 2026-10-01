# 08 — Programa / portafolio / proyecto

Ciclo de vida de contenedores. Spec `2026-08-16-programa-portafolio-proyecto`. Quién puede cada acción: tabla 2 del [flujo 14](14-accesos-y-restricciones.md) (no se repite aquí).

**Adjudicar y crear:** adjudicar un proyecto y crear un programa o un portafolio: administrador, jefe de proyectos y jefe de oficina técnica.

**Borrado administrador:** archivar y eliminar un proyecto, y eliminar un contenedor (programa o portafolio): administrador y jefe de proyectos. El jefe de oficina técnica **no** archiva ni elimina proyectos (regla transversal «Borrado administrador» del [índice](README.md)). Cascada en `borrado-cascada.ts` (RDT + storage primero).

**Transición `EN_PLANEACION` → `EJECUCION`:** restrictiva desde PR Fase 2 (regla 8, ver [20-plan-maestro.md](20-plan-maestro.md)) — exige un Plan Maestro en estado `APROBADO` para el proyecto. Sin eso, `POST /api/proyectos/[id]/confirmar-transicion` la rechaza con un mensaje explicando qué falta, validado en servidor. Quien confirma la transición: administrador, jefe de proyectos y jefe de oficina técnica.

**Estructura de niveles y paso a ejecución:** la carga del DP de un servicio pasa por la **aprobación de sus niveles** en la pantalla de Importar DP (flujo 09): mientras haya filas «para revisar» sin confirmar, «Aprobar niveles» queda bloqueado y la pantalla no deja importar. Como el checklist del servicio exige el DP importado, esas filas frenan en la práctica la transición `EN_PLANEACION` → `EJECUCION`; la transición en sí solo valida en servidor el Plan Maestro `APROBADO` y el checklist completo (el bloqueo por filas «para revisar» es de la pantalla, no de la API).
