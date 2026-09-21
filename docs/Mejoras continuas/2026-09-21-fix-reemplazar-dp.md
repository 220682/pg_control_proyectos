# Fix — reemplazar_dp no borraba partidas/recursos viejos (2026-09-21)

## Contexto

Victor reportó: "no se puede reemplazar un DP creado" en el último deployment (commit `6ac3976`, `py_control_proyectos_web`).

## Diagnóstico

El commit `6ac3976` (`fix: permitir reemplazo DP y borrar dependencias`) creó la función `reemplazar_dp()` en `db/049_reemplazar_dp_desvincula_cronograma.sql`, llamada desde `src/lib/dp/guardar.ts` vía `admin.rpc('reemplazar_dp', {...})`.

**Causa raíz:** la función borraba `proyecto_dp` (cabecera) pero **nunca borraba `dp_partidas` ni `dp_recursos`** (las tablas reales con las partidas del presupuesto) antes de insertar las nuevas. Al reemplazar, las partidas viejas seguían en `dp_partidas` con el mismo `proyecto_id`; el INSERT de las partidas nuevas chocaba contra el `unique (proyecto_id, wbs)` y la transacción completa hacía rollback — el reemplazo simplemente no entraba, sin perder el DP anterior (por estar todo en una sola transacción) pero tampoco permitiendo el nuevo.

También faltaba borrar `dp_moi`, `dp_subpresupuestos` y `dp_paquetes` — sin `unique constraint`, ahí el síntoma habría sido duplicados silenciosos en vez de error.

## Fix

`db/050_fix_reemplazar_dp.sql` (`py_control_proyectos_web`) — mismo `reemplazar_dp()`, agregando el borrado completo del DP viejo antes de insertar:

```sql
delete from dp_paquetes where proyecto_id = p_proyecto_id;
delete from dp_subpresupuestos where proyecto_id = p_proyecto_id;
delete from dp_moi where proyecto_id = p_proyecto_id;
delete from dp_recursos where proyecto_id = p_proyecto_id;
delete from dp_partidas where proyecto_id = p_proyecto_id;
delete from proyecto_dp where proyecto_id = p_proyecto_id;
```

Mismo comportamiento atómico que ya tenía (todo en una transacción, revierte si algo falla después), solo que ahora limpia completo antes de insertar.

## Estado

- ✅ Commit local: `56f1abd` (`py_control_proyectos_web`)
- ✅ Migración aplicada en Supabase por Victor (2026-09-21)
- ⏳ Pendiente: verificar en vivo que el reemplazo de DP funciona correctamente (sin duplicados, cronograma vinculado se reconstruye bien)

## Mejoras a flujos

(vacío)
