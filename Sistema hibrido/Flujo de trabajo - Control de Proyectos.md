# Flujo de trabajo — Control de Proyectos (app web)

Este es el documento "cerebro" del sistema: define el flujo completo entre
formatos y el **diccionario de datos canónico** que todos deben respetar.
Sin esto, cada formato termina llamando distinto a la misma métrica y el
sistema deja de ser trazable — que es exactamente el problema que este
documento existe para cerrar.

## 1. Los dos archivos de gobierno

- **`Indicadores EVM - Teoria y Ejemplo.xlsx`** — la base. Define cómo
  funciona el plan de control de calidad: qué métricas existen, cómo se
  calculan (BAC, PV, EV, AC, CPI, SPI, % Avance Físico, HH Ganadas, IP) y
  **cómo se llama cada columna**. Todo nombre de columna en cualquier otro
  formato del sistema debe poder trazarse hasta un nombre de esta hoja.
- **`Consolidado de servicios.xlsx`** — la auditoría. Matriz de trazabilidad
  que compara el nombre canónico (Indicadores) contra el nombre real en cada
  formato y marca dónde se rompe la coherencia. Se actualiza cada vez que se
  revisa un formato nuevo (ver sección 4).

## 2. Pipeline general del sistema

```
Presupuesto (ej. "Presupuesto HDPE", puede ser cualquiera)
        │  se sube al sistema
        ▼
      DP  (Datos de Proyecto — línea base)
        │  ya en producción, plantilla existe, se está mejorando
        │  (parser flexible de columnas — ver spec-hoja-dp.md)
        ▼
      PR  (Project Report — avance real)
        │  copia toda la línea base de DP por fórmula
        │  y agrega el avance real acumulado
        ▲
      RDT (Reporte Diario de Trabajo — dato de campo)
        alimenta el avance de PR (hoy: formato existe, sin datos reales)

  (en paralelo, no dependen de DP/PR para existir)

      OT  (Orden de Trabajo — apertura y cierre del servicio)
        plantilla ya existe (control_de_proyectos.txt sección 8)

      3WLA (Three Week Look Ahead — programación semanal, nivel portafolio)
        se alimenta de PR, NO de DP directamente
        (DP no tiene columnas de avance por diseño — ver spec-hoja-3wla.md §1)
```

**Paso 1 (lo que se está trabajando ahora):** estandarizar los encabezados
de columnas de DP, PR, RDT, OT y 3WLA usando como base los de Indicadores.

## 3. Diccionario canónico de columnas

**Actualizado 2026-08-18: los encabezados de DP/PR/RDT/OT/3WLA ya se
renombraron** para calzar con la forma abreviada de la hoja `0. Diccionario`
de Indicadores (ver punto 7 de la sección 5). La tabla de abajo refleja el
estado YA renombrado.

| Concepto | Nombre canónico (Indicadores, abreviado) | DP | PR | RDT | OT | 3WLA |
|---|---|---|---|---|---|---|
| Identificador de partida | `WBS` | `WBS` | `WBS` | `WBS` | `WBS` | `Activity ID` (WBS) |
| Nombre de la partida | `Partida` | `Partida` | `Partida` | `Descripción de la Actividad` | `Descripción de partida` | `Descripción de la actividad` |
| Unidad | `Unid.` | `Unid.` | `Unid.` | `Unid.` | `Unid.` | — |
| Metrado contractual | `Metrado` | `Metrado` | `Metrado` | — | `Metrado` | `Metrado` |
| Metrado programado/planificado (por reporte, no acumulado) | `Metrado Planificado Acumulado` (concepto acumulado) | — | — | `Metrado Programado` (dato diario, ver 4.2) | — | — |
| Metrado ejecutado (por reporte / acumulado) | `Metrado Ejecutado Acumulado` | — | `Metrado Ejecutado Acumulado` | `Metrado Ejecutado` (dato diario) | `Metrado` (fila 34, semanal) | `Metrado Ejecutado Acumulado` |
| Precio unitario | `Precio Unit.` | — | `Precio Unit.` | — | `Precio Unit.` | — |
| Costo real acumulado | `Costo Real Acumulado` | — | — (no hay consolidado por partida) | — | `Costo acumulado` (por recurso) | — |
| Rendimiento (HH/Und) | `Rendimiento` | `Rendimiento` | `Rendimiento` | — | — | `Rendimiento` |
| HH contractual (por partida) | *(no está en Indicadores, término propio de PR/OT/3WLA/CS)* | — | `HH Contractual` | — | `HH Contractual` | `HH Contractual` |
| HH reales acumuladas | `HH Reales Acumuladas` | — | `hh acumulado` (por trabajador, no por partida) | `Total` (Tareo, por persona/día, sin WBS — ver 4.2) | — | `HH Reales Acumuladas` ⚠️ formula sigue mal, ver 4.3 |
| HH ganadas | `HH Ganadas` | — | `P. horas ganadas` | — | — | `HH Ganadas` |
| Valor Ganado (EV) | `EV` | — | `Valor Ganado (EV)` | — | — | — |
| % Avance Físico | `% Avance Fisico` | — | — | — | `% Avance Fisico` | `% Avance Fisico` (total) / `% Avance Fisico x Partida` (por fila) |
| BAC / AC / CPI / EAC | igual | — | — (parcial, por recurso) | — | `BAC` / `AC` / `CPI` / `EAC` (calculados) | — |
| IP (Índice de Productividad) | `IP` | — | — (no existe) | — | — | `IP` ⚠️ ver hallazgo 4.3 |

**`CURVA S`** es distinta a las demás: no tiene encabezados de columna, es
una tabla mensual donde **cada fila es una métrica** y cada columna es un
mes (para graficar la curva S clásica de PV/EV/AC en el tiempo). Renombrada
2026-08-18:

| Fila (rótulo) | Antes | Después | Nota |
|---|---|---|---|
| Planificado, del mes | `Valor Planificado (PV)` | `PV Periodo` | valor del mes, no acumulado |
| Planificado, acumulado | `Valor Planificado Acumulado` | `PV` | este SÍ es el `PV` del diccionario — en EVM, PV ya es por definición "a la fecha" |
| Ganado, del mes | `Valor ganado (EV)` | `EV Periodo` | valor del mes |
| Ganado, acumulado | `Valor ganado acumulado` | `EV` | corresponde al `EV` del diccionario |
| Costo real, del mes | `Costo Real (AC)` | `AC Periodo` | valor del mes |
| Costo real, acumulado | `Costo Real Acumulado` | `AC` | corresponde al `AC` del diccionario |

El diccionario define PV/EV/AC como el valor acumulado a la fecha (así es
como se usan en CS y en la fórmula de CPI/SPI) — por eso solo las filas
"...Acumulado" se renombraron al nombre canónico exacto; las filas de
periodo (mensuales) son un concepto que el diccionario no cubre, así que se
etiquetaron `<Métrica> Periodo` para que sigan siendo trazables por raíz de
palabra sin inventar una falsa equivalencia. `CURVA S` tiene 1 gráfico
(chart) incrustado — el rename se hizo por COM para no arriesgarlo.

Fuente de cada columna real: `Trazabilidad.xlsx` (hojas DP/PR/RDT/OT/3WLA/CS/CURVA S),
verificado leyendo cada hoja directamente vía COM, no de memoria. `PR`
(`hh acumulado`, `P. horas ganadas`) y el `Total` del Tareo de RDT quedaron
sin renombrar a propósito: no representan el mismo concepto acumulado por
partida que pide el diccionario (ver 4.2) y renombrarlos habría sido
incorrecto, no solo cosmético.

## 4. Hallazgos de trazabilidad

### 4.1 Simples (renombrar encabezado, no toca fórmulas) — RESUELTO 2026-08-18

- **Rendimiento (HH/Und)** tenía **cuatro** nombres distintos: `Rendimiento
  Estandar (HH/Und)` (Indicadores), `hh und part.` (DP), `Rend hh x part.`
  (PR), `Rend. HH x partida` (3WLA). Renombrado a `Rendimiento` en DP, PR y
  3WLA.
- **Metrado Ejecutado Acumulado** perdía la palabra "Ejecutado" en PR y
  3WLA (`Metrado acumulado`) — renombrado a `Metrado Ejecutado Acumulado`
  en ambos. En RDT (dato diario, no acumulado) se dejó `Metrado Ejecutado`
  sin la palabra "Acumulado", porque ahí de verdad no lo es (ver 4.2).
- **Precio Unitario**: unificado el nombre a `Precio Unit.` en DP, PR y OT
  (sin tocar la moneda de cada archivo, que es un tema aparte de la
  nomenclatura).
- **Nombre de la partida**: se dejó sin tocar — RDT y OT usan "Descripción
  de..." porque describen la actividad/partida con más detalle que un
  simple nombre corto; no es una inconsistencia de trazabilidad real.

Detalle completo del rename ejecutado: ver punto 7 de la sección 5.

### 4.2 Con hueco real de datos (no solo de nombre)

- **Costo Real Acumulado por partida**: ni PR ni OT lo arman a nivel de WBS
  (PR lo tiene por recurso — mano de obra/equipos/materiales — pero no
  consolidado por partida). Sin esto no se puede calcular AC ni CPI **por
  partida**, solo a nivel de proyecto completo.
- **HH reales por partida**: el Tareo de RDT registra horas por
  persona/día, no por WBS. Sin ese cruce, "HH Reales Acumuladas" nunca llega
  desglosada por partida ni a PR ni a 3WLA.

  **Aclarado por Victor (2026-08-18):** el vínculo RDT → WBS ya existe como
  campo (columna `WBS` en la hoja `2.0 REPORTE DE AVANCE` de RDT) — el
  operativo lo pone a mano o se digita al cargar el RDT. No es un campo
  nuevo que falte diseñar. Lo que falta es la parte de **agregación**: sumar
  las filas de RDT que comparten un mismo código WBS (a través de todas las
  semanas/días) hacia Costo Real Acumulado y HH Reales Acumuladas por
  partida en CS. Eso es implementación futura, no un hueco de diseño.
  Decisión de alcance explícita (ver sección 5): la hoja `CS` mapea **todos**
  los datos que el sistema va a necesitar aunque hoy no tengan de dónde
  salir (de ahí el `"Pendiente"` en vez de dejar la columna sin crear) — el
  orden es primero mapear el dato completo, después decidir de dónde e
  implementar cómo se llena.
- **IP no baja al PR**: Indicadores lo calcula, 3WLA lo replica (columna
  `P`), pero PR no tiene esa columna todavía.

### 4.3 Bug conceptual real (no es solo de nombre) — 3WLA columnas L/O/P

Verificado en `spec-hoja-3wla.md` §2: la columna `L` de 3WLA, llamada `HH
acumulado`, se calcula como `F * N` (`Metrado ejecutado acumulado ×
Rendimiento`) — pero esa es exactamente la fórmula de **`HH Ganadas`**, no
de **`HH Reales`**. La columna `O`, que sí se llama `HH ganadas`, usa la
misma fórmula `F * N`. Como ambas columnas son literalmente la misma
fórmula, `P` (`IP = O / L`) da **siempre 1.00**, sin importar el proyecto:
nunca puede reflejar productividad real, porque `HH Ganadas` y `HH Reales`
en este archivo son el mismo número por construcción.

`HH Reales` es, por definición (ver Indicadores), un dato **independiente**
que viene de campo (horas efectivamente trabajadas, del RDT) — no se puede
derivar de `Metrado × Rendimiento`, porque esa cuenta ya da `HH Ganadas`.
Mientras el RDT no aporte una columna real de horas trabajadas por partida
(ver 4.2), no hay forma de que 3WLA calcule un IP que signifique algo.

## 5. Estado actual (actualizado 2026-08-18)

El plan original de esta sección (renombrar encabezados en cada archivo) se
reemplazó por un enfoque distinto que Victor pidió antes de tocar nada:
primero construir el diccionario canónico y la tabla consolidada, recién
después decidir renombres. Ya implementado:

1. **`Indicadores EVM - Teoria y Ejemplo.xlsx`, hoja `0. Diccionario`**
   (nueva, primera hoja del libro): dos columnas — encabezado completo tal
   como queda en Indicadores, y su forma abreviada para usar en
   DP/PR/RDT/OT/3WLA/CS. Pensada explícitamente para que, cuando más
   adelante se creen tablas de base de datos a partir de estos formatos, no
   haya conflicto de nombres.
2. **Encabezados de Indicadores ya renombrados** (hojas `2. Datos
   Ficticios` y `3. Ejemplo - Calculo EVM`) según la nomenclatura que Victor
   definió — ej. `Monto contractual BAC ($/)`, `PV ($/) (metr.plan. x
   P.U.)`, `Rendimiento (HH/Und)`. `Metrado` se mantiene así (no
   `Metrado Contractual` como se proponía antes).
3. **`Trazabilidad.xlsx`** (antes `Consolidado proyecto.xlsx` — Victor lo
   renombró) tiene ahora una hoja **`CS` (Consolidado del Servicio)**: una
   sola tabla por proyecto con las 9 partidas que ya sigue PR (00.01,
   02.01-02.06, 03.01, 04.01), en tres grupos de columnas —
   **A. Línea base** (contractual, de DP) | **B. Acumulado real** (RDT →
   PR) | **C. Derivados** (EVM calculado: BAC/PV/EV/AC/CPI/SPI/%Avance
   Físico/HH Ganadas/IP/EAC/VAC) — con nomenclatura abreviada del
   diccionario.
4. **Decisión de Victor sobre `PR`**: ya no calcula EV ni HH Ganadas (las
   columnas correspondientes se borraron a propósito) — `PR` solo recoge el
   acumulado real que llega del RDT; **`CS` es la única hoja que calcula
   derivados**. `CS!EV` y `CS!HH Ganadas` se calculan ahí mismo
   (`Metrado Ejecutado × Precio Unit.` / `× Rendimiento`), no se leen de `PR`.
5. **Decisión de Victor sobre alcance de `CS`**: la hoja mapea **todos** los
   campos que el sistema va a necesitar, existan o no los datos todavía —
   por eso usa `"Pendiente"` (nunca `0` ni celda vacía) en vez de omitir la
   columna. Primero se mapea el dato completo; de dónde sale y cómo se
   implementa se resuelve después, uno por uno.
6. **Aclarado (hallazgo 4.2)**: el vínculo RDT → WBS no es un campo nuevo
   que falte diseñar — el RDT ya tiene columna `WBS` por fila de actividad,
   la pone a mano el operativo en campo. Lo pendiente es la agregación
   (sumar filas de RDT por WBS a través del tiempo) hacia `CS`, no el campo
   en sí.
7. **Encabezados de `DP`/`PR`/`RDT`/`OT`/`3WLA` renombrados en
   `Trazabilidad.xlsx`** siguiendo la forma abreviada del diccionario (24
   celdas, verificadas contra el valor real antes de escribir, una por
   una). Detalle en la sección 3. Se dejaron **sin tocar** a propósito los
   nombres que no representan el mismo concepto acumulado por partida que
   pide el diccionario (`hh acumulado` y `P. horas ganadas` en PR, `Total`
   del Tareo de RDT, `Metrado restante`/`HH restante` en PR/OT) — renombrarlos
   habría sido trazabilidad falsa, no real.

## 6. Pendientes que este documento NO resuelve todavía

- **Agregación RDT → CS por WBS**: sumar Costo Real y HH Reales de las
  filas de RDT que comparten un mismo código WBS (a través de las semanas)
  hacia `Costo Real Acumulado` y `HH Reales Acumuladas` en `CS` (ver
  hallazgo 4.2 y punto 6 de la sección 5). El campo de origen ya existe: lo
  que falta es dónde y cómo se acumula.
- Bug de `HH acumulado`/`HH Ganadas` en `3WLA` (hallazgo 4.3) — la fórmula
  sigue sin resolver (columna `L` sigue siendo `F*N`, igual que `O`). El
  header de `L` ahora dice `HH Reales Acumuladas` (renombrado en el punto 7
  de la sección 5) — el nombre ya es el correcto, pero la fórmula debajo
  sigue calculando `HH Ganadas`, no horas reales. El rename no oculta el
  bug, lo hace más visible: cuando se implemente el dato real de HH desde
  RDT (ver 4.2), esta columna necesita que le cambien la fórmula, no el
  nombre. Cuando eso pase, `3WLA` debería terminar leyendo el IP de `CS`
  en vez de recalcularlo con la fórmula duplicada.
- Fuente de cronograma valorizado (PV) — sigue pendiente, afecta a `CS`
  (columnas PV/SPI/EAC/VAC) igual que ya afectaba al Dashboard y a `3WLA`
  columnas Q/R/S (`spec-hoja-3wla.md` §3).
