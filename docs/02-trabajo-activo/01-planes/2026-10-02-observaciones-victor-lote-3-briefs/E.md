# Brief Tanda E — Worker 2 (`qwen3.8-flash` si va directa; escalar a Plus solo si bloquea)

**Plan:** `2026-10-02-observaciones-victor-lote-3-plan.md` · **Carril:** rama `local-worker-4`, worktree `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\local-worker-4` (NO ramas nuevas, NO `main`, NO merge, NO push). **Precondition:** aplica TÚ la migración `091` (`db/091_plan_maestro_declaracion_paquete.sql`) siguiendo `2026-09-30-niveles-paquetes-plan-maestro-rdt-briefs/00-protocolo-migraciones.md` (candado, transacción, conteos antes/después, script `migrar_E.py` fuera del repo, sin secretos en salida; si el clasificador la deniega: NO la rodees — déjala lista, anota el comando exacto y detente). Verifica después en `information_schema` que las 3 columnas existen en `plan_maestro_partidas`.

## Qué hacer (solo esto)

Completar la UI del Lienzo del Plan Maestro (`F4-C/F4-D pendientes`, ver plan § "Pendiente para completar F4-C/D en la UI real"):

1. **Celdas editables (verde)** en filas con `esDeclaracionPaquete = true` para editar `metradoPaquete`; las partidas comunes muestran el metrado contractual como **texto plano no editable** (corrección de Victor, 2026-10-02). Guardar debe persistir por la API ya actualizada (`8b33cdd`).
2. **Indicador rojo** en `fechaInicio`/`fechaFin` cuando estén fuera del rango visible del lienzo; fechas editables.

## Reglas

- No tocar RDT, Cronograma, ni `middleware.ts`. Archivos esperados: `FormularioPlanMaestro.tsx` / `LienzoPlanMaestro` y su lógica de celdas; la API solo si falta el campo.
- Recordatorio (G-M2/G-O1): tsc/vitest con mock no prueban esquema — after coding, **una llamada viva** (SSR GET + PATCH/POST de guardado con valor neutro restaurado, técnica del aprendizaje 2026-10-02, dev en el puerto del worktree) sobre un servicio de prueba.
- Validación: `npx tsc --noEmit` · `npx vitest run src/lib/plan-maestro` (115 verdes de base) · verificación en vivo.
- Commits claros en `local-worker-4`. Cierre en `resultados/E.md` (qué hiciste, salidas, hallazgos en las 4 categorías, pendientes).
