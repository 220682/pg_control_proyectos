"""Mide el contexto con el que ARRANCA cada sesion de agente, no solo como crece.

Uso:
  python scripts/arranque.py [N]                    las N sesiones mas recientes
  python scripts/arranque.py [N] --bloques          ademas, de donde vino el contexto
  python scripts/arranque.py [N] --bloques 12       los 12 bloques de herramienta mas grandes

Que mide y por que:
  «Contexto de la 1a llamada» son los tokens que el agente ya traia ANTES de hacer
  nada: prompt del sistema, AGENTS.md, bloque de Skills y el brief. Es la linea base
  que ningun brief puede bajar. «ctx max.» es el pico de la sesion (medir.py lo da
  tambien). La diferencia entre las dos es lo que el agente leyo por su cuenta.

  --bloques descompone el contexto en resultados de herramienta, agrupados por
  herramienta, para distinguir una fuga de politica (leer archivos de mas) de un
  costo normal (una captura de navegador, un log largo).

Solo lee los registros locales de sesion; no usa red, no cuesta tokens y no modifica nada.
Se complementa con medir.py, que mide costo y calidad: este script mide el arranque.

Ver docs/00-estandar-agentes/08-medicion-y-relevo.md y
docs/01-contexto-repositorio/09-medicion-y-modelos.md.
"""
import argparse
import datetime
import glob
import json
import os

CARPETAS = ('D--VICTOR-CLAUDE-CODE-pg-control-proyectos', 'D--VICTOR-CLAUDE-CODE-py-control-proyectos-web')


def total_ctx(u):
    """Tokens de contexto de una llamada: lo no cacheado + lo creado + lo leido de cache."""
    return u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0)


def texto_de(bloque):
    """Texto de un bloque de contenido: str, o lista de dicts con text/input."""
    c = bloque.get('content')
    if isinstance(c, str):
        return c
    if isinstance(c, list):
        out = []
        for x in c:
            if isinstance(x, dict):
                out.append(x.get('text', '') or json.dumps(x.get('input', ''), ensure_ascii=False))
            else:
                out.append(str(x))
        return ' '.join(out)
    return ''


def descripcion(ruta):
    """Descripcion con que se lanzo el subagente («Rol N · tanda»). Vacia si es la sesion principal."""
    meta = ruta[:-6] + '.meta.json'
    if os.path.exists(meta):
        try:
            return json.load(open(meta, encoding='utf-8')).get('description', '') or ''
        except Exception:
            return ''
    return ''


def analizar(ruta):
    """Recorre el .jsonl una vez y devuelve arranque, pico, llamadas y bloques de herramienta."""
    vistos, nombres = set(), {}
    arranque = None
    pico, llamadas, bloques = 0, 0, []

    for linea in open(ruta, encoding='utf-8'):
        try:
            o = json.loads(linea)
        except Exception:
            continue
        m = o.get('message') or {}
        u = m.get('usage')
        clave = m.get('id') or o.get('uuid')
        c = m.get('content')

        # los nombres de herramienta y sus resultados viven en turnos distintos: el
        # tool_use en el turno del asistente, el tool_result en el turno del usuario.
        if isinstance(c, list):
            for b in c:
                if not isinstance(b, dict):
                    continue
                if b.get('type') == 'tool_use':
                    nombres[b.get('id')] = b.get('name', '?')
                elif b.get('type') == 'tool_result':
                    bloques.append((len(texto_de(b)), nombres.get(b.get('tool_use_id'), '?')))

        if o.get('type') != 'assistant' or not u:
            continue
        if clave not in vistos:
            vistos.add(clave)
            llamadas += 1
            ctx = total_ctx(u)
            pico = max(pico, ctx)
            if arranque is None:
                arranque = dict(ctx=ctx,
                                creada=u.get('cache_creation_input_tokens', 0),
                                leida=u.get('cache_read_input_tokens', 0))
        else:
            pico = max(pico, total_ctx(u))

    return arranque, pico, llamadas, bloques


def fmt(n):
    return f'{n / 1e6:.2f}M' if n >= 1e6 else f'{n / 1e3:.0f}k'


def main():
    ap = argparse.ArgumentParser(description='Mide el contexto de arranque de las sesiones de agentes.')
    ap.add_argument('n', nargs='?', type=int, default=15)
    ap.add_argument('--bloques', nargs='?', type=int, const=5, default=None,
                    help='Muestra los N bloques de herramienta mas grandes de cada sesion.')
    a = ap.parse_args()

    raiz = os.path.expandvars(r'%USERPROFILE%\\.claude\\projects')
    archivos = []
    for c in CARPETAS:
        base = os.path.join(raiz, c)
        if os.path.isdir(base):
            archivos += glob.glob(base + '/**/*.jsonl', recursive=True)
    archivos.sort(key=os.path.getmtime)

    filas = []
    for f in archivos[-400:]:
        arranque, pico, llamadas, bloques = analizar(f)
        if not arranque:
            continue
        es_sub = f'{os.sep}subagents{os.sep}' in f or '/subagents/' in f
        d = descripcion(f)
        filas.append(dict(
            fecha=datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%m-%d %H:%M'),
            quien=(d or ('(principal)' if not es_sub else '(sub sin etiqueta)')),
            rol=('principal' if not es_sub else 'subagente'),
            ctx1=arranque['ctx'], creada1=arranque['creada'], leida1=arranque['leida'],
            pico=pico, llamadas=llamadas, bloques=bloques))

    filas.sort(key=lambda x: (x['fecha'], x['quien']))
    filas = filas[-a.n:]

    cab = (f"{'fecha':11} {'agente':38} {'rol':10} {'ctx 1a':>7} {'crea 1a':>8} {'lee 1a':>7} "
           f"{'creci\u00f3':>8} {'llam':>5} {'ctx m\u00e1x':>8}")
    print(cab)
    for f in filas:
        print(f"{f['fecha']:11} {f['quien'][:38]:38} {f['rol']:10} {fmt(f['ctx1']):>7} {fmt(f['creada1']):>8} "
              f"{fmt(f['leida1']):>7} {fmt(f['pico'] - f['ctx1']):>8} {f['llamadas']:>5} {fmt(f['pico']):>8}")

    subs = [f for f in filas if f['rol'] == 'subagente']
    for etiqueta, grupo in (('Subagentes (Workers, Planner, Auditor)', subs),
                            ('Sesion principal (Orquestador)', [f for f in filas if f['rol'] == 'principal'])):
        if not grupo:
            continue
        arr = sorted(f['ctx1'] for f in grupo)
        print(f"\n{etiqueta}: n={len(arr)}  min={fmt(arr[0])}  mediana={fmt(arr[len(arr) // 2])}  "
              f"max={fmt(arr[-1])}  media={fmt(sum(arr) // len(arr))}")
    if subs:
        print("\n'ctx 1a' es lo que el agente trae antes de trabajar: AGENTS.md, bloque de Skills y el brief.")
        print("'creci\u00f3' es lo que leyo por su cuenta durante la sesion (flujos, plan, logs, capturas).")

    if a.bloques is None:
        return
    print()
    for f in filas[-a.bloques:]:
        por_herr = {}
        for largo, herr in f['bloques']:
            por_herr[herr] = por_herr.get(herr, 0) + largo
        total = sum(por_herr.values())
        print(f"--- {f['fecha']} | {f['quien'][:44]} | resultados de herramienta: {fmt(total)} caracteres (~{fmt(total // 4)} tokens)")
        print("    " + ", ".join(f"{h}={fmt(v)}" for h, v in sorted(por_herr.items(), key=lambda x: -x[1])[:6]))
        for largo, herr in sorted(f['bloques'], reverse=True)[:3]:
            print(f"      mayor bloque: {fmt(largo)} caracteres, via {herr}")


if __name__ == '__main__':
    main()