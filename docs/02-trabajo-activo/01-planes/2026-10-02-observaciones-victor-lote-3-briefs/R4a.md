# Brief Tanda R4a — Reposicionar los RDT al aprobar un Plan Maestro nuevo (código y pruebas)

**Plan:** `pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-lote-3-plan.md`, Enmienda E1, reglas U4, U7 y U8. Gate 1 Complementario de Victor del 2026-10-03.
**Rama y worktree:** `local-worker-4`, en el directorio desde el que corres. **Sin push. Sin merge a `main`.**
**Alcance de esta tanda:** escribir el código, la migración y las pruebas, y validarlos. **NO te conectes a la base de datos y NO apliques la migración**: eso lo hace el Orquestador en la tanda R4b, con el protocolo de migraciones. No leas ni escribas nada fuera de este worktree.

## La regla, con las palabras de Victor (2026-10-04)

> «Cargo los datos que se extrajeron del RDT para reposicionarlos en el nuevo Plan Maestro. Pero lo que no se está entendiendo hasta ahora es que, aunque se cambie el Plan Maestro, **el PR sigue conservando los datos de todos los RDTs porque estos no se han cambiado**. Lo que se cambia es **la forma en que se muestran en el Plan Maestro**; no cambia la forma en que están declarados en el PR consolidado.»

Traducido a regla implementable:

| # | Qué hace el reposicionamiento |
|---|---|
| **Sí** | Al aprobar un Plan Maestro nuevo, cada RDT del servicio se vuelve a **asociar a las líneas del plan vigente**, para que el Plan Maestro muestre ese RDT en las **fechas y metrados del plan nuevo** |
| **No** | **No** se reescribe `metrado_ejecutado` de los RDT, ni las horas reales, ni las fotos, ni el historial de ejecución |
| **No** | **No** cambian las cifras del **PR consolidado**. El recálculo que ya se dispara al aprobar sigue ahí (U8), pero su resultado **no debe cambiar** por efecto del reposicionamiento |
| **Rastro** | Cada RDT afectado deja una entrada en su **historial** (`rdt_partes_historial`) con qué se movió, por qué, a qué fecha y metrado, y quién aprobó el Plan Maestro (U7) |
| **Alcance** | **Todos** los RDT del servicio, **incluidos los `VALIDADO`** (U4). El RDT no cambia de `estado_validacion` |
| **Orden** | U8: **Plan Maestro → reposicionamiento → recálculo del PR**, y es **todo o nada**: si algo falla, no queda nada aprobado |

## Qué hacer

1. **Verifica antes de escribir.** Lee y confirma en el código: dónde está la acción de aprobación, cómo se llama hoy al recálculo del PR, qué tablas vinculan un RDT con las líneas del plan, y qué admite el historial. Si algo de eso no existe como se supone, **detente y repórtalo**; no lo inventes.
2. **`db/093_*.sql`** (solo el archivo, sin aplicarlo): una función PL/pgSQL que en **una sola transacción** marque el plan anterior `REEMPLAZADO`, marque el nuevo `APROBADO`, reposicione los RDT (re-vínculo) y escriba el historial. Si `recalcular_pr_planificado` es una función de Postgres, inclúyela dentro para que U8 sea verdad; si es lógica de TypeScript, **no la metas** y anótalo como riesgo residual. Si el historial exige un valor nuevo en `accion`, amplía su CHECK en la misma migración. **Actualiza `db/README.md`** con la fila de la 093.
3. **Módulo nuevo en `src/lib/rdts/`** con la lógica de reposicionamiento: una función ** pura** (testeable sin base) y la de servidor.
4. **`src/app/api/plan-maestro/route.ts`:** la acción `APROBAR` llama a la función nueva en vez de a las llamadas sueltas. Actualiza `plan-maestro-api.test.ts`, que hoy afirma las llamadas sueltas.
5. **Pruebas:** unitarias de la función pura (caso `VALIDADO` incluido, caso «RDT no afectado no cambia», caso de la fila de historial con el diff) y de la ruta (que la aprobación llama a la función y devuelve 200; que un fallo del reposicionamiento no deja el plan aprobado).

## Anclajes verificados (úsalos, no los re-descubras)

- Aprobación: `src/app/api/plan-maestro/route.ts`, `PATCH`, `accion: 'APROBAR'`; `update({estado:'APROBADO', aprobado_por_id, aprobado_en})` y luego el `rpc('recalcular_pr_planificado')`.
- Historial append-only: tabla `rdt_partes_historial`; se lee en `src/app/api/rdts/partes/[id]/historial/route.ts` y `src/lib/rdts/historial.ts`; migraciones `db/041`, `db/042`, `db/053`.
- Plan y líneas: `db/037_plan_maestro.sql`, `db/091_plan_maestro_declaracion_paquete.sql`, `src/lib/plan-maestro/lineas.ts`, `src/lib/plan-maestro/plan-maestro.ts`.
- RDT: `src/lib/rdts/declaracion-paquete.ts`, `src/lib/rdts/real-por-clave.ts`, `src/lib/rdts/partes-paquetes-servidor.ts`, `db/083_rdt_filas_derivadas.sql`, `db/026_rdt_estructurado.sql`.
- PR: `db/061_pr_planificado_plan_maestro.sql`, `db/053_pr_motor_rdt.sql`, `src/lib/pr/evm.ts`, `src/lib/pr/acumulacion-rdt.ts`.
- Un benchmark del 2026-10-04, con tres modelos distintos, coincidió en un punto: hoy la aprobación son llamadas HTTP sueltas a Supabase y **eso no es una transacción**; de ahí la función.

## Validación obligatoria antes de cerrar

1. `npx tsc --noEmit` → exit 0.
2. `npx vitest run` → suite completa en verde, con el conteo real.
3. La migración se valida **leyéndola y con una prueba que no dependa de la base**: escribe el `.sql` para que sea seguro aplicarla en un solo paso.
4. `git status --short` → solo los archivos de la tanda. Un commit por paso lógico, con mensajes que empiecen por `R4:`.

## Entrega

Escribe `R4a-resultado.md` en la raíz del worktree, **sin commitearlo**, con: qué se hizo, qué NO se hizo (sobre todo: la migración no se aplicó), las validaciones con su salida real, los commits, y los **hallazgos en las cuatro categorías** (mejoras de trabajo · reglas de negocio · observaciones sobre la política · huérfanos), uno por línea y con destino propuesto. No muevas hallazgos a sus destinos.
