"""Mide el consumo de tokens por modelo y lo reparte en 5 niveles.

Uso:
  python scripts/niveles-modelos.py                tabla de niveles con los modelos medidos
  python scripts/niveles-modelos.py --niveles 3    solo los modelos del nivel 3
  python scripts/niveles-modelos.py --modelo deepseek   detalle de un modelo
  python scripts/niveles-modelos.py --json         salida para otro script

Que mide: lee la tabla `session` de la base de opencode (%USERPROFILE%\\.local\\share\\opencode\\opencode.db),
en modo solo lectura, y agrupa por modelo (id + variante). De cada modelo da sesiones, tokens por tipo,
USD, USD por millon de tokens (la metrica que define el nivel), USD por sesion y tokens por sesion.

Nivel = banda de USD por millon de tokens consumidos. Nivel 1 es lo que menos consume; nivel 5, lo que mas.
Las bandas por defecto son 0.02 / 0.06 / 0.20 / 1.00 USD por millon; se cambian con --cortes.
Un modelo con costo 0 (free) cae siempre en nivel 1, aunque su consumo de tokens sea alto.

Advertencia de lectura: el tamano de muestra importa. Con menos de 3 sesiones el nivel es provisional,
y la tabla lo marca. Un mismo modelo con variante distinta es otro modelo (deepseek-v4-pro default y
deepseek-v4-pro high difieren en un orden de magnitud).

Solo lee la base; no modifica nada. Ver docs/00-estandar-agentes/10-niveles-de-modelos.md.
"""
import json
import os
import sqlite3
import sys

DB_POR_DEFECTO = os.path.join(os.path.expanduser('~'), '.local', 'share', 'opencode', 'opencode.db')
CORTES_POR_DEFECTO = (0.02, 0.06, 0.20, 1.00)
MINIMO_MUESTRAS = 3


def nivel_de(usd_por_mtok, cortes):
    if usd_por_mtok < cortes[0]:
        return 1
    if usd_por_mtok < cortes[1]:
        return 2
    if usd_por_mtok < cortes[2]:
        return 3
    if usd_por_mtok < cortes[3]:
        return 4
    return 5


def agregar(db, directorio=None):
    """Devuelve {modelo: metricas} con las sesiones reales (descarta filas sin modelo o sin consumo)."""
    con = sqlite3.connect('file:%s?mode=ro' % db.replace('\\', '/'), uri=True)
    cur = con.cursor()
    sql = ('select model, parent_id, tokens_input, tokens_output, tokens_reasoning, '
           'tokens_cache_read, tokens_cache_write, cost, time_created, time_updated, directory '
           'from session')
    if directorio:
        sql += ' where directory like ?'
    filas = cur.execute(sql, ('%' + directorio + '%',) if directorio else ()).fetchall()
    con.close()

    agg = {}
    for model, parent, ti, to, tr, tcr, tcw, cost, tc, tu, _dir in filas:
        if not model:
            continue
        try:
            m = json.loads(model)
        except ValueError:
            continue
        mid = m.get('id') or ''
        if not mid:
            continue
        var = m.get('variant') or 'default'
        clave = '%s/%s%s' % (m.get('providerID') or '?', mid, ' [' + var + ']' if var != 'default' else '')
        a = agg.setdefault(clave, dict(n=0, sub=0, ti=0, to=0, tr=0, tcr=0, tcw=0, cost=0.0, min=0.0))
        a['n'] += 1
        if parent:
            a['sub'] += 1
        a['ti'] += ti or 0
        a['to'] += to or 0
        a['tr'] += tr or 0
        a['tcr'] += tcr or 0
        a['tcw'] += tcw or 0
        a['cost'] += cost or 0.0
        a['min'] += max(0, (tu or 0) - (tc or 0)) / 60000.0

    salida = []
    for clave, a in agg.items():
        tok = a['ti'] + a['to'] + a['tr'] + a['tcr'] + a['tcw']
        if tok == 0 and a['cost'] == 0:
            continue  # sesion sin consumo: no dice nada del modelo
        fresco = a['ti'] + a['to'] + a['tr']
        usd_mtok = a['cost'] / tok * 1e6 if tok else 0.0
        salida.append(dict(modelo=clave, n=a['n'], sub=a['sub'], costo=round(a['cost'], 4),
                           tokens=tok, frescos=fresco, usd_por_mtok=usd_mtok,
                           usd_por_fresco=a['cost'] / fresco * 1e6 if fresco else 0.0,
                           usd_por_sesion=a['cost'] / a['n'],
                           tokens_por_sesion=tok / a['n'],
                           minutos_por_sesion=a['min'] / a['n']))
    salida.sort(key=lambda r: (r['usd_por_mtok'], r['modelo']))
    return salida


def formatear(filas, cortes):
    lineas = []
    lineas.append('%-34s %3s %4s %8s %10s %10s %11s %10s  %s' % (
        'modelo', 'niv', 'n', 'USD', 'USD/Mtok', 'USD/ses', 'tok/ses', 'min/ses', 'nota'))
    lineas.append('-' * 118)
    for r in filas:
        nota = []
        if r['n'] < MINIMO_MUESTRAS:
            nota.append('muestra baja (%d)' % r['n'])
        if r['n'] and r['sub'] == r['n']:
            nota.append('solo subagentes')
        lineas.append('%-34s %3d %4d %8.4f %10.4f %10.4f %11s %10.1f  %s' % (
            r['modelo'][:34], nivel_de(r['usd_por_mtok'], cortes), r['n'], r['costo'], r['usd_por_mtok'],
            r['usd_por_sesion'], '{:,.0f}'.format(r['tokens_por_sesion']), r['minutos_por_sesion'],
            ', '.join(nota)))
    total = sum(r['costo'] for r in filas)
    lineas.append('-' * 118)
    lineas.append('total medido: %.4f USD en %d sesiones-modelo' % (total, len(filas)))
    return '\n'.join(lineas)


def main(argv):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    db = DB_POR_DEFECTO
    cortes = CORTES_POR_DEFECTO
    nivel = None
    modelo = None
    como_json = False
    directorio = None
    i = 1
    while i < len(argv):
        a = argv[i]
        if a == '--db':
            i += 1
            db = argv[i]
        elif a == '--cortes':
            i += 1
            cortes = tuple(float(x) for x in argv[i].split(','))
        elif a == '--niveles':
            i += 1
            nivel = int(argv[i])
        elif a == '--modelo':
            i += 1
            modelo = argv[i]
        elif a == '--dir':
            i += 1
            directorio = argv[i]
        elif a == '--json':
            como_json = True
        else:
            print('opcion desconocida: %s' % a)
            return 2
        i += 1

    if not os.path.exists(db):
        print('no existe la base de opencode: %s' % db)
        print('se busca en %%USERPROFILE%%\\.local\\share\\opencode\\opencode.db; se puede indicar con --db')
        return 2

    filas = agregar(db, directorio)
    if not filas:
        print('sin sesiones con consumo en %s' % db)
        return 1

    if nivel:
        filas = [r for r in filas if nivel_de(r['usd_por_mtok'], cortes) == nivel]
    if modelo:
        filas = [r for r in filas if modelo.lower() in r['modelo'].lower()]

    if como_json:
        for r in filas:
            r['nivel'] = nivel_de(r['usd_por_mtok'], cortes)
        print(json.dumps({'cortes': cortes, 'filas': filas}, indent=2, ensure_ascii=False))
        return 0

    if not filas:
        print('ningun modelo coincide con el filtro')
        return 1
    print(formatear(filas, cortes))
    print('bandas: nivel 1 < %.2f | 2 < %.2f | 3 < %.2f | 4 < %.2f | 5 >= %.2f  (USD por millon de tokens)'
          % (cortes[0], cortes[1], cortes[2], cortes[3], cortes[3]))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))
