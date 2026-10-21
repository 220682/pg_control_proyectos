#!/usr/bin/env python3
"""Borra los RDT de PS-0001 (prueba). Cuenta con permiso de borrar (administrador o jefe de proyectos).

  python scripts/prueba_rdt_ps0001/limpiar.py            # solo lista
  python scripts/prueba_rdt_ps0001/limpiar.py --borrar   # borra los listados

Necesita las variables de entorno PG_CORREO y PG_CLAVE (ver comun.py).
La app deja una foto de cada RDT en rdt_partes_historial (accion BORRADO) antes de
borrarlo y recalcula el PR. Ademas se guarda aqui un respaldo JSON del listado.
"""
import argparse
import sys

from comun import PROYECTO_ID, api, guardar, sesion


def filas_de(respuesta):
    if isinstance(respuesta, list):
        return respuesta
    return respuesta.get("partes") or respuesta.get("filas") or []


ap = argparse.ArgumentParser()
ap.add_argument("--borrar", action="store_true")
a = ap.parse_args()

with sesion() as pg:
    estado, partes = api(pg, "GET", f"/api/rdts/partes?proyectoId={PROYECTO_ID}")
    if estado != 200:
        sys.exit(f"No se pudo listar: {estado} {partes}")
    filas = filas_de(partes)
    for f in filas:
        print(f["fecha"], f["turno"], f["estadoValidacion"], f["cargadoPor"], f["id"])
    print(f"{len(filas)} RDT en PS-0001")
    print("Respaldo:", guardar("respaldo-rdts-antes-de-borrar.json", filas))
    if a.borrar:
        for f in filas:
            e, j = api(pg, "DELETE", f"/api/rdts/partes/{f['id']}")
            print("borrado" if e == 200 else f"FALLO {e} {j}", f["fecha"], f["id"])
        _, resto = api(pg, "GET", f"/api/rdts/partes?proyectoId={PROYECTO_ID}")
        print(f"Quedan {len(filas_de(resto))} RDT en PS-0001")
