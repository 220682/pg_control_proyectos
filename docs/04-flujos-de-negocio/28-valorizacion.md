# 28 — Valorización
> Lee si: la tarea toca la pantalla «Valorización» del grupo Costos: los rangos de fecha de cada valorización, de dónde sale el metrado (RDT, transversal o subcontrato), suma alzada o precios unitarios, o los gastos generales, la utilidad y el combustible.

Origen: pedido de Victor del 2026-11-03, con su PDF de ejemplo `Valorizacion_Final_Cierre_PROMCOSER_AESA_CONTRACTUAL.pdf` (formato de valorización de PROMCOSER). Quién puede: tabla 1 del [flujo 14](14-accesos-y-restricciones.md), nota 26. **Estado (2026-11-04): programada; falta aplicar `db/128_valorizaciones.sql`. Hasta entonces la pantalla muestra el presupuesto base y no deja agregar valorizaciones.**

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
| Pie | Costo directo, gastos generales, combustible, utilidad, total sin IGV, IGV 18 % y total con IGV |

## Valorizaciones

- «Agregar valorización» pide nombre (p. ej. «Julio»), **desde** y **hasta** (fecha de corte) con calendario. El «desde» sugerido es el día siguiente al corte anterior.
- Las valorizaciones son **consecutivas y sin traslape**: el servidor rechaza un rango que se cruza con otra. Se pueden editar y quitar. Si se quita una, su metrado queda en «Por valorizar».
- Un RDT con fecha después del corte pasa solo a la valorización siguiente.

## De dónde sale el metrado (columna Fuente)

| Fuente | Regla |
|---|---|
| RDT | Metrado ejecutado de los RDT **validados**, actividades D, por el vínculo oficial `rdt_actividad_partidas` (lo mismo que el PR y la Curva S) |
| Transversal | Partidas transversales del Plan Maestro **aprobado**: acumulado = metrado × p, con p = avance del resto del servicio al corte (declarado ÷ base, regla de `db/112`). No se cambia desde aquí |
| Subc. % | Partida marcada «por subcontrato»: en cada valorización se escribe el % del contrato |
| Subc. US$ | Partida marcada «por subcontrato»: en cada valorización se escribe el monto |

## Tipo de valorización (por servicio)

- **Suma alzada:** tope de 100 % por partida. Lo que pasa va a «Excedente» y no entra al acumulado ni al saldo (regla de cierre de Victor del 2026-10-16).
- **Precios unitarios:** sin tope. El metrado puede pasar o no llegar al contractual; el saldo puede quedar negativo.

## Gastos generales, utilidad y combustible

Cada uno se fija por servicio en **porcentaje** (sobre el costo directo de cada columna) o en **monto**. En monto, el del presupuesto base va en la configuración y el de cada valorización se escribe al agregarla o editarla.

## Datos

`db/128_valorizaciones.sql` crea las tablas siguientes. Ninguna se lee por RLS: solo el servidor las lee y escribe, después de validar el rol y el alcance.

| Tabla | Qué guarda |
|---|---|
| `proyecto_valorizacion_config` | Tipo de valorización, y GG, utilidad y combustible con su modo y su valor |
| `proyecto_valorizaciones` | Nombre, desde, hasta y los montos de los conceptos en modo monto |
| `proyecto_valorizacion_partida_manual` | Partidas por subcontrato y su modo (% o monto) |
| `proyecto_valorizacion_manual_valores` | % o monto escrito para cada valorización y partida |

Código: `src/lib/valorizacion/` (`calcular.ts`, `validar.ts`, `cargar.ts`) y `src/components/valorizacion/PanelValorizacion.tsx`.
