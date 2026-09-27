# 21 — Curva S

## Objetivo

Mostrar la evolución acumulada de PV, EV y AC a lo largo del tiempo, en una
pantalla propia con su propio chip. Responde:

```text
¿Cómo va el servicio en el tiempo — lo planificado contra lo realmente
ejecutado y lo realmente gastado — y en qué momento se separaron?
```

No es una tabla de snapshots históricos ni un cálculo aparte del PR: es la
misma cuenta que hace el PR (`pr_partidas.costo_real_acum`,
`pr_partidas.metrado_acumulado`), cortada en cada fecha en vez de colapsada
a un único total. No reemplaza el PR, el Dashboard ni `evm.ts` — los
reutiliza.

## Por qué existe pantalla propia (y no es el Bloque G del Dashboard)

El spec original del Dashboard Completo (`2026-08-16-dashboard-parcial-design.md`
§2, Fase 3 previa a esta) reservaba la Curva S como su **Bloque G**, fuera de
alcance por dos razones que ya cayeron:

1. Dependía del RDT, que en agosto "no capturaba nada" — el RDT ya alimenta
   el PR desde [PR Fase 1 y 2](../Tareas%20de%20implementacion/2026-09-21-pr-fase-1-pipeline-rdt.md).
2. Se creía que hacía falta una tabla de snapshots semanales, equivalente al
   `HISTORIAL` del Excel. **Ese supuesto quedó obsoleto**: el dato diario ya
   existe en las tablas de origen (Plan Maestro y RDT validado); no hace
   falta materializar ningún histórico aparte — se agrega por fecha al leer.

Por decisión de Victor (2026-09-21), la Curva S **salió del Dashboard
Completo a pantalla propia con chip propio**, porque dentro del Dashboard no
le alcanza el espacio. El Dashboard Completo (flujo 11, Agente C) la
**enlaza**, no la dibuja.

## Fuentes de verdad

| Serie | De dónde sale el dato diario |
|---|---|
| **PV** (valor planificado) | `plan_maestro_asignaciones.metrado_planificado × plan_maestro_partidas.precio_unitario`, del Plan Maestro con `estado = 'APROBADO'`, por día |
| **EV** (valor ganado) | `rdt_actividades.metrado_ejecutado` (solo `ta = 'D'`) × `dp_partidas.precio_unitario`, vía `rdt_actividad_partidas`, de partes con `estado_validacion = 'VALIDADO'` y su `fecha_lima` |
| **AC** (costo real) | `rdt_tareo_horas.horas × rdt_tareo.tarifa_hh` (excluyendo MOI, regla 10) + `rdt_equipos_parte.horas × tarifa_hm`, de los mismos partes validados y su `fecha_lima` — tarifa congelada al validar (EVM Fase 1) |

Función SQL: `curva_s_proyecto(proyecto_id, desde, hasta)` (`db/070_curva_s_serie.sql`),
que agrega por fecha en una sola pasada (no una subconsulta por día) y
acumula con función de ventana — necesario para que la pantalla no se
vuelva cuadrática con proyectos grandes.

**AC no filtra por partida vinculada, a propósito**: suma todas las horas
(no-MOI) de partes validados, tengan o no vínculo a una partida vigente del
DP — así el total cuadra exacto con el AC del PR
(`Σ pr_partidas.costo_real_acum + proyecto_pr.costo_legacy_sin_partida_acum`)
sin sumar el balde legacy aparte. El EV sí exige el vínculo, porque sin él
no hay con qué partida calcular metrado × precio.

## Reglas fijas (Victor)

1. Pantalla propia con chip propio (`/proyectos/{id}/curva-s`, grupo
   Planificación) — no una sección del Dashboard.
2. Todo en USD, rotulado como costo directo (reglas 9 y 11 de PR Fase 2).
3. **Sin Plan Maestro aprobado no hay PV** — la pantalla lo dice
   explícitamente y no dibuja una curva de PV inventada (patrón "Pendiente"
   ya usado en PR/Dashboard).
4. Sin dependencias nuevas de gráficos: el gráfico es SVG a mano, igual
   criterio que la dona del Dashboard.
5. El AC cubre solo HH y HM con tarifa congelada (regla 1 de EVM) —
   materiales y subcontratos se miden por % de avance económico (regla 5),
   nunca por costo capturado; la pantalla lo dice en una nota fija.
6. Las HH de MOI no se valorizan (regla 10) — no entran al AC.
7. **La curva real (EV/AC) nunca se dibuja más allá de la fecha de corte.**
   El PV sí sigue hasta el fin del Plan Maestro aprobado. El hueco entre
   ambos es la lectura central del gráfico — extenderlos con ceros o una
   línea plana sería una lectura falsa.
8. El EV histórico se recalcula con el BAC vigente hoy (`pr_partidas.bac`,
   `metrado_contractual × precio_unitario` del DP actual). Si el DP se
   reimportó, la curva pasada se recalcula con la base nueva — es
   consistente con que solo existe una línea base vigente a la vez (mismo
   criterio que el PR), no un histórico de BAC por fecha.

## Granularidad

La serie se calcula día a día. La pantalla la agrupa por semana (sábado a
viernes, mismo criterio que el Plan Maestro — `generarSemanasPlanMaestro`,
flujo 20 §4) por defecto; la vista diaria queda disponible para el detalle.
El punto de cada semana es el acumulado a su día de cierre (viernes), o al
último dato real si la semana todavía está en curso.

## Endpoint

`GET /api/curva-s?proyectoId=...&desde=...&hasta=...` — validación en
servidor: rol (todos menos asistente, igual que PR/Plan Maestro) y alcance
sobre la OT (`validarEscrituraProyecto`, con bypass de administrador). Sin
`desde`/`hasta`, el servidor calcula "todo el servicio" a partir de los
datos reales (mínimo entre el primer día del Plan Maestro aprobado y el
primer RDT validado; máximo entre el fin del Plan Maestro y la fecha de
corte, para que el PV siempre llegue hasta el fin del plan aunque el rango
visible sea más corto).

## El gráfico

SVG a mano, un solo eje Y (los tres son dinero acumulado). Leyenda siempre
presente + etiqueta directa al final de cada línea (identidad nunca solo
por color). Línea de corte vertical punteada con etiqueta. Crosshair que
sigue al puntero y se ancla a la fecha más cercana, con un único tooltip
que muestra las tres series a la vez — operable también con teclado
(flechas izquierda/derecha, Home/End), mismo detalle que el hover. Paleta
fija: PV `#3987e5` (azul), EV `#199e70` (aqua), AC `#d95926` (naranja) —
compartida con el Dashboard, nunca se reasigna.

## Lectura del punto

Al seleccionar una fecha: PV, EV, AC, SV, CV, SPI y CPI a esa fecha,
reutilizando las fórmulas de `dashboard.ts` (las mismas que usa `evm.ts`,
nunca reimplementadas). PPC no aparece acá — mide algo distinto (flujo 18)
y no se mezcla con SPI.

## Fuera de alcance de esta fase

- Proyección / EAC dibujado hacia el futuro sobre la curva real.
- Pareto de CNC, cierre semanal auditado y 3WLA.
- El motor de RDT → PR y la pantalla del PR (`src/lib/pr/evm.ts` se importa,
  nunca se modifica).

## Archivos

| Qué | Dónde |
|---|---|
| Función SQL | `db/070_curva_s_serie.sql` |
| Lógica pura (recorte al corte, agrupación semanal, lectura del punto) | `src/lib/curva-s/curva-s.ts` (+ `curva-s.test.ts`) |
| Endpoint | `src/app/api/curva-s/route.ts` |
| Pantalla | `src/app/(workspace)/proyectos/[id]/curva-s/page.tsx` |
| Componentes | `src/components/curva-s/PantallaCurvaS.tsx`, `GraficoCurvaS.tsx` |
| Ítem de navegación | `src/lib/config/nav-proyecto.ts` (clave `curva-s`, grupo Planificación) |

Ver [2026-09-21-curva-s-fase-3-agente-d.md](../Tareas%20de%20implementacion/2026-09-21-curva-s-fase-3-agente-d.md)
para el detalle de implementación, la Punch List verificada y el cuadre
documentado contra el PR.
