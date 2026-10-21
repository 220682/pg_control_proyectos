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
for d, (mat, m) in extra.items():
    print(f"INFO {d} materiales observado {mat}  (M implicito {m:.2f}; A=5307.00, B=3570.22, suma APU=5389.32)")
print(f"{fallas} diferencia(s)")
