# Resultados F5-H · Crear RDT lee la versión más reciente del Plan Maestro

**Skills revisados:** `cerrar-tanda` (aplicado). La app no tiene carpeta de Skills.

## Decisión aplicada (Victor, 2026-10-01)
Crear RDT (catálogo + validación de partes) lista las líneas de la versión MÁS RECIENTE del Plan Maestro (aprobada o borrador), por `creado_en`. El gate se conserva: sin una versión `APROBADO` no se puede crear RDT (`MENSAJE_SIN_PLAN_MAESTRO` intacto).

## Qué cambió
| Ítem | Estado | Evidencia |
|---|---|---|
| `src/app/api/rdts/catalogos/route.ts` | Conforme (pruebas) | Gate sobre `proyecto_plan_maestro` `.eq('estado','APROBADO')` (igual); líneas leídas de la versión más reciente `.order('creado_en', { ascending: false }).limit(1).maybeSingle()` sin filtro de estado. `construirCatalogoPlanMaestro` recibe `Boolean(planAprobado.data)` (gate) y las líneas del reciente |
| `src/lib/rdts/partes-paquetes-servidor.ts` `cargarPlanAprobado()` | Conforme (pruebas) | Mismo cambio. `aprobado` sigue significando «hay versión aprobada» (gate); `lineas` salen de la versión más reciente |
| `src/lib/rdts/rdt-paquetes.test.ts` | Conforme | Mock con filtros/orden/limit; caso nuevo: APROBADO viejo + BORRADOR reciente → líneas del reciente |
| `src/lib/rdts/partes-paquetes.test.ts` | Conforme | `baseSimulada` con `order`/`limit`; dos casos nuevos de `cargarPlanAprobado` |

**Columna verificada:** `proyecto_plan_maestro.creado_en timestamptz not null default now()` (db/037). El orden descendente por `creado_en` devuelve la versión más reciente. No hay otro nombre: `creado_en` es el real.

**No se tocaron** `consolidado/route.ts`, `curva-s/route.ts` ni `plan-maestro/route.ts` (PR, Dashboard y Curva S siguen leyendo la versión APROBADA; PV/EV sin cambios). `integracion-rdt.test.ts` no mockea estas consultas (solo funciones puras) y no requirió cambios.

## Evidencia
- `npx vitest run src/lib/rdts src/app/api/rdts`: 13 archivos, 160 pruebas verdes.
- `npx tsc --noEmit`: 0 errores.
- `eslint` de los 5 archivos tocados: sin problemas (0). El lint global tiene 9 errores preexistentes en archivos no tocados (componentes/layout), igual que en `main`.
- Commit en `local-worker-1` con `git add` explícito de los 4 archivos de código/prueba. Sin push ni merge.

## Hallazgos
- La tabla `proyecto_plan_maestro` también tiene columna `version int` (unique por proyecto), pero la decisión de Victor fija `creado_en` como criterio de «más reciente»; se usó `creado_en`.
- Los mocks de pruebas no tenían `limit` ni `order` con estado; se les agregó para reflejar la nueva consulta.

## Regla de negocio (destino: flujo 06 RDT)
«Crear RDT lista la versión más reciente del Plan Maestro (aprobada o borrador); sin versión aprobada no se puede crear RDT».

## Handoff
1. Verificación por pantalla pendiente: crear/editar un paquete tras aprobar y confirmar que aparece en Crear RDT.
2. Sin push ni merge; sin migraciones ni cambios de RLS.
3. PR, Dashboard y Curva S no cambian (PV/EV siguen sobre la versión APROBADA).

Mejoras de trabajo: ninguna nueva. Huérfanos: ninguno.

**Llamadas:** ~8.
