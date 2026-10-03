# Resultado Tanda V — arreglo del verificador de acciones (`scripts/verificar.ps1`)

**Plan:** `2026-10-02-observaciones-victor-lote-3-plan.md` · **Worker:** flash Tanda V · **Fecha:** 2026-10-03
**Commit:** `53dbee9` en `main` local (SIN push) — `V: verificar.ps1 - nombre del informe sin sufijo -plan y conteo de Registrada con acentos graves`

## Qué cambié (único archivo: `scripts/verificar.ps1`)

### Defecto 1 — informe del Auditor (antes línea 82)

Antes se buscaba `04-auditoria\<nombre del plan tal cual>`, o sea `…-plan.md`, que la convención nunca usa. Ahora (nuevas líneas 82-87):

```powershell
$leaf = Split-Path $Plan -Leaf
$auditoriaDir = Join-Path (Split-Path (Split-Path $Plan -Parent) -Parent) '04-auditoria'
$candidatos = @((Join-Path $auditoriaDir ($leaf -replace '-plan\.md$', '.md')), (Join-Path $auditoriaDir $leaf))
$informe = $candidatos | Where-Object { Test-Path $_ } | Select-Object -First 1
```

Se aceptan ambos nombres (con y sin `-plan`), como pide el brief. Comentario en español junto al arreglo.

### Defecto 2 — conteo de `Registrada` (antes línea 89, ahora 96)

```powershell
$hechos.filas_de_hallazgos_sin_trasladar = ([regex]::Matches($planTxt, '\|\s*`?Registrada`?\s*\|')).Count
```

El patrón acepta el estado con o sin acentos graves. Umbrales (0,9 / 0,1), clases y preguntas: intactos. No se tocó nada más.

## Validación

Script temporal **fuera del repositorio** (`%TEMP%\opencode\test-verificar-V.ps1`, ya borrado) con estructura fixture `…\01-planes\` + `…\04-auditoria\` replicando la derivación de rutas del script. Salidas reales:

Con las expresiones viejas (control, caso A) — confirman ambos defectos:

```text
control (expresiones viejas, caso A): informe_viejo_existe = False | filas_viejas = 0
```

Con las expresiones corregidas (los dos casos pedidos):

```text
2026-10-02-prueba-A-plan.md: informe_de_auditoria = existe (2026-10-02-prueba-A.md) | filas_de_hallazgos_sin_trasladar = 1
2026-10-02-prueba-B.md: informe_de_auditoria = existe (2026-10-02-prueba-B.md) | filas_de_hallazgos_sin_trasladar = 1
```

- Caso A: plan **con** `-plan` y fila `` | X | `Registrada` | `` → encuentra 1 informe (buscado sin `-plan`) y cuenta 1 fila. ✔
- Caso B: plan **sin** `-plan` y fila `| X | Registrada |` → encuentra 1 informe y cuenta 1 fila. ✔
- Verificación extra con datos reales del repo: existe `docs/02-trabajo-activo/04-auditoria/2026-10-02-observaciones-victor-lote-2.md` (sin `-plan`), exactamente el nombre que la lógica vieja no encontraba.
- Parseo sintáctico del script modificado (`Parser::ParseFile`): `sintaxis OK`. No se ejecutó el verificador real: requiere `OPENROUTER_API_KEY` (fuera de alcance según el brief).

## `git diff --stat`

```text
 scripts/verificar.ps1 | 13 ++++++++++---
 1 file changed, 10 insertions(+), 3 deletions(-)
```

## Hallazgos (4 categorías)

### Mejoras (de trabajo)

- Al construir fixtures de prueba de rutas, la anidación debe replicar la **derivación exacta** del script (parent-parent del archivo de plan), no la ruta "visible" del repo: mi primer intento falló porque colgué `04-auditoria` un nivel más arriba. Vale como patrón general para probar este script.
- En PowerShell 5.1, escribir acentos graves dentro de cadenas de doble comilla se corrompe (`` ` `` es escape); para fixtures con `` `Registrada` `` usar cadena de comilla simple.

### Reglas de negocio acordadas en esta tarea

- Ninguna nueva. La tanda solo alineó el verificador con reglas ya escritas (convención del nombre del informe en `02-roles-y-delegacion.md` § Auditor y formato del libro de hallazgos en las plantillas).

### Observaciones sobre la política

- El standard nombra el informe como "el mismo nombre base sin `-plan`", pero `verificar.ps1` nació contradictorio con esa regla: la política no exige una prueba de routinas/nombres contra un fixture cuando se escribe un script que lee el árbol de `docs/`. El Auditor podría añadir esa comprobación al revisar scripts del tipo `scripts/`.
- `04-auditoria` cuelga de `docs/02-trabajo-activo/`, y el script lo deriva con dos `Split-Path -Parent` sin validar que el plan realmente viva bajo `01-planes`; si alguien pasa un plan fuera de esa estructura, el fallback `no existe` es silencioso. Menor, por si el Orquestador quiere documentarlo.

### Carpetas/archivos huérfanos

- Nada creado ni detectado por esta tanda dentro de `pg_control_proyectos`. Preexistentes observados en `git status` (no tocados, no míos): `.opencode/config.json` modificado sin commitear, y este mismo brief `…/briefs/V.md` queda sin seguimiento (lo dejó el Orquestador; no lo commiteé porque el brief ordenaba commit solo del script).
