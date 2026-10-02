# 11 — Dashboard
> Lee si: la tarea toca el Dashboard: sus dos versiones, ubicación, filtros, indicadores, diagnóstico o la paleta de series compartida con la Curva S.


Vista ejecutiva derivada del PR. No calcula: lee. Si un número está mal, se
arregla en el pipeline (PR / motor RDT → PR), nunca en la pantalla. Esto es
lo que garantiza que Dashboard, PR y Curva S digan siempre lo mismo.

## Los dos Dashboards

`proyectos.tipo_dashboard` (`'PARCIAL'` | `'COMPLETO'`, `db/008_dashboard.sql`)
decide cuál se muestra. Es el mismo esqueleto, y el Completo agrega bloques
al final — quien conoce el Parcial no tiene que reaprender el Completo. Desde
el 2026-10-02 (plan dashboard-economia-y-curva-s) el Parcial **no tiene ningún
dato económico**: todo lo monetario vive en el Completo.

| | Parcial | Completo |
|---|---|---|
| Filtros (fecha de corte y orden de la matriz) | ✓ | ✓ |
| KPI de avance físico (%) | ✓ | ✓ |
| KPI de dinero (BAC, PV, EV, AC, SV, CV, SPI, CPI, EAC, VAC) | — | ✓ |
| Gráficos de dinero (composición del costo, desempeño por partida) | — | ✓ |
| Matriz de partidas (sin columnas de costo) | ✓ | ✓ |
| Panel de diagnóstico | ✓ | ✓ |
| **Bloque E** (PPC + Pareto de CNC) | ✓ | ✓ |
| **Enlace a la Curva S** | ✓ | ✓ |
| Resumen ejecutivo y chip semáforo (derivan de SPI/CPI) | — | ✓ |
| Bloque **«Costo real de recursos»** | — | ✓ |

**El interruptor Parcial/Completo es funcional**: lo activan los roles que pueden
ver datos económicos según la matriz aprobada (`puedeVerEconomia`; tabla 1 del
[flujo 14](14-accesos-y-restricciones.md)) — decisión de Victor, 2026-09-29. Cambia
sin recargar a mano ni dejar la pantalla en un estado intermedio
(`router.refresh()`) y no crea un permiso nuevo. El interruptor se ve en los dos
modos para todos los roles: quien tiene economía alterna; quien no la tiene lo ve
**deshabilitado con título** y queda **fijo en Parcial** (D3, 2026-10-02). El
servidor fuerza Parcial para el rol sin economía aunque `tipo_dashboard` esté en
`COMPLETO` (solo respeta la BD para quien tiene economía). `puedeAdjudicarProyecto`
ya no rige el interruptor.

**La Curva S no vive en ningún Dashboard.** Tiene pantalla propia
(`(workspace)/proyectos/[id]/curva-s`) y chip propio (ubicación por panel
abajo). El Parcial y el Completo la **enlazan**, nunca la embeben; desde el
Parcial el enlace abre `?modo=fisica` para quien no tiene economía (D4).

## Ubicación en la app

`(workspace)/proyectos/[id]/dashboard` — dentro del shell (`WorkspaceShell`),
mismo nav izquierda / panel derecho que el resto de pantallas de un
servicio.

El chip **Dashboard** se declara una sola vez en el registro único de accesos
(`registro-accesos.ts`, flujo 16), en la cadena de control
`… → DP → PR → Dashboard → Curva S`, y se ubica distinto según el panel:

- **Panel izquierdo** (con un servicio abierto): grupo **Reportes**.
- **Panel derecho:** grupo **Planificación**.
- **Mi entorno:** no aparece (no es uno de sus diez chips, flujo 03).

Lo ven habilitado los **13 roles** (`puedeVerDashboard`, 2026-10-02): la pantalla
se abre en Parcial, sin datos económicos; el Completo (dinero) requiere datos
económicos (`puedeVerEconomia`, flujo 16). Requiere un servicio elegido.
Además, el alcance por OT es requisito de partida (flujo 14, tabla 1).

## Filtros (scopean todo lo de abajo)

Una sola fila, arriba, fuera de las tarjetas:

- **Fecha de corte**: presets (`Hoy`, `Ayer`, `Hace 7 días`, `Fecha
  personalizada`) antes que calendario. Recalcula PV al corte, SV y SPI de
  todo el Dashboard contra la misma fecha.
- **Orden de la matriz de partidas**: por WBS (orden contractual, default),
  mayor desviación de costo primero, o sobre-ejecutadas primero. **En el
  Parcial, «mayor desviación de costo» no aplica** (es dinero derivado): el
  servidor fuerza el orden a WBS aunque la URL traiga otro, y la matriz llega
  en orden contractual (RB5, 2026-10-02).

Ambos viven en la URL (`?corte=…&fecha=…&orden=…`); mientras recargan, el
contenido anterior se mantiene atenuado (sin esqueleto ni salto de layout).

## Indicadores

Se separan por modo: el **Parcial** muestra solo lo físico/operativo; el
**Completo** agrega todo lo económico. Los KPI de dinero van en **USD, costo
directo** — el BAC no es el monto total del contrato y la interfaz lo dice.
Fuente: `src/lib/pr/evm.ts` (leído, nunca recalculado por el Dashboard — es
el mismo motor que usa la pantalla PR, por eso los dos siempre coinciden).

- **Parcial:** % avance físico.
- **Completo:** además, BAC, PV al corte, EV, AC, SV, CV, SPI, CPI, EAC y VAC.
- **Sin Plan Maestro aprobado**: PV, SV y SPI muestran **"Pendiente"**,
  nunca 0 ni un número inventado.
- **PPC (Percent Plan Complete)**, en ambos modos: indicador **LPS**,
  no EVM. Se muestra con nombre, fórmula y unidad, **separado y rotulado
  aparte de SPI** — miden cosas diferentes y no se mezclan (flujo 18).
- **Pareto de CNC**, en ambos modos: causas de no cumplimiento de
  `rdt_actividades.cnc_causa_id` contra `catalogo_cnc` (`db/054`), de
  actividades de partes **VALIDADO**. Ordenado por frecuencia, con
  agrupación "Otras" para la cola larga.

**Ningún dato monetario en el Parcial (lista cerrada, PD5).** Además de los
KPI de arriba, el Parcial oculta la cabecera «Costo directo (US$)», el resumen
ejecutivo (imprime SPI/CPI), el chip semáforo (deriva de CPI), la dona
«Composición del costo», el gráfico «Desempeño por partida», las columnas
PV/EV/AC/SPI/CPI de la matriz de partidas y la opción de orden «mayor desviación
de costo». **Conserva** filtros, % avance físico, matriz de partidas sin costo,
panel de diagnóstico, Bloque E (PPC/Pareto) y el enlace a la Curva S.

## Costo real de recursos (solo Completo)

Bloque propio del Dashboard Completo (D2, 2026-10-02): desagrega el AC real por
recurso para ver su incidencia. El dato se lee del PR; el Dashboard no recalcula.

- **Filas:** `pr_recursos` de tipo **MO (personal, HH)** y **HM (equipos)**, con
  su `descripcion` y su costo acumulado.
- **Total = AC** del PR (la misma fuente que el KPI AC), nunca una suma paralela.
- **Fila «Sin resolver»** = `AC − Σ filas`, visible **solo** cuando la diferencia
  es distinta de cero; explica las filas sin partida vinculada (deuda de
  `db/055`). No se fuerza a cero ni se inventa dato.
- El balde `costo_legacy_sin_partida_acum` es una **nota informativa, nunca una
  fila sumable**: ya está dentro de las filas de recursos y sumarlo duplicaría.
- **Materiales y subcontratos no entran** (regla 5: se miden por % de avance
  económico, no por costo capturado); **las HH de MOI no se valorizan** (regla 10).
- **Vista solo por recurso**, no por partida.

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

**Color del avance real.** Cuando una pantalla pinta el avance físico real (hoy, el «Físico acum. (%)» de las filas «Real» del lienzo del Plan Maestro, flujos 18 y 20), usa los mismos colores de estado: 0 % sin color (blanco), en curso amarillo (`amber`) y 100 % verde (`emerald`, con la marca ✓ para no depender solo del color). **Solo el avance real lleva color; lo programado nunca.** Es un color de estado, no una serie: no cambia la paleta de PV, AC y EV de arriba.

## Resumen ejecutivo breve

Califica **plazo y costo por separado** (SPI y CPI, cada uno con su propio umbral) — nunca con una sola palabra derivada del semáforo (que es CPI+IP por diseño, sin SPI a propósito). Un CPI muy favorable puede convivir con un SPI de atraso real (ej. AC casi en cero porque el RDT real todavía no se capturó del todo); calificar con el semáforo en ese caso produce una frase contradictoria con el propio SPI impreso al lado. Implementado en `construirResumenEjecutivoBreve` (`src/lib/dashboard/dashboard.ts`).

## Qué no hace el Dashboard

- No recalcula nada: lee el PR.
- No administra el catálogo CNC (eso vive en Recursos → Causas CNC).
- No dibuja la Curva S ni ninguna serie temporal.
- No modifica `evm.ts` ni el motor de RDT → PR.
