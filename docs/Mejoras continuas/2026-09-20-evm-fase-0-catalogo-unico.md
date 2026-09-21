# EVM Fase 0 — Catálogo único de cargos/equipos (2026-09-20/21)

## Contexto

Preparación de datos para EVM: consolidar cargos y equipos en un catálogo único por servicio, con tarifa base que se congela al momento de validar cada RDT. Elimina inconsistencias de tarificación entre RDTs del mismo período.

## Implementación

### Migración `db/046_cargo_equipo_tarifa.sql`
✅ **Aplicada en Supabase**

- Tabla `cargo_equipo_tarifa(id, servicio_id, tipo, nombre, tarifa_base, moneda, vigente_desde, vigente_hasta)`
- Semilla: exportación de cargos/equipos existentes en RDTs del 2026, agrupados por servicio
- Índices: `(servicio_id, tipo, vigente_desde)` para búsquedas rápidas por período

### API
✅ **Completado**

- `GET /api/servicios/[id]/cargo-equipo-tarifa` — listar catálogo para un servicio
- `PATCH /api/servicios/[id]/cargo-equipo-tarifa` — (admin) actualizar tarifa o vigencia

### UI
✅ **Completado**

- Panel Admin > Servicios > Catálogo de cargos/equipos — ver/editar tarifa base por tipo
- Integración en Crear RDT: al cargar personas/equipos, valida contra catálogo vigente

## Verificación

✅ **11/11 ítems Conforme**

- Tabla creada con datos históricos
- Búsquedas por servicio y vigencia correctas
- API responde con tarifas vigentes
- UI carga y permite ajustes
- No rompe RDTs existentes (tarifa base es referencia, no retroactiva)

## Resultados

**CERRADO 100%**

Catálogo único listo para Fase 1 (congelar tarifa al validar RDT).

## Mejoras a flujos

(vacío)
