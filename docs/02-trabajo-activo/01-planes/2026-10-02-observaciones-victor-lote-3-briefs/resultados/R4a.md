# R4a — Reposicionar los RDT al aprobar un Plan Maestro nuevo

Rama/worktree `local-worker-4`. Sin push, sin merge a `main`. Sin conexión a la base.

## Qué se hizo

1. **Módulo nuevo** `src/lib/rdts/reposicionamiento.ts` (función **pura** `calcularReposicionamiento`) y `src/lib/rdts/reposicionamiento-servidor.ts` (`aprobarPlanMaestroConReposicionamiento`).
2. **Migración** `db/093_aprobar_plan_maestro_reposicion.sql`: función `aprobar_plan_maestro_con_reposicionamiento(uuid, uuid, jsonb)` que en una sola transacción marca el plan anterior `REEMPLAZADO`, marca el nuevo `APROBADO`, reposiciona los RDT (re-vínculo de la clave de reporte), escribe una fila de historial por RDT afectado y ejecuta `recalcular_pr_planificado` (U8). Amplía el CHECK de `rdt_partes_historial.accion` con `REPOSICIONAMIENTO`.
3. **Ruta** `src/app/api/plan-maestro/route.ts` (`PATCH`, `accion: 'APROBAR'`): reemplaza las tres llamadas HTTP sueltas por una sola llamada a la función transaccional.
4. **Tipos/UI del historial**: `historial.ts`, `src/app/api/rdts/partes/[id]/historial/route.ts` y `ModalHistorialRdt.tsx` conocen `REPOSICIONAMIENTO`.
5. **`db/README.md`**: fila 71 de la migración 093.
6. **Pruebas**: pura (`reposicionamiento.test.ts`, incluye caso `VALIDADO`, caso «no afectado», diff de la fila de historial, sin línea/ambigua), de la migración sin base (`reposicionamiento-sql.test.ts`) y de la ruta (`plan-maestro-api.test.ts`: llama a la función, 200; fallo del reposicionamiento → 400 y el plan no queda aprobado).

### Interpretación de «re-vínculo» (verificada en código)

No existe una FK directa RDT → línea del Plan Maestro. El real de un RDT se ubica en el lienzo por **clave de reporte** `(paquete_trabajo_id|DIRECTA):dp_partida_id` (`real-por-clave.ts`, `declaracion-paquete.ts`), estable entre versiones. Por eso el reposicionamiento **solo actualiza la asociación de paquete** (`rdt_actividades.paquete_trabajo_id` y `rdt_actividad_partidas.paquete_trabajo_id`) para que el RDT caiga en la clave del plan vigente. No toca `metrado_ejecutado`, ni horas, ni `estado_validacion`. El PR consolida por `wbs`/`dp_partida_id` (`db/053`, `db/061`), así que sus cifras no cambian.

## Qué NO se hizo

- **La migración 093 NO se aplicó** ni se probó contra la base (lo hace el Orquestador en R4b).
- No se tocó `dp_partida_id` de los vínculos (solo el paquete). No se recalcularon filas derivadas (cambiaría cifras del PR).
- No se hizo push ni merge.

## Validaciones (salida real)

- `npx tsc --noEmit` → exit 0 (sin salida).
- `npx vitest run` → `Test Files 106 passed (106)`, `Tests 1094 passed (1094)`, `Duration 18.75s`.
- `npx eslint` sobre los 8 archivos tocados → sin salida (limpio).
- Migración validada **leyéndola** y con prueba sin base (`reposicionamiento-sql.test.ts`): firma correcta, incluye `perform recalcular_pr_planificado`, CHECK con `REPOSICIONAMIENTO` idempotente, no contiene `set metrado_ejecutado`, `set ... horas`, `set estado_validacion`, `delete from`, `drop table` ni `truncate`.
- `git status --short` → solo `_protocolo-migraciones.md` sin trackear (preexistente, no commiteado). `R4a-resultado.md` sin commitear.

## Commits

- `11804b6` R4: migracion 093, aprobacion transaccional del Plan Maestro con reposicion de RDT y recalculo del PR (E1/U4/U7/U8)
- `56c66e0` R4: modulo de reposicionamiento de RDT (regla pura + servidor) y pruebas
- `d7d96fd` R4: la aprobacion del Plan Maestro usa la funcion transaccional y el historial muestra REPOSICIONAMIENTO

## Hallazgos

### Mejoras de trabajo
- El servidor relee todos los RDT del servicio en cada aprobación (lotes de 200) para calcular el diff; conviene mover el cálculo a la función SQL o filtrar por vínculos → `plan de mejoras / rendimiento`.
- `FilaHistorialRdt.accion` seguía sin incluir `BORRADO` (existe en el CHECK desde db/053); la unión TS está desalineada con la base → `deuda técnica / tipos`.
- La regla de reposicionamiento vive dos veces (pura en TS y aplicada en SQL); el TS es la fuente de verdad y el SQL aplica el payload → `nota de diseño`.

### Reglas de negocio
- El reposicionamiento resuelve solo por `dp_partida_id`; si un RDT apunta a un `dp_partida` que ya no está en el plan (p. ej. tras reemplazo de DP), queda «sin línea» y no se re-vincula por WBS → `aclaración de Victor / plan`.
- Una partida presente en dos líneas del plan con paquetes distintos es «ambigua» y no se reposiciona; falta definir el desempate → `regla de negocio`.
- Las filas derivadas también cambian de paquete pero no recalculan su metrado (cambiaría el PR); si el plan reagrupa partidas, el set derivado puede quedar inconsistente → `regla/validación`.
- No se reescribe `metrado_ejecutado` derivado, así que el % puede haber quedado calculado sobre el plan viejo; falta decidir si debe recalcularse → `aclaración de Victor`.

### Observaciones sobre la política
- El `_protocolo-migraciones.md` dice que los Workers aplican las migraciones de su rango, pero el brief de R4a prohíbe conectarse a la base y lo deja a R4b → `actualizar protocolo/plan`.
- U8 exige «todo o nada», pero hasta esta tanda la aprobación no era transaccional; conviene un ítem de revisión que prohíba llamadas sueltas en flujos de aprobación → `checklist de revisión`.

### Huérfanos
- `_protocolo-migraciones.md` sigue sin trackear en el worktree (preexistente), no commiteado → `decisión del Orquestador`.
- La migración 093 queda sin aplicar hasta R4b → `tanda R4b`.
- `R4a-resultado.md` sin commitear por indicación del brief → `no commitear`.
