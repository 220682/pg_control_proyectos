# 10 — Consolidado de servicio
> Lee si: la tarea toca el Consolidado de servicio (antes PR), de dónde sale cada número del sistema, sus bloques, cuándo se recalcula, o su relación con el Dashboard y las demás pantallas.

Origen: orden de Victor del 2026-11-05 («todo el sistema se alimenta del consolidado»). El antiguo PR **deja de existir** como pantalla, nombre y concepto: lo que era el PR es ahora el Consolidado de servicio. Antecedentes: Spec `2026-08-16-pr`, [PR Fase 1](../02-trabajo-activo/01-planes/2026-09-21-pr-fase-1-pipeline-rdt.md) y [PR Fase 2](../02-trabajo-activo/01-planes/2026-09-21-pr-fase-2-pipeline-linea-base.md); plan de este cambio: [consolidado como fuente única](../02-trabajo-activo/01-planes/2026-11-05-consolidado-fuente-unica.md).

## Regla central

```text
Presupuesto + Cronograma → DP → CONSOLIDADO ← RDT validados
                                   ↓
        Dashboard · Portafolio · Informes · Curva S · Valorización · Status · descargas
```

- **Victor solo sube el presupuesto y el cronograma, y solo revisa el DP** (quién es directo o indirecto, que las HH y los costos cuadren, tarifas de personal y equipos: «Revisión del DP», [flujo 9](09-importar-dp.md)).
- **El DP extrae el presupuesto y convierte a HH** (1 MES = 8 × 26 = 208 HH), al importar y en un solo lugar. Ninguna otra pantalla convierte.
- **El Plan Maestro** toma las partidas del presupuesto y sus fechas; no agrega nada más. Desde el 2026-11-05 **no se crean paquetes ni transversales nuevas por costumbre**: los servicios que ya los tienen siguen funcionando ([flujo 20](20-plan-maestro.md)).
- **El RDT no crea nada:** cargos, tarifa y si es directo o indirecto salen del DP ([flujo 6](06-rdt.md)). Solo el RDT **validado** entra al Consolidado.
- **El Consolidado reúne lo contractual del DP y lo de campo de los RDT, y crea todas las métricas.** Ninguna interfaz calcula: todas leen de la misma lectura (`src/lib/consolidado/leer.ts`, `leerConsolidado`), que devuelve la misma cifra a todas. Si una interfaz necesita algo que el Consolidado no tiene (por ejemplo fechas), va al Plan Maestro.
- **Si un dato no existe, el sistema dice que no existe.** Nunca lo inventa: «Pendiente», «No existe», o «Todavía no existe el Consolidado de este servicio».
- **Detalle por día o por periodo:** el Consolidado guarda acumulados. El detalle por fecha (informes diarios y semanales, real por día del Plan Maestro, matriz «Consolidado RDTs», metrado por periodo de Valorización) se lee de los mismos RDT validados y suma lo mismo que el acumulado.

Un candado automático (`src/lib/consolidado/frontera.test.ts`) hace fallar las pruebas si una pantalla vuelve a leer por su cuenta las tablas internas. Esas tablas conservan su nombre técnico (`pr_partidas`, `pr_recursos`, `proyecto_pr`, `pr_subcontrato_medicion`): renombrarlas exige SQL a mano y no cambia nada visible; solo `src/lib/consolidado/` las toca.

**Botón «Recalcular» + barra de progreso (O1, Victor 2026-10-02):** la pantalla muestra el botón (solo Admin y Jefe Proyectos) con una barra de progreso (`<progress>`) durante el recálculo. El Consolidado se recalcula solo al validar un RDT; el botón permite forzarlo. Endpoint: `POST /api/proyectos/[id]/consolidado/recalcular`. Permiso: `puedeRecalcularConsolidado`. La pantalla es `/proyectos/[id]/consolidado`; `/proyectos/[id]/pr` redirige ahí para no romper enlaces y avisos guardados.

**Cuadre visible (Victor, 2026-11-05):** arriba de la pantalla sale, solo si existe, lo que no cuadra: HH de las partidas contra HH de los cargos, costo de las partidas contra costo de los recursos (tolerancia 1) y recursos sin tarifa. Lo muestra, nunca lo corrige. Lo mismo se avisa a administrador y jefe de proyectos al importar el presupuesto (evento `dp.sin_cuadrar`).

**Cargos y equipos:** tabla con una sola fila por cargo o equipo (por nombre normalizado: `PEON` y `PEON.` son uno), en HH o HM ya convertidas; un cargo que viene en HH y en MES a la vez no duplica sus horas acumuladas (`src/lib/consolidado/recursos.ts`).

## Qué es el Consolidado

El Consolidado es la tabla que consolida todo lo que alimenta al Dashboard: una sola fila por partida (`pr_partidas`), más una cabecera por proyecto (`proyecto_pr`). No es la fuente original del alcance ni del cronograma — es la capa de consolidación entre plan y real.

Regla de oro: lo que cambia cuando ocurre un hecho (se importa un DP, se aprueba un Plan Maestro, se valida un RDT) **se materializa** (el pipeline lo escribe en una columna); lo que depende de la fecha de corte o es derivación pura (PV, EV, CPI, SPI, PPC…) **se calcula al leer**.

## Tres bloques

```text
A. CONTRACTUAL (DP)  |  A'. PLANIFICADO (PLAN MAESTRO)  |  B. CAMPO (RDT VALIDADOS)  |  C. MÉTRICAS
```

### A — Línea base contractual

Origen: DP, hoja CD (costo directo, regla 9 de [18-control-avance.md](18-control-avance.md)). Se llena en `reemplazar_dp()` al importar el DP.

- `hh_contractual` = `hh_und_partida × metrado_contractual`.
- `bac` = `metrado_contractual × precio_unitario`, en USD.

### A' — Planificado

Origen: Plan Maestro aprobado y Cronograma. Se recalcula cuando se aprueba una versión nueva del Plan Maestro (la anterior pasa a `REEMPLAZADO`, sin dejar rastro en el Consolidado).

- `metrado_planificado_acum`: suma de `plan_maestro_asignaciones` de la versión `APROBADO`, por partida. **La suma es por partida aunque esté repartida en varios paquetes** (y/o como directa): todas las líneas de la partida se suman (fórmula sin cambio).
- `fecha_inicio_base` / `fecha_fin_base`: desde `cronograma_actividad_partidas` — inicio es la fecha más temprana de las actividades vinculadas a la partida, fin la más tardía. Se recalculan cuando cambia el vínculo cronograma ↔ partida. **El vínculo con metrado se declara en Paquetes** ([flujo 19](19-paquetes-de-trabajo-y-jerarquia-de-control.md)), no en el Cronograma.

PV **no se almacena** aquí — depende de la fecha de corte y se calcula al leer (bloque C).

### B — Ejecución real

Origen: RDT validado. Toda actividad (D, C y NC) se carga a una partida (regla 12 de negocio), dentro de un paquete × partida del Plan Maestro aprobado — solo las D generan metrado ejecutado; C y NC aportan horas y costo, no avance.

**El Consolidado suma por partida.** El real por paquete × partida vive solo en el Plan Maestro ([flujo 20](20-plan-maestro.md)); el real por partida (la suma de lo declarado en todos sus paquetes) es lo que alimenta al Consolidado. **Las filas derivadas** del modo «por avance del paquete» ([flujo 06](06-rdt.md)) se guardan como actividades propias de su partida: el motor del Consolidado (`recalcular_pr_desde_rdt`, `db/053`) **no cambia**, no hay doble conteo de metrado ni de horas, y **cada derivada cuenta como una actividad D más en `actividades_acum`**, por lo que también entra en el PPC (decisión de Victor).

- `metrado_acumulado`, `hh_reales_acum`, `hh_d_acum`, `hh_c_acum`, `hh_nc_acum`, `hh_transversal_acum` (solo en la fila de una partida transversal, informativa), `hm_reales_acum`, `costo_real_acum`, `actividades_acum`, `actividades_con_cnc_acum`.
- A nivel proyecto (`proyecto_pr`): `hh_mo_indirecta_acum` (MOI, horas sin costo — regla 10 de negocio), el balde `*_legacy_sin_partida_acum` (solo RDT anteriores a la regla 12, que no se pueden reasignar retroactivamente) y, desde la migración `102`, `costo_materiales_acum` y `costo_subcontratos_acum` (ver «Costo real (AC)» abajo).

#### Costo real (AC): todo suma (Victor, 2026-10-15)

**Regla de costo real (reemplaza la de septiembre «materiales y subcontratos no suman al costo real»):** *si se gasta plata en algo, es costo real.* El AC del servicio es la suma de cuatro partes, todas costo directo en US$:

| Parte | Cuenta |
|---|---|
| Mano de obra | HH del RDT × tarifa congelada. Las **HH extra** (las que el supervisor marca por persona en el RDT, [flujo 06](06-rdt.md)) valen **tarifa × 1,25**; el recargo se reparte entre las actividades de la persona en proporción a sus horas. Las HH de MOI siguen sin valorizarse (regla 10). |
| Equipos | (HM operativas + **HM stand-by**) × tarifa del equipo. **El equipo no lleva partida (Victor, 2026-10-21):** su costo suma al AC del servicio pero no se reparte por partida; va al balde `costo_legacy_sin_partida_acum`, que reúne equipos y actividades sin partida (RDT anteriores a la regla 12). Los RDT históricos con WBS de equipo siguen repartidos por partida. |
| Materiales | Presupuesto del material × % de avance físico del servicio. |
| Subcontratos | **Por avance físico** (por defecto): contractual × % de avance físico. **Con ingreso manual** (Reporte del proyecto, [flujo 11](11-dashboard.md)): el monto ingresado, que es su costo real. |

* **Qué no cambia:** las HH reales, el IP, el EV, el PV y el BAC. Lo que cambia es solo el AC (y con él CV, CPI, EAC y VAC).
* **Se calcula a nivel servicio.** Los materiales y subcontratos no se pueden ligar a una partida (`pr_recursos` y `dp_recursos` no tienen partida), así que entran al AC del **servicio** y **no** al `costo_real_acum` de cada partida. El Consolidado lo muestra como una fila «Materiales y subcontratos (sin partida)», una fila **«Equipos (sin partida)»** al pie de la tabla (el balde `costo_legacy_sin_partida_acum`, visible solo si es distinto de cero) y una franja de desglose sobre el pie (Personal, Equipos, Materiales, Subcontratos y «Sin resolver»; con partidas transversales aprobadas esa diferencia se rotula **«Transversales (prorrata)»**, Victor 2026-10-21, igual que en el Dashboard).
* **Avance físico para esta cuenta** = EV / BAC **sin tope** en 100 % (`Σ pr_partidas.bac` como BAC). Si el BAC del Consolidado y el que suma el Dashboard (`calcularBac`, desde los recursos) difirieran, el % saldría distinto según la pantalla: no se midió diferencia con una base real y queda anotado como pendiente de comprobar.
* **En la Curva S** el subcontrato con ingreso manual entra con su monto **desde el día (Lima) de su último cambio**; antes de ese día vale lo que daba el avance físico. Las series de la Curva S usan la función `ac_materiales_subcontratos_al_corte` (`db/102`).
* **Mismo AC en todas partes:** Consolidado, Dashboard (pantalla, PDF y Excel), Curva S e informe de Costos dan el mismo AC. Los servicios que existían antes de la migración `102` guardan en 0 las dos columnas nuevas hasta que se recalcula su Consolidado («Recalcular Consolidado» por servicio): al aplicar la `102` hay que recalcular el Consolidado de los servicios existentes.
* **Seguridad:** la función SQL de la Curva S no se expone por RPC a `anon` ni a `authenticated`; las rutas validan sesión, rol y alcance en servidor y luego leen con el cliente de servicio.

#### Partidas transversales (Victor, 2026-10-19; `db/111` y `db/112`)

Una **partida transversal** ocurre durante todo el servicio (p. ej. movilización de personal). Se marca en Paquetes ([flujo 19](19-paquetes-de-trabajo-y-jerarquia-de-control.md)), no se declara en el RDT y rige desde la **versión del Plan Maestro que la aprueba** ([flujo 20](20-plan-maestro.md)). Su fila en `pr_partidas` es **calculada y de solo lectura**: la escribe `recalcular_pr_desde_rdt` y nada la edita a mano. Con `p` = **% físico del resto del servicio**, sin las transversales (`EV del resto / BAC del resto`; así no se define a sí mismo):

| Dato de la transversal | Cuenta |
|---|---|
| EV (`metrado_acumulado`) | `BAC × p` (metrado contractual × `p`) |
| PV | `BAC × PV % del resto` al corte (se calcula con asignaciones sintéticas por fecha) |
| HM | las del APU × `p` |
| HH | las del APU × `p`, **solo informativas** (`hh_transversal_acum`, `db/116`): no entran a `hh_reales_acum` ni a las HH ganadas ni al IP (Victor, 2026-10-21) |
| Costo real | **(mano de obra + equipo del APU) × `p`** |

* **Sus materiales y subcontratos no se suman aparte, para no contarlos dos veces:** `pr_recursos` es del servicio (ya incluye los de la transversal) y el AC de materiales y subcontratos es «todo × avance físico»; con las transversales dentro del EV, ese avance total es exactamente `p`. Así el AC no declara de más ni de menos.
* **Para separar mano de obra y equipo por partida**, al importar el DP se guarda la composición de cada partida (`dp_partida_costos`, [flujo 09](09-importar-dp.md)). Un DP importado antes no la tiene: hay que **reimportar el DP** antes de marcar o aprobar transversales (la app lo avisa).
* **HH de transversales (Victor, 2026-10-21; `db/116`, por aplicar):** las HH de la transversal no entran a las HH reales, ni a las HH ganadas, ni al IP, con la misma regla en los dos lados (si no, el IP mezclaría un lado con y otro sin). Se guardan aparte en `pr_partidas.hh_transversal_acum` y se muestran como «HH de transversales (informativas)» (nota del Consolidado, tarjeta IP del Dashboard y resumen del Excel). El metrado de la transversal **sí suma al EV**. `hh_d_acum` y `hh_reales_acum` de la fila de la transversal quedan en 0. Las HH programadas del Plan Maestro **sí** incluyen la transversal (Victor, 2026-10-21; [flujo 20](20-plan-maestro.md)). **Pendiente de decisión (no es regla):** si `hm_legacy_sin_partida_acum` (HM de equipos sin partida) debe entrar a HH/IP, hoy no entra.
* **Una transversal ignora el RDT:** no tiene actividades ni metrado ni vínculos, y cualquier dato de RDT que tuviera la partida antes de marcarse no cuenta.
* **Sin transversales aprobadas nada cambia** (el resultado es idéntico al anterior). Suman a EV, PV y AC (sus HH solo como información, ver abajo), en Dashboard, Curva S, informes y Consolidado.
* **Limitación conocida:** el «Costo real de recursos» por recurso (mano de obra y equipo) sigue saliendo del RDT y no incluye la parte de las transversales; el total del AC sí.
* **C/NC no tienen relación** con las transversales (siguen como están, flujo 06).

### C — Derivados EVM

No se almacena. Se calcula al leer en `src/lib/pr/evm.ts` — funciones puras sobre las columnas de A/A'/B. Reutiliza lo que ya existe en `src/lib/dashboard/dashboard.ts` (PV al corte, SV, SPI, CPI, EAC, IP) sin modificarlo.

| Indicador | Fórmula |
|---|---|
| BAC | `metrado_contractual × precio_unitario` (partida) · suma (proyecto). Costo directo |
| PV al corte | `Σ metrado_planificado × PU` hasta la fecha de corte. "Pendiente" sin Plan Maestro aprobado |
| % avance físico | `metrado_acumulado / metrado_contractual` |
| EV | `metrado_acumulado × precio_unitario` — no sale del dinero gastado |
| AC | `costo_real_acum` (partida: solo personal y equipos) · proyecto: suma + balde legacy + materiales + subcontratos (ver «Costo real (AC)»). Costo directo |
| % trabajo productivo | `hh_d_acum / hh_reales_acum` |
| SV / CV | `EV − PV` · `EV − AC` |
| SPI / CPI | `EV / PV` · `EV / AC` |
| HH ganadas | `% avance físico × hh_contractual`, sin la parte de las partidas transversales (`db/116`) |
| IP | `HH ganadas / HH reales` (ambas sin las HH de las transversales, que se muestran aparte) |
| EAC / VAC | `BAC / CPI` · `BAC − EAC` |
| Metrado restante | `contractual − acumulado`, con alerta si sale negativo (sobre-ejecución) |
| HH restantes | `hh_contractual − hh_reales_acum` |
| Rendimiento real vs base | `metrado ejecutado / HH reales` contra `hh_und_partida` |
| PPC | `(actividades_acum − actividades_con_cnc_acum) / actividades_acum × 100`, a nivel proyecto |

Todo indicador se rotula con nombre, fórmula y unidad — nunca solo la sigla. PPC y SPI se muestran separados, nunca mezclados (regla de [18-control-avance.md](18-control-avance.md)). Sin dato suficiente (ej. denominador en 0, sin Plan Maestro aprobado), el indicador muestra "Pendiente", nunca 0 ni un número inventado.

## Pipeline: cuándo se recalcula cada bloque

| Bloque | Se dispara desde | Función |
|---|---|---|
| A | Importar DP | `reemplazar_dp()` (extendida en `db/060`) |
| A' — planificado | Aprobar Plan Maestro | `recalcular_pr_planificado()` (`db/061`) |
| A' — fechas base | Guardar vínculo Cronograma ↔ DP (automático o manual) | `recalcular_pr_fechas_base()` (`db/062`) |
| B | Validar/corregir/rechazar/borrar un RDT, reimportar un DP o aprobar un Plan Maestro | `recalcular_pr_desde_rdt()` (`db/053`; con transversales, `db/112`; HH de transversales aparte, `db/116`) — de recálculo completo, no incremental |

Reimportar un DP borra y reconstruye el Consolidado contractual (`delete from proyecto_pr` + insert); para no perder la ejecución real acumulada, `reemplazar_dp()` llama a `recalcular_pr_desde_rdt()` al final, así el lado real se reconstruye desde los RDT ya validados en la misma transacción.

## Pantalla

`src/app/(workspace)/proyectos/[id]/consolidado/page.tsx`. Tabla larga con scroll horizontal, columnas de identificación de partida (WBS, descripción, unidad) fijas a la izquierda, encabezado de dos filas (grupo de bloque + columna) sticky en la celda. Fila de total del proyecto al pie — el total físico va como N/A (no se suman unidades físicas incompatibles entre partidas) y la variación global se expresa en valor económico. Fecha de corte siempre visible. Diseño según `docs/05-diseno-y-referencias/design.md`.

**Subcontratos (Victor, 2026-11-05; reemplaza la sección del 2026-10-15):** la casilla para medir el subcontrato a mano **desaparece**. El contrato se llena a mano en Valorización ([flujo 28](28-valorizacion.md)) y el costo real sale del avance del servicio o de lo que Logística declare en el registro de costos.

## Relación con Dashboard

El Dashboard lee las mismas columnas que este flujo llena (incluido el AC con materiales y subcontratos, con el mismo cálculo que la pantalla del Consolidado) — no necesita cambios de código para reflejar datos reales; el semáforo, antes en `PENDIENTE` por falta de dato (AC = 0), toma color real en cuanto el Consolidado se llena.
