# 08 — Programa / portafolio / proyecto

Ciclo de vida de contenedores. Jefe de oficina técnica adjudica. Spec `2026-08-16-programa-portafolio-proyecto`.

**Borrado admin:** solo administrador (o jefe OT en proyecto según permiso). Cascada en `borrado-cascada.ts` (RDT + storage primero).

**Transición `EN_PLANEACION` → `EJECUCION`:** restrictiva desde PR Fase 2 (regla 8, ver [20-plan-maestro.md](20-plan-maestro.md)) — exige un Plan Maestro en estado `APROBADO` para el proyecto. Sin eso, `POST /api/proyectos/[id]/confirmar-transicion` la rechaza con un mensaje explicando qué falta, validado en servidor. Quien confirma la transición sigue siendo el jefe de oficina técnica.
