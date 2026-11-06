# 28 — Valorización
> Lee si: la tarea toca la pantalla «Valorización» del grupo Costos: los rangos de fecha de cada valorización, de dónde sale el metrado (RDT, transversal o subcontrato), suma alzada o precios unitarios, o los gastos generales, la utilidad y los campos adicionales.

Origen: pedido de Victor del 2026-11-03, con su PDF de ejemplo `Valorizacion_Final_Cierre_PROMCOSER_AESA_CONTRACTUAL.pdf` (formato de valorización de PROMCOSER). Quién puede: tabla 1 del [flujo 14](14-accesos-y-restricciones.md), nota 26. **Estado (2026-11-04): db/128 y db/129 aplicadas; falta `db/131_valorizacion_fuente_por_defecto.sql`. Sin db/131 una partida de subcontrato por defecto no se puede volver a RDT (la marca no se guarda).**

## Qué es

Una pantalla por servicio (`/proyectos/{id}/valorizacion`, chip «Valorización» del grupo Costos) con la tabla del formato de valorización:

| Columna | Qué muestra |
|---|---|
| Ítem, descripción, unidad | Partidas del DP, con títulos (subpresupuesto) y subtítulos (paquete) y su subtotal |
| Fuente | RDT, Transversal, Subc. % o Subc. US$ (ver abajo) |
| Presupuesto base | Metrado contractual, P.U. y parcial (US$) |
| Una columna por valorización | Metrado y parcial del rango «desde–hasta»; la última lleva «(actual)» |
| Acumulado, saldo y % avance | Saldo = base − acumulado |
| Excedente | Solo en suma alzada y si hay: lo que pasa del 100 % (no se valoriza) |
| Por valorizar | Solo si hay: metrado de RDT con fecha fuera de toda valorización |
| Pie | Costo directo, gastos generales, campos adicionales (solo si se agregaron), utilidad, total sin IGV, IGV 18 % y total con IGV |

## Valorizaciones

- «Agregar valorización» pide nombre (p. ej. «Julio»), **desde** y **hasta** (fecha de corte) con calendario. El «desde» sugerido es el día siguiente al corte anterior.
- Las valorizaciones son **consecutivas y sin traslape**: el servidor rechaza un rango que se cruza con otra. Se pueden editar y quitar. Si se quita una, su metrado queda en «Por valorizar».
- Un RDT con fecha después del corte pasa solo a la valorización siguiente.
- Si hay RDT con fecha fuera de toda valorización, un aviso dice qué días son: su metrado queda en «Por valorizar» (caso PS-108: el RDT del 13-10 con la valorización desde el 14-10).
- El encabezado de la tabla queda fijo al bajar. La tabla usa todo el alto y el botón del asistente flota encima, como en Plan Maestro (`data-area-completa`).

## De dónde sale el metrado (columna Fuente)

| Fuente | Regla |
|---|---|
| RDT | Metrado ejecutado de los RDT **validados**, actividades D, por el vínculo oficial `rdt_actividad_partidas` (lo mismo que el Consolidado y la Curva S) |
| Transversal | Partidas transversales del Plan Maestro **aprobado**: acumulado = metrado × p, con p = avance del resto del servicio al corte (declarado ÷ base, regla de `db/112`). No se cambia desde aquí |
| Subc. % | Partida marcada «por subcontrato»: en cada valorización se escribe el % del contrato |
| Subc. US$ | Partida marcada «por subcontrato»: en cada valorización se escribe el monto |

**Por defecto:** una partida cuyo APU es subcontrato en 50 % o más de su costo entra como «Subc. %» sin marcarla (las transversales siguen como transversales). Lo que Victor elija en Fuente manda, también «RDT». El costo de subcontrato por partida se guarda al importar el DP (db/131); en los DP importados antes se lee del archivo de origen guardado.

En las dos de subcontrato la tabla muestra solo metrado y parcial US$, igual que una partida de RDT. El % o el monto se escribe en un desplegable de la celda US$ y no aparece en la valorización: solo sirve para sacar el metrado y el costo (pedido de Victor del 2026-11-04).

## Tipo de valorización (por servicio)

- **Suma alzada:** tope de 100 % por partida. Lo que pasa va a «Excedente» y no entra al acumulado ni al saldo (regla de cierre de Victor del 2026-10-16).
- **Precios unitarios:** sin tope. El metrado puede pasar o no llegar al contractual; el saldo puede quedar negativo.

## Gastos generales, utilidad y campos adicionales

Cada uno se fija por servicio en **porcentaje** (sobre el costo directo de cada columna; se guarda con hasta 6 decimales y se muestra con 2) o en **monto**. En monto, el del presupuesto base va en la configuración y el de cada valorización se escribe al agregarla o editarla.

**Por defecto, tal cual el presupuesto (Victor, 2026-11-05):** al importar el presupuesto, sus gastos generales y su utilidad quedan aquí como porcentaje, para que costo directo + gastos generales + utilidad den el monto del presupuesto en la columna contractual. Cada valorización los toma sola con ese porcentaje sobre su costo directo; no hay que calcular nada. Para cambiarlo en todas se edita la configuración. Para cambiarlo en **una sola** se escribe su monto al agregarla o editarla: ese monto manda solo en ella y, si se deja vacío, vuelve al porcentaje.

El combustible **no es fijo** (no siempre se da): se agrega como **campo adicional** con nombre libre (p. ej. «Combustible (reembolsable)»), hasta 10 por servicio. Un campo adicional solo aparece al pie si se agregó, entre GG y utilidad.

## Exportar

Botones «PDF» y «Excel» (quien ve la pantalla). Formato de la plantilla de Victor `Valorizacion_Final_Cierre_PROMCOSER_AESA_plantilla.xlsx` (hoja SDC01): título en banda azul, proyecto, cliente, contratista, tipo de contrato, fechas y periodo; encabezado de dos filas; títulos en celeste con letra roja; pie de costo directo a total con IGV; firmas «Elaborado por PROMCOSER», «Revisado por Supervisión» y «Aprobado por» el cliente. Todo redondeado a 2 decimales. El Excel trae además la columna «Observación» vacía. Ruta: `GET /api/proyectos/{id}/valorizaciones/exportar?formato=pdf|xlsx`.

## Datos

`db/128_valorizaciones.sql`, `db/129_valorizacion_tipo_y_campos_adicionales.sql` y `db/131_valorizacion_fuente_por_defecto.sql` crean y ajustan las tablas siguientes. Ninguna se lee por RLS: solo el servidor las lee y escribe, después de validar el rol y el alcance.

| Tabla | Qué guarda |
|---|---|
| `proyecto_valorizacion_config` | Tipo de valorización (columna de db/129), y GG y utilidad con su modo y su valor. Las columnas `combustible_*` de db/128 quedan sin uso |
| `proyecto_valorizaciones` | Nombre, desde, hasta y los montos de los conceptos en modo monto |
| `proyecto_valorizacion_partida_manual` | Fuente elegida por Victor: `rdt`, `porcentaje` o `monto` (`rdt` desde db/131) |
| `dp_partida_costos.costo_subcontrato` (db/131) | Costo de subcontrato del APU de cada partida: decide la fuente por defecto |
| `proyecto_valorizacion_manual_valores` | % o monto escrito para cada valorización y partida |
| `proyecto_valorizacion_conceptos` (db/129) | Campos adicionales del servicio: nombre, modo, valor base y orden |
| `proyecto_valorizacion_concepto_montos` (db/129) | Monto de cada campo adicional (modo monto) en cada valorización |

Código: `src/lib/valorizacion/` (`calcular.ts`, `validar.ts`, `cargar.ts`, `guardar.ts`, `fuente-defecto.ts`, `exportar.ts`) y `src/components/valorizacion/PanelValorizacion.tsx`.
