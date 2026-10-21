"""Utilidades comunes de los scripts de la prueba del RDT en PS-0001.

Sin agentes: Playwright (Python) abre Chrome, inicia sesion con una cuenta y
llama a la propia app desde esa sesion. Las credenciales NUNCA van en el
repositorio: se leen de las variables de entorno PG_CORREO y PG_CLAVE.
"""
import json
import os
import sys
from contextlib import contextmanager

from playwright.sync_api import sync_playwright

APP = os.environ.get("PG_APP", "https://py-control-proyectos-web.vercel.app")
PROYECTO_ID = "70c696ae-a810-4e83-b44c-c8dec352c631"  # PS-0001 TECNET


@contextmanager
def sesion(visible=False):
    """Abre el navegador, inicia sesion y entrega la pagina."""
    correo, clave = os.environ.get("PG_CORREO"), os.environ.get("PG_CLAVE")
    if not correo or not clave:
        sys.exit("Faltan las variables de entorno PG_CORREO y PG_CLAVE")
    with sync_playwright() as p:
        navegador = p.chromium.launch(headless=not visible)
        pagina = navegador.new_context(viewport={"width": 1600, "height": 900}).new_page()
        pagina.goto(f"{APP}/login")
        pagina.fill('input[name="correo"]', correo)
        pagina.fill('input[type="password"]', clave)
        pagina.click('button[type="submit"]')
        pagina.wait_for_url(lambda u: "/login" not in u, timeout=30000)
        try:
            yield pagina
        finally:
            navegador.close()


def api(pagina, metodo, ruta, cuerpo=None):
    """Llama a la API de la app con la sesion del navegador. Devuelve [status, json]."""
    return pagina.evaluate(
        """async ([metodo, ruta, cuerpo]) => {
            const r = await fetch(ruta, {method: metodo,
              headers: cuerpo ? {'Content-Type': 'application/json'} : {},
              body: cuerpo ? JSON.stringify(cuerpo) : undefined});
            let j = null; try { j = await r.json(); } catch (e) {}
            return [r.status, j];
        }""",
        [metodo, ruta, cuerpo],
    )


def guardar(nombre, datos):
    carpeta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "salida")
    os.makedirs(carpeta, exist_ok=True)
    ruta = os.path.join(carpeta, nombre)
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=2, ensure_ascii=False)
    return ruta
