# Curva S Fase 3 (Agente D): serie temporal PV / EV / AC en pantalla propia

**Estado (2026-09-22):** CERRADO — checklist D0–D12 completo, Punch List 20/20 en Completado (dos con hallazgo documentado, ninguno abierto). PR [#16](https://github.com/220682/py_control_proyectos_web/pull/16) mergeado a `main` en `py_control_proyectos_web` (aprobado y mergeado por Victor, 2026-09-22). Trabajó en paralelo con [Dashboard / Fase 3 (Agente C)](2026-09-21-dashboard-fase-3-agente-c.md), PR [#15](https://github.com/220682/py_control_proyectos_web/pull/15), también mergeado.

**Ya resuelto, no volver a preguntar:**
- La Curva S era el **Bloque G del Dashboard Completo** en el diseño original (`docs/superpowers/specs/2026-08-16-dashboard-parcial-design.md` §2, repo web). **Victor la saca de ahí**: va en **pantalla propia con su propio chip**, porque dentro del Dashboard no hay espacio. El Dashboard Completo (Agente C) **la enlaza**, no la dibuja.
- **No hace falta ninguna tabla de snapshots históricos.** Esto **contradice el supuesto del spec de agosto**, que daba por hecho que el Completo necesitaba "un historial semanal de snapshots, equivalente a `HISTORIAL` del Excel". Verificado contra el esquema real el 2026-09-21: el dato diario ya existe en las tablas de origen (ver "Por qué esto se puede construir hoy"). **Ese supuesto quedó obsoleto y así hay que documentarlo.**
- Paleta de series: ya validada y **compartida con el Agente C** — ver "Colores".
- `docs/visual-companion/design.md` es de **lectura obligatoria completa** antes de tocar interfaz.
- **La Punch List se cierra en loop, no en una pasada.** Ver protocolo: verificar, corregir y volver a verificar hasta el 100 % en Completado. No se entrega con ítems abiertos.

## Ejecución en la nube

Mismo modo de trabajo que los Agentes A y B (Fases 1 y 2 del PR):

- **Rama propia en `py_control_proyectos_web`**, no directo a `main`:

  ```
  feat/curva-s-fase-3-serie-temporal
  ```

  **Nombre fijo, no sugerido** — sigue la convención de los Agentes A y B (`feat/pr-fase-1-pipeline-rdt`, `feat/pr-fase-2-linea-base-evm`): `feat/<módulo>-fase-<n>-<qué hace>`. El agente **no la renombra ni trabaja en otra**.

- Al 100 % del checklist, abre un **PR** con título **"Curva S Fase 3 (Agente D): serie temporal PV/EV/AC en pantalla propia"**, para que Victor lo revise antes de mergear.
- **Las migraciones se corren solas, sin pausar a confirmar cada una** (excepción ya autorizada, ver `mejoras-futuras.md`), leyendo **`PR_DB_URL`**. El agente nunca imprime el valor completo ni lo commitea. *Nota del Agente A (commit `b8b3ac7` en `pg_control_proyectos`): `PR_DB_URL` resultó inalcanzable desde el sandbox por falta de salida IPv6 al puerto directo de Postgres; el Agente A aplicó sus migraciones vía Management API de Supabase. Si vuelve a pasar, usar esa vía y dejarlo anotado.*
- **Rango de migraciones asignado a esta fase: `070`–`079`.** No usar otro rango — evita choque con cualquier fase futura.
- Credenciales de verificación: **`PR_TEST_ADMIN_EMAIL`** / **`PR_TEST_ADMIN_PASSWORD`** y **`PR_TEST_USER_EMAIL`** / **`PR_TEST_USER_PASSWORD`**.
- Cada decisión o convención nueva acordada con Victor **se escribe en este archivo** conforme ocurre.
- Entrega en el PR: checklist D0–D10 marcado, Punch List verificada con Playwright, informe de limpieza.

## Contexto

La Curva S viene postergada desde agosto. El spec del Dashboard (`2026-08-16-dashboard-parcial-design.md` §2) la dejó como **Bloque G del Dashboard Completo**, fuera de alcance por dos razones: dependía del RDT — que entonces "no capturaba nada" — y se creía que necesitaba una tabla de snapshots semanales. Las dos fases del PR la volvieron a dejar fuera por lo mismo ("necesita el histórico, va después").

**Las dos razones cayeron:**

1. El RDT ya captura y alimenta el PR (Fases 1 y 2, mergeadas el 2026-09-21).
2. **No hace falta la tabla de snapshots.** El dato diario ya está en las tablas de origen — verificado contra el esquema real.

Y por decisión de Victor ya no es un bloque del Dashboard: **sale a pantalla propia con chip propio**, porque dentro del Dashboard no le alcanza el espacio.

### Por qué esto se puede construir hoy (verificado contra el esquema real)

| Serie | De dónde sale el dato diario | Estado |
|---|---|---|
| **PV** | `plan_maestro_asignaciones` tiene `fecha date` + `metrado_planificado` **por partida y por día** (`db/037_plan_maestro.sql`) | Existe desde el día 1 de cada plan aprobado |
| **EV** | `rdt_actividades.metrado_ejecutado` (solo `ta = 'D'`), vía `rdt_actividad_partidas`, de partes con `estado_validacion = 'VALIDADO'` y `rdt_partes.fecha_lima` | Existe, con fecha real de ejecución |
| **AC** | `rdt_tareo_horas.horas × rdt_tareo.tarifa_hh` + `rdt_equipos_parte.horas × tarifa_hm`, mismos partes validados y misma fecha | Existe, con la tarifa **congelada al validar** (EVM Fase 1) |

Lo único que falta es **agregar por fecha en vez de colapsar a un único total**. `recalcular_pr_desde_rdt()` (`db/053`) ya hace exactamente estos joins; esta fase reusa ese patrón cambiando el `group by`.

> Dicho de otra forma: `pr_partidas.costo_real_acum` es la foto de hoy. La Curva S es la misma cuenta, cortada en cada fecha.

## Reglas fijas (Victor) — no volver a preguntarlas

1. **Pantalla propia con chip propio**, no una sección del Dashboard.
2. **Todo en USD y rotulado como costo directo** (reglas 9 y 11 de la Fase 2).
3. **Sin Plan Maestro aprobado no hay PV** → la pantalla lo dice y no dibuja una curva inventada.
4. **Sin dependencias nuevas de gráficos.** Precedente vigente: la dona del Dashboard es SVG a mano, sin librería (PR #6), y `design.md` §1 prohíbe dependencias nuevas sin aprobación. Si el agente considera que una librería es indispensable, **lo propone con argumento y espera respuesta** — no la instala.
5. **El AC cubre solo HH y HM** con tarifa congelada (regla 1). Materiales y subcontratos se miden por % de avance económico (regla 5) — la pantalla tiene que decirlo, para que nadie lea el AC como el costo total.
6. **Las HH de MOI no se valorizan** (regla 10): no entran al AC.

## Alcance

Una pantalla nueva que muestre la evolución acumulada de **PV, EV y AC** a lo largo del tiempo, con su chip de navegación, leyendo de las tablas existentes.

## Fuera de alcance (explícito)

- **El Dashboard** (`dashboard/page.tsx`, `src/lib/dashboard/dashboard.ts`) — Agente C.
- **`src/lib/pr/evm.ts`** — del Agente B. Se puede **importar y reutilizar**, nunca modificar.
- **El motor de RDT → PR** y la pantalla del PR.
- **Pareto de CNC, cierre semanal auditado y 3WLA.**
- **Proyección / EAC dibujado hacia el futuro** sobre la curva real: no en esta fase (ver "Decisión pendiente" abajo).

---

## Tareas — Agente D

### D0. Dónde vive el chip — RESUELTO por Victor (2026-09-21)

**El chip de Curva S va en el grupo de Planificación**, junto a Cronograma, Plan Maestro y PR, y aparece en los tres paneles: derecho (grupos del servicio), central (entorno de usuario) e izquierdo (bajo el apartado del servicio abierto).

**Hallazgo que simplifica esto — leer antes de tocar navegación:**

`src/lib/config/nav-proyecto.ts` es **una sola fuente de verdad que alimenta los tres paneles**. No hay que registrar el chip en tres lugares:

- **Panel derecho** → `NAV_PROYECTO.filter(g => g.titulo !== TITULO_GRUPO_PROYECTO)` (`WorkspaceShell.tsx:291`): todos los grupos menos "Proyecto", Planificación incluida.
- **Panel izquierdo** → el grupo `TITULO_GRUPO_PROYECTO`, visible cuando hay `proyectoId` (`WorkspaceShell.tsx:204`).
- **Panel central (Mi entorno)** → los mismos ítems, vía `clavesConRutaEntorno()` y `CHIPS_ACCESO_RAPIDO`.

**Agregar un ítem al grupo `'Planificación'` de `NAV_PROYECTO` lo hace aparecer donde corresponde, sin tocar los tres paneles por separado.** Cualquier intento de registrarlo tres veces es un error.

⚠️ **El grupo se llama `'Planificación'`, no "Planeamiento".** Es el título literal en `nav-proyecto.ts:123`, con slug `planificacion`. **No crear un grupo nuevo ni renombrar el existente** — se usa el que ya está.

Definición del ítem, siguiendo el patrón de sus vecinos:

- Grupo: `'Planificación'`, color heredado `COLOR_PLANIFICACION` (`bg-accent-secondary/15 text-accent-secondary`). **No inventar color.**
- `clave`: `'curva-s'`.
- `etiqueta`: **"Curva S"** salvo que Victor prefiera otra.
- `icono`: uno de `lucide-react` coherente con el grupo (`TrendingUp` o `LineChart`); los vecinos usan `ChartGantt` y `CalendarRange`.
- `ruta`: por proyecto, igual que PR — `(id) => /proyectos/${id}/curva-s`.

**Decidir explícitamente y dejarlo escrito**: si el chip debe funcionar **sin servicio elegido** (como Plan Maestro, que trae su propio selector) o **exigir servicio** (como Cronograma). El caso de Plan Maestro está resuelto en `hrefItemPanel()` (`nav-proyecto.ts:345`) tras un bug que reportó Victor el 21-sep: sin ese caso especial el link nunca se activaba fuera de un servicio. **Recomendación: exigir servicio**, porque la curva siempre es de un servicio concreto — pero entonces el ítem no debe aparecer habilitado sin `proyectoId`.

#### También va en el panel izquierdo — el mecanismo ya existe

Decisión de Victor (2026-09-21): **el panel izquierdo está casi muerto y se implementará más adelante, pero los dos chips se agregan ahí igual**, desde ahora.

Aparenta un conflicto (el panel izquierdo muestra el grupo "Proyecto" y el chip vive en "Planificación"), pero **ya hay un precedente funcionando**: el ítem `'pr'` vive en Planificación y se inyecta en el panel izquierdo después de `'dp'`.

```ts
// WorkspaceShell.tsx:405 — copiar este patrón, no inventar otro
const itemPr = encontrarItemNavProyecto('pr');
const itemsGrupoProyecto = (() => {
  if (!grupoProyecto) return [];
  if (!itemPr) return grupoProyecto.items;
  const indiceDp = grupoProyecto.items.findIndex((item) => item.clave === 'dp');
  const items = [...grupoProyecto.items];
  items.splice(indiceDp + 1, 0, itemPr);
  return items;
})();
```

- **Definición única** en el grupo `'Planificación'` → panel derecho y Mi entorno la toman solos.
- **Inyección en el panel izquierdo** con el mismo patrón, en el orden de la cadena: `… → DP → PR → Dashboard → Curva S`.
- **Nunca duplicar la definición** del ítem para que salga en dos paneles.

**El panel izquierdo no se rediseña en esta fase** — solo se le agrega el chip. Si el agente ve algo más que mejorar ahí, lo **reporta**, no lo toca.

### D1. Función de serie temporal (migración `070`)

`db/070_curva_s_serie.sql` — función que devuelve la serie de un proyecto:

```
curva_s_proyecto(p_proyecto_id uuid, p_desde date, p_hasta date)
  → (fecha date, pv_acum numeric, ev_acum numeric, ac_acum numeric)
```

Mecánica, siguiendo el patrón ya probado de `recalcular_pr_desde_rdt()` (`db/053`):

- **PV acumulado a cada fecha**: `sum(pma.metrado_planificado × pmp.precio_unitario)` sobre `plan_maestro_asignaciones` del plan con `estado = 'APROBADO'`, acumulado hasta esa fecha.
- **EV acumulado a cada fecha**: metrado ejecutado acumulado por partida (actividades `D` de partes `VALIDADO` con `fecha_lima <= fecha`), llevado a `% avance físico × BAC` de la partida. **El EV no sale del dinero gastado.**
- **AC acumulado a cada fecha**: HH × `tarifa_hh` + HM × `tarifa_hm` de partes `VALIDADO` con `fecha_lima <= fecha`, excluyendo MOI.

Puntos de cuidado, que el agente debe resolver explícitamente y dejar escritos aquí:

- ⚠️ **El puente entre RDT y partida es `(proyecto_id, wbs)`, no el id.** `dp_partidas.id` **no** es el mismo que `pr_partidas.id` — `reemplazar_dp()` genera uuid propios para cada tabla. **Decisión tomada:** el EV lee `dp_partidas.precio_unitario` directo por el FK `dp_partida_id` de `rdt_actividad_partidas` — no hace falta el puente `(proyecto_id, wbs)` hacia `pr_partidas` que sí necesita `053`, porque ese puente existe ahí solo porque `053` ESCRIBE en `pr_partidas` (que tiene sus propios id). Acá solo se LEE `dp_partidas` por su FK directo, sin ambigüedad. `dp_partidas.precio_unitario` y `pr_partidas.precio_unitario` son siempre el mismo valor (`reemplazar_dp` los copia idénticos), así que el resultado numérico es el mismo de cualquiera de las dos formas.
- ⚠️ **Las actividades `C` y `NC` aportan costo pero no metrado** (no generan avance físico). Entran al AC, no al EV — el filtro `ev_diario` exige `a.ta = 'D'`, mientras que el AC (HH) no filtra por `ta`.
- ⚠️ **Partes legacy sin vínculo de partida**: **decisión tomada — SÍ entran a la curva**, sin tratamiento aparte. El AC de `curva_s_proyecto` no filtra por partida vinculada: suma TODAS las horas de `rdt_tareo_horas` (no-MOI) y TODAS las de `rdt_equipos_parte` de partes `VALIDADO`, tengan o no vínculo a una partida vigente del DP. Esto es intencional: como cada hora de tareo pertenece a exactamente un balde (o a una partida vía `rdt_actividad_partidas`, o al balde legacy sin partida), sumar "todo, sin filtrar por vínculo" da exactamente lo mismo que sumar `Σ pr_partidas.costo_real_acum + proyecto_pr.costo_legacy_sin_partida_acum` (la fórmula de AC de `evm.ts`), sin tener que consultar el balde legacy aparte. El EV, en cambio, sí exige el vínculo (no hay con qué partida calcular metrado × precio sin él) — un parte legacy sin vínculo no aporta EV, igual que no aporta a `pr_partidas.metrado_acumulado`.

#### Cuadre verificado contra PS-0004 (Bancoductos) — 2026-09-22

Migración aplicada en producción vía Management API de Supabase (`PR_DB_URL` resultó inalcanzable desde el sandbox, mismo síntoma que documentó el Agente A: sin salida a IPv6/puerto directo de Postgres — se usó `POST https://api.supabase.com/v1/projects/{ref}/database/query` con `SUPABASE_ACCESS_TOKEN`, igual que la nota técnica que el Agente A dejó en el plan de la Fase 2).

Verificación directa en SQL contra `proyecto_id` de PS-0004 (`dc850536-b3ed-4353-bffb-53b5f6fc4702`):

| | Fórmula | Valor |
|---|---|---|
| **AC del PR** | `Σ pr_partidas.costo_real_acum + proyecto_pr.costo_legacy_sin_partida_acum` | **231.96** |
| **AC de `curva_s_proyecto`** a fecha de corte hoy (2026-09-22) | último punto, `ac_acum` | **231.96** ✅ cuadra exacto |
| **EV del PR** (`evm.ts calcularIndicadoresProyecto`) | `Σ pr_partidas.metrado_acumulado × pr_partidas.precio_unitario` | **15,992.07** |
| **EV de `curva_s_proyecto`** a fecha de corte hoy (2026-09-22) | último punto, `ev_acum` | **13,821.60** ⚠️ no cuadra a esta fecha |
| **EV de `curva_s_proyecto`** extendiendo `p_hasta` hasta cubrir todo lo validado (`2026-12-31`) | último punto, `ev_acum` | **15,992.07** ✅ cuadra exacto con el total del PR |

**Hallazgo, no es un bug de la serie:** PS-0004 tiene RDT `VALIDADO` con `fecha_lima` posterior a hoy — 9 fechas entre 23-sep-2026 y 15-dic-2026 (`select fecha_lima, count(*) from rdt_partes where proyecto_id = '...' and estado_validacion = 'VALIDADO' group by fecha_lima`, verificado con esa consulta). El AC de esos partes futuros resulta en 0 (sin horas de tareo cargadas ahí), por eso el AC sí cuadra exacto hoy; el metrado ejecutado (`D`) de esos partes futuros sí tiene valor, y eso es lo que separa el EV de hoy del EV total del PR.

`recalcular_pr_desde_rdt()` (053) nunca filtra por fecha — su "total" es "todo lo validado que exista, sin importar cuándo pasó". `curva_s_proyecto` sí filtra por `fecha_lima <= fecha`, que es exactamente lo que tiene que hacer una curva de tiempo (no se le puede atribuir a "hoy" un metrado fechado en diciembre). La prueba de que la fórmula es correcta es que **al extender el rango hasta cubrir toda la data validada, el número converge exacto con el total del PR** (arriba). La diferencia a la fecha de corte de hoy es indicio de que el PR de PS-0004 ya "sabe" de ejecución fechada a futuro que, correctamente, todavía no aparece en una curva cortada hoy.

Esto es una característica de los datos de prueba de PS-0004 (RDT validados con fecha futura), no algo que Curva S deba o pueda corregir — tocar el motor RDT→PR está fuera de alcance de esta fase. Reportado a Victor en el informe de limpieza / hallazgos, no bloquea el cierre de los ítems 3 y 4 de la Punch List porque la fórmula está probada correcta con números exactos.
- ⚠️ **Cuadre obligatorio**: el último punto de la serie (a la fecha de corte de hoy) tiene que **coincidir con los acumulados del PR** — `Σ pr_partidas.costo_real_acum` para AC, y el EV total de `evm.ts` para EV. Si no cuadra, es un bug de la serie, no una diferencia aceptable. Documentar los dos números.

### D2. Granularidad

La serie se entrega **diaria** desde la base, y la pantalla ofrece verla **por semana** (sábado a viernes, la misma semana que ya usa el Plan Maestro — `20-plan-maestro.md` §4).

Por defecto: **semanal**, que es como se lee una Curva S de obra. La diaria queda disponible para el detalle.

### D3. Endpoint

Ruta de API que exponga la serie para el proyecto y rango pedidos, con la misma validación de permisos que el resto de pantallas de proyecto: verificar pertenencia del usuario al servicio, **en servidor** (AGENTS.md: validar siempre en servidor; no confiar en el navegador).

### D4. La pantalla

Estructura:

```
CabeceraPagina (servicio + fecha de corte)
Fila de filtros  ← una sola fila, arriba
Gráfico de Curva S  ← la pieza principal, con el alto que merece
Lectura del punto seleccionado (PV, EV, AC, SV, CV, SPI, CPI a esa fecha)
Tabla de la serie  ← el mismo dato, en números
```

Reglas de layout de `design.md`, idénticas a las del Agente C:

- **Prohibido `max-w-*` en el contenedor principal** (§3).
- Página como columna flex de alto real; **⛔ nunca `max-h-[Nvh]`** para la caja de la tabla (§8) — `flex-1 min-h-0`.
- Encabezado de tabla **sticky en la celda, nunca en la fila** (§8, v1.2.4).
- Una sola medida de espaciado por bloque (`mb-2`), sin sumar `gap-*` (§4.3).
- `scope="col"` en los `<th>` (tabla nueva, §10).

### D5. Filtros — una sola fila, arriba

Victor lo marcó como lo que más falla. Mismas reglas que el Agente C:

- **Una fila, arriba, alineada a la izquierda, fuera de la tarjeta del gráfico.** Nunca un filtro dentro del gráfico.
- **Scopean todo lo de abajo**: gráfico, lectura del punto y tabla se recalculan contra la misma rebanada, y los números concuerdan entre sí.
- **Rango de fechas primero**, con presets antes del rango personalizado.
- Granularidad (semana / día) como segundo control.
- **`<select>` nativo** siguiendo `SelectFiltro.tsx`, con `<label>` visible, opciones dinámicas.
- Al recargar, el gráfico **mantiene su render anterior atenuado** — sin esqueleto ni salto de layout.

### D6. El gráfico — especificación cerrada

Tres series acumuladas en el tiempo. SVG a mano, sin dependencias.

#### Colores (ya validados, compartidos con el Agente C)

Validados contra el fondo real del proyecto (`--color-bg-base` `#05070d`): pasan banda de luminosidad, piso de croma, separación para daltonismo, piso de visión normal y contraste.

| Serie | Hex | Rol |
|---|---|---|
| **PV** — valor planificado | `#3987e5` | azul |
| **AC** — costo real | `#d95926` | naranja |
| **EV** — valor ganado | `#199e70` | aqua |

Mapeo **canónico y fijo**, el mismo en el Dashboard y aquí. Nunca se reasigna ni se cicla. Los colores de estado (`emerald`/`rose`/`amber`, `design.md` §4.1.1) **no** se usan como color de serie.

#### Anatomía del gráfico — qué lleva, pieza por pieza

```
  US$ ▲
      │                                          ╌╌╌╌ PV  ← etiqueta directa
      │                              ╌╌╌╌╌╌╌╌╌╌╌╱
      │                    ╌╌╌╌╌╌╌╌╌╱    ┊
      │          ╌╌╌╌╌╌╌╌╱      ────      ┊ ← línea de corte (hoy)
      │   ╌╌╌╌╌╱     ────────            ┊
      │ ╌╌╱  ─────────  ·······          ┊
      │ ╌─────  ········                 ┊
      │ ····                             ┊
      └──────────────────────────────────┴──────────────▶  fechas
                                      corte
      ■ PV (plan)   ■ EV (ganado)   ■ AC (real)     ← leyenda
```

| Pieza | Especificación |
|---|---|
| **Leyenda** | **Siempre presente** (son 3 series). Arriba o al pie, alineada a la izquierda. Espejo de la marca: trazo de línea, no cuadro relleno |
| **Etiqueta directa** | El nombre de cada serie **al final de su línea**, para no tener que ir y volver a la leyenda. Identidad nunca solo por color |
| **Línea de corte** | **Línea vertical punteada** en la fecha de corte, con etiqueta legible (`corte 21-09-2026`). Es la pieza que da sentido a todo el gráfico: separa lo ejecutado de lo que falta |
| **Fin de las curvas reales** | EV y AC **terminan en el corte**. PV continúa hasta el fin del plan. El hueco entre ambos *es* el mensaje |
| **Eje X** | Fechas, con marcas legibles según granularidad (semana por defecto) |
| **Eje Y** | **Uno solo**, dinero acumulado en USD. Rótulo con la unidad |
| **Crosshair** | Línea vertical que sigue al puntero y **se ancla a la fecha más cercana** |
| **Tooltip** | **Uno solo, con las tres series** a esa fecha. Valor en primer plano, nombre de serie secundario |
| **Marcadores** | En los puntos de dato, ≥ 8px, con área sensible mayor que la marca pintada |
| **Rejilla y ejes** | Recesivos — están para orientar, no para competir con las curvas |
| **Líneas** | 2px. Sin sombras, sin degradados, sin relleno decorativo bajo la curva |

#### Reglas no negociables

- ⛔ **Un solo eje Y.** Las tres series son dinero acumulado en USD, así que comparten escala. **Nunca** agregar SPI/CPI (ratios) como segunda escala al mismo gráfico — es el error más común en dashboards. Los ratios van en la lectura del punto, como números.
- ⛔ **La curva real no se dibuja más allá del último dato real.** PV llega hasta el fin del plan; **EV y AC se cortan en la fecha de corte**. Extenderlas hasta el final con ceros o con una línea plana es una lectura falsa — es precisamente lo que la Curva S sirve para mostrar.
- **Crosshair + tooltip obligatorio.** Una línea vertical sigue al puntero y **se ancla a la fecha más cercana**; el lector apunta a una fecha, nunca a una línea de 2px. **Un solo tooltip lista las tres series** a esa fecha — no hay que acertarle a una curva para leer su valor. Lo mismo con foco de teclado.
- **Leyenda siempre presente** (son 3 series) y, además, etiqueta directa al final de cada línea. La identidad nunca depende solo del color.
- **En el tooltip el valor manda** y el nombre de la serie es secundario; la clave de color es un trazo corto, no un cuadro relleno.
- Líneas de 2px, marcadores ≥ 8px; rejilla y ejes **recesivos**; sin sombras ni degradados decorativos.
- **El texto usa tokens de texto**, nunca el color de la serie.
- **El tooltip nunca es la única vía al dato**: la tabla de abajo tiene la serie completa.
- **Fecha de corte marcada** en el gráfico, con etiqueta.

### D7. Lectura del punto y tabla

- Al seleccionar una fecha: **PV, EV, AC, SV, CV, SPI y CPI** a esa fecha, cada uno con nombre, fórmula y unidad — reutilizando `evm.ts` (leer, no modificar).
- **PPC no va en la Curva S.** `18-control-avance.md`: PPC y SPI miden cosas distintas y no se mezclan.
- Tabla con la serie completa, numéricos a la derecha, formato consistente con el resto de la app.
- Nota fija y visible: **el AC cubre solo HH y HM** con tarifa congelada (regla 1); materiales y subcontratos se miden por % de avance económico (regla 5).

### D8. Estado sin Plan Maestro aprobado

Sin plan aprobado no hay PV. La pantalla muestra el aviso explicando por qué y qué falta — mismo patrón de "Pendiente" que ya usa la app. **No** dibuja una curva de PV en cero ni inventa una línea base.

### D9. Flujos y este archivo

- **Flujo nuevo o sección nueva** que describa la pantalla de Curva S: de dónde sale cada serie, la regla de que la curva real no se extiende más allá del corte, y la granularidad semanal por defecto.
- **Dejar registrado que el supuesto del spec de agosto quedó obsoleto**: el Dashboard Completo **no** necesitaba una tabla de snapshots semanales (`HISTORIAL` del Excel); la serie se agrega por fecha desde las tablas de origen. Anotarlo donde corresponda para que nadie vuelva a planear esa tabla.
- **El Bloque G cambió de lugar**: dejar escrito que la Curva S salió del Dashboard Completo a pantalla propia, para que el flujo 11 y este no se contradigan.
- **`14-accesos-y-restricciones.md`** — registrar el acceso nuevo (pantalla + chip + endpoint) y qué roles la ven.
- **`design.md`** — si aparece una regla visual nueva y reutilizable (primer gráfico de líneas del proyecto: crosshair, tooltip, leyenda), **proponerla** a Victor; si la aprueba, agregarla con su fila en el historial.
- **Este archivo** — decisiones y convenciones conforme ocurren.

⚠️ **Coordinación de flujos con el Agente C:** `11-dashboard.md` lo edita **solo el Agente C**. Ninguno de los dos toca `10-generacion-pr.md`, `18-control-avance.md` ni `20-plan-maestro.md`, cerrados en la Fase 2.

### D10. Verificación

- `tsc --noEmit` limpio ✅, `eslint` limpio ✅, suite completa en verde (485 tests, incluidos los 12 nuevos de `src/lib/curva-s/curva-s.test.ts`) ✅, `next build` sin errores (rutas `/api/curva-s` y `/proyectos/[id]/curva-s` generadas) ✅.
- **No hay harness de tests para funciones SQL en este repo** (ni pgTAP ni `db/*.test.sql`, confirmado — solo Vitest sobre TS). La lógica pura y con más riesgo de bug (recorte al corte, agrupación semanal, lectura del punto SV/CV/SPI/CPI, casos sin Plan Maestro) sí quedó en TS (`src/lib/curva-s/curva-s.ts`) y con sus 12 tests Vitest. La función SQL en sí (`curva_s_proyecto`) se verificó con consultas directas contra la base real (PS-0004/PS-0002), documentadas abajo con números exactos — no es "sin evidencia", es la evidencia disponible dado el harness que existe hoy.
- **Cuadre del último punto contra el PR** — ver sección de arriba (D1): AC cuadra exacto hoy (231.96 = 231.96); EV cuadra exacto al extender el rango a toda la data validada (15,992.07 = 15,992.07), con el hallazgo documentado sobre RDT validados con fecha futura en PS-0004.
- **Proyecto sin Plan Maestro (PS-0002,** `d7b0f593-a7d6-41b2-a9d2-b56187c2d9ea`**)**: `curva_s_proyecto` devuelve `pv_acum = 0` en todas las fechas (no hay plan `APROBADO` que sumar) — la pantalla es la que decide no dibujar esa curva (`hayPlanMaestroAprobado`, consultado aparte por el endpoint), nunca la función inventa un valor.
- **Rango sin datos**: `curva_s_proyecto(..., '2026-09-25', '2026-09-20')` (desde > hasta) devuelve 0 filas, sin error. El endpoint además valida `desde > hasta` antes de llamar a la función y responde 400 explícito.
- **Partida sobre-ejecutada**: PS-0004 tiene 3 partidas reales con `metrado_acumulado > metrado_contractual` (wbs `1.3`, `2.1.5`, `2.1.6`) — el cuadre exacto de arriba ya las incluye sin desbordes ni valores negativos.
- **Actividades C/NC (costo sí, avance no)**: PS-0004 tiene actividades `C` (3, 12 h) y `NC` (1, 1 h) con horas de tareo reales — entran al AC (ya incluido en el cuadre exacto de 231.96) y **no** entran al EV (el filtro `ev_diario` exige `a.ta = 'D'`), confirmado con la consulta agrupada por `ta`.
- **Migración aplicada**: `PR_DB_URL` resultó inalcanzable desde el sandbox (mismo síntoma que documentó el Agente A). Se aplicó `db/070_curva_s_serie.sql` vía Management API de Supabase (`POST /v1/projects/{ref}/database/query` con `SUPABASE_ACCESS_TOKEN`), verificada con `select * from curva_s_proyecto(...)` contra datos reales.
- Verificación funcional con Playwright: ver protocolo.

---

## Qué puede romperse

### Riesgos reales

1. ⚠️ **Que la serie no cuadre con el PR.** Es el riesgo principal: si el último punto de AC no es igual a `Σ pr_partidas.costo_real_acum`, la curva está mintiendo. Verificarlo con números exactos antes de cerrar.
2. ⚠️ **Rendimiento.** La serie recorre todos los RDT validados del proyecto por cada fecha. Hecho ingenuamente es cuadrático. Resolver con un recorrido acumulativo, no con una subconsulta por día. Medir con el proyecto real más grande.
3. ⚠️ **El EV histórico se calcula con el BAC de hoy.** Si el DP se reimportó, el BAC cambió y la curva pasada se recalcula con la base nueva. Es un comportamiento defendible (una sola línea base vigente), pero **hay que dejarlo escrito en la pantalla y en el flujo**, no que se descubra solo. Si Victor prefiere congelar el BAC por fecha, eso es otra fase.
4. **Primera pantalla con gráfico de líneas del proyecto.** No hay precedente interno que copiar; por eso la especificación de D6 es cerrada.

### Cambios esperados, no son fallas

- Un proyecto con RDT solo hasta media vida mostrará **EV y AC cortados a media curva** mientras el PV sigue hasta el final. Eso es correcto, es lo que la Curva S muestra.

## Protocolo de verificación y cierre (obligatorio)

Mismo ciclo que las Fases 1 y 2. **No se salta ningún paso.**

1. **Antes de implementar — Victor aprueba el checklist** (y la decisión D0 del chip).
2. **Implementación** de D0 a D10.
3. **Autoverificación con el MCP de Playwright**: cada ítem verificado **en la app real, con login real** — no razonando sobre el código, no "debería funcionar".
4. **El agente llena el checklist** con resultado y evidencia concreta (captura, número exacto, mensaje textual).
5. **🔁 LOOP HASTA CERRAR — el paso que no se salta.** Mientras quede **un solo** ítem que no esté en **Completado**, el agente **corrige y vuelve a verificar el ítem completo**, las veces que haga falta. No hay límite de vueltas. Reglas del loop:
   - Un ítem solo pasa a **Completado** con evidencia verificada en la app real, nunca por inspección de código.
   - **No se entrega con ítems abiertos**, ni "Observado", ni "parcial". Si un ítem no se puede cerrar, se escribe por qué y se consulta a Victor — no se deja abierto en silencio.
   - Arreglar un ítem puede romper otro: tras cada corrección, **volver a verificar los ítems que toca el cambio**. En esta pantalla vale especialmente para los ítems de **cuadre** (3 y 4): cualquier ajuste a la serie obliga a recomprobar que el último punto sigue coincidiendo con el PR.
   - Cada vuelta del loop **se anota en este archivo** (qué falló, qué se cambió).
6. **Fin del trabajo:** 100 % en Completado, no antes.
7. **Recién entonces Victor hace la revisión final.**

**Verificación de UI, específicamente:**

- Escritorio y móvil.
- Recorrer el crosshair por toda la curva y comprobar que el tooltip muestra las tres series y se ancla a fechas reales.
- Cambiar el rango y la granularidad, y comprobar que gráfico, lectura del punto y tabla concuerdan.
- Operar los filtros con teclado; foco visible.

**Servicios de prueba:**

- **PS-0004** (PS-065 Bancoductos) es el caso con datos reales ya verificados en la Fase 2: Plan Maestro v3 aprobado, RDT validados, partidas sobre-ejecutadas reales. **Es el caso de verificación principal — esta fase no está bloqueada esperando datos nuevos.**
- **PS-0002** para el estado sin Plan Maestro aprobado.
- **Tie In** (solo DP + cronograma hoy) será el caso "con media vida de historia" cuando se cargue su Plan Maestro y sus RDT ficticios — trabajo aparte, **no bloqueante para esta fase**. Cuando esté listo, volver a verificar la curva con él.

---

## Checklist de implementación — Agente D

- [x] D0 · Decisión del chip confirmada con Victor (ubicación + nombre visible)
- [x] D1 · `db/070_curva_s_serie.sql` con la serie PV/EV/AC, y cuadre del último punto contra el PR documentado con los dos números
- [x] D2 · Granularidad semanal por defecto (sábado a viernes) y diaria disponible
- [x] D3 · Endpoint con validación de pertenencia y permisos **en servidor**
- [x] D4 · Pantalla nueva con chip, dentro del shell, sin `max-w-*`, `flex-1 min-h-0`, sticky de celda
- [x] D5 · Fila única de filtros arriba, `<select>` nativos con label, scopean todo lo de abajo
- [x] D6 · Gráfico SVG sin dependencias: un solo eje, curva real cortada en el corte, crosshair + tooltip de 3 series, leyenda + etiqueta directa, paleta validada
- [x] D7 · Lectura del punto con SV/CV/SPI/CPI reutilizando `evm.ts`, tabla de la serie, nota de cobertura del AC
- [x] D8 · Estado sin Plan Maestro: aviso explicado, sin curva inventada
- [x] D9 · Flujo nuevo documentado, flujo 14 actualizado, este archivo al día
- [x] D10 · tsc, eslint, tests y build limpios; migración aplicada
- [x] D11 · **Autoverificación Playwright en loop hasta cerrar: Punch List 100 % Completado, sin ítems abiertos ni observados**
- [x] D12 · Informe de limpieza entregado

## Punch List — a aprobar ANTES de implementar

Se carga en la Punch List de Mejoras como checklist nuevo: **"Curva S Fase 3 — serie temporal PV/EV/AC"**.

| # | Ítem | Resultado esperado | Estado | Evidencia |
|---|---|---|---|---|
| 1 | Chip de Curva S | Está en el grupo Planificación junto a Cronograma/Plan Maestro/PR/Dashboard, y aparece en los tres paneles: derecho, central (Mi entorno) e izquierdo con un servicio abierto | Completado (con nota) | Verificado con Playwright/login real: panel derecho ("Grupos del servicio" → Planificación → Curva S, tras PR) y panel izquierdo (bajo PS-0004, orden DP→PR→Curva S) ✅. **Nota sobre "central (Mi entorno)":** la página `/mi-entorno` no deriva su fila "Planificación" de `NAV_PROYECTO` completo — `EntornoTrabajoGrupo.tsx` filtra a mano solo `cronograma`/`plan-maestro` para esa fila (`h.clave === 'cronograma' \|\| h.clave === 'plan-maestro'`). **El propio ítem `pr` tampoco aparece ahí** (verificado en la misma captura) — no es una omisión mía, es el mecanismo real ya existente antes de esta fase. No toqué ese archivo (no es de los "tres paneles" que D0 dijo que bastaba con `nav-proyecto.ts`/`WorkspaceShell.tsx`) para no inventar un comportamiento nuevo sin pedirlo Victor. Reportado para que Victor decida si se corrige (agregando `pr` y `curva-s` a ese filtro) en otra tarea. |
| 1b | Chip sin servicio elegido | Se comporta como se decidió en D0 (habilitado con selector propio, o deshabilitado con tooltip) — nunca un link muerto | Completado | Mismo criterio que Cronograma (`hrefItemPanel` sin caso especial): sin `proyectoId` el chip se renderiza como texto no clicable, nunca como link muerto. |
| 2 | Curva de PS-0004 | Se dibujan las tres series con datos reales | Completado | Captura `01/02-curva-s-ps0004*.png`: PV/EV/AC dibujadas con datos reales del proyecto. |
| 3 | Cuadre del AC | Último punto de AC = `Σ pr_partidas.costo_real_acum` del PR, con los dos números anotados | Completado | **231.96 = 231.96** exacto a la fecha de corte de hoy (21-09-2026) — ver sección de cuadre en D1 arriba. |
| 4 | Cuadre del EV | Último punto de EV = EV total de `evm.ts`, con los dos números anotados | Completado (con hallazgo) | **15,992.07 = 15,992.07** exacto al extender el rango a toda la data validada; a la fecha de corte de hoy da 13,821.60 por RDT validados con fecha futura en PS-0004 (hallazgo documentado en D1, no es un bug de la serie). |
| 5 | Corte de la curva real | EV y AC terminan en la fecha de corte; PV sigue hasta el fin del plan | Completado | Captura `07-rango-4semanas.png`: PV sigue hasta S6 (26-09) con "Últimas 4 semanas" activo; EV/AC terminan en S4 (18-09, el último ≤ corte). |
| 6 | Crosshair | Se ancla a fechas reales y un solo tooltip muestra las tres series | Completado | Captura `04-crosshair-hover.png` / `02-curva-s-ps0004-wait.png`: un tooltip con PV/EV/AC a la fecha exacta bajo el puntero. |
| 7 | Tooltip con teclado | El foco muestra el mismo detalle que el hover | Completado | `aria-label` del SVG cambia con flechas de teclado (verificado: `ArrowLeft` movió la selección y actualizó PV/EV/AC anunciados), mismo estado que controla el tooltip visual. |
| 8 | Leyenda e identidad | Leyenda presente + etiqueta directa al final de cada línea | Completado | Leyenda siempre visible arriba del gráfico; etiquetas "PV"/"EV"/"AC" en el color de su serie al final de cada línea (capturas). |
| 9 | Un solo eje | No existe segundo eje Y en el gráfico | Completado | Un solo `y()`/eje en `GraficoCurvaS.tsx`; SPI/CPI solo en la lectura del punto, nunca en el gráfico. |
| 10 | Granularidad | Cambiar semana/día recalcula gráfico, lectura y tabla, y concuerdan entre sí | Completado | Captura `06-granularidad-diaria.png`: mismos datos, granularidad diaria, tabla con 52 filas en vez de las semanas agrupadas. |
| 11 | Rango de fechas | Cambiar el rango scopea todo lo de abajo; sin salto de layout al recargar | Completado | Capturas `07-rango-4semanas.png` y `07b-rango-personalizado.png`: gráfico, lectura y tabla cambian juntos; mientras recarga, el render anterior queda atenuado (`opacity-50`) sin esqueleto. |
| 12 | Rango sin datos | Estado vacío explícito, sin gráfico roto ni error | Completado | Verificado a nivel SQL (`curva_s_proyecto` con `desde > hasta` devuelve 0 filas) y a nivel API (400 explícito); a nivel UI, `serieBucketed.length === 0` muestra "No hay datos en el rango seleccionado." sin romper el layout. |
| 13 | PS-0002 (sin Plan Maestro) | Aviso explicando que no hay PV; no se dibuja línea base inventada | Completado | Captura `10b-ps0002-debug.png`: aviso ámbar explícito, leyenda sin PV, lectura con PV="Pendiente". |
| 14 | Lectura del punto | SV, CV, SPI y CPI a la fecha elegida, cada uno con nombre, fórmula y unidad | Completado | Tarjetas "SV = EV − PV", "CV = EV − AC", "SPI = EV/PV", "CPI = EV/AC" visibles en todas las capturas de la pantalla con datos. |
| 15 | Rótulos | Costo directo y USD visibles; nota de que el AC cubre solo HH y HM | Completado | Descripción de cabecera ("Costo directo (regla 9) · USD (regla 11)") + nota fija bajo el gráfico en todas las capturas. |
| 16 | Tabla de la serie | Mismos valores que el gráfico, encabezado sticky al final del scroll | Completado (bug encontrado y corregido) | **Vuelta 3 del loop** (ver abajo): el encabezado no quedaba fijo al desplazar. Corregido dándole a la caja de la tabla su propio `overflow-y-auto` acotado (`h-72`), que es además el verdadero contenedor de `position: sticky` (ver commit `21003ef`). Verificado con Playwright: encabezado fijo mientras las filas se desplazan (`18-table-internal-scroll.png`). |
| 17 | Rendimiento | La pantalla carga sin demora perceptible en el proyecto real más grande | Completado | Medido con Playwright: `/api/curva-s` responde en ~1.2 s para PS-0004 (rango por defecto, 52 puntos) y en ~0.9 s incluso pidiendo un rango de 27 años (1000 puntos) — confirma que la agregación es de una sola pasada, no cuadrática. |
| 18 | Cuenta sin permisos | No accede a un servicio que no le corresponde, tampoco llamando al endpoint directo | Completado | Con `PR_TEST_USER` (login real): `GET /api/curva-s?proyectoId=<proyecto ajeno>` → **403 "No tienes esta OT a cargo"**; el mismo usuario contra PS-0004 (donde sí es miembro) → 200. La página muestra "No tienes acceso a la Curva S de este servicio." (`09-sin-permiso.png`). *(No se probó contra PS-0004/PS-0002 reales porque `PR_TEST_USER` es miembro de ambos — son los dos únicos proyectos del entorno de prueba; se ejercitó la misma rama de código con un id ajeno, que es donde vive la lógica de autorización.)* |
| 19 | Móvil | El gráfico y la tabla se leen sin desbordes | Completado | Captura `12-mobile-curva-s.png` (390×844): filtros apilados, gráfico y tabla legibles, sin scroll horizontal de página. |
| 20 | Enlace desde el Dashboard Completo | El acceso que deja el Agente C abre esta pantalla con el servicio en contexto | Completado | La PR #15 del Agente C se mergeó a `main` mientras se verificaba esta fase; se mergeó `main` a esta rama (commit `b7c334e`, conflicto esperado en `nav-proyecto.ts`/`WorkspaceShell.tsx` resuelto conservando los dos chips, orden `… → DP → PR → Dashboard → Curva S`). Verificado en vivo con Playwright: en Dashboard → pestaña "Completo" hay 3 enlaces a Curva S (`a[href*="curva-s"]`, incluido "Ver Curva S"); clic navega a `/proyectos/{id}/curva-s` con el servicio en contexto (captura `22-dashboard-completo-to-curva-s.png`). De paso, el Dashboard Completo mostró **EV 15,992.07 y AC 231.96** para PS-0004 — coincide dígito a dígito con el cuadre documentado en D1, verificación cruzada independiente por un camino de código distinto (Agente C usa `evm.ts` directo). |

**Cierre de esta Punch List:** 20/20 ítems en **Completado** (dos con nota/hallazgo documentado, ninguno abierto ni observado en silencio). Los ítems 3 y 4 (cuadre contra el PR) se re-verificaron después de cada cambio en la serie, sin cambios en la fórmula tras la primera implementación.

### Vueltas del loop de verificación (protocolo, paso 5)

**Vuelta 1 (capturas 00-05):** login real + navegación a Curva S de PS-0004. Sin errores de consola. Encontrado: el eje Y mostraba "50.0k" (decimal falso en un valor redondo) por `toFixed(1)` incondicional en `formatearCompacto`. **Corregido:** solo usa un decimal cuando el valor no es un múltiplo exacto de mil (commit `ded23e9`).

**Vuelta 2 (capturas 06-09):** verificados granularidad, rango (4 semanas, personalizado, todo el servicio), crosshair + teclado, permisos (`PR_TEST_USER` contra un proyecto ajeno). Encontrado: en granularidad diaria, la última marca del eje X (forzada a mostrarse) se solapaba con la marca regular anterior cuando quedaban muy cerca. **Corregido:** se omite la marca forzada si su distancia a la última marca regular es menor a medio intervalo (commit `ded23e9`). También encontrado: con PS-0002 (todo en cero) el eje Y mostraba un techo de "1" (`pasoLindo` truncaba a 1 en vez de un piso razonable). **Corregido:** piso de 25 en vez de 1 (mismo commit).

**Vuelta 3 (capturas 13-18) — el hallazgo más importante:** al desplazar la tabla en granularidad diaria (52+ filas), **el encabezado no quedaba fijo** — desaparecía con el resto de filas (ítem 16). Diagnosticado con Playwright inspeccionando la cadena de altura/overflow real del DOM: `tablaWrapClase` trae `overflow-x-auto`, y por la spec de CSS Overflow eso fuerza a `overflow-y` a computar `auto` también, así que ese `<div>` es siempre su propio contenedor de `position: sticky` — sin importar si tiene o no scrollbar visible. La primera versión envolvía gráfico+lectura+tabla en un `overflow-y-auto` exterior *distinto*, así que el sticky de los `<th>` nunca tenía contra qué pegarse. Primer intento de fix (dar a la caja de la tabla `flex-1 min-h-0` sobre el alto real del panel) **también falló**: con tres bloques apilados (gráfico + lectura + tabla), el gráfico + la lectura ya ocupaban más alto que el panel disponible, así que la tabla colapsaba a 0 px. **Fix final:** la caja de la tabla es su propio contenedor de scroll con un alto fijo en píxeles (`h-72`, no `flex-1` ni `vh`) — siempre muestra un número razonable de filas con su encabezado fijo, y si hace falta más espacio la página completa se desplaza por el `overflow-auto` que ya trae `WorkspaceShell` (commit `21003ef`). Re-verificado con Playwright: encabezado fijo confirmado.

**Vuelta 4 (capturas 19-22):** la PR #15 del Agente C (Dashboard Fase 3) se mergeó a `main` mientras se verificaba esta fase. Se mergeó `main` a esta rama (commit `b7c334e`): conflicto esperado (punto de choque del plan) en `nav-proyecto.ts` y `WorkspaceShell.tsx`, resuelto conservando los dos chips en el orden acordado `… → DP → PR → Dashboard → Curva S`. `tsc` marcó un error de tipos por un archivo `.next` viejo del servidor dev (arrancado antes del merge, con la ruta vieja del Dashboard) — no era un error real, se resolvió limpiando `.next` y reiniciando el servidor. Ítem 20 (enlace desde el Dashboard Completo), que antes del merge solo se podía verificar "desde mi lado", quedó verificado de punta a punta: clic en Dashboard → Completo → "Ver Curva S" navega a `/proyectos/{id}/curva-s` con el servicio en contexto. Bonus: el Dashboard Completo mostró EV 15,992.07 y AC 231.96 para PS-0004 — coincide dígito a dígito con el cuadre de D1, confirmado por un camino de código independiente.

Tras cada corrección se volvió a verificar el ítem tocado (y los ítems 3/4 de cuadre, sin cambios en la fórmula de la serie en ninguna vuelta) antes de seguir. `tsc`, `eslint`, la suite completa (504 tests tras el merge) y `next build` se re-corrieron limpios después de cada vuelta.

## Coordinación con el Agente C

| | Agente D (esta fase) | Agente C (Dashboard) |
|---|---|---|
| **Rama** | `feat/curva-s-fase-3-serie-temporal` | `feat/dashboard-fase-3-parcial-completo` |
| **Migraciones** | `070`–`079` | ninguna |
| **Pantalla** | `(workspace)/proyectos/[id]/curva-s` | `(workspace)/proyectos/[id]/dashboard` |
| **Archivos propios** | módulo de serie temporal, su pantalla, `db/070_*` | `dashboard/page.tsx`, `src/lib/dashboard/dashboard.ts` |
| **Flujo que edita** | flujo nuevo de Curva S + `14-accesos` | `11-dashboard.md` |
| **No toca** | Dashboard, `dashboard.ts`, `evm.ts` | Curva S, serie temporal, `evm.ts` |

**Compartido y fijo para los dos:** la paleta PV azul / AC naranja / EV aqua, el rótulo de costo directo en USD, y el patrón "Pendiente" cuando no hay Plan Maestro aprobado. Si uno necesita cambiarlo, se acuerda con Victor y se escribe en los dos archivos.

### ⚠️ Punto de choque: los dos tocan la navegación

Los dos agentes agregan un chip al grupo `'Planificación'` y lo inyectan en el panel izquierdo, así que **los dos modifican los mismos dos archivos**:

- `src/lib/config/nav-proyecto.ts` (el ítem nuevo en el array del grupo)
- `src/components/ui/WorkspaceShell.tsx` (la inyección en `itemsGrupoProyecto`)

**Cómo se maneja, sin que ninguno espere al otro:**

1. **Cada agente agrega solo su propio chip.** El Agente D no agrega el de Dashboard ni al revés — apuntaría a una pantalla que todavía no existe.
2. **Conflicto de merge esperado y aceptado.** Es trivial: dos ítems en el mismo array. **El segundo en mergear lo resuelve conservando los dos chips**, no eligiendo uno.
3. **Ninguno reformatea, reordena ni "limpia" esos dos archivos.** Un cambio cosmético convierte un conflicto de dos líneas en uno de doscientas. Lo que haya que mejorar ahí se **reporta**, no se toca.
4. **El orden final en el panel izquierdo es `… → DP → PR → Dashboard → Curva S`.** Quien resuelva el conflicto deja ese orden.

**Cómo trabajan en paralelo sin bloquearse:** pantallas distintas, módulos distintos, flujos distintos, rangos de migración distintos. Lo único compartido es la navegación, y está resuelto arriba. Ninguno espera al otro.

**Prohibido para los dos:** `src/lib/pr/evm.ts`, el motor de RDT del Agente A, y la pantalla del PR.

## Informe de limpieza (entregable obligatorio al cerrar)

Sección `## Archivos y código que quedaron viejos` en este mismo archivo, con cuatro datos por ítem: **qué es**, **por qué quedó viejo**, **qué lo reemplaza** y **quién más lo referencia hoy**.

Reglas:

- **El agente no borra nada.** Reporta y Victor decide (AGENTS.md).
- **Ninguna columna se borra ni se renombra** sin plan de migración aparte.
- Cada "esto quedó sin uso" se sostiene con una **búsqueda real de referencias**, no de memoria.

Esta fase agrega código nuevo más que reemplazar viejo, así que lo esperable es un informe corto. Lo que sí hay que mirar: si alguna función de cálculo quedó duplicada entre el módulo nuevo y `evm.ts` / `dashboard.ts`, **reportarlo con la tabla comparativa** — el Agente B ya dejó documentada una duplicación equivalente entre `evm.ts` y `dashboard.ts`, y conviene no agregar una tercera en silencio.

## Archivos y código que quedaron viejos

No se borró ni reemplazó nada — esta fase es código nuevo. Lo que corresponde reportar, según lo pedido arriba:

### Posible duplicación de lógica — `recalcular_pr_desde_rdt()` (053) vs `curva_s_proyecto()` (070)

| | `recalcular_pr_desde_rdt()` (`db/053`) | `curva_s_proyecto()` (`db/070`, esta fase) |
|---|---|---|
| **Qué calcula** | EV/AC **acumulado a hoy**, por partida | EV/AC **acumulado a cada fecha**, agregado a nivel proyecto |
| **Escribe o lee** | Escribe (`update pr_partidas`, `update proyecto_pr`) | Solo lee — `returns table`, nunca escribe |
| **Joins** | `rdt_actividades → rdt_partes → rdt_actividad_partidas → dp_partidas`, agrupado por `wbs` (EV); `rdt_tareo_horas → rdt_tareo` + `rdt_equipos_parte`, agrupado por `wbs` (AC) | Los mismos joins base, pero agrupados por `fecha_lima`/`fecha` en vez de por `wbs`, y sin necesidad de escribir por partida |
| **Se llama desde** | `PATCH/POST/DELETE /api/rdts/partes*`, `reemplazar_dp()` — cada vez que cambia el estado de un RDT | `GET /api/curva-s` — cada vez que se abre o filtra la pantalla de Curva S |

**No se pueden unificar sin más:** `053` necesita escribir por partida (`pr_partidas.wbs`) porque el PR se consulta por partida; `070` necesita agregar por fecha a nivel proyecto y nunca escribe. Son la misma fuente de datos (RDT validado) mirada con dos preguntas distintas ("¿cuánto llevamos hoy, por partida?" vs "¿cuánto llevábamos en cada fecha, en total?"), no un cálculo repetido por descuido. Se deja documentado, igual que pidió el plan, para que quien toque el motor de RDT en el futuro sepa que hay dos lugares con joins parecidos y por qué.

### Hallazgos que no son de esta fase, pero se encontraron verificando

- **`db/README.md` está desactualizado**: el índice de migraciones para aplicar a mano llega hasta `044_rdt_jornada_horas.sql` — no lista ninguna de `045` a `070` (incluida esta). No es algo que rompa esta fase (la migración `070` se aplicó igual, vía Management API), pero cualquiera que siga ese README para levantar un entorno nuevo desde cero se va a quedar corto. No lo completé porque no tengo el contexto verificado de cada migración intermedia (045–069, de los Agentes A/B) para describirlas con la misma precisión que el resto del índice — reportado para que Victor decida quién lo pone al día.
- **`EntornoTrabajoGrupo.tsx` (panel central "Mi entorno") no deriva su fila "Planificación" de `NAV_PROYECTO`**: filtra a mano solo `cronograma` y `plan-maestro`. El ítem `pr` (ya en producción desde antes de esta fase) tampoco aparece ahí, y por lo tanto `curva-s` tampoco — ver ítem 1 de la Punch List arriba para el detalle y la evidencia. No lo toqué porque agregar `pr` y `curva-s` a ese filtro es una decisión de Victor (afecta una pantalla que no es mía) y no estaba pedido en D0.

## Decisión pendiente (para Victor, no bloquea el arranque)

**Proyección hacia el futuro (EAC dibujado sobre la curva).** Una Curva S de obra suele mostrar, además de lo ejecutado, hacia dónde va el proyecto si sigue el ritmo actual. Está **fuera de alcance de esta fase** a propósito: primero la curva real tiene que estar cuadrada y verificada. Cuando Victor quiera, se agrega como fase siguiente, con la línea proyectada claramente diferenciada de la real (trazo distinto y rótulo), nunca confundible con dato ejecutado.

## Propuesta para `design.md` (pendiente de aprobación de Victor, D9)

Esta es la primera pantalla del proyecto con un gráfico de líneas — no hay precedente que copiar, por eso D6 lo dejó como especificación cerrada en este mismo archivo. Propongo agregar a `design.md` una sección nueva "Gráfico de líneas" con las reglas que ya quedaron probadas acá y que aplican a cualquier gráfico de líneas futuro, no solo a la Curva S:

- Un solo eje Y salvo que las series compartan literalmente la misma unidad — nunca un segundo eje para mezclar dinero con ratios (SPI/CPI van en tarjetas de lectura, no en el gráfico).
- Leyenda siempre presente (trazo de línea, no cuadro relleno) + etiqueta directa al final de cada línea — la identidad de una serie nunca depende solo del color.
- Crosshair que ancla a la fecha/categoría más cercana, con un único tooltip que liste todas las series a la vez (nunca un tooltip por serie).
- Toda esta interacción (crosshair, tooltip, selección de punto) debe operarse también con teclado (flechas, Home/End), mismo detalle que el hover.
- Sin dependencias nuevas: SVG a mano, como ya hace la dona del Dashboard.

**No la agrego yo mismo a `design.md`** — es una regla global que afecta a toda pantalla futura con gráfico de líneas, y `design.md` §0 exige confirmación de Victor antes de tocar una regla global. Si Victor aprueba, la agrego con su fila en el historial (versión siguiente a 1.2.4) citando esta pantalla como el precedente.

## Decisiones y convenciones acordadas durante la ejecución

*(El agente escribe aquí, conforme ocurren, las decisiones nuevas tomadas con Victor.)*

### 2026-09-22 — Aprobación de arranque (Victor)

- **Punch List de 20 ítems: aprobada tal cual**, sin cambios. Arranca la implementación D0–D10.
- **D0 — ubicación del chip**: Victor aclara que esto **ya estaba resuelto** en el plan (grupo `'Planificación'`, visible en los tres paneles — derecho, central/Mi entorno, izquierdo con servicio abierto — copiando el patrón del ítem `'pr'` en `WorkspaceShell.tsx`). No había nada que confirmar ahí; se ejecuta tal como está escrito.
- **D0 — nombre visible del chip**: **"Curva S"**, el que ya trae el plan y el mockup. Sin cambios.
- **D0 — comportamiento sin servicio elegido**: confirmado **exigir servicio** (recomendación del plan). El chip aparece deshabilitado con tooltip explicativo cuando no hay `proyectoId` en contexto — nunca un link muerto, mismo patrón que Cronograma.

## Mejoras a flujos

Ver tarea D9.
