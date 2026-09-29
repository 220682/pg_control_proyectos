# F5C-A · Acciones de ciclo de vida: adjudicar, transición, archivar, borrar contenedor, editar servicio/checklist/perfil

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F5C · **Depende de:** F5B-C cerrada (fin de F5B).
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-128 | Adjudicar proyecto, crear programa y crear portafolio: **suma administrador y jefe de proyectos** (el jefe de oficina técnica conserva); el resto de roles, sin acceso | Tabla 13 roles (UI, prueba unitaria, API sin efecto) |
| PL-129 | Confirmar transición de estado: **suma administrador y jefe de proyectos**; se mantiene la precondición del Plan Maestro aprobado (validada en servidor, no se ejecuta la transición) | Tabla 13 roles + revisión del guardia |
| PL-130 | Archivar y eliminar proyecto: **el jefe de proyectos entra y el jefe de oficina técnica sale**; administrador conserva | Tabla 13 roles; DELETE con id inexistente (403 o 404) |
| PL-131 | Eliminar contenedor (programa y portafolio): **suma jefe de proyectos** | Tabla 13 roles; DELETE con id inexistente |
| PL-132 | Editar servicio: función propia; **entra el jefe de proyectos y sale el jefe de oficina técnica**; el enlace de la ficha y `api/proyectos/[id]/datos` usan la misma función | Tabla 13 roles; PATCH con cuerpo inválido |
| PL-133 | Editar checklist: **entra el jefe de proyectos y sale el jefe de oficina técnica** (pantalla, enlace de la ficha y API) | Tabla 13 roles; API sin efecto |
| PL-135 | Editar perfil extendido propio: **sale el jefe de oficina técnica** | Tabla 13 roles (UI y API sin efecto) |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

Fuente de roles: tabla 2 de `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\04-flujos-de-negocio\14-accesos-y-restricciones.md` (leer del archivo). Cambios respecto del código (`src/lib/permisos/permisos.ts`, líneas de 1942b01): `puedeAdjudicarProyecto` ~32, `puedeCrearPrograma` ~122, `puedeCrearPortafolio` ~126 → **suman administrador y jefe de proyectos** (JOT conserva); `puedeConfirmarTransicionEstado` ~36 → suma administrador y JP (precondición: Plan Maestro aprobado, validada en servidor); `puedeArchivarProyecto` ~137 y `puedeEliminarProyecto` ~141 → **entra JP, sale JOT**, administrador conserva; `puedeEliminarContenedor` ~180 → suma JP; `puedeEditarServicio` **nueva** (hoy `proyectos/[id]/editar` y `api/proyectos/[id]/datos/route.ts` usan `puedeAdjudicarProyecto`) → entra JP, sale JOT; `puedeModificarChecklist` ~133 → entra JP, sale JOT; `puedeEditarPerfilExtendido` ~322 → sale JOT.
- Usos a cambiar junto con la función (Grep `<función>` en `src/` y revisa cada uno): `programas/**`, `proyectos/nuevo`, `api/proyectos/route.ts`, `siguiente-ot`, `api/programas`, `api/portafolios`, `api/proyectos/[id]/confirmar-transicion`, ficha `proyectos/[id]/page.tsx`, `proyectos/[id]/editar/page.tsx`, `proyectos/[id]/checklist/editar/page.tsx`, `api/proyectos/[id]/checklist/route.ts`, `api/proyectos/[id]` (DELETE/archivar), `mi-perfil`, `api/perfil/route.ts`, y los `estados` de botones en pantalla.
- El interruptor Parcial/Completo ya no usa `puedeAdjudicarProyecto` (F5B-A).
- Las acciones con «Requiere OT a cargo: Sí» siguen sujetas a `proyecto_miembros` para JP y JOT (solo el administrador salta la restricción). **Ninguna prueba ejecuta escrituras ni borrados reales**: por cada acción, estado del botón/chip, prueba unitaria de la función con los 13 roles y llamada a la API sin efecto (id inexistente o cuerpo inválido: 403 por rol = rechazo; 404/400 = pasó la guardia de rol). Tabla 13 roles por acción; «Ver como» con `POST /api/ver-como` (R28).

## Qué NO hacer

- No ejecutes borrados ni archivados reales. No cambies las funciones de RDT/RQ/DP (siguientes tandas).
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
