# Dashboard Híbrido LPS+EVM — Plan de Implementación

> **Adaptación de la plantilla estándar a este proyecto:** no es un repo de
> código (no hay git, no hay pytest). Cada tarea reemplaza "test" por
> **verificación**: recalcular el libro vía Excel COM
> (`CalculateFullRebuild`) y leer el valor de celdas concretas, comparando
> contra el valor esperado calculado a mano — mismo patrón usado toda la
> sesión para DP/PR. "Commit" se reemplaza por "guardar el archivo"
> (`wb.save(...)`), no hay control de versiones.

**Goal:** Construir la hoja `DASHBOARD` de `Consolidado proyecto.xlsx`
(bloques A-G) más las hojas de soporte `HISTORIAL` y `CNC_LOG`, todo por
fórmula, según la spec.

**Architecture:** `DP` (línea base) → `PR` (avance real) → `HISTORIAL` /
`CNC_LOG` (snapshots semanales) → `DASHBOARD` (lee de `PR` para "hoy", de
`HISTORIAL`/`CNC_LOG` para tendencia).

**Tech Stack:** Python + openpyxl (escritura de fórmulas), Excel COM vía
PowerShell (`New-Object -ComObject Excel.Application`) para recalcular y
verificar.

**Spec:** `Sistema hibrido/dashboard-diseno-lps-evm.md`

## Global Constraints

- Todo por fórmula nativa de Excel. Sin VBA, sin Power Query (spec sección 2).
- Ninguna fórmula de índice/ratio (CPI, IP de MO, EAC, %consumidas, etc.)
  puede dividir por una celda que pueda estar en 0 o vacía sin una guarda
  `IFERROR(...,"Pendiente")` — no solo las que dependen de PV (spec sección
  7 amplía a **cualquier** ratio: en día cero, AC=0 y HH reales=0, así que
  CPI/IP también dividirían por cero si no se protegen).
- Antes de cada escritura al archivo, verificar que no exista
  `~$Consolidado proyecto.xlsx` (candado de Excel abierto) — si existe,
  detenerse y pedir a Victor que cierre el archivo.
- Toda celda combinada (`MergedCell`) se escribe en su celda ancla
  (superior-izquierda), nunca en las celdas fusionadas no-ancla — usar el
  helper `anchor()` ya usado en `trazabilidad_completa.py` de esta sesión.

---

### Task 1: Corregir encabezados desalineados de la tabla PPC en PR

**Files:**
- Modify: `Sistema hibrido/Consolidado proyecto.xlsx`, hoja `PR`, fila 12
  (columnas P:V)

**Interfaces:**
- Consumes: nada (fix aislado)
- Produces: columnas R13:R22 (Cumplido Sí/No) y S13:S22 (Causa CNC) con sus
  encabezados correctos en R12/S12 — de aquí en adelante el resto del plan
  lee PPC desde estas columnas confirmadas.

- [ ] **Step 1: Confirmar el desalineamiento actual**

```python
import openpyxl
PATH = r"c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
wb = openpyxl.load_workbook(PATH)
ws = wb["PR"]
for dv in ws.data_validations.dataValidation:
    print(dv.formula1, "->", dv.sqref)
# Esperado: list "Sí,No" -> R13:R22 ; list "Trabajo previo..." -> S13:S22
print([ws.cell(12, c).value for c in range(14, 23)])  # N..V
```

**Expected:** las validaciones confirman R=Cumplido, S=CNC; el encabezado
en R12 dice "Partida / WBS" (incorrecto) y en S12 "Cuadrilla / Responsable"
(incorrecto).

- [ ] **Step 2: Recorrer las etiquetas 2 columnas a la izquierda**

```python
# Guardar los textos originales antes de sobreescribir
partida_wbs = ws.cell(12, 18).value       # R12 actual: "Partida / WBS"
cuadrilla = ws.cell(12, 19).value          # S12 actual: "Cuadrilla / Responsable"

ws.cell(12, 16, partida_wbs)               # P12 <- "Partida / WBS"
ws.cell(12, 17, cuadrilla)                 # Q12 <- "Cuadrilla / Responsable"
ws.cell(12, 18, "Cumplido\n(Sí/No)")       # R12 <- correcto, coincide con la validacion
ws.cell(12, 19, "Causa de No Cumplimiento (CNC)")  # S12 <- correcto
ws.cell(12, 20, "Comentario")              # T12 <- lo que sobra de la etiqueta vieja
ws.cell(12, 21).value = None               # U12: limpiar (quedaba "Comentario" duplicado)
ws.cell(12, 22).value = None               # V12: limpiar
wb.save(PATH)
```

- [ ] **Step 3: Verificar con Excel COM**

```powershell
$path = "c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false; $excel.DisplayAlerts = $false
$wb = $excel.Workbooks.Open($path)
$ws = $wb.Sheets.Item("PR")
Write-Output $ws.Range("R12").Value2   # esperado: "Cumplido\n(Sí/No)"
Write-Output $ws.Range("S12").Value2   # esperado: "Causa de No Cumplimiento (CNC)"
$wb.Save(); $wb.Close($false); $excel.Quit()
```

**Expected:** R12 y S12 muestran las etiquetas correctas, alineadas con
las columnas donde realmente caen los dropdowns.

---

### Task 2: Crear la hoja HISTORIAL

**Files:**
- Modify: `Sistema hibrido/Consolidado proyecto.xlsx` (agrega hoja `HISTORIAL`)

**Interfaces:**
- Consumes: nada (snapshot manual, no fórmulas de otras hojas)
- Produces: rango `HISTORIAL!A2:I2` en adelante — Task 9 (Curva S) y Task
  7/8 (tendencia PPC) leen de aquí. Columnas: A=Fecha de corte,
  B=Semana N°, C=PV, D=EV, E=AC, F=HH Meta Acum., G=HH Real Acum.,
  H=PPC de la semana, I=% Avance físico.

- [ ] **Step 1: Crear la hoja con encabezados y la fila de día cero**

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side

PATH = r"c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
wb = openpyxl.load_workbook(PATH)
if "HISTORIAL" in wb.sheetnames:
    del wb["HISTORIAL"]
ws = wb.create_sheet("HISTORIAL", index=wb.sheetnames.index("DASHBOARD") + 1)

headers = ["Fecha de corte", "Semana N°", "PV", "EV", "AC",
           "HH Meta Acum.", "HH Real Acum.", "PPC de la semana", "% Avance físico"]
header_fill = PatternFill("solid", fgColor="1F4E78")
header_font = Font(bold=True, color="FFFFFF")
for i, h in enumerate(headers):
    c = ws.cell(1, 1 + i, h)
    c.fill = header_fill
    c.font = header_font

# Fila de dia cero: todo en 0, PV en blanco (no existe cronograma valorizado)
import datetime
ws.cell(2, 1, datetime.date(2026, 8, 15))
ws.cell(2, 2, 0)
ws.cell(2, 3, None)   # PV pendiente
ws.cell(2, 4, 0)
ws.cell(2, 5, 0)
ws.cell(2, 6, 0)
ws.cell(2, 7, 0)
ws.cell(2, 8, 0)
ws.cell(2, 9, 0)

widths = {"A": 14, "B": 10, "C": 10, "D": 10, "E": 10, "F": 13, "G": 13, "H": 15, "I": 14}
for col, w in widths.items():
    ws.column_dimensions[col].width = w
ws.sheet_view.showGridLines = False

wb.save(PATH)
print("HISTORIAL creada, fila 2 = dia cero")
```

- [ ] **Step 2: Verificar**

```powershell
# mismo patron COM: abrir, leer HISTORIAL!A1:I2, cerrar
```
**Expected:** hoja `HISTORIAL` existe, fila 1 = encabezados, fila 2 = fecha
de hoy con ceros y C2 vacío (PV pendiente).

---

### Task 3: Crear la hoja CNC_LOG

**Files:**
- Modify: `Sistema hibrido/Consolidado proyecto.xlsx` (agrega hoja `CNC_LOG`)

**Interfaces:**
- Consumes: nada (se llena a mano cada viernes, copiando las filas de la
  Tabla D de `PR` antes de limpiarla para la semana entrante — decisión
  pendiente de confirmar con Victor, spec sección 4; se construye la
  estructura igual para no bloquear el resto del plan).
- Produces: rango `CNC_LOG!A2:D...` — Task 8 (Pareto de CNC) lee de aquí.
  Columnas: A=Semana N°, B=Fecha de corte, C=Actividad, D=Causa de No
  Cumplimiento (CNC).

- [ ] **Step 1: Crear la hoja (solo encabezados, sin filas — vacía hasta
  la primera semana real)**

```python
import openpyxl
from openpyxl.styles import Font, PatternFill

PATH = r"c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
wb = openpyxl.load_workbook(PATH)
if "CNC_LOG" in wb.sheetnames:
    del wb["CNC_LOG"]
ws = wb.create_sheet("CNC_LOG", index=wb.sheetnames.index("HISTORIAL") + 1)
headers = ["Semana N°", "Fecha de corte", "Actividad", "Causa de No Cumplimiento (CNC)"]
header_fill = PatternFill("solid", fgColor="1F4E78")
header_font = Font(bold=True, color="FFFFFF")
for i, h in enumerate(headers):
    c = ws.cell(1, 1 + i, h)
    c.fill = header_fill
    c.font = header_font
widths = {"A": 10, "B": 14, "C": 40, "D": 30}
for col, w in widths.items():
    ws.column_dimensions[col].width = w
ws.sheet_view.showGridLines = False
wb.save(PATH)
print("CNC_LOG creada (vacia)")
```

- [ ] **Step 2: Verificar** — abrir con COM, confirmar hoja `CNC_LOG`
  existe con 4 encabezados en fila 1 y ninguna fila de datos.

---

### Task 4: DASHBOARD Bloque A — Encabezado + semáforo general

**Files:**
- Modify: `Sistema hibrido/Consolidado proyecto.xlsx`, hoja `DASHBOARD`

**Interfaces:**
- Consumes: `DP!B4` (Proyecto), `DP!B5` (Cliente), `HISTORIAL!A2` (fecha de
  corte vigente = última fila), `PR!J51`/`PR!J50` (para CPI), `PR!L29`/`PR!F50`
  (para IP de MO — ver Task 7 donde se definen las celdas CPI/IP finales;
  aquí el semáforo referencia las MISMAS celdas que Task 7 va a crear en
  `DASHBOARD!D` para no duplicar lógica).
- Produces: `DASHBOARD!B2` (Proyecto), `B3` (Cliente), `B4` (Fecha de
  corte), `B5` (texto+color del semáforo general) — Task 5/6 empiezan en
  la fila 7, después de este bloque.

- [ ] **Step 1: Escribir el encabezado**

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

PATH = r"c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
wb = openpyxl.load_workbook(PATH)
ws = wb["DASHBOARD"]

ws.cell(1, 1, "DASHBOARD - CONTROL DE PROYECTO (LPS + EVM)").font = Font(bold=True, size=14)

ws.cell(2, 1, "Proyecto:").font = Font(bold=True)
ws.cell(2, 2, "=DP!B4")
ws.cell(3, 1, "Cliente:").font = Font(bold=True)
ws.cell(3, 2, "=DP!B5")
ws.cell(4, 1, "Fecha de corte:").font = Font(bold=True)
ws.cell(4, 2, "=HISTORIAL!A2")
ws.cell(4, 2).number_format = "dd/mm/yyyy"

ws.cell(5, 1, "Estado general:").font = Font(bold=True)
# CPI y IP se calculan aqui mismo (duplicado intencional de la formula que
# Task 7 tambien deja en el bloque D - ambas leen las mismas celdas fuente
# de PR, no hay doble fuente de verdad, solo dos lugares donde se ve el
# mismo numero)
ws.cell(5, 2,
    '=IFERROR(IF(OR(D_CPI<0.85,D_IP<0.85),"ROJO",IF(OR(D_CPI<0.95,D_IP<0.95),"AMBAR","VERDE")),"Pendiente")'
)
wb.save(PATH)
print("Bloque A escrito (con nombres D_CPI/D_IP definidos en Task 7)")
```

**Nota para quien ejecute esta tarea:** la fórmula de B5 usa los rangos con
nombre `D_CPI` y `D_IP` que Task 7 define (`Formulas > Name Manager`,
apuntando a `DASHBOARD!$D$xx` donde vive el CPI/IP calculado). Si se
ejecuta Task 4 antes que Task 7, B5 mostrará `#NAME?` hasta que Task 7 cree
esos nombres — es esperado, no es un error a corregir en este paso.

- [ ] **Step 2: Verificar** — COM: `B2`="SUMINISTRO, INSTALACION..." (el
  proyecto real), `B3`="COPREFA...", `B4`=fecha de hoy.

---

### Task 5: DASHBOARD Bloque B — Resumen Ejecutivo (texto plano)

**Files:**
- Modify: `Sistema hibrido/Consolidado proyecto.xlsx`, hoja `DASHBOARD`

**Interfaces:**
- Consumes: `PR!L30` (%Avance físico), `PR!L28` (EV=Valor ganado),
  `PR!C28` (BAC=Costo directo contractual), `PR!F50` (HH real, C1 acumulado),
  `PR!L29` (HH ganadas), `PR!N13:N22`/`R13:R22` (PPC: comprometidas/cumplidas,
  ver Task 1), `PR!R23` (PPC%), `DP!C10` (celda de referencia para saber si
  PV existe, hoy vacía).
- Produces: `DASHBOARD!A8` (el párrafo completo, celda combinada A8:H8) —
  ningún bloque posterior depende de esto (es el destino final del texto).

- [ ] **Step 1: Calcular el AC total (costo real) — antes no existía una
  sola celda con este número, hay que armarla desde las 4 partes**

```python
import openpyxl
PATH = r"c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
wb = openpyxl.load_workbook(PATH)
ws_pr = wb["PR"]

# Fix previo necesario: W46 (Subcontrata, item Prueba Hidrostatica) hoy
# tiene "=DP!D81" (el valor CONTRACTUAL, $800) en la columna que en el
# resto de la tabla significa "acumulado/real gastado" (ver W36/W37 en
# Materiales, que SI son acumulado). En dia cero no se ha pagado nada del
# subcontrato todavia -> debe quedar vacio, no 800, para que AC=0 hoy.
ws_pr["W46"] = None

wb.save(PATH)
print("W46 corregido a vacio (acumulado real del subcontrato = 0 en dia cero)")
```

- [ ] **Step 2: Verificar que AC se pueda calcular correctamente**

```powershell
# COM: recalcular, leer PR!J50 (Costo real MOD), PR!J60 (Costo real equipos),
# PR!W41 (Costo material acumulado), PR!W51 (Costo subcontrata acumulado)
# Esperado los 4 en 0 (dia cero, nada ejecutado)
```

- [ ] **Step 3: Escribir el bloque B en DASHBOARD**

```python
import openpyxl
from openpyxl.styles import Font, Alignment

PATH = r"c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
wb = openpyxl.load_workbook(PATH)
ws = wb["DASHBOARD"]

ws.cell(7, 1, "RESUMEN EJECUTIVO").font = Font(bold=True, size=12)

ac_formula = "PR!J50+PR!J60+PR!W41+PR!W51"
formula = (
    '="Al cierre del "&TEXT(HISTORIAL!A2,"dd/mm/yyyy")&'
    '", el proyecto presenta un avance f\u00edsico ejecutado del "&TEXT(PR!L30,"0%")&'
    '" sobre el metrado total de las partidas. En t\u00e9rminos de Valor Ganado, '
    'el trabajo realmente ejecutado representa $"&TEXT(PR!L28,"#,##0")&'
    '" USD de un presupuesto total de $"&TEXT(PR!C28,"#,##0")&'
    '" USD. A la fecha se ha gastado $"&TEXT(' + ac_formula + ',"#,##0")&'
    '" USD en mano de obra, equipos y materiales. En mano de obra, la cuadrilla '
    'ha trabajado "&TEXT(PR!F50,"0.0")&" horas frente a las "&TEXT(PR!L29,"0.0")&'
    '" horas que ese avance deber\u00eda haber tomado. De las "&COUNTA(PR!N13:N22)&'
    '" actividades comprometidas esta semana, se cumplieron "&COUNTIF(PR!R13:R22,"S\u00ed")&'
    '" ("&TEXT(IFERROR(PR!R23,0),"0%")&")."&'
    'IF(DP!C10="","  A\u00fan no se cuenta con la programaci\u00f3n valorizada del proyecto, '
    'por lo que no es posible comparar el avance contra lo planificado en el tiempo.","")'
)
ws.cell(8, 1, formula)
ws.merge_cells("A8:H8")
c = ws.cell(8, 1)
c.alignment = Alignment(wrap_text=True, vertical="top")
ws.row_dimensions[8].height = 90

wb.save(PATH)
print("Bloque B (Resumen Ejecutivo) escrito en A8")
```

- [ ] **Step 4: Verificar con COM**

```powershell
$path = "c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false; $excel.DisplayAlerts = $false
$wb = $excel.Workbooks.Open($path)
$excel.CalculateFullRebuild()
$ws = $wb.Sheets.Item("DASHBOARD")
Write-Output $ws.Range("A8").Value2
$wb.Save(); $wb.Close($false); $excel.Quit()
```

**Expected:** un párrafo legible que empieza "Al cierre del [fecha], el
proyecto presenta un avance físico ejecutado del 0%..." (0% porque es día
cero) y termina con la nota de PV pendiente.

---

### Task 6: DASHBOARD Bloque B2 — Listado de partidas (avance y estado)

**Files:**
- Modify: `Sistema hibrido/Consolidado proyecto.xlsx`, hoja `DASHBOARD`

**Interfaces:**
- Consumes: `PR!A13:A21` (WBS), `PR!B13:B21` (Partida), `PR!F13:F21` (Und.),
  `PR!G13:G21` (Metrado Contractual), `PR!H13:H21` (Metrado Acumulado).
- Produces: `DASHBOARD!A11:G21` — tabla visible, ningún bloque posterior
  depende de estas celdas por fórmula (es contenido terminal).

- [ ] **Step 1: Escribir la tabla con fórmulas de Estado y formato
  condicional**

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment
from openpyxl.formatting.rule import CellIsRule

PATH = r"c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
wb = openpyxl.load_workbook(PATH)
ws = wb["DASHBOARD"]

ws.cell(11, 1, "LISTADO DE PARTIDAS - AVANCE Y ESTADO").font = Font(bold=True, size=12)

headers = ["WBS", "Partida", "Und.", "Metrado Contractual", "Metrado Acumulado", "% Avance", "Estado"]
header_fill = PatternFill("solid", fgColor="1F4E78")
header_font = Font(bold=True, color="FFFFFF")
thin = Side(style="thin", color="999999")
border = Border(left=thin, right=thin, top=thin, bottom=thin)
for i, h in enumerate(headers):
    c = ws.cell(12, 1 + i, h)
    c.fill = header_fill
    c.font = header_font
    c.border = border

for i in range(9):  # 9 partidas reales, PR filas 13-21
    r = 13 + i
    pr_row = 13 + i
    ws.cell(r, 1, f"=PR!A{pr_row}")
    ws.cell(r, 2, f"=PR!B{pr_row}")
    ws.cell(r, 3, f"=PR!F{pr_row}")
    ws.cell(r, 4, f"=PR!G{pr_row}")
    ws.cell(r, 5, f"=PR!H{pr_row}")
    ws.cell(r, 6, f'=IFERROR(E{r}/D{r},0)')
    ws.cell(r, 6).number_format = "0%"
    ws.cell(r, 7, f'=IF(OR(E{r}="",E{r}=0),"NO INICIA",IF(E{r}>=D{r},"TERMINADO","EJECUTANDOSE"))')
    for col in range(1, 8):
        ws.cell(r, col).border = border

# Formato condicional de la columna Estado (G13:G21)
red_fill = PatternFill("solid", fgColor="F4CCCC")
amber_fill = PatternFill("solid", fgColor="FCE4A6")
green_fill = PatternFill("solid", fgColor="C6E0B4")
rng = "G13:G21"
ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"NO INICIA"'], fill=red_fill))
ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"EJECUTANDOSE"'], fill=amber_fill))
ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"TERMINADO"'], fill=green_fill))

widths = {"A": 10, "B": 45, "C": 6, "D": 12, "E": 12, "F": 10, "G": 14}
for col, w in widths.items():
    ws.column_dimensions[col].width = w

wb.save(PATH)
print("Bloque B2 escrito, filas 11-21")
```

- [ ] **Step 2: Verificar con COM** — `G13` (Estado de la primera
  partida) debe dar `"NO INICIA"` (Metrado acumulado vacío, día cero).

---

### Task 7: DASHBOARD Bloque C — Tarjetas de KPI + Bloque D — Tabla EVM

**Files:**
- Modify: `Sistema hibrido/Consolidado proyecto.xlsx`, hoja `DASHBOARD`

**Interfaces:**
- Consumes: `PR!L30` (%avance), `PR!L28` (EV), `PR!C28` (BAC), AC (misma
  fórmula de 4 partes que Task 5), `PR!L29`/`PR!F50` (HH ganadas/reales),
  `PR!R23` (PPC), `PR!P31` (Duración estimada).
- Produces: `DASHBOARD!D24` (CPI) y `DASHBOARD!D25` (IP de MO) — Task 4
  (semáforo) los referencia por nombre definido `D_CPI`/`D_IP`; se crean
  esos nombres en este mismo paso.

- [ ] **Step 1: Escribir tarjetas KPI (C) y tabla EVM (D)**

```python
import openpyxl
from openpyxl.styles import Font, PatternFill, Border, Side
from openpyxl.workbook.defined_name import DefinedName

PATH = r"c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
wb = openpyxl.load_workbook(PATH)
ws = wb["DASHBOARD"]
AC = "(PR!J50+PR!J60+PR!W41+PR!W51)"

ws.cell(23, 1, "TARJETAS DE KPI").font = Font(bold=True, size=12)
kpis = [
    ("% Avance físico", "=PR!L30", "0%"),
    ("CPI", f'=IFERROR(PR!L28/{AC},"Pendiente")', "0.00"),
    ("EAC", f'=IFERROR(PR!C28/(PR!L28/{AC}),"Pendiente")', "$#,##0"),
    ("IP de MO Global", "=IFERROR(PR!L29/PR!F50,\"Pendiente\")", "0%"),
    ("PPC de la semana", "=IFERROR(PR!R23,\"Pendiente\")", "0%"),
    ("Duración estimada (días)", "=PR!P31", "0.0"),
]
for i, (label, formula, fmt) in enumerate(kpis):
    r = 24 + i
    ws.cell(r, 1, label).font = Font(bold=True)
    c = ws.cell(r, 4, formula)
    c.number_format = fmt
    c.font = Font(bold=True, size=12, color="1F4E78")

wb.save(PATH)

# Nombres definidos para que el semaforo del Bloque A (Task 4) los use
wb = openpyxl.load_workbook(PATH)
wb.defined_names["D_CPI"] = DefinedName("D_CPI", attr_text="DASHBOARD!$D$25")
wb.defined_names["D_IP"] = DefinedName("D_IP", attr_text="DASHBOARD!$D$27")
wb.save(PATH)

# Bloque D: tabla EVM completa
wb = openpyxl.load_workbook(PATH)
ws = wb["DASHBOARD"]
ws.cell(31, 1, "BLOQUE EVM").font = Font(bold=True, size=12)
evm_rows = [
    ("BAC", "=PR!C28", "$#,##0"),
    ("PV", '=IF(DP!C10="","Pendiente",0)', "$#,##0"),
    ("EV", "=PR!L28", "$#,##0"),
    ("AC", f"={AC}", "$#,##0"),
    ("SV (EV-PV)", '=IF(DP!C10="","Pendiente",PR!L28-0)', "$#,##0"),
    ("CV (EV-AC)", f"=PR!L28-{AC}", "$#,##0"),
    ("SPI (EV/PV)", '=IF(DP!C10="","Pendiente","Pendiente")', "0.00"),
    ("CPI (EV/AC)", f'=IFERROR(PR!L28/{AC},"Pendiente")', "0.00"),
    ("EAC (BAC/CPI)", f'=IFERROR(PR!C28/(PR!L28/{AC}),"Pendiente")', "$#,##0"),
    ("VAC (BAC-EAC)", f'=IFERROR(PR!C28-(PR!C28/(PR!L28/{AC})),"Pendiente")', "$#,##0"),
]
for i, (label, formula, fmt) in enumerate(evm_rows):
    r = 32 + i
    ws.cell(r, 1, label).font = Font(bold=True)
    c = ws.cell(r, 3, formula)
    c.number_format = fmt

wb.save(PATH)
print("Bloques C y D escritos; nombres D_CPI/D_IP definidos")
```

**Nota:** SV/SPI quedan como `"Pendiente"` incondicionalmente hasta que se
defina la fuente de PV (spec sección 7) — el `IF(DP!C10="",...)` es un
placeholder de estructura, no una fuente real de PV; cuando exista PV real,
esta fórmula se reemplaza apuntando a la celda real donde viva el
cronograma valorizado.

- [ ] **Step 2: Verificar con COM** — `D25`(CPI)="Pendiente" (AC=0, día
  cero), `C32`(BAC)=5798.31 (mismo valor validado toda la sesión).

---

### Task 8: DASHBOARD Bloque E — PPC + tendencia + Pareto de CNC

**Files:**
- Modify: `Sistema hibrido/Consolidado proyecto.xlsx`, hoja `DASHBOARD`

**Interfaces:**
- Consumes: `PR!R23` (PPC de hoy), `HISTORIAL!A:H` (tendencia), `CNC_LOG!D`
  (Pareto — vacío hasta la primera semana real, el gráfico se construye
  igual, mostrará vacío).
- Produces: `DASHBOARD!A42` (título), gráfico de línea (PPC en el tiempo) y
  gráfico de barras (Pareto CNC) anclados en `DASHBOARD!A44`/`E44`.

- [ ] **Step 1: PPC actual + tabla de apoyo para el Pareto**

```python
import openpyxl
from openpyxl.styles import Font
from openpyxl.chart import LineChart, BarChart, Reference

PATH = r"c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
wb = openpyxl.load_workbook(PATH)
ws = wb["DASHBOARD"]
ws_cnc = wb["CNC_LOG"]

ws.cell(42, 1, "BLOQUE LPS - PPC Y CAUSAS DE NO CUMPLIMIENTO").font = Font(bold=True, size=12)
ws.cell(43, 1, "PPC de la semana vigente:").font = Font(bold=True)
ws.cell(43, 3, "=IFERROR(PR!R23,\"Pendiente\")").number_format = "0%"

# Tabla de apoyo para el Pareto: conteo por causa (8 categorias fijas)
causas = ["Trabajo previo no terminado", "Mano de obra", "Materiales", "Equipos",
          "Diseño-Información", "Clima", "Permisos-SSOMA", "Reprogramación"]
ws.cell(45, 1, "Causa").font = Font(bold=True)
ws.cell(45, 2, "N° de veces").font = Font(bold=True)
for i, causa in enumerate(causas):
    r = 46 + i
    ws.cell(r, 1, causa)
    ws.cell(r, 2, f'=COUNTIF(CNC_LOG!$D:$D,A{r})')

# Grafico de tendencia PPC (linea) desde HISTORIAL
chart1 = LineChart()
chart1.title = "Tendencia PPC"
data = Reference(wb["HISTORIAL"], min_col=8, min_row=1, max_row=wb["HISTORIAL"].max_row)
cats = Reference(wb["HISTORIAL"], min_col=1, min_row=2, max_row=wb["HISTORIAL"].max_row)
chart1.add_data(data, titles_from_data=True)
chart1.set_categories(cats)
chart1.height, chart1.width = 7, 12
ws.add_chart(chart1, "A55")

# Grafico Pareto CNC (barras) desde la tabla de apoyo A46:B53
chart2 = BarChart()
chart2.title = "Pareto de Causas de No Cumplimiento"
data2 = Reference(ws, min_col=2, min_row=45, max_row=53)
cats2 = Reference(ws, min_col=1, min_row=46, max_row=53)
chart2.add_data(data2, titles_from_data=True)
chart2.set_categories(cats2)
chart2.height, chart2.width = 7, 12
ws.add_chart(chart2, "H55")

wb.save(PATH)
print("Bloque E escrito: PPC, tabla de apoyo Pareto (46-53), 2 graficos")
```

- [ ] **Step 2: Verificar con COM** — `C43` (PPC) = "Pendiente" (día cero,
  `COUNTA`/`COUNTIF` sobre la tabla PPC vacía cae en el `IFERROR`); `B46:B53`
  todos en 0 (CNC_LOG vacío).

---

### Task 9: DASHBOARD Bloque F — Desglose de costo (gráfico)

**Files:**
- Modify: `Sistema hibrido/Consolidado proyecto.xlsx`, hoja `DASHBOARD`

**Interfaces:**
- Consumes: `PR!F28` (Costo mano de obra), `PR!F29` (Costo equipos),
  `PR!F30` (Costo Materiales), `PR!I28` (Subcontratos) — los 4 ya
  trazables a `DP` desde la sesión anterior.
- Produces: `DASHBOARD!A65` (tabla de apoyo) + gráfico de dona anclado en
  `DASHBOARD!D65`.

- [ ] **Step 1: Tabla de apoyo + gráfico**

```python
import openpyxl
from openpyxl.styles import Font
from openpyxl.chart import PieChart, Reference

PATH = r"c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
wb = openpyxl.load_workbook(PATH)
ws = wb["DASHBOARD"]

ws.cell(64, 1, "DESGLOSE DE COSTO (CONTRACTUAL)").font = Font(bold=True, size=12)
componentes = [("Mano de obra", "=PR!F28"), ("Equipos", "=PR!F29"),
               ("Materiales", "=PR!F30"), ("Subcontratos", "=PR!I28")]
for i, (label, formula) in enumerate(componentes):
    r = 65 + i
    ws.cell(r, 1, label)
    c = ws.cell(r, 2, formula)
    c.number_format = "$#,##0"

chart = PieChart()
chart.title = "Costo Directo Contractual por componente"
data = Reference(ws, min_col=2, min_row=65, max_row=68)
cats = Reference(ws, min_col=1, min_row=65, max_row=68)
chart.add_data(data)
chart.set_categories(cats)
chart.height, chart.width = 8, 12
ws.add_chart(chart, "D65")

wb.save(PATH)
print("Bloque F escrito: filas 64-68 + grafico de dona")
```

- [ ] **Step 2: Verificar con COM** — suma de `B65:B68` = 5798.31 (mismo
  BAC validado en toda la sesión).

---

### Task 10: DASHBOARD Bloque G — Curva S (PV/EV/AC en el tiempo)

**Files:**
- Modify: `Sistema hibrido/Consolidado proyecto.xlsx`, hoja `DASHBOARD`

**Interfaces:**
- Consumes: `HISTORIAL!A:E` (Fecha, PV, EV, AC).
- Produces: gráfico de línea anclado en `DASHBOARD!A80`.

- [ ] **Step 1: Gráfico Curva S**

```python
import openpyxl
from openpyxl.styles import Font
from openpyxl.chart import LineChart, Reference

PATH = r"c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
wb = openpyxl.load_workbook(PATH)
ws = wb["DASHBOARD"]
ws_hist = wb["HISTORIAL"]

ws.cell(79, 1, "CURVA S (PV / EV / AC)").font = Font(bold=True, size=12)

chart = LineChart()
chart.title = "Curva S"
chart.y_axis.title = "USD"
chart.x_axis.title = "Fecha de corte"
data = Reference(ws_hist, min_col=3, max_col=5, min_row=1, max_row=ws_hist.max_row)  # PV,EV,AC
cats = Reference(ws_hist, min_col=1, min_row=2, max_row=ws_hist.max_row)
chart.add_data(data, titles_from_data=True)
chart.set_categories(cats)
chart.height, chart.width = 9, 18
ws.add_chart(chart, "A80")

wb.save(PATH)
print("Bloque G escrito: grafico Curva S")
```

- [ ] **Step 2: Verificar con COM** — el gráfico existe y referencia
  `HISTORIAL!C1:E2` (una sola fila hoy, día cero — se irá poblando cada
  viernes).

---

### Task 11: Verificación final cruzada de todo el DASHBOARD

**Files:**
- Ninguno (solo lectura/verificación)

**Interfaces:**
- Consumes: todo lo construido en Tasks 4-10.
- Produces: reporte de verificación (no se escribe al archivo).

- [ ] **Step 1: Recalcular todo el libro y volcar los valores clave**

```powershell
$path = "c:\Users\BRANDY\Downloads\VICTOR\CLAUDE CODE\pg_control_proyectos\Sistema hibrido\Consolidado proyecto.xlsx"
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false; $excel.DisplayAlerts = $false
$wb = $excel.Workbooks.Open($path)
$excel.CalculateFullRebuild()
$ws = $wb.Sheets.Item("DASHBOARD")
Write-Output ("B2 Proyecto: " + $ws.Range("B2").Value2)
Write-Output ("B5 Semaforo: " + $ws.Range("B5").Value2)
Write-Output ("A8 Resumen (primeros 80 char): " + $ws.Range("A8").Value2.Substring(0,80))
Write-Output ("G13 Estado partida 1: " + $ws.Range("G13").Value2)
Write-Output ("D25 CPI: " + $ws.Range("D25").Value2)
Write-Output ("C32 BAC: " + $ws.Range("C32").Value2)
Write-Output ("C43 PPC: " + $ws.Range("C43").Value2)
Write-Output ("Suma costo B65:B68: " + ($ws.Range("B65").Value2+$ws.Range("B66").Value2+$ws.Range("B67").Value2+$ws.Range("B68").Value2))
$wb.Save(); $wb.Close($false); $excel.Quit()
```

**Expected:** `B2`="SUMINISTRO, INSTALACION..."; `B5`="Pendiente" o
"ROJO"/"AMBAR" según guarda IFERROR (día cero: `IFERROR` cae a
"Pendiente"); `G13`="NO INICIA"; `D25`="Pendiente"; `C32`=5798.31 (o
5798.3074, mismo número validado toda la sesión); `C43`="Pendiente"; suma
de costo = 5798.31.

- [ ] **Step 2: Reportar a Victor** cualquier celda que no coincida con lo
  esperado antes de dar la tarea por cerrada.

---

## Resumen de cobertura de la spec

| Sección de la spec | Task que la implementa |
|---|---|
| 2. Enfoque técnico (solo fórmulas) | Todas |
| 4. HISTORIAL | Task 2 |
| 4. Decisión CNC_LOG | Task 3 |
| 5.A Encabezado + semáforo | Task 4 |
| 5.B Resumen Ejecutivo | Task 5 |
| 5.B2 Listado de partidas | Task 6 |
| 5.C Tarjetas KPI | Task 7 |
| 5.D Bloque EVM | Task 7 |
| 5.E Bloque LPS | Task 8 |
| 5.F Desglose de costo | Task 9 |
| 5.G Curva S | Task 10 |
| 6. Umbrales de semáforo | Task 4 |
| 7. Manejo de ausencia de PV | Task 7 (todas las celdas EVM) |
| 8. Validación | Task 11 |
