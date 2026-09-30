# F4-C · RDT: pantalla de Crear RDT, consolidado y status

Lee primero `00-reglas-de-contexto.md`. Carril **4 · RDT** · rama `local-worker-4`, puerto 3114.
Fase F4 · **Depende de:** F4-B cerrada **y de la maqueta aprobada por Victor**: `mockups/crear-rdt-selector-paquetes.html` (F0-B). Sin maqueta aprobada, no empieces.
**Punto de commit:** al cerrar la tanda, en `local-worker-4`.

## Ítems (estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| F4C-1 | El selector de actividad de **Crear RDT** lista los **paquetes (plegables) y sus partidas** del Plan Maestro, más las **partidas directas** aparte; elegir una rellena descripción, WBS y unidad y fija el tipo D, como hoy | Lógica en módulo puro con prueba; build |
| F4C-2 | **Modo «por avance del paquete»** en la pantalla: se escribe la unidad de la guía y las demás partidas aparecen calculadas, en solo lectura | Prueba de la lógica + build |
| F4C-3 | Actividades **C/NC** y **materiales** usan el mismo selector para elegir el paquete × partida al que cargan | Prueba |
| F4C-4 | **Status** y **Consolidado RDTs** muestran el paquete y permiten filtrarlo, sin perder los filtros actuales ni el aspecto con servicios sin paquetes | Prueba de la lógica de filtros + build |
| F4C-5 | Estados **vacío, carga y error**, móvil (390 px), accesibilidad y el mensaje **«sin Plan Maestro aprobado»** (no se puede crear RDT); `npx tsc --noEmit`, suite, lint comparado con `main` y `next build --webpack` | Salida de comandos |

## Contrato técnico verificado (2026-09-30, `45c9e0a`)

- Pantalla actual: `src/components/ui/FormularioCrearRdt.tsx` (elegir partida por WBS ~326-354; `agruparPorSubpresupuesto(catalogos.partidas, catalogos.subpresupuestos)` ~484; desplegable de partida con texto cortado, pedido de Victor del 13-sep: se conserva). Páginas: `src/app/(workspace)/rdts/crear/page.tsx`, `rdts/status`, `rdts/consolidado`; tablas `TablaStatusRdts.tsx`, `TablaConsolidadoRdts.tsx`.
- Catálogo nuevo de C5 (`lineasPlanMaestro`, `estadoPlanMaestro`). **No importes `src/lib/niveles/`** hasta la integración: la jerarquía entra por `NodoEstructura` (C1) o por el agrupador por paquete.
- Permisos de la pantalla: sin cambios (flujo 06/14). Las pantallas reciben el servicio con `?proyectoId=` y lo preseleccionan (ya implementado).
- Interfaz: `design.md` §5 (selects y tablas), §8, §9, §10 y la maqueta aprobada; no inventes componentes.
- Sin navegador en esta tanda: lo que lo exija queda `Observado — pendiente de F5`.

## Qué NO hacer

- No edites `api/rdts/**` de tandas anteriores salvo lo que el brief pida (la API ya está en F4-B). No edites archivos de otros carriles ni congelados. No cambies permisos. No apliques migraciones. Sin push.
- Ante contradicción con un flujo o con la maqueta: detente y devuelve la pregunta.

## Cierre

`resultados/F4-C.md` (estado de F4C-1 a F4C-5, handoff, comprobaciones para F5, llamadas). Commit en `local-worker-4`, `git add` explícito.
