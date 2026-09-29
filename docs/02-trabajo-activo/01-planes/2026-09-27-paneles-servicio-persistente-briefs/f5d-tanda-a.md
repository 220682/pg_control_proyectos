# F5D-A · Gestión de Recursos: función única, acciones existentes y Personal (editar y desactivar)

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F5D · **Depende de:** F5C-D cerrada (fin de F5C).
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-157 | Existe `puedeGestionarRecursos` (administrador y jefe de proyectos) y `puedeGestionarCatalogoCnc` delega en ella; el POST de Personal deja de usar `puedeVerRecursos`. Pruebas unitarias por los 13 roles | `npm test` |
| PL-158 | Crear Personal (ya existente): con la cuenta A y con "Ver como" administrador y jefe de proyectos, el formulario crea sin error; con la cuenta B o cualquier otro rol, sin control visible y `POST /api/recursos/personal` responde 403 | Capturas + respuesta API |
| PL-159 | Crear Causa CNC (ya existente): mismo patrón que PL-158 sobre `POST /api/recursos/catalogo-cnc` | Capturas + respuesta API |
| PL-160 | Activar o desactivar Causa CNC (ya existente): mismo patrón sobre `PATCH /api/recursos/catalogo-cnc/[id]` con `activo` | Capturas + respuesta API |
| PL-161 | Editar Personal existente (construir): botón o control de editar en `TablaPersonal.tsx`, `PATCH /api/recursos/personal/[id]` nuevo; administrador y jefe de proyectos editan sin error, cualquier otro rol no ve el control y la API responde 403 | Capturas + respuesta API |
| PL-162 | Eliminar o desactivar Personal (construir): control que pone `activo = false` (nunca borra la fila); mismo patrón de permiso que PL-161; el trabajador desactivado deja de aparecer en el desplegable de Crear RDT | Capturas + verificación en Crear RDT |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- `puedeGestionarRecursos` **nueva** (administrador y jefe de proyectos; único punto de cambio): reemplaza `puedeVerRecursos` en el POST de Personal (`src/app/api/recursos/personal/route.ts` ~42) y `puedeGestionarCatalogoCnc` (`permisos.ts` ~234) delega en ella (mismo patrón de F5C).
- Ya existen y solo se **confirman** con la función nueva: crear Personal (`TablaPersonal.tsx`, POST), crear Causa CNC (`api/recursos/catalogo-cnc/route.ts` POST ~28) y activar/desactivar Causa CNC (`catalogo-cnc/[id]/route.ts` PATCH con `activo`).
- **Construir:** editar Personal y desactivar Personal: control en `TablaPersonal.tsx` y `PATCH /api/recursos/personal/[id]` (archivo nuevo). «Eliminar» = `activo = false`, **nunca borrado físico**. El trabajador desactivado deja de aparecer en el desplegable de Crear RDT (revisa `api/rdts/catalogos/route.ts`: por verificar por el Worker).
- Escritura: `api/recursos/personal/route.ts` valida rol y usa `crearClienteAdmin()` (`src/lib/supabase/admin.ts`) para insertar (~línea 61); las tablas `recursos_*` solo tienen política RLS de `select` (`db/025`, `026`), así que la escritura pasa por el cliente admin **tras** la guardia de rol. Sigue ese patrón; **sin migraciones ni cambios en `db/`**.
- Reglas que no cambian: DNI único; cargo tomado del catálogo activo (`recursos_cargos.activo = true`).
- **Datos reales (pregunta abierta para Victor, plan v8 §Resumen):** PL-158, 159, 160, 161 y 162 dicen «crea/edita sin error», pero el método del plan es solo lectura. **Hasta que el Orquestador confirme que Victor autorizó registros de prueba marcados, no escribas datos reales:** verifica el control presente y la API con cuerpo inválido/id inexistente (400/404 = pasó la guardia; 403 = rechazo por rol) y deja el camino feliz `Observado` con esa causa.

## Qué NO hacer

- No cambies el catálogo de Materiales ni qué recursos son «de empresa». No borres filas nunca.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
