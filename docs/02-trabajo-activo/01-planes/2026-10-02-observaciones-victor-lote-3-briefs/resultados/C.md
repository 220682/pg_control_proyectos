# Resultados Tanda C — Alinear `.opencode/config.json` con el config global

**Plan:** `2026-10-02-observaciones-victor-lote-3-plan.md` · **Worker:** flash · **Fecha:** 2026-10-03 · **Rama:** `main` local, sin push.

## Cambio ejecutado

- Archivo único modificado: `.opencode/config.json`.
- Eliminadas las 6 referencias a `opencode-go/qwen3.8-plus` y todos los modelos por rol (`general`, `explore`, `orchestrator`, `roles.*` con sus `default`/`alternatives`/`levels.*.model`).
- Eliminada también la clave `model` de `jev` (`typesafe/jev-1.13`): no aparece en `opencode models` (verificado 2026-10-03). Se conservaron `endpoint`, `use_for` y `thresholds`.
- Conservados sin cambios: `$schema`, sección `mcp` (Playwright), `effort_policy`, `effort` por rol, `criteria`/`requires_approval`/`log_always` de los niveles de worker, `context_thresholds`, notas existentes.
- Añadida clave `"$comment"` con la línea que pide el brief: `Fuente de verdad de los modelos por rol: ~/.config/opencode/opencode.jsonc (decision de Victor, 2026-10-03). Este archivo no define modelos.`

## Commit

`ba7e371` — `config: el repo deja de definir modelos por rol (fuente de verdad: config global)` · 1 file changed, 8 insertions(+), 32 deletions(-) · **sin push**.

## Validaciones (4 salidas)

### 1. JSON válido

```
PS> python -c "import json;json.load(open(r'.opencode/config.json',encoding='utf-8'))"
(sin error) → JSON OK
```

### 2. Cero referencias a `qwen3.8-plus`

```
PS> Select-String -Path .opencode/config.json -Pattern "qwen3.8-plus"
(sin coincidencias)
```

### 3. Modelos que sobreviven

Búsqueda de cualquier identificador de modelo (`model|qwen|typesafe|opencode-go`): única coincidencia es la palabra "modelos" dentro del texto de `$comment`. **Lista de modelos restantes: ninguna.** No aplica verificación contra `opencode models` porque ningún rol declara modelo; el repo remite al global.

### 4. `git diff --stat` y `git status --short`

Antes del commit:

```
 .opencode/config.json                              | 40 +++++-----------------
 .../00-protocolo-migraciones.md                    |  3 +-
```

`git status --short` mostraba además, ajenos a esta tanda: ` M docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/00-protocolo-migraciones.md` y los untracked `?? .../2026-10-02-observaciones-victor-lote-3-briefs/C.md` y `?? .../M.md`. **No se tocaron ni se stagearon** (solo se añadió `.opencode/config.json` al commit). Después del commit queda:

```
 M docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/00-protocolo-migraciones.md
?? docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-lote-3-briefs/C.md
?? docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-lote-3-briefs/M.md
```

Nota: `git` advierte `LF will be replaced by CRLF` en `.opencode/config.json` (config de línea de fin de archivo del entorno; no afecta al contenido commiteado).

## Hallazgos (4 categorías)

### Mejoras (de trabajo)

- El brief pedía "deja un comentario `// ...`" en un archivo `.json` (no `.jsonc`): un comentario `//` invalidaría el JSON. Se resolvió usando la clave estándar `$comment`, que es válida en JSON y legible para el harness. Pendiente de confirmar por Victor/Auditor si prefiere mover esa nota a un `.md` del repo.

### Reglas de negocio acordadas en esta tarea

- Ninguna nueva. La regla ya acordada (decisión de Victor 2026-10-03: el config global `~/.config/opencode/opencode.jsonc` es la fuente de verdad de modelos por rol; el repo no define modelos) quedó materializada en `$comment` del archivo.

### Observaciones sobre la política

- `jev.model` (`typesafe/jev-1.13`) tampoco existe en `opencode models`: el fallo del proveedor no se limitaba a `qwen3.8-plus`. Si el verificador de acciones necesita un modelo, debe declararse en el config global (o en `docs/00-estandar-agentes/07-verificador-de-acciones.md`), no en este archivo. Se eliminó la clave por indicación del brief ("si una clave exige un valor de modelo, quítala en vez de inventar uno").

### Carpetas/archivos huérfanos

- `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/00-protocolo-migraciones.md` aparece modificado sin que esta tanda lo toque (posible residuo de otra sesión; reportado, no borrado).
- `docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-lote-3-briefs/M.md` existe como untracked junto al brief C; no es de esta tanda (reportado a la Orquestadora).
