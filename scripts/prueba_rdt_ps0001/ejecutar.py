#!/usr/bin/env python3
"""Ejecuta la prueba del RDT en PS-0001 (guion v2, dias D1 a D5) por navegador, sin agentes.

  python scripts/prueba_rdt_ps0001/ejecutar.py                 # todos los dias cuya fecha ya llego
  python scripts/prueba_rdt_ps0001/ejecutar.py --dias D1,D2    # solo esos dias
  python scripts/prueba_rdt_ps0001/ejecutar.py --solo-leer     # no crea nada: lee PR y Dashboard de hoy

Por cada dia: crea el RDT (POST), lo valida (PATCH) y lee las pantallas del PR y del Dashboard,
guardando su texto en salida/. D2 crea primero la version con error (9.5 ml), la rechaza y
la corrige. Un dia con fecha futura se omite (la app bloquea fecha futura).
El calculo de los esperados vive aparte (scripts/esperados_rdt_ps0001.py) y no mira la app.
Necesita PG_CORREO y PG_CLAVE (ver comun.py); la cuenta debe poder crear, validar y rechazar.
"""
import argparse
import datetime
import re
import sys

from comun import PROYECTO_ID, api, guardar, sesion, APP

# (cargo, personas, [h act1, h act2, h act3], horas extra por persona)
OP, OF = "OPERARIO CIVIL", "OFICIAL CIVIL"
PERSONAL = {
    "D1": [("CAPATAZ", 1, [7, 0, 1], 0), (OP, 2, [7, 0, 1], 0), (OF, 2, [3, 4, 1], 0),
           ("OPERADOR DE LINEA AMARILLA", 1, [7, 0, 1], 0), ("INGENIERO SSOMA", 1, [1, 0, 1], 0)],
    "D2": [("CAPATAZ", 1, [8, 0, 0], 0), (OP, 2, [5, 3, 0], 0), (OF, 2, [8, 0, 0], 0),
           ("OPERADOR DE LINEA AMARILLA", 1, [8, 0, 0], 0), ("INGENIERO SSOMA", 1, [2, 0, 0], 0)],
    "D3": [("CAPATAZ", 1, [9, 0, 1], 2), (OP, 2, [6, 3, 1], 2), (OF, 2, [6, 3, 1], 2),
           ("OPERADOR DE LINEA AMARILLA", 1, [9, 0, 1], 2), ("INGENIERO SSOMA", 1, [2, 0, 0], 0)],
    "D4": [("CAPATAZ", 1, [3, 4, 1], 0), (OP, 2, [3, 3, 2], 0), (OF, 2, [2, 3, 3], 0),
           ("OPERADOR DE LINEA AMARILLA", 1, [4, 4, 0], 0), ("TOPOGRAFO", 1, [2, 2, 0], 0),
           ("INGENIERO SSOMA", 1, [1, 1, 0], 0)],
    "D5": [("CAPATAZ", 1, [6, 2, 0], 0), (OP, 2, [6, 2, 0], 0), (OF, 2, [6, 2, 0], 0),
           ("PEON", 2, [8, 0, 0], 0), ("OPERADOR DE LINEA AMARILLA", 1, [8, 0, 0], 0),
           ("INGENIERO SSOMA", 1, [2, 0, 0], 0)],
}
# (texto del catalogo, actividad que lo usa, HM operativas, HM stand-by)
EQUIPOS = {
    "D1": [("RETROEXCAVADORA JOHN DEERE 310G", 8, 0), ("GRUPO ELECTROGENO 11KW", 8, 0)],
    "D2": [("RETROEXCAVADORA JOHN DEERE 310G", 6, 2), ("GRUPO ELECTROGENO 11KW", 8, 0)],
    "D3": [("RETROEXCAVADORA JOHN DEERE 310G", 8, 0), ("ROTOMARTILLO", 6, 0), ("GRUPO ELECTROGENO 11KW", 8, 0)],
    "D4": [("RETROEXCAVADORA JOHN DEERE 310G", 8, 0), ("CAMION BARANDA", 4, 0), ("GRUPO ELECTROGENO 11KW", 8, 0)],
    "D5": [("RETROEXCAVADORA JOHN DEERE 310G", 8, 0), ("ROTOMARTILLO", 4, 0), ("CAMION BARANDA", 6, 0)],
}
FECHAS = {"D1": "2026-10-19", "D2": "2026-10-20", "D3": "2026-10-21", "D4": "2026-10-22", "D5": "2026-10-23"}
UBICACION = {"PT-01": "Lingo 1 y vestuarios", "PT-02": "Vestidores y lingo oxidos"}
P = "PRUEBA FUNCIONAL"


def actividades(dia, ml_t1=None):
    """Lista de actividades del dia. Cada una: (ta, clave, descripcion, prog, ejec, cnc, restriccion)."""
    if dia == "D1":
        return [("D", "PT-01", "Perfilado y nivelacion PT-01", 8.9, 6.0, "CNC", None),
                ("D", "3.1", "Suministro de buzon", 1, 1, None, None),
                ("C", "PT-01", f"{P} charla de seguridad y reunion de inicio", None, None, None, None)]
    if dia == "D2":
        return [("D", "PT-01", "Perfilado y nivelacion PT-01", 8.9, ml_t1 or 8.9, None, None),
                ("D", "3.1", "Suministro de buzon", 1, 1, None, None)]
    if dia == "D3":
        return [("D", "PT-01", "Perfilado y nivelacion PT-01", 8.9, 10.0, None,
                 f"{P}: falta liberacion del frente de lingo 1 para continuar perfilado"),
                ("D", "3.1", "Suministro de buzon", 1, 1, None, None),
                ("NC", "PT-01", f"{P} espera por liberacion de frente", None, None, None, None)]
    if dia == "D4":
        return [("D", "PT-01", "Perfilado y nivelacion PT-01", 3.3, 5.1, None, None),
                ("D", "PT-02", "Perfilado y nivelacion PT-02", 5.6, 4.0, "CNC", None),
                ("D", "3.1", "Suministro de buzon", 1, 1, None, None)]
    return [("D", "PT-02", "Perfilado y nivelacion PT-02", 8.9, 8.9, None, None),
            ("D", "3.2", "Instalacion de buzon", 4, 4, None, None)]


OBS = {"D1": f"{P} D1: avance parcial por inicio de frente.", "D2": f"{P} D2: corregido tras rechazo.",
       "D3": f"{P} D3: sobreproduccion de 1.1 ml sobre lo programado.",
       "D4": f"{P} D4: cierre de PT-01 y de 3.1.", "D5": f"{P} D5: cierre de 3.2."}


class Catalogo:
    def __init__(self, cat):
        self.cat = cat
        self.lineas = cat["lineasPlanMaestro"]

    def clave(self, ref):
        """ref: 'PT-01' (guia 2.3 del paquete), 'PT-02' o '3.1'/'3.2' (partida directa)."""
        if ref.startswith("PT-"):
            c = [l for l in self.lineas if l.get("paqueteCodigo") == ref and l["wbs"] == "2.3"]
        else:
            c = [l for l in self.lineas if not l.get("paqueteId") and l["wbs"] == ref]
        if not c:
            sys.exit(f"No hay linea del Plan Maestro para {ref}. Claves: "
                     f"{[(l.get('paqueteCodigo'), l['wbs']) for l in self.lineas][:20]}")
        return c[0]

    def personas(self, cargo, n, usadas):
        """n personas distintas del catalogo con ese cargo."""
        lote = [p for p in self.cat["personal"]
                if (p.get("cargo") or "").strip().upper() == cargo and p["id"] not in usadas][:n]
        usadas.update(p["id"] for p in lote)
        # Sin personas del catalogo para ese cargo: filas libres (sin DNI) con nombre PRUEBA FUNCIONAL.
        while len(lote) < n:
            lote.append({"id": None, "dni": "", "nombre": f"{P} {cargo} {len(lote) + 1}", "especialidad": None})
        return lote

    def equipo(self, nombre):
        e = [q for q in self.cat["equipos"] if q["descripcion"].strip().upper() == nombre]
        if not e:
            sys.exit(f"Equipo no encontrado en el catalogo: {nombre}")
        return e[0]


def cuerpo_rdt(cat, dia, ml_t1=None, correccion=False):
    acts = actividades(dia, ml_t1)
    lista = []
    for i, (ta, ref, desc, prog, ejec, cnc, restr) in enumerate(acts, 1):
        lin = cat.clave(ref)
        lista.append({
            "orden": i, "descripcion": desc, "wbs": lin["wbs"], "ta": ta, "unidad": lin["unidad"] if ta == "D" else None,
            "metradoProgramado": prog, "metradoEjecutado": ejec,
            "restricciones": restr, "restriccionFotoIds": [], "cnc": (cat.cat["causasCnc"][0] if cnc else None),
            "claveReporte": lin["claveReporte"],
        })
    usadas, personas, orden = set(), [], 0
    for cargo, n, horas, extra in PERSONAL[dia]:
        for p in cat.personas(cargo, n, usadas):
            orden += 1
            personas.append({
                "orden": orden, "personalId": p["id"], "dni": p["dni"], "nombre": p["nombre"], "cargo": cargo,
                "especialidad": p.get("especialidad"), "horasExtra": extra,
                "horas": [{"ordenActividad": k + 1, "horas": h} for k, h in enumerate(horas[:len(acts)]) if h],
            })
    equipos = []
    for i, (nombre, hm, sb) in enumerate(EQUIPOS[dia], 1):
        e = cat.equipo(nombre)
        equipos.append({"orden": i, "equipoId": e["id"], "descripcion": e["descripcion"], "wbs": None,
                        "horas": hm, "horasStandby": sb, "estado": "OPERATIVO"})
    c = {"proyectoId": PROYECTO_ID, "fechaLima": FECHAS[dia], "turno": "DIA", "especialidad": "Civil",
         "semana": 1, "ubicacion": UBICACION["PT-01" if dia != "D5" else "PT-02"], "observaciones": OBS[dia],
         "jornadaHoras": 8 if dia != "D3" else 10, "actividades": lista, "personas": personas, "equipos": equipos,
         "inasistencias": []}
    pers = cat.cat["personal"]
    if dia == "D2" and not correccion:
        c["observaciones"] = f"{P} D2 v1: metrado con error, rechazar"
    if correccion:
        c.update(reemplazar=True, motivoCorreccion=f"{P}: metrado corregido a 8.9 ml")
    if dia == "D2":
        ausente = pers[-1] if pers else {"id": None, "dni": "", "nombre": f"{P} ausente"}
        c["inasistencias"] = [{"personalId": ausente["id"], "nombre": ausente["nombre"], "dni": ausente["dni"],
                               "motivo": "Falta", "nota": f"{P}: inasistencia informativa"}] if correccion else []
    return c


def leer_pantallas(pg, dia):
    """Guarda el texto del PR y del Dashboard tras validar el dia."""
    textos = {}
    for nombre in ("pr", "dashboard", "curva-s"):
        pg.goto(f"{APP}/proyectos/{PROYECTO_ID}/{nombre}", wait_until="networkidle")
        textos[nombre] = pg.inner_text("body")
        guardar(f"pantalla-{dia}-{nombre}.txt".replace(".txt", ".json"), {"texto": textos[nombre]})
    return textos


def numeros_cerca(texto, etiqueta):
    """Primeros numeros que aparecen tras una etiqueta (ayuda a la lectura; se revisa a ojo)."""
    m = re.search(re.escape(etiqueta) + r"[^0-9\-]{0,40}(-?[0-9][0-9.,]*)", texto, re.I)
    return m.group(1) if m else None


ap = argparse.ArgumentParser()
ap.add_argument("--dias", default="D1,D2,D3,D4,D5")
ap.add_argument("--solo-leer", action="store_true")
a = ap.parse_args()
hoy = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=-5))).date().isoformat()
dias = [d for d in a.dias.split(",") if d in FECHAS]

with sesion() as pg:
    e, cat = api(pg, "GET", f"/api/rdts/catalogos?proyectoId={PROYECTO_ID}")
    if e != 200:
        sys.exit(f"Catalogos: {e} {cat}")
    cat = Catalogo(cat)
    print("Personal del catalogo:", len(cat.cat["personal"]), "- cargos:",
          sorted({(p.get("cargo") or "").strip() for p in cat.cat["personal"]}))
    guardar("catalogo-claves.json", [(l.get("paqueteCodigo"), l["wbs"], l["claveReporte"]) for l in cat.lineas])
    resultado = {}
    for dia in dias:
        if a.solo_leer:
            resultado[dia] = leer_pantallas(pg, "hoy")
            break
        if FECHAS[dia] > hoy:
            print(f"{dia} {FECHAS[dia]}: fecha futura, se omite")
            continue
        if dia == "D2":
            e, j = api(pg, "POST", "/api/rdts/partes", cuerpo_rdt(cat, dia, ml_t1=9.5))
            print(dia, "crear v1", e, j)
            if e != 200:
                sys.exit("D2 v1 fallo")
            e2, j2 = api(pg, "PATCH", f"/api/rdts/partes/{j['id']}",
                         {"accion": "RECHAZAR", "motivoRechazo": f"{P}: el metrado de la guia no coincide con el control de campo; corregir a 8.9 ml"})
            print(dia, "rechazar", e2, j2)
            e, j = api(pg, "POST", "/api/rdts/partes", cuerpo_rdt(cat, dia, correccion=True))
            print(dia, "corregir", e, j)
        else:
            e, j = api(pg, "POST", "/api/rdts/partes", cuerpo_rdt(cat, dia))
            print(dia, "crear", e, j)
        if e != 200:
            sys.exit(f"{dia}: no se pudo crear. Se detiene.")
        e, j2 = api(pg, "PATCH", f"/api/rdts/partes/{j['id']}", {"accion": "VALIDAR"})
        print(dia, "validar", e, j2)
        if e != 200:
            sys.exit(f"{dia}: no se pudo validar. Se detiene.")
        resultado[dia] = leer_pantallas(pg, dia)
        print(f"{dia}: pantallas guardadas en salida/")
    print("Listo. Resultados en", guardar("resultado-ejecucion.json", {d: list(v) for d, v in resultado.items()}))
