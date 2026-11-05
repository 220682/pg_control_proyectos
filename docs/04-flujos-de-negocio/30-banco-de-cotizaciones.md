# 30 — Banco de cotizaciones
> Lee si: la tarea toca el chip «Cotizaciones» del grupo Logística: subir la cotización de un proveedor en PDF, la lectura de sus datos e ítems, el buscador de precios (mínimo, promedio y último), el listado de cotizaciones, descargar o eliminar una cotización, los proveedores, o el cuadro comparativo por RQ.

Origen: sugerencia del área de Almacén, presentada por Victor el 2026-11-04 (plan [`2026-11-04-banco-de-cotizaciones`](../02-trabajo-activo/01-planes/2026-11-04-banco-de-cotizaciones.md)). Quién puede: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md), nota ²⁹. **Estado (2026-11-04): etapa 1 publicada (app `aad4e13` y `59d4d73`); falta que Victor aplique `db/134_banco_cotizaciones.sql`. Sin db/134 la pantalla abre pero no lista, no busca ni guarda.**

## Qué es

Una base **única para toda la empresa** con las cotizaciones de proveedores que reciben Almacén y Logística, para saber qué precio dio cada proveedor antes de comprar. Pantalla `/logistica/cotizaciones`, chip «Cotizaciones» del grupo Logística.

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
5. Guardar: el PDF se guarda tal cual, junto con los datos revisados.

**Cómo lee los ítems (sin IA, D4):** una fila es ítem cuando trae **cantidad × precio unitario = total** (con 1 % de tolerancia), con el precio y el total al final de la fila. La descripción se toma de la misma línea o de las de arriba. Cada proveedor arma su PDF distinto: en formatos donde el lector separa los números de las descripciones, los ítems salen con precio y la descripción vacía, para llenarla en la revisión. Probado con cotizaciones reales de PS-108 (Tradisa, Rotoplas, Alquimodul y Jofer).

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
- Arriba: **mínimo, promedio y último cotizado**, sin IGV, en S/ y US$.
- Una fila por ítem cotizado: descripción, unidad, cantidad, precio cotizado (con su marca c/IGV o s/IGV), precio sin IGV en S/ y US$, proveedor, fecha, válida hasta, servicio, quién la subió, y los botones **Ver PDF** y **Descargar PDF**.
- Orden por precio (más barato primero, por defecto) o por fecha (más reciente primero).
- Una cotización con **más de 6 meses** sale marcada «antigua».
- Las unidades pueden variar entre proveedores: la pantalla lo recuerda; la app no las convierte.
- Al tocar la descripción se abre la cotización completa.

## Cotizaciones (listado)

Todas las cotizaciones de la empresa, de la más reciente a la más antigua: fecha, N°, proveedor, RUC, total, ítems, válida hasta, servicio y quién la subió. Se abren para ver sus ítems y se ven o descargan en PDF, **las haya subido quien las haya subido**.

**Filtros (comunes a las dos pestañas):** moneda, desde, hasta y servicio; en el listado, además, el proveedor.

## Eliminar

Solo **quien la subió o el administrador**, con confirmación. Se borran la cotización, sus ítems y el PDF, y queda registrado quién la eliminó y cuándo (tabla `cotizaciones_eliminadas`).

## Datos

Migración aditiva `db/134_banco_cotizaciones.sql`:

- `proveedores`: RUC único (opcional) y razón social.
- `cotizaciones`: proveedor, N°, fecha, moneda, precios con o sin IGV, tipo de cambio, válida hasta, plazo, forma de pago, observaciones, servicio y RQ opcionales, total, ruta del PDF (`documentos-proyecto/cotizaciones/`), quién la subió y cuándo.
- `cotizacion_items`: descripción, unidad, cantidad, precio unitario tal cual, precios sin IGV en S/ y US$, y el texto normalizado para el buscador (índice de trigramas).
- `cotizaciones_eliminadas`: quién eliminó qué cotización y cuándo.

Sin lectura directa (RLS sin políticas): todo pasa por el servidor, que valida el rol en cada ruta (`api/cotizaciones`, `/leer`, `/buscar`, `/[id]`, `/[id]/pdf`).

## Etapas siguientes (aprobadas en el Spec, sin construir)

- **Etapa 2 — Cuadro comparativo por RQ:** se eligen 2 o más cotizaciones de un RQ; material por proveedor con el mejor precio resaltado, total por proveedor, plazo y forma de pago; se marca la cotización elegida (con historial); descarga en Excel y PDF con el encabezado configurable.
- **Etapa 3 — Proveedores e historial:** ficha del proveedor, historial de precio de un material y precio cotizado contra precio pagado (Registro de costos).

## Fuera de alcance

Fotos, Excel o capturas (D3); lectura con IA o agentes (D4); pedir cotizaciones o enviar correos a proveedores; órdenes de compra.
