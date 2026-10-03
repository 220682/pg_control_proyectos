# Brief Tanda V — Worker flash (arreglo del verificador de acciones)

**Plan:** `2026-10-02-observaciones-victor-lote-3-plan.md` · **Repositorio:** `pg_control_proyectos` (documentación), rama `main` **local, SIN push** (decisión de Victor 2026-10-02: el push de docs se hace en el cierre, tras el Gate 2). **Archivo único:** `scripts/verificar.ps1`. **NO** toques la app `py_control_proyectos_web`, ni el estándar, ni `AGENTS.md`, ni ningún plan.

## Por qué esta tanda existe

Con `PLAN_ACTIVO`, este script decide si se puede mergear a `main` y si se puede escribir el mensaje de cierre. Hoy tiene **dos defectos que lo hacen pasar siempre o bloquear siempre mal**:

### Defecto 1 — el informe del Auditor nunca se encuentra (línea 82)

Hoy: `$informe = Join-Path (…) ('04-auditoria\' + (Split-Path $Plan -Leaf))`

Como `$Plan` es el archivo de plan y estos se llaman `…-plan.md`, el script busca `04-auditoria/…-plan.md`. Pero la convención (`02-roles-y-delegacion.md` § Auditor) es **el mismo nombre base sin el sufijo `-plan`**: el plan `2026-10-02-observaciones-victor-lote-2-plan.md` se audita en `04-auditoria/2026-10-02-observaciones-victor-lote-2.md`. Resultado: `informe_de_auditoria = 'no existe'` aunque el informe exista → bloqueo falso en el Gate 2.

**Arregla:** quitar el sufijo `-plan` del nombre antes de buscar (acepta ambos nombres: con y sin `-plan`).

### Defecto 2 — el conteo de hallazgos sin trasladar no cuenta nada (línea 89)

Hoy: `([regex]::Matches($planTxt, '\|\s*Registrada\s*\|')).Count`

El libro de hallazgos escribe el estado entre acentos graves: `| G-O1 | … | \`Registrada\` | … |`. El regex exige `Registrada` pegado a la barra, así que **no cuenta ninguna fila** → `filas_de_hallazgos_sin_trasladar = 0` → la clase `cierre` puede declarar `listo` con hallazgos sin trasladar.

**Arregla:** que el patrón acepte el estado con o sin acentos graves.

## Reglas

- Cambio mínimo, solo `scripts/verificar.ps1`. Nada más.
- **No cambies los umbrales** (0,9 / 0,1), ni las clases, ni las preguntas: solo las dos rutas/patrones defectuosos.
- Comentario breve y en español junto a cada arreglo, diciendo qué corrigió y por qué.
- Nada de secretos. No abras `auth.json` ni ningún archivo de credenciales.

## Validación (obligatoria, en este orden)

1. **`pwsh`/`powershell -NoProfile -File` no aplica: el script necesita `OPENROUTER_API_KEY`.** En vez de llamar al verificador real, **prueba las dos funciones con un caso de prueba local y sin credenciales**: crea un script temporal **fuera del repositorio** (carpeta temporal de la sesión) que replique la expresión de cada línea corregida contra dos textos de entrada:
   - plan **con** `-plan` en el nombre y fila `` | X | `Registrada` | `` → debe encontrar **1** informe y contar **1** fila;
   - plan **sin** `-plan` y fila `| X | Registrada |` → debe encontrar **1** informe y contar **1** fila.
   Incluye las dos salidas reales en tu resumen. Borra el script temporal al terminar.
2. `git diff` de `scripts/verificar.ps1` para que se vea que solo cambiaron esas dos líneas.
3. `git status --short` para confirmar que no queda nada más sucio.

## Cierre

- Commit en `main` local, mensaje: `V: verificar.ps1 - nombre del informe sin sufijo -plan y conteo de Registrada con acentos graves`.
- **No push.**
- Escribe `resultados/V.md` en `2026-10-02-observaciones-victor-lote-3-briefs/resultados/` con: qué cambiaste, las dos salidas de prueba, el `git diff --stat`, y tus **hallazgos en las 4 categorías** (mejoras de trabajo · reglas de negocio · observaciones sobre la política · huérfanos). No edites el archivo del plan.
- Responde en **una línea**: commit, resultado de la validación y si queda algún pendiente.