#!/usr/bin/env python3
"""Revision completa de la prueba del RDT en PS-0001 con UNA sola cuenta (administrador).

  python scripts/prueba_rdt_ps0001/revisar_todo.py

Usa «Ver como» (POST /api/ver-como) para ver la app con cada uno de los 13 roles, asi que no
necesita mas cuentas. Hace, en orden:
  1. Permisos por rol: llamadas sin efecto (error por fecha futura o por accion invalida) que
     distinguen «no autorizado» (403) de «autorizado» (400); compara con la tabla de permisos.
  2. Avisos: las notificaciones que ve cada rol (validadores deben ver los RDT registrados).
  3. Pruebas negativas (D.8) que la app debe rechazar sin guardar nada.
  4. Rechazar el RDT del 21.10 ya VALIDADO (el PR vuelve a D2), exigir justificacion y revalidarlo.
  5. Restriccion RE-1: recepcionar y atender, y ver el cambio en su pantalla.
Termina siempre devolviendo la vista al rol propio. Resultado: salida/revision-todo.json.
Necesita PG_CORREO y PG_CLAVE (ver comun.py).
"""
import re

from comun import APP, PROYECTO_ID, api, guardar, sesion
from ejecutar import Catalogo, cuerpo_rdt

ROLES = ["administrador", "jefe_de_proyectos", "jefe_de_oficina_tecnica", "supervisor_oficina_tecnica", "planner",
         "supervisor_costos", "jefe_de_costos", "supervisor_operativo", "supervisor_logistica",
         "supervisor_administracion", "supervisor_ssoma", "asistente", "rrhh"]
PUEDEN_CREAR = {"administrador", "jefe_de_proyectos", "jefe_de_oficina_tecnica", "supervisor_operativo"}
PUEDEN_VALIDAR = {"administrador", "jefe_de_proyectos", "jefe_de_oficina_tecnica"}
P = "PRUEBA FUNCIONAL"
resultados = []


def anotar(grupo, caso, esperado, observado, ok=None):
    ok = (esperado == observado) if ok is None else ok
    resultados.append({"grupo": grupo, "caso": caso, "esperado": esperado, "observado": observado, "ok": ok})
    print(f"{'OK   ' if ok else 'FALLA'} [{grupo}] {caso}: esperado {esperado} | observado {observado}")


def como(pg, rol):
    if rol is None:
        return api(pg, "DELETE", "/api/ver-como")[0]
    return api(pg, "POST", "/api/ver-como", {"rol": rol})[0]


def texto(pg, ruta):
    pg.goto(f"{APP}{ruta}", wait_until="networkidle")
    return pg.inner_text("body")


def ev_del_pr(pg):
    t = texto(pg, f"/proyectos/{PROYECTO_ID}/pr")
    fila = next(l for l in t.splitlines() if l.startswith("Total proyecto"))
    celdas = [c.strip() for c in fila.split("\t") if c.strip()]
    return float(re.sub(r"[^0-9.\-]", "", celdas[11]))


def main():
    with sesion() as pg:
        try:
            _, lista = api(pg, "GET", f"/api/rdts/partes?proyectoId={PROYECTO_ID}")
            filas = {f["fecha"]: f for f in lista["filas"] if f["estadoValidacion"] != "RECHAZADO"}
            d3 = filas["2026-10-21"]["id"]
            cat = Catalogo(api(pg, "GET", f"/api/rdts/catalogos?proyectoId={PROYECTO_ID}")[1])

            # 1. Permisos por rol (sin efecto)
            futuro = {"proyectoId": PROYECTO_ID, "fechaLima": "2026-12-31"}
            for rol in ROLES:
                como(pg, rol)
                e1, j1 = api(pg, "POST", "/api/rdts/partes", futuro)
                anotar("permisos", f"{rol} crea RDT", rol in PUEDEN_CREAR, e1 != 403,
                       ok=(e1 != 403) == (rol in PUEDEN_CREAR))
                e2, _ = api(pg, "PATCH", f"/api/rdts/partes/{d3}", {"accion": "NINGUNA"})
                anotar("permisos", f"{rol} valida/rechaza RDT", rol in PUEDEN_VALIDAR, e2 != 403,
                       ok=(e2 != 403) == (rol in PUEDEN_VALIDAR))
                e3, _ = api(pg, "GET", f"/api/rdts/partes?proyectoId={PROYECTO_ID}")
                anotar("permisos", f"{rol} ve los RDT", 200, e3)

            # 2. Avisos: son por usuario (quien actua no recibe el suyo), asi que se ve la app como cada usuario
            pg.goto(f"{APP}/proyectos/{PROYECTO_ID}/pr", wait_until="networkidle")
            usuarios = pg.eval_on_selector_all(
                "select option", "os => os.filter(o => o.value.startsWith('usuario:')).map(o => [o.value.slice(8), o.textContent.trim()])")
            conteo = {}
            for uid, nombre in usuarios:
                api(pg, "POST", "/api/ver-como", {"usuario": uid})
                t = texto(pg, "/notificaciones")
                hoy = [x for x in t.split("Recibida") if "21/10/2026" in x and "RDT registrado para validar" in x]
                conteo[nombre] = len(hoy)
                guardar(f"avisos-usuario-{nombre.replace(' ', '_')}.json", {"texto": t})
            como(pg, None)
            print("Avisos de RDT registrado el 21.10 por usuario:", {k: v for k, v in conteo.items() if v})
            anotar("avisos", "algun validador recibio los avisos de RDT registrado (4 RDT el 21.10)", ">= 1 usuario con >= 3",
                   max(conteo.values(), default=0), ok=max(conteo.values(), default=0) >= 3)

            # 3. Negativos (no deben guardar nada)
            d1 = cuerpo_rdt(cat, "D1")
            e, j = api(pg, "POST", "/api/rdts/partes", d1)
            anotar("negativos", "mismo RDT (OT + fecha + turno)", 409, e)
            d1c = cuerpo_rdt(cat, "D1", correccion=True)
            e, j = api(pg, "POST", "/api/rdts/partes", d1c)
            anotar("negativos", "reemplazar un RDT VALIDADO", 400, e)
            e, j = api(pg, "PATCH", f"/api/rdts/partes/{d3}", {"accion": "RECHAZAR"})
            anotar("negativos", "rechazar sin motivo", 400, e)
            grande = cuerpo_rdt(cat, "D3")
            grande["fechaLima"] = "2026-10-21"
            grande["actividades"][0]["metradoEjecutado"] = 31.0
            e, j = api(pg, "POST", "/api/rdts/partes", grande)
            anotar("negativos", "declarar mas de 30 ml en PT-01", 400, e)
            fut = cuerpo_rdt(cat, "D3")
            fut["fechaLima"] = "2026-12-31"
            e, j = api(pg, "POST", "/api/rdts/partes", fut)
            anotar("negativos", "fecha futura", "FECHA_FUTURA", (j or {}).get("codigo"))
            sin = cuerpo_rdt(cat, "D3")
            sin["fechaLima"] = "2026-10-21"
            sin["personas"][0]["cargo"] = "TOPOGRAFO"
            e, j = api(pg, "POST", "/api/rdts/partes", sin)
            anotar("negativos", "cargo sin tarifa en el presupuesto", "CARGO_SIN_TARIFA", (j or {}).get("codigo"))

            # 4. Rechazar el RDT validado del 21.10, exigir justificacion y revalidar
            ev0 = ev_del_pr(pg)
            e, _ = api(pg, "PATCH", f"/api/rdts/partes/{d3}",
                       {"accion": "RECHAZAR", "motivoRechazo": f"{P}: rechazo de un RDT ya validado"})
            anotar("rechazo validado", "administrador rechaza el RDT validado", 200, e)
            anotar("rechazo validado", "el PR vuelve a D2 (EV 2,978.37)", 2978.37, ev_del_pr(pg),
                   ok=abs(ev_del_pr(pg) - 2978.37) < 0.02)
            e, _ = api(pg, "PATCH", f"/api/rdts/partes/{d3}", {"accion": "VALIDAR"})
            anotar("rechazo validado", "revalidar sin justificacion", 400, e)
            e, _ = api(pg, "PATCH", f"/api/rdts/partes/{d3}",
                       {"accion": "VALIDAR", "motivoValidacion": f"{P}: se revalida tras la prueba"})
            anotar("rechazo validado", "revalidar con justificacion", 200, e)
            anotar("rechazo validado", "el PR vuelve a D3 (EV 4,827.62)", round(ev0, 2), round(ev_del_pr(pg), 2),
                   ok=abs(ev_del_pr(pg) - ev0) < 0.02)

            # 5. Restriccion RE-1: recepcionar, atender y ver el cambio en Informes
            e, j = api(pg, "GET", f"/api/proyectos/{PROYECTO_ID}/restricciones")
            lista = j if isinstance(j, list) else (j or {}).get("restricciones") or []
            re1 = next((r for r in lista if "RE-1" in str(r.get("codigo", ""))), None)
            if not re1:
                anotar("restriccion", "RE-1 existe", True, False)
            else:
                for accion in ("recepcionar", "atender"):
                    e, j = api(pg, "PATCH", f"/api/proyectos/{PROYECTO_ID}/restricciones/{re1['id']}", {"accion": accion})
                    anotar("restriccion", f"{accion} RE-1", "200 (o 409 si ya estaba)", e, ok=e in (200, 409))
                t = texto(pg, f"/proyectos/{PROYECTO_ID}/restricciones")
                anotar("restriccion", "la pantalla Restricciones la muestra Atendida", True, "Atendido (1)" in t)
        finally:
            como(pg, None)

    fallas = [r for r in resultados if not r["ok"]]
    print("Resultado:", guardar("revision-todo.json", resultados))
    print(f"{len(resultados)} comprobaciones, {len(fallas)} con diferencia")


if __name__ == "__main__":
    main()
