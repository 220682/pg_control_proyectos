# 10 — Generación PR
> Lee si: la tarea toca la generación del PR, sus tres bloques, cuándo se recalcula cada uno, o su relación con el Dashboard.


Independiente de importar DP (usa datos del DP, pero es otro flujo). Spec `2026-08-16-pr`, ampliado en PR Fase 1 ([2026-09-21-pr-fase-1-pipeline-rdt.md](../02-trabajo-activo/01-planes/2026-09-21-pr-fase-1-pipeline-rdt.md)) y PR Fase 2 ([2026-09-21-pr-fase-2-pipeline-linea-base.md](../02-trabajo-activo/01-planes/2026-09-21-pr-fase-2-pipeline-linea-base.md)).

**Botón "Recalcular PR" + barra de progreso (O1, Victor 2026-10-02):** la pantalla muestra un botón "Recalcular PR" (solo para Admin y Jefe Proyectos) con una barra de progreso (`<progress>`) durante el recálculo. El PR se recalcula automáticamente al validar RDT, pero este botón permite forzar el recálculo manual (útil después de cambios o para actualizar). Endpoint: `POST /api/proyectos/[id]/pr/recalcular`. Permiso: `puedeGestionarPr` (solo Admin y Jefe Proyectos).

## Qué es el PR

El PR es la tabla que consolida todo lo que alimenta al Dashboard: una sola fila por partida (`pr_partidas`), más una cabecera por proyecto (`proyecto_pr`). No es la fuente original del alcance ni del cronograma — es la capa de consolidación entre plan y real.

Regla de oro: lo que cambia cuando ocurre un hecho (se importa un DP, se aprueba un Plan Maestro, se valida un RDT) **se materializa** (el pipeline lo escribe en una columna); lo que depende de la fecha de corte o es derivación pura (PV, EV, CPI, SPI, PPC…) **se calcula al leer**.

## Tres bloques

```text
A. LÍNEA BASE (CONTRACTUAL — DP)  |  B. ACUMULADO REAL (RDT → PR)  |  C. DERIVADOS (EVM CALCULADO)
```

### A — Línea base contractual

Origen: DP, hoja CD (costo directo, regla 9 de [18-control-avance.md](18-control-avance.md)). Se llena en `reemplazar_dp()` al importar el DP.

- `hh_contractual` = `hh_und_partida × metrado_contractual`.
- `bac` = `metrado_contractual × precio_unitario`, en USD.

### A' — Planificado

Origen: Plan Maestro aprobado y Cronograma. Se recalcula cuando se aprueba una versión nueva del Plan Maestro (la anterior pasa a `REEMPLAZADO`, sin dejar rastro en el PR).

- `metrado_planificado_acum`: suma de `plan_maestro_asignaciones` de la versión `APROBADO`, por partida. **La suma es por partida aunque esté repartida en varios paquetes** (y/o como directa): todas las líneas de la partida se suman (fórmula sin cambio).
- `fecha_inicio_base` / `fecha_fin_base`: desde `cronograma_actividad_partidas` — inicio es la fecha más temprana de las actividades vinculadas a la partida, fin la más tardía. Se recalculan cuando cambia el vínculo cronograma ↔ partida. **El vínculo con metrado se declara en Paquetes** ([flujo 19](19-paquetes-de-trabajo-y-jerarquia-de-control.md)), no en el Cronograma.

PV **no se almacena** aquí — depende de la fecha de corte y se calcula al leer (bloque C).

### B — Ejecución real

Origen: RDT validado. Toda actividad (D, C y NC) se carga a una partida (regla 12 de negocio), dentro de un paquete × partida del Plan Maestro aprobado — solo las D generan metrado ejecutado; C y NC aportan horas y costo, no avance.

**El PR suma por partida.** El real por paquete × partida vive solo en el Plan Maestro ([flujo 20](20-plan-maestro.md)); el real por partida (la suma de lo declarado en todos sus paquetes) es lo que alimenta al PR. **Las filas derivadas** del modo «por avance del paquete» ([flujo 06](06-rdt.md)) se guardan como actividades propias de su partida: el motor del PR (`recalcular_pr_desde_rdt`, `db/053`) **no cambia**, no hay doble conteo de metrado ni de horas, y **cada derivada cuenta como una actividad D más en `actividades_acum`**, por lo que también entra en el PPC (decisión de Victor).

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
* **Se calcula a nivel servicio.** Los materiales y subcontratos no se pueden ligar a una partida (`pr_recursos` y `dp_recursos` no tienen partida), así que entran al AC del **servicio** y **no** al `costo_real_acum` de cada partida. El PR lo muestra como una fila «Materiales y subcontratos (sin partida)», una fila **«Equipos (sin partida)»** al pie de la tabla (el balde `costo_legacy_sin_partida_acum`, visible solo si es distinto de cero) y una franja de desglose sobre el pie (Personal, Equipos, Materiales, Subcontratos y «Sin resolver»; con partidas transversales aprobadas esa diferencia se rotula **«Transversales (prorrata)»**, Victor 2026-10-21, igual que en el Dashboard).
* **Avance físico para esta cuenta** = EV / BAC **sin tope** en 100 % (`Σ pr_partidas.bac` como BAC). Si el BAC del PR y el que suma el Dashboard (`calcularBac`, desde los recursos) difirieran, el % saldría distinto según la pantalla: no se midió diferencia con una base real y queda anotado como pendiente de comprobar.
* **En la Curva S** el subcontrato con ingreso manual entra con su monto **desde el día (Lima) de su último cambio**; antes de ese día vale lo que daba el avance físico. Las series de la Curva S usan la función `ac_materiales_subcontratos_al_corte` (`db/102`).
* **Mismo AC en todas partes:** PR, Dashboard (pantalla, PDF y Excel), Curva S e informe de Costos dan el mismo AC. Los servicios que existían antes de la migración `102` guardan en 0 las dos columnas nuevas hasta que se recalcula su PR («Recalcular PR» por servicio): al aplicar la `102` hay que recalcular el PR de los servicios existentes.
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
* **HH de transversales (Victor, 2026-10-21; `db/116`, por aplicar):** las HH de la transversal no entran a las HH reales, ni a las HH ganadas, ni al IP, con la misma regla en los dos lados (si no, el IP mezclaría un lado con y otro sin). Se guardan aparte en `pr_partidas.hh_transversal_acum` y se muestran como «HH de transversales (informativas)» (nota del PR, tarjeta IP del Dashboard y resumen del Excel). El metrado de la transversal **sí suma al EV**. `hh_d_acum` y `hh_reales_acum` de la fila de la transversal quedan en 0. **Pendiente de decisión (no es regla):** si las HH contractuales y las HH programadas del Plan Maestro también deben excluir la transversal; y si `hm_legacy_sin_partida_acum` (HM de equipos sin partida) debe entrar a HH/IP, hoy no entra.
* **Una transversal ignora el RDT:** no tiene actividades ni metrado ni vínculos, y cualquier dato de RDT que tuviera la partida antes de marcarse no cuenta.
* **Sin transversales aprobadas nada cambia** (el resultado es idéntico al anterior). Suman a EV, PV y AC (sus HH solo como información, ver abajo), en Dashboard, Curva S, informes y PR.
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

Reimportar un DP borra y reconstruye el PR contractual (`delete from proyecto_pr` + insert); para no perder la ejecución real acumulada, `reemplazar_dp()` llama a `recalcular_pr_desde_rdt()` al final, así el lado real se reconstruye desde los RDT ya validados en la misma transacción.

## Pantalla

`src/app/(workspace)/proyectos/[id]/pr/page.tsx`. Tabla larga con scroll horizontal, columnas de identificación de partida (WBS, descripción, unidad) fijas a la izquierda, encabezado de dos filas (grupo de bloque + columna) sticky en la celda. Fila de total del proyecto al pie — el total físico va como N/A (no se suman unidades físicas incompatibles entre partidas) y la variación global se expresa en valor económico. Fecha de corte siempre visible. Diseño según `docs/05-diseno-y-referencias/design.md`.

**Sección Subcontratos del Reporte del proyecto (Victor, 2026-10-15):** cada subcontrato del servicio tiene un selector de medición, **Por avance físico** (por defecto: acumulado = contractual × % de avance físico del servicio) o **Ingreso manual** (se escribe el monto acumulado y el sistema calcula el %: contractual 200, ingreso 40 → 20 %). Se ingresa aquí —no en «Recursos del servicio», que no muestra costos— y solo lo hacen los **5 roles con datos económicos** con el servicio asignado (`PUT /api/proyectos/[id]/pr/subcontratos`, migración `101`, tabla `pr_subcontrato_medicion`, que se guarda por servicio y descripción del subcontrato). El monto manual es el costo real del subcontrato y suma al AC (regla «Costo real (AC)»). Sin subcontratos, la sección dice «Este servicio no tiene subcontratos». El pie de la pantalla dice que el AC incluye materiales y subcontratos, no que se midan «por % de avance económico».

## Relación con Dashboard

El Dashboard lee las mismas columnas que este flujo llena (incluido el AC con materiales y subcontratos, con el mismo cálculo que la pantalla del PR) — no necesita cambios de código para reflejar datos reales; el semáforo, antes en `PENDIENTE` por falta de dato (AC = 0), toma color real en cuanto el PR se llena.
