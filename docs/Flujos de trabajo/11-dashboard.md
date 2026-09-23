# 11 — Dashboard

Vista ejecutiva derivada del PR. No calcula: lee. Si un número está mal, se
arregla en el pipeline (PR / motor RDT → PR), nunca en la pantalla. Esto es
lo que garantiza que Dashboard, PR y Curva S digan siempre lo mismo.

Construido en dos fases:

- **PR #6** (2026-08-17, spec `2026-08-16-dashboard-parcial-design.md`):
  Dashboard Parcial, sobre un diseño aprobado en Excel.
- **Dashboard Fase 3** (Agente C, plan
  `2026-09-21-dashboard-fase-3-agente-c.md`): interfaz rehecha dentro del
  shell de la app, y construcción del Dashboard Completo (antes solo
  mostraba un aviso).

## Los dos Dashboards

`proyectos.tipo_dashboard` (`'PARCIAL'` | `'COMPLETO'`, `db/008_dashboard.sql`)
decide cuál se muestra. Es el mismo esqueleto, y el Completo agrega bloques
al final — quien conoce el Parcial no tiene que reaprender el Completo.

| | Parcial | Completo |
|---|---|---|
| Filtros | ✓ | ✓ |
| KPI (BAC, PV, EV, AC, SPI, CPI, % avance físico) | ✓ | ✓ |
| Gráficos (composición del costo, desempeño por partida) | ✓ | ✓ |
| Matriz de partidas | ✓ | ✓ |
| Panel de diagnóstico | ✓ | ✓ |
| **Bloque E** (PPC + Pareto de CNC) | — | ✓ |
| **Enlace a la Curva S** | — | ✓ |
| Resumen ejecutivo (2 líneas, al final) | ✓ | ✓ |

**El toggle es funcional** (Fase 3): se edita con el mismo permiso que ya
edita el proyecto (`puedeAdjudicarProyecto`), cambia sin recargar a mano ni
dejar la pantalla en un estado intermedio (`router.refresh()`), y no crea
un permiso nuevo.

**La Curva S no vive en ningún Dashboard.** Tiene pantalla propia
(`(workspace)/proyectos/[id]/curva-s`, Agente D) y chip propio en el grupo
Planificación. El Completo solo la **enlaza**, nunca la embebe.

## Ubicación en la app

`(workspace)/proyectos/[id]/dashboard` — dentro del shell (`WorkspaceShell`),
mismo nav izquierda / panel derecho que el resto de pantallas de un
servicio. Antes de la Fase 3 vivía fuera del route group `(workspace)` y se
veía "suelto"; moverlo no cambió la URL.

El chip **Dashboard** vive en el grupo **Planificación** (`nav-proyecto.ts`),
en la cadena de control: `… → DP → PR → Dashboard → Curva S`. Aparece en
los tres paneles (derecho, Mi entorno, e izquierda con un servicio abierto),
desde una única definición.

## Filtros (scopean todo lo de abajo)

Una sola fila, arriba, fuera de las tarjetas:

- **Fecha de corte**: presets (`Hoy`, `Ayer`, `Hace 7 días`, `Fecha
  personalizada`) antes que calendario. Recalcula PV al corte, SV y SPI de
  todo el Dashboard contra la misma fecha.
- **Orden de la matriz de partidas**: por WBS (orden contractual, default),
  mayor desviación de costo primero, o sobre-ejecutadas primero.

Ambos viven en la URL (`?corte=…&fecha=…&orden=…`); mientras recargan, el
contenido anterior se mantiene atenuado (sin esqueleto ni salto de layout).

## Indicadores

Todo en **USD, costo directo** — el BAC no es el monto total del contrato y
la interfaz lo dice. Fuente: `src/lib/pr/evm.ts` (leído, nunca recalculado
por el Dashboard — es el mismo motor que usa la pantalla PR, por eso los
dos siempre coinciden).

- **BAC, PV al corte, EV, AC, SV, CV, SPI, CPI, EAC, VAC, % avance físico.**
- **Sin Plan Maestro aprobado**: PV, SV y SPI muestran **"Pendiente"**,
  nunca 0 ni un número inventado.
- **PPC (Percent Plan Complete)**, solo en el Completo: indicador **LPS**,
  no EVM. Se muestra con nombre, fórmula y unidad, **separado y rotulado
  aparte de SPI** — miden cosas diferentes y no se mezclan (flujo 18).
- **Pareto de CNC**, solo en el Completo: causas de no cumplimiento de
  `rdt_actividades.cnc_causa_id` contra `catalogo_cnc` (`db/054`), de
  actividades de partes **VALIDADO**. Ordenado por frecuencia, con
  agrupación "Otras" para la cola larga.

## Diagnóstico

Cuatro puntos, tomados de datos que ya existen en el PR:

- Partidas sobre-ejecutadas (metrado restante negativo).
- Partidas sin actividad registrada.
- Recursos sin tarifa (`proyecto_pr.recursos_sin_tarifa`), con camino a
  Recursos → Personal / Equipos para corregirlo.
- HH de MOI acumuladas — horas, **nunca valorizadas** (regla 10).

## Paleta de series (compartida con la Curva S)

Mapeo canónico y fijo, tokens en `globals.css`:

| Serie | Token | Hex |
|---|---|---|
| PV / planificado | `--color-serie-pv` | `#3987e5` (azul) |
| AC / costo real | `--color-serie-ac` | `#d95926` (naranja) |
| EV / valor ganado | `--color-serie-ev` | `#199e70` (aqua) |

Una vez asignado, nunca se reasigna ni se cicla. Los colores de estado
(`emerald`/`rose`/`amber`, design.md §4.1.1) son para semáforo y
validación — no se reutilizan como color de serie.

## Resumen ejecutivo breve

Califica **plazo y costo por separado** (SPI y CPI, cada uno con su propio umbral) — nunca con una sola palabra derivada del semáforo (que es CPI+IP por diseño, sin SPI a propósito). Un CPI muy favorable puede convivir con un SPI de atraso real (ej. AC casi en cero porque el RDT real todavía no se capturó del todo); calificar con el semáforo en ese caso produce una frase contradictoria con el propio SPI impreso al lado. Implementado en `construirResumenEjecutivoBreve` (`src/lib/dashboard/dashboard.ts`).

## Qué no hace el Dashboard

- No recalcula nada: lee el PR.
- No administra el catálogo CNC (eso vive en Recursos → Causas CNC).
- No dibuja la Curva S ni ninguna serie temporal.
- No modifica `evm.ts` ni el motor de RDT → PR.
