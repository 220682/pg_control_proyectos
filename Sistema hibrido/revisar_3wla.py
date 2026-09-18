# -*- coding: utf-8 -*-
"""
Revisar 3WLA — mecanismo de verificacion para la hoja 3WLA de un libro
"Consolidado proyecto.xlsx" (o del futuro archivo de portafolio).

Dos chequeos independientes, ver spec-hoja-3wla.md seccion 5:

  A. Integridad de formulas: recorre la estructura Portafolio -> Proyecto ->
     Subpresupuesto -> Partida (detectada por la sangria de la columna D y
     los codigos de la columna C) y compara el TEXTO de cada formula contra
     la plantilla esperada. No mira valores, mira si alguien pego un valor
     encima de una formula o rompio una referencia.

  B. Traslado de datos: para cada partida de 3WLA, si su Activity ID
     (columna C) coincide con un WBS de la hoja PR de origen, compara los
     campos que se copian de PR (E, F, N) contra los valores vivos en PR.
     Uso pensado para cuando ya haya un traslado real PR -> 3WLA (hoy los
     datos de prueba son ficticios, no vienen de PR, asi que el check B
     reporta "sin fuente" para todas las filas de prueba y eso es lo
     esperado).

Uso:
    python revisar_3wla.py "ruta\\Consolidado proyecto.xlsx" [--pr "ruta\\OtroLibro.xlsx"]

Si no se pasa --pr, el check B compara contra la hoja PR del MISMO libro
(uso valido solo si en algun momento 3WLA y PR conviven en un archivo).
"""
import sys
import os
import argparse
import win32com.client

sys.stdout.reconfigure(encoding="utf-8")

COLS_LEAF = ["G", "H", "I", "J", "K", "M", "N", "O", "P", "AB", "AC", "AD"]
COLS_LEAF_DIARIAS = ["V", "W", "X", "Y", "Z", "AA"]
COLS_SUBTOTAL = ["E", "F", "G", "J", "K", "L", "M", "O", "P"]  # H no aplica a rollups (solo a nivel partida, ver spec EVM)


def formula_leaf(col, r, subtotal_row):
    templates = {
        "G": f"=E{r}-F{r}",
        "H": f"=IFERROR(F{r}/E{r},0)",
        "I": f"=IFERROR(K{r}/$K${subtotal_row},0)",  # ponderado por HH, no por metrado (ver spec 2, EVM)
        "J": f"=H{r}*I{r}",
        "K": f"=E{r}*N{r}",  # HH contractual: se calcula, N es el valor pegado de PR!D (ver spec 2)
        "M": f"=K{r}-L{r}",
        "N": None,  # valor de entrada (Rendimiento HH x partida, pegado de PR!D)
        "O": f"=F{r}*N{r}",
        "P": f"=IFERROR(O{r}/L{r},0)",
        "AB": f"=SUM(U{r}:AA{r})",
        "AC": f"=IFERROR(AB{r}/E{r}*I{r},0)",
        "AD": f"=N{r}*AB{r}",
    }
    return templates[col]


def formula_subtotal(col, r, child_ranges):
    # child_ranges: lista de (ini,fin) de filas de partida hijas directas
    sum_expr_col = lambda cc: "+".join(f"SUM({cc}{a}:{cc}{b})" for (a, b) in child_ranges)
    templates = {
        "E": f"={sum_expr_col('E')}",
        "F": f"={sum_expr_col('F')}",
        "G": f"={sum_expr_col('G')}",
        "H": f"=IFERROR(F{r}/E{r},0)",
        "J": f"={sum_expr_col('J')}",
        "K": f"={sum_expr_col('K')}",
        "L": f"={sum_expr_col('L')}",
        "M": f"={sum_expr_col('M')}",
        "O": f"={sum_expr_col('O')}",
        "P": f"=IFERROR(({sum_expr_col('P')})/COUNT(P{child_ranges[0][0]}:P{child_ranges[-1][1]}),0)",
    }
    return templates[col]


def leading_spaces(s):
    if not isinstance(s, str):
        return -1
    return len(s) - len(s.lstrip(" "))


def detectar_estructura(ws, fila_ini, fila_fin):
    """Recorre columna D y arma el arbol Portafolio->Proyecto->Subpresupuesto->Partida
    usando la sangria (2/4/6 espacios) como nivel."""
    filas = []
    for r in range(fila_ini, fila_fin + 1):
        d = ws.Range(f"D{r}").Value
        if d in (None, ""):
            continue
        filas.append((r, leading_spaces(d), d.strip()))
    return filas


def construir_arbol(filas):
    """filas: lista (row, indent, texto). indent 2=Portafolio/Proyecto (mismo nivel
    visual pero Portafolio es raiz), 4=Subpresupuesto, 6=Partida."""
    portafolio_row = None
    proyectos = []  # cada uno: {row, subpresupuestos:[{row, partidas:[row,...]}]}
    cur_proy = None
    cur_sub = None
    for row, indent, texto in filas:
        if indent == 2 and texto.lower() == "portafolio":
            portafolio_row = row
        elif indent == 2:
            cur_proy = {"row": row, "nombre": texto, "subpresupuestos": []}
            proyectos.append(cur_proy)
            cur_sub = None
        elif indent == 4:
            cur_sub = {"row": row, "nombre": texto, "partidas": []}
            if cur_proy is not None:
                cur_proy["subpresupuestos"].append(cur_sub)
        elif indent == 6:
            if cur_sub is not None:
                cur_sub["partidas"].append(row)
    return portafolio_row, proyectos


def check_a_integridad(ws, portafolio_row, proyectos):
    hallazgos = []

    # Partidas (leaf)
    for proy in proyectos:
        for sub in proy["subpresupuestos"]:
            for r in sub["partidas"]:
                for col in COLS_LEAF:
                    esperado = formula_leaf(col, r, proy["row"])
                    real = ws.Range(f"{col}{r}").Formula
                    if esperado is None:
                        continue
                    if real != esperado:
                        hallazgos.append(
                            f"[PARTIDA] {col}{r}: esperado `{esperado}`  real `{real}`"
                        )
                for col in COLS_LEAF_DIARIAS:
                    esperado = f'=IFERROR(IF(AND({col}$9>=$R{r},{col}$9<=$S{r}),$G{r}/$Q{r},""),"")'
                    real = ws.Range(f"{col}{r}").Formula
                    if real != esperado:
                        hallazgos.append(
                            f"[PARTIDA-DIARIA] {col}{r}: esperado `{esperado}`  real `{real}`"
                        )

    # Subtotales de proyecto
    for proy in proyectos:
        child_ranges = [(s["partidas"][0], s["partidas"][-1]) for s in proy["subpresupuestos"] if s["partidas"]]
        if not child_ranges:
            continue
        r = proy["row"]
        for col in COLS_SUBTOTAL:
            esperado = formula_subtotal(col, r, child_ranges)
            real = ws.Range(f"{col}{r}").Formula
            if real != esperado:
                hallazgos.append(
                    f"[PROYECTO {proy['nombre']}] {col}{r}: esperado `{esperado}`  real `{real}`"
                )

    # Portafolio: solo columnas homogeneas en HH se suman directo (E/F/G de metrado
    # NO se suman aqui a proposito -- mezclar unidades entre partidas no tiene sentido, ver spec)
    if portafolio_row and proyectos:
        proy_rows = [p["row"] for p in proyectos]
        for col in ["K", "L", "M", "O"]:
            esperado = "=" + "+".join(f"{col}{r}" for r in proy_rows)
            real = ws.Range(f"{col}{portafolio_row}").Formula
            if real != esperado:
                hallazgos.append(
                    f"[PORTAFOLIO] {col}{portafolio_row}: esperado `{esperado}`  real `{real}`"
                )
        esperado_j = f"=IFERROR(O{portafolio_row}/K{portafolio_row},0)"
        real_j = ws.Range(f"J{portafolio_row}").Formula
        if real_j != esperado_j:
            hallazgos.append(f"[PORTAFOLIO] J{portafolio_row}: esperado `{esperado_j}`  real `{real_j}`")
        esperado_p = f"=IFERROR(O{portafolio_row}/L{portafolio_row},0)"
        real_p = ws.Range(f"P{portafolio_row}").Formula
        if real_p != esperado_p:
            hallazgos.append(f"[PORTAFOLIO] P{portafolio_row}: esperado `{esperado_p}`  real `{real_p}`")

    return hallazgos


def check_b_traslado(ws_3wla, ws_pr, proyectos):
    hallazgos = []
    sin_fuente = 0
    # PR: WBS en columna A, filas 13 en adelante hasta que A quede vacio
    pr_map = {}
    r = 13
    while True:
        wbs = ws_pr.Range(f"A{r}").Value
        if wbs in (None, ""):
            break
        pr_map[str(wbs).strip()] = r
        r += 1

    for proy in proyectos:
        for sub in proy["subpresupuestos"]:
            for r3 in sub["partidas"]:
                activity_id = ws_3wla.Range(f"C{r3}").Value
                key = str(activity_id).strip() if activity_id is not None else None
                if key not in pr_map:
                    sin_fuente += 1
                    continue
                rpr = pr_map[key]
                pares = [("E", "G"), ("F", "H"), ("N", "D")]
                for col_3wla, col_pr in pares:
                    v3 = ws_3wla.Range(f"{col_3wla}{r3}").Value
                    vpr = ws_pr.Range(f"{col_pr}{rpr}").Value
                    if v3 != vpr:
                        hallazgos.append(
                            f"[TRASLADO] fila {r3} ({key}) col {col_3wla}: "
                            f"3WLA={v3}  PR!{col_pr}{rpr}={vpr}  <- NO COINCIDE"
                        )

    return hallazgos, sin_fuente


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archivo")
    ap.add_argument("--pr", default=None, help="Archivo con la hoja PR de origen (default: mismo archivo)")
    ap.add_argument("--fila-ini", type=int, default=9)
    ap.add_argument("--fila-fin", type=int, default=200)
    args = ap.parse_args()

    path = os.path.abspath(args.archivo)
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    wb = excel.Workbooks.Open(path, ReadOnly=True)
    ws_3wla = wb.Sheets("3WLA")

    pr_path = os.path.abspath(args.pr) if args.pr else None
    wb_pr = wb
    abrio_pr_aparte = bool(pr_path) and pr_path != path
    if abrio_pr_aparte:
        wb_pr = excel.Workbooks.Open(pr_path, ReadOnly=True)
    ws_pr = wb_pr.Sheets("PR")

    filas = detectar_estructura(ws_3wla, args.fila_ini, args.fila_fin)
    portafolio_row, proyectos = construir_arbol(filas)

    print(f"Estructura detectada: Portafolio en fila {portafolio_row}, {len(proyectos)} proyecto(s)")
    for p in proyectos:
        n_partidas = sum(len(s["partidas"]) for s in p["subpresupuestos"])
        print(f"  - {p['nombre']} (fila {p['row']}): {len(p['subpresupuestos'])} subpresupuesto(s), {n_partidas} partida(s)")

    print("\n=== CHECK A: Integridad de formulas ===")
    hallazgos_a = check_a_integridad(ws_3wla, portafolio_row, proyectos)
    if not hallazgos_a:
        print("OK - todas las formulas coinciden con la plantilla esperada.")
    else:
        for h in hallazgos_a:
            print(h)
        print(f"\n{len(hallazgos_a)} desviacion(es) encontrada(s).")

    print("\n=== CHECK B: Traslado de datos (3WLA vs PR) ===")
    hallazgos_b, sin_fuente = check_b_traslado(ws_3wla, ws_pr, proyectos)
    print(f"{sin_fuente} partida(s) de 3WLA sin Activity ID coincidente en PR (esperado si son datos de prueba).")
    if hallazgos_b:
        for h in hallazgos_b:
            print(h)
        print(f"\n{len(hallazgos_b)} desviacion(es) de traslado encontrada(s).")
    else:
        print("Sin desviaciones en las partidas que si tienen fuente en PR.")

    if abrio_pr_aparte:
        wb_pr.Close(SaveChanges=False)
    wb.Close(SaveChanges=False)
    excel.Quit()

    total = len(hallazgos_a) + len(hallazgos_b)
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
