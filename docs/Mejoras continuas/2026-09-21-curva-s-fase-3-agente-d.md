# Curva S Fase 3 (Agente D): serie temporal PV / EV / AC en pantalla propia

**Estado (2026-09-21):** PLAN INICIAL — **pendiente de aprobación de Victor** (plan + Punch List). Sin checklist aprobado, la implementación no arranca. Trabaja en paralelo con [Dashboard / Fase 3 (Agente C)](2026-09-21-dashboard-fase-3-agente-c.md).

**Ya resuelto, no volver a preguntar:**
- La Curva S era el **Bloque G del Dashboard Completo** en el diseño original (`docs/superpowers/specs/2026-08-16-dashboard-parcial-design.md` §2, repo web). **Victor la saca de ahí**: va en **pantalla propia con su propio chip**, porque dentro del Dashboard no hay espacio. El Dashboard Completo (Agente C) **la enlaza**, no la dibuja.
- **No hace falta ninguna tabla de snapshots históricos.** Esto **contradice el supuesto del spec de agosto**, que daba por hecho que el Completo necesitaba "un historial semanal de snapshots, equivalente a `HISTORIAL` del Excel". Verificado contra el esquema real el 2026-09-21: el dato diario ya existe en las tablas de origen (ver "Por qué esto se puede construir hoy"). **Ese supuesto quedó obsoleto y así hay que documentarlo.**
- Paleta de series: ya validada y **compartida con el Agente C** — ver "Colores".
- `docs/visual-companion/design.md` es de **lectura obligatoria completa** antes de tocar interfaz.
- **La Punch List se cierra en loop, no en una pasada.** Ver protocolo: verificar, corregir y volver a verificar hasta el 100 % en Completado. No se entrega con ítems abiertos.

## Ejecución en la nube

Mismo modo de trabajo que los Agentes A y B (Fases 1 y 2 del PR):

- **Rama propia en `py_control_proyectos_web`**, no directo a `main`. Rama sugerida: `feat/curva-s-serie-temporal`. Al 100 % del checklist, abre un **PR** para que Victor lo revise antes de mergear.
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

- ⚠️ **El puente entre RDT y partida es `(proyecto_id, wbs)`, no el id.** `dp_partidas.id` **no** es el mismo que `pr_partidas.id` — `reemplazar_dp()` genera uuid propios para cada tabla. Está documentado en `053`; repetir el mismo criterio.
- ⚠️ **Las actividades `C` y `NC` aportan costo pero no metrado** (no generan avance físico). Entran al AC, no al EV.
- ⚠️ **Partes legacy sin vínculo de partida**: el Agente A los dejó en un balde a nivel proyecto (`hh_legacy_sin_partida_acum` y compañía). Decidir si entran a la curva y **dejarlo escrito**; si entran, tienen que cuadrar con el total del PR.
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

- `tsc --noEmit` limpio, `eslint` limpio, suite completa en verde, `next build` sin errores.
- **Tests de la función de serie**: cuadre del último punto contra el PR, proyecto sin Plan Maestro, rango sin datos, partida sobre-ejecutada, y el caso de actividades C/NC (costo sí, avance no).
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

- [ ] D0 · Decisión del chip confirmada con Victor (ubicación + nombre visible)
- [ ] D1 · `db/070_curva_s_serie.sql` con la serie PV/EV/AC, y cuadre del último punto contra el PR documentado con los dos números
- [ ] D2 · Granularidad semanal por defecto (sábado a viernes) y diaria disponible
- [ ] D3 · Endpoint con validación de pertenencia y permisos **en servidor**
- [ ] D4 · Pantalla nueva con chip, dentro del shell, sin `max-w-*`, `flex-1 min-h-0`, sticky de celda
- [ ] D5 · Fila única de filtros arriba, `<select>` nativos con label, scopean todo lo de abajo
- [ ] D6 · Gráfico SVG sin dependencias: un solo eje, curva real cortada en el corte, crosshair + tooltip de 3 series, leyenda + etiqueta directa, paleta validada
- [ ] D7 · Lectura del punto con SV/CV/SPI/CPI reutilizando `evm.ts`, tabla de la serie, nota de cobertura del AC
- [ ] D8 · Estado sin Plan Maestro: aviso explicado, sin curva inventada
- [ ] D9 · Flujo nuevo documentado, flujo 14 actualizado, este archivo al día
- [ ] D10 · tsc, eslint, tests y build limpios; migración aplicada
- [ ] D11 · **Autoverificación Playwright en loop hasta cerrar: Punch List 100 % Completado, sin ítems abiertos ni observados**
- [ ] D12 · Informe de limpieza entregado

## Punch List — a aprobar ANTES de implementar

Se carga en la Punch List de Mejoras como checklist nuevo: **"Curva S Fase 3 — serie temporal PV/EV/AC"**.

| # | Ítem | Resultado esperado | Estado | Evidencia |
|---|---|---|---|---|
| 1 | Chip de Curva S | Está en el grupo Planificación junto a Cronograma/Plan Maestro/PR/Dashboard, y aparece en los tres paneles: derecho, central (Mi entorno) e izquierdo con un servicio abierto | Pendiente | |
| 1b | Chip sin servicio elegido | Se comporta como se decidió en D0 (habilitado con selector propio, o deshabilitado con tooltip) — nunca un link muerto | Pendiente | |
| 2 | Curva de PS-0004 | Se dibujan las tres series con datos reales | Pendiente | |
| 3 | Cuadre del AC | Último punto de AC = `Σ pr_partidas.costo_real_acum` del PR, con los dos números anotados | Pendiente | |
| 4 | Cuadre del EV | Último punto de EV = EV total de `evm.ts`, con los dos números anotados | Pendiente | |
| 5 | Corte de la curva real | EV y AC terminan en la fecha de corte; PV sigue hasta el fin del plan | Pendiente | |
| 6 | Crosshair | Se ancla a fechas reales y un solo tooltip muestra las tres series | Pendiente | |
| 7 | Tooltip con teclado | El foco muestra el mismo detalle que el hover | Pendiente | |
| 8 | Leyenda e identidad | Leyenda presente + etiqueta directa al final de cada línea | Pendiente | |
| 9 | Un solo eje | No existe segundo eje Y en el gráfico | Pendiente | |
| 10 | Granularidad | Cambiar semana/día recalcula gráfico, lectura y tabla, y concuerdan entre sí | Pendiente | |
| 11 | Rango de fechas | Cambiar el rango scopea todo lo de abajo; sin salto de layout al recargar | Pendiente | |
| 12 | Rango sin datos | Estado vacío explícito, sin gráfico roto ni error | Pendiente | |
| 13 | PS-0002 (sin Plan Maestro) | Aviso explicando que no hay PV; no se dibuja línea base inventada | Pendiente | |
| 14 | Lectura del punto | SV, CV, SPI y CPI a la fecha elegida, cada uno con nombre, fórmula y unidad | Pendiente | |
| 15 | Rótulos | Costo directo y USD visibles; nota de que el AC cubre solo HH y HM | Pendiente | |
| 16 | Tabla de la serie | Mismos valores que el gráfico, encabezado sticky al final del scroll | Pendiente | |
| 17 | Rendimiento | La pantalla carga sin demora perceptible en el proyecto real más grande | Pendiente | |
| 18 | Cuenta sin permisos | No accede a un servicio que no le corresponde, tampoco llamando al endpoint directo | Pendiente | |
| 19 | Móvil | El gráfico y la tabla se leen sin desbordes | Pendiente | |
| 20 | Enlace desde el Dashboard Completo | El acceso que deja el Agente C abre esta pantalla con el servicio en contexto | Pendiente | |

**Cierre de esta Punch List:** se cierra **en loop** (ver protocolo, paso 5). El agente verifica, corrige y vuelve a verificar hasta que los 20 ítems estén en **Completado**, con evidencia real de la app. Los ítems 3 y 4 (cuadre contra el PR) se re-verifican después de **cualquier** cambio en la serie. No se entrega con ítems abiertos ni observados.

## Coordinación con el Agente C

| | Agente D (esta fase) | Agente C (Dashboard) |
|---|---|---|
| **Migraciones** | `070`–`079` | ninguna |
| **Pantalla** | Curva S (nueva, chip propio) | `(workspace)/proyectos/[id]/dashboard` |
| **Archivos propios** | módulo de serie temporal, su pantalla, `db/070_*` | `dashboard/page.tsx`, `src/lib/dashboard/dashboard.ts` |
| **Flujo que edita** | flujo nuevo de Curva S + `14-accesos` | `11-dashboard.md` |
| **No toca** | Dashboard, `dashboard.ts`, `evm.ts` | Curva S, serie temporal, `evm.ts` |

**Compartido y fijo para los dos:** la paleta PV azul / AC naranja / EV aqua, el rótulo de costo directo en USD, y el patrón "Pendiente" cuando no hay Plan Maestro aprobado. Si uno necesita cambiarlo, se acuerda con Victor y se escribe en los dos archivos.

**Cómo trabajan en paralelo sin bloquearse:** pantallas distintas, módulos distintos, flujos distintos, rangos de migración distintos. Ninguno espera al otro.

**Prohibido para los dos:** `src/lib/pr/evm.ts`, el motor de RDT del Agente A, y la pantalla del PR.

## Informe de limpieza (entregable obligatorio al cerrar)

Sección `## Archivos y código que quedaron viejos` en este mismo archivo, con cuatro datos por ítem: **qué es**, **por qué quedó viejo**, **qué lo reemplaza** y **quién más lo referencia hoy**.

Reglas:

- **El agente no borra nada.** Reporta y Victor decide (AGENTS.md).
- **Ninguna columna se borra ni se renombra** sin plan de migración aparte.
- Cada "esto quedó sin uso" se sostiene con una **búsqueda real de referencias**, no de memoria.

Esta fase agrega código nuevo más que reemplazar viejo, así que lo esperable es un informe corto. Lo que sí hay que mirar: si alguna función de cálculo quedó duplicada entre el módulo nuevo y `evm.ts` / `dashboard.ts`, **reportarlo con la tabla comparativa** — el Agente B ya dejó documentada una duplicación equivalente entre `evm.ts` y `dashboard.ts`, y conviene no agregar una tercera en silencio.

## Decisión pendiente (para Victor, no bloquea el arranque)

**Proyección hacia el futuro (EAC dibujado sobre la curva).** Una Curva S de obra suele mostrar, además de lo ejecutado, hacia dónde va el proyecto si sigue el ritmo actual. Está **fuera de alcance de esta fase** a propósito: primero la curva real tiene que estar cuadrada y verificada. Cuando Victor quiera, se agrega como fase siguiente, con la línea proyectada claramente diferenciada de la real (trazo distinto y rótulo), nunca confundible con dato ejecutado.

## Decisiones y convenciones acordadas durante la ejecución

*(El agente escribe aquí, conforme ocurren, las decisiones nuevas tomadas con Victor.)*

## Mejoras a flujos

Ver tarea D9.
