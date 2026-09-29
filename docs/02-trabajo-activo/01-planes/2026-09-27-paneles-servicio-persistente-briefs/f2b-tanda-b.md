# F2B-B · Descargas de interfaces sin economía y revisión de dinero en pantallas abiertas

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F2B · **Depende de:** F2B-A cerrada.
**Punto de commit:** Al cerrar la fase F2B (fin de esta tanda).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-121 | Las interfaces declaradas sin datos económicos no muestran dinero (USD ni S/: costos, precios, tarifas, valores): revisión de Consolidado RDTs, Paquetes de Trabajo, Status y archivo de RDTs, RQ, Recursos de empresa, ficha del servicio y grilla del portafolio. Si aparece alguno, es un hallazgo que se devuelve a Victor antes de seguir | Revisión de código + capturas |
| PL-152 | Guardias de servidor de las descargas de interfaces sin economía (`rdts/exportar` ZIP y PDF PROM-GP-0006, `rdts/partes/[id]/pdf`, `rdts/[id]/archivo`, `…/requerimientos/exportar` listado PROM-GP-008): cumplen la misma regla que "ver" su interfaz (los 13 roles, supuesto A12) y un usuario sin ningún rol conocido es rechazado; hoy `requerimientos/exportar` no tiene guardia de rol | Respuestas por rol (13 roles) |
| PL-154 | Descargar RDTs (ZIP), listado de RDTs (PDF PROM-GP-0006) y listado RQ (PDF PROM-GP-008): habilitadas para los 13 roles (supuesto A12); el botón y la API coinciden; no se cambian los conjuntos de los demás controles de esas pantallas | Tabla 13 roles + capturas |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- Regla A12 (supuesto vigente, no decisión): las descargas de estas interfaces cumplen la misma regla que «ver» su interfaz (13 roles) y un usuario sin rol conocido es rechazado.
- Rutas (guardia actual, verificada): `src/app/api/rdts/exportar/route.ts` ~87 (`puedeVerRdts`; ZIP y PDF PROM-GP-0006), `rdts/partes/[id]/pdf/route.ts` ~47 (`puedeVerRdts`), `rdts/[id]/archivo/route.ts` ~11 (`puedeVerRdts`), `proyectos/[id]/requerimientos/exportar/route.ts` (**sin guardia de rol**; listado PROM-GP-008 y PDF individual `tipo=detalle`). El botón y la API coinciden; no cambian los conjuntos de los demás controles de esas pantallas.
- **No tocar** (A13, se reportan): `cronograma/plantilla`, `requerimientos/formato-vacio`, `logistica/requerimientos/exportar-004` (`puedeDescargarConsolidadoRq`, F5C), `registro-costos` y `dp/exportar` (F5B/F5C).
- **PL-121:** revisa que estas pantallas no muestran dinero (USD ni S/: costos, precios, tarifas, valores): `TablaConsolidadoRdts`, `FormularioPaquetesTrabajo`, `TablaStatusRdts`, `TablaListadoRdts`, `ListadoRequerimientos`, `TablaConsolidadoRq`, `TablaRecursos`, `TablaPersonal`, ficha `proyectos/[id]/page.tsx` y `GrillaProyectosReales.tsx` (Grep de `precio|costo|tarifa|USD|S/|valor` y revisión). **Si aparece dinero, no lo edites: es un hallazgo que se devuelve a Victor por el Orquestador antes de seguir** (R25).
- Verificación de códigos por rol: un `browser_evaluate` que recorre los 13 roles con «Ver como» y lee el código de estado (sin descargar el archivo completo).

## Qué NO hacer

- No cambies las descargas de A13 ni las de economía. No edites pantallas por dinero encontrado: repórtalo.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
