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
| Supervisor operativo a cargo (etiqueta bajo el encabezado) | ✓ | ✓ |
| KPI de avance físico (%), más grande y con barra ejecutado / programado / restante | ✓ | ✓ |
| IP y HH contractuales / acumuladas / restantes (no son dinero) | ✓ (tarjeta propia en la fila) | ✓ (fila propia «Productividad», bajo la dona y el desempeño) |
| Gráfica «Avance físico por nivel» y gráfica «Recursos: contractual · acumulado · restante» (barras por recurso, HH, HM, Mano de obra indirecta; Subcontratos y Materiales solo en Completo) | ✓ | ✓ |
| Descargar (PDF o Excel, con la Curva S) | ✓ (sin dinero) | ✓ |
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
abajo). El Parcial y el Completo la **enlazan**, nunca la embeben en pantalla (el archivo descargado sí la lleva, ver «Descargar»); desde el
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

- **Parcial:** % avance físico, **IP y HH** (contractuales, acumuladas y restantes: no son dinero, se ven en los dos modos).
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
panel de diagnóstico, Bloque E (PPC/Pareto), el enlace a la Curva S, y desde el
2026-10-15 el IP, las HH, las gráficas de avance por nivel y de recursos HH/HM, y
el botón Descargar (todo sin dinero). **Pantalla y archivo descargado usan el mismo
criterio de modo** (Completo solo si `tipo_dashboard` es COMPLETO y el rol tiene
economía): un rol con economía y `tipo_dashboard` = PARCIAL ve el Parcial en la
página igual que en el archivo. En el Parcial, la tarjeta de avance dice «Avance
físico ejecutado (RDT validados)» y no nombra BAC. La gráfica por nivel recibe del
servidor solo porcentajes por nodo (nunca pesos ni montos).

## Responsable operativo, IP y HH (Victor, 2026-10-15)

- **Supervisor operativo a cargo:** etiqueta justo bajo el encabezado del servicio, en el color de Supervisión operativa. Fuente única: el campo «Supervisor operativo a cargo» de Editar servicio ([flujo 08](08-programa-portafolio-proyecto.md)); **uno solo por servicio**. Sin asignar: «Sin supervisor a cargo».
- **IP y HH (rediseño 2026-10-23, ver «Rediseño de la pantalla»).** En Completo, una fila propia «Productividad» con dos tarjetas del mismo alto: **IP** (valor, HH ganadas y HH reales; con partidas transversales aprobadas, una línea «HH de transversales (informativas)») y **HH reales del servicio** (número grande = HH acumuladas, «de N contractuales», barra de consumo —roja si excede—, Consumo %, Restan o Exceso, y una línea «Aparte, informativas: transversales X · MOI Y»). Las tarjetas SPI y CPI **no** llevan cuadros adicionales. En Parcial, el IP y las HH tienen tarjeta propia en la misma fila del % avance.
- **% Avance físico** más grande y con barra: lo ejecutado en verde, una marca en lo programado al corte (Plan Maestro; sin Plan Maestro aprobado no hay marca) y el restante.
- **Matriz de partidas:** suma las columnas HH contractuales, HH acumuladas e IP por partida (sin dinero; también en Parcial). Con el rediseño de 2026-10-23 la matriz es compacta (12 columnas en Completo, 7 en Parcial) y cabe en el ancho útil sin cortar el IP.
- **HH de las partidas transversales (Victor, 2026-10-21; `db/116`).** Las HH de una partida transversal **no entran a las HH reales, ni a las HH ganadas, ni al IP** (la misma regla en los dos lados: si no, el IP mezclaría un lado con y otro sin). Se muestran aparte como **«HH de transversales (informativas)»**: en la tarjeta IP, en la nota del PR ([flujo 10](10-generacion-pr.md)) y en el resumen del Excel de la descarga. Su metrado **sí suma al EV**. En la fila de la transversal se ven sus HH, pero el total real del servicio no las suma (Plan Maestro, [flujo 20](20-plan-maestro.md)).

## Rediseño de la pantalla (Victor, 2026-10-23)

Pasada de orden y de interactividad sobre el Dashboard; **no cambia ninguna regla de cálculo ni de acceso** (no hay accesos nuevos: el flujo 14 y la Matriz de permisos no cambian).

- **Orden de arriba abajo (Completo):** franja de partida en revisión (si hay) → **Resumen ejecutivo** (banda de una fila, ya no al final) → botones **«Ir a»** (Indicadores, Costo, Avance por nivel, Recursos, Partidas, Diagnóstico, Costo real, PPC y CNC) → fila de indicadores (% avance de doble ancho, BAC, PV, EV, AC, SPI, CPI) → composición del costo + desempeño por partida → fila «Productividad» (IP y HH) → avance por nivel + recursos → matriz → diagnóstico → costo real de recursos → Bloque E. Todas las tarjetas de una fila tienen el mismo alto y el valor no se corta ni baja de línea.
- **SPI y CPI con semáforo:** franja de color arriba de la tarjeta (verde desde 0.95, ámbar de 0.85 a 0.95, rojo por debajo; los mismos cortes del resumen ejecutivo). % avance muestra «▲/▼ ±X pp vs. programado» cuando hay Plan Maestro aprobado. Los importes se escriben «US$ 1,758.45».
- **Detalle de cada tarjeta con listas:** al tocar una tarjeta, además del texto, se ven las filas que la explican (por subpresupuesto, por tipo de recurso, por cargo, las partidas más atrasadas o con menor CPI/IP, las causas de PPC). En Parcial las listas de dinero no se arman. Tocar una fila con partida la marca en revisión y lleva a la matriz.
- **HH reales del servicio (cuadre).** El detalle de la tarjeta de HH explica que la cifra **es la suma de las partidas**, la reparte por tipo de actividad (directas D, contributorias C y no contributorias NC), comprueba que **cuadra con la suma por cargo** y dice aparte —sin sumarlas a las HH reales— las HH de transversales y de mano de obra indirecta.
- **Composición del costo:** dona de tamaño fijo con el total al centro y leyenda a un costado con monto y % alineados. **Desempeño por partida** y **Pareto de CNC** son barras horizontales de texto constante (etiqueta, barra y valor; el Pareto muestra «conteo · %» y «acum. %»).
- **Avance por nivel:** programado en azul y real en verde (los mismos colores de la Curva S), eje con líneas guía en números redondos (20/40/60/80/100 %), valores sobre cada barra, un segundo selector **«Dentro de»** (todo el servicio o un grupo con hijos) y, al tocar una barra, una franja con sus valores, la diferencia en pp, **«Bajar un nivel»** y **«Ver sus partidas en la matriz»** (filtra la matriz por ese nivel).
- **Recursos:** una lista compacta (los 8 mayores y «Ver los N restantes»), con contractual en gris, acumulado en verde y exceso en rojo; clic en un cargo o equipo abre las partidas donde se usó.
- **Matriz de partidas:** columnas Metrado (acumulado arriba, «/ contractual unidad» debajo), % avance con barra, PV, EV, AC (importes sin decimales), SPI y CPI como insignias de color, HH contract., HH acum. e IP. «Sobre-ejecutada · restante X» va bajo la descripción. Encima de la tabla hay un **buscador** (partida o WBS), chips **Todas / Atrasadas (solo Completo) / Sobre-ejecutadas / Sin actividad**, el nivel elegido en «Avance por nivel» (con «quitar»), un contador «N partidas» y **«Limpiar filtros»**; si ninguna coincide, avisa. Los filtros solo ocultan filas en pantalla, no cambian ningún cálculo ni la descarga.
- **Costo real de recursos:** agrupado por tipo (Mano de obra, Equipos, Materiales, Subcontratos) con subtotal, % del total y barra; cada grupo muestra los 5 de mayor costo y «Ver los N restantes (incluye sin costo)»; Transversales (prorrata) y Sin resolver aparte; al pie, Σ recursos + diferencia = Total (AC).

## Gráficas, detalles y partida en revisión (Victor, 2026-10-15)

- **«Avance físico por nivel»:** barras verticales, programado al corte (Plan Maestro) contra real (RDT validados), con selector de nivel (Servicio, subpresupuestos, títulos…) tomado del mapa de niveles del DP (`servicio_encabezados`). Clic en una barra baja un nivel, con una ruta para volver. Sin Plan Maestro aprobado, la barra programada dice «Pendiente».
- **Una barra por recurso, arriba del panel (Victor, 2026-10-22):** en el panel «Recursos», antes de las pestañas, sale una fila por cada recurso que el servicio tiene: **HH, HM, Mano de obra indirecta, Subcontratos y Materiales**. El relleno es el **consumo** (acumulado ÷ contractual) y la marca vertical es el **avance físico** del servicio (la misma en todas): el relleno en ámbar indica que se consume más rápido de lo que se avanza y en rojo que se excede lo contractual. **Clic en una barra abre la pestaña de ese recurso.** Subcontratos y Materiales son dinero y solo salen en Completo; HH, HM y Mano de obra indirecta son horas y salen en ambos. La mano de obra indirecta compara las horas del DP (`dp_moi`) con las acumuladas del PR y no suma al costo directo. En cada pestaña los recursos van ordenados: primero los que exceden lo contractual, luego por mayor consumo (empate: mayor contractual); Materiales grafica los 15 de mayor consumo y la tabla «Ver valores» trae todos.
- **«Recursos: contractual · acumulado · restante»:** barras horizontales por recurso, con pestañas **Mano de obra (HH)**, **Equipos (HM)**, **Mano de obra indirecta**, **Subcontratos** y **Materiales**. La barra mide lo contractual; la parte de color es lo acumulado, la gris lo restante y la roja el exceso. Las HM acumuladas suman operativas más stand-by. Subcontratos se miden en dinero y **solo en Completo**: en Parcial la pestaña sale deshabilitada con título; lee el acumulado de cada subcontrato según su forma de medir (avance físico o monto ingresado en el Reporte del proyecto, [flujo 10](10-generacion-pr.md)) y ya no queda «Pendiente». La unidad de las cantidades contractuales de equipos se toma como HM (lo que fija el import del DP); confirmado por Victor el 2026-10-17: las cantidades de equipos de sus presupuestos vienen en horas.
- **Tocar un cargo o un equipo** muestra en qué partidas se usó (solo horas; el equipo de un RDT nuevo muestra «Sin partida vinculada», porque ya no se asigna a una partida; el cargo del tareo se une al recurso del PR por nombre normalizado, sin tildes ni mayúsculas, porque no hay llave entre ambos).
- **Interactividad:** cada barra y cada sector de la dona muestran su valor al pasar el mouse, al tocar o con el teclado; la leyenda oculta o muestra series; clic en la dona (Mano de obra o Equipos) lleva la gráfica de recursos a esa pestaña; clic en una barra de «Desempeño por partida» marca la partida y baja a la matriz. Ningún valor queda solo en el globo: también está en la etiqueta o en una tabla «Ver valores».
- **Tarjetas de arriba con clic:** cada tarjeta abre debajo de la fila un detalle y lo cierra al volver a tocarla: % avance (por subpresupuesto), BAC (por tipo de recurso), PV y EV (por subpresupuesto), AC (por recurso; lleva a «Costo real de recursos»), SPI (partidas más atrasadas), CPI (partidas con menor CPI), IP (por partida), HH (por cargo) y PPC (causas; el detalle va dentro del Bloque E). Cada detalle tiene un botón a la gráfica o la matriz que corresponde y sus filas de partida se pueden tocar para revisarla. En Parcial las tarjetas de dinero no existen y los detalles no muestran dinero.
- **Partida en revisión:** al elegir una partida (en «Desempeño por partida», en el detalle de una tarjeta, en la gráfica de recursos o en la matriz) aparece arriba una franja fija «Revisando partida …» con su avance, IP y CPI (CPI solo en Completo), que acompaña al bajar; la fila de la matriz queda resaltada con la marca «En revisión» y las demás barras se atenúan. Se quita con «Quitar» o con Escape.
- **Estilo:** los recuadros del Dashboard (tarjetas, paneles de gráfica, detalle y matriz) llevan contorno **punteado amarillo** (ver [design.md](../05-diseno-y-referencias/design.md)).

## Descargar (Victor, 2026-10-15)

- Botón en la fila de filtros, con menú PDF o Excel (`GET /api/proyectos/[id]/dashboard/descargar?formato=pdf|xlsx&corte=AAAA-MM-DD`). Lo ven y lo usan los 13 roles; el servidor valida sesión, rol y alcance.
- **El archivo incluye siempre el Dashboard, la Matriz de partidas y la Curva S.** El PDF A4 horizontal entrega tres cosas (Victor, 2026-10-18): **(1) el Dashboard en una sola hoja**, con el aspecto de la pantalla (fondo oscuro, tarjetas, barras de avance por nivel, recursos HH y HM, composición del costo y desviación en Completo, Pareto de CNC y diagnóstico); **(2) la Matriz de partidas**, con su título y su banda, que sigue en más hojas si hace falta (y los subcontratos en Completo); **(3) la Curva S**, con título, resumen al corte y cada gráfica enmarcada (económica y física en Completo, solo física en Parcial). Excel: una hoja por bloque y las series de la Curva S.
- **Usa la fecha de corte y el modo de la pantalla:** `corte` es una fecha AAAA-MM-DD (el filtro ya resuelto, no el preset) y la Curva S del archivo recorta EV y AC a ese corte. La descarga no lleva hoy tabla semanal; cuando la lleve, usará **la misma regla de fila parcial que la pantalla** ([flujo 21](21-curva-s.md), «Granularidad»): PV, EV y AC de cada fila al mismo corte. En Completo (rol con economía y `tipo_dashboard` COMPLETO): Curva S económica y física, con dinero; en Parcial: sin dinero y Curva S solo física. Una prueba comprueba que el archivo Parcial no contiene ningún símbolo ni sigla de dinero.
- El AC del archivo se arma con el mismo cálculo que la pantalla (materiales y subcontratos incluidos), así que PDF, Excel y pantalla dan el mismo AC. Ruta con `maxDuration = 60`.

## Costo real de recursos (solo Completo)

Bloque propio del Dashboard Completo (D2, 2026-10-02): desagrega el AC real por
recurso para ver su incidencia. El dato se lee del PR; el Dashboard no recalcula.

- **Filas:** `pr_recursos` de tipo **MO (personal, HH)**, **HM (equipos)**,
  **materiales** y **subcontratos**, con su `descripcion` y su costo acumulado
  (los cuatro tipos suman, regla de costo real del [flujo 10](10-generacion-pr.md)).
- **Total = AC** del PR (la misma fuente que el KPI AC), nunca una suma paralela.
- **Fila «Sin resolver»** (con partidas transversales aprobadas se rotula **«Transversales (prorrata)»**, Victor 2026-10-21, igual que en el PR) = `AC − Σ filas`, visible **solo** cuando la diferencia
  es distinta de cero; explica las filas sin partida vinculada (deuda de
  `db/055`). Con las cuatro clases resueltas vale 0. No se fuerza a cero ni se
  inventa dato.
- El balde `costo_legacy_sin_partida_acum` es una **nota informativa, nunca una
  fila sumable**: ya está dentro de las filas de recursos y sumarlo duplicaría.
- **Materiales y subcontratos entran al AC desde el 2026-10-15** (Victor: «todo
  debe sumar a todo»): materiales por % de avance físico, subcontratos por
  avance físico o por el monto ingresado en el Reporte del proyecto. Reemplaza
  la regla de septiembre «no suman al costo real». **Las HH de MOI no se
  valorizan** (regla 10).
- **Vista solo por recurso**, no por partida.
- **Partidas transversales (Victor, 2026-10-19):** suman al BAC, PV, EV, AC y a las HH/HM del Dashboard como **filas calculadas de solo lectura** en la matriz de partidas (fórmulas en el [flujo 10](10-generacion-pr.md)). **Limitación:** el costo por recurso de esta tabla (`pr_recursos.costo_acumulado` de mano de obra y equipo) **no incluye la parte de las transversales**; por eso, con transversales aprobadas, «Sin resolver» puede mostrar esa diferencia, y no se fuerza a cero.

## Diagnóstico

Cuatro puntos, tomados de datos que ya existen en el PR:

- Partidas sobre-ejecutadas (metrado restante negativo).
- Partidas sin actividad registrada.
- Recursos sin tarifa (`proyecto_pr.recursos_sin_tarifa`): la tarjeta **lista hasta 4 nombres** («y N más») y su enlace abre la **página del DP del servicio**, donde se declara la equivalencia en «Equivalencias de cargos del servicio» ([flujo 09](09-importar-dp.md)); la descarga Excel agrega una fila «Cuáles (sin tarifa)» con todos los nombres.
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
- No dibuja la Curva S ni ninguna serie temporal **en pantalla**: el archivo que se descarga sí la incluye (ver «Descargar»).
- No modifica `evm.ts` ni el motor de RDT → PR.
