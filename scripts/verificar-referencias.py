"""Verifica que ningun documento quede suelto y que ningun enlace este roto.

Uso:
  python scripts/verificar-referencias.py                  revisa el nucleo de la politica
  python scripts/verificar-referencias.py docs/02-trabajo-activo docs/04-flujos-de-negocio
                                                           revisa solo las carpetas indicadas (las que toco un plan)

Que comprueba, sobre cada archivo .md del alcance:
  1. HUERFANO: ningun otro .md lo menciona (por enlace o por su nombre entre comillas invertidas).
  2. ENLACE ROTO: un enlace relativo [texto](ruta) cuyo destino no existe.
  3. MENCION SIN ARCHIVO: un nombre `algo.md` entre comillas invertidas que no existe en el repositorio.

Termina con codigo 0 si no hay huerfanos ni enlaces rotos; con 1 si los hay.
Solo lee archivos; no modifica nada. Ver docs/00-estandar-agentes/02-roles-y-delegacion.md (Documentador).
"""
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXCLUIR = ('.git', 'node_modules', '.worktrees', '__pycache__')
NUCLEO = ['AGENTS.md', 'README.md', 'docs/README.md', 'docs/00-estandar-agentes', 'docs/01-contexto-repositorio',
          'docs/02-trabajo-activo/README.md', 'docs/02-trabajo-activo/05-eficiencia', '.claude/skills']
ENLACE = re.compile(r'\[[^\]]*\]\(([^)\s]+)(?:\s+"[^"]*")?\)')
MENCION = re.compile(r'`([A-Za-z0-9_.\-/]+\.md)`')


def todos_los_md():
    res = []
    for d, ds, fs in os.walk(RAIZ):
        ds[:] = [x for x in ds if x not in EXCLUIR]
        for f in fs:
            if f.lower().endswith('.md'):
                res.append(os.path.join(d, f))
    return res


def leer(p):
    try:
        return open(p, encoding='utf-8').read()
    except Exception:
        return ''


def expandir(rutas):
    res = []
    for r in rutas:
        p = os.path.normpath(os.path.join(RAIZ, r))
        if os.path.isfile(p):
            res.append(p)
        elif os.path.isdir(p):
            for d, ds, fs in os.walk(p):
                ds[:] = [x for x in ds if x not in EXCLUIR]
                res += [os.path.join(d, f) for f in fs if f.lower().endswith('.md')]
    return sorted({os.path.normpath(x) for x in res})


def rel(p):
    return os.path.relpath(p, RAIZ).replace(os.sep, '/')


def main():
    rutas = sys.argv[1:] or NUCLEO
    alcance = expandir(rutas)
    md = todos_los_md()
    textos = {p: leer(p) for p in md}
    nombres = {os.path.basename(p).lower() for p in md}
    huerfanos, rotos, menciones = [], [], []

    for f in alcance:
        base = os.path.basename(f)
        clave = base
        if base.upper() == 'SKILL.MD':
            clave = os.path.basename(os.path.dirname(f))
        es_indice = base.upper() == 'README.MD' or base.endswith('00-indice.md')
        # 1. huerfano: otro .md lo menciona por nombre o por ruta relativa
        if not es_indice:
            r = rel(f)
            citado = any(o != f and (clave in t or r in t) for o, t in textos.items())
            if not citado:
                huerfanos.append(r)
        # 2 y 3. enlaces rotos y menciones sin archivo
        t = textos.get(f, '')
        for m in ENLACE.finditer(t):
            destino = m.group(1)
            if re.match(r'^(https?:|mailto:|#)', destino):
                continue
            destino = destino.split('#')[0].replace('%20', ' ')
            if destino and not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), destino))):
                rotos.append((rel(f), m.group(1)))
        for m in MENCION.finditer(t):
            nombre = os.path.basename(m.group(1)).lower()
            if nombre not in nombres and '<' not in m.group(1) and 'YYYY' not in m.group(1):
                menciones.append((rel(f), m.group(1)))

    print(f'Archivos revisados: {len(alcance)}')
    print(f'\nHUÉRFANOS ({len(huerfanos)}): nadie los menciona')
    for h in huerfanos:
        print('  ', h)
    print(f'\nENLACES ROTOS ({len(rotos)})')
    for a, b in rotos:
        print(f'   {a} -> {b}')
    print(f'\nMENCIONES SIN ARCHIVO ({len(menciones)}): nombres entre comillas invertidas que no existen')
    for a, b in sorted(set(menciones)):
        print(f'   {a} -> {b}')
    sys.exit(1 if (huerfanos or rotos) else 0)


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    main()
