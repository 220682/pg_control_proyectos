# Informe de Auditoría — Observaciones de Victor, Lote 3 (Enmienda E1)

> Auditoría emitida antes del Gate 2. El plan solo enlaza a este archivo; este archivo no se edita desde el plan.
> Modo del Auditor: **solo lectura** sobre ambos repositorios. Lo único que este informe escribe es este archivo.

## Alcance auditado

Plan `docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-lote-3-plan.md`, Enmienda E1 («el Plan Maestro es el umbral»), reglas U1–U10, tareas R1–R6b (nueve tandas), libro de hallazgos (17 mejoras, 9 reglas, 13 observaciones) y registro de decisiones.

El Auditor verificó, con herramientas y no de memoria:

1. Que el reposicionamiento **no pueda** tocar los datos del RDT ni las cifras del PR (acl. de U4, 2026-10-04).
2. Que la atomicidad de U8 sea real (migración `093` + `src/app/api/plan-maestro/route.ts`).
3. Que las cuatro reglas de R4a sigan **sin resolver** y el Worker no las haya cerrado por su cuenta.
4. Que las nueve tandas estén cerradas de verdad en código y en documentación.
5. Que lo escrito en los flujos 06, 14, 15, 19 y 20 se corresponda con el código.
6. Que la evidencia no sobrevalore lo verificado (OP9, las cuatro reglas abiertas).

## Material revisado

- Plan, progreso (`02-progreso/2026-10-02-observaciones-victor-lote-3.md`) y evidencia (`03-evidencia/2026-10-02-observaciones-victor-lote-3.md`) homónimos.
- Resultados de tanda: `resultados/R1.md`, `R2-R3.md`, `R4a.md`, `R5.md`, `R6a.md`, `R6b.md`, `N.md`.
- Código, worktree `local-worker-4` HEAD `d7d96fd`: `db/093_aprobar_plan_maestro_reposicion.sql`, `src/app/api/plan-maestro/route.ts`, `src/lib/rdts/reposicionamiento.ts`, `reposicionamiento-servidor.ts`, `reposicionamiento.test.ts`, `reposicionamiento-sql.test.ts`, `src/app/api/plan-maestro/plan-maestro-api.test.ts`, `src/app/api/paquetes-trabajo/route.ts` y `vinculos/route.ts`, `src/app/api/rdts/route.ts`, `src/app/api/rdts/partes/route.ts`, `src/app/api/rdts/partes/[id]/route.ts`, `src/lib/rdts/real-por-clave.ts`, `declaracion-paquete.ts`, `historial.ts`, `src/app/api/rdts/consolidado/route.ts`, y las migraciones `040`, `061`, `053`, `082`, `083`, `084`.
- Flujos `06-rdt.md`, `14-accesos-y-restricciones.md`, `15-cronograma.md`, `19-paquetes-de-trabajo-y-jerarquia-de-control.md`, `20-plan-maestro.md` y su `README.md` (diff no commiteado).
- `docs/00-estandar-agentes/02-roles-y-delegacion.md` (rol del Auditor y del Documentador) y `06-plantillas/06-informe-auditoria.md`.

**Comprobado con herramienta:** `git log`/`worktree list`/`branch`/`show --stat` en `py_control_proyectos_web`; `git status` y `git diff` en `pg_control_proyectos`; lectura de los archivos citados; `Select-String` sobre `src` y `docs`; `python scripts/verificar-referencias.py`.

**NO comprobado (y se declara):** la base de datos. No hay conexión ni credenciales en esta sesión, así que **no se verificó** que la migración `093` esté aplicada, ni los conteos antes/después, ni el CHECK ampliado, ni la existencia de `aprobar_plan_maestro_con_reposicionamiento` y de `recalcular_pr_planificado`. Todo eso se toma del registro de la tanda R4b (evidencia §3), no de una comprobación propia. Tampoco se probó en vivo ninguna ruta de la Enmienda E1.

## Verificación de rama

```
main                        cd10882  [origin/main]
local-worker-4              d7d96fd
origin/local-worker-4       (no existe)
worktrees: .worktrees/local-worker-4 -> d7d96fd
git status --short --branch -> ## main...origin/main   (limpio)
```

Los ocho commits de hoy están en `local-worker-4`, **no en `main`**, y la rama **no existe en el remoto**:

| Commit | Hora | Tanda |
|---|---|---|
| `ceb269e` | 2026-10-04 00:12 | R1 |
| `d916716` | 2026-10-04 00:33 | R2 |
| `74734d7` | 2026-10-04 00:33 | R3 |
| `26288bf` | 2026-10-04 08:03 | R6a |
| `9d033e3` | 2026-10-04 08:20 | R6b |
| `11804b6` | 2026-10-04 08:36 | R4a (migración `093`) |
| `56c66e0` | 2026-10-04 08:37 | R4a (módulo y pruebas) |
| `d7d96fd` | 2026-10-04 08:37 | R4a (ruta e historial) |

`git show --stat` de los ocho coincide con lo que el plan y la evidencia declaran (tamaños y archivos). El worktree está limpio: la deuda del cambio sucio en `FormularioPlanMaestro.tsx` que el plan registra está realmente resuelta.

**Chats de Worker separados:** existen siete resultados de cierre, uno por tanda (`resultados/R1.md`, `R2-R3.md`, `R4a.md`, `R5.md`, `R6a.md`, `R6b.md`, `N.md`) y el plan registra que las cinco últimas corrieron con `opencode run --agent build --model opencode-go/deepseek-v4.1-flash`. Eso es evidencia de sesión separada, no un chat con nombre en opencode (el estándar no lo exige). **No verificado:** los títulos reales de sesión en la base de opencode; el progreso dice que el costo por tanda no está desglosado (correcto).

## Cumplimiento de SDD, plan, Punch List y evidencia

| Tanda | Declarado | Verificado por el Auditor | Veredicto |
|---|---|---|---|
| R1 | `ceb269e`, 8 archivos, +4/−608 | Los 4 archivos borrados **no existen**; `puedeEditarActividadCronograma`, `NotificacionImpacto` y `EditarActividadCronograma` tienen **0 apariciones** en `src`; el `PATCH /api/cronograma/actividades/[id]` y el `impacto/` están borrados | **Cerrada de verdad** |
| R2 | `d916716` | Guardia `planMaestroAprobado` en `POST` (línea 211) y en `PATCH` (312) **antes de cualquier escritura**, y en `vinculos/route.ts:48` | **Cerrada** |
| R3 | `74734d7` | `rdts/partes/route.ts:191` (plan) y `:204` (estado `EJECUCION`) antes de insertar; mensajes y `codigo` nominales | **Cerrada** |
| R4a | `11804b6`, `56c66e0`, `d7d96fd` | Módulo puro, servidor, 3 pruebas y migración `093` presentes; la ruta llama **una sola vez** a la función | **Cerrada en código**, pero con los defectos de este informe (§1 y §2) |
| R4b | Migración aplicada 08:41 | **No verificado** (sin acceso a la base). Consistente con lo escrito | **Aceptado por registro** |
| R5 | `resultados/R5.md` | Los seis documentos sí contienen lo que R5 dice (ver §5). Dos filas del libro no se trasladaron y una afirmación de la fila de estado es inexacta | **Cerrada con observación** |
| R5b | «Flujos 06, 19 y 20» | U10 está escrita **solo en el flujo 19**; el flujo 20 §6 no nombra `MOVER` y el flujo 06 no lo menciona | **Parcial** |
| R6a | `26288bf` | Guardia de las dos condiciones en `rdts/route.ts:133-157`, **antes** de `storage.upload` (163) y del `insert` (171) | **Cerrada** |
| R6b | `9d033e3` | La excepción `accion !== 'MOVER'` desapareció; la guarda (312) va **antes** de `moverPaquete` (318) | **Cerrada** |

**Las nueve tareas de código están en el código.** Los dos huecos no son de código: una regla aprobada que no existe (U6, §1) y la segunda mitad de U9 sin guardia (§2).

### 1. Verificación prioritaria — el reposicionamiento no toca los datos del RDT ni las cifras del PR

**Resultado: la garantía se sostiene en lo sustancial, pero el lenguaje con que se afirma es más fuerte que lo que hace el código.**

Lo que sí se comprobó, siguiendo todos los caminos:

- **El `payload` jsonb solo puede cambiar la asociación de paquete.** En `db/093` hay exactamente tres sentencias de escritura: dos `UPDATE` que hacen `set paquete_trabajo_id` (`rdt_actividad_partidas` filtrando por `rdt_actividad_id` **y** `dp_partida_id`; `rdt_actividades` por `id`) y un `INSERT` en `rdt_partes_historial`. De los seis campos del payload, la función solo lee `paqueteNuevo` para escribir; `parteId` y las claves solo van al `snapshot`. No hay forma de que ese `payload` alcance `metrado_ejecutado`, `metrado_derivado`, horas, `estado_validacion` ni `rdt_partes`. La función tampoco contiene `delete`, `drop` ni `truncate` (verificado leyendo el archivo, y también por `reposicionamiento-sql.test.ts`).
- **El `payload` no viene del navegador.** `PATCH` acepta solo `accion`, `planId`, `asignaciones`, `disciplinas` y `declaraciones`; el payload lo arma `aprobarPlanMaestroConReposicionamiento` con lecturas del propio servicio (`eq('proyecto_id', proyectoId)`). No hay superficie de ataque externa.
- **El PR no se mueve.** El motor del PR (`db/053`) agrupa el real de los RDT por `dp_partidas.wbs` a través de `rdt_actividad_partidas.dp_partida_id` y **no lee `paquete_trabajo_id`**. `recalcular_pr_planificado` (`db/061`) solo reescribe `pr_partidas.metrado_planificado_acum` desde `plan_maestro_asignaciones` del plan `APROBADO`. El consolidado (`rdts/consolidado/route.ts`) usa `paquete_trabajo_id` solo para construir filtros y etiquetas por WBS (`construirPaquetesConsolidado`), sin cifras.
- **El显示 en el Plan Maestro sí cambia, como se pretendía:** `real-por-clave.ts:58` construye la clave con `v.paqueteId ?? a.paqueteId`, así que al cambiar la asociación el real cae en la línea del plan vigente.

**Lo que hay que corregir antes del Gate 2 (importante, porque es el punto que Victor más cuidado puso):**

- El plan (flujo 20, §3) y el progreso dicen, sin matiz, que el reposicionamiento **«no cambia los datos del RDT»**. Escribes `rdt_actividades.paquete_trabajo_id` y `rdt_actividad_partidas.paquete_trabajo_id`, que son datos del RDT y que **se muestran en el propio RDT**: `rdts/partes/[id]/route.ts:114` los devuelve como `paquetesActividades` y `:122` como `paqueteId` de las filas derivadas, y el Status de RDTs los usa para la columna «Paquete». Al aprobar un Plan Maestro nuevo, un RDT registrado puede ** verse con otro paquete en su propia pantalla y en el Status, no solo en el Plan Maestro. No es un defecto de datos (no hay tabla de unión; la clave de reporte *es* `paquete × partida`), pero la frase escrita es incorrecta y debe decir exactamente qué campo cambia y dónde se ve.
- **Riesgo real no registrado (y el más grave de este punto).** `db/093` actualiza `rdt_actividades` con `where a.id = (c->>'actividadId')::uuid` alimentado por `jsonb_array_elements`. Si una actividad tiene **dos o más vínculos** (`rdt_actividad_partidas` tiene PK `(rdt_actividad_id, dp_partida_id)`, así que sí puede tenerlos: declarada + derivadas, `db/083`) y el plan nuevo los reparte en paquetes distintos, el payload trae dos entradas con el mismo `actividadId` y PostgreSQL elige **una arbitrariamente**. Combinado con el fallback `v.paqueteId ?? a.paqueteId` de `claveReporte`, un vínculo que pasa a **DIRECTA** (su `paqueteNuevo` queda en `null`) puede calcular su clave con el paquete que el POST带有 arbitrariamente dejó en la actividad: el real de ese RDT aparecería en la línea de otro paquete. No está en el libro de hallazgos, no tiene prueba y no se ha visto en vivo. No es una vía para tocar `metrado_ejecutado`, pero sí es una vía para **descolocar el real** — justo lo que U4 vino a corregir.
- **`sinLinea` se descarta en silencio.** `calcularReposicionamiento` clasifica en `sinLinea` los RDT cuya partida no está en el plan o que son ambiguos, y la ruta **solo pasa `resultado.cambios`** al RPC y **nunca usa `resultado`**. Los casos «sin línea» y «ambiguo» no dejan fila de historial, no salen en la respuesta (la ruta devuelve `{ ok: true }`) y no aparecen en ningún log. El propio test `reposicionamiento.test.ts:87` dice «queda sin linea (con historial)», y ese historial nunca llega a la base.

### 2. Verificación prioritaria — atomicidad de U8

**Real.** Comprobado:

- `aprobar_plan_maestro_con_reposicionamiento` es una función PL/pgSQL: sus tres pasos (marcar `REEMPLAZADO`, marcar `APROBADO`, reposicionar, insertar historial y `perform recalcular_pr_planificado`) corren en la transacción del llamador. Si algo falla, el `raise exception` y el error del RPC la revierten.
- `PATCH … accion: 'APROBAR'` (línea 583) hace **una sola** llamada a esa función y, si falla, devuelve 400 sin haber escrito nada por esa vía (prueba `plan-maestro-api.test.ts:286`). No queda ninguna llamada suelta: `grep` de `estado: 'APROBADO'`/`REEMPLAZADO` sobre `src` no encuentra ninguna otra escritura del estado del Plan Maestro fuera de la función.
- El `for update` del plan y del plan anterior, y el filtro `ppm.estado = 'APROBADO'` de `recalcular_pr_planificado`, garantizan que el recálculo use solo el plan nuevo.

**Matices que no rompen U8 pero conviene registrar:** las escrituras de `disciplinas` y `declaraciones` del mismo `PATCH` ocurren **fuera** de la transacción (líneas 445-488) cuando vienen en la misma petición; son ediciones del borrador, no de la aprobación, así que no violan U8, pero conviene que el plan lo diga si alguien lee «todo o nada» en sentido amplio. Y `v_cambios` cuenta entradas del payload, no cambios efectivos: un payload con entradas que no emparejan nada informaría «cambios: N» sin haber movido nada.

### 3. Verificación prioritaria — las cuatro reglas de R4a

**Siguen sin resolver, y el Worker no las cerró por su cuenta.** Verificado en `reposicionamiento.ts`: una partida ausente del plan → `sinLinea` con motivo y `continue` (líneas 114-123); una partida en dos líneas con paquetes distintos → `sinLinea` «paquete ambiguo» y `continue` (124-133); las filas derivadas cambian de clave **sin** recalcular `metrado_derivado` (no hay código que lo haga); el porcentaje de avance no se recalcula en ningún punto. Las pruebas de `reposicionamiento.test.ts:87` y `:97` documentan los dos primeros casos como no resueltos, no como resueltos. Ninguna de las cuatro aparece como cerrada en el plan, en el progreso ni en los flujos; el flujo 06 las declara «pendientes de decisión». **Es el comportamiento correcto del Worker.**

### 4. Verificación prioritaria — las cuatro filas del libro que nunca llegaron

El **segundo chequeo que el rol del Auditor exige** (`02-roles-y-delegacion.md` § Auditor: «verificar que las mejoras de trabajo, reglas de negocio y archivos/carpetas huérfanos encontrados durante la sesión estén en los apartados obligatorios del plan») **no pasa**. Al cotejar los siete resúmenes de cierre con el libro, hay **doce hallazgos de tres tandas que nunca se pasaron al plan**, todos escritos en los resultados y ninguno en el libro:

| Resumen | Hallazgo no registrado |
|---|---|
| `R1.md` | Verificar en vivo por API + SSR + **Playwright** para una tabla que se arma en `useEffect` |
| `R1.md` | `planMaestroAprobado` es subcadena de `hayPlanMaestroAprobado`: grep con falsos positivos |
| `R2-R3.md` | El criterio «Plan Maestro aprobado» ya vivía en **tres** sitios distintos; conviene un único helper |
| `R4a.md` | En cada aprobación el servidor **relee todos los RDT del servicio** (lotes de 200) para calcular el diff |
| `R4a.md` | `_protocolo-migraciones.md` dice que el Worker aplica las migraciones de su rango y el brief de R4a se lo prohíbe: el protocolo y el brief se contradicen |
| `R4a.md` | U8 exige «todo o nada» y la aprobación **no era** transaccional: conviene un ítem de revisión que prohíba llamadas sueltas en flujos de aprobación |
| `R5.md` | Buscar una regla derogada por palabra suelta (`impacto`) da falsos positivos: hay que buscar por símbolo o ruta |
| `R5.md` | **Regla de negocio:** G-R2 y V-R1 quedan superadas por U2/U3 y deben pasarse a «Descartada» |
| `R5.md` | **Regla de negocio:** U9 no estaba en el mapeo de R5 (la carga por archivo no estaba en el flujo 06) |
| `R5.md` | La política no dice si un registro histórico de cambio se conserva o se reescribe al derogarse una regla (R5 lo reescribió) |
| `R5.md` | `impacto` es término prohibido en la verificación del brief y a la vez el nombre del concepto vigente U6 |
| `R6a.md` | **Regla de negocio:** los RDT por archivo ya existentes en servicios fuera de `EJECUCION` no se migran ni se ocultan |

El plan nombra como regla del rol del Orquestador «pasar a él, fila por fila y en el momento, lo que cada Worker deja en su resumen de cierre». No ocurrió para R1, R2-R3, R4a y R5. **Tres de esas filas son reglas de negocio** y una de ellas (R5-R2) es la que pide cerrar como «Descartada» lo que este informe ya clasifica abajo.

### 5. Verificación prioritaria — flujos contra código

| Lo escrito | Código | Veredicto |
|---|---|---|
| Flujo 14: se retira la fila de «Editar actividad del cronograma con PM aprobado» y su nota 11 | Fila y nota borradas; permiso y endpoints eliminados | **Coincide** |
| Flujo 14: matriz de permisos | La fila de «Gestionar paquetes de trabajo» sigue describiendo «mover partidas» como acción vigente (línea 110) | **Correcto** (la acción existe; lo que se congeló es *cuándo* se puede, y eso está en el flujo 19). Falta registrar que el **artefacto «Matriz de permisos»** sigue mostrando la acción retirada del cronograma y no refleja el congelamiento de `MOVER` |
| Flujo 15: con PM aprobado el cronograma queda congelado | No hay ruta de edición; la recarga sigue bloqueada | **Coincide** |
| Flujo 19: no crear, editar, archivar **ni reordenar** (`MOVER`), ni declarar vínculos | `POST`, `PATCH` (las tres acciones) y `PUT` de vínculos, todos con guarda antes de escribir | **Coincide** |
| Flujo 06 / 20: el RDT exige PM aprobado **y** servicio en Ejecución, en toda vía de creación | Correcto en `rdts/partes/route.ts` (estructurado) y `rdts/route.ts` (archivo) | **Coincide en esas dos; falta la tercera** (§2) |
| Flujo 20: **aviso de impacto antes de confirmar (U6)**, con cuántos RDT y con qué fechas y metrados | **No existe.** `grep` de `impacto|previsual|preview|simular` en `src/components/plan-maestro` y `src/app/api/plan-maestro`: 0 coincidencias. El único componente es `LienzoPlanMaestro.tsx` | **NO COINCIDE — es el hallazgo más grave** |
| Flujo 06: el historial registra «qué se movió, por qué, **a qué fecha y a qué metrado**, y quién aprobó» | El `snapshot` guarda `parte`, `planAnteriorId`, `planNuevoId`, `planVersion` y el diff de **claves**. **No guarda ninguna fecha ni ningún metrado** | **NO COINCIDE** |
| Flujo 20: la aprobación es atómica (U8) | Una función SQL | **Coincide** |
| Flujo 20 §6: qué queda congelado | DP, cronograma, PR, paquetes (crear/editar/archivar/vínculos). **No menciona `MOVER`**, que sí congela el flujo 19 (U10) | **Incompleto** |

### 6. Verificación prioritaria — la evidencia no sobrevalora

- **OP9 está bien tratado.** La evidencia tiene una sección titulada «Verificación en vivo: la que NO hay», el progreso lo repite en «Deuda que sigue abierta» y el handoff al Auditor dice «no lo des por cierto». La Enmienda E1 **no** puede declararse verificada en la app y no se declara. Correcto.
- **Las cuatro reglas de R4a están marcadas «Pendiente de decisión (Victor)»** en el plan, listadas en los pendientes del progreso y en el plan de este informe. Correcto.
- **Tres exageraciones o huecos, sí:**
  1. «El reposicionamiento **no toca los datos del RDT** ni el PR» (progreso, «Avances terminados»): es falso tal como está escrito; lo que no toca es el metrado, las horas, el estado y las cifras del PR. Ver §1.
  2. La fila **R5b** dice «Flujos 06, 19 y 20» para U10; U10 solo está en el 19.
  3. La tabla de evidencia deja `tsc` y tests en «—» para R1 y R2, aunque `resultados/R1.md` (exit 0, 1075 tests) y `resultados/R2-R3.md` (exit 0, 1079) sí los tienen. Hueco, no exceso.
- La evidencia de R4b (conteos, CHECK, firma de la función, `COMMIT ok`) **no se pudo comprobar** y así queda dicho arriba.

## Clasificación de hallazgos

Las 39 filas del libro (17 mejoras, 9 reglas, 13 observaciones), una línea cada una.

### Mejoras (de trabajo) — 17

| ID | Estado | Justificación |
|---|---|---|
| G-M1 | **Registrada** | Poner la ruta de credenciales y el puerto en el brief: no está en `03-aprendizaje-continuo/` ni en la base de briefs. Se puede cerrar con una línea. |
| G-M2 | **Registrada** | Llamada viva mínima antes de integrar endpoints ajenos: no escrita; el aprendizaje más cercano (`2026-10-01-pruebas-de-api-con-base-simulada.md`) no la contiene. |
| V-M1 | **Registrada** | Los dos defectos de `verificar.ps1` **están corregidos** (`53dbee9`), pero la lección («un control que no vigila es peor que no tenerlo») no se escribió en ninguna parte. |
| V-M2 | **Trasladada** | La metodología del benchmark ya está en `docs/03-aprendizaje-continuo/2026-10-04-opencode-run-modelo-por-invocacion-y-niveles.md` §5, con la conclusión de que con n=1 no se ordena por latencia. |
| V-M3 | **Registrada** | Los fixtures deben replicar la derivación exacta de rutas del script: no escrita. Hermana de OP5; conviene cerrar las dos juntas. |
| V-M4 | **Registrada** | El acento grave como carácter de escape en PS 5.1: el destino propuesto es `2026-10-02-entorno-windows…md` §3, y ese §3 habla de UTF-8 y de `node -e`, **no** del acento grave. |
| V-M5 | **Trasladada** | La fuente real de medición es la tabla `session` de la base de opencode: materializado en `scripts/niveles-modelos.py` y en `10-niveles-de-modelos.md`. Lo que falta es la ruta y el nombre de la tabla, que solo están en el archivo de evidencia. |
| M-M1 | **Registrada** | El nombre real de la tabla es `disciplinas`, no `catalogo_disciplinas`: no se trasladó a aprendizaje continuo; es una línea en el README de `db/`. |
| E-M1 | **Registrada** | El login sin navegador con `createServerClient` + `cookieStore` tipo `Map` y la cookie de sesión completa serializada **no está** en `2026-10-02-entorno-windows…md` §2, que solo describe el password grant y el troceado a 3180. E-M1 es precisamente la parte que faltaba. |
| E-M2 | **Registrada** | `npm run dev -- --webpack -p <puerto>` en un worktree, y «arranca el propio, no reutilices el de otra sesión»: no está en el archivo §1 (que trata de `next build`) ni en `03-entorno-git-y-worktrees.md`. |
| E-M3 | **Trasladada** | «Una llamada que devuelve HTML es fallo de sesión, no del endpoint» ya está escrito en `2026-10-02-entorno-windows-worktrees-y-evidencia-sin-navegador.md` §2, párrafo «Trampa» (texto anterior a este hallazgo: la fila se cerró por duplicado, no por nuevo aporte). |
| F-M1 | **Registrada** | «Promover E-M1 antes de la siguiente tanda que necesite verificación en vivo»: no se promovió, y la consecuencia se materializó — R4a, R6a y R6b nunca tuvieron verificación en vivo. |
| R4a-M1 | **Trasladada** | El re-vínculo por clave de reporte y la ausencia de tabla de unión están en la cabecera de `db/093` (líneas 4-6 y 20-26), en `reposicionamiento.ts` y en los flujos 06 y 20. No se usó el destino propuesto (`03-aprendizaje-continuo/`), pero el contenido está donde un lector lo encuentra. |
| R4a-M2 | **Trasladada** | «La regla vive en TS y la aplicación en SQL, con el payload jsonb de unión» está en la cabecera de `db/093` y en `reposicionamiento-servidor.ts`. Mismo matiz: no llegó a `03-aprendizaje-continuo/`. |
| R4a-M3 | **Registrada** | Verificado: `src/lib/rdts/historial.ts` sigue con `accion: 'CORRECCION' \| 'VALIDAR' \| 'RECHAZAR' \| 'REPOSICIONAMIENTO'` — **sin `BORRADO`**, que sí existe en el CHECK de la base desde `db/053`. Deuda técnica de tipos, no resuelta. |
| R6a-M1 | **Registrada** | Verificado: `briefs/R6a.md:32` **sigue citando** `src/app/api/rdts/partes/partes-paquetes.test.ts`, que no existe. Corrección de una línea, pendiente del Documentador. |
| R6a-M2 | **Registrada** | Los dos helpers (`planMaestroAprobado` y `cargarPlanAprobado`) siguen existiendo y duplicando el criterio; no hay nota que diga cuál usar. Backlog de refactor menor. |

### Reglas de negocio — 9

| ID | Estado | Justificación |
|---|---|---|
| G-R1 | **Descartada** | El conteo de partes por el endpoint de impacto desaparece con la función (E1-D3); `resultados/R5.md` lo confirma y el endpoint está borrado del repo. |
| G-R2 | **Descartada** | La edición individual con permiso y su aviso de impacto quedan superados por U2/U3: la acción ya no existe en el código (verificado). |
| V-R1 | **Descartada** | Mismo motivo que G-R1: el aviso que contar solo validados ya no existe (E1-D3). |
| F-R1 | **Trasladada** | Declaración por paquete (`PQ-001`), partidas directas y libertad de WBS para C/NC, equipos y materiales **ya están escritos** en `06-rdt.md` § «Crear RDT con el Plan Maestro»; la fila nunca se cerró. |
| F-R2 | **Trasladada** | El catálogo de 8 disciplinas está escrito en `06-rdt.md` § «Disciplinas», con la referencia a la migración `090`. Fila nunca cerrada. |
| R4a-R1 | **Pendiente de decisión (Victor)** | Verificado en código: el RDT cuya partida no está en el plan queda `sinLinea` y no se reasocia. Sin regla escrita. |
| R4a-R2 | **Pendiente de decisión (Victor)** | Verificado: la partida en dos líneas con paquetes distintos se marca ambigua y no se reposiciona; falta el desempate. |
| R4a-R3 | **Pendiente de decisión (Victor)** | Verificado: las filas derivadas cambian de paquete sin recalcular `metrado_derivado`; la inconsistencia del conjunto derivado está sin regla. |
| R4a-R4 | **Pendiente de decisión (Victor)** | Verificado: no hay ningún punto del código que recalcule el porcentaje de avance tras reposicionar. |

### Observaciones sobre la política — 13

| ID | Estado | Justificación |
|---|---|---|
| G-O1 | **Pendiente de decisión (Victor, Gate 2)** | «Conforme» sin llamada viva se repetiría: R4a, R6a y R6b se cerraron sin verificación en vivo. La regla solo se aplicó a R1 y R3. Recomiendo que el criterio sea explícito en el estándar (ver «APLICAR AHORA»). |
| G-O2 | **Registrada** | `crearClienteServidor` escribiendo sobre tablas con RLS de solo lectura, con `message` vacío: el diagnóstico sigue siendo el mismo y no hay nota nueva. Lo clasifico **NO PROMOVER** con una recomendación de checklist. |
| OP1 | **Pendiente de decisión (Victor)** | Verificado: `qwen3.8-plus` **sigue** en `09-orquestacion-y-modelos.md:32`, `10-niveles-de-modelos.md:105` y `01-contexto-repositorio/09-medicion-y-modelos.md:35`. Los tres sitios都需要 corrección y el propio plan dice que no la edita un agente. |
| OP2 | **Pendiente de decisión (Victor, Gate 2)** | Sin Spec/SDD ni Gate Spec, con el mensaje de cierre escrito antes del Auditor. El plan ya lo marca como borrador anticipado; el estándar sigue sin decir qué hacer con un plan aprobado sin Spec. |
| OP3 | **Pendiente de decisión (Victor, Gate 2)** | Verificado que el conflicto sigue: `04-flujo-sdd-y-planes.md:76` asigna 16a al Orquestador, `02-roles-y-delegacion.md:66` se lo prohíbe y `:172` se lo da al Worker git, y `09-orquestacion-y-modelos.md:202` dice que el merge no requiere aprobación de Victor. Cuatro enunciados, tres dueños. |
| OP4 | **Registrada** | `09-orquestacion-y-modelos.md` trata el verificador como control obligatorio mientras `07-verificador-de-acciones.md` lo deja en borrador por probar: la contradicción sigue. |
| OP5 | **Registrada** | El estándar no exige probar con un fixture las rutinas que leen `docs/`; agrupar con V-M3 y resolver en el mismo Gate. |
| OP6 | **Registrada** | `verificar.ps1` sigue derivando `04-auditoria/` con dos `Split-Path -Parent` sin validar que el plan viva bajo `01-planes/`. No se corrigió en la Tanda V (que corrigió otros dos defectos). |
| OP7 | **Registrada (la fila dice «Resuelta» y no del todo)** | Verificado: `.opencode/config.json` **no existe** en el repo de código, así que la mitad del repo está resuelta; pero el progreso (pendiente 5) dice que `agent.roles` sigue nombrando `qwen3.8-plus` en los dos archivos, y las tablas del estándar lo publican. **Corregir el estado de la fila** o resolver lo que falta. |
| OP8 | **Descartada** | Resuelta por la Enmienda E1: el disparador único es la aprobación de un Plan Maestro nuevo (U4), escrito en el plan, en el flujo 06 y en el flujo 20. |
| OP9 | **Registrada** | Sigue vigente: no hay servicio de prueba con Plan Maestro en BORRADOR. Es la razón de que el reposicionamiento no se haya probado en vivo. **No la resuelve este plan.** |
| R4b-O1 | **Trasladada** | El corte por directorio externo está escrito en `2026-10-04-opencode-run-modelo-por-invocacion-y-niveles.md` §4, con el workaround del brief y la regla de que las credenciales las aplica el Orquestador. Falta recogerlo en `10-niveles-de-modelos.md` § Política 3 (destino propuesto). |
| R5b-O1 | **Registrada** | El Worker de R5b se cayó por un comando propio y la tarea la hizo el Orquestador: no hay ninguna regla escrita sobre qué hacer cuando un Worker falla en su primer comando. |

**Además, cuatro hallazgos que no están en el libro y que este informe deja registrados para que el Documentador los pase** (ver §4): R1-M1, R1-M2, R2-R3-M1, R4a-M1 (rendimiento), R4a-O1, R4a-O2, R5-M1, R5-R2, R5-R3, R5-O1, R5-O2, R6a-R1. Tres son reglas de negocio.

### Resumen de la clasificación

| Categoría | Trasladada | Descartada | Pendiente de decisión | Registrada |
|---|---|---|---|---|
| Mejoras (17) | 4 | 0 | 0 | 13 |
| Reglas (9) | 2 | 3 | 4 | 0 |
| Observaciones (13) | 1 | 1 | 4 | 7 |

**Ninguna fila queda en `Registrada` por ignorancia:** las 20 que quedan registradas están ahí porque su destino no se escribió, y el mecanismo que las iba a escribir (el Documentador) lo hizo parcialmente (una de 39). Eso es en sí un hallazgo de proceso, no 20 pendientes sueltos.

## Verificación de la revisión de fuentes de verdad por fase

- **Fase F6 (documentación de flujos)**: revisada arriba (§5). Correcta en 14, 15, 19 y en lo esencial de 06 y 20; tres afirmaciones no se corresponden con el código (U6, el rastro con fecha y metrado, y el congelamiento de `MOVER` que falta en §6 del flujo 20).
- **Fase R5 (documentación de U1–U8)**: el contenido de U1, U2, U3, U4, U5, U7 y U8 está en los flujos; U6 está escrita pero sin implementar; U10 está a medias (§5).
- **Fase R5b (precisiones)**: tres de las cuatro respuestas de Victor quedaron integradas (U4 aclarada, U9, U8 transaccional, U10 en el flujo 19). La cuarta, U10 en el flujo 20, falta.
- **Índice de `04-flujos-de-negocio/`**: la línea del Lote 3 existe y nombra los cinco flujos. Dice «en curso», lo cual es correcto antes del Gate 2.
- **`scripts/verificar-referencias.py`**: ejecutado por el Auditor → `Archivos revisados: 46` · `HUÉRFANOS (0)` · `ENLACES ROTOS (0)` · `EXIT=0`. Las dos «menciones sin archivo» son preexistentes y ajenas a este plan. **Este archivo no introduce huérfanos**: el plan ya lo enlaza.
- **Artefacto «Matriz de permisos»**: la política de `AGENTS.md` exige que toda acción o permiso eliminado actualice el artefacto en la misma tarea. El artefacto lo actualiza solo Victor y **no se pidió**. Es el punto que el Gate 2 debe resolver explícitamente.

## Pendientes técnicos y documentales

### APLICAR AHORA (confirmado, sin decisión de negocio)

1. **Corregir el lenguaje de lo escrito sobre lo que el reposicionamiento no cambia** (flujo 20 §3 y § «Qué ocurre al aprobar», flujo 06, progreso). Debe decir: no se reescriben el metrado ejecutado, los metrados derivados, las horas ni el estado de validación, y las cifras del PR consolidado no cambian; lo que **sí** cambia es la asociación de paquete del RDT (`rdt_actividades.paquete_trabajo_id` y `rdt_actividad_partidas.paquete_trabajo_id`), que es la clave de reporte y que **se ve en el propio formulario del RDT y en el Status**.
2. **Eliminar la fila duplicada malformada de la línea 336 del plan** (repite el contenido de G-O1 sin ID y sin `|` inicial). No estaba en `HEAD`: se introdujo hoy y rompe la tabla del libro; el conteo de `Registrada` del verificador puede leer esa fila como una fila más.
3. **Corregir la fila R5b** del plan: U10 quedó escrita en el flujo 19, no en 06, 19 y 20.
4. **Añadir el congelamiento de `MOVER` al §6 del flujo 20** para que la lista de datos congelados coincida con el flujo 19 y con `db`/`route.ts`.
5. **Añadir a `db/README.md` o a la cabecera de `db/093` la dependencia de versión**: la acción de aprobación **falla por completo** si la `093` no está aplicada en ese entorno (una base restaurada, otro ambiente). El progreso lo declara como riesgo, pero no quedó en la fila de la migración como advertencia de dependencia.
6. **Registrar el riesgo de `db/093` §(3) sobre `rdt_actividades`** (actualización no determinista cuando una actividad tiene varios vínculos que se reparten en paquetes distintos) en el libro de hallazgos y en el código, con la alternativa de agrupar el payload por actividad o de no escribir `rdt_actividades` cuando hay más de un paquete nuevo para la misma actividad.
7. **Decidir y escribir qué pasa con `sinLinea`**: hoy se calcula, se descarta y no deja rastro. O se devuelve en la respuesta y se muestra, o se registra en el historial del RDT, o se acepta explícitamente que esos RDT quedan fuera y sin rastro. Lo que no puede seguir es que la regla aprobada diga que quedan «sin resolver» sin que nada lo indique.

### PROPONER A RESPONSABLE (requiere decisión de Victor)

1. **U6 (aviso de impacto antes de aprobar)**: aprobarlo como implemented en la Enmienda E1 o sacarlo del flujo 20 y del plan como regla del futuro. Hoy está escrito como vigente y no existe. **Es la corrección de mayor peso.**
2. **U7 (historial con fecha y metrado)**: o se amplía el `snapshot` de `db/093` para incluir la fecha y el metrado nuevo de cada línea afectada, o se corrigen el flujo 06 y el plan para que prometan solo lo que se guarda (plan, versión, diff de claves, quién aprobó).
3. **Segunda mitad de U9**: «mover un RDT ya registrado se permite exigiendo las dos condiciones de U1». Hoy `rdts/partes/[id]/route.ts` exige Plan Maestro aprobado (líneas 228 y 301) pero **no** el servicio en Ejecución, en las dos rutas: `REASIGNAR_PAQUETE` y la de validar/corregir. Decidir si se añade la segunda condición (tanda nueva) o si U9 se reescribe para decir que la segunda condición aplica solo a la creación.
4. **Las cuatro reglas de R4a**, tal como están registradas.
5. **El artefacto «Matriz de permisos»**: actualizarla con la eliminación de la acción del cronograma y con el congelamiento de `MOVER`.
6. **OP1** (los tres sitios con `qwen3.8-plus`) y **OP3/OP4** (dueño de 16a y obligatoriedad del verificador): decisiones de estándar.
7. **F5 parcial** (libertad de WBS para C/NC, equipos y materiales) y **OP9**: para un plan futuro.

### NO PROMOVER (puntuales o no confirmados)

- **G-O2** (`crearClienteServidor` sobre RLS de solo lectura con `message` vacío): correcto y útil, pero no es una regla de política; basta una línea en el checklist de revisión de endpoints de escritura.
- **La fila OP7**: no promoverla como Resuelta hasta que se verifique qué queda en los dos archivos de configuración; hoy el estado de la fila y el pendiente 5 del progreso se contradicen.
- **R4a-M3** (`BORRADO` fuera del tipo TS): deuda técnica de tipos, no de política. Puede ir en el backlog del código.

### PROPONER SKILL (procedimiento reusable, agnóstico)

1. **«Auditar un payload que viaja de la aplicación a una función SQL»**: el método que siguió esta auditoría — leer la función y contar las sentencias de escritura, enumerar qué campos del payload se leen para escribir, preguntarse quién puede construir el payload y si viene del navegador, y seguir el consumidor de cada columna tocada hasta la fuente de verdad que alimenta. Se repitió en las tres corridas del benchmark de R4 y otra vez aquí.
2. **«Verificar en vivo o declarar el hueco»**: el patrón que evitó el falso «Conforme» de G-O1 —tsc y la suite con doble de Supabase no ven errores de esquema ni de sesión; si no hay datos que permitan la llamada, se dice en el resultado y en la evidencia, no se deduce.
3. **`opencode run --model` + medición por nivel** (ya escrito en `2026-10-04-opencode-run-modelo-por-invocacion-y-niveles.md` y promovible a Skill): candidato directo, con el caveat de que solo vale para el harness de opencode.

## Recomendación

**Requiere corrección mayor.**

El trabajo de código de las nueve tandas está bien hecho y es verificable: los ocho commits están en la rama del Worker y no en `main`, los símbolos derogados desaparecieron, las guardas están antes de cualquier escritura, la aprobación es una sola transacción y el `payload` no tiene ningún camino hacia `metrado_ejecutado`, las horas, el estado de validación o las cifras del PR. Las cuatro reglas de R4a están efectivamente sin resolver, que es lo correcto.

Lo impide cerrar son tres cosas, y ninguna es «un detalle de redacción»:

1. **Una regla que Victor aprobó y que está escrita como vigente en una fuente de verdad no existe en el código** (U6, el aviso de impacto antes de aprobar). El flujo 20 la describe dos veces y el plan no la registra como pendiente. Un plan no puede pasar el Gate 2 con una regla aprobada fantasma en la documentación.
2. **El segundo chequeo del Auditor no pasa**: doce hallazgos de cuatro resúmenes de cierre —tres de ellos reglas de negocio— nunca llegaron al libro de hallazgos, y una regla ya está superada sin marcarse como descartada. El estándar exige lo contrario.
3. **La garantía que Victor Ask clearestó con más cuidado está escrita más fuerte de lo que el código garantiza** (el reposicionamiento sí escribe datos del RDT y sí se ven en su propia pantalla), y en el mismo mecanismo hay un riesgo no registrado que puede **descolocar el real** de un RDT en el Plan Maestro, que es exactamente lo que U4 vino a arreglar.

Recomendación de secuencia: (a) el Orquestador cierra 1 y 2 con Victor antes deGate2; (b) el Documentador ejecuta «APLICAR AHORA» y vuelve a pasar las doce filas; (c) una tanda de código solo para lo que Victor decida de U6, U7 y U9, si decide que van ahora; (d) con eso, el Gate 2.

Pendientes que quedan después del Gate 2 aunque se apruebe el cierre: F5 parcial, OP9 (verificación en vivo del reposicionamiento), las cuatro reglas de R4a si Victor las difiere, y el artefacto «Matriz de permisos».