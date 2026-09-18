# Spec — Hoja `3WLA` (Three Week Look Ahead)

Documenta de dónde sale cada dato de la hoja `3WLA` y cómo se traslada desde
el sistema por-proyecto (`Consolidado proyecto.xlsx`) hacia el portafolio.
Escrito 2026-08-16/17 tras corregir errores reales de fórmula en `3WLA` (ver
`memoria.md` / historial de conversación) y antes de construir el mecanismo
de verificación ("revisar") — ver pendiente en sección 5.

## 0. Decisión de arquitectura (confirmada por Victor)

- **Un `Consolidado proyecto.xlsx` por proyecto real**, cada uno con su
  propia `DP`/`PR`. No se centralizan varios proyectos en un mismo libro.
- `3WLA` vive en un **archivo de portafolio aparte**, con un bloque de filas
  por proyecto (mismo patrón que las filas de prueba "Proyecto A" / "Proyecto
  B" ya construidas: fila de subtotal del proyecto + Subpresupuesto1/2 +
  Partida1-3).
- El traslado de datos de cada `PR` de proyecto hacia el bloque
  correspondiente en `3WLA` es **por valores** (copiar-pegar o un script de
  refresco), **no por enlace vivo entre archivos** (`='[Consolidado
  ProyectoX.xlsx]PR'!G13`). Motivo: los enlaces externos son el mecanismo que
  generó los 14,646 nombres definidos corruptos que ya causaron una
  corrupción real en este mismo archivo (ver historial de conversación,
  2026-08-16) — no se repite ese patrón a propósito.
- Consecuencia: el mecanismo de "revisar" (sección 5, pendiente) tiene que
  verificar una **copia de valores**, no una fórmula viva — es decir, debe
  comparar el valor pegado en `3WLA` contra el valor fuente en el `PR` de
  origen en el momento del traslado, no confiar en que la fórmula siga
  correcta indefinidamente.

## 1. Por qué `PR`, no `DP`

`DP` es la línea base (día cero): metrado contractual, HH contractual, P.U.
— pero **sus columnas de avance quedan vacías a propósito** (ver
`spec-hoja-dp.md`, sección 0). `PR` ya copia toda la línea base de `DP` por
fórmula **y además** agrega el avance real acumulado (`PR!H`, entrada
manual). Es decir: `PR` = `DP` + avance real.

Si `3WLA` tomara datos de `DP`, las columnas `F` (Metrado acumulado) y `L`
(HH acumulado) de `3WLA` no tendrían de dónde salir — `DP` no las tiene por
diseño. `PR` es la única fuente que contiene todo lo que `3WLA` necesita.

**Por lo tanto: `PR` es la fuente por defecto para llenar cada bloque de
proyecto en `3WLA`.**

## 2. Mapeo de columnas `PR` → `3WLA` (por partida)

Verificado fila por fila contra datos reales del proyecto HDPE Tie-In-06
(`PR` fila 13 = partida `00.01`, `DP` fila 10):

| `3WLA` (por partida) | Fuente | Fórmula/origen |
|---|---|---|
| `C` Activity ID / WBS | `PR!A` | `=DP!B<fila>` dentro de PR |
| `D` Descripción de la actividad | `PR!B` | `=DP!C<fila>` dentro de PR |
| `E` Metrado Contractual | `PR!G` | `=DP!F<fila>` dentro de PR |
| `F` Metrado acumulado | `PR!H` | **entrada manual en PR** — este es el dato real de avance |
| `N` Rend. HH x partida | `PR!D` | `=DP!D<fila>` dentro de PR |

**Estos 5 campos son los únicos que necesitan copiarse desde `PR`.** El
resto de columnas de `3WLA` (`G, H, I, J, K, L, M, O, P`) ya son fórmulas
locales que derivan de esos 5 (confirmado y reparado en la sesión anterior):

```
G (Metrado restante)   = E - F
H (Avance físico)      = IFERROR(F/E, 0)
I (Incidencia x part.) = IFERROR(E/$E$<subtotal proyecto>, 0)
J (Avance físico pond.)= H * I
K (HH contractual)     = E * N        ← pendiente: hoy es valor pegado a mano en las filas de prueba, debe pasar a fórmula
L (HH acumulado)       = F * N        (mismo cálculo que PR!L "P. horas ganadas")
M (HH restante)        = K - L
O (HH ganadas)         = F * N        (duplica L; se deja así porque ya alimenta AD, no se toca)
P (IP)                 = IFERROR(O/L, 0)
```

**No copiar `K` directamente de `PR!E`** aunque `PR!E` tenga el mismo valor
(`PR!E = D*G`, es decir `N*E` con los nombres de PR) — es más robusto que
`3WLA` calcule `K=E*N` con sus propias columnas ya traídas, así una sola
fórmula (`K`) no depende de un sexto campo copiado de `PR`.

**Nota — la plantilla de prueba tenía `K`/`N` al revés; ya está resuelto.**
En las filas de prueba originales ("Proyecto A"/"Proyecto B") `K` era un
valor pegado a mano y `N` la fórmula derivada (`N=IFERROR(K/E,0)`) — servía
para probar con HH inventadas sin preocuparse de cuál era la fuente. Con
`PR` real la dirección es la de esta sección: `N` es el valor copiado de
`PR!D`, `K` es la fórmula `=E*N`. `trasladar_pr_a_3wla.py` escribe siempre
en esta dirección (real), y `revisar_3wla.py` (`formula_leaf`, sección 5)
ya exige esta dirección al auditar — ambos scripts asumen datos reales de
`PR`, no la plantilla de prueba original.

## 3. Columnas que NO vienen de `PR` ni de `DP`

- `Q` (Duración días), `R` (Inicio), `S` (Fin): no existen en `PR` ni en
  `DP` — ninguno de los dos maneja cronograma por partida, solo cantidades y
  costos. **Fuente todavía sin definir.** Hoy están con fechas ficticias
  (instrucción explícita de Victor, 2026-08-16) precisamente porque este
  mapeo no está resuelto. Necesita una fuente de cronograma (¿un Gantt /
  programa maestro que no existe todavía en este sistema?) antes de poder
  automatizarse — **pendiente, no bloquea el resto de la spec**.
- `B` (Programado, "Si/No"): es una fórmula local de `3WLA` que evalúa si la
  partida cae dentro de la ventana de 3 semanas (`P6`/`R6`) — no depende de
  `PR`/`DP`, ya está resuelta.

## 4. Nivel de agregación — de partida de `PR` a partida de `3WLA`

`PR` no tiene jerarquía de Subpresupuesto — es una lista plana de partidas
(`B1 Working package`, filas 13-21). `3WLA` sí espera una jerarquía
Proyecto → Subpresupuesto → Partida (ver filas 10-18 de las pruebas
"Proyecto A"). Al trasladar datos de un `PR` real a un bloque de `3WLA`:

- Cada fila de partida de `PR` (13-21 en este archivo) mapea a una fila de
  partida (`Partida1`, `Partida2`, ...) dentro de ALGÚN Subpresupuesto de
  `3WLA` — pero `PR` no dice a qué Subpresupuesto pertenece cada partida.
  **Ese agrupamiento (qué partidas van en qué Subpresupuesto) es una
  decisión de planificación semanal, no un dato que ya exista en `PR`/`DP`**
  — la hace el planner al armar el lookahead de la semana, es la esencia
  del proceso LPS ("qué se hará", ver primera fase de esta conversación).
  No es automatizable desde `PR` solo; `PR` aporta el metrado/HH de cada
  partida, pero el planner decide en qué Subpresupuesto/semana la ubica.

## 4.1 Avance físico ponderado — por qué se pesa por HH y no por metrado (EVM)

Agregado 2026-08-17, a raíz de una pregunta de Victor tras editar la fila
Portafolio a mano. El metrado de partidas distintas **no es sumable ni
comparable entre sí** cuando tienen unidades distintas (verificado con datos
reales de `PR`: VJE, GLB, ML, UND mezclados en el mismo proyecto) — sumar
"1 GLB + 33.75 ML" no significa nada. Por eso:

- `E9/F9/G9` (metrado a nivel Portafolio) **no existen** — Victor las borró
  correctamente, no se reponen.
- `H` (Avance físico x partida = F/E) **solo es válida a nivel de partida**
  individual (misma unidad). No se usa como rollup — `H10`/`H19`/`H9` no
  existen a propósito.
- El agregado correcto es el **Earned Value clásico de EVM**: convertir todo
  a una unidad homogénea (HH) antes de promediar.
  - `I` (Incidencia x partida) = `IFERROR(K{r}/$K${proyecto},0)` — peso por
    HH contractual, **no** por metrado (`E{r}/$E${proyecto}`, que era el
    error original).
  - `J` (Avance físico ponderado) = `H×I`, igual que antes, pero ahora
    correctamente ponderado. En rollup (`J10`, `J19`) se mantiene
    `SUM(J_hijos)` — matemáticamente equivale a `O/K` (HH ganadas / HH
    contractual) del mismo bloque, se puede verificar así.
  - A nivel Portafolio, `J9 = IFERROR(O9/K9,0)` directo (no se puede sumar
    `J10+J19`, cada uno está en la escala 0-100% de SU PROPIO proyecto — el
    mismo problema que dio 200% en `AC9`, ver sección 0 de la conversación
    original).

**Rendimiento HH x partida (`N`)** — corregido en la misma sesión: es
`HH contractual / Metrado contractual` (cuántas HH hacen falta para 1 unidad
de metrado), fórmula `N=IFERROR(K/E,0)`, **no** `E/K`. Verificado contra
`PR` real: partida `02.02`, HH=35.81, Metrado=33.75 → Rendimiento=1.061,
coincide exacto con `PR!D15`.

## 5. Herramientas — "trasladar" y "revisar" (implementadas, 2026-08-17)

- **`trasladar_pr_a_3wla.py`** — hace el traslado real descrito en la sección
  2: por cada fila de partida de `3WLA` cuyo `C` (Activity ID) coincida con
  un WBS de `PR!A`, copia `D/E/F/N` como valores y escribe `K` como fórmula
  `=E*N`. El agrupamiento Partida→Subpresupuesto (sección 4) sigue siendo
  decisión del planner: el script no lo infiere, requiere que `C` ya tenga
  el código WBS (a mano, o vía `--mapa "fila:codigo,..."` para escribirlo de
  una). Preserva el prefijo de 6 espacios en `D` que usa la detección de
  estructura por sangría (ver `revisar_3wla.py`). Soporta `--dry-run`.
  Uso: `python trasladar_pr_a_3wla.py "archivo.xlsx" [--pr "otro.xlsx"] --mapa "12:00.01,13:02.01,..."`.
- **`revisar_3wla.py`** — verifica lo que dejó el traslado:
  1. Por cada partida trasladada, compara `E/F/N` pegados contra el valor
     vivo en el `PR` de origen (mismo WBS en columna `C`) — detecta traslado
     incorrecto o `PR` que cambió después (re-planificación).
  2. Verifica que las fórmulas locales de `3WLA` (incluida `K=E*N`, ver nota
     de la sección 2) sigan siendo exactamente las de la plantilla — texto
     de fórmula, no resultado.

Ambos scripts probados juntos sobre datos reales de `PR` (proyecto HDPE
Tie-In-06): traslado de 6 partidas, 0 desviaciones tras el traslado,
4 gráficos intactos.
