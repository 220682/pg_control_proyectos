# F3-B · Recursos de empresa con mostrar/ocultar, pie del panel y móvil

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F3 · **Depende de:** F3-A cerrada.
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-27 | Recursos de empresa: botón mostrar/ocultar; sin servicio aparece visible por defecto y con servicio, oculto por defecto; el botón funciona en ambos casos; abrir Personal, Cargos o Equipos no cierra el servicio; el apartado es visible y accesible para los 13 roles (A4 ampliado por la matriz base) | Capturas en los dos estados y con las dos cuentas |
| PL-28 | "Materiales" ya no aparece en Recursos de empresa | Captura |
| PL-29 | El pie del panel izquierdo (Usuarios, Notificaciones, Configuraciones, Cerrar sesión, "Ver como", Mi entorno) sigue funcionando, no queda tapado por el nuevo contenido y sus enlaces llevan el servicio | Captura y clic en cada uno |
| PL-49 | Recursos de empresa visible y accesible para los 13 roles: con la cuenta A y con la cuenta B los chips de Personal, Cargos, Equipos y Causas CNC (consulta) están activos y sus pantallas abren; el alta y la baja de Causas CNC solo aparecen para administrador y jefe de proyectos y las llamadas de escritura con otro rol responden 403 | Captura de cada cuenta + respuesta de la API |
| PL-59 | Móvil (390 px): el cajón izquierdo y el derecho muestran el mismo contenido que en escritorio, se cierran al navegar y la página no tiene scroll horizontal | Capturas móvil |
| PL-60 | Escritorio: el panel izquierdo con todos los grupos hace scroll interno y no oculta el pie; con Recursos de empresa oculto queda compacto | Captura |
| PL-62 | Botón mostrar/ocultar con `aria-expanded`, operable con teclado; las secciones usan `<nav>` y encabezados | Snapshot de accesibilidad + prueba con teclado |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- Bloque Recursos actual (`WorkspaceShell.tsx` ~162-203): Personal, Cargos, Equipos, «Materiales» (un `<span>` sin ruta ~178-186, **se elimina**) y Causas CNC (solo con `puedeGestionarCatalogoCnc`). Pasa a: botón mostrar/ocultar (`aria-expanded`, operable con teclado; `<nav>` y encabezados), **visible por defecto sin servicio y oculto con servicio**, disponible con y sin servicio; abrir Personal, Cargos o Equipos no cierra el servicio.
- **Visible y accesible para los 13 roles** (A4 ampliado): chips de Personal, Cargos, Equipos y Causas CNC (consulta) activos; F2B-A ya abrió páginas y APIs de lectura. El alta y la baja de Causas CNC solo aparecen para administrador y jefe de proyectos y la escritura con otro rol responde 403 (`api/recursos/catalogo-cnc/route.ts` POST, `[id]/route.ts` PATCH).
- Pie (`mt-auto`, `pb-[max(3.5rem,env(safe-area-inset-bottom))]`): Usuarios (`puedeGestionarUsuarios`), Notificaciones con badge (`BotonIconoCompacto`), Configuraciones, Cerrar sesión (form con `cerrarSesion`), `SelectorVerComo` (`puedeVerComo`) y Mi entorno (nombre y `rolPrincipal`). No debe quedar tapado por el contenido nuevo; sus enlaces llevan el servicio (A2).
- Móvil: `CajonMovil` (~313-357: `role="dialog"`, `z-50`, `w-[min(18rem,88vw)]`); el contenido del cajón izquierdo es el mismo que en escritorio, se cierra al navegar (lógica `rutaPrevia` ~379-386) y no hay scroll horizontal de página. En escritorio el panel hace scroll interno y no oculta el pie.
- Las llamadas de escritura de CNC con otro rol se prueban con cuerpo inválido/id inexistente (403 = rechazo por rol).

## Qué NO hacer

- No cambies permisos ni implementes gestión de Recursos (F5D). No borres «Materiales» del catálogo de datos: solo del panel.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
