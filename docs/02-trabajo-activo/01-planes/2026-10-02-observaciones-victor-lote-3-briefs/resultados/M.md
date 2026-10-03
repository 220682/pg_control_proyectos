# Resultado Tanda M — migraciones 090 → 091 → 092

**Worker:** M · **Hora:** 2026-10-03 00:35:45 – 00:35:49 · **Vía:** directa (`PR_DB_URL`, psycopg2).

## Migraciones aplicadas (una transacción por archivo, en orden)

| # | Archivo | Resultado |
|---|---------|-----------|
| 1 | `090_ampliar_catalogo_disciplinas.sql` | OK — commit exitoso |
| 2 | `091_plan_maestro_declaracion_paquete.sql` | OK — commit exitoso |
| 3 | `092_rdt_declaracion_paquete.sql` | OK — commit exitoso |

## Conteos antes / después

| Tabla | Antes | Después | ¿Cambio? |
|-------|------:|--------:|----------|
| `disciplinas` | 5 | 8 | +3 (Preliminares, Cierre, Subcontratos) — esperado |
| `plan_maestro_partidas` | 267 | 267 | sin cambio |
| `rdt_actividades` | 104 | 104 | sin cambio |

## Verificación de columnas (information_schema.columns)

6 de 6 esperadas:

- `plan_maestro_partidas.es_declaracion_paquete` ✓
- `plan_maestro_partidas.metrado_paquete` ✓
- `plan_maestro_partidas.fecha_inicio` ✓
- `plan_maestro_partidas.fecha_fin` ✓
- `rdt_actividades.es_declaracion_paquete` ✓
- `rdt_actividades.metrado_paquete` ✓

## Verificación de disciplinas nuevas

Total = 8. Nuevas confirmadas: Preliminares, Cierre, Subcontratos. ✓

## Estado del árbol de git (repo de la app)

`git status --short` en `py_control_proyectos_web`: **sin cambios** (árbol limpio). ✓

## Limpieza

- Script temporal `migrar_M.py`: borrado. ✓
- Candado `CANDADO-MIGRACIONES.txt`: borrado. ✓

## Hallazgos (4 categorías)

- **Mejoras de trabajo:** ninguna.
- **Reglas de negocio acordadas:** ninguna (esta tanda solo aplica migraciones ya escritas).
- **Observaciones sobre la política:** el brief dice `catalogo_disciplinas` pero la tabla real se llama `disciplinas` (creada en 085). No bloqueó, pero conviene alinear el nombre en el brief para que el siguiente Worker no dude.
- **Huérfanos:** ninguno.
