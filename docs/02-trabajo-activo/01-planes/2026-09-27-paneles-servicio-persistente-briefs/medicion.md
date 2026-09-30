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
| F0-A | `agent-ac7e20c931d0250e` | 15 | 24 | 120k | 1,2M | Sí |  |  |
| F0-B | `agent-abfa8261b8df4ba5`<br>`agent-a0365b950d885059` (F0-B-2) | 10<br>48 | 18<br>70 | 75k<br>94k | 0,6M<br>3,3M | Sí |  |  |
| F0-C | `agent-a020c8887028c1a2` | 36 | 42 | 143k | 3,3M | Sí |  |  |
| F1-A | `agent-a2df08e29b7869dc` | 16 | 23 | 94k | 1,2M | Sí |  |  |
| F1-B | `agent-a06b4625a5b2becb` | 29 | 40 | 135k | 3,0M | Sí |  |  |
| F2-A | `agent-a47cd74a430ef1ef` | 38 | 53 | 125k | 3,6M | Sí |  |  |
| F2-B | `agent-a363930716082649` | 47 | 70 | 101k | 3,4M | Sí |  |  |
| F2-C | `agent-a19bf54e405dd290` | 60 | 79 | 143k | 6,3M | Sí |  |  |
| F2-D | `agent-a5652b6b561c560c` | 39 | 62 | 120k | 3,6M | Sí |  |  |
| F2-E | `agent-aa635c77c73adb99` | 32 | 48 | 93k | 2,2M | Sí |  |  |
| F2B-A | `agent-aaaf1b72ca844025` | 37 | 56 | 141k | 3,9M | Sí |  |  |
| F2B-B | `agent-ace58806a13adf18`<br>`agent-ae9d105164e13bcd` (F2B-B-2) | 33<br>32 | 47<br>40 | 93k<br>84k | 2,4M<br>2,1M | Sí |  |  |
| F3-A | `agent-a9c6365c0eff2b66` | 41 | 56 | 133k | 4,2M | Sí |  |  |
| F3-B | `agent-a290198ca9561f37` | 37 | 49 | 96k | 2,8M | Sí |  |  |
| F3-C | `agent-af16f2f3cd326266` | 63 | 75 | 117k | 5,8M | Sí |  |  |
| F4-A | `agent-abdad01b5e9ce568` | 45 | 59 | 141k | 4,9M | Sí |  |  |
| F4B-A | `agent-a48e5dc2882efdbf` | 22 | 30 | 88k | 1,4M | Sí |  |  |
| F4B-B | `agent-ac444abe4f86425b` | 34 | 55 | 88k | 2,3M | Sí |  |  |
| F4B-C | `agent-ad79b362a3995d42` | 29 | 40 | 88k | 1,9M | Sí |  |  |
| F5-A | `agent-a3fe836e5e21bf61` | 31 | 43 | 136k | 3,1M | Sí |  |  |
| F5B-A | `agent-aaea55a60fb2cc31` | 30 | 40 | 117k | 2,8M | Sí |  |  |
| F5B-B | `agent-a39c9e653743a68e` (sesión inicial)<br>`agent-a2c62c9929bf60b1` | 1<br>35 | 0<br>68 | 0k<br>111k | 0,0M<br>2,8M | Sí |  |  |
| F5B-C | `agent-acd4bf9fb15f59cb` | 31 | 49 | 105k | 2,4M | Sí |  |  |
| F5C-A | `agent-a91fb6cd0deb8c6b` | 32 | 42 | 114k | 2,8M | Sí |  |  |
| F5C-B | `agent-ab20533282825810` | 26 | 68 | 116k | 2,3M | Sí |  |  |
| F5C-C | `agent-a1be100a626dd6f4` | 39 | 44 | 108k | 3,2M | Sí |  |  |
| F5C-D | `agent-af4f12fe80c23e92` | 35 | 42 | 119k | 3,1M | Sí |  |  |
| F5D-A | `agent-af775b9c41dbcaf2` | 22 | 26 | 86k | 1,5M | Sí |  |  |
| F5D-B | `agent-a804c718af8d2e38` | 43 | 73 | 118k | 4,0M | Sí |  |  |
| F6-A | `agent-a90af07b88081ef6` | 38 | 56 | 177k | 4,2M | Sí |  |  |
| F6-B | `agent-a8f8890695c50e24` | 68 | 93 | 128k | 6,3M | Sí |  |  |
| F6-C | `agent-afb1ca943ad75ff9` | 23 | 30 | 94k | 1,5M | Sí |  |  |
| F6-D | `agent-a5ac69ead2cab836` | 27 | 37 | 100k | 1,8M | Sí |  |  |
| F6-E | `agent-a4f6cf4a0027f5a4` | 10 | 12 | 68k | 0,5M | Sí |  |  |
| F7-A | `agent-a7fda924c76a5a18` | 19 | 52 | 107k | 1,4M | Sí |  |  |
| F7-B | `agent-a4c44d07ce73d509` | 31 | 36 | 126k | 2,8M | Sí |  |  |
| F7-C | `agent-aea299abcc8d24b5`<br>`agent-af0c370ad97d221d` (F7-C2) | 34<br>9 | 69<br>20 | 139k<br>66k | 3,2M<br>0,5M | Sí |  |  |
| F7-D | `agent-a6a2f40ce6805a9c` | 2 | 4 | 50k | 0,1M | Sí (parcial: sesión en curso al medir) |  |  |
| F6-R1 | `agent-a8ba1d3999b1d085` | 19 | 25 | 69k | 1,1M | Sí |  |  |

Medido el 2026-09-30 con `medir.py 60` (columnas de sesión, llamadas, herramientas, contexto y caché tomadas tal cual de su salida; «¿Cumple meta?» compara con las metas de arriba: ≤ 80 llamadas, ≤ 200k de contexto, ≤ 12M de caché). Máximos observados en las tandas de Worker: 68 llamadas (F6-B), 177k de contexto (F6-A) y 6,3M de caché (F2-C y F6-B). Las columnas «Ítems cerrados / pendientes» y «Causa» quedan sin rellenar porque la salida del script no las contiene (el detalle está en los handoffs del progreso). F7-D: medición parcial (la sesión seguía en curso al medir).
