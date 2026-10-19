# 22 — Informes de supervisión
> Lee si: la tarea toca los informes diarios o semanales del supervisor operativo, el chip «Informes de supervisión», la foto de campo y su banco de fotos, los formatos y bloques de informe, el código del informe, el período del semanal, la descarga en PDF, Word o Excel, el aviso al emitir, o la pestaña Inasistencias.


Origen: plan [Informes de supervisión y Dashboard](../02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md) (Spec aprobado por Victor el 2026-10-15; reglas validadas en su Gate 1). Quién puede cada acción: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md); no se repite aquí. Las pantallas y chips: [flujo 16](16-paneles.md). El informe **lee** el RDT ([flujo 06](06-rdt.md)), el PR ([flujo 10](10-generacion-pr.md)) y la Curva S ([flujo 21](21-curva-s.md)); no los cambia.

## Qué es

El supervisor operativo arma desde la app su informe **diario** o **semanal**: elige un formato, el sistema llena solo los datos del servicio (actividades del RDT, personal y equipos, avance, IP, HH), él agrega texto y fotos, lo guarda como borrador y, cuando está listo, lo **emite** para que lo vea todo el equipo del servicio. Lo descarga en PDF, Word o Excel. Desde el celular, el chip «Foto de campo» deja fotos en un banco del servicio para usarlas en el informe.

## Pantallas

| Pantalla | Ruta | Contenido |
|---|---|---|
| Listado | `/proyectos/{id}/informes` | Informes del servicio: código, tipo, fecha o período, formato, autor, estado, versión, cantidad de fotos y acciones. Filtros por tipo, estado, autor y fecha. Lleva además la pestaña **Inasistencias** (ver abajo). |
| Nuevo | `/proyectos/{id}/informes/nuevo` | Elegir tipo, formato (o «Mis formatos») y fecha o período; resumen del período; avisos antes de crear. |
| Editor / emitido | `/proyectos/{id}/informes/{informeId}` | Editor por bloques con vista previa de hoja A4 (borrador) o la hoja congelada (emitido); descarga. |
| Foto de campo | `/proyectos/{id}/informes/foto` | Botón grande «Tomar foto», servicio, actividad (opcional) y descripción (obligatoria). |

Chips (flujo 16): **Informes de supervisión** (informativo, con acciones internas; id `informe-servicio`, el chip que antes decía «Informe de servicio» y estaba inerte) en Supervisión operativa del panel derecho y en Reportes del panel izquierdo; **Foto de campo** (acción) en Supervisión operativa, Accesos rápidos (el nº 8) y Acciones del panel izquierdo. Ver el listado no muta nada.

## Tipos, código y estados

* **Tipos:** Diario (una sola fecha: Desde = Hasta) y Semanal (período configurable desde – hasta).
* **Código:** `{N° OT}-ID-{n}` para diarios y `{N° OT}-IS-{n}` para semanales, con el mismo patrón del RQ (`{N° OT}-RQ-{n}`). **El número es correlativo por fecha** (Victor, 2026-10-18): dentro de un servicio y un tipo, el informe de fecha más antigua es el 1; si luego se crea, o se cambia a, un informe de una fecha anterior, ese toma el número que le corresponde y los siguientes se corren. **También se renumeran los emitidos** (única excepción a «emitido congelado», y solo para el código); el código anterior queda en un historial (`informes_codigo_historial`) y todas las versiones de un informe comparten código. Un semanal ya emitido conserva, dentro de su foto fija, los códigos de diarios tal como eran al emitir. La renumeración la hace la base (`renumerar_codigos_informes`, migración `db/110`, aplicada por Victor el 2026-10-18); `siguiente_codigo_informe` sigue dando el número provisorio al crear. Si la función falla o no existe, el informe conserva el código provisorio y nada se cae.
* **Estados:** `Borrador` (solo lo ve su autor; se guarda solo) → `Emitido` (lo ven los 13 roles con el servicio asignado; queda congelado) → `Reemplazado` (cuando se emite una versión nueva). **Un emitido no se edita**: se corrige emitiendo la versión siguiente y la anterior queda consultable. La base rechaza (409) editar un emitido.
* **Versión nueva de un informe ajeno:** solo administrador y jefe de proyectos; el autor puede versionar el suyo.
* **Sin aprobación previa** en esta versión: emitir no pasa por la jefatura (Victor, 2026-10-15).

## Foto fija al emitir y avance validado

* **Foto fija:** al emitir, los bloques de datos guardan los valores del momento; el informe emitido **no cambia** si después cambia el RDT o el PR. Un borrador usa los datos en vivo (el listado y el detalle del borrador los calculan al abrirlo).
* **Avance real solo validado:** los indicadores usan RDT `VALIDADO`. Lo del día que aún no se valida entra rotulado **«reportado, pendiente de validación»**, nunca como avance real.
* **Indicadores «al corte» de un diario** salen de la **fecha del diario**, no del PR de hoy: avance, programado y SPI de la serie física de la Curva S en esa fecha; HH ganadas, HH reales e IP de los partes `VALIDADO` hasta esa fecha. Límite: las HH legacy sin partida no se reconstruyen por fecha.
* **El acumulado por actividad suma el metrado por el vínculo oficial** `rdt_actividad_partidas` (el mismo del PR); el texto `wbs` de la actividad solo se muestra. Una actividad con texto 9.9 vinculada a la partida 1.2 suma a 1.2.
* **PPC y causas de no cumplimiento:** el PPC cuenta las actividades directas de los partes validados del período. El Pareto de causas cuenta, igual que el Dashboard, toda actividad con causa (directa, contributoria o no contributoria) de los partes validados. Las causas reportadas en partes aún sin validar (no rechazados) no entran al Pareto: salen como «Causas reportadas, pendientes de validación» (Victor, 2026-10-18).
* **Días sin diario:** el aviso del informe se calcula con los **partes del RDT** (días sin ningún parte), no con los diarios emitidos.

## Formatos

Cada formato tiene contenido distinto:

| Formato | Contenido |
|---|---|
| **Técnico completo** (diario) | Actividades del RDT, personal desglosado (nombre, cargo, partida, HH normales, HH extra, total), equipos desglosados (equipo, código, partida, HM operativas, HM stand-by, estado), incidencias, fotos y firmas. |
| **Semanal acumulado** | El Técnico en tipo Semanal. Por actividad: contractual, acumulado anterior, metrado de cada día del período (de cada semana si pasa de 10 días), total del período, acumulado a la fecha y %; personal y equipos con sus horas por día o semana, total, acumulado y contractual; avance acumulado (programado contra real); indicadores del período y acumulados; restricciones y próximo período; fotos destacadas y la lista de diarios que lo forman. |
| **Ejecutivo** (1 página) | Semáforo, indicadores, avance por nivel, logros y alertas, dos fotos; sin tablas. |
| **Registro fotográfico** | Solo fotos con hora, partida y descripción, en cajas (filas × columnas y alto elegidos por el usuario; ver § Editor por bloques). |
| **Costos** (diario o semanal) | EV, AC, CV, CPI y SPI; personal y equipos valorizados; costo por partida. Costo directo en US$; las HH de MOI no se valorizan; el AC sigue la regla de costo real del [flujo 10](10-generacion-pr.md). |
| **Mis formatos** | Cada usuario que puede crear informes (administrador, jefe de proyectos, jefe de oficina técnica, supervisor operativo, supervisor de costos y jefe de costos) guarda su propio arreglo de bloques desde el editor, como las plantillas del RDT. Un formato con bloques de Costos solo lo sirve a quien tiene economía (decidido por Victor el 2026-10-17). |

**El formato Costos y todo bloque con dinero** (indicadores de costo, personal y equipos valorizados, costo por partida) **solo lo crean, ven y descargan los 5 roles con datos económicos** (administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos y jefe de costos; regla 2 del flujo 14). A los demás el formato les sale deshabilitado con título y el informe no les aparece en la lista; por URL directa el servidor responde 403. Los otros formatos **no llevan dinero** en ningún byte.

**Quién crea qué:** los formatos que no son Costos (técnico, ejecutivo, fotográfico y personalizado) los crean, editan y emiten los 4 roles de supervisión y dirección (administrador, jefe de proyectos, jefe de oficina técnica y supervisor operativo), con el servicio asignado. Costos lo crean los 5 roles con economía. El supervisor de costos y el jefe de costos **solo** crean, editan, emiten y versionan informes Costos.

**Bloques económicos:** solo se ofrecen en un informe de formato Costos y a quien tiene economía; el servidor rechaza el resto con 403. Un formato de usuario con bloques de Costos solo sirve como informe Costos (en Personalizado se rechaza). Al aplicar un formato propio a un informe que no los admite, esos bloques se omiten con aviso.

## Editor por bloques

Con vista previa de hoja A4: los bloques se quitan, ocultan (casilla), agregan y reordenan (arrastrando ⠿ o con flechas); el guardado automático se arma desde los manejadores de cambio. Cada bloque de la lista lleva el rótulo **Dato** (lo llena el sistema) o **Libre** (lo escribe el usuario). **Un clic en un bloque de la hoja lo selecciona y lleva su panel de edición a la vista**; la hoja usa la barra azul de sección con su origen («dato del sistema», «texto libre»), el encabezado con LOGO, título, código y datos del servicio, y las tarjetas de indicadores de la maqueta. El banco de fotos va en una columna a la derecha, con la etiqueta «en informe» o «sin ubicar» en cada foto y el botón «Ubicar las N sin ubicar». **Encabezado (cajetín) editable.** El bloque de encabezado dibuja el cajetín de la empresa: nombre de la empresa, **logo propio** (por defecto el de Promcoser), título del informe, **código** y **versión** (los pone el sistema), **fecha de elaboración** (por defecto el último día del período), **aprobado por**, **cliente o mina** con su **logo** opcional, servicio y la franja **gerencia / área / subárea**. Todo es editable salvo código y versión; los logos se suben desde el editor (se reducen en el navegador, hasta 150 KB cada uno) y se pueden quitar. **Firmas en cuadros:** cada firmante es una caja con «Nombre» y «Firma» dentro y el cargo como rótulo debajo, y puede llevar una **imagen** (firma o sello, PNG o JPG, hasta 60 KB, igual que el logo del encabezado) colocada dentro del cuadro en pantalla, PDF y Word; el usuario elige la cantidad de cuadros (1 a 8, cuatro por fila). **Cajas de fotos:** el usuario elige **filas × columnas** (hasta 8 × 4, por ejemplo 2 × 2), el **alto de la fila** (20 a 140 mm; el ancho es todo el ancho de impresión), qué mostrar al pie (hora, partida, descripción) y puede editar la descripción de cada foto. **Un clic en una caja** abre el listado de fotos del período; las de **otros días** salen agrupadas por día en un desplegable aparte. Un bloque de fotos anterior a las cajas se sigue viendo como antes (dos columnas con todas sus fotos). La pantalla y las tres descargas usan los mismos datos (`partesDeBloque`), de modo que la hoja se ve como sale el PDF. En pantalla ancha los tres paneles tienen su propio desplazamiento: **la lista de bloques (izquierda) y el banco de fotos (derecha) quedan fijos y solo se desplaza la hoja del centro** (Victor, 2026-10-18); en pantallas angostas la página se desplaza entera. El informe muestra una insignia «Informe diario» o «Informe semanal» con su código y un enlace «Crear otro informe (diario o semanal)»; los dos tipos se editan igual.

**Encabezado (cajetín) con cuadrícula y semana (Victor, 2026-10-18):** el código, la versión, la fecha de elaboración y el aprobador van en celdas con sus divisiones, y la celda de abajo del cliente lleva la semana del informe. La semana se elige en «Datos del servicio»: **semana del año** (ISO, empieza el lunes; la opción por defecto), **semana desde el inicio del servicio** (los 7 primeros días son la semana 1; el inicio se escribe o, vacío, es el primer día con parte) o no mostrarla. Se cuenta con el último día del período. **Firmas:** sin cuadros guardados el editor ya muestra los dos de siempre (Elaboró y Revisó) para poder ponerles nombre o imagen.

**Barra de sección con resumen (Victor, 2026-10-18):** cada sección lleva una barra azul con una pestaña de acento a la izquierda y un filete del mismo color abajo. El acento se elige en el bloque «Datos del servicio» entre una paleta de seis colores (turquesa por defecto; no hay amarillo) y vale para todo el informe. A la derecha de la barra, los bloques de datos (indicadores, PPC, curva S, avance por nivel y por partida, actividades, personal, equipos, inasistencias y costos) muestran hasta 4 cifras chicas, con barrita de progreso si son porcentaje. Salen del mismo dato congelado del bloque (sin dato no hay cifras) y el usuario marca cuáles ver en el panel del bloque; sin elegir, salen las de siempre. Con cifras, la barra no muestra el origen del dato. Aplica a pantalla, PDF y Word (en Word, una línea bajo el título); Excel no cambia.

**Alineación y decimales de las tablas del informe (Victor, 2026-10-18):** la cabecera de cada columna va centrada y **los datos van a la derecha**; solo las columnas de texto largo (descripción, nombre, cargo, equipo, observaciones, causa, motivo) van a la izquierda para poder leerse. **Toda cifra lleva siempre dos decimales** (metrados, horas, porcentajes, índices; los conteos y numeraciones como N.º y versión son enteros). *(Difiere del `design.md` § Alineación de columnas, que alinea la cabecera igual que el dato; queda pendiente que Victor confirme cuál manda para los informes.)*

**Inasistencias en el informe.** Bloque de datos opcional «Inasistencias» (no viene en ningún formato por defecto; se agrega con «Agregar bloque»): persona, DNI, turno, motivo y observación de las inasistencias que el RDT registró en el período, de partes no rechazados; lo que aún no se valida se avisa bajo la tabla. Son informativas: no suman horas ni costo (Victor, 2026-10-18; antes las inasistencias solo vivían en su pestaña).

**Tablas de actividades.** En el diario, «Actividades ejecutadas» solo lleva actividades **directas (D)**, con las columnas N.º, Turno, Descripción, WBS, Un., **Contractual, Acumulado, Restante, Metrado del día** y **Observaciones** (sin «% avance» y **sin columna «Estado»**: lo pendiente de validación se avisa en una línea bajo la tabla, «Reportado, pendiente de validación: …»; Victor, 2026-10-18; el orden respeta el de metrados del `design.md`). En el semanal, las columnas de día van como DD/MM, más Restante y % avance. Las actividades **contributorias y no contributorias** van en su **propia caja** (bloque «Actividades contributorias y no contributorias», con horas, sin metrado), no en la tabla de partidas. El bloque «Avance de una partida» pasa a llamarse **«Actividades ejecutadas acumuladas personalizadas»**: el usuario marca con un check las partidas que quiere, **o un grupo completo**: las partidas se muestran agrupadas por los niveles del presupuesto (área, subpresupuesto, paquete de partidas) en grupos plegables con casilla a medias, buscador y «Marcar las que se ven»; la tabla muestra WBS, descripción, Un., contractual, acumulado validado a la fecha, restante y % de avance; un bloque anterior con una sola partida (`wbs`) se sigue leyendo.

El **color de la hoja de trabajo** (blanca, crema, gris u oscura, con su marco) lo elige cada usuario y solo es de pantalla: la descarga siempre sale blanca. **La hoja se ve partida en páginas A4** («Hoja 1 de N», los bloques no se parten: el que no cabe pasa a la hoja siguiente) y la vista previa dice cuántas hojas ocupa; el botón «Contar hojas del PDF» pide al servidor el PDF real y muestra cuántas hojas trae (`GET …/descargar?formato=pdf&contar=1`). **El PDF se dibuja con las mismas medidas que la hoja** (margen de 10 mm, encabezado de tres columnas con LOGO, barra azul de sección con su origen, tarjetas de indicadores, tablas, cajas de fotos de filas × columnas, cuadros de firma, «Hoja X de N» al pie); la tipografía no es idéntica (Helvetica en el PDF), así que algún salto de línea puede mover un corte: la cantidad de la vista previa es una muy buena aproximación, no una garantía (decidido por Victor el 2026-10-18: se reescribe el PDF con `pdfkit`, no se usa un navegador sin pantalla).

* **Bloques de datos del servicio** (se llenan solos): encabezado y datos del servicio, indicadores al corte, actividades ejecutadas, actividades contributorias y no contributorias, personal, equipos, avance por nivel (el usuario marca qué profundidades del presupuesto ve: nivel 1, 2, 3…; el servicio puede tener de 2 a 5; sin marcar, todas; columnas iguales a las de «Actividades ejecutadas»: WBS, Descripción, Un., Contractual, Acumulado y Restante; como un nivel mezcla unidades, no suma metrado: se mide en % ponderado por presupuesto, con Un. «%», Contractual 100 %, Acumulado su avance y Restante lo que falta; Victor, 2026-10-18), Curva S física, PPC y causas, actividades ejecutadas acumuladas personalizadas, Plan Maestro próximos 7 días, lista de diarios del período.
* **Bloques libres:** texto, fotos, tabla, clima y turno, firmas.
* **Bloques sin fuente automática** (semáforo, incidencias, logros y alertas, restricciones, próximas actividades y fotos destacadas) **congelan lo que el usuario escribió**: no se calcula ningún semáforo ni se inventan umbrales.
* **Claves de `config` oficiales:** TEXTO `{texto}`; TABLA `{columnas[], filas[][]}`; CLIMA_TURNO `{clima, turno, observacion}`; FIRMAS `{firmantes[{nombre, cargo, imagen}]}`; AVANCE_NIVEL `{niveles[profundidades]}`; FOTOS y FOTOS_DESTACADAS `{columnas, filas, altoMm, cajas[idFoto|null], pies{idFoto: texto}, mostrar}`; ENCABEZADO `{empresa, logoPropio, logoCliente, titulo, fechaElaboracion, aprobadoPor, cliente, servicio, gerencia, area, subarea}`; INCIDENCIAS, RESTRICCIONES y PROXIMAS_ACTIVIDADES `{items[]}`; LOGROS_ALERTAS `{logros[], alertas[]}`; SEMAFORO `{estado: VERDE|AMARILLO|ROJO, texto}` (lo elige el usuario); AVANCE_PARTIDA `{partidas[wbs]}` (antes `{wbs}`) y COSTO_PARTIDA `{wbs}`. Las fotos de un bloque son las de `fotos_campo` con ese `bloqueId`. Un bloque AVANCE_PARTIDA sin ninguna partida elegida impide emitir.
* **Traer del informe anterior:** al crear, «Restricciones y pendientes» y «Próximas actividades» arrancan con lo del último informe emitido del mismo tipo.

## Período del semanal

* **Configurable** (desde – hasta). Al crear hay atajos «Semana en curso» (lunes a hoy), «Semana anterior», «Últimas 2 semanas» (los 14 días que terminan hoy), «Mes anterior» y «Personalizado». Debajo, un resumen: días del período, días trabajados, diarios emitidos, días sin diario emitido y si las columnas irán por día o por semana.
* **Límites** (validados también en el servidor): no antes del inicio de ejecución del servicio, **Hasta no después de hoy** (fecha de Lima), Desde no posterior a Hasta y **máximo 3 meses** (Hasta ≤ Desde + 3 meses − 1 día).
* **Hasta 10 días las tablas van por día; más de 10, por semana.** Si el período pasa de 7 días el título es «Informe del período». El código sigue siendo `{N° OT}-IS-{n}`.
* **Se arma con los diarios emitidos del período**: propone actividades, avance y fotos de los diarios. Un día trabajado sin diario emitido entra solo con los datos del RDT (validado o «reportado, pendiente de validación»), sin texto ni fotos, y la pantalla avisa antes de crear.
* **Resumen de Nuevo:** «trabajados» = días con parte RDT no rechazado; «diarios emitidos» = informes DIARIO emitidos (sin Costos) con fecha en el período; «sin diario» = trabajados sin diario emitido.
* **Un período que se cruza con otro semanal emitido se permite** (cada informe guarda su propio período) y la pantalla solo lo avisa.
* Se puede cambiar desde el editor mientras sea borrador; al emitir queda congelado.

## Foto de campo y banco de fotos

* **Foto de campo:** el chip abre una pantalla con el botón «Tomar foto» (un navegador no abre la cámara sin un toque). Pide servicio, actividad (partida o paquete, opcional) y **descripción obligatoria**; guarda hora y, si el usuario lo permite, GPS. Solo JPEG, hasta 3 MB; el navegador reduce la imagen a 1600 px antes de subirla. La cabecera `Permissions-Policy` permite la ubicación solo para la propia app (`geolocation=(self)`, decidido por Victor el 2026-10-16); la cámara no se tocó.
* **Banco de fotos del servicio:** cada foto queda en el banco del servicio y del día (hora de Lima). Muestra las fotos de **todo el servicio**, no solo las propias; **cualquier foto del servicio se puede asignar a un borrador propio** mientras no esté en un informe emitido. En un semanal se ve el período completo del informe. **El banco lo ven y usan los 13 roles** dentro de sus servicios (Victor, 2026-10-17); subir una foto de campo sigue siendo solo de los 4 roles de campo.
* **Quitar un bloque** libera sus fotos; al emitir no queda ninguna foto bajo un bloque inexistente.
* Fuera de esta versión: guardar fotos sin señal y subirlas después, y editar fotos (recorte o anotaciones).

## Descarga

* **PDF** (igual a la vista previa), **Word** `.docx` (editable) y **Excel** `.xlsx` (una hoja por bloque y una hoja «Fotos» con miniatura, descripción y partida). Los tres salen de un único modelo de documento, así que llevan los mismos datos.
* **Alcance:** *completo*, *resumen* (Datos del servicio, Semáforo, Indicadores, Logros y alertas, Avance por nivel, Costos-indicadores y Firmas) o *fotos* (Datos del servicio y bloques de fotos).
* Los importes no llevan símbolo de moneda. Un **borrador** se descarga igual que un emitido: sin marca «BORRADOR» en el PDF, Word ni Excel, ni en el título ni en el nombre del archivo (Victor, 2026-10-18).
* Las fotos se reducen a 1000 px (JPEG calidad 70) al incrustarlas para que el archivo quepa en el límite de respuesta de la función de servidor (~4,5 MB, por confirmar contra el plan de alojamiento). Medido con 6 fotos: unos 360 KB por archivo; la ruta tiene `maxDuration = 60`.
* **Quién descarga:** quien puede ver el informe (los 13 roles para los que no son Costos; Costos solo los 5 con economía).

## Aviso al emitir

Al emitir se notifica en `/notificaciones` (tipo `MENSAJE`) a los **miembros del servicio**, menos el autor. La app no tiene «seguir un servicio». Un fallo al notificar no deshace la emisión.

## Pestaña Inasistencias

Pestaña propia dentro de «Informes de supervisión», aparte de los informes (sin chip propio): lista las inasistencias que ya se registran en el RDT (persona, DNI, motivo, nota, fecha, servicio y RDT de origen).

* **Filtros:** **Diario** (una fecha, hoy en Lima por defecto) o **Semanal** (desde – hasta, con el mismo control de período del informe semanal); **todos mis servicios** o **uno en particular**.
* **Descarga en PDF** con el filtro aplicado.
* **Quién:** los 13 roles, siempre dentro de los servicios asignados al usuario (el administrador ve todos).
* **Fuente:** solo partes que no estén `RECHAZADO`. Los límites son desde ≤ hasta, hasta ≤ hoy (fecha de Lima) y máximo 3 meses; **no exige «Desde ≥ inicio de ejecución»**, porque con «Todos mis servicios» no hay un solo inicio de ejecución.
* **Las inasistencias van en su pestaña y, además, un informe puede llevar el bloque opcional «Inasistencias»** (cambio pedido por Victor el 2026-10-18; antes decía que no iban dentro de los informes).

## Qué no hace

* No calcula avance ni costo por su cuenta: usa el PR, la Curva S y el RDT.
* No tiene aprobación previa de la jefatura, informe mensual ni de cierre; el «Acta de conformidad» sigue sin pantalla.
* No muestra dinero salvo en el formato Costos y solo a los 5 roles con economía.
