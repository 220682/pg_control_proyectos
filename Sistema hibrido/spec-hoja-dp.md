# Spec — Hoja `DP` (Datos de Proyecto)

Documenta cómo se construye la hoja `DP` de `Consolidado proyecto.xlsx`: de qué
archivos sale cada dato, qué fórmula lleva cada celda y por qué. Escrito
después de corregir errores reales de referencias movidas (2026-08-16), para
que sirva de base a un agente que genere esta hoja automáticamente en
proyectos futuros — ver pendiente en `memoria.md` (2026-08-15, "más adelante
quiere crear agentes...").

`DP` es la **línea base** del proyecto (día cero, antes de cualquier avance).
Todas sus celdas de avance quedan vacías a propósito; el avance real se
captura en la hoja `PR`, que lee su línea base desde aquí.

## 1. Fuentes

| Fuente | Qué aporta |
|---|---|
| `CD` (hoja de este mismo libro) | Código WBS, nombre de partida, unidad, metrado contractual y precio unitario ya resueltos — copia de un presupuesto `PRESUPUESTO` externo (`CD!D2:D4` conserva la fórmula `=[1]PRESUPUESTO!E12` sin resolver un enlace externo real; son valores congelados, no un link vivo). |
| `Presupuesto_HDPE_TieIn06-GCI_Promcoser.xlsx`, hoja `APU` | Análisis de precios unitarios: para cada partida, su rendimiento, y el desglose de mano de obra (rol + cuadrilla + HH/persona), equipos (HM) y materiales/subcontratos que la componen. |

`DP` no tiene fórmulas que lean directamente el archivo APU (es un libro
aparte) — los valores se copian ya calculados. Reconstruir `DP` para un
proyecto nuevo significa volver a correr este cálculo contra el nuevo APU,
no dejar una fórmula viva entre archivos.

### 1.1 Estructura de un bloque de partida en `APU`

Cada partida es un bloque de filas que empieza con una fila
`"<código> <nombre partida>"` en la columna A (p. ej. `"00.01 MOVILIZACION..."`)
y sigue con:

- Fila `Rendimiento: <N> <UND>/DIA` — cuántas unidades produce la cuadrilla
  en una jornada.
- Fila de encabezado `Insumo | Unidad | Cuadrilla | Cantidad | PU | Parcial`.
- Una fila por insumo:
  - `Unidad = 'HH'` → insumo de mano de obra. `Cuadrilla` = cuántas personas
    de ese rol trabajan a la vez; `Cantidad` = HH por persona por unidad de
    partida = `horas_jornada / rendimiento` (constante para toda la
    partida, igual en todas sus filas HH).
  - `Unidad = 'HM'` → insumo de equipo. Mismo patrón que HH pero sin
    columna `Cuadrilla` usada (se asume 1).
  - Sin `Unidad` en HH/HM → insumo de material.
- Filas de subtotal: `Mano de obra:`, `Equipo:`, `Materiales:` (columna G),
  con el monto en columna H.

**HH totales de una partida** (usado como `hh und part.` en `DP` B1) = suma
de `Cuadrilla × Cantidad` de todas sus filas `HH`. Verificado: partida
`00.01` → `(1×3.333) + (2×3.333) = 10`, igual al valor que ya tenía `DP!D10`.

**Horas por jornada**: en este proyecto es **10** para todas las partidas
(se despeja de `Cantidad = horas_jornada / rendimiento` con el rendimiento
de cada partida — da 10 de forma consistente en las 8 partidas con mano de
obra). Confirmar este número contra el APU de cada proyecto nuevo, no darlo
por constante entre proyectos.

## 2. Bloques de `DP` y de dónde sale cada uno

### A. Datos generales (filas 3-6)
Copia literal (no fórmula) de `CD!D2` (Proyecto), `CD!D4` (Cliente) y el
área del proyecto. Texto plano, se pega a mano al construir la hoja.

### B1. Partidas de Control — Work Package (filas 9-33)
Una fila por partida de `CD` (mismo orden y código WBS):

| Columna DP | Origen |
|---|---|
| B (WBS) | `CD` columna C (código) |
| C (Partida) | `CD` columna D (descripción) |
| D (hh und part.) | Suma de `Cuadrilla × Cantidad` en las filas HH del bloque de esa partida en `APU` (0 si la partida no tiene mano de obra, solo materiales) |
| E (Und.) | `CD` columna E |
| F (Metrado Contractual) | `CD` columna F |
| G (P.U. $) | `CD` columna G (ya es el costo unitario total de la partida, mano de obra + equipo + materiales, calculado por el APU) |

Fila `TOTAL` (33): `F33 = SUMPRODUCT(D10:D32, F10:F32)` → HH contractuales
totales del proyecto. `G33 = SUMPRODUCT(F10:F32, G10:G32)` → costo directo
contractual total del proyecto. **Ojo:** F33 es horas, G33 es dólares — no
confundirlas al enlazarlas desde otro bloque (era exactamente el bug
corregido el 2026-08-16, ver sección 4).

### B2. Cuadro Resumen (filas 36-43)
Costo directo contractual desglosado en 4 componentes (dólares) + 2 filas de
referencia en horas-hombre. El TOTAL (`D43`) suma **solo los 4 componentes
de costo**, nunca las filas de HH (mezclar dólares con horas no tiene
sentido, confirmado con Victor 2026-08-16).

| Fila | Concepto | Fórmula correcta |
|---|---|---|
| 37 | Costo mano de obra | `=G53` (TOTAL Costo Contractual de C1) |
| 38 | Costo equipos | `=G63` (TOTAL Costo Contractual de C2) |
| 39 | Costo materiales | `=E83` (TOTAL Costo Contractual de C3) |
| 40 | Costo subcontratos | `=E88` (TOTAL Costo Contractual de C4) |
| 41 | HH Contractual (Work Package) — referencia, no entra al TOTAL | `=F33` |
| 42 | HH Contractual (Mano de Obra) — referencia, no entra al TOTAL | `=E53` |
| 43 | TOTAL | `=SUM(D37:D40)` |

También en este bloque, columna E-G, va el sub-bloque **Duración estimada
del proyecto** (ver sección 3).

### C1-C4. Recursos — línea base (filas 45-88)
Cada tabla lista los insumos **únicos** que aparecen en cualquier partida del
proyecto (un rol de mano de obra, un tipo de equipo, un material o un
subcontrato puede repetirse en varias partidas — aquí aparece una sola vez,
con el total agregado).

- **C1 Mano de Obra (filas 47-53)** y **C2 Equipos (filas 57-61)**: por cada
  rol/equipo único, `HH ó HM Contractual = Σ (Cuadrilla × Cantidad × Metrado
  de la partida)` sumado sobre TODAS las partidas donde aparece ese insumo.
  Verificado con script contra el APU real: "Oficial Mecanico" aparece en 2
  partidas (00.01 y 02.05), su HH total agregado (92.955) coincide con
  `DP!E48` (92.95). `P.U. (costo-hora)` es la tarifa del insumo (constante
  entre partidas). `Costo Contractual = HH × P.U.` (fórmula por fila).
  - `C2` tiene una fila extra, **"Herramientas menores (%MO)"** (`G62`) —
    **corregido el 2026-08-16: sí sale del APU**, no es un recargo global
    inventado. En el APU, cada bloque de partida puede tener una línea
    `HERRAMIENTAS MANUALES` (`Unidad = '%MO'`) — **no todas las partidas la
    tienen** (en el proyecto real: solo 02.01-02.06 y 04.01, 7 de 15
    partidas) — cuyo costo unitario es `3% × costo de mano de obra de ESA
    partida` (`Cantidad × PU` donde `PU = costo MO unitario de la partida`,
    `Cantidad = 3`). El total que va en `DP!G62` es la suma, sobre todas las
    partidas que tienen esa línea, de `costo unitario de la línea × metrado
    de la partida` (`CD` columna F). Verificado con script contra el APU
    real: da `68.065`, que redondea al `68.07` que ya estaba puesto a mano
    — el valor previo era correcto, solo le faltaba la fórmula/metodología
    documentada detrás. Sigue incluido en `G63 = SUM(G57:G62)`.
- **C3 Materiales (filas 67-83)** y **C4 Subcontratos (filas 87-88)**: una
  fila por insumo único (los materiales no se repiten entre partidas en
  este proyecto), `Costo Contractual` = el monto `Parcial` del subtotal
  `Materiales:`/insumo tal como aparece en su bloque del APU.

## 3. Duración estimada del proyecto (filas 37-40, columna G)

Agregado el 2026-08-15, reconstruido el 2026-08-16 tras perderse en una
edición. Metodología confirmada por Victor: usar el HH contractual total,
la cuadrilla promedio que indican las partidas del APU, y la jornada
laboral que figura en el APU.

| Celda | Contenido | Tipo |
|---|---|---|
| `G37` HH Contractual Total (Work Package) | `=F33` | Fórmula (vive del bloque B1) |
| `G38` Cuadrilla promedio por actividad | Promedio simple de la cuadrilla total (suma de `Cuadrilla` de las filas HH) de cada partida **que tiene mano de obra** — partidas sin mano de obra (solo material) no cuentan. En este proyecto: 8 partidas, cuadrillas 3, 3.5, 3.5, 3.5, 3.5, 2.5, 2.5, 2.5 → promedio 3.0625 | **Valor fijo**, no fórmula — la composición de cuadrilla por partida no vive en `DP`, solo en el APU externo |
| `G39` Horas por jornada | 10 (ver §1.1) | **Valor fijo** |
| `G40` Duración estimada (días) | `=G37/(G38*G39)` → 5.75 días | Fórmula |

`PR!I30` (bajo la etiqueta "Duración estimada (días):") lee `=DP!G40`.

## 4. Trazabilidad `DP → PR`

`PR` no tiene datos propios de línea base — todo lo que no es "avance real"
(columnas de acumulado/restante) lo trae de `DP` por fórmula directa
(`=DP!<celda>`), para que actualizar `DP` (p. ej. corregir un metrado)
propague solo a `PR` sin tocarlo a mano. Mapeo completo:

- `PR!A13:A21,B,D,F,G,J` (Partidas de Control) ← `DP!B10,B25:B32` y sus
  columnas C/D/E/F/G paralelas (fila por fila, mismo orden que `DP` B1).
- `PR!F29` (Costo equipos) ← `DP!G63`.
- `PR!I29` (HH Contractual) ← `DP!E24` (dentro de la propia PR, no de DP —
  nota aparte).
- `PR!I30` (Duración estimada) ← `DP!G40`.
- `PR!B35:I40` (Mano de Obra) ← `DP!C47:F52`.
- `PR!B54:I58` (Equipos) ← `DP!C57:F61`.
- `PR!J72` (Costo materiales) ← `DP!E83`.
- `PR!B76,I76` (Subcontratos) ← `DP!C87,D87`.
- `PR!J82` (Costo subcontratos) ← `DP!E88`.
- `DASHBOARD!B2,B3` (Proyecto, Cliente) ← `DP!C4,C5`.
- `DASHBOARD!A8,C33,C36` usan `DP!D10` como bandera: si está vacío, el
  proyecto todavía no tiene programación valorizada (curva PV) y esas
  celdas muestran `"Pendiente"` en vez de calcular con datos que no
  existen.

**Regla al editar `DP`:** insertar o borrar filas/columnas en los bloques
B1-C4 rompe estas referencias (fueron escritas como enlaces directos a
celda, no como rango con nombre ni tabla estructurada). Si hace falta
insertar una fila, revisar después esta lista completa contra `PR` y
`DASHBOARD` antes de dar la hoja por buena.

## 4.1 Validación / Auditoría — reconciliación top-down vs. bottom-up

Agregado el 2026-08-16 (filas 91-104 de `DP`), a pedido de Victor: verificar
que el Costo Directo Total dé el mismo número calculado de dos formas
independientes, y dejar la evidencia en la propia hoja.

- **Top-down** (`G93 = DP!G33`): `Σ metrado × P.U. contractual` de cada
  partida (bloque B1, Work Package).
- **Bottom-up** (`G94 = DP!D43`): `Σ` de los 4 componentes de Recursos
  (Mano de Obra + Equipos + Materiales + Subcontratos, bloques C1-C4).
- `G95` diferencia absoluta, `G96` diferencia relativa (`G95/G93`), `G97`
  veredicto por fórmula (`IF(G96<=0.0001,"OK...","REVISAR...")`).
- Nota técnica (`B99:G104`, fórmula `TEXT()`/`&`, se recalcula sola si
  cambian los datos): explica la causa de la diferencia y cita el monto
  exacto. **Verificado en el proyecto real (recalculado con Excel vía
  COM): diferencia de $0.03 (0.0005%)**, causada por que la tabla Work
  Package (`DP` columna G) guarda el P.U. redondeado a 3 decimales para
  presentación, mientras que las tablas de Recursos usan los valores del
  APU sin redondear — no es un error de datos, es tolerancia de redondeo
  de copiado.
- **Límite técnico de Excel a tener en cuenta si se edita esta nota:**
  cada literal `"..."` dentro de una fórmula tiene un máximo de 255
  caracteres — un texto narrativo largo como este debe partirse en
  fragmentos cortos unidos con `&`, nunca como un solo literal largo (un
  literal de más de 255 caracteres corrompe el archivo para Excel real,
  aunque `openpyxl` lo siga leyendo sin quejarse — así se rompió una vez
  al construir este mismo bloque, se detectó porque `Workbooks.Open` vía
  COM fallaba con un error genérico mientras `openpyxl` abría el archivo
  sin problema).
- Esta validación es el patrón a replicar para cualquier proyecto nuevo:
  si el veredicto da "REVISAR", hay un error real de trazabilidad entre
  el presupuesto (`CD`) y el APU, no solo una diferencia de redondeo.

## 5. Reglas operativas (de `memoria.md`, aplican a cualquier edición de estos archivos)

- Antes de escribir en un `.xlsx` de este proyecto, revisar que no exista
  el archivo de candado `~$<nombre>.xlsx` en la misma carpeta — si existe,
  el archivo está abierto en Excel, parar y pedir que se cierre primero.
- No reconstruir tablas que Victor ya tiene armadas en su plantilla real
  con datos de ejemplo — preguntar por la ubicación del archivo real antes
  de rehacer algo desde cero.

## 6. Limitaciones conocidas / no automatizado todavía

- "Herramientas menores (%MO)" (`DP!G62`) **ya tiene fórmula/metodología
  documentada** (ver §2, bloque C2) y sale del APU real, pero el valor en
  `DP` sigue siendo pegado a mano, no una fórmula viva entre archivos
  (mismo criterio que el resto de `DP` — ver §1). Cualquier automatización
  debe calcularlo por script contra el APU del proyecto nuevo (sumando la
  línea `HERRAMIENTAS MANUALES` × metrado de cada partida que la tenga),
  no asumir un 3% fijo global ni copiar el número de otro proyecto.
- La Cuadrilla promedio y las Horas por jornada del bloque de Duración
  (§3) son valores fijos pegados a mano, no fórmulas que lean el APU en
  vivo — un agente que genere `DP` automáticamente sí debería calcularlos
  por script (tal como se hizo aquí) en vez de dejarlos como constantes
  editables sueltas.
- Los Datos generales (§ A) son texto copiado, no enlazados por fórmula al
  `CD` ni al presupuesto original.
