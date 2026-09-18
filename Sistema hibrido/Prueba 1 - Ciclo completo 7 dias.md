# Prueba 1 — Ciclo completo de una semana (sin RDT, con RTDs)

Objetivo: probar el sistema de punta a punta con datos inventados, para
confirmar si el flujo `DP → PR → CS → Curva S / OT` está bien armado o
tiene algún quiebre — no es un ejercicio decorativo, es una prueba de
integridad del sistema. Este documento es la plantilla de cómo se
desglosa una prueba; las siguientes pruebas deberían seguir esta misma
estructura de secciones.

## 0. Decisión que falta confirmar con Victor

**¿La prueba se hace en hojas nuevas y separadas, o sobre las hojas reales
(`DP`/`PR`/`CS`/`CURVA S`/`OT`) del proyecto HDPE?**

`CD` y `APU` son de otro proyecto ("CASA HABITACION", numeración WBS
1.1/1.2/2.1...) — no tienen ninguna partida en común con el proyecto real
que ya vive en `DP`/`PR`/`CS` (COPREFA, WBS 00.01/01.01...). Mezclar los
datos de prueba en las mismas hojas del proyecto real destruiría el
trabajo ya hecho y validado esta sesión (línea base, fórmulas, hallazgos).

**Propuesta (pendiente de tu confirmación):** crear hojas nuevas con
sufijo `_PRUEBA`: `DP_PRUEBA`, `PR_PRUEBA`, `RTDs`, `CS_PRUEBA`,
`CURVA S_PRUEBA`, `OT_PRUEBA`. `CD` y `APU` no se tocan (ya son la fuente).
Así el proyecto HDPE real queda intacto y la prueba queda aislada,
revisable y descartable.

## 1. Parámetros de la prueba

| Parámetro | Valor |
|---|---|
| Ventana de medición | 7 días corridos |
| Fecha de corte | día 7 |
| Granularidad `CURVA S_PRUEBA` | diaria (7 columnas de fecha, no mensual) |
| Granularidad `OT_PRUEBA` | semanal (1 solo corte, al día 7) |
| Proyecto fuente | `CD` + `APU` ("CASA HABITACION") |
| Meta de cierre | IP final cercano a 0.9 |
| Costo de materiales | 5 requerimientos (RQ) de logística durante la semana |

## 2. Paso 1 — `DP_PRUEBA` ← `CD` + `APU`

- De `CD`: `Item` → `WBS`, `Partida`, `Unidad` → `Unid.`, `Metrado`, `CU` →
  columna auxiliar (no es parte de `DP`, `DP` no tiene precio — igual que
  en el proyecto real).
- De `APU`: por cada partida, el `Rendimiento` (`Cuadrilla/Rendimiento` de
  la cabecera de cada análisis) → columna `Rendimiento` de `DP_PRUEBA`.
- Filtrar: igual que en el proyecto real, sólo interesan para la prueba
  las partidas que **tienen mano de obra** (Rendimiento > 0 en su APU) —
  las partidas 100% material/subcontrato no llegan a `PR_PRUEBA` (mismo
  criterio ya usado con las 01.xx del proyecto real).

## 3. Paso 2 — `PR_PRUEBA` ← `DP_PRUEBA`

Mismo patrón que el `PR` real: por cada partida con HH, una fila con
fórmula `=DP_PRUEBA!...` para WBS/Partida/Rendimiento/Unid./Metrado, y
`HH Contractual = Rendimiento × Metrado`. La columna **`Metrado Ejecutado
Acumulado` (columna H, "la celda verde") se deja vacía/en 0** — es la que
llena `RTDs` en el paso siguiente.

## 4. Paso 3 — `RTDs` (hoja nueva, PRIMERO que todo lo demás)

Es el registro diario — a diferencia del `RDT` original (una sola
actividad por reporte), acá va **un reporte por día**, 7 filas mínimo
(uno por día 1 a 7), con estos campos (para saber exactamente qué celdas
se están usando):

| Campo | Fuente / uso |
|---|---|
| Fecha | día 1 al día 7 |
| WBS / código de partida | igual que en el RDT real, se conecta a `PR_PRUEBA` por WBS |
| Metrado ejecutado (del día) | dato inventado, positivo, ≤ metrado restante |
| CNC (si hubo) | opcional, para probar que ese campo también se usa |
| Turno / especialidad | opcional, copiar estructura del RDT real si aplica |

**Regla clave (la pediste explícita):** `RTDs` no reemplaza el dato en
`PR_PRUEBA!H`, lo **acumula**: el metrado ejecutado acumulado de una
partida en `PR_PRUEBA!H` = suma de todas las filas de `RTDs` con ese WBS,
desde el día 1 hasta el día de corte. Esto es exactamente la "agregación
RDT→WBS" que quedó pendiente en la sección 6 del documento de flujo — esta
prueba es la primera vez que se implementa, aunque sea a mano.

## 5. Paso 4 — `CS_PRUEBA` ← `PR_PRUEBA` + `3WLA`

Igual estructura que la `CS` real (3 grupos: línea base / acumulado real /
derivados). Dos datos que hoy son `"Pendiente"` en la `CS` real, en esta
prueba SÍ se llenan (inventados, a propósito, para poder cerrar el
ciclo):

- **Metrado Planificado Acumulado**: se inventa un cronograma valorizado
  simple (ej. metrado contractual repartido linealmente en 7 días) — esto
  habilita PV/SPI/EAC/VAC, que en el proyecto real siguen en "Pendiente"
  por falta de esta fuente.
- **Costo Real Acumulado**: se llena con la suma de los 5 RQ de
  logística (ver paso 6), no inventado aparte — tiene que salir de ahí
  para que la prueba sea honesta.

## 6. Paso 5 — Costos de materiales (logística) → 5 RQ

Logística reporta, durante la semana, **5 requerimientos**, cada uno con
su costo. El costo de cada RQ se calcula en función del avance del
metrado ejecutado en `RTDs` hasta ese punto (no un monto arbitrario) —
así el costo real acumulado queda atado al avance real, no a un número
suelto. Se registran en `PR_PRUEBA` como texto/nota por partida:

```
RQ N° 00001   $ xxxxx
RQ N° 00002   $ xxxxx
RQ N° 00003   $ xxxxx
RQ N° 00004   $ xxxxx
RQ N° 00005   $ xxxxx
```

**Criterio de cierre de la prueba:** ajustar el metrado diario en `RTDs` y
el costo de los 5 RQ hasta que, al día 7, el `IP` de `CS_PRUEBA` (HH
Ganadas / HH Reales Acumuladas) dé **cercano a 0.9** — ese es el
resultado que confirma que la cadena completa (RTDs → PR → CS) está bien
conectada de punta a punta.

## 7. Paso 6 — `CURVA S_PRUEBA` y `OT_PRUEBA` ← `CS_PRUEBA`

- `CURVA S_PRUEBA`: 7 columnas de fecha (una por día), filas PV/PV
  Periodo/EV/EV Periodo/AC/AC Periodo alimentadas desde los totales
  diarios de `CS_PRUEBA` (requiere que `CS_PRUEBA` tenga un corte por día,
  no solo el corte final — ver nota abajo).
- `OT_PRUEBA`: un solo corte semanal (día 7), tabla "Control del
  Servicio" con Metrado/HH/% Avance Físico/IP tomados del total de
  `CS_PRUEBA` en la fecha de corte.

**Resuelto por Victor (2026-08-18):** `CS` guarda solo el **acumulado a la
fecha de corte** — es una foto, no una serie. La que guarda el
**desagregado día a día** es `RTDs`. Por eso `CURVA S_PRUEBA` (que
necesita 7 columnas diarias) se alimenta directo de `RTDs` (sumando por
día, por partida, hasta cada fecha), no de fotos repetidas de `CS_PRUEBA`.
`CS_PRUEBA` sigue siendo una sola foto al día 7, usada para `OT_PRUEBA`
(que es un corte semanal, no diario) y como control final (el IP≈0.9).

## 7b. Aclarado por Victor (2026-08-18) — 3WLA sí entra en Prueba 1, y todo debe ser formula

- **`3WLA_PRUEBA` sí se construye en Prueba 1** (no se deja todo para
  Prueba 2). Prueba 2 sigue siendo solo la parte de **continuidad**: correr
  2-3 semanas encadenadas y ver que el lookahead recalcula la ventana hacia
  adelante. Pero una sola semana de `RTDs` ya trae los ingredientes para
  que `3WLA_PRUEBA` calcule bien sus columnas (Metrado/HH/IP) esa semana,
  así que se conecta ahora.
- **Regla no negociable para toda la prueba:** las hojas se conectan entre
  sí por **fórmula** (`SUMIFS`, referencias de celda), nunca pegando un
  número que yo calculé aparte. Si `PR_PRUEBA!H` necesita el acumulado de
  `RTDs`, es un `SUMIFS(RTDs...)`, no un valor tecleado. Si `3WLA_PRUEBA`
  necesita el mismo dato, es la misma fórmula o una referencia a
  `PR_PRUEBA`, nunca un número aparte. Esto es lo que la prueba está
  midiendo: si la cadena de fórmulas de verdad conecta.

## 7c. Resultado — EJECUTADA 2026-08-18

Construida completa en `Trazabilidad.xlsx`: `DP_PRUEBA`, `RTDs`, `PR_PRUEBA`
(con su tabla de 5 RQ de logística), `CS_PRUEBA`, `3WLA_PRUEBA`,
`CURVA S_PRUEBA`, `OT_PRUEBA`. Partidas usadas: `1.2` (CARTEL), `1.3`
(LIMPIEZA MANUAL DE TERRENO), `3.2` (NIVELACIÓN) — las únicas 3 de
`CD`/`APU` elegidas para mantener la prueba manejable, de las 33 que sí
tienen mano de obra real en su APU. Semana: 2026-08-10 a 2026-08-16.

**Todo conectado por fórmula, cero valores pegados a mano fuera de
`RTDs` (el dato de campo) y la tabla de 5 RQ (el dato de logística) — que
son las dos únicas fuentes primarias reales de esta prueba:**

- `PR_PRUEBA!H` (Metrado Ejecutado Acumulado) = `SUMIFS(RTDs...)` por WBS
  hasta la fecha de corte.
- `PR_PRUEBA!K` (Costo Real Acumulado) = `SUMIFS` de la tabla de 5 RQ por
  WBS.
- `CS_PRUEBA` = fórmulas `<- PR_PRUEBA` + `SUMIFS(RTDs...)` propio para HH
  Reales Acumuladas.
- `3WLA_PRUEBA` = fórmulas `<- PR_PRUEBA` + `SUMIFS(RTDs...)` propio
  (independiente de `CS_PRUEBA`, igual que en el diseño real).
- `CURVA S_PRUEBA` = `SUMIFS(RTDs...)` y `SUMIFS` de la tabla de RQ,
  filtrando por rango de fecha (día a día), acumulando fila por fila.
- `OT_PRUEBA` = fórmulas `<- CS_PRUEBA` (corte único, semanal).

**Resultado al día 7 (100% ejecutado en las 3 partidas):**

| Métrica | `CS_PRUEBA` | `3WLA_PRUEBA` | `OT_PRUEBA` | `CURVA S_PRUEBA` (día 7) |
|---|---|---|---|---|
| EV | 4717.06 | — | — | 4717.06 |
| AC | 4902.60 | — | — | 4902.60 |
| % Avance Físico | 100% | — | 100% | — |
| CPI | 0.9622 | — | — | — |
| **IP** | **0.8998** | **0.8998** | **0.8998** | — |

Las 4 hojas coinciden exactamente porque leen la misma fuente (`RTDs` +
`PR_PRUEBA`) por fórmula — si alguna hubiera dado un número distinto,
sería evidencia de una conexión rota. No fue el caso: el sistema pasó la
prueba.

**Gotcha técnico nuevo (para futuras pruebas con fecha vía COM):** al
escribir un `datetime.datetime` de Python en una celda vía
`win32com`, Excel lo guarda con un desfase horario (en este caso, +5h —
`2026-08-10 05:00` en vez de `2026-08-10 00:00`). Un `SUMIFS` con
igualdad exacta contra `DATE(a,m,d)` (medianoche exacta) **no matchea** y
da `0` silenciosamente, sin error. Se detectó porque `EV`/`AC` de
`CURVA S_PRUEBA` dieron `0.0` en la primera pasada. Arreglo: usar rango
(`">="&DATE(...)` y `"<"&DATE(...)+1 día`) en vez de igualdad exacta en
cualquier `SUMIFS`/`COUNTIFS` por fecha cuando las fechas vienen de una
celda escrita por COM.

## 8. Qué confirma esta prueba (y qué no)

Si el ciclo cierra con IP≈0.9 sin necesidad de tocar ninguna fórmula de
`CS`/`3WLA`/`PR` fuera de lo ya arreglado, confirma que el diseño del
sistema es correcto y lo único que faltaba era la implementación de la
agregación RDT→WBS (ya lo sabíamos, ver sección 6 de
`Flujo de trabajo - Control de Proyectos.md`). Si el ciclo NO cierra o
aparece un valor imposible, es evidencia de un quiebre real en el diseño,
no solo un hueco de datos — y hay que pararse ahí antes de seguir con más
pruebas.

## 9. Plantilla para pruebas futuras

Toda prueba siguiente debería declarar, como mínimo, estas mismas 9
secciones: decisión de aislamiento (hojas nuevas vs. reales), parámetros
de ventana/corte, y un paso por cada eslabón de la cadena que se está
probando, terminando siempre en un criterio de cierre numérico
verificable (como el IP≈0.9 acá) — no basta con "que no dé error", tiene
que dar un número esperado.
