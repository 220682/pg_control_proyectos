#!/usr/bin/env python3
"""Compara lo que mostro el PR tras validar cada dia (salida/pantalla-Dn-pr.json) con los esperados.

  python scripts/prueba_rdt_ps0001/comparar.py

Los esperados salen de scripts/esperados_rdt_ps0001.py (presupuesto y cronograma, no de la app).
Materiales no se compara con A/B: se informa el monto observado y el M implicito (monto / % fisico).
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, ".."))
import esperados_rdt_ps0001 as esp  # noqa: E402


def num(s):
    return float(re.sub(r"[^0-9.\-]", "", s))


def leer(texto):
    fila = next(l for l in texto.splitlines() if l.startswith("Total proyecto"))
    t = [c.strip() for c in fila.split("\t") if c.strip()]
    r = {"ev": num(t[11]), "pv": num(t[10]), "sv": num(t[13]), "spi": num(t[15]),
         "hh_reales": num(t[7]), "hh_ganadas": num(t[17]), "ip": num(t[18])}
    for clave, etq in (("ac_personal", "Personal"), ("ac_equipos", "Equipos"),
                       ("ac_transversales", "Transversales (prorrata)"), ("ac_materiales", "Materiales")):
        m = re.search(r"^" + re.escape(etq) + r" US\$ ([\d,.\-]+)$", texto, re.M)
        r[clave] = num(m.group(1)) if m else None
    return r


def cargar(d, nombre):
    ruta = os.path.join(AQUI, "salida", f"pantalla-{d}-{nombre}.json")
    return json.load(open(ruta, encoding="utf-8"))["texto"] if os.path.exists(ruta) else None


def tras(t, etiqueta):
    """Primer monto US$ que aparece despues de una etiqueta del Dashboard."""
    m = re.search(re.escape(etiqueta) + r"\s+US\$ ([\d,.\-]+)", t)
    return num(m.group(1)) if m else None


def leer_dashboard(t):
    r = {"ev": tras(t, "EV\n\nUS$") if False else tras(t, "Valor ganado al"), "ac": tras(t, "Costo real acumulado")}
    ip = re.search(r"IP .. .NDICE DE PRODUCTIVIDAD\s+([\d.]+)", t, re.I)
    hh = re.search(r"HH ganadas ([\d,.]+)\s+HH reales ([\d,.]+)", t)
    r["ip"] = num(ip.group(1)) if ip else None
    r["hh_ganadas"], r["hh_reales"] = (num(hh.group(1)), num(hh.group(2))) if hh else (None, None)
    return r


def leer_curva(t):
    m = re.search(r"Semana \d+ . [\d-]+\s+PV\s+US\$ ([\d,.]+)\s+EV\s+US\$ ([\d,.]+)\s+AC\s+US\$ ([\d,.]+)", t)
    return {"pv": num(m.group(1)), "ev": num(m.group(2)), "ac": num(m.group(3))} if m else {}


esperado = esp.calcular("nueva")
observado, extra = {}, {}
for d in esp.DIAS:
    ruta = os.path.join(AQUI, "salida", f"pantalla-{d}-pr.json")
    if not os.path.exists(ruta):
        continue
    r = leer(json.load(open(ruta, encoding="utf-8"))["texto"])
    mat = r.pop("ac_materiales")
    p = esperado[d]["pct_fisico"] / 100
    extra[d] = (mat, mat / p if mat is not None and p else None)
    # PV, SV y SPI del PR son "al corte" (fecha de la lectura): solo son comparables el dia en que se lee.
    # La prueba lee varios dias seguidos, asi que se omiten en los dias anteriores al ultimo leido.
    observado[d] = {k: v for k, v in r.items() if v is not None}
    corte = re.search(r"fecha de corte (\d\d)-(\d\d)-(\d{4})", json.load(open(ruta, encoding="utf-8"))["texto"])
    if corte and f"{corte[3]}-{corte[2]}-{corte[1]}" != esperado[d]["fecha"]:
        for k in ("pv", "sv", "spi"):
            observado[d].pop(k, None)
fallas = esp.comparar(esperado, observado)
# Dashboard y Curva S del dia: deben mostrar lo mismo que el PR (misma lectura, otra pantalla).
for d in observado:
    pr = observado[d]
    comp = []
    t = cargar(d, "dashboard")
    if t:
        dash = leer_dashboard(t)
        comp += [("dashboard", k, dash[k], pr[k], 0.5 if k.startswith("hh") else 0.02 if k != "ip" else 0.01)
                 for k in ("ev", "hh_ganadas", "hh_reales", "ip") if dash.get(k) is not None and k in pr]
    t = cargar(d, "curva-s")
    if t:
        cur = leer_curva(t)
        comp += [("curva-s", k, cur[k], pr[k], 0.02) for k in ("ev",) if k in cur and k in pr]
        if "ac" in cur and None not in (pr.get("ac_personal"), pr.get("ac_equipos"), pr.get("ac_transversales")):
            comp.append(("curva-s", "ac vs pr", cur["ac"], round(pr["ac_personal"] + pr["ac_equipos"] + pr["ac_transversales"] + extra[d][0], 2), 0.02))
    for pantalla, clave, valor, ref, tol in comp:
        ok = abs(valor - ref) <= tol + 1e-9
        fallas += 0 if ok else 1
        print(f"{'OK   ' if ok else 'FALLA'} {d} {pantalla:<9} {clave:<10} pantalla {valor:>10}  PR {ref:>10}")
for d, (mat, m) in extra.items():
    print(f"INFO {d} materiales observado {mat}  (M implicito {m:.2f}; A=5307.00, B=3570.22, suma APU=5389.32)")
print(f"{fallas} diferencia(s)")
