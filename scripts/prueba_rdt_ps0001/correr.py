#!/usr/bin/env python3
"""Lanza un script de la prueba con la cuenta guardada en la memoria local (sin teclear claves).

  python scripts/prueba_rdt_ps0001/correr.py ejecutar.py --dias D1,D2,D3
  python scripts/prueba_rdt_ps0001/correr.py limpiar.py --borrar
  python scripts/prueba_rdt_ps0001/correr.py --cuenta "López" ejecutar.py

Lee la fila de la cuenta (por defecto «Victor») de la tabla Cuenta | Correo | Contraseña de
cuentas-prueba.md, en la carpeta de memoria de Claude Code de este usuario, y la pasa al script
como PG_CORREO y PG_CLAVE solo para ese proceso. No imprime ni guarda nada de las credenciales.
"""
import os
import subprocess
import sys

MEMORIA = os.path.expanduser(
    r"~\.claude\projects\D--VICTOR-CLAUDE-CODE-pg-control-proyectos\memory\cuentas-prueba.md")
args = sys.argv[1:]
cuenta = "Victor"
if args[:1] == ["--cuenta"]:
    cuenta, args = args[1], args[2:]
if not args:
    sys.exit("Uso: correr.py [--cuenta NOMBRE] script.py [argumentos]")

correo = clave = None
with open(MEMORIA, encoding="utf-8") as f:
    for linea in f:
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")]
        if len(celdas) >= 3 and celdas[0].startswith(cuenta) and "@" in celdas[1]:
            correo, clave = celdas[1].strip("`"), celdas[2].strip("`")
            break
if not correo or not clave:
    sys.exit(f"No encontre la cuenta «{cuenta}» en la memoria")

print(f"Cuenta: {correo}", flush=True)  # el correo no es secreto; la clave nunca se imprime
aqui = os.path.dirname(os.path.abspath(__file__))
entorno = dict(os.environ, PG_CORREO=correo, PG_CLAVE=clave)
sys.exit(subprocess.call([sys.executable, os.path.join(aqui, args[0]), *args[1:]], env=entorno, cwd=aqui))
