# Brief Tanda M — Worker (migraciones `090` → `091` → `092`)

**Plan:** `2026-10-02-observaciones-victor-lote-3-plan.md` · **Precondición de las tandas E y F.** Aplicar tres migraciones ya escritas, revisadas y documentadas en `db/README.md` (filas 68-70).

## Leer antes

- **Protocolo de migraciones (norma):** `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/00-protocolo-migraciones.md`
- **Ruta de las credenciales:** `D:\1 Nueva carpeta\todo\DIARIO\entorno_variable.txt` (movida el 2026-10-03; la ruta anterior `C:\Users\BRANDY\Downloads\DIARIO` **ya no existe**).

## Qué hacer

1. Conéctate y comprueba `select 1`.
2. Aplica **de una en una y en este orden**: `db/090_ampliar_catalogo_disciplinas.sql` → `db/091_plan_maestro_declaracion_paquete.sql` → `db/092_rdt_declaracion_paquete.sql`. Una transacción por archivo.
3. **Candado:** crea `resultados/CANDADO-MIGRACIONES.txt` con `set -o noclobber` antes de la primera; bórralo al terminar, aunque falle. Si ya existe y tiene menos de 30 minutos, no lo rompas: detente y avisa.
4. **Script de un solo uso** con nombre `migrar_M.py`, Python con `psycopg2`, **fuera del repositorio** (carpeta temporal de la sesión) y **borrado al terminar**. Lee el valor de la variable **dentro del proceso**: no lo imprimas, no lo pases como argumento de línea de comandos, no abras ni muestres `entorno_variable.txt`.
5. **Conteos antes y después** de las tablas que toca cada archivo: `catalogo_disciplinas`, `plan_maestro_partidas`, `rdt_actividades`. Los datos existentes **no pueden cambiar**.

## Verificación obligatoria (sin esto la tanda no está cumplida)

- `information_schema.columns`: las 3 columnas de `plan_maestro_partidas` (`es_declaracion_paquete`, `metrado_paquete`, `fecha_inicio`, `fecha_fin`) y las 2 de `rdt_actividades` (`es_declaracion_paquete`, `metrado_paquete`) existen.
- `catalogo_disciplinas` tiene **8 filas** y las tres nuevas son Preliminares, Cierre y Subcontratos.
- Conteos antes/después idénticos en las tres tablas.
- `git status --short` en el repo de la app: **sin cambios** (esto solo aplica migraciones, no escribe código).

## Si algo falla

**Detente y avisa; no improvises.** No busques otras credenciales, no uses la llave REST de servicio para forzar cambios de estructura, no toques datos de ningún servicio. Si el sistema pide aprobación o deniega el script, **no lo rodees**: déjalo listo, anota el comando exacto en tu resultado y detente.

## Cierre

- `resultados/M.md` en esta carpeta (`resultados/`): archivo, vía usada (directa o API de administración), hora, verificación, conteos antes/después. **Ningún valor secreto.**
- Confirma en una línea si el **árbol de git del repo de la app sigue limpio**.
- Hallazgos en las **4 categorías** (mejoras · reglas · observaciones sobre la política · huérfanos). No edites el archivo del plan.