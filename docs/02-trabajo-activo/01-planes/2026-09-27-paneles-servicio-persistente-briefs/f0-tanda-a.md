# F0-A · Línea base técnica, inventario de descargas y funciones de permisos

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F0 · **Depende de:** Gate 1 aprobado; el Orquestador creó los archivos de progreso y evidencia (plantillas 03-progreso.md y 04-evidencia.md).
**Punto de commit:** Ninguno (solo evidencia).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-127 | Inventario de descargas y exportaciones del código (rutas de `src/app/api/` con `Content-Disposition`, `BotonDescargarPdf` y descargas por almacenamiento) contra la sección «Descargas» del artefacto y el flujo 14: lo que no figura en el artefacto se **lista y se reporta a Victor**, y su guardia actual no se cambia sin decisión | Inventario en la evidencia |
| PL-146 | Entregable de F0: lista de funciones de `permisos.ts` que cambian (la tabla "Funciones de permisos.ts que cambian" confirmada o corregida contra el código), con las páginas, APIs y guardias de servidor que las usan, sin omitir alias | Tabla en la evidencia |

## Entregable sin ID: LB-01 (línea base técnica)
Antes de tocar código, en el worktree (HEAD `1942b01` = `main`): `npm test`, `npm run lint` y `npx next build --webpack`. Anota en la evidencia los totales de cada uno (pruebas pasadas/falladas; errores y advertencias de lint como número del resumen del runner, no de un filtro de texto). El baseline de lint de 2026-09-23 fue 9 errores y 18 advertencias: vuelve a medirlo. Es la referencia de PL-74 a PL-76 (F6-E).

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- `package.json`: `test` = `vitest run`, `lint` = `eslint`, `build` = `next build`. Con `node_modules` como Junction, dev y build llevan `--webpack` (`docs/01-contexto-repositorio/03-entorno-git-y-worktrees.md` § Worktrees y bundler). `vitest.config.ts`: entorno `node`, `include: src/**/*.test.ts` (no hay pruebas de componentes React).
- **PL-127, descargas del código (verificadas con Grep de `Content-Disposition`, 9 rutas):** `src/app/api/` → `cronograma/plantilla`, `logistica/requerimientos/exportar-004`, `proyectos/[id]/dp/exportar`, `proyectos/[id]/registro-costos`, `proyectos/[id]/requerimientos/exportar`, `rdts/[id]/archivo`, `rdts/exportar`, `rdts/partes/[id]/pdf`, `requerimientos/formato-vacio`. Componente `src/components/ui/BotonDescargarPdf.tsx`, usado en `DetalleRqNotificacion.tsx`, `FormularioRequerimiento.tsx` y `PanelVerRq.tsx`. **Por verificar por el Worker:** si descargan adjuntos de RQ (`api/proyectos/[id]/requerimientos/[rqId]/lineas/[lineaId]/adjuntos/route.ts`) y documentos del checklist (`api/proyectos/[id]/documentos/[documentoId]/route.ts`). Para cada una anota la guardia actual (función de `permisos.ts` o ninguna).
- Compara con la sección «Descargas» del artefacto «Matriz de permisos» (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT, `Artifact` con `action: read`) y con el flujo 14. Lo que no figure se lista para Victor; **su guardia no se cambia** (A13). Esa lista es también la entrada de PL-155 (F7-B).
- **PL-146:** la tabla de referencia es la sección «Funciones de permisos.ts que cambian» del plan (Grep por ese título y lee solo esa sección). Confírmala contra `src/lib/permisos/permisos.ts` (352 líneas) con `Grep` de cada función en `src/`. Ya verificado: `puedeVerRecursos` es alias de `puedeVerApartadoProyectos` (~línea 197); `puedeGestionarCatalogoCnc` ~234 (admin y JP); `proyectos/[id]/dp/page.tsx` ~101 usa `puedeSubirDocumento(roles, 'supervisor_oficina_tecnica')`; `proyectos/[id]/dashboard/page.tsx` ~97 y `api/proyectos/[id]/tipo-dashboard/route.ts` ~12 usan `puedeAdjudicarProyecto`. **No existen aún:** `puedeVerEconomia`, `puedeVerDashboard`, `puedeVerDashboardPortafolio`, `puedeVerPr`, `puedeVerDp`, `puedeVerRegistroCostos`, `puedeVerStatusRequerimiento`, `puedeEditarServicio`, `puedeImportarDp`, `puedeCorregirRdt`, `puedeRechazarRdtValidado`, `puedeGestionarRecursos`. Corrige la tabla si el código la contradice y entrega las páginas, APIs y guardias por función, sin omitir alias.

## Qué NO hacer

- No cambies ninguna guardia ni permiso. No abras el navegador (eso es F0-B).
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
