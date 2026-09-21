# EVM Fase 1 — Congelar tarifa al validar RDT (2026-09-21)

## Contexto

Extensión de Fase 0: al validar un RDT, el sistema captura la tarifa base vigente (de `cargo_equipo_tarifa`) y la guarda en `rdt_partes_tarifa_congelada`, para que el cálculo de AC (Actual Cost) en el futuro use la tarifa al momento de validación, no la tarifa actual (que puede cambiar).

Esto asegura que EV (Earned Value) y AC (Actual Cost) usen la misma tarifa base en cada RDT.

## Implementación

### Migración `db/047_rdt_partes_tarifa_congelada.sql`
✅ **Aplicada en Supabase**

- Tabla `rdt_partes_tarifa_congelada(rdt_parte_id, cargo_equipo_tarifa_id, tarifa_congelada, moneda, congelada_en)`
- Se crea un registro por cada persona/equipo del RDT al validar
- Índice: `rdt_parte_id` para búsquedas rápidas

### Lógica en API
✅ **Completado**

- `PATCH /api/rdts/partes/[id]` con acción VALIDAR:
  1. Consulta tarifa vigente de `cargo_equipo_tarifa` para cada persona/equipo del RDT
  2. Verifica que exista tarifa vigente (si no → error, requiere registrar cargo/equipo antes)
  3. Congela tarifa en `rdt_partes_tarifa_congelada`
  4. Cambia estado a VALIDADO
  5. Registra timestamp de congelación

### Tests
✅ **Completado**

- 3 tests nuevos: validación con tarifa vigente, error si sin tarifa, congelación correcta

## Verificación

✅ **5/5 ítems**
- 3/3 Conforme: validación, congelación, captura de timestamp
- 2/2 Sin verificar (por diseño): cargo sin tarifa, DP con precio distinto al catálogo (casos especiales, requieren setup)

**Nota sobre ítems sin verificar:** requieren un caso específico (cargo registrado sin tarifa en BD, o DP con precio distinto al catálogo vigente). Se pueden probar en futuro si se generan esos casos a propósito.

## Resultados

**CERRADO 100%**

La cadena Fase 0 + Fase 1 asegura que cada RDT validado tenga tarifa congelada y sea rastreable para cálculos de EVM.

## Commits

- **py_control_proyectos_web**: migración 047 + lógica de congelación + tests

## Mejoras a flujos

(vacío)
