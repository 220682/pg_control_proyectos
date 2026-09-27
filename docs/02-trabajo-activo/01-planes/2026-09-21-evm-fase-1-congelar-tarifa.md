# EVM Fase 1 — Congelar tarifa al validar RDT (2026-09-21)

**Corrección (2026-09-21):** esta versión reemplaza una anterior con datos incorrectos (tabla `rdt_partes_tarifa_congelada` y archivo `047_rdt_partes_tarifa_congelada.sql` inventados, sin verificar contra el código real). Contenido corregido contra el commit real `523f11a`.

## Contexto

Extensión de Fase 0. Mismo precedente que `plan_maestro_partidas` (`037_plan_maestro.sql`), que ya congela `precio_unitario` para no perder la línea base cuando el DP cambia: `reemplazar_dp()` borra y recrea `dp_recursos`, así que sin congelar, reimportar un presupuesto reescribiría hacia atrás el costo real de RDT ya validados.

Congela la tarifa (S/. o USD por HH / por HM, según moneda del DP) directamente sobre el RDT al momento de Validarlo — para que EV y AC usen la tarifa vigente en ese momento, no la tarifa actual del DP (que puede cambiar después).

## Implementación (commit `523f11a`)

### Migración `db/047_rdt_tarifas.sql`
✅ **Aplicada en Supabase**

No crea tabla nueva — agrega columnas a tablas ya existentes:
- `rdt_tareo.tarifa_hh` (numeric) — la tarifa es del cargo de esa persona en ese parte, constante entre sus actividades; el costo por celda sale de `rdt_tareo_horas.horas * rdt_tareo.tarifa_hh`
- `rdt_equipos_parte.tarifa_hm` (numeric) — `rdt_equipos_parte` ya tenía `horas` directo en la fila, la tarifa va ahí mismo

**Nota de diseño:** ambas columnas quedan `NULL` para RDT ya validados antes de esta migración (no hay forma de reconstruir la tarifa retroactivamente) y para cargos de mano de obra indirecta (MOI, `dp_moi`), que nunca se valorizan por diseño — `NULL` en `tarifa_hh` no siempre significa dato faltante.

### Lógica en API (`src/lib/dp/tarifas-servidor.ts`, `src/lib/dp/tarifas.ts`)
- `src/app/api/proyectos/[id]/dp/route.ts` y `src/app/api/rdts/partes/[id]/route.ts` — al validar RDT, resuelve la tarifa vigente de `dp_recursos` para cada cargo/equipo del parte y la congela en las columnas nuevas

### Tests
✅ `src/lib/dp/tarifas.test.ts` — 120 líneas de tests nuevos

## Verificación

✅ Según checklist "EVM Plan Maestro — Fase 1" en Punch List: 5 ítems, 3 Conforme, 2 sin verificar (requieren caso armado a propósito: cargo/equipo sin tarifa en el DP, o DP con precio distinto al que traía antes).

## Resultados

**CERRADO 100%** (confirmado por Victor, 2026-09-21).

La cadena Fase 0 + Fase 1 asegura que cada RDT validado tenga tarifa congelada y trazable para los cálculos de EVM (Fase 3 pendiente: EV/AC/CV/CPI/SPI/Curva S).

## Commits

- **py_control_proyectos_web**: `523f11a` — `db/047_rdt_tarifas.sql` + lógica de congelación + tests

## Mejoras a flujos

(vacío)

---

## Mejoras (de trabajo)

Ninguna identificada en esta tarea.

## Reglas de negocio acordadas en esta tarea

- Tarifa congelada al validar el RDT (no recalculada retroactivamente si el catálogo cambia después) → ya documentada en [docs/Flujos de trabajo/21-curva-s.md](../Flujos%20de%20trabajo/21-curva-s.md) ("tarifa congelada al validar (EVM Fase 1)").

## Resumen de checklist (migrado)

> Migrado desde `docs/Tareas de implementacion/resumen-checklists.md` (eliminado, decisión 6 de §6.1 del plan de reestructuración documental, 2026-09-27). Fila original — Flujo 020, Plan Maestro, #4:

| Fecha | Fase / sub-lote | Checklist (Punch List) | Ítems | Conforme | Observado | Sin verificar | Estado |
|---|---|---|---|---|---|---|---|
| 2026-09-21 | EVM Fase 1 — Congelar tarifa al validar RDT | "EVM Plan Maestro — Fase 1: congelar tarifa al Validar RDT" | 5 | 5 | 0 | 0 | **Cerrado 100%** |
