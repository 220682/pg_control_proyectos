# Entorno Windows (npm bloqueado, Playwright sin `file://`) y cómo delegar a Workers

**Fecha:** 2026-10-16
**Origen:** Orquestador, Worker git y Worker CR-1 · C0 del plan `2026-10-15-cronograma-gantt-linea-base-histogramas` (hallazgos M1, M2 y M3)
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-10-15-cronograma-gantt-linea-base-histogramas.md`
**Categoría:** `entorno/windows` y `delegacion/modelos`

## Origen

Durante la ola 0 y la ola 1 del plan: al preparar la carpeta de trabajo `local-worker-4`, al verificar la maqueta con Playwright y al revisar la primera entrega de un Worker Haiku.

## Observaciones

1. **`npm ci` falla con EPERM en Windows (M1).** Al borrar `node_modules/lightningcss-win32-x64-msvc/lightningcss.win32-x64-msvc.node`, `npm ci` falla si algún proceso mantiene abierto el archivo. Se comprobó con una apertura exclusiva (`File.Open` con `FileShare.None`) que seguía bloqueado; no se pudo identificar qué proceso lo retenía (el que el Worker sospechó ya no existía). Lo que sí funcionó: **renombrar** la carpeta `node_modules` (el renombre se permite aunque el archivo esté abierto) a una carpeta aparte, en un lugar ignorado por git, y correr `npm ci` de nuevo. La carpeta sobrante no se borra sin aprobación; se reporta como huérfana.
2. **Playwright del entorno no abre `file://` y solo guarda capturas dentro del repositorio (M2).** Se sirve la carpeta con `python -I -m http.server <puerto> --bind 127.0.0.1` en segundo plano y se detiene al terminar. En Git Bash no existe `pkill`: usar PowerShell (`Get-NetTCPConnection -LocalPort <puerto>` y `Stop-Process`). Las capturas se guardan con `filename` dentro de `.playwright-mcp/`.
3. **Delegar con lecturas exactas y el modelo adecuado (M3).** Un Worker Haiku al que solo se le dijo «el brief dice qué leer» leyó `design.md` completo y varias maquetas: su contexto llegó a 308k y entregó un acabado básico (sin leyenda ni títulos de ejes) que el Orquestador no detectó porque solo probó la vista por defecto. Victor pidió: «delega bien, dile qué leer». Práctica: el prompt de lanzamiento lista los archivos con rangos de líneas y dice qué **no** leer; Haiku solo para tareas simples de brief cerrado (git, documentación, entorno); Sonnet cuando hay criterio visual o lógica; al revisar una entrega de interfaz, probar también el caso con filtros y el ancho real de pantalla de Victor (~1873 px, paneles ocultos).

## Evidencia

- Plan, libro de hallazgos: filas M1, M2 y M3 (`2026-10-15-cronograma-gantt-linea-base-histogramas.md`).
- Medición del 2026-10-15 con `python -I scripts/medir.py --resumen --desde 2026-10-15`: la sesión de C0 (Haiku) llegó a 308k de contexto; la de C7 (Sonnet, con lecturas acotadas), a 201k.
- Resumen de cierre de C0 (`resultados/C0.md`, hallazgo C0-H1).

## Clasificación

Mejora de trabajo (workaround de herramienta y práctica de delegación). No es una regla de negocio.

## Etiqueta de categoría

`entorno/windows`, `delegacion/modelos`

## Destino propuesto

Queda como aprendizaje. La práctica de delegación (3) es candidata a promoverse a `00-estandar-agentes/` (sección de briefs y lanzamiento de Workers) y a la plantilla `13-brief-de-tanda.md`, para que «qué leer» incluya rangos de líneas. Decide el Auditor y Victor en el Gate 2.

## Cambio propuesto

Agregar a la plantilla de brief de tanda: «Qué leer: archivo y rango de líneas; Qué NO leer: lista explícita», y a las notas de entorno Windows el workaround de `node_modules` renombrado.

## Estado

`Borrador` — pendiente de revisión del Auditor.

## Referencia a la aprobación

Pendiente (Gate 2 de Victor).
