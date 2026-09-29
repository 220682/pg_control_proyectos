# Medición de eficiencia de contexto

Se mide con los transcripts de sesión. Los Workers son subagentes del Orquestador: su transcript vive en `<sesión del Orquestador>/subagents/agent-*.jsonl` (con un `agent-*.meta.json` que trae la descripción), dentro de `%USERPROFILE%\.claude\projects\d--VICTOR-CLAUDE-CODE-pg-control-proyectos` (verificado el 2026-09-29; en Windows la carpeta no distingue mayúsculas: `D--` y `d--` son la misma). Para la app existiría `D--VICTOR-CLAUDE-CODE-py-control-proyectos-web` si se abriera una sesión desde ese directorio; **hoy no existe** (solo hay una carpeta antigua `c--Users-BRANDY-Downloads-…-py-control-proyectos-web` de otro origen), y el script la incluye por si aparece. Métricas por sesión: llamadas a la API (mensajes de asistente sin duplicar), herramientas usadas, contexto máximo y tokens leídos de caché (la cifra que crece con `llamadas × contexto`).

## Línea base (medida el 2026-09-29, antes de los cambios)

| Sesión | Rol | Llamadas | Herramientas | Contexto máx. | Leído de caché |
|---|---|---|---|---|---|
| `agent-af9399834b746cbf` | Planner del plan (v1 a v7) | 193 | 217 | 685k | 82,0M |
| `b7806143-…` | Orquestador anterior (paneles) | 220 | 301 | 552k | 71,0M |
| Referencia (`hermes_agent`, otro plan) | Worker de fase entera F1 (16 ítems) | 156 | — | 682k | 83,8M |
| Referencia (`hermes_agent`) | Worker de fase entera F2 (parcial) | 191 | — | 625k | 97,4M |
| Referencia (`hermes_agent`) | Tandas F2-A a F3-B (8 Workers) | 21 a 70 | 32 a 81 | 93k a 186k | 1,5M a 8,7M cada una; ~28M en total |

Este plan aún no tiene Workers ejecutados: la línea base propia es la del Planner y el Orquestador; la de Workers es la referencia de `hermes_agent`.

## Metas por tanda de Worker (todas las tandas)

- Llamadas ≤ 80 (cierre a las ~60 con handoff). Contexto máximo ≤ 200k. Leído de caché ≤ 12M por tanda.
- Objetivo agregado (estimación, no medición): las 6 tandas de referencia de `hermes_agent` promedian ~4,7M de caché; 38 tandas × 4,7M ≈ **180M** en total, con techo teórico de 38 × 12M = 456M si todas llegaran a la meta. Compárese con los ~82M de un solo Planner y con un Worker de fase entera (84–97M cada uno) que además no cabe en una sesión.
- Si una tanda supera una meta, el Orquestador anota la causa (qué se leyó o repitió) en la tabla de resultados y corrige el brief de la siguiente antes de lanzarla.

## Cómo medir (tras cada tanda)

Guarda este script como `medir.py` en la carpeta temporal de tu sesión (no en el repositorio) y ejecútalo con Python desde cualquier terminal: `python medir.py 6` lista las 6 sesiones más recientes (probado el 2026-09-29 sobre este proyecto). La fila del Worker es la que trae su `descripción`.

```python
import json, glob, os, datetime, sys

# Uso: python medir.py [N]   (N = cuantas sesiones recientes listar; por defecto 8)
n_ultimas = int(sys.argv[1]) if len(sys.argv) > 1 else 8
raiz = os.path.expandvars(r'%USERPROFILE%\.claude\projects')
carpetas = [os.path.join(raiz, d) for d in ('D--VICTOR-CLAUDE-CODE-pg-control-proyectos', 'D--VICTOR-CLAUDE-CODE-py-control-proyectos-web')]
archivos = []
for base in carpetas:
    if os.path.isdir(base):
        archivos += glob.glob(base + '/**/*.jsonl', recursive=True)
for f in sorted(archivos, key=os.path.getmtime)[-n_ultimas:]:
    vistos = set(); usos = set(); llamadas = cache = mx = 0
    for linea in open(f, encoding='utf-8'):
        try:
            o = json.loads(linea)
        except Exception:
            continue
        m = o.get('message') or {}
        u = m.get('usage')
        if o.get('type') != 'assistant':
            continue
        if isinstance(m.get('content'), list):
            for b in m['content']:
                if isinstance(b, dict) and b.get('type') == 'tool_use':
                    usos.add(b.get('id'))
        if not u:
            continue
        clave = m.get('id') or o.get('uuid')
        if clave in vistos:
            continue
        vistos.add(clave)
        llamadas += 1
        cache += u.get('cache_read_input_tokens', 0)
        mx = max(mx, u.get('input_tokens', 0) + u.get('cache_creation_input_tokens', 0) + u.get('cache_read_input_tokens', 0))
    desc = ''
    meta = f[:-6] + '.meta.json'
    if os.path.exists(meta):
        try:
            desc = json.load(open(meta, encoding='utf-8')).get('description', '')
        except Exception:
            pass
    print(os.path.basename(f)[:22], datetime.datetime.fromtimestamp(os.path.getmtime(f)).strftime('%m-%d %H:%M'),
          f'llamadas={llamadas}', f'herramientas={len(usos)}', f'ctx_max={mx // 1000}k', f'cache={round(cache / 1e6, 1)}M', desc)
```

## Resultados por tanda

Se rellena tras cada tanda (llamadas y herramientas del script; «¿Cumple?» compara con las metas; «Causa» solo si no cumple).

| Tanda | Sesión (`agent-…`) | Llamadas | Herramientas | Contexto máx. | Leído de caché | ¿Cumple meta? | Ítems cerrados / pendientes | Causa y ajuste al siguiente brief |
|---|---|---|---|---|---|---|---|---|
| F0-A |  |  |  |  |  |  |  |  |
| F0-B |  |  |  |  |  |  |  |  |
| F0-C |  |  |  |  |  |  |  |  |
| F1-A |  |  |  |  |  |  |  |  |
| F1-B |  |  |  |  |  |  |  |  |
| F2-A |  |  |  |  |  |  |  |  |
| F2-B |  |  |  |  |  |  |  |  |
| F2-C |  |  |  |  |  |  |  |  |
| F2-D |  |  |  |  |  |  |  |  |
| F2-E |  |  |  |  |  |  |  |  |
| F2B-A |  |  |  |  |  |  |  |  |
| F2B-B |  |  |  |  |  |  |  |  |
| F3-A |  |  |  |  |  |  |  |  |
| F3-B |  |  |  |  |  |  |  |  |
| F3-C |  |  |  |  |  |  |  |  |
| F4-A |  |  |  |  |  |  |  |  |
| F4B-A |  |  |  |  |  |  |  |  |
| F4B-B |  |  |  |  |  |  |  |  |
| F4B-C |  |  |  |  |  |  |  |  |
| F5-A |  |  |  |  |  |  |  |  |
| F5B-A |  |  |  |  |  |  |  |  |
| F5B-B |  |  |  |  |  |  |  |  |
| F5B-C |  |  |  |  |  |  |  |  |
| F5C-A |  |  |  |  |  |  |  |  |
| F5C-B |  |  |  |  |  |  |  |  |
| F5C-C |  |  |  |  |  |  |  |  |
| F5C-D |  |  |  |  |  |  |  |  |
| F5D-A |  |  |  |  |  |  |  |  |
| F5D-B |  |  |  |  |  |  |  |  |
| F6-A |  |  |  |  |  |  |  |  |
| F6-B |  |  |  |  |  |  |  |  |
| F6-C |  |  |  |  |  |  |  |  |
| F6-D |  |  |  |  |  |  |  |  |
| F6-E |  |  |  |  |  |  |  |  |
| F7-A |  |  |  |  |  |  |  |  |
| F7-B |  |  |  |  |  |  |  |  |
| F7-C |  |  |  |  |  |  |  |  |
| F7-D |  |  |  |  |  |  |  |  |
| F6-R# (si hay) |  |  |  |  |  |  |  |  |
