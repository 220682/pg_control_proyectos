# -*- coding: utf-8 -*-
"""
"Crear 3WLA" (nombre de cara al usuario; ver nota mas abajo) — copia datos
reales de una hoja PR hacia un bloque de partidas ya existente en 3WLA,
siguiendo el mapeo de spec-hoja-3wla.md seccion 2.

Nota de nombre: tecnicamente esto es un TRASLADO de datos (no crea filas ni
estructura desde cero, el bloque de 3WLA ya tiene que existir). Se llama
"Crear 3WLA" porque asi lo entiende el planner: es la accion de armar el
3WLA real de la semana a partir del PR. Cualquier interfaz futura (web)
debe usar ese nombre de cara al usuario aunque el codigo siga siendo un
traslado de valores.

Requisito previo (decision de planificacion, NO automatizable — ver spec
seccion 4): cada fila de partida en 3WLA debe tener ya su codigo WBS en la
columna C (Activity ID); ese codigo le dice a este script CUAL partida de
PR va en esa fila. Si el codigo todavia no esta escrito, se puede pasar con
--mapa (mas abajo) para que el script lo escriba, o escribirlo a mano en
Excel antes de correr esto.

Por cada partida de 3WLA cuyo C coincida con un WBS de PR, escribe:
    D <- "      " + PR!B   (Descripcion; se preserva el prefijo de 6
                             espacios que usa revisar_3wla.py para detectar
                             el nivel Partida por sangria — NO escribir la
                             descripcion sin ese prefijo o la fila se vuelve
                             invisible para el chequeo de estructura)
    E <- PR!G   (Metrado contractual)
    F <- PR!H   (Metrado acumulado, avance real)
    N <- PR!D   (Rendimiento HH x partida, VALOR pegado, no formula aqui)
    K <- formula =E{fila}*N{fila}   (HH contractual: se calcula, no se pega)

No toca G,H,I,J,L,M,O,P,V:AA — son formulas locales de 3WLA que ya dependen
de E/F/K/N (ver revisar_3wla.py, formula_leaf).

Uso:
    python trasladar_pr_a_3wla.py "Consolidado proyecto.xlsx" \
        [--pr "OtroLibro.xlsx"] \
        [--fila-ini 12 --fila-fin 27] \
        [--mapa "12:00.01,13:02.01,14:02.02"] \
        [--dry-run]

Si no se pasa --pr, se busca la hoja PR en el mismo libro. Correr
revisar_3wla.py despues de cualquier traslado real para confirmar que no
quedaron desviaciones.
"""
import sys
import os
import argparse
import zipfile
import win32com.client

sys.stdout.reconfigure(encoding="utf-8")

PREFIJO_PARTIDA = "      "  # 6 espacios — nivel Partida, ver detectar_estructura en revisar_3wla.py


def check_lock(path):
    lock = os.path.join(os.path.dirname(path), "~$" + os.path.basename(path))
    if os.path.exists(lock):
        raise SystemExit(
            f"ERROR: existe candado de Excel para este archivo ({lock}).\n"
            "Cierra el archivo en Excel (o espera a que termine de guardarse) "
            "antes de correr el traslado."
        )


def contar_charts(path):
    try:
        with zipfile.ZipFile(path) as z:
            return sum(1 for n in z.namelist() if n.startswith("xl/charts/chart") and n.endswith(".xml"))
    except Exception:
        return None


def leer_pr_map(ws_pr, fila_ini=13):
    pr_map = {}
    r = fila_ini
    while True:
        wbs = ws_pr.Range(f"A{r}").Value
        if wbs in (None, ""):
            break
        pr_map[str(wbs).strip()] = r
        r += 1
    return pr_map


def parse_mapa(s):
    mapa = {}
    for par in s.split(","):
        par = par.strip()
        if not par:
            continue
        fila, codigo = par.split(":")
        mapa[int(fila.strip())] = codigo.strip()
    return mapa


def aplicar_mapa(ws_3wla, mapa):
    for fila, codigo in mapa.items():
        celda = ws_3wla.Range(f"C{fila}")
        celda.NumberFormat = "@"  # evita que "02.01" se convierta en 2.01 (ver feedback-excel-write-method)
        celda.Value = codigo


def trasladar(ws_3wla, ws_pr, fila_ini, fila_fin, dry_run=False):
    pr_map = leer_pr_map(ws_pr)
    escritos = []
    sin_match = []

    for r in range(fila_ini, fila_fin + 1):
        codigo = ws_3wla.Range(f"C{r}").Value
        if codigo in (None, ""):
            continue
        key = str(codigo).strip()
        if key not in pr_map:
            sin_match.append((r, key))
            continue
        rpr = pr_map[key]

        d_val = ws_pr.Range(f"B{rpr}").Value
        e_val = ws_pr.Range(f"G{rpr}").Value
        f_val = ws_pr.Range(f"H{rpr}").Value
        n_val = ws_pr.Range(f"D{rpr}").Value

        if not dry_run:
            d_cell = ws_3wla.Range(f"D{r}")
            d_cell.NumberFormat = "@"
            d_cell.Value = PREFIJO_PARTIDA + str(d_val)
            ws_3wla.Range(f"E{r}").Value = e_val
            ws_3wla.Range(f"F{r}").Value = f_val
            ws_3wla.Range(f"N{r}").Value = n_val
            ws_3wla.Range(f"K{r}").Formula = f"=E{r}*N{r}"

        escritos.append((r, key, d_val, e_val, f_val, n_val))

    return escritos, sin_match


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("archivo")
    ap.add_argument("--pr", default=None, help="Archivo con la hoja PR de origen (default: mismo archivo)")
    ap.add_argument("--fila-ini", type=int, default=9)
    ap.add_argument("--fila-fin", type=int, default=200)
    ap.add_argument("--mapa", default=None, help='fila:codigo separados por coma, ej "12:00.01,13:02.01"')
    ap.add_argument("--dry-run", action="store_true", help="Solo mostrar que se escribiria, sin tocar el archivo")
    args = ap.parse_args()

    path = os.path.abspath(args.archivo)
    pr_path = os.path.abspath(args.pr) if args.pr else None
    if not args.dry_run:
        check_lock(path)  # solo bloquea si se va a escribir; --dry-run puede leer aunque este abierto
        if pr_path:
            check_lock(pr_path)

    charts_antes = contar_charts(path)

    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False
    excel.DisplayAlerts = False

    wb = excel.Workbooks.Open(path, ReadOnly=True if args.dry_run else False)
    ws_3wla = wb.Sheets("3WLA")

    wb_pr = wb
    abrio_pr_aparte = bool(pr_path) and pr_path != path
    if abrio_pr_aparte:
        wb_pr = excel.Workbooks.Open(pr_path, ReadOnly=True)
    ws_pr = wb_pr.Sheets("PR")

    print("=== Crear 3WLA ===")
    if args.mapa:
        mapa = parse_mapa(args.mapa)
        print(f"Escribiendo {len(mapa)} codigo(s) WBS en columna C...")
        if not args.dry_run:
            aplicar_mapa(ws_3wla, mapa)
        for fila, codigo in mapa.items():
            print(f"  C{fila} = {codigo}")

    escritos, sin_match = trasladar(ws_3wla, ws_pr, args.fila_ini, args.fila_fin, dry_run=args.dry_run)

    prefijo = "[DRY-RUN] " if args.dry_run else ""
    print(f"\n{prefijo}Partidas trasladadas: {len(escritos)}")
    for r, key, d, e, f, n in escritos:
        print(f"  fila {r} ({key}): D={d!r} E={e} F={f} N={n}  K=E*N (formula)")

    if sin_match:
        print(f"\n{len(sin_match)} partida(s) con codigo en C sin match en PR (revisar el codigo):")
        for r, key in sin_match:
            print(f"  fila {r}: C={key!r}")

    hubo_escritura = bool(escritos) and not args.dry_run
    if hubo_escritura:
        wb.Save()
        print("\nGuardado.")
    elif args.dry_run:
        print("\n[DRY-RUN] no se guardo nada.")

    if abrio_pr_aparte:
        wb_pr.Close(SaveChanges=False)
    wb.Close(SaveChanges=False)
    excel.Quit()

    if hubo_escritura:
        charts_despues = contar_charts(path)
        print(f"Graficos antes/despues: {charts_antes}/{charts_despues}", end="")
        print("  OK" if charts_antes == charts_despues else "  ALERTA: cambio el numero de graficos")

    if sin_match:
        sys.exit(1)


if __name__ == "__main__":
    main()
