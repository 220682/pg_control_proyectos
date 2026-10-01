# Pruebas de API con base simulada: alias, lógica pura y trampas del simulador

**Fecha:** 2026-10-01
**Origen:** Workers F1-B, F2-A, F2-D, F3-A, F3-B, F3-D, F3-E, F4-B, F4-C y F5-A del plan niveles-paquetes-plan-maestro-rdt
**Tarea relacionada:** `docs/02-trabajo-activo/01-planes/2026-09-30-niveles-paquetes-plan-maestro-rdt.md`
**Categoría:** `tests`

## Hallazgo

Probar rutas de API de la app (Next + Supabase) con `vitest` fue posible, pero con trampas repetidas en varios carriles:

1. **Alias `@/` en `vitest.config.ts`:** su ausencia impidió probar rutas de API directamente; los carriles sacaron la lógica a funciones puras de `src/lib` (con imports relativos) y, al integrar, hubo que redirigir módulos con `vi.mock` relativo (unas 18 líneas de ruido). Definir el alias desde el primer carril lo evita.
2. **Simulador de Supabase:** `insert` debe asignar ids y guardarlos en la tabla para encadenar `select` posteriores; el simulador no persiste `update` (para probar «aprobar con disciplina» se sembró `disciplina_id` en las tablas simuladas); al revertir, copiar los valores previos antes de modificarlos (los objetos son referencias; un bug real de reversión salió así).
3. **Validar tipos numéricos en servidor:** `JSON.stringify(NaN)` da `null`; un `MOVER` aceptaba una posición inválida hasta que se validó el tipo.
4. **Archivos de medición fuera de `src/`:** un script de medición dentro de `src/` que ninguna entrada carga rompe `modulos-huerfanos.test.ts`; los scripts van en `scripts/`.
5. **Lint de React:** la regla `react-hooks/set-state-in-effect` obliga a derivar el estado de carga (por ejemplo, clave servicio + reintento) y a sanear en los manejadores, no en efectos.
6. **PowerShell:** `npx vitest` emite el aviso de Vite por stderr y marca exit 1 aunque pase; usar Bash con `VITE_CONFIG_NATIVE_IGNORE_WARNING=true`.

## Destino propuesto

Dejar como aprendizaje; el punto 1 y el 4 son candidatos a `docs/01-contexto-repositorio/04-pruebas-y-evidencia.md` si Victor lo aprueba.
