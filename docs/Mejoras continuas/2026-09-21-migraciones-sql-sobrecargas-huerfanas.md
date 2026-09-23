# Mejora de trabajo — `CREATE OR REPLACE FUNCTION` deja sobrecargas huérfanas si cambia la firma

> Origen: tarea [2026-09-21-pr-fase-2-pipeline-linea-base.md](../Tareas%20de%20implementacion/2026-09-21-pr-fase-2-pipeline-linea-base.md), sección "Archivos y código que quedaron viejos". Extraído el 2026-09-23.

## Qué pasó

`CREATE OR REPLACE FUNCTION` en Postgres solo reemplaza una función cuando la firma (tipos y orden de parámetros) coincide exacto. Cada vez que una migración de `reemplazar_dp()` agregó un parámetro opcional nuevo al final, Postgres creó una función **nueva** en vez de reemplazar la anterior, porque la firma ya no coincidía. Resultado: 4 sobrecargas viejas de `reemplazar_dp` (9, 10, 11 y 12 parámetros) quedaron vivas en la base junto a la vigente (13 parámetros), y `pg_get_functiondef('reemplazar_dp'::regproc)` empezó a fallar por ambigüedad ("more than one function named...").

## Cómo se detectó y resolvió

Se identificó que nadie corría el `DROP FUNCTION` de la versión vieja al agregar un parámetro. Se eliminaron las 4 sobrecargas huérfanas con una migración dedicada, autorizada explícitamente por Victor, y se verificó que la función quedara sin ambigüedad.

## Cómo evitarlo a futuro

Al agregar un parámetro nuevo a una función existente (con `default` para no romper llamadas viejas), verificar si la firma cambió — si cambió, incluir un `DROP FUNCTION <firma_vieja>` explícito en la misma migración, no confiar en que `CREATE OR REPLACE` la reemplace sola.
