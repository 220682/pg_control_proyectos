# 30 — Banco de cotizaciones
> Lee si: la tarea toca el chip «Cotizaciones» del grupo Logística: subir la cotización de un proveedor en PDF, la lectura de sus datos e ítems, el buscador de precios (mínimo, promedio y último), el listado de cotizaciones, descargar o eliminar una cotización, los proveedores, o el cuadro comparativo por RQ.

Origen: sugerencia del área de Almacén, presentada por Victor el 2026-11-04 (plan [`2026-11-04-banco-de-cotizaciones`](../02-trabajo-activo/01-planes/2026-11-04-banco-de-cotizaciones.md)). Quién puede: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md), nota ²⁹. **Estado (2026-11-04): etapas 1, 2 y 3 publicadas (app `aad4e13`, `59d4d73`, `d7c8ed1`, `314ba53` y ajustes hasta `d22be39`). db/134 ya está aplicada; falta que Victor aplique `db/136_cuadro_comparativo_y_proveedores.sql`. Sin db/136 el cuadro comparativo se arma y se descarga con lo marcado en pantalla, pero no guarda la selección, las correcciones a mano ni la elección, y la ficha del proveedor no guarda los datos de contacto.**

## Qué es

Una base **única para toda la empresa** con las cotizaciones de proveedores que reciben Almacén y Logística, para saber qué precio dio cada proveedor antes de comprar. Pantalla `/logistica/cotizaciones`, chip «Cotizaciones» del grupo Logística, con cuatro pestañas: **Buscar precios**, **Cotizaciones**, **Cuadro comparativo** y **Proveedores**.

## Decisiones de Victor (2026-11-04)

| # | Regla |
|---|---|
| D1 | **Logística ve los precios** («ellos manejan precios con normalidad»). Es una excepción acotada a la regla 2 de la tabla 1 del flujo 14: entran los 5 roles con economía más el supervisor de logística. El Registro de costos no cambia (Logística solo lo carga). |
| D2 | **Una sola base para toda la empresa**, no por servicio. El servicio y el RQ son datos **opcionales** de cada cotización. Ninguna acción pide la OT a cargo. |
| D3 | **Solo PDF** (hasta 4 MB). Fotos, Excel o capturas de WhatsApp quedan fuera. |
| D4 | **La app funciona sola, sin agentes ni IA.** Cualquier usuario sube y consulta desde la app; la lectura la hace la propia app con su lector de PDF, el mismo del Registro de costos. |

Propuestas del Orquestador tomadas en el Gate Spec (Victor puede cambiarlas): entran los 6 roles de D1 (P1); elimina una cotización quien la subió o el administrador (P2).

## Subir una cotización

1. «Subir cotización» → se elige el PDF.
2. La app lee el PDF y propone:
   - **datos generales:** proveedor, RUC, N° de cotización, fecha, moneda, «válida hasta», plazo de entrega, forma de pago y total;
   - **ítems:** descripción, unidad, cantidad y precio unitario.
3. **Revisión obligatoria antes de guardar.** La persona corrige, agrega o quita ítems. La app no inventa: lo que no pudo leer queda vacío. No se guarda un ítem sin descripción.
4. Opcional: el **servicio** (se propone el del chip si se abrió desde un servicio) y el **RQ** de ese servicio.
5. Guardar: el PDF se guarda tal cual en **Cloudflare R2** (el mismo almacén de la [Gestión documentaria](25-archivos-documentarios.md)), y los datos revisados en la base. Ver y descargar pasan por el servidor, que comprueba el rol y redirige a un enlace firmado de 5 minutos.

**Cómo lee los ítems (sin IA, D4):** una fila es ítem cuando trae **cantidad × precio unitario = total** (con 1 % de tolerancia), con el precio y el total al final de la fila. La descripción se toma de la misma línea o de las de arriba. Cada proveedor arma su PDF distinto, así que la app lo lee de **dos formas** y se queda con la que saca más ítems con descripción: el texto en el orden en que viene guardado y el texto **ordenado por su posición en la hoja** (renglón por renglón, de izquierda a derecha). La segunda resuelve los PDF que guardan los números separados de las descripciones (caso de la cotización 2061 de Jofer para PS-108, 2026-11-04). En la lectura por posición la descripción es la celda más larga del renglón y el proveedor sale del membrete (nunca PROMCOSER, que es la empresa). Si aun así un ítem queda sin descripción, se llena en la revisión. Probado con cotizaciones reales de PS-108 (Tradisa, Rotoplas, Alquimodul, Dalka y Jofer).

**PDF escaneado:** si el PDF no tiene texto, la app avisa y deja llenar todo a mano; el PDF se guarda igual.

**Duplicados:** si ya existe una cotización del mismo proveedor con el mismo N° y fecha, la app avisa (quién la subió) y solo la guarda si la persona confirma.

**Proveedor:** se reconoce por el **RUC** (11 dígitos, opcional). La primera vez se crea solo con su razón social; las siguientes cotizaciones se juntan bajo el mismo proveedor. Sin RUC, se junta por la razón social.

## Precios

| Regla | Detalle |
|---|---|
| Precio tal cual | Se guarda el precio unitario como viene, en la moneda de la cotización. |
| Con o sin IGV | Es un dato de cada cotización: la app lo detecta comparando la suma de los ítems con el subtotal y el total, y se corrige en la revisión con la casilla «Los precios unitarios incluyen IGV». |
| Sin IGV en S/ y US$ | Cada ítem guarda además su precio **sin IGV** (18 %) en soles y en dólares, al **tipo de cambio venta SUNAT del día de la cotización** (si ese día no hay, el del día de hoy). El tipo de cambio se puede corregir en la revisión y es obligatorio. |
| Lo que muestra el buscador | Siempre el precio **sin IGV**. |

## Buscar precios

- Se escriben palabras del material, por ejemplo «tubo 1 1/4 sch 40». Busca en la descripción de todos los ítems **sin importar mayúsculas, tildes ni el orden**; cada palabra debe aparecer (hasta 8 palabras).
- **Autocompletado:** mientras se escribe, la caja propone hasta 8 descripciones ya cotizadas que tienen todas las palabras; se elige con el mouse o con las flechas y Enter (Escape cierra).
- Arriba: **mínimo, promedio y último cotizado**, sin IGV, en S/ y US$.
- Una fila por ítem cotizado: descripción, unidad, cantidad, precio cotizado (con su marca c/IGV o s/IGV), precio sin IGV en S/ y US$, proveedor, fecha, válida hasta, servicio, quién la subió, y los botones **Ver PDF** y **Descargar PDF**.
- Orden por precio (más barato primero, por defecto) o por fecha (más reciente primero).
- Una cotización con **más de 6 meses** sale marcada «antigua».
- Las unidades pueden variar entre proveedores: la pantalla lo recuerda; la app no las convierte.
- Al tocar la descripción se abre la cotización completa.
- **Historial de precios:** con 2 o más resultados, un gráfico muestra cada precio sin IGV en S/ en la fecha de su cotización, con una línea punteada que une el mínimo de cada mes. Al pasar el mouse por un punto se ven el precio, la unidad, el proveedor, la fecha y la descripción. Los filtros de arriba también lo filtran.

## Cotizaciones (listado)

Todas las cotizaciones de la empresa, de la más reciente a la más antigua: fecha, N°, proveedor, RUC, total, ítems, válida hasta, servicio y quién la subió. Se abren para ver sus ítems y se ven o descargan en PDF, **las haya subido quien las haya subido**.

**Filtros (comunes a Buscar precios y Cotizaciones):** moneda, desde, hasta y servicio; en el listado, además, el proveedor.

## Cuadro comparativo por RQ (etapa 2)

1. Se elige el **servicio** y luego el **RQ**. Las filas del cuadro son los **materiales del RQ** (descripción, unidad y cantidad del RQ).
2. Se marcan las cotizaciones a comparar: **mínimo 2, máximo 6**. Se ofrecen las ligadas a ese RQ y las del mismo servicio (marcadas «del servicio»). La primera vez la app propone las ligadas al RQ. Lo marcado queda guardado para el RQ.
3. **Qué ítem corresponde a cada material.** La app lo propone sola comparando las palabras de la descripción; las **medidas y números pesan el doble**. Prefiere dejar la celda vacía antes que proponer una pieza equivocada, porque un precio mal relacionado engaña al comparar. No propone cuando:
   - **la pieza no es la misma**: la primera palabra del material (codo, tubería, reducción, accesorios…) tiene que estar en el ítem, en singular o plural; «tubo» y «tubería» valen igual;
   - **las medidas no cuadran**: el material tiene una medida que el ítem no tiene y el ítem tiene otra que el material no tiene (codo de 45° contra codo de 90°; unión de 1" contra una de 1 1/2"). «5M» es «5 m», «10,000» es «10 000» y «½» es «1/2»;
   - **SAP contra SAL**, o **macho contra hembra**;
   - la palabra viene negada en el ítem: «tanque sin accesorios» no es «accesorios».

   Cada ítem de una cotización se usa para un solo material, y si ningún ítem se parece lo suficiente, la celda queda vacía. Bajo cada precio se ve el ítem relacionado y se puede corregir a mano: otro ítem, «No lo cotiza» o volver a la propuesta. **La corrección a mano manda** y queda guardada.
4. Por proveedor se muestran el **P.U. y el parcial** (cantidad del RQ × P.U.), **sin IGV**, en soles o en dólares a elección. Cada cotización se convierte con su propio tipo de cambio.
5. El **mejor precio** de cada material sale **en verde**, solo si al menos 2 proveedores lo cotizan.
6. Al pie, por proveedor: **total sin IGV**, materiales cotizados («n de N»), cuántos mejores precios tiene, **plazo de entrega**, **forma de pago** y **válida hasta**. El total en verde es el menor entre los proveedores que cotizan **todos** los materiales.
7. **Elegir cotización:** botón «Elegir» por proveedor, con un **motivo obligatorio** (por ejemplo «menor precio total y entrega en 3 días»). La elegida sale marcada «ELEGIDA» en azul. Se puede **quitar la elección**. Cada elección y cada retiro quedan en el **historial**, con quién, cuándo y el motivo.
8. **Descarga en PDF** (A4 horizontal, fondo claro) **y Excel**, con el mismo cuadro, la elegida con su motivo, y el **encabezado configurable** (botón «Encabezado», reporte «Cuadro comparativo de cotizaciones»): la empresa y el logo los cambia solo el administrador; el responsable lo cambian los 6 roles del Banco.

La app no elige por la persona: resalta precios y totales, y la elección la hace quien usa el cuadro.

## Proveedores (etapa 3)

**Listado:** proveedor, RUC, contacto, número de cotizaciones, fecha de la última, **veces elegido** en un cuadro comparativo y los plazos de entrega que suele ofrecer. Se filtra por razón social, RUC o contacto.

**Ficha del proveedor** (al tocar su nombre):

- **Datos:** contacto, teléfono, correo y notas. Los 6 roles del Banco los pueden editar, igual que la razón social. **El RUC no se cambia**, porque es lo que junta las cotizaciones del proveedor.
- **Sus cotizaciones:** fecha, N°, total, servicio, RQ y plazo, con acceso a cada una.
- **Elegido en:** servicio, RQ y motivo de cada vez que fue elegido.
- **Cotizado contra pagado** (US$ sin IGV), por servicio. Cotizado = suma de cantidad × precio de sus cotizaciones elegidas en ese servicio. Pagado = compras del **Registro de costos** con el **mismo RUC en el mismo servicio**. Se muestra la diferencia y el número de compras. Sin RUC no se puede cruzar.
  - **Lo ven solo los 5 roles con economía.** Logística ve precios de cotizaciones (D1), pero no los montos del Registro de costos (regla 2 de la tabla 1 del flujo 14, sin cambio). Para Logística la ficha no muestra este bloque.

## Eliminar

Solo **quien la subió o el administrador**, con confirmación. Se borran la cotización, sus ítems y el PDF, y queda registrado quién la eliminó y cuándo (tabla `cotizaciones_eliminadas`).

## Datos

Migración aditiva `db/134_banco_cotizaciones.sql`:

- `proveedores`: RUC único (opcional) y razón social.
- `cotizaciones`: proveedor, N°, fecha, moneda, precios con o sin IGV, tipo de cambio, válida hasta, plazo, forma de pago, observaciones, servicio y RQ opcionales, total, clave del PDF en R2 (`banco-cotizaciones/{id}/{nombre}`; las 3 cotizaciones subidas antes del 2026-11-05 tienen `cotizaciones/…` y siguen en el almacén de Supabase hasta moverlas), quién la subió y cuándo.
- `cotizacion_items`: descripción, unidad, cantidad, precio unitario tal cual, precios sin IGV en S/ y US$, y el texto normalizado para el buscador (índice de trigramas).
- `cotizaciones_eliminadas`: quién eliminó qué cotización y cuándo.

Migración aditiva `db/136_cuadro_comparativo_y_proveedores.sql` (etapas 2 y 3):

- `cuadros_comparativos`: uno por RQ, con las cotizaciones comparadas, la elegida, el motivo y quién la eligió y cuándo.
- `cuadro_comparativo_pares`: las correcciones a mano (material del RQ × cotización → ítem, o vacío = «no lo cotiza»).
- `cuadro_comparativo_historial`: cada elección y cada retiro, con proveedor, motivo, quién y cuándo.
- `proveedores`: además, contacto, teléfono, correo, notas y quién los cambió por última vez.
- Vuelve a crear `cotizaciones_eliminadas` si no existe, por si db/134 se aplicó antes de que se le agregara esa tabla.

Sin lectura directa (RLS sin políticas): todo pasa por el servidor, que valida el rol en cada ruta (`api/cotizaciones`, `/leer`, `/buscar`, `/sugerencias`, `/[id]`, `/[id]/pdf`, `/comparativo/[rqId]`, `/comparativo/[rqId]/descargar`, `/proveedores`, `/proveedores/[id]`).

## Fuera de alcance

Fotos, Excel o capturas (D3); lectura con IA o agentes (D4); pedir cotizaciones o enviar correos a proveedores; órdenes de compra.
