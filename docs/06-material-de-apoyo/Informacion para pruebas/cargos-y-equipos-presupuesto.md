# Cargos, equipos y subcontratos del presupuesto (APU) — Bancoductos

Fuente: `Informacion para pruebas/PS-065-2026 - … BANCODUCTOS - AESA v2.xlsx`, hoja **APU**.
Extracción con detección dinámica de columnas (no atada a un layout fijo).
Partidas APU únicas: **48**.

Reglas aplicadas (acordadas 2026-09-06):
1. Descripción normalizada — espacios colapsados, punto final quitado, MAYÚSCULAS
   (fusiona `CAPATAZ`/`CAPATAZ.`, `PEON.`, `MINICARGADOR … YD3.`, etc.).
2. `MES` → `HH` con factor **8 h/día × 26 días/mes (sin domingos) = 208 HH/MES**.
   En el catálogo de cargos la unidad siempre es HH.
3. Herramientas eléctricas = **HM**, entran a equipos. Herramientas manuales
   (incluidas las `%MO`) NO entran.
4. Vehículos → se quedan en `MES`.
5. Subcontratos → se incluyen.

---

## Cargos (mano de obra) → `recursos_cargos` — 13 únicos

| # | Cargo | Unidad | Nº partidas | Apar. | Origen MES→HH |
|---|---|---|---|---|---|
| 1 | AYUDANTE TOPOGRAFO | HH | 1 | 1 | sí (×208) |
| 2 | CAPATAZ | HH | 29 | 31 | sí (×208) |
| 3 | CONDUCTOR | HH | 1 | 1 | sí (×208) |
| 4 | LOGISTICA | HH | 8 | 9 |  |
| 5 | OFICIAL | HH | 14 | 14 |  |
| 6 | OFICIAL ELECTRICISTA | HH | 3 | 3 |  |
| 7 | OPERADOR DE EQUIPO LIVIANO | HH | 6 | 7 |  |
| 8 | OPERADOR DE LINEA AMARILLA | HH | 9 | 10 |  |
| 9 | OPERARIO | HH | 15 | 15 | sí (×208) |
| 10 | OPERARIO ELECTRICISTA | HH | 3 | 3 |  |
| 11 | PEON | HH | 14 | 15 |  |
| 12 | TOPOGRAFO | HH | 1 | 1 | sí (×208) |
| 13 | VIGIA | HH | 11 | 12 |  |

Cargos cuyo insumo venía en MES (se convierten con ×208): AYUDANTE TOPOGRAFO, CAPATAZ, CONDUCTOR, OPERARIO, TOPOGRAFO.

## Equipos → `recursos_equipos` — 12

Regla: del bloque "Equipo:" del APU entra **todo** con su unidad tal cual
(HM / MES / UND). Único excluido: `%MO` (herramienta manual = % s/ mano de obra).
`ALICATE CRIMPADOR` conserva su unidad `UND` del presupuesto; todo lo demás es HM
salvo los vehículos, que van en MES.

| # | Equipo | Unidad propuesta | Categoría | ¿Duda? | Nº partidas | Apar. |
|---|---|---|---|---|---|---|
| 1 | ALICATE CRIMPADOR / PONCHADOR COAXIAL RG6-RG59 | UND | herramienta electrica | no | 2 | 2 |
| 2 | CAMION BARANDA | HM | maquinaria | no | 2 | 3 |
| 3 | CAMION VOLQUETE DE 15 M3 | HM | maquinaria | no | 8 | 8 |
| 4 | CAMIONETA PICK UP | MES | vehiculo | no | 1 | 1 |
| 5 | ESCALERA CON PLATAFORMA | HM | herramienta electrica | no | 3 | 3 |
| 6 | GRUPO ELECTROGENO 11KW | HM | herramienta electrica | no | 4 | 4 |
| 7 | MEZCLADOR PARA PINTURA | HM | herramienta electrica | no | 4 | 4 |
| 8 | MINICARGADOR 70 HP 0.5 YD3 | HM | maquinaria | no | 1 | 2 |
| 9 | MINIVAN 14 PASAJEROS | MES | vehiculo | no | 1 | 1 |
| 10 | ROTOMARTILLO | HM | herramienta electrica | no | 4 | 4 |
| 11 | TALADRO INALAMBRICO | HM | herramienta electrica | no | 2 | 2 |
| 12 | VIBRO APISONADOR | HM | herramienta electrica | no | 4 | 4 |

## Subcontratos → (tabla nueva `recursos_subcontratos`) — 1 únicos

| # | Subcontrato | Unidad | PU (USD) | Nº partidas | Apar. |
|---|---|---|---|---|---|
| 1 | MATERIAL DE AFIRMADO | M3 | 45.45 | 4 | 4 |

## Excluidos (1)

| # | Descripción | Unidad | Motivo | Nº partidas |
|---|---|---|---|---|
| 1 | HERRAMIENTAS MANUALES | %MO | herramienta manual (% s/ mano de obra) | 25 |
