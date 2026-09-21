# PR enriquecido — Fase 2 (Agente B): línea base, planificado y derivados EVM

**Estado (2026-09-21):** PLAN APROBADO por Victor. Migración `052` corrida en Supabase. **Lista para que el Agente B arranque la implementación.** Trabaja en paralelo con [Fase 1](2026-09-21-pr-fase-1-pipeline-rdt.md) (Agente A).

**Ya resuelto, no volver a preguntar:**
- Punch List de esta fase (15 ítems, tabla más abajo) — **aprobada por Victor.**
- `db/052_pr_enriquecido.sql` — **corrida en Supabase por Victor.** El contrato del PR ya existe: `pr_partidas` y `proyecto_pr` tienen todas las columnas del Paso 0.
- Credenciales de verificación en memoria (`cuentas-prueba.md`), reglas de negocio de costo/EVM (`reglas-costo-evm.md`), protocolo de verificación con Playwright (`protocolo-verificacion-agente.md`).

**Único punto que sigue pendiente de coordinar con el Agente A:** el orden de migraciones — la `053` de la Fase 1 va antes que la `060` de esta fase (ver B1, "reimportar un DP borra el PR").

## Ejecución en la nube (decidido 2026-09-21)

- **Cada agente trabaja en su propia rama** (no directo a `main`). Al llegar al 100% de su checklist de implementación, abre un **PR** para que Victor lo revise antes de mergear. Rama sugerida: `feat/pr-fase-2-linea-base-evm`.
- **Las migraciones se corren solas, sin pausar a confirmar cada una** — excepción puntual autorizada por Victor solo para esta tarea (ver `mejoras-futuras.md`, sección "Acceso directo a Postgres/Supabase"). El agente lee la cadena de conexión directa de Postgres de la variable de entorno **`PR_DB_URL`**, configurada por Victor en el entorno de `claude.ai/code` de este repositorio. **No es un secreto cifrado** — la documentación de Claude Code advierte que cualquiera con acceso a ese entorno puede leerla —, así que el riesgo aceptado es acotado a que hoy solo Victor tiene ese acceso. El agente nunca imprime el valor completo en su salida ni lo commitea.
- Credenciales de verificación (Playwright) en las variables **`PR_TEST_ADMIN_EMAIL`** / **`PR_TEST_ADMIN_PASSWORD`** (cuenta con permisos altos) y **`PR_TEST_USER_EMAIL`** / **`PR_TEST_USER_PASSWORD`** (cuenta sin permisos de administración), mismo entorno.
- Aun así, **cada migración queda documentada en su propio archivo `db/0NN_*.sql`, commiteada, y resumida en el PR** — la autonomía es sobre no pausar a pedir permiso, no sobre dejar de dejar rastro.
- Al terminar, el agente entrega en el PR: el checklist de implementación (B1–B10) marcado, la Punch List de 15 ítems con el resultado de cada uno verificado con Playwright, y el informe de limpieza.

## Contexto

El PR es la tabla que alimenta a todo el sistema. Hoy es una copia pobre del DP: `reemplazar_dp()` lo genera con las columnas contractuales y los acumulados en 0, y nada más lo vuelve a tocar.

Mientras el Agente A trae el dato **real** desde el RDT validado, esta fase trae al PR todo lo que falta desde **las demás interfaces** — empezando por el Plan Maestro, que es de donde sale el PV — y construye la capa de indicadores derivados (bloque C).

Diagnóstico completo del eslabón roto: ver el contexto de la [Fase 1](2026-09-21-pr-fase-1-pipeline-rdt.md).

## Reglas de negocio fijas (Victor)

Decididas y confirmadas. **No volver a preguntarlas — quedan escritas aquí.**

1. **El AC medido sale solo de HH y HM**, con tarifa congelada al validar el RDT.
2. **Todas las HH del RDT suman al costo real: D, C y NC.**
3. **Las HM de equipos declarados suman aunque el equipo no esté en el presupuesto contractual.**
4. Recurso sin costo en ninguna tabla: **avisar** a administrador y jefe de proyectos, **sin bloquear** nada.
5. **Materiales, subcontratos y todo lo que no sea HH ni HM se miden por % de avance económico (EV)**, no por costo capturado.
6. **El metrado programado del RDT es solo informativo.** No es PV y no entra a ningún cálculo.
7. **El CNC lo marca el supervisor según su criterio de campo**, en catálogo mantenible y obligatorio cuando hay incumplimiento.
8. **El PV sale del Plan Maestro, y el Plan Maestro es restrictivo: debe definir el PV del servicio desde el inicio. Sin Plan Maestro aprobado, el servicio no puede pasar a Ejecución.**
9. **El sistema calcula solo COSTO DIRECTO.** Por eso el DP extrae únicamente de la hoja **CD**. Gastos generales, utilidad y todo lo que no sea costo directo **no entran a ningún cálculo**. **BAC = costo directo.** AC también es costo directo, así ambos quedan en la misma base y el CPI es comparable.
10. **Las HH del personal indirecto (MOI) sí se acumulan como horas en el consolidado de RDTs**, pero **no se valorizan** (`tarifa_hh` NULL por diseño, EVM Fase 1). Horas sí, costo no.
11. **Todo el sistema trabaja en USD.** No hay multi-moneda.
12. **Toda actividad se carga a una partida: las D, las C y las NC.** Ninguna hora queda huérfana. La D trae su WBS; la C y la NC se asignan a una partida elegida de un desplegable con las partidas de las actividades D ya declaradas ese día, igual que los equipos. Lo implementa el Agente A en la Fase 1.

### Terminología — dos cosas distintas que NO se deben confundir

| Término | Qué es | Dónde vive |
|---|---|---|
| Actividad **Contributoria (C)** / **No Contributoria (NC)** | Categoría de la **ACTIVIDAD**: traslado, charla, espera. No genera metrado, pero **sí se carga a una partida** (regla 12). | `rdt_actividades.ta` |
| **Mano de obra indirecta (MOI)** | Categoría de la **PERSONA**: supervisor, ingeniero. No es un tipo de actividad. | `dp_moi` |

Son **ejes independientes**: una persona MOI puede declarar horas en actividades D, C o NC.

> **Regla de redacción: nunca llamar "indirectas" a las HH de actividades C/NC.** Se las nombra por su tipo — contributorias y no contributorias. **"Indirecto" queda reservado exclusivamente para MOI.**

Lo que C/NC sí cambian respecto de las D: **no generan metrado ejecutado**. Aportan horas y costo a la partida, no avance físico. De ahí sale el % de trabajo productivo que esta fase calcula.

## Alcance de esta fase

Traer al PR la línea base contractual (DP), lo planificado (Plan Maestro y Cronograma), y calcular los indicadores derivados. Más la pantalla del PR con los tres bloques.

## Fuera de alcance (explícito)

- **Dashboard — no se toca.** Ni el de proyecto, ni el rollup de portafolio, ni el Dashboard 2 "Completo".
- Curva S y serie temporal semanal (necesitan el histórico, van después).
- Pareto de CNC y cierre semanal auditado.
- 3WLA (pospuesto en `mejoras-futuras.md`).

> **Efecto esperado, no es cambio de alcance:** los dashboards existentes empezarán a mostrar números reales sin ser tocados, porque leen las mismas columnas que estas dos fases empiezan a llenar.

---

## Paso 0 — COMPARTIDO: definición del PR (se hace UNA sola vez)

**Idéntico en las dos fases. Se ejecuta una sola vez, antes de que los dos agentes empiecen en paralelo.** El PR queda definido como **una sola tabla de partidas** (`pr_partidas`), más la cabecera ya existente (`proyecto_pr`). Ningún agente inventa columnas por su cuenta.

Migración **`db/052_pr_enriquecido.sql`** — idempotente. La corre Victor en Supabase antes de arrancar.

```sql
-- BLOQUE A — Línea base contractual, COSTO DIRECTO (origen DP, hoja CD).  Llena: Agente B
alter table pr_partidas
  add column if not exists hh_contractual numeric,
  add column if not exists bac numeric;

-- BLOQUE A' — Planificado (origen Plan Maestro y Cronograma).             Llena: Agente B
alter table pr_partidas
  add column if not exists metrado_planificado_acum numeric not null default 0,
  add column if not exists fecha_inicio_base date,
  add column if not exists fecha_fin_base date;

-- BLOQUE B — Ejecución real (origen RDT validado).                        Llena: Agente A
-- metrado_acumulado ya existe (007_pr.sql) y ES el metrado ejecutado.
-- Regla 12: toda actividad (D, C y NC) se carga a una partida, así que el
-- desglose por tipo vive aquí, por partida, y no en un balde de proyecto.
-- Solo las D generan metrado; las C y NC aportan horas y costo, no avance.
alter table pr_partidas
  add column if not exists hh_reales_acum numeric not null default 0,
  add column if not exists hh_d_acum numeric not null default 0,
  add column if not exists hh_c_acum numeric not null default 0,
  add column if not exists hh_nc_acum numeric not null default 0,
  add column if not exists hm_reales_acum numeric not null default 0,
  add column if not exists costo_real_acum numeric not null default 0,
  add column if not exists actividades_acum int not null default 0,
  add column if not exists actividades_con_cnc_acum int not null default 0,
  add column if not exists recalculado_en timestamptz;

-- Nivel proyecto.                                                         Llena: Agente A
alter table proyecto_pr
  -- MOI: horas acumuladas, SIN costo a propósito (regla 10, no se valoriza).
  add column if not exists hh_mo_indirecta_acum numeric not null default 0,
  -- Balde SOLO para datos anteriores a la regla 12: RDT ya validados cuyas
  -- actividades C/NC o equipos quedaron sin partida y no se pueden reasignar
  -- retroactivamente. En partes nuevos esto queda en 0 y debe seguir en 0.
  add column if not exists hh_legacy_sin_partida_acum numeric not null default 0,
  add column if not exists hm_legacy_sin_partida_acum numeric not null default 0,
  add column if not exists costo_legacy_sin_partida_acum numeric not null default 0,
  add column if not exists recursos_sin_tarifa jsonb not null default '[]'::jsonb,
  add column if not exists recalculado_en timestamptz;
```

**Bloque C (derivados EVM) no se almacena.** Se calcula al leer, en `src/lib/pr/evm.ts` — lo construye esta fase.

Regla de oro del PR, para los dos agentes:

| Qué | Cómo |
|---|---|
| Cambia cuando ocurre un hecho (se importa un DP, se valida un RDT) | **Se materializa**: el pipeline lo escribe en la columna |
| Depende de la fecha de corte o es derivación pura (PV, EV, CPI, SPI, PPC…) | **Se calcula al leer** |

---

## Tareas — Agente B

### B1. Pipeline DP → PR (bloque A)

Migración **`db/060_pr_linea_base_dp.sql`**. Extender `reemplazar_dp()` para que, al copiar DP → PR, llene también:

- `hh_contractual` = `hh_und_partida × metrado_contractual` (el campo `hh_und_partida` **ya existe** en `dp_partidas` y `pr_partidas`, es el "Rendimiento (HH/Und)").
- `bac` = `metrado_contractual × precio_unitario`, en USD.

⚠️ **Cuidado con `create or replace function`.** `reemplazar_dp()` ya se rompió una vez exactamente así: `028` y `029` la reescribieron sin incluir el bloque de PR que `007` le había agregado, y el PR dejó de generarse sin avisar (ver `030_recuperar_generacion_pr.sql`). Partir de la versión vigente completa — hoy `050_fix_reemplazar_dp.sql` — y agregar encima, nunca reconstruir de memoria.

⚠️ **Punto de choque con el Agente A — reimportar un DP borra el PR.** `reemplazar_dp()` hace `delete from proyecto_pr` y lo reconstruye con los acumulados en 0. Hoy eso no molesta porque no hay dato real que perder; **en cuanto el Agente A ponga su motor a funcionar, reimportar un DP borraría toda la ejecución real acumulada.**

Fix obligatorio: al final de `reemplazar_dp()`, después de reconstruir el PR contractual, **llamar a `recalcular_pr_desde_rdt(p_proyecto_id)`** (la función del Agente A, migración `053`). Como ese motor es de recálculo completo y no incremental, reconstruye el lado real desde los RDT validados y el PR vuelve a quedar entero. Por eso se diseñó así.

Esto obliga a un orden: **la `053` del Agente A se corre antes que la `060` de esta fase.** Si por lo que sea la `060` llega primero, envolver la llamada para que no falle si la función todavía no existe, y dejarlo anotado.

**Verificación de coherencia del BAC.** Regla 9: el sistema es de costo directo, el DP extrae solo de CD. Entonces estos dos números **deben coincidir**:

- `Σ (metrado_contractual × precio_unitario)` de `pr_partidas`
- `Σ pr_recursos.costo_contractual` (lo que hoy usa el dashboard como BAC)

Si no coinciden contra el presupuesto real **PS-065 Bancoductos**, no es una decisión de diseño: es un bug de extracción o de alcance del parser, y hay que encontrarlo. Documentar el resultado de esta comprobación con el número exacto de ambos lados.

### B2. Pipeline Plan Maestro → PR (bloque A')

- `metrado_planificado_acum` por partida, acumulado a la fecha de corte, desde `plan_maestro_asignaciones` del plan **APROBADO** (`proyecto_plan_maestro.estado = 'APROBADO'`).
- Se recalcula cuando se aprueba una versión nueva (al aprobar, la anterior pasa a `REEMPLAZADO`).
- El vínculo partida ↔ plan ya existe: `plan_maestro_partidas.dp_partida_id`.

**PV no se almacena** — depende de la fecha de corte y avanza cada día aunque no pase nada. Se calcula al leer en B5.

### B3. Pipeline Cronograma → PR

`fecha_inicio_base` y `fecha_fin_base` por partida, desde las actividades de cronograma vinculadas por la tabla puente `cronograma_actividad_partidas` (`db/039`): inicio = la fecha más temprana de sus actividades, fin = la más tardía.

Son las columnas "Inicio base", "Fin base" y "Duración" que `18-control-avance.md` pide como columnas fijas. Duración se deriva, no se almacena.

### B4. Plan Maestro restrictivo para pasar a Ejecución

Regla 8, pedido expreso de Victor. Los estados del proyecto son `EN_PLANEACION`, `EJECUCION`, `CERRADO` (`db/001_esquema.sql`).

- **Sin Plan Maestro en estado `APROBADO`, el proyecto no puede pasar de `EN_PLANEACION` a `EJECUCION`.**
- Validación **en servidor**, no solo en la interfaz (AGENTS.md: validar siempre en servidor).
- Mensaje claro explicando por qué está bloqueada la transición y qué falta.
- Quien confirma la transición sigue siendo el jefe de oficina técnica (flujo 14).

### B5. Bloque C — módulo de derivados `src/lib/pr/evm.ts`

Archivo nuevo, propiedad exclusiva de esta fase. Funciones puras sobre las columnas almacenadas. **Se puede importar y reutilizar `src/lib/dashboard/dashboard.ts`, pero no modificarlo** (el dashboard está fuera de alcance).

| Indicador | Fórmula (`18-control-avance.md`) |
|---|---|
| BAC | `metrado_contractual × precio_unitario` (partida) · suma (proyecto). **Costo directo** |
| PV al corte | `Σ metrado_planificado × PU` hasta la fecha de corte |
| % Avance físico | `metrado_acumulado / metrado_contractual` |
| EV | `% avance físico × BAC` — **no sale del dinero gastado** |
| AC | `costo_real_acum` (partida) · suma + balde legacy (proyecto). **Costo directo** |
| **% trabajo productivo** | `hh_d_acum / hh_reales_acum` — cuánto de las horas de la partida fue trabajo directo y cuánto contributorio o no contributorio (análisis LPS) |
| SV / CV | `EV − PV` · `EV − AC` |
| SPI / CPI | `EV / PV` · `EV / AC` |
| HH ganadas | `% avance físico × hh_contractual` |
| IP | `HH ganadas / HH reales` |
| EAC / VAC | `BAC / CPI` · `BAC − EAC` |
| Metrado restante | `contractual − acumulado`, **con alerta si sale negativo** (sobre-ejecución) |
| HH restantes | `hh_contractual − hh_reales_acum` |
| Rendimiento real vs base | `metrado ejecutado / HH reales` contra `hh_und_partida` |
| **PPC** | `(actividades_acum − actividades_con_cnc_acum) / actividades_acum × 100` |
| HH de MOI | Se muestran como **horas acumuladas**, nunca valorizadas (regla 10) |

Reglas de presentación, no negociables:

- **PPC y SPI se muestran separados y rotulados.** `18-control-avance.md`: "PPC y SPI miden cosas diferentes y no deben mezclarse".
- **Todo se rotula como costo directo** (regla 9), para que nadie lea el BAC como el monto total del contrato.
- **Cada indicador lleva nombre, fórmula y unidad**, no solo la sigla (el flujo 18 lo pide explícitamente para IP).
- Importes en **USD** (regla 11).
- Sin Plan Maestro aprobado no hay PV: los indicadores que dependen de él muestran **"Pendiente"**, nunca 0 ni un número inventado. Es el patrón que la app ya usa.

### B6. Pantalla del PR — tres bloques

`src/app/(workspace)/proyectos/[id]/pr/page.tsx`. Hoy muestra una tabla pobre. Pasa a los tres bloques de la estructura nueva:

```
A. LÍNEA BASE (CONTRACTUAL - DP) │ B. ACUMULADO REAL (RDT → PR) │ C. DERIVADOS (EVM CALCULADO)
```

- **Lectura obligatoria antes de tocar interfaz: [`docs/visual-companion/design.md`](../visual-companion/design.md)** (layout, tokens, columnas, accesibilidad, checklist de pre-vuelo). No es opcional.
- Tabla larga con scroll horizontal sin perder contexto, encabezado sticky **en la celda, nunca en la fila** (lección de la ronda 14 del sub-lote 1), columnas de identificación de la partida fijas a la izquierda.
- Fila de total del proyecto al pie. **No se suman unidades físicas incompatibles** — el total físico va como N/A y la variación global se expresa en valor económico.
- Fecha de corte visible: todo acumulado necesita decir a qué fecha está.

### B7. Actualizar los flujos (Victor ya lo autorizó)

Victor pidió expresamente dejar escritas estas reglas. Según `docs/README.md` el agente no edita flujos por su cuenta, pero **aquí ya está confirmado por él**, así que procede:

- `20-plan-maestro.md`: el Plan Maestro define el PV del servicio desde el inicio y es requisito restrictivo para pasar a Ejecución.
- `08-programa-portafolio-proyecto.md`: la transición a `EJECUCION` exige Plan Maestro aprobado.
- `18-control-avance.md`: las reglas 9, 10 y 11 (solo costo directo, MOI horas sin costo, USD) y la aclaración de terminología C/NC vs MOI.
- `10-generacion-pr.md`: hoy es un stub de dos líneas; pasa a describir el PR real de tres bloques.
- `14-accesos-y-restricciones.md`: registrar cualquier acceso nuevo.

### B8. Verificación

- `tsc --noEmit` limpio, `eslint` limpio, suite completa en verde, `next build` sin errores.
- Tests nuevos: cada fórmula del bloque C, el caso sin Plan Maestro (todo "Pendiente"), la alerta de sobre-ejecución, el bloqueo de transición a Ejecución.
- Migraciones aplicadas en Supabase por Victor, **con el SQL completo pegado en el mensaje**.
- Verificación funcional en la app real: ver el protocolo de abajo.

---

## Qué puede romperse

### Cambios de comportamiento esperados — no son fallas

1. **El semáforo del Dashboard pasa de PENDIENTE a color real.** Hoy `calcularCpi` devuelve `'Pendiente'` cuando AC = 0, así que **todos los servicios están en PENDIENTE**. Al llenarse el PR, el semáforo toma color. Umbral `peor < 0.85 → ROJO`. Es aritmética, no un bug.
2. El rollup de portafolio y el resumen ejecutivo cambian solos, sin tocarles el código.
3. **Proyectos en `EN_PLANEACION` sin Plan Maestro aprobado dejan de poder pasar a Ejecución.** Los que ya están en `EJECUCION` no se tocan — el bloqueo aplica a la transición, no retroactivamente. Conviene revisar antes cuántos servicios quedarían trabados.

### Riesgos reales de rotura

1. ⚠️ **`reemplazar_dp()` es la superficie más frágil del sistema.** Ya se rompió dos veces: `028` y `029` la reescribieron perdiendo el bloque de PR que había agregado `007`, y el PR dejó de generarse sin avisar hasta que `030` lo recuperó; después `050` arregló otro bug de la misma función. Partir **siempre** de la versión vigente completa y agregar encima. Al terminar, comprobar que importar un DP sigue generando el PR.
2. ⚠️ **Reimportar un DP borraría la ejecución real** si no se agrega la llamada a `recalcular_pr_desde_rdt()` al final (ver B1). Es el punto de choque con el Agente A.
3. **La pantalla PR funciona hoy y se reescribe entera.** Riesgo contenido pero real: hay que dejarla al menos tan usable como está.
4. **La suite de tests.** 409 tests pasando hoy. Que pasen todos es requisito de cierre.

## Protocolo de verificación y cierre (obligatorio)

Este es el ciclo de trabajo del agente. **No se salta ningún paso.**

1. **Antes de implementar — Victor aprueba el checklist.** El resultado esperado se define **antes** de escribir código, no después. Sin checklist aprobado, la implementación no arranca.
2. **Implementación** de las tareas B1 a B8.
3. **Autoverificación del agente con el MCP de Playwright.** Al terminar, el agente verifica **cada ítem del checklist en la app real, con login real** — no razonando sobre el código.
4. **El agente llena el checklist** con el resultado de cada ítem.
5. **Loop hasta cerrar.** Mientras quede un ítem que no esté en **Completado**, el agente corrige y vuelve a verificar. No se entrega con ítems abiertos.
6. **Fin del trabajo del agente:** cuando el 100% de los ítems está en Completado.
7. **Recién entonces Victor hace la revisión final.**

### Credenciales de verificación

Las dos cuentas están en la **memoria local del proyecto**, archivo `cuentas-prueba.md` (`C:\Users\BRANDY\.claude\projects\d--VICTOR-CLAUDE-CODE-pg-control-proyectos\memory\`). **Fuera del repositorio a propósito:** los dos repos están en GitHub y AGENTS.md prohíbe publicar credenciales, así que aquí se referencia la ubicación y nunca el valor.

Para esta fase hacen falta los dos perfiles: uno **administrador o jefe de proyectos** (aprueba el Plan Maestro, intenta la transición a Ejecución) y uno **sin permiso de Plan Maestro** (comprueba que el bloqueo se respeta también en servidor, no solo escondiendo el botón). Un permiso que solo se comprueba con la cuenta de admin no está comprobado.

---

## Informe de limpieza (entregable obligatorio al cerrar)

Al terminar, **antes de dar la fase por cerrada**, el agente entrega un informe de qué quedó viejo. Va escrito en este mismo archivo, en una sección `## Archivos y código que quedaron viejos`.

Qué se reporta:

| Tipo | Ejemplos |
|---|---|
| Archivos | Módulos, componentes o scripts que ya no usa nadie |
| Código dentro de un archivo | Funciones, constantes, tipos o props que quedaron sin referencias |
| Tests | Casos que prueban algo que ya no existe o que quedó reemplazado |
| Columnas de base de datos | Columnas que dejaron de leerse o escribirse |
| Documentación | Párrafos de flujos o de `Mejoras continuas` que quedaron contradichos |

Por cada ítem, cuatro datos: **qué es**, **por qué quedó viejo**, **qué lo reemplaza** y **quién más lo referencia hoy**.

Reglas:

- **El agente no borra nada.** Reporta y Victor decide (AGENTS.md: no eliminar archivos sin aprobación explícita).
- **Ninguna columna de base de datos se borra ni se renombra** sin un plan de migración aparte, aunque quede sin uso (AGENTS.md).
- Cada "esto quedó sin uso" se sostiene con una **búsqueda real de referencias en el código**, no de memoria.

Dos cosas que esta fase tiene que mirar sí o sí:

- **Duplicación entre `src/lib/pr/evm.ts` y `src/lib/dashboard/dashboard.ts`.** El módulo nuevo reutiliza funciones del viejo. Reportar qué quedó calculado en dos lados, aunque **no se toque `dashboard.ts`** (está fuera de alcance): es información que Victor necesita para decidir si más adelante se unifican.
- **La pantalla PR anterior.** Al reescribirla, reportar qué componentes o helpers de la versión vieja quedaron sin uso.

## Checklist de implementación — Agente B

- [ ] B0 · Migración `052_pr_enriquecido.sql` aplicada (compartida, una sola vez)
- [ ] B1 · `reemplazar_dp()` extendida en `060` con `hh_contractual` y `bac` + comprobación de coherencia del BAC documentada
- [ ] B2 · `metrado_planificado_acum` desde el Plan Maestro aprobado
- [ ] B3 · `fecha_inicio_base` / `fecha_fin_base` desde el cronograma vinculado
- [ ] B4 · Sin Plan Maestro aprobado no se pasa a Ejecución (validado en servidor)
- [ ] B5 · `src/lib/pr/evm.ts` con todos los indicadores del bloque C, PPC incluido
- [ ] B6 · Pantalla PR de tres bloques, siguiendo `design.md`
- [ ] B7 · Flujos 20, 08, 18, 10 y 14 actualizados
- [ ] B8 · tsc, eslint, tests y build limpios; migraciones aplicadas
- [ ] B9 · Autoverificación Playwright completa, checklist 100% Completado
- [ ] B10 · Informe de limpieza entregado: qué quedó viejo, con referencias comprobadas

## Punch List — checklist a aprobar ANTES de implementar

Se carga en la Punch List de Mejoras como checklist nuevo: **"PR Fase 2 — línea base, planificado y derivados EVM"**. **Victor lo aprueba antes de que arranque la implementación.** El agente lo llena con Playwright al terminar y hace loop hasta cerrarlo completo.

| # | Ítem | Resultado esperado |
|---|---|---|
| 1 | Importar un DP | El PR queda con HH contractual y BAC por partida |
| 2 | BAC total del PR | Cuadra con el costo directo del presupuesto PS-065; ambos números documentados |
| 3 | Servicio sin Plan Maestro aprobado | **No** puede pasar a Ejecución, y el mensaje dice por qué |
| 4 | Intentar la transición por URL directa, sin pasar por el botón | También se bloquea (validación en servidor) |
| 5 | Aprobar el Plan Maestro | Se llena el metrado planificado del PR |
| 6 | Aprobar una versión nueva del Plan Maestro | Actualiza el planificado, sin rastros de la anterior |
| 7 | Fechas base de cada partida | Coinciden con el cronograma vinculado |
| 8 | Pantalla PR | Muestra los tres bloques y se recorre en horizontal sin perder la partida de vista |
| 9 | Sin Plan Maestro | Los indicadores que dependen de PV dicen "Pendiente", no 0 |
| 10 | SPI y CPI | Coinciden con un caso calculado a mano |
| 11 | % de avance físico | Coincide con metrado ejecutado sobre contractual |
| 12 | Partida sobre-ejecutada | Levanta la alerta de metrado restante negativo |
| 13 | PPC y SPI | Se muestran separados, cada uno con su nombre y fórmula |
| 14 | Rótulos | Todo dice costo directo y USD; el AC indica su cobertura (HH y HM) |
| 15 | Fecha de corte | Visible, y los acumulados corresponden a ella |

## Coordinación con el Agente A

| | Agente B (esta fase) | Agente A (Fase 1) |
|---|---|---|
| **Migraciones** | `060`–`069` | `053`–`059` |
| **Escribe en el PR** | Bloque A y A' (contractual y planificado) | Bloque B (real) + nivel proyecto |
| **Archivos propios** | `src/lib/pr/evm.ts`, `src/lib/dp/**`, Plan Maestro, cronograma, `proyectos/[id]/pr/page.tsx` | `src/lib/pr/acumulacion-rdt.ts`, `src/lib/rdts/**`, `src/app/api/rdts/**`, `FormularioCrearRdt.tsx`, catálogo CNC |
| **No toca** | El motor de RDT, el catálogo CNC | La pantalla PR, `src/lib/pr/evm.ts` |

**Prohibido para los dos:** `src/app/proyectos/[id]/dashboard/page.tsx`, `src/lib/dashboard/dashboard.ts` y el rollup de portafolio.

**Cómo trabajan en paralelo sin bloquearse:** el contrato del PR está congelado en el Paso 0, así que esta fase escribe contra columnas cuya forma ya está definida aunque el Agente A todavía no las llene. Mientras el real esté en 0, los derivados que dependen de él se muestran "Pendiente" — el mismo patrón que ya usa la app. Ninguno de los dos espera al otro.

## Mejoras a flujos

Ver tarea B7 — las actualizaciones de flujo son parte del trabajo de esta fase, ya autorizadas por Victor.
