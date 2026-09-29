# F1-B · Migrar Mi entorno, Accesos rápidos y rutas fijas al registro

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F1 · **Depende de:** F1-A cerrada (existe `registro-accesos.ts` con sus derivaciones; verifica sus nombres reales con Read antes de usarlos).
**Punto de commit:** Al cerrar la fase F1 (fin de esta tanda).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-50 | Existe un único registro de accesos; `NAV_PROYECTO`, `herramientasPorGrupo`, `CHIPS_ACCESO_RAPIDO`, `hrefItemPanel` y las rutas fijas del panel izquierdo derivan de él: no queda ninguna lista paralela de chips | Búsqueda de código (`rg`) + diff |
| PL-52 | Migración completa: los 41 ítems de `NAV_PROYECTO`, los 10 chips de Mi entorno, los 7 de Accesos rápidos y los 4 de Recursos de empresa que se conservan (Personal, Cargos, Equipos y Causas CNC; "Materiales" se elimina y no se migra) están en el registro; tabla clave anterior → id nuevo sin pérdidas; las únicas diferencias visibles son las declaradas (por ejemplo la unión de `rdt` y `subir-rdt`, y E3 según la respuesta de Victor) | Tabla de mapeo + prueba de equivalencia |

## Entregable sin ID: prueba de equivalencia
Compara lo que derivan Mi entorno y el panel derecho contra la línea base de F0-B (LB-03). Las **únicas** diferencias visibles permitidas: la unión de `rdt` y `subir-rdt` y E3 (recomendación vigente: «Status de RDTs» = `/rdts/status` en todos los paneles y «Archivo de RDTs subidos» = `/rdts/listado`; hoy el chip `listado-rdts` de Mi entorno va a `/rdts/listado`). Entrega la tabla clave anterior → id nuevo, sin pérdidas.

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- `herramientasPorGrupo(tituloGrupo, proyectoId, roles)` (`src/lib/notificaciones/grupo-proceso.ts` ~143) devuelve `HerramientaEntorno {clave, etiqueta, href?, accion?, habilitado, tituloDeshabilitado?}` (~27): 10 chips (`enviar-notificacion`, `crear-requerimiento-servicios`, `status-requerimiento`, `consolidado-rq`, `cronograma`, `plan-maestro`, `listado-rdts`, `consolidado-rdts`, `crear-rdt`, `subir-rdt`), el **mismo conjunto en los 8 grupos** (A3: no se agregan chips a Mi entorno). Consumido por `EntornoTrabajoGrupo.tsx` (`ChipHerramienta` ~48, `EntornoTrabajoGrupo` ~103) y probado en `grupo-proceso.test.ts`.
- `CHIPS_ACCESO_RAPIDO` (7) lo consume `AccesosRapidos` (`PanelSecciones.tsx` ~26); `GruposAccordion` (~77) consume los grupos.
- Rutas fijas del panel izquierdo: `RUTA_PERSONAL`, `RUTA_CARGOS`, `RUTA_EQUIPOS`, `RUTA_CAUSAS_CNC` (`WorkspaceShell.tsx` ~36-39; bloque Recursos ~162-203). Solo se **declaran** en el registro (4 accesos que se conservan; «Materiales» no se migra). El panel izquierdo se rehace en F3: aquí no cambia lo que se ve.
- **PL-50:** al terminar, `Grep` no debe encontrar listas paralelas de chips (`NAV_PROYECTO`, `herramientasPorGrupo`, `CHIPS_ACCESO_RAPIDO`, `hrefItemPanel` y rutas fijas derivan del registro).
- **PL-52:** migración completa: 41 ítems de `NAV_PROYECTO`, 10 de Mi entorno, 7 de Accesos rápidos y 4 de Recursos de empresa. Actualiza `nav-proyecto.test.ts`, `grupo-proceso.test.ts` (contadores congelados: R12).
- En F1 el `permiso` de cada acceso es la función de `permisos.ts` vigente: no cambia quién puede.

## Qué NO hacer

- No cambies permisos ni el aspecto del panel izquierdo. No envíes aún `?proyectoId=` a más chips (F2-A).
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
