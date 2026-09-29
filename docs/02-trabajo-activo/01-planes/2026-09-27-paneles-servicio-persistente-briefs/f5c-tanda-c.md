# F5C-C · Acciones de RQ, registro de costos y descargas

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F5C · **Depende de:** F5C-B cerrada.
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-126 | Descargar registro de costos por servicio: **suma administrador** (el jefe de proyectos conserva); los roles que ven la pantalla pero no descargan (jefe de oficina técnica, supervisor de costos, jefe de costos) no tienen el control y `GET …/registro-costos` les responde 403; logística tampoco descarga | Tabla 13 roles (control y API) |
| PL-139 | Crear RQ: **suma administrador** (los 13 roles); el formulario abre con servicio preseleccionado sin guardar | Tabla 13 roles + captura |
| PL-140 | Actualizar estado de RQ (dar de alta, atendido): **suma administrador**; los botones del consolidado y del Status siguen a la misma función | Tabla 13 roles; PATCH con id inexistente |
| PL-141 | Eliminar requerimiento: **suma jefe de proyectos** | Tabla 13 roles; DELETE con id inexistente |
| PL-142 | Descargar consolidado RQ (PROM-GP-004): se desacopla de "ver" y conserva su conjunto actual (nota 5 del flujo 14); los 13 roles ven el consolidado pero solo esos descargan | Tabla 13 roles (botón y ruta de exportación) |
| PL-143 | Registro de costos, modo "solo subir": logística sube y no ve ni descarga el contenido; se comprueba sin subir (control presente o ausente, y API con archivo ausente) | Capturas por rol + respuesta |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

Fuente de roles: tabla 2 de `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\04-flujos-de-negocio\14-accesos-y-restricciones.md`. Funciones (`permisos.ts`, líneas de 1942b01):
- `puedeCrearRequerimiento` ~154 (hoy todos menos administrador) → **13 roles** (usos: `mi-entorno`, `proyectos/[id]/requerimientos/nuevo`, `POST api/proyectos/[id]/requerimientos/route.ts`); el formulario abre con servicio preseleccionado sin guardar.
- `puedeActualizarEstadoRequerimiento` ~301 (logística) → **suma administrador** (usos: Consolidado RQ, Status RQ/`PanelVerRq.tsx`, notificaciones `AccionesRqEnNotificacion.tsx`, `api/.../[rqId]/estado/route.ts`). **Decisión de Victor 2026-09-29: no suma al jefe de proyectos.**
- `puedeEliminarRequerimiento` ~149 → **suma JP** (`requerimientos`, `api/.../[rqId]/route.ts` DELETE; sin borrar: id inexistente).
- `puedeDescargarConsolidadoRq` ~350: hoy alias de `puedeVerConsolidadoRq` ~331 → **se desacopla y conserva su conjunto actual** (léelo del código; nota 5 del flujo 14); usos: `api/logistica/requerimientos/exportar-004/route.ts` y el botón de `TablaConsolidadoRq.tsx`. Los 13 roles ven el consolidado (F2B-A) pero solo esos descargan.
- **PL-126** `puedeDescargarRegistroCostosServicio` ~309 → **suma administrador** (JP conserva); usos: `GET registro-costos` ~20 y el control de descarga de `PanelRegistroCostos.tsx`. JOT, supervisor de costos, jefe de costos ven la pantalla pero no descargan (sin control y 403); logística tampoco.
- **PL-143** modo «solo subir» (la pantalla ya lo tiene desde F5B-C): logística sube y no ve ni descarga el contenido; se comprueba sin subir (control presente o ausente; API con archivo ausente).
- Método: los 13 roles por función, tabla por acción con UI, prueba unitaria y API sin efecto (R28).

## Qué NO hacer

- No subas ni descargues registros reales ni borres RQ. No toques A13 (descargas no listadas en el artefacto).
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
