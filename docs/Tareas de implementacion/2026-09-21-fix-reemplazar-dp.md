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

- ✅ Commit `56f1abd` → pusheado a `origin/main` (`py_control_proyectos_web`), incluido en el deploy
- ✅ Migración `050_fix_reemplazar_dp.sql` aplicada en Supabase por Victor (2026-09-21)
- ✅ Verificado en vivo por Victor (2026-09-21): el reemplazo de DP funciona correctamente

**CERRADO 100%.**

## Semilla de catálogo — Presupuesto de prueba 01 (mismo día)

Al revisar el flujo de DP se aprovechó para cargar cargos/equipos del archivo `Informacion para pruebas/PPTO-prueba N°01.xlsx` (hoja APU) que no estaban en el catálogo maestro `recursos_cargos`/`recursos_equipos`.

**SQL**: `db/051_semilla_cargos_equipos_ppto_prueba01.sql` (`py_control_proyectos_web`)
- Cargos nuevos: OFICIAL MECANICO, OPERARIO ARMADOR, OPERARIO MECANICO, OPERARIO SOLDADOR, OPERARIO TERMOFUSIONISTA HDPE
- Equipos nuevos: ESMERIL ANGULAR 4 1/2", ESMERIL ANGULAR 7", MAQUINA DE SOLDAR, MAQUINA DE TERMOFUSION HDPE (ALQUILER)
- (CAPATAZ y CAMION BARANDA ya existían, no se duplicaron)

**Estado**: ✅ Corrido en Supabase por Victor y verificado — el sistema reconoció los cargos/equipos correctamente al importar el DP de prueba (flujo de conciliación de EVM Fase 0). Commit `2dacb22` → pusheado a `origin/main`.

## Mejoras a flujos

(vacío)

---

## Mejoras (de trabajo)

Ninguna identificada en esta tarea.

## Reglas de negocio acordadas en esta tarea

Ninguna nueva — fue un fix de bug (`reemplazar_dp` no borraba partidas/recursos viejos al reimportar), no introdujo una regla de negocio nueva. El comportamiento correcto (reemplazar_dp reconstruye completo, sin dejar residuos) es el esperado por diseño, ya implícito en [docs/Flujos de trabajo/09-importar-dp.md](../Flujos%20de%20trabajo/09-importar-dp.md).
