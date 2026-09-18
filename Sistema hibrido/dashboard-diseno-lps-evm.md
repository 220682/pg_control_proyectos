# Diseño — Dashboard Híbrido LPS + EVM

Fecha: 2026-08-15
Archivo destino: `Sistema hibrido/Consolidado proyecto.xlsx`, hoja `DASHBOARD` (ya existe, vacía)
Estado: diseño aprobado por Victor en conversación, pendiente de implementar

## 1. Objetivo

Dashboard interactivo, formal (audiencia: Jefe de Proyectos / Cliente), que integra
Last Planner System (PPC/CNC) y Valor Ganado (EVM), y genera un resumen ejecutivo
en texto plano orientado a proyectos **pequeños**: habla en metrado y plata
ejecutada, no en jerga de índices (CPI/SPI/IP) como primer mensaje.

## 2. Enfoque técnico (decidido)

- **Solo fórmulas nativas de Excel** (TEXTJOIN/IF/SUMPRODUCT/formato condicional).
  Sin VBA (evita macro-habilitada .xlsm y advertencias de seguridad) ni Power
  Query (DP y PR ya viven en el mismo libro, no hay fuentes externas que
  combinar). Mismo criterio de trazabilidad por fórmula ya usado en DP→PR.
- Todo el dashboard es de **solo lectura visual**: no se edita nada en
  `DASHBOARD`, todo se calcula desde `DP`, `PR` e `HISTORIAL`.

## 3. Arquitectura de datos

```
DP (línea base, presupuesto/APU)
  -> PR (avance real, se edita cada semana con el RDT validado)
       -> HISTORIAL (nueva hoja: una fila-snapshot por corte semanal/viernes)
            -> DASHBOARD (lee de PR para "estado de hoy", de HISTORIAL para tendencia)
```

## 4. Hoja HISTORIAL (nueva)

Una fila por corte semanal. **Valores pegados, no fórmulas** — es a propósito:
un historial con fórmulas vivas dejaría de ser historial (cambiaría solo con
que alguien edite `PR` después). Cada viernes de cierre se agrega una fila
nueva copiando los totales de ese momento.

Columnas: `Fecha de corte` | `Semana N°` | `PV` (en blanco hasta que exista
cronograma valorizado) | `EV` | `AC` | `HH Meta Acum.` | `HH Real Acum.` |
`PPC de la semana` | `% Avance físico`.

Hoy arranca con una sola fila (todo en 0 / vacío) — proyecto en día cero.

**Decisión pendiente de confirmar con Victor:** el Pareto de CNC (bloque E)
necesita causas de no cumplimiento por semana, y hoy la tabla de CNC vive
solo en `PR` (Tabla D, PPC semanal) y se sobrescribe cada viernes. Propuesta
por defecto: agregar una hoja `CNC_LOG` (o columnas extra en `HISTORIAL`)
donde, cada viernes, se copien las filas de CNC de esa semana antes de
limpiar la Tabla D de `PR` para la semana entrante. Si Victor no lo confirma,
el Pareto se implementa solo con los datos de la semana vigente (sin
histórico) como fallback.

## 5. Hoja DASHBOARD — bloques

### A. Encabezado + semáforo general
Proyecto, Cliente (enlazado a `DP`), fecha de corte vigente (última fila de
`HISTORIAL`), y un semáforo único: el **peor** de CPI e IP de MO (ver
umbrales en sección 7). SPI queda fuera del semáforo mientras no haya PV.

### B. Resumen Ejecutivo (texto plano, primero)
Párrafo armado con `TEXTJOIN`/`IF`, en este orden: avance físico y valor
ganado en $ → gasto real en $ → horas reales vs. horas que el avance debería
haber tomado (en plata/horas, no como "IP=X%") → PPC de la semana → nota de
PV pendiente (solo si aplica). Plantilla exacta:

> "Al cierre del [fecha de corte], el proyecto presenta un avance físico
> ejecutado del [%avance]% sobre el metrado total de las partidas. En
> términos de Valor Ganado, el trabajo realmente ejecutado representa
> $[EV] USD de un presupuesto total de $[BAC] USD. A la fecha se ha gastado
> $[AC] USD en mano de obra, equipos y materiales. En mano de obra, la
> cuadrilla ha trabajado [HH real] horas frente a las [HH ganadas] horas que
> ese avance debería haber tomado. De las [N] actividades comprometidas esta
> semana, se cumplieron [M] ([PPC]%). [Nota condicional: "Aún no se cuenta
> con la programación valorizada del proyecto, por lo que no es posible
> comparar el avance contra lo planificado en el tiempo."]"

### B2. Listado de partidas — avance y estado
Tabla desde `PR` (las 9 partidas reales): WBS, Partida, Und., Metrado
Contractual, Metrado Acumulado, % Avance, **Estado**:
- `NO INICIA` — Metrado Acumulado vacío o 0
- `EJECUTÁNDOSE` — 0 < Metrado Acumulado < Metrado Contractual
- `TERMINADO` — Metrado Acumulado ≥ Metrado Contractual

Formato condicional por color (gris/rojo, ámbar, verde — mismo lenguaje
visual que el semáforo general).

### C. Tarjetas de KPI (detalle técnico, más abajo)
% Avance físico, CPI, EAC, IP de MO Global, PPC de la semana, Duración
estimada restante. Aquí sí aparecen los nombres técnicos (CPI/IP), como
apoyo para quien los busca — no en el resumen de arriba.

### D. Bloque EVM (tabla)
BAC / PV / EV / AC / CV / CPI / EAC / VAC. **PV, SV y SPI muestran
"Pendiente"** (`IF(PV="","Pendiente",fórmula)`) hasta que exista cronograma
valorizado — nunca 0 ni error, para que no se lea como "vas a tiempo".

### E. Bloque LPS
PPC de la semana + gráfico de tendencia (línea, desde `HISTORIAL`). Pareto
de CNC (barras) — ver decisión pendiente en sección 4.

### F. Desglose de costo
Gráfico de barras/dona: Mano de obra / Equipos / Materiales / Subcontratos
(enlazado a `DP`/`PR`, ya trazable desde el trabajo de esta sesión).

### G. Curva S
PV/EV/AC en el tiempo, leyendo de `HISTORIAL` (PV en blanco hasta que
exista).

## 6. Semáforos — umbrales por defecto (ajustables)

| Indicador | Verde | Ámbar | Rojo |
|---|---|---|---|
| CPI | ≥ 0.95 | 0.85 – 0.95 | < 0.85 |
| IP de MO | ≥ 0.95 | 0.85 – 0.95 | < 0.85 |
| PPC | ≥ 80% | 60% – 80% | < 60% |
| Semáforo general (encabezado) | el peor color entre CPI e IP |

## 7. Manejo de la ausencia de PV

Toda celda dependiente de PV usa `IF(PV="","Pendiente",fórmula)`. El resto
del dashboard (costo, productividad de MO, PPC, avance físico) funciona
100% desde hoy con los datos de `DP`/`PR`.

## 8. Validación

Igual que el resto de esta sesión: tras implementar, recalcular con Excel
vía COM (`CalculateFullRebuild`) y verificar que los totales del dashboard
igualen a los de `DP`/`PR` (mismo patrón de verificación cruzada ya usado
para `DP`↔`CD` y `PR`↔`DP`).

## 9. Fuera de alcance de esta v1

- No se automatiza la captura semanal de `HISTORIAL` (es manual, a
  propósito — ver sección 4).
- No hay slicers/filtros interactivos (proyecto pequeño, 9 partidas, no se
  justifica la complejidad todavía).
- No se resuelve la fuente del cronograma valorizado (PV) — queda como
  "Pendiente" explícito hasta que Victor lo defina.
