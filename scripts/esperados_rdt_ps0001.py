#!/usr/bin/env python3
"""Valores ESPERADOS de la prueba funcional del RDT en PS-0001 (TECNET).

Se calculan SOLO desde el presupuesto y el cronograma del servicio (no desde
lo que muestra la app). Asi la comparacion detecta errores de la app en vez
de repetirlos. Fuentes: docs/02-trabajo-activo/06-pruebas/02-prueba-rdt-ps0001-plan.md
(secciones C y D) y 04-prueba-rdt-ps0001-v2-guion.md.

Uso:
  python scripts/esperados_rdt_ps0001.py                  # tabla de esperados
  python scripts/esperados_rdt_ps0001.py --json           # lo mismo en JSON
  python scripts/esperados_rdt_ps0001.py --regla-hh antigua   # regla vieja (con HH de la transversal)
  python scripts/esperados_rdt_ps0001.py --comparar observados.json
        # observados.json: {"D1": {"ev": 1284.44, "ac_personal": 681.6, ...}, "D2": {...}}

Un dia que falte en observados.json se omite. Tolerancias: montos y HH 0.02
(centavos de redondeo), indices 0.005, porcentajes 0.02 puntos.
"""
import argparse
import json
import sys

# ---- Linea base (plan 02, seccion C) --------------------------------------
BAC = 39930.56                  # costo directo total
BAC_RESTO = 28441.04            # sin transversales
K = BAC / BAC_RESTO             # EV total = EV_resto * K
VALOR_ML = 26852.68 / 267       # USD por ml de guia (zanja completa 267 ml)
HH_ML = 880.45 / 267            # HH contractuales por ml de guia
PU_31, HH_31 = 311.43, 48.80 / 4   # buzon 3.1 por und
PU_32, HH_32 = 85.66, 21.00 / 4    # buzon 3.2 por und
HH_TRANSVERSAL_11 = 42.0        # HH del APU de la transversal 1.1
AC_TRANSVERSAL_BASE = 9670.42   # (MO + equipo del APU de las transversales)
MATERIALES = 5389.32            # confirmado por Victor (3,570.22 + 1,819.10)

# Programado acumulado al cierre de cada dia (plan 02, C.3), por cronograma.
PV_ACUM = {"D1": 1693.93, "D2": 3387.85, "D3": 5081.78, "D4": 6775.70, "D5": 8513.44}

# ---- Avance por dia (plan 02, D.2 a D.6): ml de guia y und -----------------
AVANCE = {
    "D1": {"pt01": 6.0, "pt02": 0.0, "u31": 1, "u32": 0},
    "D2": {"pt01": 8.9, "pt02": 0.0, "u31": 1, "u32": 0},
    "D3": {"pt01": 10.0, "pt02": 0.0, "u31": 1, "u32": 0},
    "D4": {"pt01": 5.1, "pt02": 4.0, "u31": 1, "u32": 0},
    "D5": {"pt01": 0.0, "pt02": 8.9, "u31": 0, "u32": 4},
}

# ---- Personal: (cargo, personas, horas totales c/u, horas extra c/u, tarifa HH)
# tarifa None = MOI (solo horas, sin costo). Tarifas del APU del DP.
# D4 no lleva TOPOGRAFO: en la v2 un cargo sin tarifa en el presupuesto se
# rechaza al crear el RDT (prueba negativa aparte), no se registra.
OP = ("OPERARIO CIVIL", 2, 8, 0, 13.94)
PERSONAL = {
    "D1": [("CAPATAZ", 1, 8, 0, 15.38), OP, ("OFICIAL CIVIL", 2, 8, 0, 13.37),
           ("OPERADOR DE LINEA AMARILLA", 1, 8, 0, 15.20), ("INGENIERO SSOMA", 1, 2, 0, None)],
    "D2": [("CAPATAZ", 1, 8, 0, 15.38), OP, ("OFICIAL CIVIL", 2, 8, 0, 13.37),
           ("OPERADOR DE LINEA AMARILLA", 1, 8, 0, 15.20), ("INGENIERO SSOMA", 1, 2, 0, None)],
    "D3": [("CAPATAZ", 1, 10, 2, 15.38), ("OPERARIO CIVIL", 2, 10, 2, 13.94),
           ("OFICIAL CIVIL", 2, 10, 2, 13.37), ("OPERADOR DE LINEA AMARILLA", 1, 10, 2, 15.20),
           ("INGENIERO SSOMA", 1, 2, 0, None)],
    "D4": [("CAPATAZ", 1, 8, 0, 15.38), OP, ("OFICIAL CIVIL", 2, 8, 0, 13.37),
           ("OPERADOR DE LINEA AMARILLA", 1, 8, 0, 15.20), ("INGENIERO SSOMA", 1, 2, 0, None)],
    "D5": [("CAPATAZ", 1, 8, 0, 15.38), OP, ("OFICIAL CIVIL", 2, 8, 0, 13.37),
           ("PEON", 2, 8, 0, 11.86), ("OPERADOR DE LINEA AMARILLA", 1, 8, 0, 15.20),
           ("INGENIERO SSOMA", 1, 2, 0, None)],
}

# ---- Equipos: (equipo, HM operativas + stand-by, tarifa HM) -----------------
RETRO, ROTO, CAMION, GRUPO = 38.23, 3.50, 75.00, 9.20
EQUIPOS = {
    "D1": [("RETROEXCAVADORA", 8, RETRO), ("GRUPO ELECTROGENO", 8, GRUPO)],
    "D2": [("RETROEXCAVADORA", 8, RETRO), ("GRUPO ELECTROGENO", 8, GRUPO)],  # 6 + 2 stand-by
    "D3": [("RETROEXCAVADORA", 8, RETRO), ("ROTOMARTILLO", 6, ROTO), ("GRUPO ELECTROGENO", 8, GRUPO)],
    "D4": [("RETROEXCAVADORA", 8, RETRO), ("CAMION BARANDA", 4, CAMION), ("GRUPO ELECTROGENO", 8, GRUPO)],
    "D5": [("RETROEXCAVADORA", 8, RETRO), ("ROTOMARTILLO", 4, ROTO), ("CAMION BARANDA", 6, CAMION)],
}

DIAS = ["D1", "D2", "D3", "D4", "D5"]
FECHAS = {"D1": "2026-10-19", "D2": "2026-10-20", "D3": "2026-10-21", "D4": "2026-10-22", "D5": "2026-10-23"}


def costo_persona(n, h, extra, tarifa):
    """Costo de n personas: tarifa x horas x (1 + 0.25 x extra / total)."""
    return n * h * tarifa * (1 + 0.25 * extra / h)


def calcular(regla_hh):
    """regla_hh: 'nueva' = HH solo de actividades (decidido 2026-10-19);
    'antigua' = suma ademas 42 x p de la transversal 1.1."""
    acum = {"pt01": 0.0, "pt02": 0.0, "u31": 0, "u32": 0}
    ac_pers = ac_eq = hh_reales = 0.0
    salida = {}
    for d in DIAS:
        for clave in acum:
            acum[clave] += AVANCE[d][clave]
        ev_resto = (acum["pt01"] + acum["pt02"]) * VALOR_ML + acum["u31"] * PU_31 + acum["u32"] * PU_32
        p = ev_resto / BAC_RESTO
        for cargo, n, h, ex, tar in PERSONAL[d]:
            if tar is None:
                continue  # MOI: ni costo ni HH reales (solo horas informativas)
            ac_pers += costo_persona(n, h, ex, tar)
            hh_reales += n * h
        for _, hm, tar in EQUIPOS[d]:
            ac_eq += hm * tar
        hh_ganadas = (acum["pt01"] + acum["pt02"]) * HH_ML + acum["u31"] * HH_31 + acum["u32"] * HH_32
        extra_transv = HH_TRANSVERSAL_11 * p if regla_hh == "antigua" else 0.0
        hh_r = hh_reales + extra_transv
        hh_g = hh_ganadas + extra_transv
        ev = ev_resto * K
        ac_tr = AC_TRANSVERSAL_BASE * p
        ac_mat = MATERIALES * p
        ac_total = ac_pers + ac_eq + ac_tr + ac_mat
        pv = PV_ACUM[d]
        salida[d] = {
            "fecha": FECHAS[d],
            "pt01_ml": round(acum["pt01"], 4), "pt02_ml": round(acum["pt02"], 4),
            "u31": acum["u31"], "u32": acum["u32"],
            "ev": round(ev, 2), "pct_fisico": round(p * 100, 2),
            "pv": pv, "pct_programado": round(pv / BAC * 100, 2),
            "sv": round(ev - pv, 2), "spi": round(ev / pv, 3),
            "ac_personal": round(ac_pers, 2), "ac_equipos": round(ac_eq, 2),
            "ac_transversales": round(ac_tr, 2), "ac_materiales": round(ac_mat, 2),
            "ac_total": round(ac_total, 2), "cv": round(ev - ac_total, 2), "cpi": round(ev / ac_total, 3),
            "hh_reales": round(hh_r, 2), "hh_ganadas": round(hh_g, 2), "ip": round(hh_g / hh_r, 3),
        }
    return salida


TOL = {"montos": 0.02, "indices": 0.005, "pct": 0.02}
TIPO = {"spi": "indices", "cpi": "indices", "ip": "indices", "pct_fisico": "pct", "pct_programado": "pct"}


def comparar(esperado, observado):
    fallas = 0
    for d, vals in observado.items():
        if d not in esperado:
            print(f"{d}: dia desconocido, se omite")
            continue
        for clave, valor in vals.items():
            if clave not in esperado[d] or clave == "fecha":
                continue
            e = esperado[d][clave]
            tol = TOL[TIPO.get(clave, "montos")]
            ok = abs(valor - e) <= tol + 1e-9
            fallas += 0 if ok else 1
            print(f"{'OK   ' if ok else 'FALLA'} {d} {clave:<17} esperado {e:>10}  observado {valor:>10}")
    return fallas


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--regla-hh", choices=["nueva", "antigua"], default="nueva")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--comparar", metavar="OBSERVADOS.json")
    a = ap.parse_args()
    esperado = calcular(a.regla_hh)
    if a.comparar:
        with open(a.comparar, encoding="utf-8") as f:
            sys.exit(1 if comparar(esperado, json.load(f)) else 0)
    if a.json:
        print(json.dumps(esperado, indent=2, ensure_ascii=False))
        return
    claves = [k for k in esperado["D1"] if k != "fecha"]
    print(f"Regla de HH: {a.regla_hh}. Materiales = {MATERIALES}. Acumulado tras validar cada dia.\n")
    print(f"{'dato':<17}" + "".join(f"{d + ' ' + FECHAS[d][5:]:>14}" for d in DIAS))
    for c in claves:
        print(f"{c:<17}" + "".join(f"{esperado[d][c]:>14}" for d in DIAS))


if __name__ == "__main__":
    main()
