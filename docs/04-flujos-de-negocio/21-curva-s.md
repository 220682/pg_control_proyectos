# 21 — Curva S
> Lee si: la tarea toca la Curva S: sus reglas fijas, granularidad, endpoint, o por qué tiene pantalla propia y no es el Bloque G del Dashboard.


## Objetivo

Mostrar la evolución acumulada de PV, EV y AC a lo largo del tiempo, en una
pantalla propia con su propio chip y con **dos modos**: **económico** (PV/EV/AC
en USD) y **avance físico** (%: PV/BAC y EV/BAC). Responde:

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
   el PR desde [PR Fase 1 y 2](../02-trabajo-activo/01-planes/2026-09-21-pr-fase-1-pipeline-rdt.md).
2. Se creía que hacía falta una tabla de snapshots semanales, equivalente al
   `HISTORIAL` del Excel. **Ese supuesto quedó obsoleto**: el dato diario ya
   existe en las tablas de origen (Plan Maestro y RDT validado); no hace
   falta materializar ningún histórico aparte — se agrega por fecha al leer.

Por decisión de Victor (2026-09-21), la Curva S **salió del Dashboard
Completo a pantalla propia con chip propio**, porque dentro del Dashboard no
le alcanza el espacio. El Dashboard Completo (flujo 11) la
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

**Sin cambio de fórmulas por el plan niveles-paquetes-plan-maestro-rdt.** Una partida puede repetirse en el Plan Maestro (repartida en varios paquetes y/o directa): `curva_s_proyecto` y el PV **suman todas las líneas de la partida**, y el vínculo del RDT lleva el paquete **sin afectar el EV** (que sigue siendo metrado × `dp_partidas.precio_unitario` por partida).

**AC no filtra por partida vinculada, a propósito**: suma todas las horas
(no-MOI) de partes validados, tengan o no vínculo a una partida vigente del
DP — así el total cuadra exacto con el AC del PR
(`Σ pr_partidas.costo_real_acum + proyecto_pr.costo_legacy_sin_partida_acum`)
sin sumar el balde legacy aparte. El EV sí exige el vínculo, porque sin él
no hay con qué partida calcular metrado × precio.

**BAC del modo físico.** El % de avance físico divide PV y EV entre el BAC
vigente = **`Σ pr_partidas.bac`** (misma base que el PR, §8). Se lee en el
servidor y **no se devuelve** en la respuesta de `modo=fisica` (contrato PD2,
V02): el cuerpo físico solo lleva series en % y la brecha en puntos
porcentuales, sin montos USD.

## Reglas fijas (Victor)

1. Pantalla propia con chip propio (`/proyectos/{id}/curva-s`) — no una
   sección del Dashboard. El chip se declara una sola vez en el registro
   único de accesos (flujo 16) y se ubica por panel: **Reportes** en el
   panel izquierdo (con servicio abierto) y **Planificación** en el derecho;
   no está en Mi entorno (flujo 03). Lo ven habilitado los **13 roles**
   (`puedeVerCurvaS`, 2026-10-02); dentro de la pantalla, el selector muestra
   «Económica (USD)» **deshabilitada con título** a quienes no tienen economía
   (flujo 16).
2. **Dos modos con un selector** (D1/PD4, 2026-10-02):
   - **Económica (USD):** PV/EV/AC acumulados, rotulados como costo directo
     (reglas 9 y 11 de PR Fase 2). Solo los 5 roles con economía.
   - **Avance físico (%):** planificado = **PV/BAC** y real = **EV/BAC**, con
     la misma regla de «% avance físico» de `control_de_proyectos.txt` §2.1
     (ponderación interna por dinero, salida en %; nunca promedio simple de
     metrados). Los 13 roles; **nunca expone montos**.
   El rol ve las dos opciones; la que no le corresponde queda deshabilitada
   con título (patrón "ver no es acceder", flujo 16).
3. **Sin Plan Maestro aprobado no hay PV** (en los dos modos) — la pantalla lo
   dice explícitamente («Pendiente») y no dibuja una curva de PV inventada
   (patrón "Pendiente" ya usado en PR/Dashboard).
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
9. **El modo físico lee el BAC del servidor** (`Σ pr_partidas.bac`, §8) para
   calcular PV/BAC y EV/BAC, y **no lo devuelve** en la respuesta de
   `modo=fisica`: el cuerpo físico no expone USD (contrato PD2/V02).
10. **Sin BAC no hay serie física:** con `BAC = 0` la pantalla muestra «Este
    servicio no tiene BAC…» y no dibuja gráfico. Es distinto del servicio
    **sin RDT validados**: allí hay BAC (>0) pero todas las EV del rango son
    0, la serie real (EV/BAC) queda vacía con su nota y la tabla muestra «—»
    en real (aclaración de E01; la línea EV no se dibuja).

## Granularidad

La serie se calcula día a día. La pantalla la agrupa por semana (sábado a
viernes, mismo criterio que el Plan Maestro — `generarSemanasPlanMaestro`,
flujo 20 §4) por defecto; la vista diaria queda disponible para el detalle.
El punto de cada semana es el acumulado a su día de cierre (viernes), o al
último dato real si la semana todavía está en curso.

## Endpoint

`GET /api/curva-s?proyectoId=...&desde=...&hasta=...&modo=economica|fisica` —
validación en servidor:

- **Rol:** la pantalla la ve cualquier rol con `puedeVerCurvaS` (los 13); el
  **modo económico** exige `puedeVerCurvaSEconomica` = `puedeVerEconomia`
  (administrador, jefe de proyectos, jefe de oficina técnica, supervisor de
  costos y jefe de costos) y responde **403** si se fuerza sin permiso
  (criterio 6).
- **Modo:** sin `modo` el servidor lo deriva por permiso (`economica` si tiene
  economía; si no, `fisica`), de forma determinista; un `modo` inválido
  responde 400. La respuesta de `modo=fisica` **no incluye** montos USD ni
  `bac` (PD2/V02).
- **Alcance:** sobre la OT (`validarEscrituraProyecto`, con bypass de
  administrador). Sin `desde`/`hasta`, el servidor calcula "todo el servicio" a
  partir de los datos reales (mínimo entre el primer día del Plan Maestro
  aprobado y el primer RDT validado; máximo entre el fin del Plan Maestro y la
  fecha de corte, para que el PV siempre llegue hasta el fin del plan aunque el
  rango visible sea más corto).

## El gráfico

SVG a mano. **Un solo eje Y por modo, con su unidad rotulada** — nunca % y USD
en el mismo eje: en económico, «US$ acumulado (CD)» con PV/EV/AC; en físico,
«Avance físico (%)» con PV/BAC y EV/BAC (sin AC). Leyenda siempre
presente + etiqueta directa al final de cada línea (identidad nunca solo
por color). Línea de corte vertical punteada con etiqueta. Crosshair que
sigue al puntero y se ancla a la fecha más cercana, con un único tooltip
que muestra las series del modo a la vez — operable también con teclado
(flechas izquierda/derecha, Home/End), mismo detalle que el hover. Paleta
fija: PV `#3987e5` (azul), EV `#199e70` (aqua), AC `#d95926` (naranja) —
compartida con el Dashboard, nunca se reasigna.

## Lectura del punto

Al seleccionar una fecha, según el modo:

- **Económico:** PV, EV, AC, SV, CV, SPI y CPI a esa fecha, reutilizando las
  fórmulas de `dashboard.ts` (las mismas que usa `evm.ts`, nunca
  reimplementadas).
- **Físico:** % planificado (PV/BAC), % real (EV/BAC) y la brecha en **puntos
  porcentuales** (pp), sin SV/CV en USD ni montos.

PPC no aparece acá — mide algo distinto (flujo 18)
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
| Acceso (chip) | `src/lib/config/registro-accesos.ts` (id `curva-s`, grupo Planificación; derivado en `nav-proyecto.ts` y `panel-izquierdo.ts`) |
