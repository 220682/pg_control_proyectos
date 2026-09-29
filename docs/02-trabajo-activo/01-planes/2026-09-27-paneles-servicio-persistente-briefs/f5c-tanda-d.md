# F5C-D · Cierre de acciones: exclusivas del administrador, regresión, alias y alcance por OT

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F5C · **Depende de:** F5C-A, F5C-B y F5C-C cerradas.
**Punto de commit:** Al cerrar la fase F5C (fin de esta tanda).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-144 | Exclusivas del administrador (asignar rol administrador y «Ver como»): sin cambio; el jefe de proyectos no las tiene (no ve el selector de "Ver como" y la API responde 403 a la asignación) | Tabla 13 roles |
| PL-145 | Regresión de las acciones que no cambian (subir RDT, corregir RDT, subir y gestionar cronograma, gestionar Plan Maestro, gestionar paquetes, catálogo CNC, gestionar usuarios, comentar RQ, derivar RQ, subir documento del proyecto): los 13 roles coinciden con la tabla 2 | Tabla 13 roles × acciones |
| PL-148 | Sin efectos colaterales de los alias separados: `puedeEditarServicio`, `puedeImportarDp`, `puedeCorregirRdt`, `puedeRechazarRdtValidado` y `puedeDescargarConsolidadoRq` no cambian a ningún rol que la tabla 2 no cambie (por ejemplo, el jefe de oficina técnica no gana corregir RDT al ganar crear) | Pruebas unitarias por función |
| PL-151 | Alcance por OT: las acciones que la tabla 2 marca "Requiere OT a cargo: Sí" siguen sujetas a `proyecto_miembros` para el jefe de proyectos y el jefe de oficina técnica (solo el administrador salta la restricción); la verificación distingue el rechazo por rol del rechazo por falta de OT | Tabla con mensaje de respuesta por caso |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- **PL-144:** exclusivas del administrador: `puedeAsignarRolAdministrador` (`permisos.ts` ~41) y `puedeSimularRol` (`src/lib/auth/ver-como.ts`; `api/ver-como/route.ts` responde 403 «Solo el administrador puede simular»; `api/admin/usuarios` para asignar rol). El JP no ve el selector de «Ver como» y la API responde 403 a la asignación.
- **PL-145:** regresión de las que no cambian: `puedeSubirRdt`, `puedeSubirCronograma`, `puedeGestionarPlanMaestro`, `puedeGestionarPaquetesTrabajo`, `puedeGestionarCatalogoCnc`, `puedeGestionarUsuarios`, `puedeComentarRequerimiento`, `puedeDerivarRequerimientoLogistica`, `puedeSubirDocumento`: los 13 roles contra la tabla 2 de `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\04-flujos-de-negocio\14-accesos-y-restricciones.md`.
- **PL-148:** pruebas unitarias por función: `puedeEditarServicio`, `puedeImportarDp`, `puedeCorregirRdt`, `puedeRechazarRdtValidado`, `puedeDescargarConsolidadoRq` no cambian a ningún rol que la tabla 2 no cambie (ejemplo: el JOT no gana corregir RDT al ganar crear).
- **PL-151:** las acciones con «Requiere OT a cargo: Sí» siguen sujetas a `proyecto_miembros` para JP y JOT (solo el administrador salta). Distingue el rechazo por rol (`{"error":"No autorizado"}`) del rechazo por falta de OT (`{"error":"No tienes esta OT a cargo"}`, `src/lib/auth/guard-proyecto.ts`); tabla con el mensaje por caso. «Ver como» conserva el alcance del usuario real (R28).
- Si una prueba revela un alias que arrastra un rol, corrígelo aquí y anótalo.

## Qué NO hacer

- No ejecutes escrituras reales. No amplíes el alcance de permisos más allá de la tabla 2.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
