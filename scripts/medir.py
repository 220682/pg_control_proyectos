"""Mide sesiones de agentes de Claude Code: llamadas, tokens por tipo, modelo y contexto maximo.

Uso:
  python scripts/medir.py [N]                       las N sesiones mas recientes (por defecto 8)
  python scripts/medir.py --resumen                 agrupa por tanda, por Worker, por rol y total
  python scripts/medir.py --resumen --desde 2026-09-30 [--hasta 2026-10-05]

Solo lee los registros locales de sesion; no usa red, no cuesta tokens y no modifica nada.
Para agrupar bien, cada subagente se lanza con una descripcion «<Rol N> · <tanda>»
(por ejemplo «Worker 2 · F2-A»). Roles reconocidos: Worker N, Worker git, Planner,
Documentador, Auditor, Analista. Una sesion sin descripcion se cuenta como sesion principal
(la del Orquestador).

«Contexto max.» es el tamano de la sesion y NO se suma. Entrada, cache creada, cache leida
y salida SI se suman.

Ver docs/00-estandar-agentes/08-medicion-y-relevo.md y docs/01-contexto-repositorio/09-medicion-y-modelos.md.
"""
import argparse
import datetime
import glob
import json
import os
import re

CARPETAS = ('D--VICTOR-CLAUDE-CODE-pg-control-proyectos', 'D--VICTOR-CLAUDE-CODE-py-control-proyectos-web')
ETIQUETA = re.compile(r'^\s*(Worker git|Worker \d+|Worker|Planner|Documentador|Auditor|Analista)\b\s*(?:[·\-:]\s*)?(.*)$', re.I)


def leer_sesion(ruta):
    vistos, usos = set(), set()
    s = dict(llamadas=0, entrada=0, creada=0, cache=0, salida=0, ctx=0, modelos=set())
    for linea in open(ruta, encoding='utf-8'):
        try:
            o = json.loads(linea)
        except Exception:
            continue
        if o.get('type') != 'assistant':
            continue
        m = o.get('message') or {}
        if isinstance(m.get('content'), list):
            for b in m['content']:
                if isinstance(b, dict) and b.get('type') == 'tool_use':
                    usos.add(b.get('id'))
        u = m.get('usage')
        if not u:
            continue
        clave = m.get('id') or o.get('uuid')
        if clave in vistos:
            continue
        vistos.add(clave)
        s['llamadas'] += 1
        s['entrada'] += u.get('input_tokens', 0)
        s['creada'] += u.get('cache_creation_input_tokens', 0)
        s['cache'] += u.get('cache_read_input_tokens', 0)
        s['salida'] += u.get('output_tokens', 0)
        s['ctx'] = max(s['ctx'], u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0))
        if m.get('model'):
            s['modelos'].add(m['model'])
    s['herramientas'] = len(usos)
    return s


def descripcion(ruta):
    meta = ruta[:-6] + '.meta.json'
    if os.path.exists(meta):
        try:
            return json.load(open(meta, encoding='utf-8')).get('description', '') or ''
        except Exception:
            return ''
    return ''


def clasificar(desc, es_sub):
    """Devuelve (worker_o_rol, rol, tanda)."""
    if not es_sub:
        return ('Sesión principal', 'Sesión principal (Orquestador)', '')
    m = ETIQUETA.match(desc or '')
    if m:
        quien = m.group(1).strip().title().replace('Worker Git', 'Worker git')
        rol = 'Worker' if re.match(r'worker \d+', quien, re.I) else quien
        return (quien, rol, (m.group(2) or '').strip())
    return ('Subagente sin etiqueta', 'Subagente sin etiqueta', (desc or '')[:40])


def fmt(n):
    return f'{n / 1e6:.2f}M' if n >= 1e6 else f'{n / 1e3:.0f}k'


def main():
    ap = argparse.ArgumentParser(description='Mide sesiones de agentes.')
    ap.add_argument('n', nargs='?', type=int, default=8)
    ap.add_argument('--resumen', action='store_true')
    ap.add_argument('--desde')
    ap.add_argument('--hasta')
    a = ap.parse_args()

    raiz = os.path.expandvars(r'%USERPROFILE%\.claude\projects')
    archivos = []
    for c in CARPETAS:
        base = os.path.join(raiz, c)
        if os.path.isdir(base):
            archivos += glob.glob(base + '/**/*.jsonl', recursive=True)
    if a.desde:
        t0 = datetime.datetime.strptime(a.desde, '%Y-%m-%d').timestamp()
        archivos = [f for f in archivos if os.path.getmtime(f) >= t0]
    if a.hasta:
        t1 = datetime.datetime.strptime(a.hasta, '%Y-%m-%d').timestamp() + 86400
        archivos = [f for f in archivos if os.path.getmtime(f) <= t1]
    archivos = sorted(archivos, key=os.path.getmtime)
    if not a.resumen:
        archivos = archivos[-a.n:]

    filas = []
    for f in archivos:
        s = leer_sesion(f)
        if s['llamadas'] == 0:
            continue
        d = descripcion(f)
        es_sub = f'{os.sep}subagents{os.sep}' in f or '/subagents/' in f
        quien, rol, tanda = clasificar(d, es_sub)
        s.update(archivo=os.path.basename(f)[:22], fecha=datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%m-%d %H:%M'),
                 desc=d, quien=quien, rol=rol, tanda=tanda)
        filas.append(s)

    cab = f"{'sesión':22} {'fecha':11} {'quién':22} {'tanda':14} {'modelo':18} {'llam':>5} {'entr':>7} {'creada':>7} {'caché':>8} {'sal':>7} {'ctx máx':>8}"
    print(cab)
    for s in filas:
        modelo = ','.join(sorted(m.replace('claude-', '') for m in s['modelos']))[:18]
        print(f"{s['archivo']:22} {s['fecha']:11} {s['quien'][:22]:22} {s['tanda'][:14]:14} {modelo:18} {s['llamadas']:>5} {fmt(s['entrada']):>7} {fmt(s['creada']):>7} {fmt(s['cache']):>8} {fmt(s['salida']):>7} {fmt(s['ctx']):>8}")

    if not a.resumen:
        return

    def sumar(clave):
        g = {}
        for s in filas:
            x = g.setdefault(s[clave], dict(ses=0, llamadas=0, entrada=0, creada=0, cache=0, salida=0, ctx=0, tandas=set()))
            x['ses'] += 1
            for k in ('llamadas', 'entrada', 'creada', 'cache', 'salida'):
                x[k] += s[k]
            x['ctx'] = max(x['ctx'], s['ctx'])
            if s['tanda']:
                x['tandas'].add(s['tanda'])
        return g

    for titulo, clave in (('POR WORKER O SESIÓN (suma de sus tandas)', 'quien'), ('POR ROL', 'rol')):
        print(f'\n{titulo}')
        print(f"{'':30} {'ses':>4} {'llam':>6} {'entr':>8} {'creada':>8} {'caché':>9} {'sal':>8} {'ctx máx':>8}  tandas")
        for k, x in sorted(sumar(clave).items()):
            print(f"{k[:30]:30} {x['ses']:>4} {x['llamadas']:>6} {fmt(x['entrada']):>8} {fmt(x['creada']):>8} {fmt(x['cache']):>9} {fmt(x['salida']):>8} {fmt(x['ctx']):>8}  {', '.join(sorted(x['tandas']))[:40]}")

    tot = {k: sum(s[k] for s in filas) for k in ('llamadas', 'entrada', 'creada', 'cache', 'salida')}
    print(f"\nTOTAL ({len(filas)} sesiones): llamadas={tot['llamadas']} entrada={fmt(tot['entrada'])} cache creada={fmt(tot['creada'])} "
          f"cache leida={fmt(tot['cache'])} salida={fmt(tot['salida'])}  | contexto max. de cualquier sesion={fmt(max(s['ctx'] for s in filas))}")


if __name__ == '__main__':
    main()
