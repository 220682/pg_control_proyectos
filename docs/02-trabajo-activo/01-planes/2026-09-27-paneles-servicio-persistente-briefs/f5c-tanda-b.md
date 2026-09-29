# F5C-B · Acciones de RDT e importar DP: funciones propias y alineación con la tabla 2

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F5C · **Depende de:** F5C-A cerrada.
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-134 | Importar DP: función propia; **entra el jefe de proyectos y sale el supervisor de oficina técnica** (que sigue viendo el DP); el botón de importar y `POST …/dp` usan la misma función | Tabla 13 roles; POST con cuerpo inválido |
| PL-136 | Crear RDT estructurado: **suma jefe de oficina técnica**; abre `rdts/crear` y el chip está activo (sin guardar) | Tabla 13 roles + captura |
| PL-137 | Validar o rechazar RDT: **suma jefe de oficina técnica**; rechazar un RDT ya validado sigue solo con la fila propia de la tabla 2 y corregir RDT sigue sin el jefe de oficina técnica (funciones separadas) | Tabla 13 roles por las tres acciones; PATCH y PUT sin efecto |
| PL-138 | Eliminar RDT (archivo y parte estructurado): **suma jefe de proyectos**; se comprueba sin borrar (id inexistente) y con revisión del recálculo de PR que dispara | Tabla 13 roles; DELETE con id inexistente |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

Fuente de roles: tabla 2 de `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\04-flujos-de-negocio\14-accesos-y-restricciones.md`. Funciones (`permisos.ts`, líneas de 1942b01):
- **`puedeImportarDp` nueva** (hoy `proyectos/[id]/dp/page.tsx` ~101 usa `puedeSubirDocumento(roles, 'supervisor_oficina_tecnica')`): entra JP, **sale el supervisor de oficina técnica** (que sigue viendo el DP); el botón (`ImportarDp`) y `POST api/proyectos/[id]/dp/route.ts` usan la misma función.
- `puedeCrearRdtEstructurado` ~216 → **suma JOT** (usos: `rdts/status/page.tsx`, `api/rdts/partes/route.ts` POST, `api/rdts/catalogos`, `api/rdts/plantillas`, chip `crear-rdt` en `grupo-proceso.ts`). `puedeCorregirRdt` **nueva** (hoy corregir usa `puedeCrearRdtEstructurado`; usos: `api/rdts/partes/[id]/route.ts` PUT y `rdts/status`) → **el JOT no corrige**. `puedeValidarRdt` ~224 → suma JOT (`rdts/status`, PATCH en `api/rdts/partes/[id]/route.ts`). `puedeRechazarRdtValidado` **nueva** (PATCH RECHAZAR sobre un RDT ya VALIDADO) → el JOT no rechaza uno validado.
- `puedeEliminarRdt` ~175 → **suma JP** (usos: `rdts/listado/page.tsx`, `api/rdts/[id]/route.ts`, `api/rdts/partes/[id]/route.ts` DELETE). Un borrado es irreversible y recalcula el PR (R29): **no se ejecuta ningún borrado**; prueba con id inexistente y revisa el código del recálculo.
- Pruebas: los 13 roles por función; tabla por acción con UI, prueba unitaria y API sin efecto (403 = rol; 404/400 = pasó). Abre `rdts/crear` y verifica el chip activo para JOT sin guardar (PL-136).
- No dejes alias: cada función nueva solo cambia lo que la tabla 2 cambia (PL-148 se cierra en F5C-D).

## Qué NO hacer

- No guardes RDT ni importes DP. No ejecutes borrados. No cambies RQ ni registro de costos (F5C-C).
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
