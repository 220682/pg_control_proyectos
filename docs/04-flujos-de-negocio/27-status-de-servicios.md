# 27 — Status de servicios (reporte mensual de Costos)
> Lee si: la tarea toca el chip «Status de servicios» del grupo Costos, el reporte mensual de presupuestos enviados y adjudicados, las visitas técnicas, las metas mensuales de venta, la carga del Excel «DASHBOARD - REPORTE MENSUAL» de Costos, su dashboard o su PDF vertical u horizontal.

Origen: pedido de Victor del 2026-11-03 («crear algo para el apartado de Costos» con el Excel de Costos que tiene base de datos, visitas técnicas y dashboard). Quién puede cada acción: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md), nota ²⁵. **Estado (2026-11-04): publicada, con registro a mano y comparación del Excel antes de guardar; falta aplicar `db/127_costos_status_servicios.sql`.**

## Qué es

Una pantalla de la empresa, **no de un servicio** (`/costos/status-servicios`, chip «Status de servicios» del grupo Costos; Victor pidió mantener ese nombre). Lleva a la app el Excel con que Costos controla sus **presupuestos**: los que envía al cliente, sus revisiones, los que se adjudican, y las **visitas técnicas**. Tiene tres pestañas:

- **Dashboard:** indicadores y gráficas del periodo elegido.
- **Presupuestos:** la tabla completa, con scroll horizontal y buscador.
- **Visitas técnicas:** la lista de visitas.

Un presupuesto **no necesita** estar ligado a un servicio de la app (Victor, 2026-11-03): muchos nunca llegan a ser servicio. La base guarda el vínculo como opcional (`proyecto_id`); la pantalla todavía no lo pide. Una **visita técnica** sí puede ligarse al presupuesto que salió de ella (opcional, al registrarla o corregirla en la app).

## Quién lo llena y quién lo ve

- **Llenan** (cargar el Excel, registrar, corregir y borrar presupuestos y visitas en la app, y editar las metas): **jefe de costos, supervisor de costos y, por ahora, el administrador**.
- **Ven** el dashboard y las tablas, y **descargan el PDF:** esos tres más el **jefe de proyectos** y el **jefe de oficina técnica**. Son los 5 roles con datos económicos (regla 2 de la tabla 1 del flujo 14).
- **Los demás roles** ven el chip **deshabilitado**, como siempre. El servidor responde 403 también por URL directa.

## Cargar el Excel

Los datos entran **de dos formas** (Victor, 2026-11-03: «cargar datos desde la app como también desde un Excel»): el Excel de Costos, que se carga cuando se quiere actualizar (por ejemplo, cada semana), y el registro a mano en la app (ver «Registrar y corregir en la app»).

**Antes de guardar, la carga compara el Excel con lo que hay en el sistema** y muestra qué va a cambiar (Victor, 2026-11-03: «antes se debe indicar qué datos se van a cambiar, es decir algún choque»). Nada se guarda hasta que quien carga confirma con «Aplicar N cambios»; lo confirmado se guarda en una sola transacción.

- **Cómo se reconoce cada fila:**
  - Un presupuesto, por su **N° de control**. Si el Excel o el sistema no lo tienen, por **código + descripción**. El código solo no basta: se repite (PS-056 y P-008 en el Excel del 2026-11-03).
  - Una visita, por **fecha + servicio**.
- **Lo que se muestra:**
  - **Nuevos:** están en el Excel y no en el sistema; se agregan.
  - **Cambios:** el Excel trae otro valor en un dato que nadie corrigió en la app. Se ve «valor actual → valor del Excel» y se aplica.
  - **Choques:** el Excel trae otro valor en un dato que se **registró o corrigió en la app**. Por defecto **se mantiene lo de la app**; quien carga puede elegir «Usar Excel» en cada choque o en todos.
  - **Solo en el sistema:** están en la app y no en el Excel. **Se conservan**, salvo que quien carga marque «Borrar».
  - **Metas:** se reemplaza la meta de cada mes que trae el Excel. Si esa meta se editó en la app, es choque.
  - **Iguales:** solo se cuentan.
- Si el Excel ya coincide con lo corregido en la app, ese dato deja de contarse como «corregido en la app».
- Si alguien cambia algo en el sistema mientras otro revisa la comparación, la carga no se aplica y pide volver a comparar.

- **Se respetan las columnas:** cada dato se busca por el **nombre de su columna**, no por su posición:
  - En la hoja de presupuestos: No CONTROL, RESPONSABLE, CODIGO PS, GERENCIA, DESCRIPCION, FECHA DE SOLICITUD, MONTO, FECHA DE ENVIO, TR / DIAS, NIVEL DE RESPUESTA, REVISIÓN 1, FECHA2, REVISIÓN 2, FECHA3, MONTO2 (adjudicado), Fecha4 (fecha de adjudicación) y ESTADO.
  - En la hoja VISITAS TECNICAS: FECHA, GERENCIA, RESPONSABLE y SERVICIO.
  - Las metas salen de la celda «META MENSUAL», con los 12 meses debajo.
- **Si falta una columna**, ese dato queda vacío y la pantalla lo avisa antes de guardar.
- **Antes de guardar** se muestran los avisos del Excel junto con la comparación. El servidor vuelve a leer el archivo y a comparar; no confía en lo que mostró el navegador.
- **Gerencias escritas de otra forma:** «Sulfuros» se guarda como **«Planta Sulfuros»** (Victor, 2026-11-03), tanto desde el Excel como desde la app.
- **Montos escritos como texto** (por ejemplo «.2467642.43» o «1579969.97»): se leen como número y se avisan. En el Excel original esos montos **no entraban en las sumas**. Con el Excel del 2026-11-03:

  | | El Excel mostraba | Real |
  |---|---|---|
  | Enviado | 10.54 millones | 13.01 millones |
  | Adjudicado | 1.97 millones | 3.77 millones |

- **«Agregados»** venía en la columna ESTADO, pero es otra línea de negocio: la venta de agregados. Se guarda como **tipo** (Servicio o Agregados). Un presupuesto de agregados con monto adjudicado queda Aprobado; sin monto adjudicado queda sin estado.
- **Estados:** En revisión, Aprobado, Desestimado y **Sin respuesta** (agregado por Victor el 2026-11-03). Un estado que no se reconoce queda vacío y se avisa.
- **Nivel de respuesta:** se usa el que trae el Excel, incluido «Lento». Si falta, se calcula con la regla del Excel:
  - 1 día: Inmediato;
  - hasta 4 días: Óptimo;
  - más: Dependiente-terceros.

## Registrar y corregir en la app

Los que llenan pueden trabajar sin el Excel:

- **Presupuestos** (pestaña Presupuestos): «Nuevo presupuesto», el lápiz para corregir y la papelera para borrar (pide confirmar en la misma fila).
  - Solo la descripción es obligatoria.
  - Sin N° de control, se le da el siguiente.
  - El N° de control no se puede repetir.
  - Los días de respuesta se calculan con las fechas de solicitud y de envío. El nivel de respuesta se calcula con la regla de arriba, salvo que se elija uno.
  - La fecha de envío no puede ser anterior a la de solicitud; los montos no pueden ser negativos.
- **Visitas técnicas** (pestaña Visitas técnicas): «Nueva visita», corregir y borrar. Fecha y servicio son obligatorios. Se puede elegir el presupuesto que salió de la visita.
- En las tablas, cada fila muestra una marca **«app»** si se registró en la app, o **«corregido»** si se corrigió algún dato. Esos datos son los que la próxima carga del Excel avisa como choque.

## Moneda y tipo de cambio

Los montos pueden estar en **soles o en dólares** (Victor, 2026-11-03):

- Al cargar se elige la moneda del Excel. Si el Excel trae una columna MONEDA, manda esa.
- Cada fila guarda la **venta SUNAT del día en que entra al sistema** (por el Excel o a mano), el mismo visor «Dólar SUNAT» del Dashboard. Al actualizar una fila se conserva el tipo de cambio que ya tenía.
- El dashboard se ve en **S/ o en US$** con un botón, convirtiendo cada fila con su tipo de cambio guardado.
- Sin tipo de cambio del día no se guardan montos en soles: la carga avisa y se reintenta.

## El dashboard

Se calcula solo desde las fechas, sin filtros a mano. Esto corrige lo que el Excel hacía manualmente:
- tablas filtradas en un solo mes;
- ventas mensuales copiadas a mano;
- una curva acumulada con un error de fórmula en julio, que la hacía bajar.

**Filtros:**
- año;
- mes, o el año completo; al abrir sale el último mes con presupuestos enviados;
- tipo: todos, servicios o agregados;
- moneda.

**Cómo se reparte cada monto en el tiempo:**
- **Enviado:** por la fecha de envío.
- **Adjudicado:** por la fecha de adjudicación; si falta, por la de envío.

**Indicadores:**

| Indicador | Qué mide |
|---|---|
| Enviado | Monto y cantidad de presupuestos enviados en el periodo |
| Adjudicado | Monto y cantidad adjudicados en el periodo |
| Meta | Meta del periodo y cuánto se cumplió |
| Tasa de cierre | Ganados entre (ganados + desestimados + sin respuesta), por cantidad, de lo enviado en el periodo |
| Conversión en monto | Monto adjudicado entre monto enviado, solo de esos presupuestos ya cerrados |
| En revisión | Monto y cantidad esperando respuesta |
| Tiempo de respuesta | Promedio de días entre la solicitud y el envío |
| Visitas técnicas | Cantidad de visitas en el periodo |

La conversión del Excel («adjudicado del mes entre enviado del mes») comparaba presupuestos distintos; por eso se reemplazó por la tasa de cierre y la conversión en monto.

**Gráficas:**
- Enviado y adjudicado por mes, con la meta.
- Curva acumulada del adjudicado contra la meta acumulada.
- Por gerencia, en monto.
- Por responsable, en cantidad de enviados y adjudicados.
- Estado de lo enviado.
- Nivel de respuesta.
- **Visitas técnicas:** por mes, por gerencia y por responsable. El Excel solo mostraba un conteo por gerencia de un mes.

**Metas mensuales:** se ven en la pantalla y las editan los tres roles que llenan. Pueden estar en S/ o en US$.

## PDF

«PDF vertical» y «PDF horizontal» descargan el dashboard en una hoja A4 con los mismos filtros de la pantalla: tarjetas, gráficas y visitas, acomodadas según la orientación. El fondo es claro, para imprimir.

## Datos

`db/127_costos_status_servicios.sql`, sin lectura por RLS; el servidor lee después de validar el rol:
- `costos_presupuestos` y `costos_visitas_tecnicas`, con `origen` (excel o app) y `campos_editados` (los datos corregidos en la app, para avisar choques); la visita tiene un vínculo opcional a su presupuesto;
- `costos_metas_mensuales`, una fila por año y mes, con su `origen`;
- la función `costos_aplicar_carga`, que solo usa el servidor: aplica en una transacción lo confirmado de la comparación.

**Rutas:**
- `POST /api/costos/status-servicios/cargar`: el Excel, en dos pasos (`modo=comparar` y `modo=aplicar`).
- `POST /api/costos/status-servicios/presupuestos`, `PATCH` y `DELETE …/presupuestos/[id]`: registro a mano.
- `POST /api/costos/status-servicios/visitas`, `PATCH` y `DELETE …/visitas/[id]`: registro a mano.
- `PUT /api/costos/status-servicios/metas`: las metas.
- `GET /api/costos/status-servicios/pdf`: el PDF.

## Pendiente

- Medir cuántas visitas terminan en presupuesto y cuántas en adjudicación: el vínculo ya se registra; falta el indicador.
- Ligar un presupuesto a su servicio de la app.
- Confirmar con Victor si la gerencia «Logista» del Excel es «Logística».
