# F2-C · Pantallas de RDTs y RQ reciben y preseleccionan el servicio

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F2 · **Depende de:** F2-A y F2-B cerradas.
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-05 | Crear RDTs con SV1: selector de OT = SV1 y ambos paneles con SV1 | Captura + URL |
| PL-06 | Status de RDTs con SV1: ambos paneles con SV1 y filtro N° OT = SV1 (no aparecen filas de otros servicios) | Captura + URL |
| PL-07 | Archivo de RDTs subidos con SV1: ídem PL-06 | Captura + URL |
| PL-08 | Consolidado RDTs con SV1: selector de servicio = SV1 y consolidado cargado sin clic adicional | Captura + URL |
| PL-09 | Status de Requerimiento con SV1: ambos paneles con SV1 y filtro de OT = SV1; si se cambia la multiselección `ots` de la tabla, el contexto de los paneles sigue siendo SV1 | Captura + URL |
| PL-10 | Consolidado RQ con SV1: ambos paneles con SV1 y filtro N° OT = SV1 | Captura + URL |
| PL-13 | `/proyectos/<SV1>/requerimientos` redirige a Status de Requerimiento y los paneles conservan SV1 | URL final + captura |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

Mecanismo real por pantalla (verificado en 1942b01) y qué hacer:
- `rdts/crear/page.tsx` renderiza `<FormularioCrearRdt />` dentro de `Suspense`, sin props (`FormularioCrearRdt.tsx` ~195; estado `parte.proyectoId`, selector de OT): leer `?proyectoId=` y usarlo como valor inicial.
- `rdts/consolidado/page.tsx` → `<TablaConsolidadoRdts />` (~250; estado `proyectoId` vacío, selector «Elige el N° OT…»): nueva prop de valor inicial y carga automática sin clic.
- `rdts/status/page.tsx` → `TablaStatusRdts` (filtro `numeroOt`, ~40); `rdts/listado/page.tsx` → `TablaListadoRdts` (filtro `numeroOt`, ~36/49); `logistica/consolidado-rq/page.tsx` → `TablaConsolidadoRq` (~54): **sin selector**; el filtro N° OT inicial = N° OT del servicio (el servidor lo resuelve desde el id). El filtro es «contiene» (`PS-0001` coincide con `PS-00010`): usa coincidencia exacta al preseleccionar si aparece el caso (R3).
- `requerimientos/page.tsx` (`searchParams: {estado?, codigo?, ots?}` ~21-29) → `ListadoRequerimientos` (~86; prop `proyectoId={idAncla}`; filtro `numeroOt` ~65): `proyectoId` equivale a `ots=<id>` cuando no viene `ots`; `ots` sigue siendo la selección de la tabla y `proyectoId` el contexto de los paneles. `proyectos/[id]/requerimientos/page.tsx` redirige a `/requerimientos?ots=<id>`: debe conservar el servicio en los paneles (PL-13).
- E1: preseleccionado y **editable**; cambiar el selector actualiza la URL y los paneles (nunca dos servicios a la vez).
- Las salidas tras guardar (`router.push('/rdts/status')` en `FormularioCrearRdt.tsx` ~572; `router.push('/requerimientos')` en `FormularioRequerimiento.tsx` ~177) van en F2-D.

## Qué NO hacer

- No cambies permisos ni quién ve estas pantallas (F2B). No guardes datos: PL-05 se prueba hasta abrir el formulario.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
