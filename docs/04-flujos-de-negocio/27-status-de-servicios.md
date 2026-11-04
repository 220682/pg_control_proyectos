# 27 — Status de servicios (reporte mensual de Costos)
> Lee si: la tarea toca el chip «Status de servicios» del grupo Costos, el reporte mensual de presupuestos enviados y adjudicados, las visitas técnicas, las metas mensuales de venta, la carga del Excel «DASHBOARD - REPORTE MENSUAL» de Costos, su dashboard o su PDF vertical u horizontal.

Origen: pedido de Victor del 2026-11-03 («crear algo para el apartado de Costos» con el Excel de Costos que tiene base de datos, visitas técnicas y dashboard). Quién puede cada acción: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md), nota ²⁵. **Estado (2026-11-03): publicada (app `abafd28`); falta aplicar `db/127_costos_status_servicios.sql`.**

## Qué es

Una pantalla de la empresa, **no de un servicio** (`/costos/status-servicios`, chip «Status de servicios» del grupo Costos; Victor pidió mantener ese nombre). Lleva a la app el Excel con que Costos controla sus **presupuestos**: los que envía al cliente, sus revisiones, los que se adjudican, y las **visitas técnicas**. Tiene tres pestañas:

- **Dashboard:** indicadores y gráficas del periodo elegido.
- **Presupuestos:** la tabla completa, con scroll horizontal y buscador.
- **Visitas técnicas:** la lista de visitas.

Un presupuesto **no necesita** estar ligado a un servicio de la app (Victor, 2026-11-03): muchos nunca llegan a ser servicio. La base guarda el vínculo como opcional (`proyecto_id`); la pantalla todavía no lo pide.

## Quién lo llena y quién lo ve

- **Llenan** (cargar el Excel y editar las metas): **jefe de costos, supervisor de costos y, por ahora, el administrador**.
- **Ven** el dashboard y las tablas, y **descargan el PDF:** esos tres más el **jefe de proyectos** y el **jefe de oficina técnica**. Son los 5 roles con datos económicos (regla 2 de la tabla 1 del flujo 14).
- **Los demás roles** ven el chip **deshabilitado**, como siempre. El servidor responde 403 también por URL directa.

## Cargar el Excel

Costos sigue llevando su Excel y lo **carga cuando quiere actualizar** (por ejemplo, cada semana). Cada carga **reemplaza** lo que había en el sistema por lo que trae el archivo, en una sola transacción. Las metas solo se reemplazan si el Excel las trae.

- **Se respetan las columnas:** cada dato se busca por el **nombre de su columna**, no por su posición:
  - En la hoja de presupuestos: No CONTROL, RESPONSABLE, CODIGO PS, GERENCIA, DESCRIPCION, FECHA DE SOLICITUD, MONTO, FECHA DE ENVIO, TR / DIAS, NIVEL DE RESPUESTA, REVISIÓN 1, FECHA2, REVISIÓN 2, FECHA3, MONTO2 (adjudicado), Fecha4 (fecha de adjudicación) y ESTADO.
  - En la hoja VISITAS TECNICAS: FECHA, GERENCIA, RESPONSABLE y SERVICIO.
  - Las metas salen de la celda «META MENSUAL», con los 12 meses debajo.
- **Si falta una columna**, ese dato queda vacío y la pantalla lo avisa antes de guardar.
- **Antes de guardar** se muestra cuántos presupuestos, visitas y metas trae el Excel, junto con los avisos. El servidor vuelve a leer el archivo; no confía en lo que mostró el navegador.
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

## Moneda y tipo de cambio

Los montos pueden estar en **soles o en dólares** (Victor, 2026-11-03):

- Al cargar se elige la moneda del Excel. Si el Excel trae una columna MONEDA, manda esa.
- Cada fila guarda la **venta SUNAT del día de carga**, el mismo visor «Dólar SUNAT» del Dashboard.
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
- `costos_presupuestos`;
- `costos_visitas_tecnicas`, con un vínculo opcional a su presupuesto;
- `costos_metas_mensuales`, una fila por año y mes;
- la función `costos_reemplazar_reporte`, que solo usa el servidor.

**Rutas:**
- `POST /api/costos/status-servicios/cargar`: el Excel.
- `PUT /api/costos/status-servicios/metas`: las metas.
- `GET /api/costos/status-servicios/pdf`: el PDF.

## Pendiente

- Registrar o corregir un presupuesto o una visita **desde la app**, sin pasar por el Excel.
- Ligar una visita a su presupuesto, para medir cuántas visitas terminan en presupuesto y cuántas en adjudicación.
- Ligar un presupuesto a su servicio de la app.
- Unificar gerencias escritas de dos formas en el Excel (por ejemplo «Sulfuros» y «Planta Sulfuros»): hoy salen como dos gerencias distintas.
