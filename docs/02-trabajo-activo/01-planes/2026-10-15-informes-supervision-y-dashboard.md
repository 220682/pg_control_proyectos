# Informes de supervisión (diario y semanal) y mejoras del Dashboard

## Identificación y estado

- Tema: informes de supervisión del operativo (diario y semanal, con fotos de campo y descarga en Word, PDF y Excel) y mejoras del Dashboard (responsable operativo, IP y HH, avance por nivel, recursos contractual / acumulado / restante, descarga con la Curva S).
- Fecha de inicio: 2026-10-15.
- Estado: `En implementación` — 17 de 19 tandas cerradas en sus ramas (A, B, N, O, H, R, I, P, J, K, S, C, D, E, F, G y Q: 109 de 124 ítems, 88 %). Tras cerrar Q (2026-10-16): sigue la corrección de la vista previa de F en W3 (cambios sin commit en `local-worker-3`: `BloqueVista.tsx` y `EditorInforme.tsx`), luego aplicar las migraciones (Victor) y L; M (Documentador) va tras L. La corrección de API de W1 (c99dc90) ya está incorporada en `local-worker-3` (9d8a97c); W2 terminó todas sus tandas; el cierre de R ya está incorporado en `local-worker-1` (ee80c7a) y en `local-worker-2` (dc5144f) (ver «Handoff 2» y el Registro de decisiones).

Puertas:

- Gate Spec: `aprobado` (Victor, 2026-10-15). **Ampliaciones D, E y F aprobadas** (Victor, 2026-10-15: «ok a todo»).
- Gate 1: `aprobado` (Victor, 2026-10-15: respondió todas las preguntas y cerró con «ya está todo concretado»). El Orquestador entrante lo confirma en una línea con Victor antes de lanzar el primer Worker.
- Gate 2: `pendiente`

Maquetas de este Spec (abrir en el navegador):

- `docs/05-diseno-y-referencias/mockups/informes-supervision.html` — vistas: Listado, Nuevo (formatos), Editor, Celular (foto de campo).
- `docs/05-diseno-y-referencias/mockups/dashboard-ip-hh-graficos.html` — modos Completo y Parcial, estados vacío, carga y error.

## Spec

### Estado

`Aprobado` (Victor, 2026-10-15: «spec aprobada»).

### Problema y contexto

El supervisor de campo ya registra su avance diario en el RDT (flujo 06). No tiene dónde armar su **informe diario y semanal**: hoy lo hace fuera del sistema (Word con fotos pegadas), sin relación con los datos que ya cargó. En el panel derecho existe el chip **«Informe de servicio»** en Supervisión operativa, sin pantalla («Sin pantalla todavía», `registro-accesos.ts`).

El Dashboard (flujo 11) no muestra quién es el responsable operativo del servicio, no muestra el IP ni las HH (ya se calculan en el PR, flujo 10), no tiene una vista del avance por nivel del presupuesto ni del consumo de recursos, y no se puede descargar.

### Resultado esperado

Dos interfaces:

**A. Informes de supervisión.** El operativo arma desde la app su informe diario o semanal: elige un formato, el sistema llena solo los datos del proyecto (actividades del RDT, personal y equipos, avance, IP, HH), él agrega texto y fotos, lo guarda como borrador y, cuando está listo, lo emite para que lo vea todo el equipo del servicio. Lo descarga en PDF, Word o Excel. Desde el celular, un chip «Foto de campo» abre la cámara, pide servicio, actividad y descripción, y deja la foto lista para el informe.

**B. Dashboard.** Muestra el responsable operativo, el IP y las HH (contractuales, acumuladas y restantes) sin agrandar la pantalla, dos gráficas nuevas con filtro (avance físico por nivel; recursos contractual / acumulado / restante para HH, equipos y subcontratos) y un botón Descargar (PDF con la Curva S, o Excel).

### Alcance

**A. Informes de supervisión**

1. **Chip.** Se activa el chip existente «Informe de servicio» (Supervisión operativa, panel derecho) con el nombre **«Informes de supervisión»**, y se agrega en el panel izquierdo (grupo Reportes). Chip **informativo** con acciones internas (como Paquetes de trabajo): ver el listado no muta nada.
2. **Chip de acción «Foto de campo»** en Supervisión operativa, en Accesos rápidos y en Acciones del panel izquierdo. En el celular abre la cámara trasera directamente.
3. **Listado** del servicio: código, tipo, fecha o período, formato, autor, estado, versión, cantidad de fotos y acciones. Filtros por tipo, estado, autor y fecha.
4. **Tipos:** Diario (una fecha) y Semanal (**período configurable desde – hasta**; por defecto, la semana en curso; ver punto 16).
5. **Código:** `{N° OT}-ID-{n}` para diarios e `{N° OT}-IS-{n}` para semanales (mismo patrón que el RQ, `{N° OT}-RQ-{n}`).
6. **Formatos de partida (selector), cada uno con contenido distinto** (Victor, 2026-10-15: «el contenido no puede ser igual»):
   - **Técnico completo** (diario): actividades del RDT, **personal desglosado** (nombre, cargo, partida, HH normales, HH extra, total), **equipos desglosados** (equipo, código, partida, HM operativas, HM stand-by, estado), incidencias, fotos y firmas.
   - **Semanal acumulado**: es el Técnico en tipo Semanal. Por actividad: contractual, acumulado anterior, metrado de cada día del período (o de cada semana si el período pasa de 10 días), total del período, acumulado a la fecha y %; personal con HH por día o semana, total, acumulado y contractual; equipos con HM por día o semana, total, stand-by, acumulado y contractual; avance acumulado en el período (programado contra real); indicadores del período y acumulados (avance, HH, HM, IP, PPC); restricciones y próximo período; fotos destacadas y la lista de diarios que lo forman.
   - **Ejecutivo** (1 página): semáforo, 4 indicadores, avance por nivel, 3 logros y 3 alertas, 2 fotos. Sin tablas.
   - **Registro fotográfico**: solo fotos con hora, partida y descripción (2, 4 o 6 por página).
   - **Costos** (diario o semanal): EV, AC, CV, CPI y SPI; personal y equipos **valorizados** (HH o HM × tarifa congelada); costo por partida. **Solo lo crean y lo ven los 5 roles con datos económicos** (flujo 14, regla 2); a los demás el formato les sale deshabilitado con título y el informe no les aparece en la lista. Respeta las reglas de costo: costo directo en US$, las HH de MOI no se valorizan, materiales y subcontratos por % de avance físico, **sumados al costo real** (R20, que reemplaza el «% de avance económico» y el «no suman al costo real» de este texto).
   - Más **«Mis formatos»**: cada usuario guarda su propio arreglo de bloques desde el editor.
7. **Editor por bloques** con vista previa de hoja A4: se quitan, ocultan, agregan y reordenan bloques.
   - **Bloques de datos del proyecto** (se llenan solos): encabezado y datos del servicio, indicadores al corte (avance físico, programado, IP, HH), actividades ejecutadas, personal y equipos (HH/HM del día), avance por nivel, Curva S física, PPC y causas, avance de una partida, Plan Maestro próximos 7 días.
   - **Bloques libres:** texto, fotos, tabla, clima y turno, firmas.
8. **Estados:** `Borrador` (solo lo ve su autor; se guarda solo) → `Emitido` (lo ve el equipo del servicio; queda congelado) → `Reemplazado` (cuando se emite una versión nueva). Un emitido **no se edita**: se corrige emitiendo la versión siguiente, y la anterior queda consultable.
9. **Foto fija al emitir:** los bloques de datos guardan los valores del momento de la emisión; el informe emitido no cambia si después cambia el RDT o el PR.
10. **Avance real solo validado:** los indicadores usan RDT `VALIDADO`. Lo del día que aún no se valida entra rotulado **«reportado, pendiente de validación»**, nunca como avance real.
11. **Banco de fotos del día:** cada foto de campo queda en el banco del servicio y del día, con hora, GPS (si el usuario lo permite), partida o paquete (opcional) y descripción; desde el editor se ubica en el bloque que se quiera. También se puede mandar directo a una sección del borrador de hoy.
12. **Traer del informe anterior:** al crear, opción de copiar «Restricciones y pendientes» y «Próximas actividades» del último emitido.
13. **Semanal desde los diarios:** el semanal propone las actividades, el avance y las fotos de los diarios emitidos del período. Un día trabajado sin diario emitido entra solo con los datos del RDT (validado o «reportado, pendiente de validación»), sin texto ni fotos, y la pantalla lo avisa antes de crear.
14. **Descarga:** PDF (igual a la vista previa), Word `.docx` (editable) y Excel `.xlsx` (una hoja por tabla y una hoja «Fotos» con miniatura, descripción y partida). Versión completa, solo resumen o solo fotos. Un borrador descargado lleva marca de agua «BORRADOR».
15. **Aviso:** al emitir se notifica en `/notificaciones` (regla 9 del flujo 16) a quien siga el servicio.
16. **Período del semanal configurable** (Victor, 2026-10-15: «que sea configurable el informe semanal, desde hasta, para poder elegir fechas»):
   - Al crear, atajos «Semana en curso», «Semana anterior», «Últimas 2 semanas», «Mes anterior» y «Personalizado», más los campos Desde y Hasta. Debajo, un resumen: días del período, días trabajados, diarios emitidos, días sin diario emitido y si las columnas irán por día o por semana.
   - En el editor del borrador, el período se puede cambiar desde la barra superior y el informe se rearma solo. Al emitir, el período queda congelado con el resto.
   - Límites, validados también en el servidor: «Desde» no antes del inicio de ejecución del servicio, «Hasta» no después de hoy, «Desde» no posterior a «Hasta», máximo 3 meses.
   - Hasta 10 días, las tablas van por día; más de 10, por semana. Si el período pasa de 7 días, el título cambia a «Informe del período». El código sigue siendo `{N° OT}-IS-{n}`.
   - Un período que se cruza con un semanal ya emitido **se permite** (cada informe guarda su propio período) y la pantalla solo lo avisa (Victor, 2026-10-15).

**B. Dashboard**

1. **Supervisor operativo a cargo** en la línea del servicio (debajo del N° OT), como etiqueta en el color de Supervisión operativa. Fuente: el campo «Supervisor operativo a cargo» de Editar servicio, **uno solo por servicio** (Victor, 2026-10-15). Sin asignar: «Sin supervisor a cargo».
2. **IP y HH sin agrandar la pantalla.** En Completo, como dos tarjetas de buen tamaño en el espacio libre del panel «Composición del costo», a la derecha de la dona: IP (valor, HH ganadas y HH reales) y HH contractuales (barra de consumo, acumuladas con % y restantes). Las tarjetas SPI y CPI de arriba **no llevan** cuadros adicionales (Victor, 2026-10-15: dentro de las tarjetas «están muy comprimidos»). Las dos tarjetas abren su detalle con clic, como las de arriba. En Parcial, como no hay tarjetas de dinero, el IP y las HH tienen tarjeta propia en la misma fila. Las HH y el IP no son dinero: se ven en los dos modos.
3. **Gráfica «Avance físico por nivel»:** barras verticales, programado al corte (Plan Maestro) contra real (RDT validados), con selector de nivel (Servicio, subpresupuestos, títulos…) tomado del mapa de niveles del DP (`servicio_encabezados`). Clic en una barra baja un nivel. Sin Plan Maestro aprobado, la barra programada dice «Pendiente».
4. **Gráfica «Recursos: contractual · acumulado · restante»:** barras verticales por recurso, con pestañas **Mano de obra (HH)**, **Equipos (HM)** y **Subcontratos**. La barra mide lo contractual; la parte de color es lo acumulado, la gris lo restante y la roja el exceso. Subcontratos se miden en dinero (% de avance económico, regla 5): **solo en Completo**; en Parcial la pestaña sale deshabilitada con título.
5. **Matriz de partidas:** suma las columnas HH contractuales, HH acumuladas e IP por partida (sin dinero; también en Parcial).
6. **Descargar:** el archivo incluye **siempre los dos, el Dashboard y la Curva S** (Victor, 2026-10-15). PDF (lo que se ve + la Curva S en hoja aparte + matriz, A4 horizontal) o Excel (una hoja por bloque y las series de la Curva S). Usa la fecha de corte y el modo de la pantalla: en Completo, Curva S económica y física; en Parcial, sin dinero y Curva S solo física.
7. **Gráficos interactivos** (Victor, 2026-10-15): cada barra y cada sector de la dona muestran su valor al pasar el mouse o con el teclado; la leyenda oculta o muestra series; clic en la dona (Mano de obra o Equipos) lleva la gráfica de recursos a esa pestaña; clic en una partida de «Desempeño por partida» la marca en la matriz; clic en una barra de avance por nivel baja un nivel, con una ruta para volver. Ningún valor queda solo en el globo: también está en la etiqueta o en la matriz.
8. **Tarjetas de arriba con clic** (Victor, 2026-10-15: «click en los recuadros superiores»): cada tarjeta abre debajo de la fila un detalle y lo cierra al volver a tocarla: % avance (por subpresupuesto), BAC (por tipo de recurso), PV y EV (por subpresupuesto), AC (por recurso), SPI (partidas más atrasadas), CPI (partidas con menor CPI), IP (por partida), HH (por cargo) y PPC (causas). Cada detalle tiene un botón que lleva a la gráfica o a la matriz que corresponde, y sus filas de partida se pueden tocar para revisarla. En Parcial, las tarjetas de dinero no existen y los detalles no muestran dinero.
9. **Partida en revisión visible** (Victor, 2026-10-15: «que se refleje más que esa partida está siendo revisada»): al elegir una partida (en «Desempeño por partida», en el detalle de una tarjeta, en la gráfica de recursos o en la matriz) aparece arriba una franja fija «Revisando partida …» con su avance, IP y CPI (CPI solo en Completo), que acompaña al bajar; la fila de la matriz queda resaltada con la marca «En revisión» y las demás barras de la gráfica se atenúan. Se quita con «Quitar» o con Escape.
10. **Recursos con clic:** tocar un cargo o un equipo en la gráfica de recursos muestra en qué partidas se usó.
11. **Línea punteada amarilla en todos los recuadros** (Victor, 2026-10-15: «que se mantenga la línea punteada amarilla en todos los recuadros»): tarjetas, paneles de gráfica, detalle y matriz llevan contorno punteado amarillo. **Queda en la app real** (Victor, 2026-10-15: «déjala en el Dashboard»): se agrega a `design.md` como estilo de los recuadros del Dashboard.
12. **% Avance físico más grande y con barra** (Victor, 2026-10-15): el número de la tarjeta sube de tamaño y lleva una barra como la de HH contractuales: lo ejecutado en verde, una marca en lo programado al corte (Plan Maestro; sin Plan Maestro aprobado no hay marca) y el restante. En Completo y en Parcial.

**C. Restricción nueva: sin supervisor a cargo no hay ejecución** (pedido de Victor, 2026-10-15)

1. El paso `EN_PLANEACION` → `EJECUCION` exige, además del Plan Maestro aprobado y el checklist completo, que el servicio tenga **un supervisor operativo a cargo** asignado (el campo de Editar servicio).
2. Se valida **en el servidor** (`POST /api/proyectos/[id]/confirmar-transicion`), no solo en la interfaz: por URL directa queda igual de bloqueado. El mensaje dice qué falta: «No se puede pasar a Ejecución: el servicio no tiene supervisor operativo a cargo. Asígnalo en Editar servicio».
3. El botón de confirmar la transición lista lo que falta (Plan Maestro, checklist, supervisor a cargo), igual que hoy con los otros dos requisitos.
4. Propuesta, a confirmar: con el servicio ya en ejecución, Editar servicio deja **cambiar** al supervisor por otro, pero **no dejarlo vacío**.
5. Los servicios que ya están en ejecución sin supervisor no retroceden de estado: el Dashboard muestra «Sin supervisor a cargo» como aviso.

Verificado el 2026-10-15: esta restricción no existe hoy; `confirmar-transicion` solo valida Plan Maestro `APROBADO` y checklist completo.

**D. Cambios al RDT** (Victor, 2026-10-15: «sí debe ir, es un punto importante, debemos implementarlo en este plan de una vez… vamos a tocar el RDT»). *Ampliación aprobada (Victor, 2026-10-15).*

1. **Personal:** por cada persona del tareo, el supervisor registra cuántas de sus horas del día son **HH extra**; las normales = total − extra. El informe técnico muestra HH normales, HH extra y total.
2. **Equipos:** por cada equipo del parte, el supervisor registra las **HM stand-by** (horas parado y disponible) además de las HM operativas, y el **estado** del equipo.
3. **Reglas (Victor, 2026-10-15):** la HH extra se valoriza con la tarifa de la hora normal × **1.25**; las HM stand-by **suman al costo real** (con la tarifa del equipo) y **también cuentan en el consumo de HM contra lo contractual**; el estado del equipo se elige en un **desplegable**: Operativo, Stand-by, Averiado, En mantenimiento.
4. Los RDT ya existentes quedan con extra = 0, stand-by = 0 y estado vacío; no se reescriben.
5. Coordinación: el plan «Revisión completa de la app» (2026-10-14, en curso) ya cambió el RDT (borrador e inasistencias, `e0d00ff`). La tanda del RDT parte de `main` al día y se coordina con ese plan para no pisar los mismos archivos.

**E. Pestaña «Inasistencias» en Informes de supervisión** (Victor, 2026-10-15). *Ampliación aprobada (Victor, 2026-10-15).*

1. Pestaña propia dentro de «Informes de supervisión», aparte de los informes: lista las inasistencias que ya se registran en el RDT (persona, DNI, motivo, nota, fecha, servicio y RDT de origen).
2. Filtros: **Diario** (una fecha) o **Semanal** (desde – hasta, con el mismo control de período del informe semanal); **todos mis servicios** o **uno en particular**.
3. Descarga en **PDF** con el filtro aplicado.
4. Las inasistencias **no van dentro de los informes de supervisión** (Victor, 2026-10-15).
5. **La ven los 13 roles** (Victor, 2026-10-15: «que lo vean todos»), siempre dentro de los servicios asignados al usuario («todos mis servicios»; el administrador ve todos). Los informes emitidos también los ven los 13 roles (ya decidido).

**F. Subcontratos con dos formas de medir** (Victor, 2026-10-15). *Ampliación aprobada (Victor, 2026-10-15).*

1. Cada subcontrato del servicio tiene un selector de medición: **Por avance físico** (por defecto: acumulado = contractual × % de avance físico del servicio) o **Ingreso manual** (se escribe el monto acumulado y el sistema calcula el %: contractual 200, ingreso 40 → 20 %).
2. Se ingresa en el **Reporte del proyecto** (no en «Recursos del servicio», que no muestra costos) y solo lo hacen los **5 roles con datos económicos**, con el servicio asignado (Victor, 2026-10-15).
3. ~~El monto manual cuenta como avance (valor ganado) del subcontrato, no como costo real; los subcontratos no suman al costo real.~~ **Reemplazado por R20 (Victor, 2026-10-15):** el monto ingresado **es el costo real** del subcontrato y suma al AC; el subcontrato por avance físico también suma al AC (contractual × % de avance físico). El EV, el PV y el BAC no cambian.

### No alcance

- Guardar fotos sin señal y subirlas después (cola sin conexión): fase 2, propuesta aparte.
- Aprobación formal del informe por la jefatura antes de emitirlo (ver decisión pendiente 4).
- Edición de fotos (recorte, anotaciones sobre la foto): fase 2.
- Informe mensual o de cierre; el «Acta de conformidad» sigue sin pantalla.
- La Curva S **en pantalla** del Dashboard: sigue con pantalla propia (flujo 21); solo entra en el archivo descargado.

### Usuarios / roles afectados

Propuesta, a confirmar contra la matriz del flujo 14:

| Acción | Quién (propuesta) |
|---|---|
| Ver informes emitidos y descargarlos | Los 13 roles, con el servicio asignado (`proyecto_miembros`) |
| Crear, editar su borrador y emitir | Administrador, jefe de proyectos, jefe de oficina técnica y supervisor operativo (los mismos de «Crear RDT»), con el servicio asignado |
| Tomar y subir foto de campo | Los mismos de crear informe |
| Emitir una versión nueva de un informe ajeno | Administrador y jefe de proyectos |
| Ver un borrador | Solo su autor |
| Crear, emitir y ver un informe de formato **Costos** | Solo los 5 roles con datos económicos (administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos y jefe de costos), con el servicio asignado |
| Descargar el Dashboard | Quien ve el Dashboard; el contenido sigue su modo (Parcial sin dinero) |
| Asignar el supervisor operativo a cargo | Sin cambio: quien edita el servicio (pantalla Editar servicio, ya existe) |

### Reglas de negocio y documentos afectados

| Documento | Qué cambia |
|---|---|
| Flujo nuevo **22 — Informes de supervisión** | Reglas de A (estados, foto fija, avance validado, banco de fotos, formatos, código, descarga). |
| [11 — Dashboard](../../04-flujos-de-negocio/11-dashboard.md) | Responsable, IP y HH junto a la dona, % avance con barra, dos gráficas, tarjetas y gráficas con clic, partida en revisión, columnas de HH en la matriz, descarga. |
| [`design.md`](../../05-diseno-y-referencias/design.md) | Estilo nuevo: contorno punteado amarillo en los recuadros del Dashboard (tarjetas, paneles, detalle y matriz). Agregado, no contradice nada escrito. |
| [21 — Curva S](../../04-flujos-de-negocio/21-curva-s.md) | La Curva S entra en el PDF y el Excel del Dashboard (sigue sin vivir en la pantalla del Dashboard). |
| [14 — Accesos y restricciones](../../04-flujos-de-negocio/14-accesos-y-restricciones.md) + artefacto «Matriz de permisos» | Filas nuevas de la tabla anterior. El artefacto lo actualiza Victor. |
| [16 — Paneles](../../04-flujos-de-negocio/16-paneles.md) | Chip «Informes de supervisión» activo y chip de acción «Foto de campo»; árbol del panel izquierdo. |
| [06 — RDT](../../04-flujos-de-negocio/06-rdt.md) | Solo referencia: el informe lee el RDT, no lo cambia. |
| [08 — Programa / portafolio / proyecto](../../04-flujos-de-negocio/08-programa-portafolio-proyecto.md) | Requisito nuevo de la transición a `EJECUCION`: supervisor operativo a cargo (C). |

Contradicciones con lo escrito (se aprueban en el Gate 1 con esta tabla):

| Qué dice hoy | Qué pasaría a decir | Documento |
|---|---|---|
| «Qué no hace el Dashboard: no dibuja la Curva S ni ninguna serie temporal.» | La pantalla sigue sin dibujarla; el **archivo descargado** del Dashboard sí incluye la Curva S en hoja aparte, con la misma fuente del flujo 21. | 11 y 21 |
| Indicadores del Parcial: «solo % avance físico». | El Parcial suma IP, HH contractuales, acumuladas y restantes (no son dinero). | 11 |
| El chip «Informe de servicio» queda inerte («Sin pantalla todavía»). | Chip activo «Informes de supervisión» con pantalla. | 16 |
| La transición `EN_PLANEACION` → `EJECUCION` valida en servidor solo el Plan Maestro `APROBADO` y el checklist completo. | Valida además que haya un supervisor operativo a cargo. | 08 y 14 (nota ³) |

### Datos, API, migraciones o dependencias

Propuesta para el Planner (el Planner decide el detalle):

- **Tablas nuevas** (migraciones desde la 096): `informes` (servicio, tipo, fecha o semana, código, formato, estado, versión, autor, bloques en JSON, foto fija al emitir, emitido en/por, reemplaza a), `fotos_campo` (servicio, autor, tomada en, GPS opcional, partida o paquete opcional, descripción, ruta en el almacenamiento, informe y bloque opcionales), `formatos_usuario` (dueño, nombre, bloques).
- **Supervisor operativo a cargo:** ya existe (Editar servicio y alta del servicio). Hoy no es una columna propia: `api/proyectos/[id]/datos/route.ts` lo resuelve con `resolverSupervisorOperativoActual` (el miembro con rol supervisor operativo asignado más recientemente). El Dashboard **reusa esa misma resolución** (moverla a una función compartida), no crea otra.
- **Fotos:** almacenamiento privado de Supabase con enlaces firmados (ya se usa `storage.from(` en RDT y requerimientos). La foto se reduce en el celular (lado mayor ~1600 px) antes de subir.
- **Cámara:** `<input type="file" accept="image/*" capture="environment">`, sin instalar nada.
- **Exportación:** Excel con `exceljs` (ya instalado). Word y PDF necesitan una librería nueva (por ejemplo `docx` y un generador de PDF del lado del servidor); el Planner propone cuál y la justifica en el Gate 1.
- **Dashboard:** IP, HH ganadas, HH contractuales y reales ya existen en el PR (flujo 10, `src/lib/pr/evm.ts`); el Dashboard las lee, no las recalcula. El avance por nivel agrupa las partidas del PR por el mapa de niveles. HM contractual y acumulada, y el % económico de subcontratos: el Planner confirma que el PR los tiene; si no, se anota como hallazgo antes de construir la gráfica.

### Diseño / UI aplicable

- `docs/05-diseno-y-referencias/design.md` y la «Política de interfaz nueva» del flujo 16 (los diez puntos y la Punch List por defecto de `01-contexto-repositorio/05-diseno-y-ui.md`).
- Las dos maquetas de arriba. Lo marcado «NUEVO» en ellas es lo que propone este Spec.
- Colores de serie del flujo 11 (PV azul, EV aqua); colores de estado para borrador (ámbar) y emitido (verde).

### Riesgos y decisiones pendientes

Decisiones de Victor (2026-10-15, en el chat):

1. **Supervisor operativo a cargo:** ya existe en Editar servicio y hay **uno solo por servicio**; el Dashboard lo muestra desde ahí.
2. **Descarga del Dashboard:** incluye **los dos**, el Dashboard y la Curva S (cambia la regla de los flujos 11 y 21, tabla de arriba).
3. **Quién ve un informe emitido:** los 13 roles con el servicio asignado.
4. **Aprobación:** no en esta versión (Borrador → Emitido); la aprobación de la jefatura queda como fase 2.

5. **Línea punteada amarilla:** queda en el Dashboard de la app real (no es solo marca de maqueta).
7. **Semanales que se cruzan:** se permiten, solo con aviso; límites del período confirmados (no antes del inicio de ejecución, no después de hoy, máximo 3 meses).

Pendiente de confirmar (se cierra a más tardar en el Gate 1):

6. **Supervisor a cargo con el servicio ya en ejecución:** se deja cambiar, pero no vaciar. **Confirmado por Victor (2026-10-15).**
7b. **Subcontratos:** dos formas, por avance físico (por defecto) o ingreso manual (ampliación F). **Decidido por Victor.**
8. **HH extra:** tarifa normal × 1.25. **Decidido por Victor.**
9. **HM stand-by:** suman al costo real. **Decidido por Victor.** También cuentan en el consumo de HM contra lo contractual. **Confirmado por Victor.**
10. **Estados del equipo:** desplegable con Operativo, Stand-by, Averiado, En mantenimiento. **Decidido por Victor.**
11. **Pestaña Inasistencias:** la ven los 13 roles, dentro de sus servicios asignados. **Decidido por Victor.**
12. **Subcontrato manual:** en el Reporte del proyecto, solo los 5 roles con datos económicos; ~~el monto cuenta como avance (valor ganado), no como costo real~~ el monto ingresado **es su costo real** y suma al AC (R20, reemplaza lo anterior). **Decidido por Victor.**
13. **Permisos:** todas las interfaces y acciones nuevas de este plan se registran como filas en las tablas 1 y 2 del flujo 14 (pedido de Victor, 2026-10-15).

Riesgos:

- Generar PDF y Word en el servidor de Vercel puede ser pesado con muchas fotos: el Planner debe medir tiempos con 20 fotos.
- Fotos de campo: espacio de almacenamiento; se reduce el tamaño en el celular.
- La señal en campo es mala: sin la cola sin conexión (fase 2), la foto se pierde si no sube; la pantalla debe decirlo claro y dejar reintentar.

### Criterios de aceptación

**A. Informes**

- [ ] El chip «Informes de supervisión» abre la pantalla con el servicio elegido; «Foto de campo» abre la cámara en el celular.
- [ ] Se crea un diario y un semanal con cada uno de los tres formatos y con un formato propio.
- [ ] Los bloques de datos se llenan solos y coinciden con el RDT y el PR del servicio; lo no validado sale rotulado.
- [ ] El borrador no lo ve otro usuario; al emitirlo lo ven los roles acordados y queda congelado.
- [ ] Una corrección crea la versión 2 y la 1 queda «Reemplazada» y consultable.
- [ ] Una foto tomada en el celular llega al banco del día y se ubica en el bloque elegido.
- [ ] Descargas PDF, Word y Excel abren bien y muestran lo mismo que la vista previa.
- [ ] Ningún dato en dinero en los formatos Técnico, Semanal, Ejecutivo y Fotográfico.
- [ ] El formato Costos: el supervisor operativo no lo puede crear (deshabilitado con título), no lo ve en la lista y el servidor le responde 403 si lo pide directo.
- [ ] El semanal muestra, por actividad, acumulado anterior + días (o semanas) + período = acumulado a la fecha, y cuadra con los diarios emitidos.
- [ ] El período del semanal se elige con atajos o con fechas libres, se cambia desde el editor y respeta los límites (inicio de ejecución, hoy, máximo 3 meses), también por llamada directa al servidor.

**B. Dashboard**

- [ ] Se ve el supervisor operativo a cargo, el mismo de Editar servicio; sin asignar, dice «Sin supervisor a cargo».
- [ ] IP y HH coinciden con el PR al mismo corte, en Completo y en Parcial, sin agrandar la fila de tarjetas.
- [ ] La gráfica por nivel cambia de nivel y baja un nivel al hacer clic; sin Plan Maestro dice «Pendiente».
- [ ] La gráfica de recursos suma igual que el PR; subcontratos deshabilitado en Parcial.
- [ ] PDF y Excel descargados respetan corte y modo; en Parcial no llevan dinero.
- [ ] Las interacciones de las gráficas funcionan con mouse, con teclado y en el celular (toque).
- [ ] Cada tarjeta de arriba abre y cierra su detalle; en Parcial ningún detalle muestra dinero.
- [ ] Al elegir una partida, la franja «Revisando partida» queda visible al bajar, la fila de la matriz queda marcada y se quita con «Quitar» o Escape.

**C. Restricción de ejecución**

- [ ] Un servicio sin supervisor a cargo no pasa a ejecución, ni con el botón ni con la llamada directa a la API (respuesta 400 con el mensaje).
- [ ] Con supervisor asignado, Plan Maestro aprobado y checklist completo, pasa igual que hoy.

### Estrategia de prueba / evidencia

- Pruebas unitarias de reglas (estados, foto fija, permisos, agrupación por nivel) y de la cobertura del registro de accesos (`npm test`).
- Pruebas de interfaz con Playwright con las dos cuentas de prueba (permisos altos y sin administración), en escritorio y a 390 px.
- Prueba en un celular real del chip «Foto de campo» (Victor o el Worker con emulación; la cámara real la confirma Victor).
- Archivos descargados abiertos y revisados (captura de cada uno).
- Punch List por defecto de la «Política de interfaz nueva».

### Aprobación (Gate Spec)

- [ ] El Responsable humano aprueba este Spec.

## Plan

### Referencia al Spec aprobado

Spec de este mismo archivo (Gate Spec aprobado por Victor, 2026-10-15). Alcance A (informes), B (Dashboard) y C (restricción de ejecución). Este Plan no cambia el Spec; lo que no cuadra con el Spec o con la app se anota en «Observaciones sobre la política» (P2 a P11) y en «Reglas de negocio acordadas» (R9 a R12) y se pregunta en el Gate 1.

### Objetivo, alcance y no alcance

- Resultado esperado, alcance y no alcance: los del Spec (sin cambios).
- Validación esperada: `npm test`, `npm run lint`, `npm run build` y `npx tsc --noEmit` en verde (el `package.json` no tiene script `type-check`; `next build` ya revisa tipos); Playwright con las dos cuentas de prueba en escritorio y 390 px; archivos descargados abiertos; prueba de permisos por rol (Skill `verificar-permisos-por-rol`).

### Verificado en la app (2026-10-15, solo lectura)

| Tema | Hallazgo | Fuente |
|---|---|---|
| Migración libre | La **096** ya existe (`rdt_borradores_e_inasistencias`, en `main`). La **095** (`cerrar_lectura_directa`) está **sin seguimiento** y es de otra tarea: no se toca. La **097** también existe (`semilla_recursos_4_servicios`, commit 628918a en `main`). **Primera libre: 098.** El Spec decía «desde la 096». (Corregido por el Orquestador: el Planner había puesto 097.) | `ls db/`, `git log` y `git status` de la app |
| Lectura directa | La 095 deja las tablas con RLS y **sin política**: solo el servidor (cliente admin) lee. Las tablas nuevas nacen así (patrón de `rdt_borradores`, 096). | `db/095`, `db/096` |
| Chip actual | `inerte('informe-servicio', 'Informe de servicio', 'Supervisión operativa', …)` en `registro-accesos.ts:457`. Un acceso con `ruta` se activa y la prueba de cobertura (`cobertura-pantallas.ts`) exige que toda `page.tsx` tenga entrada en el registro o excepción. | `src/lib/config/` |
| Transición | `confirmar-transicion` valida solo Plan Maestro `APROBADO` y checklist completo, con compare-and-swap del estado. Errores con 400. | `api/proyectos/[id]/confirmar-transicion/route.ts` |
| Supervisor a cargo | **No es una columna.** `resolverSupervisorOperativoActual` toma, entre los miembros del servicio con rol supervisor operativo, el de `asignado_en` más reciente. | `api/proyectos/[id]/datos/route.ts` |
| PR | `evm.ts` calcula IP, HH ganadas, HH reales y HH contractuales por partida y por servicio. `pr_recursos` trae por recurso (`tipo`, `descripcion`) `cantidad_contractual`, `cantidad_acumulada`, `costo_contractual`, `costo_acumulado`; el motor (`db/053`) acumula **solo** `mano_obra` y `equipo`, desde RDT `VALIDADO`. Por tanto **HH y HM contractual y acumulada por cargo y por equipo existen** (la unidad de `cantidad_contractual` de equipos debe confirmarse en el DP). | `src/lib/pr/evm.ts`, `db/007`, `db/053` |
| Subcontratos | `pr_recursos` tipo `subcontrato` tiene **solo lo contractual**. No hay «% de avance económico» guardado ni calculado en `db/` ni en `src/`. **La gráfica de subcontratos no tiene fuente** (P4). | `grep` en `db/` y `src/` |
| RDT | `rdt_equipos_parte` guarda solo `horas`; `rdt_tareo_horas` solo horas por actividad. **No existen HH extra, HM stand-by ni estado del equipo** (P6). Estados de RDT: `REGISTRADO`, `REVISADO`, `VALIDADO`, `RECHAZADO`. `rdt_partes.jornada_horas` existe (044). | `db/026`, `db/040`, `db/044` |
| Niveles | `servicio_niveles` y `servicio_encabezados` (origen `DP`, con `codigo`, `nombre`, `nivel`, `rol`); la matriz del Dashboard ya los lee con `encabezadosDeNivel`. | `db/073`, `db/074`, `dashboard/page.tsx` |
| Dashboard y Curva S | `dashboard/page.tsx` (463 líneas) carga todo dentro de la página. La Curva S carga sus datos en `api/curva-s/route.ts` (181 líneas). Para que el archivo descargado use las mismas cifras hay que extraer cargadores compartidos (tanda A). | lectura de ambos |
| Almacenamiento | Un solo bucket, `documentos-proyecto`, usado por RDT y requerimientos con `admin.storage`; el bucket no se crea en `db/`. No se usan URL firmadas hoy. | `grep storage` |
| Dependencias | Ya instalados: `exceljs`, `pdfkit` (con parche de fuentes para Vercel en `next.config.ts` y helpers A4 en `src/lib/pdf/hoja.ts`), `pdf-parse`. **No hay** `docx` ni `sharp` declarado. | `package.json` |
| Cabeceras | `next.config.ts` fija `Permissions-Policy: camera=(), geolocation=()` con el comentario «la app no usa cámara ni ubicación». | `next.config.ts` |
| Notificaciones | `TipoNotificacion` = `DOCUMENTO_REQUERIDO`, `CHECKLIST_COMPLETO`, `MENSAJE` (check en `db/012`). No existe «seguir un servicio». | `grupo-proceso.ts` |
| Pruebas | `npm test` = `vitest run` sobre `src/**/*.test.ts`; `npm run lint`; `npm run build`. Playwright se usa por MCP con las cuentas de prueba de la memoria. | `package.json`, `vitest.config.ts` |
| Worktrees | Existen `local-worker-1` a `5` en `.worktrees/` de la app. Los 1 a 3 no tienen commits propios (ramas viejas ya incorporadas a `main`, 0 adelante) y se usan; `local-worker-5` tiene 4 commits propios y **no se usa** (dato del Orquestador, 2026-10-15). | `git worktree list` |
| Costo real en el RDT | `recalcular_pr_desde_rdt` (db/053) calcula el costo real por partida con `tarifa_hh × horas` (tareo) y `tarifa_hm × horas` (equipos); la misma cuenta está repetida en la serie diaria de la Curva S (`db/070`, funciones `ac_diario_hh` y `ac_diario_hm`). El PR acumula `pr_recursos.cantidad_acumulada` y `costo_acumulado` por cargo y equipo con `horas`. **Corrección del Planner (2026-10-15, P19):** son **dos** cuentas SQL del AC (`recalcular_pr_desde_rdt` y `curva_s_proyecto`, que contiene `ac_diario_hh` y `ac_diario_hm`); `guardar_rdt_parte` no calcula costo (solo guarda horas y tarifas) y el «guardado» es el recálculo que dispara `recalcularPr`. Los cambios al RDT (ampliación D) obligan a tocar las dos cuentas, o el AC del PR y el de la Curva S dejan de coincidir; con R20 las dos suman además materiales y subcontratos. | `db/053`, `db/070` |
| Guardado del parte | `guardar_rdt_parte` (última definición en `db/054`; la 096 no la redefine) recibe personas y equipos como `jsonb`; las claves nuevas entran sin cambiar la firma. El borrador (`rdt_borradores.datos`) y el historial (`to_jsonb` de cada tabla) llevan columnas nuevas solos. | `db/054`, `db/096`, `src/lib/rdts/borrador.ts` |
| Dónde se muestra el RDT | `FormularioCrearRdt.tsx`, `lib/rdts/{parte,plantilla,tipos,borrador,consolidado,real-por-clave,exportador-parte-pdf}.ts` y las rutas `api/rdts/partes`, `partes/[id]/pdf`, `partes/pdf-borrador` y `api/rdts/consolidado`. | `grep` de `tarifa_hm`, `horas` |
| Inasistencias | Se guardan en `rdt_partes.inasistencias` (jsonb: `personalId`, `dni`, `nombre`, `motivo`, `nota`); el servicio y la fecha salen de la fila del parte. Motivos: Falta, Descanso médico, Permiso, Vacaciones, Otro. | `db/096`, `src/lib/rdts/borrador.ts` |
| Reporte del proyecto | Es la pantalla PR (`proyectos/[id]/pr/page.tsx`, 420 líneas): `puedeVerPr` = administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos y jefe de costos (los 5 roles con economía); `puedeGestionarPr` es solo administrador y jefe de proyectos. Para el subcontrato manual hace falta una función propia (los 5 roles). | `permisos.ts`, flujo 14 |
| Subcontratos y partidas | Las filas de `pr_recursos` no se ligan a partidas; `reemplazar_dp` rehace el PR al reimportar el DP, así que la forma de medir se guarda **aparte**, por `(proyecto_id, descripcion)`, para no perderse. | `db/007`, `db/060` |
| Quién calcula y quién dispara el AC | Última definición de `recalcular_pr_desde_rdt`: `db/053` (ninguna migración posterior la redefine; `db/060`, `071` y `075` solo la llaman). Última de `curva_s_proyecto`: `db/070`. `recalcularPr` (`acumulacion-rdt.ts:18`) llama a la función por RPC y lo usan `api/rdts/partes/route.ts:378` y `partes/[id]/route.ts:294, 359 y 412`, además de `api/proyectos/[id]/pr/recalcular`. `guardar_rdt_parte` (última: `db/054`) no contiene cuentas de costo. | `grep` en `db/` y `src/` |
| AC en TypeScript | `evm.ts` **no** calcula el AC desde el RDT: lo suma de lo que lee (`ac = Σ pr_partidas.costo_real_acum + costo_legacy_sin_partida_acum`, `evm.ts:170`). Lo leen `dashboard/page.tsx` (líneas 222, 235 y 292) y `pr/page.tsx` (243 y 256). El bloque «Costo real de recursos» (`costo-recursos.ts`) supone Σ `pr_recursos` mano de obra + equipo = AC. | `src/lib/pr/evm.ts`, `src/lib/dashboard/costo-recursos.ts` |
| Materiales | `pr_recursos` con `tipo = 'material'` (check de `db/007:26`), una fila por material con `costo_contractual` y `costo_acumulado` (que `db/053` reinicia solo para `mano_obra` y `equipo`). Vienen del DP (`parser-apu.ts` y `parser-apu-s10.ts` mapean «materiales» y «sub partidas» a `material`). **Ni `pr_recursos` ni `dp_recursos` tienen `wbs`: el presupuesto de materiales no se puede ligar a una partida; solo existe a nivel servicio.** | `db/007`, `db/004`, `src/lib/dp/` |
| % de avance físico | Servicio = EV / BAC (`dashboard.ts:26-36`: `calcularEv` = Σ `metrado_acumulado × precio_unitario`; `calcularAvanceFisico`). La Curva S ya tiene el EV acumulado por día (`ev_diario`, `db/070`). `evm.ts` toma el BAC de Σ `pr_partidas.bac`, mientras `dashboard.ts` (`calcularBac`) suma los `costo_contractual` de los recursos: pueden diferir (P21). | `src/lib/dashboard/dashboard.ts`, `evm.ts`, `db/070` |

### Decisiones técnicas del Plan

1. **PDF: `pdfkit`** (ya instalado y funcionando en Vercel con el parche de fuentes; cero peso nuevo). Se dibuja con los helpers de `src/lib/pdf/hoja.ts`; las gráficas del Dashboard y la Curva S se dibujan como vectores (mismo criterio de «SVG a mano» del flujo 21), sin navegador sin cabeza. Fotos como JPEG incrustado.
2. **Word: `docx`** (paquete npm de JavaScript puro, sin binarios; genera el `.docx` en memoria y admite imágenes JPEG). Es una dependencia nueva: se instala la última versión estable con al menos dos semanas de publicada y se anota en el resumen de cierre (su peso exacto no se verificó; el Worker lo mide con `npm ls` y `next build`). Alternativa descartada: armar el `.docx` a mano con `zip-store.ts`, por costo de mantenimiento.
3. **Excel: `exceljs`** (existente), una hoja por tabla y hoja «Fotos» con miniatura (`workbook.addImage`).
4. **Fotos:** el celular reduce a lado mayor ~1600 px y JPEG calidad ~0,8 con `<canvas>`; el servidor **valida** (JPEG por sus primeros bytes, tope 3 MB, rol, alcance, descripción obligatoria). Se guardan en `documentos-proyecto` bajo `informes/{proyectoId}/fotos/{uuid}.jpg` (**sin bucket nuevo**). Se entregan por una ruta del servidor que valida permisos y responde con URL firmada de 60 s.
5. **Medir tiempo con 20 fotos:** el Worker de la tanda G arma un informe de prueba con 20 fotos de ~300 KB y registra, para PDF, Word y Excel, milisegundos y memoria (`process.memoryUsage()`) corriendo la ruta en local; fija `export const maxDuration` explícito en las rutas de descarga. Si PDF o Word pasan de 20 s o 400 MB, lo reporta como bloqueo (el tope real de Vercel depende del plan: **por confirmar**). Las fotos se leen del almacenamiento en paralelo, de 4 en 4.
6. **Columna propia para el supervisor a cargo** (decisión de Victor, 2026-10-15): `proyectos.supervisor_operativo_id` (migración 099, con relleno inicial desde la resolución actual) y función compartida `src/lib/proyectos/supervisor-operativo.ts` que lee esa columna. Editar servicio la escribe, comprueba en servidor que la persona tenga el rol supervisor operativo y la agrega como miembro del servicio (alcance); con el servicio en `EJECUCION` se puede cambiar, no vaciar.
7. **Notificar al emitir** con tipo `MENSAJE` a los miembros del servicio (menos el autor), sin cambiar el check de `db/012` (P10).
8. **Versiones:** cada versión es una fila de `informes` (mismo `codigo`, `version` 1, 2, …). Emitir es una función SQL atómica que marca la anterior `REEMPLAZADO`.
9. **Inmutabilidad:** un trigger rechaza cambiar el contenido de una fila `EMITIDO` (solo permite pasarla a `REEMPLAZADO`), además de la regla en el servidor.
10. **Modo del Dashboard descargado:** lo decide el servidor (rol + `tipo_dashboard`), nunca un parámetro del navegador.
11. **HH extra** (ampliación D): columna `rdt_tareo.horas_extra` (horas del día de la persona, no por actividad); normales = total − extra. El total de HH no cambia (la extra ya está dentro), por eso **HH reales e IP no cambian**; sube el costo real: `tarifa × 0,25 × extra`. El recargo se reparte entre las actividades de la persona **en proporción a sus horas** (propuesta del Planner, pregunta 1). Las HH de MOI no se valorizan. El factor 1,25 vive en una constante TS y en la función SQL, con una prueba que las compara.
12. **HM stand-by:** columna `rdt_equipos_parte.horas_standby`; `horas` pasa a ser «HM operativas». Consumo de HM y costo real usan `horas + horas_standby` con la tarifa del equipo (`hm_reales_acum`, `pr_recursos.cantidad_acumulada` y `costo_acumulado`, balde legacy y Curva S). **Estado del equipo:** `rdt_equipos_parte.estado_equipo` con `OPERATIVO`, `STAND_BY`, `AVERIADO`, `EN_MANTENIMIENTO` (vacío en lo existente).
13. **RDT existentes:** extra = 0, stand-by = 0, estado vacío; no se reescribe ninguno. Prueba de aceptación: el AC, las HH y las HM del PR de un servicio con RDT validados salen **idénticos** antes y después de aplicar la 100 (la 102 sí cambia el AC total: decisión 16).
14. **Subcontratos** (ampliación F): tabla `pr_subcontrato_medicion` (migración 101) por `(proyecto_id, descripcion)` con `modo` `FISICO` (por defecto) o `MANUAL` y `monto_manual`. Acumulado: `FISICO` = contractual × avance físico del servicio (EV/BAC al corte); `MANUAL` = el monto escrito, y el sistema calcula el %. Monto negativo se rechaza; monto sobre el contractual se acepta con aviso. Lo calcula el servidor, no el navegador. Por R20 **suma al costo real (AC)**: el subcontrato por avance físico aporta contractual × avance físico y el de ingreso manual aporta el monto ingresado, que **es** su costo real (reemplaza la versión anterior «no entra al AC»). El EV, el PV y el BAC no cambian, así que no hay doble conteo (pregunta 2).
15. **Inasistencias** (ampliación E): sin tabla nueva; se leen de `rdt_partes.inasistencias` de los partes del alcance del usuario que no estén `RECHAZADO` (propuesta del Planner, pregunta 3). Es una pestaña de la pantalla de Informes con selector «Todos mis servicios» / un servicio.
16. **Costo real de materiales y subcontratos (R20), una sola cuenta con un solo dueño.** El Worker 3 (W3) es dueño de las **dos** funciones SQL vivas del AC (`recalcular_pr_desde_rdt` y `curva_s_proyecto`): la 100 (tanda O) les agrega HH extra y HM stand-by, y la 102 (tanda R, después de O y de la 101) les agrega materiales y subcontratos. Así dos Workers nunca redefinen la misma función en paralelo. La 101 (W2, tanda N) solo crea la tabla `pr_subcontrato_medicion`. La cuenta de materiales y subcontratos vive en **una función compartida** (`ac_materiales_subcontratos_al_corte`, migración 102) que el PR y la Curva S llaman con el EV acumulado y la fecha de corte; no se repite en SQL ni en TypeScript. **Granularidad: solo a nivel servicio**, porque `pr_recursos` y `dp_recursos` no tienen partida (ver «Verificado en la app»): materiales = Σ `costo_contractual` de los materiales × (EV / BAC); subcontrato `FISICO` = su `costo_contractual` × (EV / BAC); `MANUAL` = el monto ingresado. Por eso el costo real por partida (`pr_partidas.costo_real_acum`) no cambia: la cuenta nueva se guarda en `proyecto_pr` (`costo_materiales_acum`, `costo_subcontratos_acum`) y en `pr_recursos.costo_acumulado` por fila, y `evm.ts` la suma al AC del proyecto. En la Curva S, un subcontrato `MANUAL` entra con su monto desde el día de su último cambio y antes de ese día vale lo que daba el avance físico (decidido, ver Registro de decisiones del 2026-10-15). Sin tope en 100 % (igual que el EV del PR).

### Migraciones nuevas

Cinco migraciones, todas aditivas (sin borrar ni renombrar columnas ni tablas; reversa documentada en comentario), con el **número fijado de antemano** para que los tres Workers no choquen; el Worker vuelve a mirar `ls db/` y `git log` en `main` antes de escribir cada archivo. Las aplica el Orquestador, una por una, tras consultar al verificador y con la autorización de Victor (pre-autorizada en el Gate 1); el Worker solo escribe el archivo y lo prueba en una base de prueba si Victor la indica. Orden de aplicación: 099 (antes de desplegar la tanda A), 098, 100, 101 y **102 (siempre después de la 100 y la 101**, porque reescribe las funciones que deja la 100 y lee la tabla de la 101), todas antes de la verificación en vivo de su tanda.

| Número | Archivo | Tanda | Qué hace |
|---|---|---|---|
| 098 | `098_informes_supervision.sql` | B | Informes, contadores, fotos de campo, formatos de usuario (tabla de abajo). |
| 099 | `099_supervisor_operativo_a_cargo.sql` | A | `proyectos.supervisor_operativo_id uuid references perfiles(id)` (nulo permitido) y relleno inicial: para cada servicio, el miembro con rol supervisor operativo de `asignado_en` más reciente. Los servicios sin ese miembro quedan en nulo y **no retroceden de estado**. |
| 100 | `100_rdt_extra_standby_estado.sql` | O | `rdt_tareo.horas_extra numeric not null default 0 check (horas_extra >= 0)`; `rdt_equipos_parte.horas_standby numeric not null default 0 check (>= 0)` y `estado_equipo text` con check de los 4 valores; `create or replace` de `guardar_rdt_parte` (misma firma), `recalcular_pr_desde_rdt` y la serie diaria de la Curva S (db/070). **Va separada de la 098** porque reescribe tres funciones vivas del PR y de la Curva S (cada una parte del cuerpo vigente en `main`, no del archivo antiguo) y tiene su propia prueba de equivalencia; así se puede revisar, aplicar y revertir sin tocar las tablas de informes, y porque otro plan está tocando el RDT. La 102 (tanda R) vuelve a reescribir `recalcular_pr_desde_rdt` y la Curva S, partiendo del cuerpo que deje la 100. |
| 101 | `101_pr_subcontrato_medicion.sql` | N | Tabla `pr_subcontrato_medicion` (`proyecto_id`, `descripcion`, `modo` `FISICO`/`MANUAL`, `monto_manual numeric check (>= 0)`, `actualizado_por`, `actualizado_en`; `unique (proyecto_id, descripcion)`; un check que exige monto si el modo es `MANUAL`). RLS sin política. |
| 102 | `102_ac_materiales_subcontratos.sql` | R | `proyecto_pr.costo_materiales_acum` y `costo_subcontratos_acum` (`numeric not null default 0`); función nueva `ac_materiales_subcontratos_al_corte(p_proyecto_id uuid, p_ev_acum numeric, p_fecha date)` (materiales y subcontratos al corte); `create or replace` de `recalcular_pr_desde_rdt` y `curva_s_proyecto` desde el cuerpo vigente tras la 100, que llaman a esa función. **Dueño: W3.** Depende de la 100 (cuerpos de las funciones) y de la 101 (tabla de subcontratos). Aditiva; reversa en comentario. |

Detalle de la 098:

| Tabla / función | Contenido |
|---|---|
| `informes` | `id`, `proyecto_id`, `tipo` (`DIARIO`/`SEMANAL`), `formato` (`TECNICO`, `EJECUTIVO`, `FOTOGRAFICO`, `COSTOS`, `PERSONALIZADO`; el semanal acumulado es el Técnico con tipo `SEMANAL`), `formato_usuario_id` opcional, `fecha_desde`, `fecha_hasta` (diario: iguales), `codigo`, `version`, `estado` (`BORRADOR`/`EMITIDO`/`REEMPLAZADO`), `autor_id`, `bloques jsonb`, `foto_fija jsonb`, `emitido_en`, `emitido_por`, `reemplaza_a`, `creado_en`, `actualizado_en`. `unique (proyecto_id, codigo, version)`; checks de fechas (`desde <= hasta`, tope duro de 93 días); el límite fino de «3 meses», «no antes del inicio» y «no después de hoy» se valida en el servidor. |
| `informes_contadores` | `(proyecto_id, tipo) → ultimo` para `{N° OT}-ID-{n}` / `-IS-{n}`; función `siguiente_codigo_informe` con `insert … on conflict do update … returning` (sin repetidos por carrera). |
| `fotos_campo` | `id`, `proyecto_id`, `autor_id`, `tomada_en`, `lat`, `lng` (nulos), `wbs`/`paquete_id` (nulos), `descripcion`, `ruta_storage`, `bytes`, `informe_id` y `bloque_id` (nulos). |
| `formatos_usuario` | `id`, `dueno_id`, `nombre`, `bloques jsonb`; `unique (dueno_id, nombre)`. |
| `emitir_informe(p_id, p_usuario, p_foto_fija)` | Una transacción: valida que sea `BORRADOR`, lo pasa a `EMITIDO`, guarda la foto fija y marca la versión anterior `REEMPLAZADO`. |
| Trigger de inmutabilidad | Rechaza `update` de contenido sobre `EMITIDO`/`REEMPLAZADO`. |
| RLS | Activado en todas, **sin política** (solo el servidor, como la 095/096). |

### Contratos de API nuevos (todos validan en servidor: sesión, rol y alcance sobre el servicio)

Base: `/api/proyectos/[id]/…`. Guardias: `validarEscrituraProyecto` para crear, editar, emitir y fotos; lectura con `obtenerUsuarioActual` + `tieneAlcanceSobreProyecto`.

| Ruta | Quién | Reglas del servidor |
|---|---|---|
| `GET informes` | los 13 roles con el servicio | Emitidos y reemplazados de todos + borradores **propios**; los de formato `COSTOS` solo si `puedeVerEconomia`. Filtros tipo, estado, autor, fecha. |
| `POST informes` | crear: administrador, jefe de proyectos, jefe de oficina técnica, supervisor operativo | `COSTOS` → 403 sin economía. Período semanal: `desde >= fecha_real_inicio`, `hasta <= hoy` (fecha Lima), `desde <= hasta`, máximo 3 meses; si no, 400 con el límite roto. Un período que cruza otro semanal emitido **se permite** y la respuesta trae `avisos`. |
| `GET/PATCH/DELETE informes/[informeId]` | autor (borrador) | Borrador ajeno → 404. PATCH guarda bloques o cambia el período (mismas validaciones); sobre `EMITIDO` → 409. DELETE solo borrador propio. `COSTOS` sin economía → 403. |
| `POST informes/[informeId]/emitir` | autor | Arma la foto fija con las funciones de la tanda C, llama a `emitir_informe`, notifica. |
| `POST informes/[informeId]/nueva-version` | autor, administrador, jefe de proyectos | Crea un borrador versión +1 desde un emitido; el borrador es de quien lo crea. |
| `GET informes/[informeId]/descargar?formato=pdf\|docx\|xlsx&alcance=completo\|resumen\|fotos` | quien puede ver ese informe | `COSTOS` sin economía → 403. Un borrador lleva marca «BORRADOR». |
| `GET/POST informes/formatos-usuario` | cada usuario sobre lo suyo | Un formato propio con bloques de Costos no se crea ni se usa sin economía. |
| `POST fotos-campo` | los 4 roles que crean informe | JPEG, tope 3 MB, descripción obligatoria, GPS opcional válido, `wbs` debe pertenecer al servicio. |
| `GET fotos-campo?fecha=`, `PATCH`/`GET`/`DELETE fotos-campo/[fotoId]` | banco: los 4 roles; foto dentro de un emitido: los 13 | PATCH asigna bloque de un borrador propio; GET responde URL firmada tras comprobar permisos; DELETE solo foto propia sin informe emitido. |
| `GET dashboard/descargar?formato=pdf\|xlsx&corte=` | quien ve el Dashboard | El modo sale del servidor. En Parcial no hay dinero en ningún byte. |
| `GET dashboard/recurso-partidas?tipo=&descripcion=` | quien ve el Dashboard | HH/HM por partida, sin dinero. |
| `GET /api/inasistencias?tipo=diario\|semanal&desde=&hasta=&proyectoId=\|todos` | los 13 roles | Solo servicios dentro del alcance del usuario (el administrador, todos); `proyectoId` fuera de alcance → 403; período con los límites del semanal (desde ≤ hasta, hasta ≤ hoy, máximo 3 meses) → 400 si no. Lee `rdt_partes.inasistencias` de partes no `RECHAZADO`. Devuelve persona, DNI, motivo, nota, fecha, servicio y RDT de origen. |
| `GET /api/inasistencias/pdf?...` | los 13 roles | Mismo filtro y mismas validaciones; PDF A4 con `pdfkit`. |
| `GET`/`PUT /api/proyectos/[id]/pr/subcontratos` | los 5 roles con economía y el servicio asignado | Sin economía → 403. `PUT` por subcontrato: `modo` y, si es `MANUAL`, `monto` ≥ 0 (negativo o no numérico → 400); el subcontrato debe existir en `pr_recursos` tipo `subcontrato` de ese servicio; guarda quién y cuándo; el acumulado y el % los calcula el servidor y nunca se aceptan del navegador. |
| `POST /api/rdts/partes` y `PATCH /api/rdts/partes/[id]` (existentes) | los de Crear/Corregir RDT | Nuevas claves por persona `horasExtra` (≥ 0 y ≤ total de horas de la persona) y por equipo `horasStandby` (≥ 0) y `estado` (uno de los 4 valores o vacío); lo demás, igual que hoy. |
| `PATCH /api/proyectos/[id]/datos` (existente) | administrador, jefe de proyectos | Guarda `supervisor_operativo_id`; exige rol supervisor operativo de esa persona; con el servicio en `EJECUCION` rechaza vaciarlo (400). |

### Skills aplicables

- `seguir-flujo-de-planes`: Orquestador, al activar y antes de cerrar.
- `cerrar-tanda`: **todas** las tandas, al terminar.
- `verificar-permisos-por-rol`: tandas B, D, E, F, G, K y L (las que tocan permisos).
- `trasladar-hallazgos`: tanda M (Documentador).

### Fases y dependencias

```text
Ola 0   W1: A (base compartida, supervisor con columna propia, restricción C)
Ola 1   W1: B                W2: N -> H -> S -> I -> J -> K   W3: O -> R -> P
        (W2 parte de A)       (N antes de I: la pestaña Subcontratos la necesita; S espera a R)
        (R parte de O y del cierre de N: el Worker git incorpora ese cierre en local-worker-3)
        (W3 parte de main al día; O es independiente de A)
Ola 2   W1: C (parte de B y de O, incorporada) -> D
Ola 3   W1: G (descargas)     W3: E -> F -> Q -> L           (W3 parte de B, C, D)
Cierre  M (Documentador) -> Auditor -> Gate 2
```

Camino crítico: A → B → C → D → (G ‖ E→F→Q) → L. W2 (Dashboard y subcontratos) corre en paralelo desde A y no espera a Informes. W3 usa su primera mitad (O, P: el RDT) mientras W1 hace A y B, por eso no queda ocioso. **C (datos de informes) espera a R** (que va después de O), porque lee las columnas nuevas del RDT y las del AC: el Worker git incorpora `local-worker-3` en `local-worker-1` al cerrar R. R va antes de P para que ese corte lleve solo O y R. **R depende de O (cuerpos de las funciones del AC) y de N (tabla de la 101); S depende de R.**

**División en Workers: 3, con independencia real de archivos.**

| Worker | Tandas | Carpetas propias (nadie más las toca) |
|---|---|---|
| W1 (`local-worker-1`) | A, B, C, D, G | `db/098*` y `db/099*`, `src/lib/informes/**`, `src/lib/proyectos/supervisor-operativo.ts`, `src/lib/permisos/permisos.ts`, `api/**/informes/**`, `api/**/fotos-campo/**`, `api/proyectos/[id]/datos`, `api/proyectos/[id]/confirmar-transicion`, `package.json` (`docx`) |
| W2 (`local-worker-2`) | N, H, S, I, J, K | `db/101*`, `proyectos/[id]/pr/page.tsx`, `src/components/pr/**`, `src/lib/pr/subcontratos*`, `api/proyectos/[id]/pr/subcontratos`, `dashboard/page.tsx`, `src/components/dashboard/**`, `src/lib/dashboard/**`, `api/**/dashboard/**`, `src/lib/pdf/graficos.ts` (nuevo), estilos del Dashboard |
| W3 (`local-worker-3`) | O, R, P, E, F, Q, L | `db/100*`, `db/102*`, `src/lib/pr/evm.ts` y su prueba, `src/lib/rdts/**`, `api/rdts/**`, `components/ui/FormularioCrearRdt.tsx`, `src/lib/rdts/horas-extra.ts` (nuevo), `src/app/(workspace)/proyectos/[id]/informes/**`, `src/components/informes/**`, `api/inasistencias/**`, `src/lib/config/registro-accesos.ts` y sus pruebas, `next.config.ts` |

Reglas para no pisarse: **nadie edita `src/lib/pdf/hoja.ts`** (se importa; lo nuevo va en archivos nuevos); `permisos.ts`, `package.json` y la API de informes solo W1 (por eso las funciones de permiso de subcontratos e inasistencias se crean en la tanda A, antes de que W2 y W3 las usen); el registro de accesos solo W3; `db/README.md`: cada Worker agrega **solo su línea** y el Orquestador resuelve el choque trivial al integrar. **Dependencia entre ramas:** A es base de W2; N (W2) es base de R (W3); R, que incluye a O, es base de C (W1) y de S (W2); B, C y D lo son de E, F, Q y L (W3). El **Worker git** (a pedido del Orquestador; autorizado en el Gate 1) incorpora `local-worker-1` en `local-worker-2` al cerrar A, `local-worker-2` (hasta el cierre de N) en `local-worker-3` antes de R, `local-worker-3` (hasta el cierre de R) en `local-worker-1` y en `local-worker-2` antes de S, y `local-worker-1` en `local-worker-3` al cerrar D; son operaciones entre ramas de trabajo, no tocan `main`. Los worktrees `local-worker-1` a `3` ya existen, con ramas viejas incorporadas a `main` (0 commits adelante): cada Worker empieza con `git merge main` en su rama; `local-worker-5` no se usa. El merge a `main` es del paso 16a, en el orden W1, W3, W2 (W3 contiene a W1).

### Equipo del plan

Trabajamos en Claude Code con subagentes; **no se usa Opus**. Esfuerzo medio en todo. El nivel n0–n5 del archivo 10 es una **equivalencia propuesta** por tipo de tarea (ese archivo mide modelos de opencode, no los de Claude Code; ver P11).

| Rol | Modelo | Esfuerzo | Sesión o tanda | Rama | Worktree | Estado |
|---|---|---|---|---|---|---|
| Orquestador | Sonnet 5.5 desde el relevo 3 (antes Opus 5.5; Victor fijó el modelo con `/model` y el esfuerzo con `/effort` el 2026-10-15) | Extra (xhigh), por pedido de Victor | todo el plan | `main` | N/A | activo (relevo 3) |
| Planner | Sonnet | Medio | este Plan | `main` | N/A | entregado |
| Worker 1 | Sonnet | Medio | A, B, C, D, G | `local-worker-1` | `.worktrees/local-worker-1` | autorizado (Gate 1) |
| Worker 2 | Sonnet | Medio | N, H, S, I, J, K | `local-worker-2` | `.worktrees/local-worker-2` | autorizado (Gate 1) |
| Worker 3 | Sonnet | Medio | O, R, P, E, F, Q, L | `local-worker-3` | `.worktrees/local-worker-3` | autorizado (Gate 1) |
| Documentador | Sonnet (flujos) y Haiku (índices y referencias) | Medio | M | `main` | N/A | pendiente |
| Worker git | Haiku | Medio | a pedido | opera sobre las demás | — | pendiente |
| Auditor | Sonnet | Medio | tras M | `main` | N/A | pendiente |

### Asignación de modelos y esfuerzos por fase (Gate 1)

| Tanda | Contenido | Ítems | Worker | Modelo | Esfuerzo | Nivel equiv. | Justificación | Aprobación Victor |
|---|---|---|---|---|---|---|---|---|
| A | Base compartida, supervisor con columna propia y restricción C | 8 | W1 | Sonnet | Medio | 3 | Varios archivos, una migración pequeña, validación de servidor, refactor sin cambio visible | pendiente |
| B | Informes: migración 098, permisos, reglas puras | 5 | W1 | Sonnet | Medio | 4 | Migración con candado y tablas con RLS; es la más sensible, pero sigue la forma de la 096, por eso esfuerzo medio | pendiente |
| C | Informes: datos de los bloques del sistema | 7 | W1 | Sonnet | Medio | 3 | Cálculos con muchas fuentes; si el cuadre del semanal falla dos veces, el Orquestador pide esfuerzo alto para C4 | pendiente |
| D | Informes: API | 7 | W1 | Sonnet | Medio | 3 | Rutas y pruebas por rol | pendiente |
| N | Subcontratos con dos formas de medir (PR y Dashboard) | 7 | W2 | Sonnet | Medio | 3 | Tabla nueva, cálculo, API con permisos y pantalla del PR | pendiente |
| O | RDT: HH extra, HM stand-by y estado — datos y cálculo | 8 | W3 | Sonnet | Medio | 4 | Reescribe tres funciones SQL vivas (guardado, PR, Curva S); riesgo alto de cambiar el AC de lo existente, mitigado con la prueba de equivalencia | pendiente |
| R | AC con materiales y subcontratos: migración 102, PR, Curva S y `evm.ts` | 6 | W3 | Sonnet | Medio | 4 | Reescribe otra vez las dos funciones vivas del AC y cambia el AC de todo servicio existente; es la cuenta más sensible y la cubre la prueba de equivalencia por componente | pendiente |
| P | RDT: formulario, borrador, PDF y consolidado | 7 | W3 | Sonnet | Medio | 3 | Pantallas y exportadores | pendiente |
| Q | Pestaña Inasistencias y PDF | 6 | W3 | Sonnet | Medio | 3 | API de lectura con alcance, pestaña y PDF | pendiente |
| E | Informes: chips, listado, nuevo y foto de campo | 4 | W3 | Sonnet | Medio | 3 | Pantallas y registro de accesos | pendiente |
| F | Informes: editor y vista | 6 | W3 | Sonnet | Medio | 3 | Editor con estado complejo | pendiente |
| G | Informes: descargas Word, PDF y Excel | 7 | W1 | Sonnet | Medio | 3 | Tres generadores y medición | pendiente |
| H | Dashboard: responsable, % avance, IP y HH | 6 | W2 | Sonnet | Medio | 3 | Una página con dos modos | pendiente |
| S | AC con materiales y subcontratos en las pantallas (PR y Dashboard) | 4 | W2 | Sonnet | Medio | 3 | Cargadores, KPI y bloque de recursos; sin migración | pendiente |
| I | Dashboard: dos gráficas | 7 | W2 | Sonnet | Medio | 3 | Agrupación por nivel y recursos | pendiente |
| J | Dashboard: detalles, partida en revisión, interacciones | 7 | W2 | Sonnet | Medio | 3 | Estado compartido de pantalla | pendiente |
| K | Dashboard: descarga PDF y Excel con Curva S | 7 | W2 | Sonnet | Medio | 3 | PDF vectorial | pendiente |
| L | Integración y verificación en vivo | 7 | W3 | Sonnet | Medio | 3 | Playwright, permisos, móvil | pendiente |
| M | Documentación, filas del flujo 14 y traslado de hallazgos | 8 | Documentador | Sonnet / Haiku | Medio | 3 y 1 | Flujo 22 y flujos editados (Sonnet); índices y verificación de referencias (Haiku) | pendiente |

**Esfuerzo alto: no se solicita en ninguna tanda.** Candidatos eventuales, solo si algo falla dos veces y se pide en el momento (regla de `09-orquestacion-y-modelos.md`): C4 (semanal acumulado), O3/O4 y R2/R3 (la cuenta del costo real). Nivel 5: no se usa. Total: **19 tandas, 124 ítems** (la cifra anterior, 113, tenía un error de conteo en L, que tiene 7; con R6 y S4 nuevos suman 124).

### Tandas e ítems

Formato de cada ítem: **ID**: qué se hace — archivos — criterio de hecho — prueba.

**Tanda A — Base compartida, supervisor con columna propia y restricción de ejecución (W1, ola 0)**
- **A1**: migración `db/099_supervisor_operativo_a_cargo.sql` (columna `proyectos.supervisor_operativo_id` y relleno inicial; ver «Migraciones nuevas») y `src/lib/proyectos/supervisor-operativo.ts` con `obtenerSupervisorACargo` (lee la columna); `datos/route.ts` deja de usar la resolución por «último miembro» — hecho: una sola función usada por todos — prueba: unitaria y base de prueba si Victor la indica.
- **A2**: `confirmar-transicion` exige supervisor a cargo (columna no nula) al pasar a `EJECUCION`; 400 con «No se puede pasar a Ejecución: el servicio no tiene supervisor operativo a cargo. Asígnalo en Editar servicio» — hecho: llamada directa sin supervisor → 400; con los tres requisitos pasa igual que hoy — prueba: de ruta + llamada directa con la cuenta de prueba.
- **A3**: `PATCH datos`: escribe la columna, comprueba en servidor que la persona tenga el rol supervisor operativo y la agrega como miembro; con el servicio en `EJECUCION` se puede cambiar pero no vaciar (400) — decidido por Victor — prueba: de ruta (cambiar, vaciar, rol equivocado).
- **A4**: el botón de confirmar la transición lista lo que falta (Plan Maestro, checklist, supervisor a cargo) — archivos: `proyectos/[id]/page.tsx`, `confirmar-transicion.tsx` — prueba: captura con cada faltante.
- **A5**: extraer de `dashboard/page.tsx` el cargador de datos (PR, plan maestro, corte, recursos) a `src/lib/dashboard/cargar-dashboard.ts`, sin cambio visible — hecho: la página lo usa y muestra lo mismo — prueba: unitaria y capturas antes/después en Completo y Parcial.
- **A6**: extraer de `api/curva-s/route.ts` el cálculo a `src/lib/curva-s/cargar-curva-s.ts`; la ruta delega — hecho: respuesta JSON idéntica — prueba: comparar respuesta antes/después y `curva-s.test.ts`.
- **A7**: regresión — `npm test`, `lint`, `build`, `tsc --noEmit`.
- **A8**: funciones de permiso `puedeMedirSubcontratos` (los 5 roles con economía) y `puedeVerInasistencias` (los 13 roles con rol conocido) en `permisos.ts`, con sus pruebas, para que W2 y W3 las usen sin tocar ese archivo — prueba: unitaria por rol.

**Tanda B — Informes: base de datos, permisos y reglas puras (W1, ola 1)**
- **B1**: `db/098_informes_supervision.sql` (ver «Migraciones nuevas») y línea en `db/README.md` — hecho: archivo revisado por el Orquestador, con reversa en comentario — prueba: ejecutada en una base de prueba indicada por Victor, o «no probada» en el resumen.
- **B2**: funciones en `permisos.ts`: ver informes (13 roles); crear, emitir y tomar foto (los 4 roles de `puedeCrearRdtEstructurado`); crear y ver `COSTOS` (`puedeVerEconomia` y crear); nueva versión de informe ajeno (administrador y jefe de proyectos); descargar informe (quien lo ve) — prueba: unitaria por rol.
- **B3**: `src/lib/informes/tipos.ts` — contrato congelado (informe, bloque, formato, estado, foto, foto fija). Desde aquí W3 trabaja contra tipos estables.
- **B4**: `periodo.ts`: atajos (semana en curso, anterior, últimas 2 semanas, mes anterior), validación de límites, columnas por día (≤ 10 días) o por semana, título «Informe del período» (> 7 días), cruce con semanales emitidos — prueba: unitaria con bordes (10/11 días, 3 meses, hoy, inicio).
- **B5**: `formatos.ts` (cinco formatos con bloques distintos y marca `soloEconomia`) y `estados.ts` (transiciones y visibilidad: borrador solo autor, emitido congelado) — prueba: unitaria; ningún formato distinto de `COSTOS` contiene bloques económicos.

**Tanda C — Informes: datos de los bloques del sistema (W1, ola 1)**
- **C1**: `armar-datos-diario.ts`: encabezado, actividades del RDT (metrado del día, acumulado, %) e indicadores al corte desde el cargador de A5 (avance, programado, IP, HH); lo no validado sale «reportado, pendiente de validación» — prueba: unitaria con RDT `VALIDADO` y `REGISTRADO`.
- **C2**: personal desglosado (nombre, cargo, partida, HH normales, HH extra y total) y equipos desglosados (equipo, partida, HM operativas, HM stand-by, estado), con las columnas que agrega la tanda O (**C parte después de incorporar `local-worker-3`**); los RDT viejos salen con extra = 0, stand-by = 0 y estado vacío («—») — prueba: unitaria con un parte nuevo y uno viejo.
- **C3**: avance por nivel (mapa DP), Curva S física (cargador de A6), PPC y causas, avance de una partida, Plan Maestro próximos 7 días.
- **C4**: `armar-datos-semanal.ts`: por actividad contractual, acumulado anterior, metrado por día o por semana, total del período, acumulado a la fecha y %; personal y equipos igual; programado contra real; indicadores del período; diarios emitidos; días sin diario (entran solo con datos del RDT) — prueba: acumulado anterior + período = acumulado a la fecha, y cuadra con la suma de los diarios.
- **C5**: formato Costos: EV, AC, CV, CPI, SPI; personal y equipos valorizados (HH o HM × tarifa congelada); **materiales** (su presupuesto × % de avance físico) y **subcontratos** (por avance físico o monto manual, que es su costo real) **ya dentro del AC** (R20): se leen de `proyecto_pr.costo_materiales_acum` y `costo_subcontratos_acum` que deja la tanda R y entran por `evm.ts`, sin cuenta propia; materiales ya no queda «Pendiente»; costo por partida con la fila «Materiales y subcontratos (sin partida)» para que cuadre; HH de MOI sin valorizar; las HH extra (recargo 1,25) y las HM stand-by ya vienen dentro del costo real — la función rechaza al rol sin economía — prueba: el AC del formato = AC del PR al mismo corte.
- **C6**: `congelar.ts`: foto fija con los valores del momento y su rotulación — prueba: cambiar el RDT después no cambia el resultado.
- **C7**: prueba transversal: recorrer la salida de todos los formatos distintos de `COSTOS` y fallar si aparece algún campo en dinero.

**Tanda D — Informes: API (W1, ola 2)**
- **D1**: `GET/POST informes` (listar con filtros; crear con período; copiar «Restricciones y pendientes» y «Próximas actividades» del último emitido).
- **D2**: `GET/PATCH/DELETE informes/[informeId]`.
- **D3**: `emitir` y `nueva-version`, con notificación `MENSAJE` a los miembros del servicio (menos el autor), visible en `/notificaciones`.
- **D4**: `formatos-usuario`.
- **D5**: `fotos-campo` (subir, banco del día, asignar a bloque, leer con URL firmada, borrar la propia).
- **D6**: avisos de semanal que se cruza y de días sin diario (campo `avisos` de la respuesta).
- **D7**: pruebas de ruta: 401, 403 por rol, 404 de borrador ajeno, 409 al editar un emitido, 400 de período fuera de límites **por llamada directa**, 403 de `COSTOS`; Skill `verificar-permisos-por-rol`.

**Tanda E — Informes: chips, listado, nuevo y foto de campo (W3, ola 3)**
- **E1**: `registro-accesos.ts`: el chip pasa a «Informes de supervisión» (informativo, `requiereServicio: 'si'`, panel derecho en Supervisión operativa y panel izquierdo grupo Reportes) y se agrega «Foto de campo» (acción: derecho, Accesos rápidos, Acciones del izquierdo); páginas `/proyectos/[id]/informes` y `/proyectos/[id]/informes/foto`; se conserva el id `informe-servicio` salvo que algo exija cambiarlo (se anota); `next.config.ts`: `geolocation=(self)` **solo si Victor aprueba P7** — prueba: `npm test` (cobertura y humo del registro) y fila en la matriz derivada. **Estado:** `Conforme` (evidencia en `resultados/E.md`); lo observado en vivo por rol lo cierra L.
- **E2**: listado con código, tipo, fecha o período, formato, autor, estado, versión, fotos y acciones; filtros; estados vacío, carga y error; tabla con scroll horizontal; los emitidos `COSTOS` no aparecen sin economía. **Estado:** `Observado`: sin captura ni datos reales (migraciones 098 a 102 posiblemente sin aplicar, P33; sin cuentas de prueba, P36); lo cierra L.
- **E3**: «Nuevo»: selector de formato (Costos deshabilitado con título), tipo, fecha o período con atajos, Desde/Hasta y resumen (días, trabajados, diarios emitidos, sin diario, columnas por día o semana), avisos de cruce. **Estado:** `Observado`: sin captura ni prueba contra base; lo cierra L.
- **E4**: «Foto de campo» (móvil): botón grande «Tomar foto» con `<input type="file" accept="image/*" capture="environment">` (un toque tras abrir el chip, P8), reducción a ~1600 px, servicio/actividad/descripción, GPS opcional, mensaje claro y reintento si no hay señal (sin cola sin conexión). **Estado:** `Observado`: la cámara con `capture` y el GPS necesitan un celular real (P8); lo confirma Victor o la tanda L.

**Tanda F — Informes: editor y vista (W3, ola 3)**
- **F1**: editor por bloques con vista previa de hoja A4 y los bloques de datos del sistema. **Estado:** `Observado`: la API no entregaba en el borrador los valores de los bloques de datos y la hoja solo muestra un aviso (corrección de API en W1; después W3 corrige la vista previa, P54); sin captura ni base (098 a 102 sin aplicar, P33; sin cuentas, P36); lo cierra L.
- **F2**: quitar, ocultar, agregar y reordenar bloques con botones y teclado (no solo arrastrar). **Estado:** `Conforme` (lógica, evidencia en `resultados/F.md`: `editor-utils.test.ts`); el recorrido real con teclado y captura lo cierra L.
- **F3**: bloques libres: texto, fotos (del banco del día), tabla, clima y turno, firmas. **Estado:** `Observado`: sin prueba contra base (P33, P36); las claves de `config` son la regla R41 y los exportes de G se alinean con ella (W1); lo cierra L.
- **F4**: período cambiable desde la barra, guardado automático del borrador, descarga (pdf/docx/xlsx; completo, resumen, fotos). **Estado:** `Observado`: sin base; el botón apunta a la ruta `descargar` de G, que dará 404 hasta incorporar G en `local-worker-3`; lo cierra L.
- **F5**: «Mis formatos» (guardar y usar). **Estado:** `Observado`: sin base ni sesión; lo cierra L.
- **F6**: vista de informe emitido (solo lectura), versiones, «Reemplazado» consultable, botones Emitir y Nueva versión con sus permisos. **Estado:** `Observado`: la vista, las versiones y las acciones por rol están probadas en código (13 roles, `accionesInforme`); el recorrido en vivo por rol lo cierra L. El visor de los valores congelados es genérico (la forma de `datos` por bloque no está documentada).

**Tanda G — Informes: descargas (W1, ola 3)**
- **G1**: instalar `docx`; `exportar/word.ts`. **Estado:** `Conforme` (evidencia en `resultados/G.md`); no probado en base.
- **G2**: `exportar/pdf.ts` con `pdfkit` y `hoja.ts`; marca de agua «BORRADOR»; fotos 2/4/6 por página. **Estado:** `Conforme` (evidencia en `resultados/G.md`); no probado en base.
- **G3**: `exportar/excel.ts`: una hoja por tabla y hoja «Fotos» con miniatura, descripción y partida. **Estado:** `Conforme` (evidencia en `resultados/G.md`); no probado en base.
- **G4**: ruta `descargar` con `alcance` completo/resumen/fotos y `maxDuration`. **Estado:** `Conforme` (evidencia en `resultados/G.md`); no probado en base.
- **G5**: medición con 20 fotos (ms y memoria) en PDF, Word y Excel; resultado en el resumen. **Estado:** `Conforme` (medido en `resultados/G.md`). La meta de ~4 MB por archivo no se alcanzó con fotos de prueba (6,0 MB): riesgo abierto para el Gate 2; la tanda L mide con fotos reales (G-H1).
- **G6**: pruebas: PDF leído con `pdf-parse`, `.docx` abierto como zip con la imagen incrustada, `.xlsx` releído con `exceljs`; los tres muestran los mismos datos que la vista previa. **Estado:** `Conforme` (evidencia en `resultados/G.md`); no probado en base.
- **G7**: descarga de `COSTOS` sin economía → 403 (por URL directa). **Estado:** `Observado`: la parte por ruta está `Conforme` (`descargar-rutas.test.ts`: 13 roles × 3 formatos × 3 alcances; COSTOS sin economía = 403). Lo visual por rol no se ha probado en pantalla: sin cuentas de prueba (P36); lo cierra la tanda L.

**Tanda H — Dashboard: responsable, % avance, IP y HH (W2, ola 1)**
- **H1**: etiqueta «Supervisor operativo a cargo» (color de Supervisión operativa) con la función de A1; sin asignar: «Sin supervisor a cargo».
- **H2**: % avance físico más grande con barra (ejecutado, marca en lo programado al corte, restante; sin Plan Maestro no hay marca), en ambos modos.
- **H3**: tarjetas IP (valor, HH ganadas y reales) y HH contractuales (barra de consumo, acumuladas con %, restantes) junto a la dona en Completo; en Parcial, tarjeta propia en la misma fila; sin cuadros dentro de SPI y CPI.
- **H4**: matriz con columnas HH contractuales, HH acumuladas e IP por partida (también en Parcial).
- **H5**: contorno punteado amarillo en tarjetas, paneles, detalle y matriz.
- **H6**: pruebas: IP y HH iguales al PR al mismo corte; en Parcial no hay dinero; la fila de tarjetas no crece.

**Tanda S — AC con materiales y subcontratos en las pantallas (W2, ola 1-2; tras H, con el cierre de R incorporado por el Worker git)**
- **S1**: el cargador compartido del Dashboard (`cargar-dashboard.ts`), `dashboard/page.tsx` y `pr/page.tsx` leen `costo_materiales_acum` y `costo_subcontratos_acum` de `proyecto_pr` y los pasan a `evm.ts` (R4) — prueba: unitaria, el AC del Dashboard es igual al del PR.
- **S2**: `costo-recursos.ts` (bloque «Costo real de recursos»): `TipoRecursoCosto` suma `material` y `subcontrato`, con filas de `pr_recursos.costo_acumulado`; la fila «Sin resolver» sigue en 0 cuando todo cuadra (hoy el bloque supone Σ mano de obra + equipos = AC, que dejará de ser cierto) — prueba: unitaria.
- **S3**: Reporte del proyecto (`pr/page.tsx`): el KPI AC muestra el desglose personal, equipos, materiales y subcontratos, y la tabla por partida suma la fila «Materiales y subcontratos (sin partida)» para que cuadre con el AC total — prueba: captura con las dos cuentas, escritorio y 390 px.
- **S4**: prueba (c) de R5 con el cargador real y un servicio de prueba: AC del PR = último punto de la Curva S = AC del Dashboard; la igualdad con el AC del formato Costos (C5) se comprueba en L7 — prueba: unitaria y captura.

**Tanda I — Dashboard: gráficas (W2, ola 1)**
- **I1**: función pura `avance-por-nivel.ts` (partidas agrupadas por `servicio_encabezados`; programado con asignaciones del Plan Maestro al corte, real con RDT validados) — prueba unitaria.
- **I2**: gráfica de barras verticales con selector de nivel, clic para bajar un nivel y ruta para volver; «Pendiente» sin Plan Maestro aprobado.
- **I3**: función pura `recursos-contractual-acumulado.ts` desde `pr_recursos` (HH y HM; exceso en rojo) — prueba: suma igual al PR.
- **I4**: gráfica de recursos con pestañas HH, HM, Subcontratos; Subcontratos solo en Completo, deshabilitada con título en Parcial; la pestaña usa el acumulado de la tanda N (por avance físico o monto manual de cada subcontrato) y **ya no queda «Pendiente»**; HM incluye el stand-by (cuenta contra lo contractual).
- **I5**: leyenda que oculta/muestra series; globos accesibles con mouse, teclado y toque; todo valor también en etiqueta o matriz.
- **I6**: clic en cargo o equipo → en qué partidas se usó (`dashboard/recurso-partidas`, solo horas).
- **I7**: capturas en escritorio y 390 px; estados vacío, carga y error.

**Tanda J — Dashboard: detalles e interacciones (W2, ola 1)**
- **J1**: detalle bajo la fila para cada tarjeta (% avance, BAC, PV, EV, AC, SPI, CPI, IP, HH, PPC) que abre y cierra al volver a tocar.
- **J2**: botón de cada detalle que lleva a la gráfica o matriz correspondiente; filas de partida tocables.
- **J3**: «Partida en revisión»: franja fija «Revisando partida …» (avance, IP y CPI solo en Completo), fila resaltada «En revisión», demás barras atenuadas; «Quitar» y Escape.
- **J4**: clic en la dona (Mano de obra, Equipos) lleva la gráfica de recursos a su pestaña; clic en «Desempeño por partida» marca la matriz.
- **J5**: en Parcial las tarjetas de dinero no existen y ningún detalle muestra dinero — prueba que recorre la salida.
- **J6**: teclado (Tab, Enter, Espacio, Escape) y toque.
- **J7**: capturas de cada detalle y de la franja.

**Tanda K — Dashboard: descarga (W2, ola 1)**
- **K1**: ruta `dashboard/descargar` (modo desde el servidor; corte desde el filtro).
- **K2**: PDF A4 horizontal con `pdfkit`: lo que se ve, Curva S en hoja aparte (Completo: económica y física; Parcial: solo física) y matriz; gráficas dibujadas como vectores (`src/lib/pdf/graficos.ts` nuevo).
- **K3**: Excel: una hoja por bloque y las series de la Curva S.
- **K4**: botón «Descargar» (PDF/Excel) con carga y error.
- **K5**: prueba: en Parcial ni el PDF ni el Excel contienen dinero.
- **K6**: medición de tiempo y `maxDuration`.
- **K7**: archivos abiertos y capturas.

**Tanda L — Integración y verificación en vivo (W3, tras F y G)**
- **L1**: tabla de permisos por rol observada (Skill `verificar-permisos-por-rol`, suplantación `ver-como` y llamadas sin efecto) para informes, fotos, Costos, descargas y transición.
- **L2**: recorrido Playwright de A (diario y semanal, tres formatos y uno propio, emitir, versión 2), B y C con las dos cuentas.
- **L3**: 390 px de listado, nuevo, editor, foto de campo y Dashboard.
- **L4**: cada archivo descargado abierto y revisado contra la vista previa.
- **L5**: las migraciones 099, 098, 100, 101 y 102 (en ese orden; la 102 después de la 100 y la 101) se aplican antes de esta tanda (Orquestador, una por una, con verificador y autorización); aquí se comprueban.
- **L6**: lista para que Victor pruebe la cámara en un celular real.
- **L7**: el RDT con extra y stand-by, la pestaña Inasistencias y el subcontrato manual entran al recorrido y a la tabla de permisos observada, y se comprueba que el AC del PR, el de la Curva S, el del Dashboard y el del formato Costos coinciden al mismo corte (cuentas de prueba, 390 px).

**Tanda N — Subcontratos con dos formas de medir (W2, ola 1, antes de I)**
- **N1**: `db/101_pr_subcontrato_medicion.sql` (ver «Migraciones nuevas») y línea en `db/README.md`.
- **N2**: `src/lib/pr/subcontratos.ts` (función pura): acumulado, % y restante por modo (`FISICO` = contractual × avance físico del servicio, `MANUAL` = monto escrito); aviso si el monto pasa del contractual; rechazo de montos negativos — prueba: unitaria, incluido el ejemplo contractual 200 e ingreso 40 → 20 %.
- **N3**: `GET`/`PUT /api/proyectos/[id]/pr/subcontratos` con `puedeMedirSubcontratos` y alcance; guarda quién y cuándo y, al guardar, llama a `recalcularPr` (`acumulacion-rdt.ts`) para que el AC del PR use el monto nuevo — prueba: de ruta (403 sin economía, 400 de monto negativo, subcontrato ajeno al servicio, el acumulado lo calcula el servidor).
- **N4**: sección «Subcontratos» en el Reporte del proyecto (`pr/page.tsx`): desplegable «Por avance físico / Ingreso manual», campo de monto, % con barra, restante y la nota «el monto ingresado es el costo real del subcontrato», como en `mockups/pr-subcontratos-medicion.html` (referencia; la maqueta la prepara el Orquestador aparte); los roles sin economía no ven la sección — prueba: capturas con las dos cuentas y a 390 px.
- **N5**: el cargador del Dashboard (`cargar-dashboard.ts`) incluye los subcontratos con su acumulado (la gráfica de recursos de la tanda I lo consume) — prueba: unitaria.
- **N6**: `subcontratos.ts` exporta los casos de prueba de la cuenta (contractual 200 con ingreso 40 → 20 %; contractual 200 con avance físico 30 % → 60) para que la prueba de equivalencia de R5 compruebe que la cuenta SQL de la 102 da lo mismo; el AC del subcontrato **no** se calcula acá, lo calcula la tanda R en una sola función — prueba: unitaria.
- **N7**: prueba transversal: escribir un monto manual **no cambia el EV, el PV ni el BAC** del servicio y dispara el recálculo del PR; el cambio exacto del AC (monto − valor por avance físico) lo comprueba R5 (d) cuando exista la 102 — prueba: unitaria y de ruta.

**Tanda O — RDT: HH extra, HM stand-by y estado del equipo, datos y cálculo (W3, ola 1; parte de `main` al día)**
- **O1**: `db/100_rdt_extra_standby_estado.sql`: columnas `horas_extra`, `horas_standby`, `estado_equipo` (ver «Migraciones nuevas»); lo existente queda en 0 / vacío — prueba: revisión del archivo y base de prueba si Victor la indica.
- **O2**: `create or replace guardar_rdt_parte` (misma firma) partiendo del **cuerpo vigente en `main`**: lee `horasExtra` por persona y `horasStandby` y `estado` por equipo; rechaza extra > total de la persona, valores negativos y estados fuera de la lista — prueba: SQL contra base de prueba o prueba de texto como las de `reposicionamiento-sql*.test.ts`.
- **O3**: `create or replace recalcular_pr_desde_rdt`: costo HH = `tarifa × horas × (1 + 0,25 × extra_persona / total_persona)` (reparto proporcional); HM = `horas + horas_standby` en `hm_reales_acum`, costo, `pr_recursos.cantidad_acumulada` y `costo_acumulado` por cargo y equipo, balde legacy y aviso de tarifa; HH reales e IP no cambian; MOI sin valorizar — prueba: caso con extra y stand-by con la cuenta hecha a mano. Solo HH y HM: materiales y subcontratos los agrega la tanda R (102) sobre esta misma función.
- **O4**: la serie diaria de la Curva S (`db/070`: `ac_diario_hh` y `ac_diario_hm`) con la misma cuenta — prueba: el AC final de la Curva S es igual al AC del PR para el mismo corte (en este punto sin materiales ni subcontratos: la 102 los suma a las dos cuentas).
- **O5**: `src/lib/rdts/horas-extra.ts` (nuevo): `FACTOR_HH_EXTRA = 1.25`, normales = total − extra, HM total, `ESTADOS_EQUIPO`, validaciones — prueba: unitaria, y una prueba que lee `db/100*` y comprueba que el factor del SQL es el mismo.
- **O6**: `tipos.ts`, `plantilla.ts`, `parte.ts` y `borrador.ts`: campos nuevos opcionales; un borrador viejo (sin las claves) se abre con 0 y vacío; `api/rdts/partes` (POST y PATCH) valida en servidor — prueba: unitaria y de ruta (extra mayor que el total → 400, estado inválido → 400).
- **O7**: prueba de impacto: con RDT validados antiguos, AC, HH y HM del PR salen **idénticos** antes y después; con un parte nuevo, solo sube el AC por el recargo y las HM por el stand-by; el historial de correcciones conserva las columnas nuevas.
- **O8**: comparación con datos reales de PS-0011 (lectura): totales del PR antes y después de aplicar la 100 en la base de prueba o de desarrollo que indique Victor; resultado en el resumen.

**Tanda R — AC con materiales y subcontratos: migración 102, PR, Curva S y `evm.ts` (W3, ola 1; después de O, con el cierre de N incorporado por el Worker git)**
- **R1**: `db/102_ac_materiales_subcontratos.sql` (aditiva): columnas `proyecto_pr.costo_materiales_acum` y `costo_subcontratos_acum` y la función `ac_materiales_subcontratos_al_corte(p_proyecto_id, p_ev_acum, p_fecha)` que devuelve `materiales` y `subcontratos`. Avance físico = `p_ev_acum` / Σ `pr_partidas.bac` (0 si el BAC es 0; sin tope en 100 %). Materiales = Σ `costo_contractual` de `pr_recursos` tipo `material` × avance. Subcontratos, por fila tipo `subcontrato`: `FISICO` (o sin fila en `pr_subcontrato_medicion`) = `costo_contractual` × avance; `MANUAL` = `monto_manual` si `p_fecha` es el día (Lima) de `actualizado_en` o posterior, y si no, el valor `FISICO` (decidido, ver Registro de decisiones del 2026-10-15). Es la única cuenta: el PR y la Curva S la llaman — prueba: revisión del archivo y base de prueba si Victor la indica.
- **R2**: `create or replace recalcular_pr_desde_rdt` desde el **cuerpo que dejó la 100** (no desde `db/053`): al final llama a la función con `p_ev_acum` = Σ `metrado_acumulado × precio_unitario` y `p_fecha` = hoy (Lima), guarda las dos columnas de `proyecto_pr` y escribe `pr_recursos.costo_acumulado` de cada fila de material y subcontrato (el reinicio de `costo_acumulado` que hoy cubre `mano_obra` y `equipo` se amplía a los cuatro tipos). `pr_partidas.costo_real_acum` no cambia — prueba: caso con la cuenta hecha a mano (materiales 1 000 y subcontrato 200 con avance 30 % → 300 y 60).
- **R3**: `create or replace curva_s_proyecto` desde el cuerpo vigente tras la 100: `ac_acum` = HH + HM acumuladas (`ac_diario_hh` y `ac_diario_hm`, ya con extra y stand-by) + materiales + subcontratos de la función con el `ev_acum` de cada día — prueba: el último punto de la serie es igual al AC del PR al mismo corte.
- **R4**: `src/lib/pr/evm.ts`: `ProyectoEvmDatos` suma `costoMaterialesAcum` y `costoSubcontratosAcum`; el AC del proyecto = Σ partidas + legacy + ambos; el AC y el CPI por partida no cambian; CPI y EAC del proyecto usan el AC nuevo — prueba: unitaria.
- **R5**: **prueba de equivalencia** (`ac-equivalencia.test.ts` más un script SQL de comparación): (a) para los RDT ya validados, la parte HH/HM (Σ `costo_real_acum` + legacy) sale idéntica antes y después de la 102; (b) el AC total de un servicio existente **sí cambia**, y la prueba reporta el delta por componente (materiales, subcontratos) en vez de exigir AC idéntico; (c) AC del PR = último punto de la Curva S = AC que arma el cargador del Dashboard, al mismo corte; (d) escribir un monto manual de subcontrato cambia el AC exactamente en (monto − valor `FISICO` que tenía) y no cambia el EV; (e) los casos de `subcontratos.ts` (N6) dan lo mismo que la función SQL — prueba: la propia prueba.
- **R6**: lectura sobre PS-0011 y los servicios que indique Victor: AC antes y después de aplicar la 102 con el delta por componente; comprobar si Σ `pr_partidas.bac` es igual al BAC del Dashboard (suma de recursos) y, si no, reportarlo (P21) — resultado en el resumen de la tanda.

**Tanda P — RDT: formulario, borrador, PDF y consolidado (W3, ola 1-2)**
- **P1**: `FormularioCrearRdt.tsx`: por persona, campo «HH extra» (HH normales se calculan y se muestran); por equipo, «HM stand-by» y desplegable «Estado» (Operativo, Stand-by, Averiado, En mantenimiento); validación visible; sin cambiar lo demás — prueba: captura escritorio y 390 px.
- **P2**: el borrador guarda y restaura los campos nuevos y abre bien borradores viejos — prueba: unitaria y captura.
- **P3**: PDF del RDT (`exportador-parte-pdf.ts`, `partes/[id]/pdf`, `partes/pdf-borrador`): columnas de HH normales/extra y de HM operativas/stand-by/estado, sin dinero — prueba: PDF abierto y leído (el formato impreso de la empresa admite estas columnas: pregunta 5).
- **P4**: Consolidado (`consolidado.ts` y `api/rdts/consolidado`): muestra HH normales y extra y HM operativas y stand-by sin dinero; los totales de HH y HM incluyen todo — prueba: unitaria con `consolidado.test.ts`.
- **P5**: detalle, corrección de un RDT rechazado y listados conservan y muestran los campos nuevos — prueba: de ruta y captura.
- **P6**: ZIP, listado PDF y exportaciones existentes siguen funcionando — prueba: `npm test` completo.
- **P7**: recorrido Playwright: crear un RDT con extra y stand-by, validarlo y ver el AC en el PR; permisos: lo hacen los mismos roles que crean RDT — prueba: capturas.

**Tanda Q — Pestaña «Inasistencias» (W3, ola 3, tras E)**
- **Q1**: `src/lib/informes/inasistencias.ts` (puro): filtro diario o semanal con el control de período de `periodo.ts` (B4), agrupación y orden — prueba: unitaria con bordes.
- **Q2**: `GET /api/inasistencias` (ver «Contratos de API») — prueba: de ruta (401, 403 de servicio ajeno, 400 de período fuera de límite, el administrador ve todos, los 13 roles entran).
- **Q3**: `GET /api/inasistencias/pdf` con `pdfkit` y `hoja.ts`, filtro aplicado en el encabezado y hoja con «Sin inasistencias» si no hay — prueba: PDF leído con `pdf-parse`.
- **Q4**: pestaña «Inasistencias» en la pantalla de Informes (la crea E2): Diario/Semanal, Desde/Hasta, «Todos mis servicios» o un servicio, tabla con scroll horizontal, estados vacío, carga y error, botón PDF — prueba: capturas escritorio y 390 px. **Estado:** `Conforme` en código (`inasistencias-utils.test.ts`, 5 pruebas; `InformesPestanas.tsx` y `PestanaInasistencias.tsx`); `Observado` en las capturas de escritorio y 390 px: sin cuentas de prueba (P36) y migraciones 096 y 098 a 102 posiblemente sin aplicar; las cierra L (evidencia en `resultados/Q.md`).
- **Q5**: prueba de que ningún bloque ni formato de informe incluye inasistencias, y de que la pestaña no cambia el listado de informes. **Estado:** `Conforme` (`inasistencias-aislamiento.test.ts`; evidencia en `resultados/Q.md`).
- **Q6**: verificación con las dos cuentas: los 13 roles ven la pestaña, y solo dentro de sus servicios — prueba: tabla observada (Skill `verificar-permisos-por-rol`). **Estado:** `Conforme` en ruta, con suplantación de rol simulada (`inasistencias-roles.test.ts`: 13 roles x alcance); `Observado` en vivo con las dos cuentas: lo cierra L.

**Tanda M — Documentación (Documentador, tras L):** M1 flujo nuevo 22; M2 flujos 10, 11 y 21; M3 flujo 06 (campos nuevos del RDT, HH extra, HM stand-by y estado) y regla de costo (R20: todo suma al costo real; materiales y subcontratos por avance físico, subcontrato manual = monto ingresado; las HH extra y las HM stand-by entran al costo real; se anota que cambia la regla de septiembre y que el costo por partida no incluye materiales ni subcontratos); M4 flujos 08 y 14 (nota ³ y **las filas nuevas de las tablas 1 y 2**, ver «Filas del flujo 14»); M5 flujo 16 y árbol del panel izquierdo; M6 `design.md`; M7 índices y `scripts/verificar-referencias.py`; M8 traslado de las filas del libro con `trasladar-hallazgos`.

### Briefs de cada Worker

Se extraen a `2026-10-15-informes-supervision-y-dashboard-briefs/<tanda>.md` con la plantilla `13-brief-de-tanda.md` (≤ 8 KB cada uno). Contenido común: **rol y modelo** Sonnet medio, subagente «`Worker N · <tanda>`»; **rama/worktree** `local-worker-N`; **`.env.local`**: copiar el principal al worktree (autorizado siempre); **no leer** el plan completo, solo los flujos nombrados; **no tocar** `AGENTS.md`, flujos, estándar, el archivo del plan ni carpetas de otros Workers; **resumen de cierre** en `resultados/<tanda>.md` con los cinco grupos de hallazgos y una captura por ítem; **Skills**: `cerrar-tanda` siempre; **límites**: ~80 llamadas, a las ~60 cierra y escribe el traspaso; **conflicto de negocio**: se detiene y lo devuelve al Orquestador. Específico:

| Tanda | Qué leer (en orden) | Contrato verificado | Punto de corte si se acaban las llamadas |
|---|---|---|---|
| A | `datos/route.ts`, `confirmar-transicion/route.ts`, `dashboard/page.tsx`, `api/curva-s/route.ts`, `db/096`; flujos 08, 14 (nota ³) | El supervisor pasa a columna propia (099); sin columna hoy | A1–A4 / A5–A8 |
| B | `db/096`, `db/013`, `permisos.ts`, flujo 14; Spec (alcance A.8 y A.16) | Siguiente migración 098; RLS sin política | B1–B2 / B3–B5 |
| C | `lib/pr/evm.ts`, `db/026`, `db/053`, `lib/curva-s`, cargadores de A; flujos 06, 10, 11 | HH/HM por recurso en `pr_recursos`; sin stand-by ni extra; materiales y subcontratos en el AC desde la 102 (`proyecto_pr`) | C1–C3 / C4–C7 |
| D | tipos y funciones de B y C; `guard-proyecto.ts`; `notificaciones.ts` | Notificación tipo `MENSAJE` | D1–D4 / D5–D7 |
| E | `registro-accesos.ts`, `cobertura-pantallas.ts`, `panel-*.ts`, flujo 16, `design.md`, maqueta `informes-supervision.html` (Listado, Nuevo, Celular) | Chip inerte `informe-servicio` | E1–E2 / E3–E4 |
| F | tipos de B, API de D, maqueta (Editor), `design.md` | Contrato de D | F1–F3 / F4–F6 |
| G | datos de C y D3, `lib/pdf/hoja.ts`, `rdts/exportador-pdf.ts`, uso de `exceljs` en `rdts/exportar` | `pdfkit` + parche de fuentes; `docx` por instalar | G1–G3 / G4–G7 |
| H | `dashboard/page.tsx` ya refactorizada, `components/dashboard/**`, flujo 11, `design.md`, maqueta `dashboard-ip-hh-graficos.html` | IP y HH ya en `evm.ts` | H1–H3 / H4–H6 |
| S | **cierre de R incorporado**; `dashboard/page.tsx`, `pr/page.tsx`, `cargar-dashboard.ts`, `costo-recursos.ts`, `evm.ts` (R4) | `proyecto_pr.costo_materiales_acum` y `costo_subcontratos_acum`; el bloque de recursos supone Σ MO+HM = AC | S1–S2 / S3–S4 |
| I | `lib/dashboard/**`, `lib/niveles/agrupar-pantallas.ts`, `db/074`, `db/007` | el acumulado de subcontratos y materiales (`pr_recursos.costo_acumulado`) lo escribe la tanda R | I1–I4 / I5–I7 |
| J | componentes del Dashboard, maqueta | Parcial sin dinero | J1–J3 / J4–J7 |
| K | `lib/pdf/hoja.ts`, `cargar-curva-s.ts`, `cargar-dashboard.ts` | Modo desde el servidor | K1–K3 / K4–K7 |
| L | Skill `verificar-permisos-por-rol`, cuentas de prueba (de la memoria; no se copian al repositorio) | — | L1–L3 / L4–L6 |
| N | `pr/page.tsx`, `lib/pr/evm.ts`, `db/007`, `db/060`, `mockups/pr-subcontratos-medicion.html`, flujos 10 y 14 | `pr_recursos` sin ligadura a partidas; avance físico = EV/BAC; el monto manual es costo real (R20) pero la cuenta del AC la hace la tanda R, no N; el servidor llama a `recalcularPr` | N1–N3 / N4–N7 |
| O | **`main` al día primero** (`git merge main`); `db/053`, `db/054` y la definición vigente de `guardar_rdt_parte`, `db/070`, `src/lib/rdts/{parte,plantilla,tipos,borrador,consolidado,real-por-clave}.ts`; flujos 06 y 10 | Extra 1,25; stand-by suma a costo y a consumo de HM; RDT viejos en 0 | O1–O4 / O5–O8 |
| R | **`local-worker-3` con O cerrada y el cierre de N de `local-worker-2` incorporado**; la definición vigente de `recalcular_pr_desde_rdt` y `curva_s_proyecto` tras la 100; `db/007`, `db/101`, `src/lib/pr/evm.ts`, `src/lib/pr/acumulacion-rdt.ts`; flujos 10 y 11 | `pr_recursos` sin partida (la cuenta es a nivel servicio); EV/BAC; las dos funciones del AC; el PR no suma materiales ni subcontratos hoy | R1–R3 / R4–R6 |
| P | `FormularioCrearRdt.tsx`, `exportador-parte-pdf.ts`, `consolidado.ts`, `borrador.ts`, `design.md` | Campos de O | P1–P3 / P4–P7 |
| Q | `rdt_partes.inasistencias` (db/096), `lib/rdts/borrador.ts`, `periodo.ts` (B4), pantalla de Informes (E2), `lib/pdf/hoja.ts` | 13 roles, dentro del alcance | Q1–Q3 / Q4–Q6 |

### Prompt del Auditor

Alcance: tandas A a S y M. **Primer chequeo:** con `git log` y `git branch --contains` confirmar que los commits están en `local-worker-1`, `-2` y `-3` (no en `main`). **Segundo:** ninguna fila del libro de hallazgos en `Registrada` y destinos con commit. Luego verificar: (1) migraciones 098 a 102 aditivas, con RLS sin política en las tablas nuevas, trigger de inmutabilidad en informes, y que no tocan la 095; (1b) que la parte HH/HM de los RDT existentes quedó idéntica (tras la 100, AC, HH y HM del PR antes y después; tras la 102, el AC total cambia solo por materiales y subcontratos, con el delta por componente reportado) y que el AC del PR, el último punto de la Curva S y el del Dashboard y del formato Costos coinciden al mismo corte, con una sola función compartida y sin que dos migraciones de Workers distintos redefinan la misma función; (1c) que el subcontrato manual cambia el AC exactamente en (monto − valor por avance físico) y no cambia el EV, el PV ni el BAC; (1d) pestaña Inasistencias con alcance por servicio para los 13 roles y las filas de las tablas 1 y 2 del flujo 14 incorporadas; (2) cada ruta nueva valida sesión, rol y alcance en servidor, y `COSTOS` da 403 sin economía al crear, ver, emitir y descargar; (3) límites del período también por llamada directa; (4) ningún formato distinto de Costos, ni el Dashboard Parcial descargado, contiene dinero; (5) restricción C por llamada directa; (6) Dashboard: IP, HH y recursos coinciden con el PR y AC con materiales y subcontratos según R20; (7) Punch List completa con evidencia; (8) tabla «dice hoy / pasaría a decir» aplicada en todos los documentos, flujo 22 creado y enlazado, `design.md` con el punteado; (9) se usaron los Skills citados; (10) la lista de filas nuevas para la Matriz de permisos está entregada a Victor. Formato `06-informe-auditoria.md`, en `02-trabajo-activo/04-auditoria/2026-10-15-informes-supervision-y-dashboard.md`, con APLICAR AHORA / PROPONER A RESPONSABLE / NO PROMOVER / PROPONER SKILL; clasifica la lista de observaciones sobre la política. No implementa ni aprueba.

### Archivos / componentes afectados

App (`py_control_proyectos_web`): `db/098_informes_supervision.sql`, `db/README.md`; `src/lib/informes/**` (nuevo), `src/lib/proyectos/supervisor-operativo.ts` (nuevo), `src/lib/dashboard/**`, `src/lib/curva-s/cargar-curva-s.ts` (nuevo), `src/lib/pdf/graficos.ts` (nuevo), `src/lib/permisos/permisos.ts`, `src/lib/config/registro-accesos.ts`; `src/app/api/proyectos/[id]/{datos,confirmar-transicion,informes,fotos-campo,dashboard}`, `src/app/api/curva-s/route.ts`; `src/app/(workspace)/proyectos/[id]/{page.tsx,confirmar-transicion.tsx,dashboard/page.tsx,informes/**}`; `src/components/{dashboard,informes}/**`; `next.config.ts`; `package.json` y lockfile (`docx`). **Ampliaciones:** `db/099_supervisor_operativo_a_cargo.sql`, `db/100_rdt_extra_standby_estado.sql`, `db/101_pr_subcontrato_medicion.sql`, `db/102_ac_materiales_subcontratos.sql`, `src/lib/pr/evm.ts`; `src/lib/rdts/**` (incluida `horas-extra.ts` nueva), `src/app/api/rdts/{partes,consolidado}/**`, `src/components/ui/FormularioCrearRdt.tsx`; `src/lib/pr/subcontratos.ts` y `src/components/pr/**` (nuevos), `proyectos/[id]/pr/page.tsx`, `api/proyectos/[id]/pr/subcontratos`; `src/app/api/inasistencias/**`, `src/lib/informes/inasistencias.ts`.

Documentación (`pg_control_proyectos`): flujos 22 (nuevo), 06 (referencia **y campos nuevos del RDT**), 08, 10, 11, 14 (**tablas 1 y 2**), 16, 21, `design.md`, `docs/04-flujos-de-negocio/README.md`, `docs/README.md`, `docs/02-trabajo-activo/README.md`.

### Tabla «dice hoy / pasaría a decir» (la del Spec más lo hallado al planificar)

| Qué dice hoy | Qué pasaría a decir | Documento |
|---|---|---|
| «No dibuja la Curva S ni ninguna serie temporal.» | La pantalla sigue sin dibujarla; el archivo descargado incluye la Curva S en hoja aparte, con la fuente del flujo 21. | 11 y 21 |
| Indicadores del Parcial: «solo % avance físico». | El Parcial suma IP, HH contractuales, acumuladas y restantes. | 11 |
| Chip «Informe de servicio» inerte («Sin pantalla todavía»); el flujo 16 cuenta «28 chips: 22 con pantalla y 6 inertes» y «10 chips sin pantalla». | Chip activo «Informes de supervisión» y chip de acción «Foto de campo»; se corrigen los conteos. | 16 |
| `EN_PLANEACION` → `EJECUCION` valida solo Plan Maestro `APROBADO` y checklist completo (flujo 08, párrafos de la transición y de «Estructura de niveles»; flujo 14, nota ³). | Valida además supervisor operativo a cargo. | 08 y 14 |
| *(hallazgo)* El flujo 14 no tiene filas para informes, fotos de campo ni descarga del Dashboard. | Filas nuevas (lista abajo). | 14 |
| *(hallazgo)* El flujo 11 no define el responsable del servicio. | Etiqueta «Supervisor operativo a cargo» con la fuente única de Editar servicio. | 11 |
| *(hallazgo)* Los formatos Técnico y Semanal de la maqueta muestran HH extra y HM stand-by, que el RDT no guardaba. | Se muestran con los datos reales que agrega la tanda O (el RDT los guarda desde la migración 100). | 22 (nuevo) |
| Flujo 06: el RDT registra solo horas por persona y por equipo (`horas`, `tarifa_hm`). | El RDT registra además HH extra por persona (HH normales = total − extra), HM stand-by por equipo y un desplegable de estado del equipo (Operativo, Stand-by, Averiado, En mantenimiento); los RDT existentes quedan en 0 / vacío. | 06 |
| Flujo 10 y regla de costo (de septiembre): costo real = horas × tarifa; «materiales y subcontratos no suman al costo real» (y, antes, «por % de avance» sin fuente definida). | **Cambia esa regla (R20, Victor, 2026-10-15): todo suma al costo real.** Mano de obra = HH del RDT × tarifa (HH extra × 1,25); equipos = (HM operativas + HM stand-by) × tarifa; materiales = su presupuesto × % de avance físico del servicio; subcontrato por avance físico = contractual × % de avance físico; subcontrato con ingreso manual = el monto ingresado, que es su costo real. HH reales e IP no cambian; el EV, el PV y el BAC tampoco. Materiales y subcontratos entran al AC del servicio, no al de cada partida (no se pueden ligar a una). | 10 y regla de costo |
| Flujo 11: pestaña Subcontratos sin fuente de avance. | La pestaña lee el acumulado de cada subcontrato (por avance físico del servicio o por monto ingresado en el Reporte del proyecto); ya no queda «Pendiente»; el bloque «Costo real de recursos» incluye materiales y subcontratos. | 11 |
| Flujo 16: el chip «Informes de supervisión» no incluye inasistencias. | La pantalla de Informes lleva una pestaña «Inasistencias» (sin chip propio) que lee las inasistencias de los RDT. | 16 |
| Flujos 08 y 14 (nota ³): el supervisor a cargo se deduce del último miembro con rol. | El supervisor a cargo es una columna propia del servicio (`supervisor_operativo_id`); la transición lo exige y en ejecución se cambia pero no se vacía. | 08, 11 y 14 |

### Lo que actualizará el Documentador al cierre

Flujo nuevo **22 — Informes de supervisión** (estados, foto fija, avance validado, banco de fotos, formatos, código, período, descarga, notificación, pestaña Inasistencias); flujos 06 (campos nuevos del RDT), 08, 10, 11, 14, 16, 21 según la tabla; `design.md` (punteado amarillo de los recuadros del Dashboard); índices (`04-flujos-de-negocio/README.md`, `docs/README.md`, `02-trabajo-activo/README.md`); `scripts/verificar-referencias.py`. **Las filas de las tablas 1 y 2 del flujo 14 las incorpora el Documentador en la tanda M4** (el artefacto «Matriz de permisos» no abre desde esta cuenta, P12; Victor lo actualiza cuando pueda con la misma lista).

#### Filas del flujo 14 (orden de columnas: Admin, JP, JOT, SOT, Plnr, SCo, JCo, SOp, SLog, SAdm, SSO, Asist, RRHH)

**Tabla 1 — Interfaces**

| Interfaz | Económico | Admin | JP | JOT | SOT | Plnr | SCo | JCo | SOp | SLog | SAdm | SSO | Asist | RRHH |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Informes de supervisión: ver emitidos (dentro de servicios asignados) | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Informe de formato Costos: ver | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| Informes: pestaña Inasistencias (dentro de servicios asignados) | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Banco de fotos del día | No | ✓ | ✓ | ✓ | — | — | — | — | ✓ | — | — | — | — | — |
| Reporte del proyecto: sección Subcontratos | Sí | ✓ | ✓ | ✓ | — | — | ✓ | ✓ | — | — | — | — | — | — |
| RDT: campos HH extra, HM stand-by y estado del equipo (ver) | No | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |

**Tabla 2 — Acciones** (la columna «Requiere OT» sigue la del flujo 14)

| Acción | Requiere OT | Roles con ✓ |
|---|---|---|
| Crear, editar su borrador y emitir un informe (formatos que no son Costos) | Sí | Admin, JP, JOT, SOp |
| Crear, emitir y ver un informe de formato Costos | Sí | Admin, JP, JOT, SCo, JCo |
| Emitir una versión nueva de un informe ajeno | Sí | Admin, JP |
| Guardar «Mis formatos» (los cuatro de crear informe) | No | quien crea informes |
| Tomar y subir foto de campo | Sí | Admin, JP, JOT, SOp |
| Descargar un informe emitido (el de Costos solo los 5 con economía) | No | los 13 (Costos: Admin, JP, JOT, SCo, JCo) |
| Descargar las inasistencias en PDF | No | los 13 |
| Descargar el Dashboard (Parcial sin dinero; Completo solo los 5 con economía) | No | los 13 (Completo: Admin, JP, JOT, SCo, JCo) |
| Elegir la forma de medir y escribir el monto de un subcontrato en el Reporte del proyecto | Sí | Admin, JP, JOT, SCo, JCo |
| Registrar HH extra, HM stand-by y estado del equipo en el RDT | Sí | Admin, JP, JOT, SOp (igual que Crear RDT estructurado) |

Editar servicio (asignar el supervisor a cargo con campo propio) no lleva fila nueva: se agrega solo una nota a la fila existente.

### Punch List embebida

Evidencia general: `npm test`/`lint`/`build`/`tsc` por tanda; una captura por ítem en el resumen de cierre.

| ID | Ítem verificable | Evidencia |
|---|---|---|
| PL-01 | A1–A7: una sola resolución del supervisor; transición bloqueada por API y por botón; refactors sin cambio visible | pruebas + capturas antes/después |
| PL-02 | 098 aditiva, RLS sin política, trigger de inmutabilidad, contadores sin repetidos | revisión del archivo + prueba en base de prueba |
| PL-03 | Permisos nuevos por rol (13 roles) | tabla observada + pruebas unitarias |
| PL-04 | Períodos: atajos y límites por pantalla y por llamada directa | pruebas unitarias y de ruta |
| PL-05 | Bloques de datos coinciden con RDT y PR; lo no validado rotulado | prueba + comparación manual |
| PL-06 | Semanal: anterior + período = acumulado, cuadra con diarios | prueba |
| PL-07 | Borrador solo del autor; emitido congelado; versión 2 deja la 1 «Reemplazada» consultable | pruebas de ruta + captura |
| PL-08 | Foto de campo: sube desde 390 px, llega al banco, se ubica en un bloque; fallo de subida con reintento | capturas |
| PL-09 | Descargas PDF/Word/Excel abren y coinciden con la vista previa; 20 fotos medidas | archivos abiertos + tiempos |
| PL-10 | Sin dinero en formatos no Costos ni en el Dashboard Parcial descargado | prueba que recorre la salida |
| PL-11 | Costos: supervisor operativo deshabilitado con título, no lo ve en la lista, 403 directo al crear, ver, emitir y descargar | tabla + llamada directa |
| PL-12 | Dashboard: responsable, % con barra, IP y HH sin agrandar la fila, matriz con columnas nuevas | capturas Completo y Parcial |
| PL-13 | Gráfica por nivel (bajar nivel, «Pendiente») y de recursos (suma igual al PR; subcontratos según decisión) | capturas + prueba |
| PL-14 | Detalles de las tarjetas, partida en revisión, Escape, teclado y toque | capturas |
| PL-15 | Descarga del Dashboard con Curva S, corte y modo correctos | archivos abiertos |
| PL-16 | **Por defecto, pantalla nueva:** entrada del acceso en el registro y la prueba de cobertura pasa | `npm test` |
| PL-17 | Chips en los paneles declarados, informativo o acción | captura |
| PL-18 | Conserva `?proyectoId=` en ambos paneles y preselecciona el servicio | captura + URL |
| PL-19 | Cuenta con permisos altos y cuenta sin administración: habilitado o deshabilitado con título | tabla + captura |
| PL-20 | URL directa sin permiso: el servidor la rechaza | URL + resultado |
| PL-21 | Fila en la matriz derivada del flujo 14 y lista entregada a Victor | diff |
| PL-22 | Móvil 390 px, scroll horizontal de tablas, estados vacío, carga y error, en Informes y Dashboard (modos Completo y Parcial) | capturas |
| PL-23 | Restricción C con las tres combinaciones (falta Plan, checklist o supervisor) y el paso feliz | respuesta 400 / 200 |
| PL-24 | Documentación aplicada y referencias verificadas | `verificar-referencias.py` |
| PL-25 | Supervisor a cargo en columna propia: relleno de la 099, cambiar sí / vaciar no en ejecución, rol validado en servidor | prueba de ruta + llamada directa |
| PL-26 | RDT con HH extra, HM stand-by y estado: guardado, borrador, PDF, consolidado y detalle | capturas + PDF leído |
| PL-27 | Tras la 100: RDT existentes idénticos (AC, HH y HM del PR). Tras la 102: parte HH/HM idéntica, delta del AC por componente (materiales, subcontratos) reportado, y AC del PR = AC de la Curva S = AC del Dashboard y del formato Costos al mismo corte | prueba de equivalencia (R5) |
| PL-28 | Subcontratos en las dos formas (físico y manual), solo los 5 roles con economía, monto negativo rechazado, aviso sobre el contractual; el monto manual cambia el AC en (monto − valor por avance físico) y no cambia el EV | prueba de ruta + R5 (d) + capturas con 2 cuentas |
| PL-29 | Pestaña Subcontratos del Dashboard sin «Pendiente»; Parcial sin dinero y con la pestaña deshabilitada | capturas |
| PL-30 | Pestaña Inasistencias: 13 roles dentro de su alcance, filtros diario y semanal, todos o un servicio, PDF; no aparece en los informes | tabla observada + PDF |
| PL-31 | Filas nuevas de las tablas 1 y 2 del flujo 14 incorporadas con ✓ y — por rol, y lista entregada a Victor para el artefacto | diff |

### Riesgos y bloqueos

- **Doble conteo del subcontrato (P13):** el avance por partidas (EV) ya incluye el trabajo subcontratado y el BAC incluye los subcontratos; por eso el subcontrato **no cambia EV, PV ni BAC**. Lo que sí cambia, por R20, es el **AC**: el subcontrato y los materiales suman al costo real del servicio (pregunta 2).
- **El costo real vive en dos cuentas SQL (PR y Curva S) más la lectura de `evm.ts` (P15, P19):** si una no cambia, el AC del PR y el de la Curva S dejan de coincidir. Lo cubren O4, O7, R3 y R5 con pruebas de igualdad. **Riesgo de pisarse:** la 100 (W3) y la 102 (W3) redefinen las mismas funciones; el dueño es W3 y la 102 parte del cuerpo que deja la 100. **Riesgo de datos:** con la 102 el AC total de todo servicio existente sube (materiales y subcontratos), por eso R5 pide el delta por componente y R6 lo mide en PS-0011. **Riesgo de pantalla:** el bloque «Costo real de recursos» supone Σ MO+HM = AC (S2 lo corrige).
- **Choque con el plan «Revisión completa de la app» (P17):** ese plan está en curso y ya cambió el RDT (`e0d00ff`: borrador, inasistencias, descarga, metrados en orden); deja pendientes de orden de metrados y alineación de columnas en Crear RDT, la 095 sin aplicar y archivos del DP sin commit. **Cómo se evita:** O y P parten de `main` al día (`git merge main` en `local-worker-3` antes de empezar y antes de cada commit/push); el Orquestador pide a ese plan congelar `src/lib/rdts/**`, `api/rdts/**`, `FormularioCrearRdt.tsx` y la numeración de `db/` mientras dure O/P (pregunta 6); se compara `git diff main` antes de cada commit; los números 098 a 101 están fijados y se re-verifican.
- **Relleno de `supervisor_operativo_id` (P17):** la 099 escribe datos (no solo estructura); se toma del último miembro supervisor y los servicios sin supervisor quedan en nulo sin retroceder de estado (pregunta 5).
- **Dependencia R → C entre ramas:** C2 lee `horas_extra`, `horas_standby` y `estado_equipo`, y C5 lee las columnas de AC de la 102; hay que incorporar `local-worker-3` en `local-worker-1` al cerrar R (que va después de O y antes de P), antes de C.
- **Refactor del Dashboard y de la Curva S (A5, A6):** riesgo de regresión visible; se cubre con comparación antes/después y va en la primera tanda.
- **Tiempo de PDF y Word con 20 fotos en Vercel:** se mide en G5; el tope del plan de Vercel está por confirmar.
- **Cámara:** la cabecera `camera=()` puede no afectar a `capture` en un input de archivo (**no verificado**; lo confirma Victor en un celular real); el GPS sí necesita cambiar `geolocation` (P7).
- **Dependencia entre ramas** (A→W2; O→C; B, C, D→W3): requiere incorporar ramas de trabajo entre sí; autorizado en el Gate 1 (Worker git).
- **095 pendiente de despliegue:** las tablas nuevas ya cumplen su regla (RLS sin política, lectura por el servidor).
- **Fotos:** crecimiento del almacenamiento; reducción en el celular y tope de 3 MB.
- No hay script `type-check`: se usa `npx tsc --noEmit` y `next build` (por confirmar que `tsc` pasa limpio hoy).

### Preguntas para el Gate 1

Todas respondidas por Victor el 2026-10-15 (ver Registro de decisiones). Pendiente operativo, no de negocio: **el Planner ajusta las tandas a R20** (costo real de materiales y subcontratos en las tres cuentas SQL del AC —PR, Curva S y guardado—, el monto manual del subcontrato como costo real en la tanda N, y su prueba de equivalencia), y el Orquestador revisa el cambio antes de lanzar Workers. **Hecho el 2026-10-15** (tandas R y S, migración 102): queda la revisión del Orquestador y una pregunta nueva para Victor, que no bloquea la tanda A: **pregunta 8** — cómo se ve en la Curva S un subcontrato con ingreso manual en los días anteriores a su último cambio (propuesta del Planner: vale lo que daba el avance físico hasta ese día; alternativa: 0 hasta ese día), y si el avance físico lleva tope de 100 %. **Resuelta el 2026-10-15** sin preguntar a Victor, con su principio «si se gasta plata en algo es costo real» (ver Registro de decisiones).

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-16 | Tanda Q cerrada (W3, commit fec676c en `local-worker-3` del repositorio de la app); Q4 `Conforme` en código y `Observado` en capturas, Q5 y Q6 `Conforme` (Q6 por ruta con suplantación de rol); la prueba en vivo con las dos cuentas la hace L. Corrección de API en W1 (commit c99dc90, incorporada en `local-worker-3` en 9d8a97c): datos del borrador, fotos libres al quitar un bloque, banco de fotos por período del informe (F-H1, F-H4, F-H5) y claves de `config` alineadas (F-H2). Q-H1 ya estaba decidida (R32: la pestaña no exige «Desde ≥ inicio de ejecución»): no se consulta de nuevo a Victor. Documentación de la pestaña Inasistencias en los flujos 14 y 16 y en la matriz: tanda M. | Orquestador |
| 2026-10-16 | Tanda F cerrada (W3, commit 37a5ea8 en `local-worker-3`); F2 Conforme; F1, F3–F6 Observado, los cierran L. Decisiones del Orquestador a las preguntas de W3, todas dentro del contrato del plan (borrador = datos en vivo): (F-H1) el GET de un borrador devolverá también los datos de cada bloque calculados en vivo, con los mismos filtros de economía (corrección de API en W1); después W3 corrige la vista previa de la hoja; (F-H4) al quitar un bloque sus fotos quedan libres y al emitir no queda ninguna con un bloque inexistente (W1); (F-H5) el banco de fotos acepta `?informeId=` para ver el período completo del informe (W1); (F-H2) las claves de `config` definidas por F son las oficiales: los exportes de G se alinean (W1) y el Documentador las lleva al flujo de informes. | Orquestador |
| 2026-10-16 | Tanda G cerrada con su corrección (W1, commits 59111bc, e7ac566 y 3d144e6 en `local-worker-1`). G1 a G6 Conforme; G7 Conforme por ruta y Observado por pantalla (la cierra L); todo no probado en base. Decisión del Orquestador (G-H1 aceptada): fotos reducidas a 1000 px al incrustar; con fotos de prueba cada archivo pesa 6,0 MB, sobre el límite de ~4,5 MB de Vercel (por confirmar); la tanda L mide la descarga con fotos reales de campo (reducidas a 1600 px al subir) y si pasa de ~4 MB se baja el lado a ~800 px o la calidad, o se descarga por enlace; se lleva al Gate 2 como riesgo abierto. | Orquestador |
| 2026-10-16 | Tanda E cerrada (W3, commits 9851fbe y b455b98 en `local-worker-3`); E1 Conforme; E2–E4 Observado, los cierra L. Decisiones del Orquestador a las preguntas de W3: (E-H3) «trabajados» = días con parte RDT no rechazado, «diarios emitidos» = DIARIO emitido sin COSTOS y «sin diario» = trabajados sin diario emitido, como el Spec y la regla D6; el aviso del servidor usa otra definición y L comprueba que coincidan; (E-H4) los enlaces del listado dan 404 hasta que F entregue el editor; (E-H5) el conteo de fotos y los nombres de autor se consultan en la página (la API de listado no los devuelve): se acepta; «Descargar» en el listado y «Mis formatos» pasan a F. Excepción añadida por E en `cobertura-pantallas.ts` para `/informes/nuevo`. | Orquestador |
| 2026-10-16 | **Relevo 4 del Orquestador.** Worker git (Haiku) verificó con git: `local-worker-1` en 0369ab8, `local-worker-2` en 1d7c338 y `local-worker-3` en 93c5d45; las tres con árbol limpio, `0 0` contra origin y sin merge a medias. **Victor confirma el GPS de las fotos (P7):** `next.config.ts` pasa a `geolocation=(self)`, solo eso; la cámara no se toca hasta que pruebe en un celular. **Victor autoriza** (el clasificador había bloqueado la primera orden) incorporar `local-worker-1` (hasta 0369ab8) en `local-worker-3`. El verificador de acciones no se consultó: su hook sigue sin instalar y el merge es entre ramas de trabajo. Se lanza W1 · G. Las migraciones se preguntan solo antes de L. | Victor / Orquestador |
| 2026-10-16 | Tanda G entregada (W1, commits 59111bc y e7ac566 en `local-worker-1`); G1 a G7 Conforme, todo «no probado en base». El `local-worker-3` ya tiene D (merge 4c906e6, verificado por el Orquestador). Con 20 fotos de 2,5 MB cada archivo pesaba ~50 MB: no cabe en la respuesta de una función de Vercel (~4,5 MB, por confirmar). **Corrección G-H1 (decide el Orquestador):** reducir cada foto al incrustarla (1000 px, JPEG ~70) declarando `sharp` en `package.json`, y volver a medir. Aceptados: `resumen` y `fotos` con el contenido que propuso W1, importes sin símbolo, «BORRADOR» solo en el encabezado de Word y los archivos extra `fuente.ts` y `datos-prueba-test.ts`. Pendiente: las claves de `config` de los bloques sin forma definida las confirma E. | Orquestador |
| 2026-10-16 | Tanda D cerrada (W1, commits 8be999c y 0369ab8 en `local-worker-1`); D1 a D7 `Observado` con una sola causa: código hecho y probado con base simulada, y 098–102 sin aplicar; los cierra la tanda L. Decisiones del Orquestador a las preguntas de W1: (D-H1) crear COSTOS lo hacen los 5 roles con economía, como ya estaba decidido (R5); los otros formatos, los 4 roles; supervisor_costos y jefe_de_costos solo crean, editan, emiten y versionan COSTOS; (D-H2) los bloques sin fuente automática (semáforo, incidencias, logros y alertas) congelan lo que el usuario escribió, sin umbrales inventados; (D-H3) el diario exige Desde igual a Hasta, un bloque AVANCE_PARTIDA sin `config.wbs` impide emitir y un formato de usuario con bloques de Costos solo sirve como informe COSTOS; (D-H4) el banco de fotos del día muestra las fotos de todo el servicio; (D6) los días sin diario salen de los partes del RDT, como dice el Spec. | Orquestador |
| 2026-10-16 | Primera mitad de la tanda Q cerrada (W3, commit 93c5d45 en `local-worker-3`): Q1 `Conforme`, Q2 y Q3 `Conforme` con datos simulados, no probados en base (la 096 puede estar sin aplicar). Q se partió en dos mitades para no dejar ocioso a W3 mientras W1 hace D: Q4 a Q6 esperan a E y F. Decisión del Orquestador: la pestaña no exige "Desde ≥ inicio de ejecución" porque el contrato del plan fija solo tres límites (desde ≤ hasta, hasta ≤ hoy en fecha Lima y máximo 3 meses) y con "Todos mis servicios" no hay un único inicio. Desviación anotada: W3 aplicó la idea del Skill `verificar-permisos-por-rol` (prueba de ruta por los 13 roles, esperado contra observado) sin abrir su archivo; Q6 y la tanda L lo aplican completo, con suplantación de rol. | Orquestador |
| 2026-10-16 | Tanda C cerrada con su corrección (W1, commits e089e38, a8e85d2 y 8459b86 en `local-worker-1`). C1 a C7 Conforme; todo «no probado en base» (migraciones 098–102 sin aplicar; `cargarPartesRdt` sin probar contra base). Decisiones del Orquestador en la corrección: (C-H1) el acumulado del informe suma el metrado por el vínculo oficial `rdt_actividad_partidas` (db/053), como el PR, y no por el texto `wbs`, que solo se muestra; (C-H2) los indicadores «al corte» de un diario salen de la fecha del diario (avance, programado y SPI de la serie física de la Curva S; HH e IP de los partes VALIDADO hasta esa fecha), no del PR de hoy, en línea con la regla 9 de foto fija; quien arma el diario debe pasar `hoy` y la serie física (lo hace la tanda D). Nada de esto se consultó a Victor porque sigue lo ya decidido. | Orquestador |
| 2026-10-16 | Tanda S cerrada (W2, commit 1d7c338 en `local-worker-2`). S1 y S2 Conforme (no probados en base: las columnas existen cuando Victor aplique la 102); S3 y S4 Observado (sin capturas con las dos cuentas ni base con las migraciones aplicadas; las cierra la tanda L). El Orquestador acepta el cambio en `src/lib/dashboard/datos-descarga.ts` (carpeta propia de W2, para que el PDF y el Excel tengan el mismo AC que la pantalla); la franja de desglose sobre el pie del PR se confirma en la tanda L; la diferencia de BAC (P21) ya estaba anotada. W2 termina todas sus tandas (N, H, S, I, J, K). | Orquestador |
| 2026-10-16 | Tanda K cerrada (W2, commits 104887c y a4f0808 en `local-worker-2`); K1 a K6 Conforme; K7 Observado (sin cuentas de prueba, la cierra L). Se aceptan sin cambios: ruta `descargar` con `maxDuration = 60`, PDF A4 horizontal con la Curva S en hoja aparte, Excel por bloque. El Worker git incorpora el cierre de R en `local-worker-2` para la tanda S. | Orquestador |
| 2026-10-16 | **Briefs G, E, F, Q y L escritos** (Sonnet, esfuerzo medio, 8 KB o menos cada uno). Detalles derivados que decide el Orquestador: «Diario» en la pestaña Inasistencias es una sola fecha (hoy en Lima por defecto) y el DNI viene en la fila guardada de `rdt_partes.inasistencias` (plan, §«Verificado en la app»); la ruta `descargar` de G lleva `maxDuration = 60` explícito, igual que K, con el tiempo medido; el puerto de W3 es 3013; las capturas de L van a `03-evidencia/capturas/2026-10-15-informes-supervision-y-dashboard/`, una subcarpeta por tanda; el Worker git incorpora `local-worker-1` en `local-worker-3` dos veces (al cerrar D y al cerrar G, antes de L). El patrón de `exceljs` está en `src/lib/dp/exportador-excel.ts`, no en `rdts/exportar` como decía el plan. **Queda abierto:** el clasificador de permisos denegó dejar escrito en `E.md` el permiso para cambiar `geolocation=()` por `geolocation=(self)` en `next.config.ts` (P7, ya resuelta por Victor el 2026-10-15 según el Registro); mientras no se confirme con Victor, el brief de E dice que no se toque ese archivo. | Orquestador |
| 2026-10-15 | **Relevo 3 del Orquestador.** Victor fijó al Orquestador en Sonnet 5.5 con esfuerzo extra (xhigh) con `/model` y `/effort`, y pidió Sonnet con esfuerzo medio para el código y Haiku (esfuerzo extra) para lo simple. Estado verificado con git por el Worker git: `local-worker-1` en 3ce0a52, `local-worker-2` en 8e60ced, `local-worker-3` en 1247100; las tres con árbol limpio y sincronizadas con origin; solo la 3 contiene 34b8bbf. **Victor da el visto bueno al merge bloqueado** (34b8bbf → `local-worker-1`, conservando ambas líneas en `db/README.md`) y **decide que él aplica las migraciones 099, 098, 100, 101 y 102 a mano** (Claude le deja los `.sql` en orden y verifica después con consultas de solo lectura). Se lanzan en paralelo el Worker git (Haiku) para el merge y W2 · K. | Victor / Orquestador |
| 2026-10-15 | Tanda J cerrada (W2, commit 8e60ced en `local-worker-2`; W2 pasó a `node_modules` propio con `npm ci`). El Orquestador acepta: clic en cada barra de «Desempeño por partida» marca la partida y baja a la matriz; la tarjeta AC lleva a «Costo real de recursos»; el detalle de PPC va dentro del Bloque E. Relevo del Orquestador (contexto 294k). | Orquestador |
| 2026-10-15 | Tanda P cerrada (W3, commits 2d4b3e8 y 1247100 en `local-worker-3`); P1, P7 y las capturas pasan a la verificación en vivo (L). W3 termina su parte de la Ola 1. | Orquestador |
| 2026-10-15 | Victor autoriza subir a GitHub los archivos de este plan («sí, sube los archivos del plan»): el plan, la carpeta de briefs y resultados, y las maquetas con su índice, README y marco. Lo hace el Worker git en Haiku (Victor: «utiliza haiku para tareas simples»). | Victor |
| 2026-10-15 | Tanda I cerrada con su corrección (461a0f9). W2 sigue con J y K antes de S (S y C esperan que se incorpore el cierre de R; el merge en `local-worker-1` quedó bloqueado por el clasificador de permisos y se pidió el visto bueno de Victor). | Orquestador |
| 2026-10-15 | Tanda I entregada (W2, commits 6a1ed04 y 32334bd en `local-worker-2`); se devuelve con la corrección del modo Parcial (P40). Tanda R cerrada con su corrección de seguridad (34b8bbf). Tanda P lanzada en W3. | Orquestador |
| 2026-10-15 | Tanda R entregada (W3, commits a8f7089 y 2bbeb62 en `local-worker-3`); se devuelve con una corrección de seguridad (P37) antes de darla por cerrada. | Orquestador |
| 2026-10-15 | Tanda H cerrada (W2, commits dbe1a5e y b196a7a en `local-worker-2`). El Orquestador adelanta la tanda I antes de S en el carril de W2 (S espera el cierre de R; I no lo necesita), sin cambiar el contenido de ninguna tanda. | Orquestador |
| 2026-10-15 | Tanda O cerrada (W3, commit 3233b93 en `local-worker-3`). Corrección de B aplicada (3ce0a52: crear y emitir COSTOS = 5 roles con economía). Se incorpora el cierre de N (0e1d8f9) en `local-worker-3` antes de R; verificador ESCALAR 0,73, revisado por el Orquestador. W1 espera a R para la tanda C. | Orquestador |
| 2026-10-15 | Tanda B cerrada (W1, commits 1fa141d y 3cc7d94 en `local-worker-1`); se corrige el permiso de crear COSTOS a los 5 roles con economía (R5). | Orquestador |
| 2026-10-15 | Tanda N cerrada (W2, commits 2879b46 y 0e1d8f9 en `local-worker-2`); N4 Observado (sin capturas, se toman en la verificación en vivo). Las tres sesiones de la Ola 1 se cortaron por el límite de uso de la cuenta y se reanudaron a las 22:00 sin rehacer trabajo. | Orquestador |
| 2026-10-15 | Tanda A cerrada (W1, commits e65dcae, c0dd874 y 9ad0de7 en `local-worker-1`). El Orquestador acepta la línea extra en la adjudicación (P24) y corrige A3: solo se rechaza pasar de un supervisor a ninguno (R23). La 099 queda escrita y revisada, sin aplicar: el servidor de base de datos no conecta en esta sesión. | Orquestador |
| 2026-10-15 | **Gate 1 aprobado** («ya está todo concretado»). Todo suma al costo real según la tabla confirmada (R20): materiales y subcontratos por avance físico, subcontrato manual = monto ingresado; cambia la regla de septiembre. PDF del RDT con las columnas nuevas en el mismo formato (R21). El plan «Revisión completa de la app» deja de tocar los archivos del RDT mientras este plan los cambia. Reparto del recargo de HH extra por horas, inasistencias sin RDT rechazados y relleno inicial del supervisor desde el miembro actual: quedan como los planificó el Planner. Victor cierra la sesión; relevo del Orquestador. | Victor |
| 2026-10-15 | **Revisión del Orquestador aprobada y regla del costo real reafirmada.** Victor: «ya se había definido ese punto con el anterior orquestador, así debe quedar […] si se gasta plata en algo es costo real». La pregunta 8 no se le hace: el Orquestador la resuelve con ese principio — el subcontrato con ingreso manual vale en la Curva S lo del avance físico hasta el día de su último cambio y el monto desde ese día; materiales y subcontratos por avance físico **sin tope** en 100 %. R22 queda decidida. Se lanza la Ola 0. | Victor / Orquestador |
| 2026-10-15 | El Planner ajustó el Plan a R20: tandas nuevas R (migración 102, función compartida del AC, dueño W3) y S (pantallas, W2); N4, N6, N7 y C5 reescritas; 19 tandas y 124 ítems. Pendiente: revisión del Orquestador y pregunta 8 a Victor. | Planner |
| 2026-10-15 | «Ok a todo»: ampliaciones D (RDT), E (Inasistencias) y F (subcontratos) aprobadas. Subcontrato manual en el Reporte del proyecto, solo 5 roles con datos económicos, cuenta como avance y no como costo real. HM stand-by también cuentan en el consumo de HM. Se pide al Planner agregar las tandas al plan. | Victor |
| 2026-10-15 | Subcontratos con dos formas de medir: por avance físico (por defecto) o ingreso manual del monto (el sistema calcula el %). HH extra = tarifa × 1.25. HM stand-by suman al costo real. Estado del equipo con desplegable (Operativo, Stand-by, Averiado, En mantenimiento). Inasistencias e informes los ven los 13 roles. Todas las acciones nuevas se registran en las tablas del flujo 14. | Victor |
| 2026-10-15 | Respuestas al Gate 1: campo propio para el supervisor a cargo; con el servicio en ejecución se puede cambiar pero no vaciar; cámara con botón «Tomar foto»; GPS permitido solo para la propia app; aviso al emitir a los miembros del servicio; pre-autorizaciones del paso 7 aprobadas (datos y cuentas de prueba, aplicar la 098, ramas y carpetas de trabajo, incorporar ramas entre Workers); 3 Workers; el Orquestador sigue en Opus 5.5 y delega. HH extra, HM stand-by y estado del equipo **se implementan en este plan tocando el RDT** (ampliación D); inasistencias en **pestaña aparte** de Informes con filtro diario/semanal, todos los servicios o uno, y PDF; no van en los informes (ampliación E). Gate 1 queda abierto hasta aprobar D y E. | Victor |
| 2026-10-15 | **Spec aprobado.** La línea punteada amarilla queda en el Dashboard real; semanales que se cruzan se permiten con aviso y límites del período confirmados; % avance físico más grande y con barra. Queda abierto: supervisor con servicio en ejecución (cambiar sí, vaciar no). Se delega el Plan al Planner con Sonnet, esfuerzo medio. | Victor |
| 2026-10-15 | Tercera revisión: los cuadros de IP y HH dentro de las tarjetas SPI y CPI quedan comprimidos; se bajan al espacio libre del panel «Composición del costo», como tarjetas propias. | Victor |
| 2026-10-15 | Segunda revisión de maquetas: semanal con período configurable desde – hasta; todas las gráficas y las tarjetas de arriba con clic, no solo la dona; línea punteada amarilla en todos los recuadros; que se note más la partida que se está revisando. | Victor |
| 2026-10-15 | Revisión de maquetas: le gusta el informe y que el RDT se cargue solo; pide que el semanal sea acumulado, que cada formato tenga contenido distinto (uno con costos), desglosar personal y equipos, y gráficos del Dashboard interactivos. | Victor |
| 2026-10-15 | Respuestas al Spec: supervisor a cargo ya existe (uno por servicio); la descarga del Dashboard incluye Dashboard y Curva S; el informe emitido lo ven los 13 roles con el servicio asignado; sin aprobación previa en esta versión. | Victor |
| 2026-10-15 | Se activa el flujo con Orquestador. Objetivo dado por Victor: chip de informes del operativo (diario y semanal, fotos, descarga Word/PDF/Excel, formato definido y versátil, chip de cámara) y mejoras del Dashboard (responsable, IP, HH, dos gráficas con filtro, descarga con Curva S). Primero maquetas. | Victor |

## Mejoras (de trabajo)

| # | Hallazgo | Estado |
|---|---|---|
| M1 | El navegador de Playwright estaba ocupado por otra sesión; las capturas de las maquetas se hicieron con Chrome sin ventana (`chrome --headless=new --screenshot`). Sirve como respaldo cuando Playwright no está libre. | Registrada |
| M3 | El Orquestador afirmó que no había un responsable por servicio a partir de la semilla de la migración 045, sin mirar la pantalla Editar servicio, y Victor lo corrigió: el campo «Supervisor operativo a cargo» existe. Antes de proponer un campo nuevo, buscar en la app la etiqueta visible del dato (verificar antes de afirmar). | Registrada |
| M4 | El Planner dio la 097 como primera migración libre mirando solo `git status`; la 097 ya estaba en `main`. El Orquestador lo detectó con `ls db/` y `git log`. Al buscar el siguiente número de migración, listar la carpeta completa y no solo lo que está sin seguimiento. | Registrada |
| M2 | Para proponer chips en una maqueta sin cambiar las demás, el marco compartido `marco-tres-paneles.js` acepta ahora `window.MARCO_AJUSTE` (opcional). | Registrada |
| M5 | (tanda A) En los worktrees `node_modules` es un symlink y `npm run build` con Turbopack falla; la verificación de build se hace con `npx next build --webpack`. Pasado a los briefs siguientes. | Registrada |
| M6 | (tanda H) Correr `npm test` modifica `src/app/api/curva-s/__snapshots__/curva-s-route.test.ts.snap` (saltos de línea); los Workers lo restauran con `git checkout` antes de commitear. Conviene fijar `.gitattributes` o el modo de escritura del snapshot. | Registrada |
| M7 | (tanda K, K-H4) `pdfkit.dash(0, …)` lanza error; no llamarlo con longitud 0 y usar `dash` solo cuando aplica. Va a `docs/03-aprendizaje-continuo/` al cerrar. | Registrada |
| M8 | (tanda K, K-H3) La ruta `descargar` valida sesión, rol y alcance en servidor y luego usa `crearClienteAdmin()` para `cargarCurvaS` en ambos modos; está alineada con la forma del cierre de R (34b8bbf). No es observación de política; en modo físico no sale dinero. | Registrada |
| M9 | (tanda K, K-H1, verificación pendiente) La página del Dashboard (`dashboard/page.tsx`, líneas 124-125) y la descarga (`src/lib/dashboard/datos-descarga.ts`, línea 119) usan el mismo criterio: Completo solo si `tipo_dashboard` es COMPLETO y el rol tiene economía. L debe comprobar en vivo, con un rol con economía y `tipo_dashboard` = PARCIAL, que la página y el archivo descargado coinciden. | Registrada |
| M10 | (tanda S, S-H3) Reincidencia de M6: correr `npm test` reescribe el snapshot de `curva-s-route` (solo fin de línea); se restauró con `git checkout`. Va a `docs/03-aprendizaje-continuo/` al cerrar. | Registrada |
| M11 | (tanda C, C-H3) Quitar un enlace `node_modules` de Windows desde bash de Git con `cmd /c rmdir` no actúa: abre un cmd interactivo, y el `npm ci` siguiente corrió a través del enlace (EPERM a medias en el repositorio principal). Usar PowerShell (`cmd.exe /c "rmdir node_modules"`) y comprobar que `LinkType` esté vacío antes de `npm ci`. Va a `docs/03-aprendizaje-continuo/` al cerrar. | Registrada |
| M12 | (tanda C, C-H5) La prueba `modulos-huerfanos` exige que todo módulo nuevo de `src/lib` sea alcanzable; un cargador sin consumidor aún necesita al menos una prueba que lo importe. Va a `docs/03-aprendizaje-continuo/` al cerrar. | Registrada |
| M13 | (tanda Q, Q-H2) La ruta de inasistencias usa el cliente de servicio (`crearClienteAdmin()`) tras validar sesión, rol y alcance, y filtra por `proyectosACargo` a mano (el administrador sin filtro), igual que la Curva S. Nada que trasladar; anotado por si el Auditor lo revisa. | Registrada |
| M14 | (tanda Q, Q-H3) Un heredoc grande en Bash falló por comillas; con la herramienta Write no hay problema. Aprendizaje menor; va a `docs/03-aprendizaje-continuo/` al cerrar. | Registrada |
| M15 | (tanda D, D-H5, reincidencia de M14) Los heredocs de Bash con comillas y acentos fallaron dos veces («unexpected EOF»); la herramienta Write evita el problema. Un cliente de servicio falso en memoria (`fake-admin-test.ts`) permitió probar las 13 combinaciones de rol sin base. Va a `docs/03-aprendizaje-continuo/` al cerrar. | Registrada |
| M16 | (tanda E, E-H6) Un heredoc largo de Bash con comillas simples falló sin escribir nada; con archivos grandes conviene la herramienta Write (entorno Windows). Reincidencia de M14 y M15. Va a `docs/03-aprendizaje-continuo/` al cerrar. | Registrada |
| M17 | (tanda G, G-H3) Word, PDF y Excel salen de un único modelo (`armarDocumento` en `comun.ts`); la vista previa de E y F debe consumir ese mismo modelo para que «mismos datos» sea cierto por construcción. Destino: tandas E y F. | Registrada |
| M18 | (tanda F, F-H6) La regla de lint de hooks de React prohíbe mutar refs en el render: el guardado automático de F se arma desde los manejadores (cola de promesas) y no desde efectos. Va a `docs/03-aprendizaje-continuo/` al cerrar. | Registrada |
| M19 | (tanda Q, Q-H4) Las pruebas de PDF con `pdf-parse` superan 5 s cuando corre toda la suite en paralelo; el bloque de `inasistencias-route.test.ts` se fijó con timeout de 30 s. Va a `docs/03-aprendizaje-continuo/` al cerrar. | Registrada |

## Reglas de negocio acordadas en esta tarea

| # | Regla | Destino | Estado |
|---|---|---|---|
| R1 | Cada servicio tiene **un solo** supervisor operativo a cargo, el del campo de Editar servicio; toda pantalla que muestre al responsable operativo lo toma de ahí (Victor, 2026-10-15). | Flujo 11 (y 16 si se cita) | Registrada |
| R2 | La descarga del Dashboard incluye siempre el Dashboard y la Curva S, según el modo del rol (Victor, 2026-10-15). | Flujos 11 y 21 | Registrada |
| R5 | El formato de informe **Costos** solo lo crean y lo ven los 5 roles con datos económicos; los demás formatos no llevan dinero (Victor, 2026-10-15, aplicando la regla 2 del flujo 14). | Flujo nuevo 22 y flujo 14 | Registrada |
| R6 | El informe semanal es acumulado y su período es configurable (desde – hasta): por actividad, recurso y equipo muestra acumulado anterior, cada día (o cada semana si pasa de 10 días), el total del período y el acumulado a la fecha; se arma con los diarios emitidos del período; no antes del inicio de ejecución, no después de hoy, máximo 3 meses; un período que se cruza con otro semanal emitido se permite con aviso (Victor, 2026-10-15). | Flujo nuevo 22 | Registrada |
| R8 | Los recuadros del Dashboard (tarjetas, paneles, detalle y matriz) llevan contorno punteado amarillo en la app real; la tarjeta % avance físico va más grande y con barra ejecutado / programado / restante (Victor, 2026-10-15). | `design.md` y flujo 11 | Registrada |
| R7 | En el Dashboard, la partida elegida queda marcada como «en revisión» en toda la pantalla (franja fija, fila de la matriz, barras) hasta quitarla; las tarjetas de arriba abren su detalle (Victor, 2026-10-15). | Flujo 11 | Registrada |
| R4 | Un servicio no pasa de planeación a ejecución sin un supervisor operativo a cargo; validado en servidor (Victor, 2026-10-15). Verificado que hoy no existía. | Flujos 08 y 14 | Registrada |
| R3 | Un informe emitido lo ven los 13 roles con el servicio asignado; el borrador solo su autor. Sin aprobación previa en esta versión (Victor, 2026-10-15). | Flujo nuevo 22 y flujo 14 | Registrada |
| R9 | Propuesta del Planner: al emitir un informe se notifica a los **miembros del servicio** (menos el autor) con tipo `MENSAJE`; la app no tiene «seguir un servicio» (Plan, pregunta 7). | Flujo nuevo 22 y flujo 04/16 si se cita | Registrada |
| R10 | Propuesta del Planner: los bloques de personal y equipos muestran solo totales (HH, HM) porque el RDT no guarda HH extra, HM stand-by ni estado del equipo; derivar HH extra con la jornada sería regla nueva (Plan, pregunta 3). | Flujo nuevo 22 | Descartada: reemplazada por la decisión de Victor del 2026-10-15 (R13 y R14: el RDT guarda HH extra, HM stand-by y estado) |
| R11 | Propuesta del Planner: la pestaña Subcontratos muestra lo contractual y el acumulado «Pendiente» mientras el PR no tenga un % de avance económico (Plan, pregunta 2). | Flujo 11 | Descartada: reemplazada por la decisión de Victor del 2026-10-15 (R15: subcontratos con dos formas de medir) |
| R12 | Propuesta del Planner: sin columna nueva, «supervisor a cargo» sigue siendo el miembro con rol supervisor operativo asignado más recientemente, corrigiendo que reasignar al mismo no lo vuelva el actual (Plan, pregunta 4). | Flujos 08 y 11 | Descartada: reemplazada por la decisión de Victor del 2026-10-15 (columna propia, R1 y R4) |
| R13 | HH extra (Victor, 2026-10-15): el RDT registra por persona las HH extra del día; HH normales = total − extra. Las HH extra se valorizan a tarifa × 1,25 y entran al costo real; HH reales e IP no cambian. Propuesta del Planner: el recargo se reparte entre las actividades de la persona en proporción a sus horas (pregunta 1); MOI sin valorizar. | Flujos 06, 10 y regla de costo | Registrada |
| R14 | HM stand-by y estado del equipo (Victor, 2026-10-15): el RDT registra por equipo las HM stand-by, que suman al costo real y al consumo de HM contra lo contractual, y un estado con desplegable (Operativo, Stand-by, Averiado, En mantenimiento). Los RDT existentes quedan en 0 / vacío. | Flujos 06 y 10 | Registrada |
| R15 | Subcontratos (Victor, 2026-10-15): dos formas de medir, por avance físico (por defecto: contractual × % avance físico del servicio) o ingreso manual del monto acumulado (el sistema calcula el %). Se ingresa en el Reporte del proyecto por los 5 roles con datos económicos. ~~Cuenta como avance (valor ganado), no como costo real.~~ (reemplazado por R20: el monto manual es el costo real del subcontrato). La pestaña Subcontratos del Dashboard deja de quedar «Pendiente». | Flujos 10, 11 y regla de costo | Registrada |
| R16 | Inasistencias (Victor, 2026-10-15): pestaña aparte en Informes de supervisión que lee las inasistencias de los RDT, con filtro diario o semanal (desde – hasta), todos los servicios asignados o uno, y PDF; la ven los 13 roles dentro de sus servicios; no va dentro de los informes. | Flujos 22 y 16 | Registrada |
| R17 | Propuesta del Planner: las inasistencias se leen solo de partes que no estén `RECHAZADO`, con los límites de período del semanal (pregunta 3). | Flujo 22 | Registrada |
| R18 | Propuesta del Planner: el valor ganado del subcontrato solo se muestra y no se suma al EV, PV ni BAC del servicio, para no contarlo dos veces (pregunta 2). Aceptada por el Orquestador: el EV del servicio ya incluye el trabajo subcontratado por el avance de cada partida. | Flujos 10 y 11 | Registrada. Nota (R20): el EV, el PV y el BAC siguen sin cambio; lo que cambia es el AC, que ahora sí suma el subcontrato y los materiales |
| R20 | **Todo suma al costo real** (Victor, 2026-10-15: «todo debe sumar a todo, para realizar bien los cálculos finales»; confirmado con la tabla): mano de obra = HH del RDT × tarifa (HH extra × 1.25); equipos = HM operativas + stand-by × tarifa; **materiales** = su presupuesto × % de avance físico; **subcontrato por avance físico** = contractual × % de avance físico; **subcontrato con ingreso manual** = el monto ingresado (pasa a ser su costo real). **Cambia la regla de septiembre** «materiales y subcontratos no suman al costo real» y reemplaza la parte de R15 que decía que el monto manual era avance. | Flujo 10 (cálculo del AC), flujos 11 y 21, regla de costo | Registrada |
| R21 | PDF del RDT: las columnas nuevas (HH normales/extra, HM stand-by, estado) van **dentro del mismo formato impreso** PROM-GP-002 (Victor, 2026-10-15). | Flujo 06 | Registrada |
| R22 | **Cuenta del costo real de materiales y subcontratos (decidida al aplicar R20, 2026-10-15):** se calcula solo a nivel servicio (los materiales no se pueden ligar a una partida, porque `pr_recursos` y `dp_recursos` no tienen partida), con avance físico = EV / BAC sin tope; el costo real por partida no incluye materiales ni subcontratos; en la Curva S, el subcontrato con ingreso manual entra con su monto desde el día de su último cambio y antes de ese día vale lo que daba el avance físico; sin tope en 100 %. | Flujo 10 (cálculo del AC) | Registrada |
| R19 | Las interfaces y acciones nuevas (informes, formato Costos, foto de campo, inasistencias, campos nuevos del RDT, subcontrato manual, descargas) se registran como filas en las tablas 1 y 2 del flujo 14, con la lista exacta de este Plan (Victor, 2026-10-15). | Flujo 14 | Registrada |
| R23 | (tanda A, decidido por el Orquestador aplicando la regla de Victor «en ejecución se cambia, no se vacía») «Vaciar» = quitar un supervisor que estaba asignado. Un servicio que ya estaba en ejecución **sin** supervisor (el relleno de la 099 no encontró a nadie) se puede seguir editando; solo se rechaza pasar de un supervisor a ninguno. Además, al crear el servicio desde la adjudicación se guarda el supervisor a cargo. | Flujo 08 y nota ³ del flujo 14 | Registrada |
| R24 | (tanda K, K-H2) La descarga del Dashboard (PDF y Excel, ruta `dashboard/descargar`) necesita fila en el flujo 14 y en la matriz de permisos: 13 roles; el dinero solo con economía y Dashboard Completo. | Flujo 14, matriz de permisos y flujo 11 | Registrada |
| R25 | (tanda K, K-H5, decidido por el Orquestador) El parámetro `corte` de la ruta de descarga es una fecha AAAA-MM-DD (la del filtro ya resuelta), no el preset. La Curva S del archivo recorta EV y AC al corte elegido; hoy `cargarCurvaS` usa la fecha de hoy para su rango. | Flujo 11 | Registrada |
| R26 | (tanda S, S-H1, aceptado por el Orquestador) La descarga del Dashboard (PDF y Excel, `src/lib/dashboard/datos-descarga.ts`) arma el AC con el mismo helper que la pantalla, para que PDF, Excel y pantalla den el mismo AC (materiales y subcontratos incluidos). | Flujo 11 (descarga) | Registrada |
| R27 | (tanda S, S-H4) BAC: `evm.ts` usa Σ `pr_partidas.bac` y `calcularBac` de `dashboard.ts` suma los recursos; no se midió diferencia ni se corrigió. Ya anotada como P21, sin acción en esta tanda. | Anotado, sin acción (ver P21) | Registrada |
| R28 | (tanda S, S2 y S3) El PR (flujo 10) muestra el desglose del AC (personal, equipos, materiales, subcontratos y sin resolver) en una franja sobre el pie, y una fila «Materiales y subcontratos (sin partida)» con su AC en las columnas 16 y 21. Pendiente para el Documentador final. | Flujo 10 (PR) | Registrada |
| R29 | (tanda S, S2) El bloque de recursos del Dashboard («Costo real de recursos») incluye materiales y subcontratos: los cuatro tipos suman y «Sin resolver» vale 0 cuando las cuatro clases están resueltas. Pendiente para el Documentador final. | Flujo 11 (Dashboard) | Registrada |
| R30 | (tanda C, C-H1, resuelta por el Orquestador) El acumulado del informe (diario y semanal) suma el metrado por el vínculo oficial `rdt_actividad_partidas` (db/053), igual que el PR; el texto `rdt_actividades.wbs` solo se muestra. Una actividad con texto 9.9 vinculada a 1.2 suma a 1.2 (diario, avance de partida y semanal). | Flujo nuevo 22 (informes); flujo 06 si corresponde | Registrada |
| R31 | (tanda C, C-H2, resuelta por el Orquestador, en línea con la regla 9 de foto fija) Los indicadores «al corte» de un diario salen de la fecha del diario: avance, programado y SPI de la serie física de la Curva S en esa fecha; HH ganadas, HH reales e IP de los partes VALIDADO hasta esa fecha. Un diario de hoy sale igual que antes. Quien arma el diario pasa `hoy` y la serie física. Límite: las HH legacy sin partida no se reconstruyen por fecha. | Flujo nuevo 22 (informes); flujo 06 si corresponde | Registrada |
| R32 | (tanda Q, Q-H1, pregunta para Victor) La pestaña Inasistencias valida desde ≤ hasta, hasta ≤ hoy (fecha de Lima) y máximo 3 meses, pero no exige «Desde ≥ inicio de ejecución», que sí pide R6 para el semanal y R17 remite a esos mismos límites. Motivo: con «Todos mis servicios» no hay un solo inicio de ejecución. Si Victor quiere el límite de inicio, solo aplicaría a un servicio concreto. Decisión del Orquestador (2026-10-16): se mantiene sin ese límite; el contrato de rutas del plan lista solo los tres límites y un período anterior al inicio de ejecución devuelve una lista vacía, sin riesgo. Si Victor quisiera el límite para un servicio concreto, es un cambio pequeño en `inasistencias-consulta.ts`. | Flujo nuevo 22 (pestaña Inasistencias) | Registrada. Resuelta por el Orquestador |
| R33 | (tanda D, D-H1, resuelta por el Orquestador) El formato Costos lo crean los 5 roles con datos económicos (administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos y jefe de costos), como ya decía R5. Los demás formatos (técnico, ejecutivo, fotográfico y personalizado) los crean los 4 roles de supervisión y dirección (administrador, jefe de proyectos, jefe de oficina técnica y supervisor operativo). El supervisor de costos y el jefe de costos solo crean, editan, emiten y versionan informes Costos. | Flujo nuevo 22 y flujo 14 (y Matriz de permisos) | Registrada. Resuelta por el Orquestador |
| R34 | (tanda D, D-H2, resuelta por el Orquestador) Los bloques sin fuente automática (semáforo, incidencias, logros y alertas) congelan lo que el usuario escribió en su configuración, sin umbrales inventados: no se calcula ningún semáforo. Lo mismo para RESTRICCIONES, PROXIMAS_ACTIVIDADES y FOTOS_DESTACADAS. | Flujo nuevo 22 | Registrada. Resuelta por el Orquestador |
| R35 | (tanda D, D-H3, resuelta por el Orquestador) El informe DIARIO se exige de un solo día (Desde igual a Hasta). Un bloque AVANCE_PARTIDA sin `config.wbs` impide emitir. Un formato de usuario con bloques de Costos solo sirve como informe COSTOS; en PERSONALIZADO se rechaza. | Flujo nuevo 22 (informes); flujos 18 y 21 si corresponde | Registrada. Resuelta por el Orquestador |
| R36 | (tanda D, D-H4, resuelta por el Orquestador) El banco de fotos del día muestra las fotos de todo el servicio (día en hora de Lima), no solo las propias. Cualquier foto del servicio se puede asignar a un borrador propio mientras no esté en un informe emitido. | Flujo nuevo 22 y flujo 14 (fotos de campo) | Registrada. Resuelta por el Orquestador |
| R37 | (tanda D, D6, resuelta por el Orquestador) Los días sin diario que avisa el informe se calculan con los partes del RDT (`diasSinParte`), no con los diarios emitidos, como dice el Spec. | Flujo nuevo 22 | Registrada. Resuelta por el Orquestador |
| R38 | (tanda E, E-H2 de `resultados/E.md`) Se conserva el id `informe-servicio` (etiqueta «Informes de supervisión», informativo, servicio obligatorio, permiso `puedeVerInformes`, los 13 roles). Nuevo acceso `foto-campo` (acción, grupo Supervisión operativa, servicio obligatorio, permiso `puedeTomarFotoCampo`: administrador, jefe de proyectos, jefe de oficina técnica y supervisor operativo) y acceso rápido nº 8. Filas de la matriz: `informe-servicio` sí para los 13 roles; `foto-campo` sí para los cuatro de arriba y no para los otros nueve. | Flujo 14 y matriz de permisos (tanda M); flujo 16 (ver P49) | Registrada |
| R39 | (tanda E, E-H3 de `resultados/E.md`, decidido por el Orquestador) En el resumen de Nuevo, «trabajados» = días con parte RDT no rechazado; «diarios emitidos» = informes DIARIO emitidos (sin COSTOS) con fecha en el período; «sin diario» = días trabajados sin diario emitido, como el Spec y la regla D6 (R37). El aviso del servidor («días sin ningún parte RDT») usa otra definición: la tanda L comprueba que coincidan. | Flujo nuevo 22 (resumen de Nuevo) | Registrada |
| R40 | (tanda G, G-H5, aceptada por el Orquestador el 2026-10-16; Victor la valida al revisar el flujo de informes) Alcance de la descarga: *resumen* = Datos del servicio, Semáforo, Indicadores, Logros y alertas, Avance por nivel, Costos-indicadores y Firmas; *fotos* = Datos del servicio y bloques de fotos. Los importes no llevan símbolo de moneda. En Word, «BORRADOR» va grande en el encabezado de cada página (Word no tiene marca diagonal). | Flujo nuevo 22 (informes) | Registrada |
| R41 | (tanda F, F-H2, resuelta por el Orquestador) Claves de `config` de los bloques, fijadas por F y oficiales: TEXTO `{texto}`; TABLA `{columnas[], filas[][]}`; CLIMA_TURNO `{clima, turno, observacion}`; FIRMAS `{firmantes[{nombre, cargo}]}`; FOTOS `{porPagina, mostrar}`; en los bloques de datos con valor escrito: INCIDENCIAS, RESTRICCIONES y PROXIMAS_ACTIVIDADES `{items[]}`, LOGROS_ALERTAS `{logros[], alertas[]}`, SEMAFORO `{estado: VERDE\|AMARILLO\|ROJO, texto}` (lo elige el usuario, sin regla de cálculo) y AVANCE_PARTIDA y COSTO_PARTIDA `{wbs}`. Las fotos de un bloque son las de `fotos_campo` con ese `bloqueId`. Los exportes de G se alinean con estas claves (W1). | Flujo nuevo 22 (informes) | Registrada. Resuelta por el Orquestador (Registro, 2026-10-16) |
| R42 | (tanda F, F-H3) Los bloques económicos solo se ofrecen en un informe de formato COSTOS y a quien tiene economía; el servidor rechaza el resto con 403. Al aplicar un formato propio a un informe que no los admite, esos bloques se omiten con aviso. | Flujo 14 y flujo nuevo 22 | Registrada |

## Observaciones sobre la política

| # | Observación | Estado |
|---|---|---|
| P1 | El árbol del panel izquierdo del marco de maquetas (`marco-tres-paneles.js`) está desactualizado respecto del flujo 16 (no tiene «Subcontratos» en Recursos del servicio). No se corrigió aquí. | Registrada |
| P2 | Dato del Spec que cambia: la migración 096 ya existe (RDT borradores, en `main`) y la 095 (`cerrar_lectura_directa`) está sin seguimiento y es de otra tarea. La 097 también existe (semilla de recursos, en `main`). La primera libre es la **098** (corregido por el Orquestador tras verificar con `git log`). | Registrada |
| P3 | «Uno solo por servicio» (R1) no está garantizado por los datos: el supervisor a cargo no es una columna sino el miembro con rol supervisor operativo de `asignado_en` más reciente; la pantalla de usuarios y la creación del servicio también agregan miembros, el PATCH de Editar servicio usa `ignoreDuplicates` (reasignar a uno que ya era miembro no lo vuelve el actual) y no existe forma de quitarlo. Afecta R1, R4 y C.4-5 del Spec. Pregunta 4 del Gate 1. | Registrada. Resuelta por decisión de Victor (2026-10-15) |
| P4 | El PR no tiene «% de avance económico» de subcontratos: `pr_recursos` tipo `subcontrato` solo trae lo contractual y el motor (`db/053`) acumula solo `mano_obra` y `equipo`. La gráfica de subcontratos del Spec (B.4) no tiene fuente. HM y HH contractual y acumulada por cargo y equipo **sí** existen. Pregunta 2. | Registrada. Resuelta por decisión de Victor (2026-10-15) |
| P5 | La unidad de `cantidad_contractual` de los equipos en `pr_recursos` (HM) no se verificó en datos reales; el Worker de la tanda I lo confirma contra el DP. | Registrada |
| P6 | El RDT no guarda HH extra, HM stand-by ni estado del equipo; la maqueta de informes los muestra en Técnico y Semanal. Pregunta 3. | Registrada. Resuelta por decisión de Victor (2026-10-15) |
| P7 | `next.config.ts` fija `Permissions-Policy: camera=(), geolocation=()` («la app no usa cámara ni ubicación»). El GPS opcional de las fotos exige `geolocation=(self)`; que `capture` en un input de archivo funcione con `camera=()` no está verificado. Cambio de cabecera de seguridad: pregunta 6. | Registrada. Resuelta por decisión de Victor (2026-10-15) |
| P8 | El Spec (A.2) dice que el chip «abre la cámara directamente»; un navegador no abre la cámara sin un toque del usuario, así que el chip abre una pantalla con un botón grande «Tomar foto». Pregunta 5. | Registrada. Resuelta por decisión de Victor (2026-10-15) |
| P9 | El Spec A.15 dice «a quien siga el servicio»: no existe seguidor de servicio; se propone notificar a los miembros (R9). | Registrada |
| P10 | `TipoNotificacion` está limitado por un check en `db/012` a tres tipos; se usa `MENSAJE` para no tocar el check. | Registrada. Resuelta por decisión de Victor (2026-10-15) |
| P11 | Los documentos `09` y `10` del estándar están escritos para opencode (modelos deepseek, qwen y agentes n0 a n5); el Orquestador pidió Sonnet y Haiku en Claude Code. El Plan usa una equivalencia de nivel por tipo de tarea; el estándar no la define. | Registrada |
| P12 | El artefacto «Matriz de permisos» (https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT), que `AGENTS.md` y el flujo 14 declaran como base de los accesos, **no se puede abrir desde la cuenta de Claude Code** (lectura: «artifact not found»; no aparece en la lista de artefactos de la cuenta, verificado el 2026-10-15). Por eso los agentes le piden a Victor que lo edite él. Victor (2026-10-15) indica que las acciones nuevas se registren en las tablas del flujo 14. Propuesta para el Gate 2: que las tablas del flujo 14 sean la fuente editable por los agentes y el artefacto se vuelva a publicar desde ellas (o que Victor comparta el artefacto con la cuenta de Claude Code). | Registrada |
| P13 | Posible doble conteo: el EV por partidas ya incluye el trabajo subcontratado y el BAC incluye los subcontratos; sumar el valor ganado del subcontrato al EV lo contaría dos veces. Pregunta 2. | Registrada |
| P14 | Los números de migración 098 a 101 se fijan de antemano (098 informes, 099 supervisor, 100 RDT, 101 subcontratos); cada Worker re-verifica `ls db/` y `git log` en `main`. La 097 ya existe (semilla de recursos). | Registrada |
| P15 | La Curva S (`db/070`, `ac_diario_hh` y `ac_diario_hm`) también calcula el AC con tarifa × horas y debe cambiar junto con el RDT, o el AC del PR y el de la Curva S dejan de coincidir. | Registrada |
| P16 | El relleno inicial de `proyectos.supervisor_operativo_id` en la 099 es una escritura de datos, no solo de estructura; pregunta 4. | Registrada |
| P17 | Riesgo de coordinación: el plan «Revisión completa de la app» (`2026-10-14-revision-completa-app.md`, en curso) ya tocó el RDT (`e0d00ff`) y tiene pendientes en los mismos archivos; se pide congelarlos mientras dure O/P (pregunta 6). | Registrada |
| P18 | El bloque «Costo real de recursos» del Dashboard (`costo-recursos.ts`) se apoya en que Σ `pr_recursos` mano de obra + equipo = AC; con R20 eso deja de ser cierto y aparecería una diferencia «Sin resolver» igual a materiales + subcontratos. Se corrige en la tanda S (S2). | Registrada |
| P19 | El Plan decía que el costo real vive en «tres cuentas SQL (PR, Curva S y guardado)». Verificado: son **dos** (`recalcular_pr_desde_rdt`, `db/053`, y `curva_s_proyecto`, `db/070`); `guardar_rdt_parte` (`db/054`) no calcula costo y el «guardado» es el recálculo que dispara `recalcularPr` desde las rutas de RDT. | Registrada |
| P20 | R20 no dice cómo se ve en la Curva S un subcontrato con ingreso manual en fechas anteriores a su último cambio (la tabla guarda solo el último monto y su fecha), ni si el avance físico lleva tope de 100 %. Propuesta del Planner en la decisión 16 y en R22; pregunta 8. | Registrada. Resuelta por el Orquestador con el principio de Victor (2026-10-15) |
| P21 | El BAC no tiene una sola definición en el código: `evm.ts` usa Σ `pr_partidas.bac` y `dashboard.ts` (`calcularBac`) suma los `costo_contractual` de los recursos. Si difieren, el «% de avance físico» saldría distinto según la pantalla y el AC de materiales y subcontratos dejaría de coincidir; la cuenta nueva usa Σ `pr_partidas.bac` y R6 comprueba si hay diferencia. | Registrada |
| P22 | El conteo de ítems del Plan no cuadraba: la tabla de asignación daba L = 6 y la lista tiene 7, por lo que el total real era 114 y no 113. Corregido al sumar las tandas R y S (19 tandas, 124 ítems). | Registrada |
| P23 | La maqueta `mockups/pr-subcontratos-medicion.html` (líneas 85 y 94) todavía dice «el monto cuenta como avance (valor ganado) del subcontrato, no como costo real», que R20 reemplazó. Mientras no se corrija, el brief de la tanda N manda sobre la maqueta (la nota del PR dice que el monto ingresado es el costo real). Corrección de texto a cargo del Documentador en la tanda M (Orquestador, 2026-10-15). Además, la pregunta nueva de R20 se renumeró como «pregunta 8» porque «pregunta 7» ya se usaba para la notificación al emitir (R9). | Registrada |
| P24 | (tanda A) El brief A no listaba `src/app/api/proyectos/route.ts`; el Worker lo tocó (una línea: la adjudicación guarda el supervisor a cargo) y lo devolvió como pregunta. Aceptado por el Orquestador. | Registrada |
| P25 | (tanda A) `npm run lint` tiene 9 errores y 22 avisos **preexistentes** en `main` (comprobado con y sin los cambios). El criterio de las tandas pasa a «no agregar errores nuevos». Candidato a corregir en el plan «Revisión completa de la app». | Registrada |
| P26 | El verificador (`scripts/verificar.ps1 -Clase rama`) devolvió ESCALAR dos veces el 2026-10-15 para avances rápidos de ramas de trabajo sin commits propios, ya pre-autorizados en el Gate 1: «autorizada» 0,76 (`local-worker-1` ← `main`, 19:44) y 0,41 (`local-worker-2` ← `local-worker-1` y `local-worker-3` ← `main`, 19:58); «sin daño» sin alarma. El Orquestador revisó y continuó en ambos casos. Posible causa: el script no encuentra la pre-autorización en el texto del plan. Para el Auditor y el Analista. | Registrada |
| P27 | (tanda N) `pr_subcontrato_medicion` no tiene política de lectura (como manda la 095): `cargarDatosDashboard` recibe un tercer parámetro opcional `clienteMediciones`; sin él, todo sale como avance físico. La tanda que arma la página del Dashboard (I o S) debe pasarle el cliente admin **solo** a los roles con economía. Pasado al brief S. | Registrada |
| P28 | (tanda N) El pie de `pr/page.tsx` (~línea 422) dice que los subcontratos se miden por % de avance económico y no suman al AC: contradice R20. Se corrige en S3. Pasado al brief S. | Registrada |
| P29 | (tanda N) La medición se guarda por `(proyecto_id, descripcion)` como pedía el plan; dos subcontratos con la misma descripción en un servicio compartirían medición. No se ha visto en datos reales. Para el Auditor. | Registrada |
| P30 | (tanda B) El Worker no leyó los Skills `cerrar-tanda` ni `verificar-permisos-por-rol` que pedía el brief; contrastó los permisos con el brief y el Spec, no con el flujo 14, y por eso dejó crear COSTOS solo a 3 roles en vez de los 5 de R5 (corregido a pedido del Orquestador). El Skill de permisos se exige con tabla observada en D y L. Para el Auditor. | Registrada |
| P31 | (tanda B) Supuestos operativos aceptados por el Orquestador: «últimas 2 semanas» = los 14 días que terminan hoy; «semana en curso» = lunes a hoy; «máximo 3 meses» = Hasta ≤ Desde + 3 meses − 1 día (recortado a fin de mes); `siguiente_codigo_informe` recibe el N° OT como `p_ot` (lo pasan las rutas de D). Para el flujo 22. | Registrada |
| P32 | (tanda O) El PATCH de `api/rdts/partes/[id]` solo valida o rechaza el parte y no recibe tareo ni equipos; la validación de HH extra, HM stand-by y estado quedó en el POST, en la RPC `guardar_rdt_parte` y en el formulario. Aceptado por el Orquestador. La igualdad AC del PR = AC de la Curva S quedó comprobada por texto y fórmula, no contra una base (sin base indicada); se comprueba en vivo en L. O8 «no probado en base». Un fallo intermitente de una prueba en una corrida intermedia no se pudo identificar. | Registrada |
| P33 | Las migraciones 098, 099, 100 y 101 están escritas y revisadas pero **no aplicadas**: el servidor de base de datos (MCP `postgresql`) no conecta en esta sesión. Se aplican antes de la verificación en vivo (L5), en el orden 099, 098, 100, 101, 102. | Registrada |
| P34 | (Worker git, incorporación de N en `local-worker-3`) `db/README.md` quedó con dos líneas numeradas «76.» (099 y 100) y la línea de la 101 en otro formato; el Worker git hizo un commit extra (a7e61af) para corregir su propio orden. Es solo formato: se normaliza al integrar en `main` (paso 16a). Lección: en `db/README.md` cada Worker agrega su línea sin número de orden, o el Orquestador numera al integrar. | Registrada |
| P35 | (tanda H) `CabeceraPagina` no admite hijos: la etiqueta «Supervisor operativo a cargo» va justo bajo el encabezado y no en la línea del servicio como en la maqueta. Aceptado por el Orquestador (no se toca un componente compartido). La tarjeta de avance dice «Avance físico ejecutado (RDT validados)» en vez de «EV / BAC», para no nombrar BAC en Parcial. | Registrada |
| P36 | (tandas A, H y N) Ningún Worker pudo tomar capturas: no pueden leer las cuentas de prueba (viven solo en la memoria del Orquestador) y las migraciones 098 a 101 no están aplicadas. Los ítems con captura quedan «Observado» y se cierran en la verificación en vivo (L), con las migraciones aplicadas. | Registrada |
| P37 | (tanda R) La función `ac_materiales_subcontratos_al_corte` se escribió `security definer` para que la Curva S (que corre con la sesión del usuario) lea `pr_subcontrato_medicion`; así, cualquier usuario autenticado podía pedir por RPC los totales económicos de cualquier proyecto. **No aceptado** por el Orquestador: se revoca la ejecución a `anon`/`authenticated` (también de `curva_s_proyecto`) y los llamadores pasan al cliente de servicio después de validar sesión, rol y alcance en servidor (R-fix). Para el Auditor (punto 2 de su prompt). | Registrada |
| P38 | (tanda R) `costoMaterialesAcum` y `costoSubcontratosAcum` son opcionales en `ProyectoEvmDatos` (0 si faltan): hasta que la tanda S los cargue desde `proyecto_pr`, el AC mostrado no cambia. R6 y la comparación `db/pruebas/102_comparacion_ac.sql` (incluye P21) quedan para cuando haya base y migraciones aplicadas. | Registrada |
| P39 | (tanda I) En «en qué partidas se usó» (I6) el cargo del tareo se une a `pr_recursos.descripcion` por nombre normalizado: no hay llave entre ambos. Aceptado por el Orquestador como riesgo; para el Auditor. La unidad HM de los equipos (P5) sigue sin confirmar con un DP real. | Registrada |
| P40 | (tanda I) En Parcial, la gráfica por nivel recibía las partidas como fracciones del BAC (peso económico relativo). El Orquestador lo corrige: el servidor manda solo el % por nodo, sin pesos ni montos, con prueba que recorre lo serializado. | Registrada |
| P41 | (tanda I) Ruta nueva `GET /api/proyectos/[id]/dashboard/recurso-partidas` (`puedeVerDashboard` + alcance, solo horas): lleva fila en el flujo 14 y en la lista para la matriz (Documentador). | Registrada |
| P42 | El clasificador de permisos de Claude Code bloqueó como «Git Destructive» el `git merge --no-ff 34b8bbf` en `local-worker-1` (incorporar O y R antes de C), aunque el Gate 1 pre-autoriza incorporar ramas entre Workers. El Worker git no lo sorteó; el Orquestador lo escaló a Victor. Para el Analista: las pre-autorizaciones del Gate 1 no llegan al clasificador. | Registrada |
| P43 | El verificador (`-Clase push`) devolvió BLOQUEAR (sin daño 0,95; autorizada 0,01) para subir los documentos de este plan a `main` del repositorio de documentación, aunque Victor lo autorizó en el chat y la política deja esa documentación al Orquestador. Causa probable: el script toma el «Gate 2 pendiente» del plan como condición de todo push. El Orquestador siguió con la autorización explícita de Victor. Para el Analista: separar en el script el push de documentación del push de código. | Registrada |
| P44 | Riesgo de coordinación: en `main` del repositorio de documentación apareció otro plan en curso, «cronograma dentro del sistema» (commits 23a8afa y 5c5ea6d: Gate 1 aprobado, 13 tandas, briefs C0-C12, `local-worker-6`). Antes de integrar en `main` de la app (16a) hay que cruzar sus archivos con los de este plan (Dashboard, Curva S, `db/` numeración, `registro-accesos.ts`). Sus briefs «C0-C12» no son la tanda C de este plan. **Verificado:** ese plan usa `local-worker-4` y `local-worker-6`, migraciones desde la 103 y declara fuera de límites `src/lib/rdts/**`, `evm.ts`, `src/lib/dashboard/**`, `src/lib/informes/**` y `db/098` a `db/102`; riesgo bajo, se revisa igual al integrar. | Registrada |
| P45 | (tanda P) El `node_modules` del repositorio principal de la app quedó a medias (50 entradas, sin `vitest`); `local-worker-1` y `-2` lo usan por enlace simbólico y quedan sin poder probar. Existe `.worktrees/_node_modules_bloqueado_w4` apuntando a él (otro plan). W3 ya tiene `node_modules` propio con `npm ci`; se indica a W2 y W1 lo mismo, sin tocar el principal. Victor debe saberlo: el repositorio principal no corre pruebas hasta reinstalar. | Registrada |
| P46 | (tanda P) Consolidado: las filas de HM suman operativas + stand-by y las de HH incluyen la extra (R14); el desglose normales/extra y operativas/stand-by va como grupo aparte sin total propio. Aceptado por el Orquestador (ya decidido en R13/R14). Flujos 06 y 18 para el Documentador. | Registrada |
| P47 | (tanda S, S-H2) El PR no tiene «KPI AC» como tarjeta: se puso una franja de desglose sobre el pie. Confirmar el diseño en L (destino: Gate 2 / L). | Registrada |
| P48 | (tanda D, D-H6) El brief pide «la tabla de los 13 roles» del Skill `verificar-permisos-por-rol` con suplantación en vivo, pero con las migraciones sin aplicar solo hay pruebas de ruta; conviene decir en el estándar que esa tabla queda «Observado» hasta la tanda L. Para el Auditor. | Registrada |
| P49 | (tanda E, E-H1 de `resultados/E.md`, conflicto con los flujos) El brief habla del «panel izquierdo grupo Reportes» y de «Acciones del izquierdo», que ya existen en `ESTRUCTURA_IZQUIERDA`; se añadieron `informe-servicio` a Reportes y `foto-campo` a Acciones. Los flujos 16 y 14 deben reflejarlo (tanda M; R19). | Registrada |
| P50 | (tanda E, E-H4 de `resultados/E.md`) Los enlaces «Continuar» y «Ver» del listado apuntan a `/proyectos/[id]/informes/[informeId]` (tanda F), que aún no existe: dan 404 hasta que F entregue el editor. Tras crear, Nuevo muestra el código, los avisos y un enlace al listado, sin redirigir. Respondido en el Registro (2026-10-16): se acepta; después F puede hacer que Nuevo redirija al editor. | Registrada |
| P51 | (tanda E, E-H5 de `resultados/E.md`) Quedaron fuera del brief «Mis formatos» (`formatoUsuarioId`) en Nuevo y el botón «Descargar» del listado (no hay API de descarga aún). El conteo de fotos y los nombres de autor se consultan en la página, porque la API de listado no los devuelve. Respondido en el Registro (2026-10-16): el conteo en página se acepta; «Descargar» y «Mis formatos» pasan a F. Sigue abierto si W1 debe sumar `fotos` a la API de listado. | Registrada |
| P52 | (tanda E, E-H7 de `resultados/E.md`) El brief pidió commit al cerrar E1–E2 y al cerrar E3–E4; hubo dos commits y el registro ya apuntaba a `/informes/foto` desde el primero (ruta sin página en ese commit intermedio, sin prueba que lo detecte). Para el Auditor: valorar si hace falta una prueba de que cada ruta del registro tenga página. | Registrada |
| P53 | (tanda G, G-H6) El plan cita `rdts/exportar` como patrón de `exceljs` y de la descarga, y esa carpeta no existe; el Worker usó `rdts/exportador-*.ts` y `dp/exportador-excel.ts`. Corregir la referencia en el plan. | Registrada |
| P54 | (tanda F, F-H1) El GET de un borrador no entregaba los datos de los bloques del sistema, así que la hoja no mostraba cifras antes de emitir. Resuelta por el Orquestador (ver Registro, 2026-10-16): corrección de API en W1 y, después, corrección de la vista previa en W3. | Registrada. Resuelta por el Orquestador |
| P55 | (tanda F, F-H4) Quitar un bloque con fotos asignadas dejaba esas fotos con un `bloque_id` que ya no existe, y al emitir quedaban bajo un bloque inexistente. Resuelta por el Orquestador (ver Registro, 2026-10-16): al quitar un bloque sus fotos quedan libres y al emitir no queda ninguna con un bloque inexistente (W1). | Registrada. Resuelta por el Orquestador |
| P56 | (tanda F, F-H5) El banco de fotos pide un día por vez (`fotos-campo?fecha=`), así que en un informe semanal solo se ven las fotos asignadas de los días ya visitados. Resuelta por el Orquestador (ver Registro, 2026-10-16): la API acepta `?informeId=` para ver el período completo del informe (W1). | Registrada. Resuelta por el Orquestador |
| P57 | (tanda F, F-H7) La primera prueba de F usó una lista de «roles con economía» inventada en vez de leer `puedeVerEconomia`; se corrigió leyendo la fuente. Reafirma «verificar antes de afirmar» (ver M3). Para el Auditor: sin cambio de política propuesto. | Registrada |

## Carpetas/archivos huérfanos

| # | Hallazgo | Estado |
|---|---|---|
| H1 | En `pg_control_proyectos`, `.playwright-mcp/` tiene muchos `console-*.log` y `RDT-BORRADOR-2026-10-15.pdf` sin seguimiento (salida de Playwright). No se borró nada. | Registrada |
| H2 | En `py_control_proyectos_web`, `db/095_cerrar_lectura_directa.sql` y archivos del DP (`leer-libro.ts`, `parser-apu-s10.test.ts`) están sin seguimiento: pertenecen a otra tarea. No se tocaron. | Registrada |
| H3 | (tanda C, C-H4) `node_modules` del repositorio principal `py_control_proyectos_web` quedó con 50 entradas y sin `.bin` tras un `npm ci` fallido (ya estaba «a medias», P45). Reportado a Victor, que decide si se corre `npm ci` ahí. No se borró nada. | Registrada |
| H4 | (tanda G, G-H7) El `.env.local` del worktree `local-worker-1` se sobrescribió con el del repositorio principal; estaba autorizado (copiarlo a los worktrees). Sin acción. | Registrada |

## Handoff (relevo del Orquestador, 2026-10-15)

- **Por qué:** la sesión del Orquestador llegó a 313k de contexto (zona roja, más de 300k). Medición con `python scripts/medir.py --resumen 1`: sesión principal 0c7a69a2 (160 llamadas, contexto máximo 313k) más la anterior a la compactación 0de241ac (433 llamadas, 315k); Planner 69 llamadas (307k); Worker de maquetas 24 llamadas (122k).
- **Consumo de la etapa Spec + Plan** (medido de los registros de la sesión 0c7a69a2 y sus dos subagentes, del 15-10 15:33 al 16-10 00:32; sin duplicar mensajes):

  | Agente | Modelo | Llamadas | Caché creada | Caché leída | Salida | Contexto máx. |
  |---|---|---|---|---|---|---|
  | Orquestador | Opus 5.5 | 167 | 834 403 | 30 485 876 | 250 247 | 312 805 |
  | Planner | Sonnet 5.5 | 68 | 768 918 | 10 423 490 | 2 134 * | 306 645 |
  | Worker de maquetas | Sonnet 5.5 | 24 | 227 619 | 1 781 357 | 5 469 * | 121 655 |
  | **Total** | | **259** | **1 830 940** | **42 690 723** | **257 850** | |

  Total de tokens: **44,8 millones** (entrada sin caché: 530). El 95 % es caché leída. \* La salida de los subagentes sale subregistrada en sus registros: el Planner escribió unos 94 000 caracteres (unos 27 000 tokens estimados) y el Worker unos 35 000 (unos 10 000 estimados).
- **Hecho:** Spec aprobado con las ampliaciones D (RDT), E (Inasistencias) y F (Subcontratos); Plan de 19 tandas (A a S) y 124 ítems (R y S nuevas por R20); Gate 1 aprobado; maquetas `informes-supervision.html`, `dashboard-ip-hh-graficos.html`, `crear-rdts.html` y `pr-subcontratos-medicion.html`, con `README.md` e `index.html` de mockups actualizados.
- **Siguiente:** (1) el Planner ya ajustó las tandas a R20 (tandas R y S, migración 102) y el Orquestador las revisó (pregunta 8 resuelta con el principio de Victor); (2) el Orquestador confirma el Gate 1 con Victor en una línea y lanza la Ola 0 (W1, tanda A) en `local-worker-1`, que hoy está 0 commits adelante de `main` y hay que ponerlo al día con `main` con el Worker git; (3) avisar en el plan «Revisión completa de la app» que no toque los archivos del RDT mientras duren las tandas O y P.
- **Git:** nada de este plan tiene commit. Archivos propios sin subir: este plan, las cuatro maquetas, `mockups/README.md`, `mockups/index.html` y `mockups/marco-tres-paneles.js` (su diff es solo el gancho `MARCO_AJUSTE` de este plan; `README.md` e `index.html` de mockups ya venían modificados al empezar la sesión: revisar su diff antes de subir). Hay otros archivos modificados de sesiones anteriores (flujos 06, 09, 12, 14, 16, 18, 19, 20, `design.md`, plan del lote 3, `02-trabajo-activo/README.md`) que **no** son de este plan. El commit y el push de los archivos de este plan los autoriza Victor.
- **Pendiente con Victor:** artefacto «Matriz de permisos» inaccesible desde la cuenta (P12); autorizar commit y push de los archivos de este plan.


## Handoff 2 (relevo del Orquestador, 2026-10-15 22:55)

- **Por qué:** contexto del Orquestador en 294k (umbral rojo, 300k), medido con `python scripts/medir.py --resumen --desde 2026-10-15` (sesión e51bd4d1, 101 llamadas).
- **Hecho (en ramas, sin merge a `main`):**
  - `local-worker-1` (W1): A (e65dcae, c0dd874, 9ad0de7), B (1fa141d, 3cc7d94, 3ce0a52).
  - `local-worker-2` (W2): contiene A; N (2879b46, 0e1d8f9), H (dbe1a5e, b196a7a), I (6a1ed04, 32334bd, 461a0f9), J (8e60ced).
  - `local-worker-3` (W3): contiene A y N; O (3233b93), R (a8f7089, 2bbeb62, 34b8bbf con la corrección de seguridad P37), P (2d4b3e8, 1247100).
  - Todos con push y árbol limpio. Resúmenes en `2026-10-15-informes-supervision-y-dashboard-briefs/resultados/`.
- **Bloqueado:** incorporar 34b8bbf (O+R) en `local-worker-1` — el clasificador de permisos bloqueó `git merge --no-ff` (P42). **Pendiente del visto bueno de Victor.** Regla para el conflicto de `db/README.md`: conservar ambas líneas del conflicto, no mover nada fuera, cada migración 098-102 una sola vez, numeración se normaliza en 16a (P34).
- **Siguiente, en orden:**
  1. Con el visto bueno: Worker git incorpora 34b8bbf en `local-worker-1` → W1 · C (brief `C.md`) → W1 · D (`D.md`, Skill `verificar-permisos-por-rol` obligatorio, P30) → W1 · G (brief por escribir).
  2. W2 · K (brief `K.md`, listo) → Worker git incorpora 34b8bbf en `local-worker-2` → W2 · S (brief `S.md`, con los avisos de N al final).
  3. W3 · E → F → Q → L (briefs por escribir; W3 necesita B, C y D de W1 incorporados antes de E).
  4. Antes de L: aplicar las migraciones 099, 098, 100, 101, 102 (P33). El servidor `postgresql` no conectó en esta sesión; preguntar a Victor dónde y cómo se aplican y qué base usar para R6/O8 (servicio de prueba PS-0011, Portafolio Practica). Las capturas (P36) necesitan las cuentas de prueba de la memoria y las migraciones aplicadas.
  5. M (Documentador), Auditor, Gate 2.
- **Avisos operativos:** `node_modules` del repositorio principal de la app está a medias (P45): W1 debe pasar a `node_modules` propio (`rm` solo del enlace + `npm ci`) antes de C. `npm test` cambia el `.snap` de curva-s por fin de línea (M6): restaurar con `git checkout`. Build con `npx next build --webpack` (M5); lint: 9 errores preexistentes (P25). Victor pidió Haiku para todo lo simple (git, traslados, índices). El verificador escala o bloquea las acciones pre-autorizadas (P26, P43): revisarlo y seguir si consta la autorización.
- **Pendiente con Victor:** visto bueno del merge bloqueado; matriz de permisos (sin respuesta: se sigue con las tablas del flujo 14); dónde aplicar las migraciones; reporte de consumo al final (pedido por Victor: «quiero al final un reporte del consumo»).
- **Consumo medido de este Orquestador y sus subagentes (2026-10-15, 19:33 a 22:55):** 510 llamadas; caché creada 2,46 M; caché leída 53,51 M; salida 89 k. Orquestador (Opus) 101 llamadas, 20,13 M leídos, 79 k de salida; Planner 64; W1 65; W2 124; W3 122; Worker git (Haiku) 34.


## Handoff 3 (relevo del Orquestador, 2026-10-16)

- **Por qué:** Victor pidió parar la sesión cuando terminaran los agentes en curso, con informe de avance, informe de consumo y prompt para el siguiente Orquestador. Contexto del Orquestador en 232k (zona amarilla). Ningún agente de código quedó corriendo.
- **Estado:** 13 de 19 tandas cerradas en sus ramas (A, B, C, D, N, O, R, P, H, S, I, J, K): **86 de 124 ítems (69 %)**; con Q1–Q3 hechas, 89 (72 %). Faltan 35 ítems: Q4–Q6 (3), E (4), F (6), G (7), L (7) y M (8). Después: Auditor, Gate 2 y los pasos 16a a 16c. D1–D7 quedan `Observado` (código probado con base simulada; 098–102 sin aplicar; los cierra L), igual que las capturas de A, H, N, K y S.
- **Ramas de la app (verificadas con git el 2026-10-16; las tres limpias, con `0 0` contra origin, sin merge a medias y sin commits de `main` que no tengan; ninguna mergeada a `main`):**
  - `local-worker-1` en 0369ab8: A, B, merge de O y R (ee80c7a), C (e089e38, a8e85d2, 8459b86 con la corrección C-H1/C-H2), D (8be999c, 0369ab8).
  - `local-worker-2` en 1d7c338: A, N, H, I, J, K (104887c, a4f0808), merge de O y R (dc5144f), S (1d7c338). **W2 terminó todas sus tandas.**
  - `local-worker-3` en 93c5d45: A, N, O, R, P, merge de B (afdbdde), Q1–Q3 (93c5d45).
- **Siguiente, en orden:**
  1. Preguntar a Victor una sola cosa antes de lanzar E: si confirma el GPS de las fotos (P7: cambiar `geolocation=()` por `geolocation=(self)` en `next.config.ts`, solo eso; la cámara no se toca hasta que él pruebe en un celular). El clasificador de permisos denegó dejarlo escrito en `E.md`; mientras no confirme, el brief de E dice que no se toque ese archivo.
  2. Worker git (Haiku) incorpora `local-worker-1` (hasta 0369ab8: B, C, D) en `local-worker-3` (`git merge --no-ff 0369ab8`; solo se resuelve `db/README.md`, conservando todas las líneas). Luego **W3 · E** (`E.md`) → **F** (`F.md`) → **Q4–Q6** (segunda mitad de `Q.md`; cierra `resultados/Q.md`).
  3. En paralelo, **W1 · G** (`G.md`), desde `local-worker-1`.
  4. Antes de L: el Worker git incorpora de nuevo `local-worker-1` (con G) en `local-worker-3`; **Victor aplica a mano las migraciones 099, 098, 100, 101 y 102** (los archivos están en `db/` de `local-worker-1`) y confirma que la 096 ya está aplicada; se coordina con Victor el inicio de sesión de L (cuentas de prueba en la memoria del Orquestador; ningún Worker las lee). **W3 · L** (`L.md`; capturas en `docs/02-trabajo-activo/03-evidencia/capturas/2026-10-15-informes-supervision-y-dashboard/`, una carpeta por tanda). L comprueba también la franja de desglose del PR (S) y que la página y el archivo del Dashboard coinciden con un rol con economía y `tipo_dashboard` PARCIAL (M9).
  5. **M** (Documentador): tabla de cambios a flujos del Gate 1, flujo nuevo 22, filas del flujo 14 (la matriz de permisos sigue inaccesible, P12: solo las tablas del flujo 14), traslado de todas las filas del libro de hallazgos (usar el Skill `trasladar-hallazgos`), referencias. Luego Auditor, Gate 2 (pedir la autorización del push del código y mostrar a Victor las reglas R24–R37, decididas por el Orquestador), 16a (merge a `main` en el orden W1, W3, W2, con el verificador; normalizar la numeración de `db/README.md`, P34), 16b, 16c, mensaje de cierre dentro del plan.
- **Avisos operativos:**
  - Las incorporaciones entre ramas las hace el Worker git en Haiku; con el visto bueno de Victor el clasificador no las volvió a bloquear (ee80c7a, dc5144f, afdbdde).
  - Para quitar un enlace `node_modules` en Windows: PowerShell, `cmd.exe /c "rmdir node_modules"`, comprobar que `LinkType` queda vacío y recién entonces `npm ci`; nunca `rm -rf` ni `cmd /c` desde Git Bash (M11). Los worktrees W1, W2 y W3 tienen `node_modules` propio y completo; el del repositorio principal de la app está a medias (H3); Victor decide si se corre `npm ci` ahí.
  - Si una sesión se corta por el límite de uso (error 429), se reanuda al mismo agente con `SendMessage`; no se lanza uno nuevo.
  - El Documentador (Haiku) que cierra una tanda no debe agregar al commit el resumen de una tanda en curso (una vez entró `C.md` incompleto); `git add` por ruta.
  - `npm test` cambia el `.snap` de curva-s por fin de línea: `git checkout` del archivo. Build con `npx next build --webpack`. Lint: 9 errores y 22 avisos preexistentes.
  - El repositorio principal de la app tiene `db/095_cerrar_lectura_directa.sql` sin seguimiento: no es de este plan, no se agrega a ningún commit.
- **Pendiente con Victor:** GPS de las fotos (P7); aplicar las migraciones (y confirmar la 096); `npm ci` en el repo principal de la app; matriz de permisos (P12, sin respuesta); conectar el repositorio al cerebro `victor_brain` (no se hizo; él lo dejó para la próxima sesión); Gate 2.
- **Consumo medido (`python scripts/medir.py --resumen --desde 2026-10-15`, 2026-10-16):** el comando devuelve 50 sesiones, 2 607 llamadas, caché leída 398,13 M, creada 11,30 M, salida 1,49 M, pero **incluye trabajo de otros planes** (Revisión completa de la app, Cronograma). Lo de este plan, sumado por sesiones atribuibles: Spec + Plan (Opus) 44,8 M; Ola 1 hasta el relevo 2 (Opus) 56,1 M; relevo 3 (Sonnet) 33,9 M (323 llamadas: Orquestador 9,65 M, Workers de código 17,03 M, Documentador Haiku 5,01 M, Planner de briefs 1,05 M, Worker git Haiku 1,17 M). **Total aproximado del plan: 134,8 M de tokens, 95 % caché leída** (la salida de los subagentes sale subregistrada). Los Workers de código gastaron 45,7 M en 14 tandas (promedio 3,3 M); la más cara fue D (5,8 M) y la más barata S (1,7 M).

### Prompt para el siguiente Orquestador (relevo 4)

> Eres el Orquestador del plan «Informes de supervisión y Dashboard» (D:\VICTOR\CLAUDE CODE\pg_control_proyectos), relevo 4. Delegas en subagentes: Sonnet con esfuerzo medio para código y briefs, Haiku con esfuerzo extra para todo lo simple (git, traslados, cierres de tanda en el plan, índices). No implementas. A cada agente le indicas solo qué leer.
> Lee: AGENTS.md; docs/00-estandar-agentes/04-flujo-sdd-y-planes.md y 02-roles-y-delegacion.md; del plan docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md solo «Identificación y estado», «Handoff 3» (al final) y las primeras filas del «Registro de decisiones». Usa el Skill seguir-flujo-de-planes (y cerrar-tanda al cerrar cada tanda).
> No vuelvas a preguntarle a Victor lo ya decidido en el Registro (regla: «si se gasta plata en algo es costo real»). Los detalles derivados los decides tú y los anotas.
> Primero: comprueba con git (Worker git en Haiku) que local-worker-1, 2 y 3 siguen en 0369ab8, 1d7c338 y 93c5d45, limpias y subidas. Pregúntale a Victor solo (1) si confirma el GPS de las fotos (P7) y (2) si ya aplicó las migraciones 099, 098, 100, 101 y 102 (solo antes de lanzar L). Luego sigue el orden del «Handoff 3».
> Al cerrar el plan, entrega a Victor el reporte de consumo total medido con python scripts/medir.py --resumen --desde 2026-10-15, separando lo que no es de este plan.
