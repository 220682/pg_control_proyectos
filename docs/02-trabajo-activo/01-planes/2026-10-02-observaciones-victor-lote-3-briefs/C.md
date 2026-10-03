# Brief Tanda C — Worker flash (alinear `.opencode/config.json` del repo con el config global)

**Plan:** `2026-10-02-observaciones-victor-lote-3-plan.md` · **Repositorio:** `pg_control_proyectos` · **Archivo único:** `.opencode/config.json` · Rama `main` local, **SIN push** (el push de docs se hace tras el Gate 2).

## Contexto

Hoy el repo tiene **su propia** tabla rol→modelo en `.opencode/config.json`, y está en dos estados que hay que corregir:

1. **6 de sus roles apuntan a `opencode-go/qwen3.8-plus`, que NO existe** en el proveedor (verificado con `opencode models`). Eso ya impedió lanzar un Worker en el Lote 3.
2. Sus modelos contradicen la decisión de Victor del 2026-10-03.

**Decisión de Victor (2026-10-03): el config global manda** — `~/.config/opencode/opencode.jsonc`, fuera de los repositorios. Ya está actualizado y válido. El archivo del repo debe **dejar de ser una segunda fuente de verdad** y solo remitir al global.

## Qué hacer (solo `.opencode/config.json`)

1. **Elimina toda referencia a `opencode-go/qwen3.8-plus`** (6 ocurrencias) y toda entrada que quede apuntando a un modelo inexistente.
2. Deja el archivo como **una declaración de que la fuente de verdad es el global**, no como una tabla de modelos que compita con él. Concretamente: conserva la estructura de claves que el harness lee (`agent`, `mcp`) y el resto de secciones, pero **ningún rol debe declarar un `model` propio**. Si una clave exige un valor de modelo, quítala en vez de inventar uno.
3. **Conserva** la sección `mcp` (Playwright) tal como está y cualquier otra configuración que no sea de modelos.
4. Deja un comentario de una línea, en español, diciendo: `// Fuente de verdad de los modelos por rol: ~/.config/opencode/opencode.jsonc (decision de Victor, 2026-10-03). Este archivo no define modelos.`
5. **No toques** `~/.config/opencode/opencode.jsonc` (ya está, es fuera del repo), ni el estándar `docs/00-estandar-agentes/09-orquestacion-y-modelos.md` (su tabla de modelos es una fuente de verdad central: la modifica el Responsable humano en el Gate 2, no tú).

## Validación

1. **El JSON sigue siendo válido.** El archivo es `.json` (no `.jsonc`): valida con `python -c "import json;json.load(open(r'.opencode/config.json',encoding='utf-8'))"` y pega la salida (sin error = OK).
2. **Cero referencias a `qwen3.8-plus`:** `Select-String -Path .opencode/config.json -Pattern "qwen3.8-plus"` no debe devolver nada.
3. **Los modelos que sobren deben existir:** si queda algún nombre de modelo en el archivo, verifica con `opencode models` que existe. Pega la lista de modelos que quedaron y el sí/no de cada uno.
4. `git diff --stat` y `git status --short`.

## Cierre

- Commit en `main` local: `config: el repo deja de definir modelos por rol (fuente de verdad: config global)`.
- **Sin push.**
- `resultados/C.md` en `2026-10-02-observaciones-victor-lote-3-briefs/resultados/` con las cuatro salidas de validación y tus hallazgos en las 4 categorías.
- Una línea de respuesta: commit, JSON válido sí/no, referencias muertas restantes.