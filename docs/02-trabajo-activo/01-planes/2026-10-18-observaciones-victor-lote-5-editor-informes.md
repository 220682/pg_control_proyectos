# 2026-10-18 — Observaciones de Victor, Lote 5 (editor de informes de supervisión)

> Lote de trabajo tradicional, sin flujo de Orquestador: Victor revisó el editor de informes en la app real y lo comparó con la maqueta [`informes-supervision.html`](../../05-diseno-y-referencias/mockups/informes-supervision.html). El agente investiga, propone, y construye en tandas; cada tanda se verifica con login real antes de pasar a la siguiente.

## Identificación y estado

- Fecha: 2026-10-18
- Estado: **Lote cerrado en código y documentación; falta autorización de Victor para el commit y push de los dos repositorios y su revisión en pantalla.** T1 a T7 y las tandas L5-13 a L5-27 (orden de columnas, firmas con imagen, partidas por grupo, inasistencias, alineación, estilo A con resumen en la barra) están construidas en `py_control_proyectos_web` (la primera parte ya se desplegó el 2026-10-18; lo posterior está sin commit). Tipos, pruebas y PDF de muestra en verde. `db/110_informes_codigo_por_fecha.sql` aplicada por Victor. Pendiente: verificación en pantalla con login (sin navegador disponible en esta sesión)
- Flujos que cambian: [22](../../04-flujos-de-negocio/22-informes-de-supervision.md) (descarga, código, editor, fotos, formatos), [16](../../04-flujos-de-negocio/16-paneles.md) si cambia alguna pantalla, [14](../../04-flujos-de-negocio/14-accesos-y-restricciones.md) solo si cambia algún permiso (hoy ninguno).

## Observaciones (Victor)

| # | Observación | Hallazgo verificado en el código |
|---|---|---|
| L5-1 | Al descargar un borrador no debe decir que es borrador | `generarPdf` (marca diagonal y «(BORRADOR)» en el título), `word.ts` (encabezado y título) y `excel.ts` (fila «BORRADOR») la ponen cuando `d.borrador`. Contradice la regla escrita en flujo 22 § Descarga: se cambia el flujo |
| L5-2 | No sabe cómo agregar fotos | Solo hay asignación desde el banco con un `select` por foto; no hay forma de crear cajas dentro del informe ni elegir cuántas |
| L5-3 | En el servicio de prueba, fecha 18/10, hay CNC y no aparecen en «PPC y causas» | **Corregido en código (2026-10-18; sin acceso a los datos para confirmar cuál era el caso):** el Dashboard cuenta toda actividad con causa de partes VALIDADOS, y el informe solo las directas; ahora el Pareto del informe cuenta igual que el Dashboard y lo no validado sale como «Causas reportadas, pendientes de validación». Hipótesis original: `armarPpc` (`src/lib/informes/bloques-avance.ts`) solo cuenta partes con estado VALIDADO y solo actividades de tipo `D`; un RDT del 18/10 sin validar, o con CNC cargadas como `C`/`NC`, sale «0 actividades / Sin registros». Si es así: mostrar «reportado, pendiente de validación» como ya hacen los otros bloques |
| L5-4 | No sabe cómo editar un campo del informe (el de «Próximas actividades — Sin elementos») | Se edita solo seleccionando el bloque en la lista de la izquierda y buscando el panel «Editar» más abajo; en la hoja no se puede hacer clic. Cambio: clic en un bloque de la hoja lo selecciona y abre su edición ahí mismo |
| L5-5 | El desplegable «Mis formatos» no deja ver las opciones y sale blanco | Los `<select>` usan fondo translúcido blanco y las opciones heredan blanco sobre blanco. Cambio: estilo de opciones en el tema oscuro |
| L5-6 | El entorno de trabajo no es el de la maqueta: es más simple, sin tantos colores | Falta lo de la maqueta: columna de bloques con etiqueta Dato/Libre y casilla de visible, encabezado del informe con LOGO, código, versión y fecha, barras azules de sección con origen («dato del sistema · RDT»), banco de fotos a la derecha con «en inf.»/«sin ubicar» y el botón «Ubicar las N sin ubicar» |
| L5-7 | Ver cuántas hojas tendrá el informe para cuadrar fotos y campos | Hoy la vista previa es HTML corrido y el PDF lo dibuja `pdfkit` aparte; no hay forma de saber cuántas hojas saldrán |
| L5-8 | Fotos: campo con la cantidad (ej. 4) y salen 4 cajas; arrastrar, achicar y agrandar; clic en la caja abre el banco para elegir; ver u ocultar y editar la descripción | Hoy solo se edita el título del bloque Fotos. `FOTOS {porPagina, mostrar}` ya existe en la configuración |
| L5-9 | Fondo de trabajo elegible (la descarga siempre sale blanca); lo mismo para firmas: elegir la cantidad de cuadros | La hoja del editor es blanca fija. Las firmas ya aceptan hasta 6 firmantes, pero sin vista de cuadros |
| L5-10 | Mostrar las partidas que quiera; cuadro de acumulados por partida y por nivel; en «por nivel» elegir el nivel según el presupuesto (hay presupuestos de 2, 3, 4 o 5 niveles) | `AVANCE_PARTIDA` es una sola partida; `AVANCE_NIVEL` no tiene selector de nivel |
| L5-11 | Código del informe correlativo y automático por fecha: el RDT más antiguo es 001; si luego se declara uno de fecha anterior, ese pasa a 002 y los siguientes se corren | Hoy el código sale de `siguiente_codigo_informe` (base): consecutivo por orden de creación, no por fecha |
| L5-12 | Logo: añadir uno o dos (cliente y propio) y editar el encabezado; todo editable | El encabezado muestra «CONTROL DE PROYECTOS» fijo; no hay bloque de encabezado editable ni subida de logo |

### Segunda tanda de observaciones (2026-10-18, con capturas)

| # | Observación | Resultado |
|---|---|---|
| L5-13 | El panel de edición se queda arriba al trabajar en la 2.ª hoja; **corregido por Victor: los paneles izquierdo y derecho no deben bajar, se desplaza el central** | Tres paneles con desplazamiento propio en pantalla ancha: laterales fijos, hoja central con su scroll (hecho) |
| L5-14 | Tabla «Actividades ejecutadas»: sin «% avance» ni «Validado»; con «Restante» y «Observaciones» | Hecho en pantalla, PDF, Word y Excel |
| L5-15 | «Avance de una partida» → «Actividades ejecutadas acumuladas personalizadas», con check de partidas y columnas contractual / actual / restante / % | Hecho |
| L5-16 | C/NC (ej. «Capacitación personal», con «7») no van en la tabla de partidas; en el RDT no debe haber metrado para ellas; caja aparte | Bloque nuevo `ACTIVIDADES_NC` (hecho); RDT: celdas de metrado deshabilitadas para C/NC, el servidor las guarda en null y no exige CNC por metrado (hecho) |
| L5-17 | No sabe cómo diferenciar diario y semanal ni crear uno u otro; el semanal también se edita | Insignia + código en la cabecera del editor y enlace «Crear otro informe» (la pantalla de crear ya existía) |
| L5-18 | Encabezado según el cajetín de Promcoser, con campos editables y logo | Hecho (logo `public/logos/promcoser.png`) |
| L5-19 | «Indicadores al corte» del semanal desfasado y tabla ancha que se pisa en la exportación | Tarjetas por grupos; tabla con letra adaptable y medidas calculadas (hecho) |
| L5-20 | Firmas como cajitas con cantidad elegible | Hecho |
| L5-21 | Fotos que se pisan; elegir filas × columnas, alto de fila y foto por caja (del día o de otros días) | Hecho (cajas, selector modal con desplegable por día) |

### Tercera tanda (2026-10-18, tras el despliegue)

| # | Observación | Resultado |
|---|---|---|
| L5-22 | Orden de columnas de «Actividades ejecutadas»: WBS, Un., Contractual, Acumulado, Restante, Metrado del día, Observaciones; sin «Estado»; lo mismo en «Avance por nivel» | Hecho; lo pendiente de validación se avisa en una línea bajo la tabla. «Avance por nivel» queda **igual que Actividades ejecutadas** (WBS, Descripción, Un., Contractual, Acumulado, Restante) con el nivel medido en % ponderado por presupuesto (Victor lo aclaró el 2026-10-18; antes el agente había supuesto otras columnas) |
| L5-23 | Firmas: opción de colocar imagen como en el encabezado | Hecho (pantalla, PDF y Word) |
| L5-24 | Elegir partidas por grupos (subpresupuesto, paquetes de partidas…), no sueltas | Hecho (árbol por niveles del presupuesto con casilla de grupo) |
| L5-25 | Campo para inasistencias; «por estándar, columnas al centro y datos a la derecha» | Bloque opcional «Inasistencias» (hecho). Alineación: cabecera centrada y cifras a la derecha en todas las tablas del informe; **contradice en parte `design.md`** (cabecera igual que el dato): Victor confirma cuál manda |
| L5-26 | Tres maquetas del estilo de los formatos, con un detalle más llamativo en la barra de sección; sin quitar el estilo actual; el nuevo, personalizable y con datos por defecto ampliables | Maquetas entregadas para elegir; Victor eligió el estilo A (pestaña de acento), sin amarillo ni más alto, y pidió ver el «pequeño dashboard»: ver L5-27 |
| L5-27 | Estilo A en la app: pestaña de acento (color elegible, sin amarillo; por defecto turquesa), barra casi del mismo alto y resumen en la barra con cifras chicas y barrita de progreso, personalizable | Hecho (pantalla, PDF y Word; Excel sin cambio). Cifras por defecto según el bloque; el usuario marca hasta 4 de un catálogo por bloque. Si hay cifras, la barra no muestra el origen del dato |
| L5-28 | Prueba en producción: datos siempre a la derecha y dos decimales; semana en el encabezado (del año o desde el inicio del servicio); cuadrícula en el cajetín; firma como imagen en los cuadros | Hecho (alineación y decimales en pantalla, PDF y Word; cajetín con cuadrícula y celda de semana; el editor de firmas muestra siempre los cuadros) |
| L5-29 | Exportación del Dashboard: una hoja con el Dashboard como la pantalla, la matriz de partidas y la Curva S enmarcada con título | Hecho en el PDF (flujo 11 § Descargar). Pendiente: probarlo con un servicio real |
| L5-30 | Prueba en producción (2026-10-19): letra mayor en la descripción de las fotos; fotos como figuras («Figura N°01», consecutivas, sin cortar, ajustadas al cuadro, como el Excel de referencia); «Avance por nivel» con barrita de avance al final (en % físico: Victor aclaró que no quiere metrados); columna «Avance» con barrita en «Actividades ejecutadas»; datos del cajetín centrados en vertical | Hecho en pantalla, PDF y Word (y en la hoja «Fotos» del Excel); los datos del cajetín y de las celdas de tabla también quedan centrados en vertical. Pendiente: que Victor lo revise en pantalla |

## Decisiones de Victor (2026-10-18)

| Decisión | Resultado |
|---|---|
| Vista previa y cajas de fotos | **Hoja dividida en páginas A4 con «Hoja 1 de N» y cajas de fotos en cuadrícula**: ancho 1 o 2 columnas, alto S/M/L, reordenables arrastrando; clic en la caja abre el banco. El PDF sale igual a la pantalla porque ambos usan el mismo diseño. No se hace posicionamiento libre al píxel |
| Código correlativo | **Automático por fecha y renumera también los emitidos** (el código anterior queda en el historial). Cambia la regla «emitido congelado» solo para el código |
| Marca «BORRADOR» al descargar | Se quita en PDF, Word y Excel (dicho por Victor el 2026-10-18) |

## Plan por tandas

| Tanda | Contenido | Observaciones |
|---|---|---|
| T1 | Quitar «BORRADOR» de las tres descargas (**hecho**); desplegable oscuro legible (**hecho**, global en `globals.css`); verificar la hipótesis de L5-3 con datos reales y corregirla (**pendiente**: sin acceso a la base ni a un navegador con sesión) | L5-1, L5-5, L5-3 |
| T2 | Editor al estilo de la maqueta: lista de bloques con Dato/Libre, encabezado con logo, barras azules de sección, banco de fotos a la derecha, clic en la hoja para editar el bloque, fondo de trabajo elegible (**hecho**; el LOGO es todavía un recuadro fijo, se vuelve editable en T5; sin numerar secciones hasta T3, para no separar más la pantalla del PDF) | L5-4, L5-6, L5-9 |
| T3 | Hoja paginada con «Hoja X de N» y conteo real de hojas del PDF (**hecho**, vista previa por mediciones en pantalla). **Hecho también:** el PDF se reescribió con las medidas de la hoja (opción elegida por Victor: `pdfkit` con las mismas medidas, sin navegador sin pantalla). Límite conocido: tipografía distinta (Helvetica/Geist), un salto de línea puede mover un corte. Las fotos del PDF van fijas en 2 columnas hasta T4 (la opción «por página» deja de aplicar) | L5-7 |
| T4 | Bloque Fotos con cajas: cantidad, arrastrar, ancho/alto, clic para elegir del banco, descripción visible y editable | L5-2, L5-8 |
| T5 | Encabezado y logos editables (cliente y propio); firmas por cuadros | L5-12, L5-9 |
| T6 | Avance por nivel con selector de nivel según la profundidad del presupuesto (**hecho**: casillas por profundidad, `config.niveles`); partidas a elección con acumulados (**hecho**) | L5-10 |
| T7 | Código correlativo por fecha con renumeración e historial (**hecho en código y migración `db/110`, aplicada por Victor el 2026-10-18**: la app llama a `renumerar_codigos_informes` al crear, al cambiar la fecha y al borrar un borrador, y si la función no existe sigue con el código provisorio) | L5-11 (toca la base: Victor revisa y aplica la migración) |

## Reglas de negocio acordadas en esta tarea

| Regla | Dónde quedó |
|---|---|
| Un borrador descargado no lleva marca «BORRADOR» | Flujo 22 § Descarga (actualizado) |
| El editor rotula los bloques Dato/Libre, edita con un clic en la hoja y deja elegir el fondo de trabajo (solo pantalla) | Flujo 22 § Editor por bloques (actualizado) |
| Las actividades C y NC no llevan metrado en el RDT ni van en la tabla de partidas del informe | Flujo 06 (actualizado) y flujo 22 § Editor por bloques (actualizado) |
| El encabezado del informe es el cajetín de la empresa, editable salvo código y versión; las firmas son cuadros; las fotos van en cajas filas × columnas con alto elegido | Flujo 22 § Editor por bloques (actualizado) |
| Las inasistencias pueden ir dentro de un informe como bloque opcional | Flujo 22 § Pestaña Inasistencias y § Editor por bloques (actualizado; reemplaza «las inasistencias no van dentro de los informes») |
| Las tablas de actividades llevan Contractual, Acumulado, Restante antes del metrado del día y no llevan columna «Estado» | Flujo 22 § Editor por bloques (actualizado) |
| El código del informe es el correlativo por fecha entre los informes del servicio y se renumera al declarar uno de fecha anterior | Flujo 22 § Tipos, código y estados (actualizado en T7) |
| Cada sección lleva barra con pestaña de acento (color elegible, sin amarillo) y hasta 4 cifras de resumen con barrita de progreso, a elección del usuario | Flujo 22 § Editor por bloques, «Barra de sección con resumen» (actualizado) |
| «Avance por nivel» tiene las mismas columnas que «Actividades ejecutadas» pero medidas en avance físico en % (un nivel no suma metrados de unidades distintas) y al final «Avance» como barrita con cifra; «Actividades ejecutadas» lleva también la columna «Avance» | Flujo 22 § Bloques de datos y § Tablas de actividades (actualizado el 2026-10-19) |
| Cada foto va como figura: «Figura N°NN» consecutivo en todo el informe, foto entera sin cortar, descripción debajo en letra mayor; datos del cajetín y de las tablas centrados en vertical | Flujo 22 § Editor por bloques (actualizado el 2026-10-19) |
| En las tablas del informe la cabecera se alinea como sus datos (cifras a la derecha, texto largo a la izquierda) y los datos van centrados en vertical | Flujo 22 § Editor por bloques (actualizado el 2026-10-19); coincide con `design.md` § Alineación de columnas |

## Mejoras (de trabajo)

- Trasladadas al cierre del lote a [`2026-10-18-lote-5-informes-aprendizajes-de-trabajo.md`](../../03-aprendizaje-continuo/2026-10-18-lote-5-informes-aprendizajes-de-trabajo.md) (seis aprendizajes: copiar la referencia que Victor da, citar el documento normativo al consultar, cerrar con los apartados llenos, PDF de muestra como imagen, parches con Write, prueba inestable de avisos).

## Observaciones sobre la política

- **Resuelta (2026-10-19).** Se había anotado que `design.md` § Alineación de columnas (cabecera alineada como su dato) contradecía el estándar del informe (cabecera centrada). Victor aclaró que nunca pidió centrar la cabecera: pidió centrar en vertical los datos pegados arriba. Las cabeceras vuelven a alinearse como sus datos, que es lo que dice `design.md`; no hay contradicción y `design.md` no se toca.

## Carpetas/archivos huérfanos

- `py_control_proyectos_web/db/095_cerrar_lectura_directa.sql`: sin versionar desde antes de este lote. No se tocó; lo decide Victor.
