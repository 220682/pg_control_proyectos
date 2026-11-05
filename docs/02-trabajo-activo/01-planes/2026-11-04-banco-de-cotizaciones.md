# Banco de cotizaciones (Logística)

## Identificación y estado

Tema: base única de cotizaciones de proveedores, con buscador de precios y descarga. Sugerencia del área de Almacén. Fecha: 2026-11-04. Estado: `Implementando (etapas 1, 2 y 3 publicadas; falta db/136 y la revisión de Victor)`.

- Gate Spec: `aprobado por Victor (2026-11-04, «por lo demás está bien» y «continua»)`
- Gate 1: `aprobado por Victor (2026-11-04, «continua»)`
- Gate 2: `pendiente`

## Spec

### Estado

`Aprobado (Gate Spec)` — Victor, 2026-11-04. P1 y P2 se toman con la propuesta del Orquestador (ver Registro de decisiones); Victor puede cambiarlas.

### Problema y contexto

Almacén y Logística reciben cotizaciones de proveedores en PDF y no tienen dónde guardarlas ni cómo consultar después qué precio dio cada proveedor. Cada compra empieza de cero, sin saber cuánto se pagó o cotizó antes por el mismo material.

### Resultado esperado

1. Un apartado **«Banco de cotizaciones»** donde Logística sube las cotizaciones en PDF.
2. Una **sola base para toda la empresa** (no por servicio).
3. Un **buscador de precios** que, al escribir un material, devuelve lo que cotizó cada proveedor.
4. **Cualquiera con acceso descarga** la cotización que subió otro.
5. Un **cuadro comparativo** de proveedores para un RQ.

### Decisiones de Victor (2026-11-04)

- **D1 — Logística ve los precios.** «Ellos manejan precios con normalidad». Es una excepción acotada a la regla 2 del flujo 14 (las interfaces con montos solo las ven 5 roles): en esta pantalla también entra Logística. El Registro de costos no cambia.
- **D2 — Una sola base para toda la empresa**, no por servicio. El servicio y el RQ son datos **opcionales** de cada cotización.
- **D3 — Solo PDF.**
- **D4 — La app funciona sola, sin agentes ni IA.** Cualquier usuario sube y consulta desde la app. La lectura del PDF la hace la propia app con su lector de PDF (el mismo del Registro de costos). Si el PDF es una imagen escaneada sin texto, la app avisa y la persona llena los datos a mano.

### Alcance

**Etapa 1 — Subir, revisar, buscar y descargar**

- **Subir:** PDF de hasta 4 MB. La app lee:
  - los **datos generales**: proveedor, RUC, N° de cotización, fecha, moneda, vigencia, plazo de entrega y forma de pago;
  - los **ítems**: descripción, unidad, cantidad, precio unitario y total.
- **Revisión antes de guardar:** la persona ve lo leído y corrige, agrega o quita ítems. La app no inventa: lo que no pudo leer queda vacío.
  - Cada proveedor arma su PDF distinto, así que no siempre acertará con todos los ítems; la revisión es la que asegura el dato.
- **Dato opcional:** servicio y RQ (y, si se elige el RQ, sus materiales).
- **Duplicados:** si ya existe una cotización del mismo RUC con el mismo N° y fecha, la app avisa antes de guardar.
- **Proveedor:** se reconoce por el RUC. La primera vez se crea solo, con su razón social; las siguientes cotizaciones se juntan bajo el mismo proveedor.
- **Precios:** se guardan en la moneda de la cotización, sin IGV, y además en soles y dólares al **tipo de cambio del día de la cotización** (el que ya usa el Registro de costos).
- **Buscador:** se escriben palabras del material (por ejemplo, «tubo 1 1/4 sch 40»).
  - Busca en la descripción de los ítems, sin importar mayúsculas, tildes ni el orden de las palabras.
  - Devuelve una fila por ítem cotizado: material, proveedor, fecha, precio unitario sin IGV (S/ y US$), unidad, vigencia y quién lo subió, con el botón **Descargar PDF**.
  - Arriba muestra el **precio más bajo, el promedio y el último**.
  - Las cotizaciones con más de 6 meses salen marcadas como **antiguas**.
- **Filtros y orden:** proveedor, rango de fechas, servicio y moneda; orden por precio o por fecha.
- **Listado de cotizaciones:** todas, con sus datos generales; se abren para ver sus ítems y se descargan.
- **Eliminar una cotización:** quien la subió o el administrador, y queda registrado quién y cuándo.

**Etapa 2 — Cuadro comparativo**

- Para un RQ se eligen 2 o más cotizaciones. La app arma el cuadro, material por proveedor, con el **mejor precio resaltado**, el total por proveedor, el plazo y la forma de pago.
- Se marca la **cotización elegida** (con historial).
- Descarga en **Excel y PDF**, con el encabezado de PDF configurable que ya existe.

**Etapa 3 — Proveedores e historial**

- **Ficha del proveedor:** RUC, contacto, cotizaciones, cuántas veces fue elegido y sus plazos.
- **Historial de precio** de un material en el tiempo.
- **Precio cotizado contra el precio pagado:** se liga con la compra del Registro de costos.

### No alcance

- Fotos, Excel o capturas de WhatsApp (D3: solo PDF).
- Lectura con IA o con agentes (D4).
- Pedir cotizaciones a proveedores desde la app, o enviarles correos.
- Órdenes de compra.

### Usuarios / roles afectados

- **Suben, ven precios, buscan y descargan:** los 5 roles que ya ven montos (administrador, jefe de proyectos, jefe de oficina técnica, supervisor de costos y jefe de costos) más el **supervisor de logística** (D1). Propuesta tomada para P1.
- Ninguna acción pide la OT a cargo: la base es de la empresa (D2) y Logística atiende todos los servicios (flujo 14, nota 28).

### Reglas de negocio y documentos afectados

- **Flujo nuevo 30 «Banco de cotizaciones»**: su línea `Lee si:` y su fila en el índice de flujos.
- **Flujo 14:** la interfaz y sus acciones, y la excepción D1 a la regla 2.
- **Flujo 16:** el chip en el grupo Logística.
- **Flujo 05:** la cotización ligada al RQ, y luego el cuadro comparativo.
- **Matriz de permisos (artefacto):** la actualiza Victor.

### Datos, API, migraciones o dependencias

- **Migración aditiva nueva**, `db/134` o el número libre siguiente; la aplica Victor y se le da la ruta completa del SQL. Tablas:
  - `proveedores`: RUC único y razón social;
  - `cotizaciones`: proveedor, N°, fecha, moneda, vigencia, plazo, forma de pago, servicio y RQ opcionales, ruta del PDF, quién subió y cuándo;
  - `cotizacion_items`: descripción, unidad, cantidad, precio unitario, total, precios en S/ y US$, y el texto normalizado para buscar.
  - Con índices para que la búsqueda sea rápida.
- **Archivos:** el PDF se guarda en el almacenamiento de la app, igual que las compras del Registro de costos.
- **Lectura:** el lector de PDF que ya se usa (`pdf-parse`) más reglas propias para encontrar las filas de ítems (líneas con cantidad, unidad y precio). Sin servicios externos (D4).
- **Rutas del servidor:**
  - leer el PDF (no guarda nada);
  - guardar la cotización;
  - buscar;
  - descargar el PDF;
  - eliminar la cotización.
  - Todas validan el rol en el servidor.

### Diseño / UI aplicable

- Chip **«Cotizaciones»** en el grupo Logística, para toda la empresa; no pide servicio.
- Pantalla a ancho completo con dos pestañas, **Buscar precios** y **Cotizaciones**, más el botón **Subir cotización**.
- La ventana de revisión imita la del Registro de costos (subir, leer, revisar, guardar), con la tabla de ítems editable.
- Se verifica con captura propia a 1366 px y a 1920 px.

### Riesgos y decisiones pendientes

- **R1 — La lectura de ítems no será perfecta.** Cada proveedor usa otro formato. Por eso la revisión es obligatoria y se pueden agregar ítems a mano. Más adelante se puede recordar el formato de cada proveedor por su RUC, para leer mejor sus siguientes cotizaciones.
- **R2 — Un mismo material se escribe de varias formas.** El buscador por palabras lo cubre en la etapa 1. Agrupar los nombres en un catálogo de materiales queda para después, si hace falta.
- **P1 — ¿Quiénes entran a la pantalla?** La propuesta es la lista de «Usuarios / roles afectados». ¿Se agrega o se quita alguno?
- **P2 — ¿Quién puede eliminar una cotización?** La propuesta: quien la subió y el administrador.

### Criterios de aceptación

1. Logística sube un PDF con texto y ve los datos generales y los ítems leídos; corrige y guarda.
2. Un PDF escaneado sin texto avisa y deja llenar los datos a mano.
3. Al buscar un material salen todos los proveedores que lo cotizaron, con precio en S/ y US$, fecha y botón para descargar el PDF de cualquier usuario.
4. Mínimo, promedio y último precio correctos; las cotizaciones de más de 6 meses salen marcadas.
5. Una misma cotización no se guarda dos veces sin aviso.
6. Un rol fuera de la lista no ve el chip, y el servidor le responde 403.
7. Nada de la pantalla usa IA ni servicios externos.

### Estrategia de prueba / evidencia

- Pruebas automáticas: la lectura con textos de PDF reales (sin datos sensibles), el buscador (tildes, orden de palabras, mayúsculas), los precios en las dos monedas y los permisos por rol.
- Prueba en la app publicada con cotizaciones reales de PS-108 que entregue Victor.
- Captura a 1366 px y a 1920 px.

### Aprobación (Gate Spec)

`Aprobado` — Victor, 2026-11-04.

## Registro de decisiones

- (2026-11-04, Orquestador) P1 y P2 con la propuesta: entran los 5 roles con economía más Logística; elimina quien subió o el administrador. Si Victor dice otra cosa, se cambia.
- (2026-11-04, Orquestador) Lectura de ítems sin IA (D4): una fila es ítem cuando trae **cantidad × precio unitario = total** (con 1 % de tolerancia). La descripción se toma de la misma línea o de las líneas de arriba. Probado con los textos de 4 cotizaciones reales de PS-108 (Tradisa, Rotoplas, Jofer, Alquimodul). En formatos donde el lector separa los números de las descripciones (Jofer), los ítems salen con precio y la descripción vacía, para llenarla en la revisión.
- (2026-11-04, Orquestador) «Queda registrado quién y cuándo» al eliminar: tabla `cotizaciones_eliminadas` en la misma db/134 (aún sin aplicar, así que no hizo falta otra migración).
- (2026-11-04, Orquestador) «Si se elige el RQ, sus materiales» se deja para la etapa 2 (cuadro comparativo): en la etapa 1 el RQ solo queda ligado a la cotización.
- (2026-11-04, Victor) «mejoralo, colócale autocompletado en el buscador; no se pudo subir la cotización 2061 de Jofer; e implementa lo que falta» → arreglo del lector, autocompletado y etapas 2 y 3.
- (2026-11-04, Orquestador) La 2061 fallaba porque el PDF guarda los números lejos de las descripciones. La app ahora lee el PDF también **por posición en la hoja** y se queda con la lectura que saca más ítems con descripción. Se verificó en producción, y la 2061 ya está en el banco, ligada a PS-108.
- (2026-11-04, Orquestador) Cuadro comparativo: de 2 a 6 cotizaciones por RQ. La propuesta de qué ítem corresponde a cada material es por parecido de palabras, con las medidas valiendo el doble, y la corrección a mano manda. El mejor precio se marca solo con 2 o más precios. El total en verde es el menor entre las cotizaciones que cotizan todo. El motivo de la elección es obligatorio en la pantalla. Se compara contra las cotizaciones del RQ y las de su servicio.
- (2026-11-04, Orquestador) En la ficha del proveedor, «cotizado contra pagado» se muestra **solo a los 5 roles con economía**, porque son montos del Registro de costos; esto no cambia D1 (Logística ve precios de cotizaciones). Pagado = `proyecto_compras` con el mismo RUC en el mismo servicio, en US$ sin IGV.
- (2026-11-04, Orquestador) Los datos del proveedor los editan los 6 roles del Banco; el RUC no se cambia. El responsable del encabezado del PDF del cuadro lo cambian los 6 roles; la empresa y el logo, solo el administrador (como en los demás PDF).
- (2026-11-04, Orquestador) **«Precios con IGV»** es un dato de cada cotización: se detecta comparando la suma de los ítems con el subtotal y con el total, y se puede corregir en la revisión. El buscador muestra siempre el precio **sin IGV**.

## Punch List

| # | Ítem | Estado |
|---|---|---|
| 1 | Migración aditiva `db/134_banco_cotizaciones.sql` (proveedores, cotizaciones, ítems e índices) | Hecho (app `aad4e13`, `59d4d73`); **sin aplicar**: la aplica Victor |
| 2 | Lectura del PDF: datos generales e ítems, con pruebas sobre los textos reales | Hecho (17 pruebas) |
| 3 | Permisos, chip «Cotizaciones» en Logística, matriz base y pruebas de conteo | Hecho |
| 4 | Rutas: leer, guardar (con aviso de duplicado), listar, buscar, detalle, descargar PDF y eliminar | Hecho |
| 5 | Pantalla: Buscar precios, Cotizaciones y Subir con revisión | Hecho (publicada; Vercel compiló) |
| 6 | Verificación en la app publicada, capturas a 1366 y 1920 px | Hecho para la etapa 1 (db/134 aplicada; 2061 subida y buscada en producción) |
| 7 | Flujo 30 nuevo, flujos 14 y 16, índice; cambios para la Matriz de permisos | Hecho (también flujo 05); la Matriz la actualiza Victor (nota ²⁹ del flujo 14) |
| 8 | Lector por posición (cotización 2061) y autocompletado del buscador | Hecho (app `d7c8ed1`, verificado en producción) |
| 9 | Etapa 2: cuadro comparativo por RQ (selección, pares, mejor precio, totales y condiciones, elegir con motivo e historial, PDF y Excel con encabezado) y `db/136` | Hecho (app `314ba53`); **db/136 sin aplicar**: la aplica Victor |
| 10 | Etapa 3: pestaña Proveedores, ficha editable, cotizado contra pagado (solo economía) e historial de precios en Buscar | Hecho (app `314ba53`) |
| 11 | Pruebas: comparativo (4), exportar PDF y Excel (2), lectura por posición (3); tsc y eslint limpios | Hecho (284 pruebas de cotizaciones, PDF, permisos y config en verde) |
| 12 | Verificación en producción de las etapas 2 y 3, capturas a 1366 y 1920 px | En curso (lo que guarda espera db/136) |
| 13 | Flujos 30, 14 (cinco filas nuevas y nota ²⁹), 16 y 05 | Hecho; la Matriz la actualiza Victor (ocho filas del Banco) |

## Mejoras (de trabajo)

- (2026-11-04) Al proponer funciones de la app, no plantear IA ni agentes: la app debe funcionar sola para cualquier usuario (D4).

## Reglas de negocio acordadas en esta tarea

- D1 a D4 (arriba): pasan al flujo 30 y al flujo 14 al cerrar.
- Reglas del cuadro comparativo y de la ficha del proveedor (Registro de decisiones, 2026-11-04): ya integradas en el flujo 30, en la nota ²⁹ del flujo 14 y en el flujo 05.

## Observaciones sobre la política

- (ninguna por ahora)

## Carpetas/archivos huérfanos

- (ninguno por ahora)
