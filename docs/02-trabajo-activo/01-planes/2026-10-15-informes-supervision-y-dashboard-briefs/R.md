# Brief — Tanda R: AC con materiales y subcontratos (migración 102, PR, Curva S y evm.ts)

## Rol, modelo y tanda

Worker 3, Sonnet, esfuerzo medio. Tanda R, Ola 1, carril W3 (después de O). Subagente «Worker 3 · R». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo). Es la cuenta más sensible del plan: cambia el AC de todo servicio existente.

## Ítems de la tanda (Punch List)

- **R1**: `db/102_ac_materiales_subcontratos.sql` y una línea en `db/README.md`. Aditiva, reversa en comentario. Columnas `proyecto_pr.costo_materiales_acum` y `costo_subcontratos_acum` (`numeric not null default 0`) y la función `ac_materiales_subcontratos_al_corte(p_proyecto_id uuid, p_ev_acum numeric, p_fecha date)` que devuelve `materiales` y `subcontratos`. Avance físico = `p_ev_acum` / Σ `pr_partidas.bac` (0 si el BAC es 0; **sin tope** en 100 %, decidido por Victor). Materiales = Σ `costo_contractual` de `pr_recursos` tipo `material` × avance. Subcontratos, por fila tipo `subcontrato`: `FISICO` (o sin fila en `pr_subcontrato_medicion`) = `costo_contractual` × avance; `MANUAL` = `monto_manual` si `p_fecha` es el día (Lima) de `actualizado_en` o posterior, y si no, el valor `FISICO` (decidido por Victor, no es pregunta). Es la **única** cuenta: el PR y la Curva S la llaman.
- **R2**: `create or replace recalcular_pr_desde_rdt`. Al final llama a la función con `p_ev_acum` = Σ `metrado_acumulado × precio_unitario` y `p_fecha` = hoy (Lima), guarda las dos columnas de `proyecto_pr` y escribe `pr_recursos.costo_acumulado` de cada fila de material y subcontrato (el reinicio de `costo_acumulado` que hoy cubre `mano_obra` y `equipo` se amplía a los cuatro tipos). `pr_partidas.costo_real_acum` no cambia. Prueba: caso hecho a mano (materiales 1 000 y subcontrato 200 con avance 30 % -> 300 y 60).
- **R3**: `create or replace curva_s_proyecto`: `ac_acum` = HH + HM acumuladas (`ac_diario_hh` y `ac_diario_hm`, ya con extra y stand-by de la 100) + materiales + subcontratos de la función con el `ev_acum` de cada día. Prueba: último punto de la serie = AC del PR al mismo corte.
- **R4**: `src/lib/pr/evm.ts`: `ProyectoEvmDatos` suma `costoMaterialesAcum` y `costoSubcontratosAcum`; AC del proyecto = Σ partidas + legacy + ambos; AC y CPI por partida no cambian; CPI y EAC del proyecto usan el AC nuevo. Prueba unitaria.
- **R5**: **corazón de la tanda.** `ac-equivalencia.test.ts` más un script SQL de comparación: (a) con RDT ya validados, la parte HH/HM (Σ `costo_real_acum` + legacy) sale idéntica antes y después de la 102; (b) el AC total de un servicio existente **sí cambia**: la prueba reporta el delta por componente (materiales, subcontratos), no exige AC idéntico; (c) AC del PR = último punto de la Curva S = AC que arma el cargador del Dashboard, al mismo corte; (d) escribir un monto manual de subcontrato cambia el AC exactamente en (monto − valor `FISICO` que tenía) y no cambia el EV; (e) los casos de `src/lib/pr/subcontratos*` (tanda N) dan lo mismo que la función SQL.
- **R6**: lectura sobre PS-0011 y los servicios que indique Victor, **solo lectura y solo si Victor indicó una base**: AC antes y después de la 102 con delta por componente; comparar Σ `pr_partidas.bac` con el BAC del Dashboard (suma de recursos) y reportar si difieren (P21). Sin base indicada: escribe «no probado en base» y sigue.

Punto de corte: R1–R3 / R4–R6.

## Rama, worktree y puerto

Rama `local-worker-3`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-3`. Debe tener la tanda O cerrada y el cierre de N de `local-worker-2` incorporado por el Worker git: verifica con `git log --oneline -8`, `ls db/` (deben existir `100*` y `101*`) y que `pr_subcontrato_medicion` aparece en `db/101*`. Si falta algo, detente y avisa. Trabaja **solo** en ese worktree. Puerto 3013 si levantas la app.

## Qué leer, y qué no

1. **El cuerpo vigente** de `recalcular_pr_desde_rdt` y `curva_s_proyecto` es el que dejó la `db/100*` de la tanda O en este worktree, **no** `db/053` ni `db/070`. Confírmalo con `grep -ln "function public.recalcular_pr_desde_rdt\|function public.curva_s_proyecto" db/*.sql`; copia el cuerpo completo y cambia solo lo de la tanda.
2. Como los nombres exactos de lo que crearon O y N aún no existen en este brief, **verifica con grep en tu worktree los nombres reales** (columnas de `pr_subcontrato_medicion`, `ac_diario_hh`, `ac_diario_hm`, `horas-extra.ts`) antes de usarlos.
3. `db/007_pr.sql`, `src/lib/pr/evm.ts`, `src/lib/pr/acumulacion-rdt.ts`, `src/lib/pr/subcontratos*`, `src/lib/dashboard/cargar-dashboard.ts` (solo leer, para R5c).
4. Flujos en `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/04-flujos-de-negocio/`: `10-generacion-pr.md` y `11-*` (Dashboard).

**No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Crear o editar: `db/102*`, una línea en `db/README.md`, `src/lib/pr/evm.ts` y su prueba, `ac-equivalencia.test.ts`, el script SQL de comparación y sus pruebas.

**No toca:** `db/100*` y `db/101*` (ya cerradas), `db/095*` (sin seguimiento: no lo agregues a ningún commit), `db/098*`, `db/099*`, `permisos.ts`, `pr/page.tsx`, `dashboard/page.tsx`, `costo-recursos.ts` y `cargar-dashboard.ts` (de la tanda S), `src/lib/pdf/hoja.ts`, `registro-accesos.ts`, `next.config.ts`, `package.json`, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica la migración**: solo escribe el archivo (la aplica el Orquestador). Otro plan («Revisión completa de la app») tiene congelados los archivos del RDT: no los edites.

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-3` (nunca a `main`) al cerrar R1–R3 y al cerrar R4–R6. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/R.md`, con la plantilla `docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` de ese repositorio (cinco grupos de hallazgos; el delta por componente de R5b y R6 va en el resumen). No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- Migración **102** (100 de O, 101 de N). Re-verifica con `ls db/`.
- Granularidad solo a nivel servicio: `pr_recursos` no tiene partida. EV, PV y BAC no cambian; lo que cambia es el AC.
- Base de prueba: ninguna salvo que Victor la dé; sin base la migración queda «revisada, no probada en base».

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). No toca permisos por rol. Comandos: `npm test`; `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar errores nuevos, anota el conteo); build con `npx next build --webpack`.

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**; no lo decidas tú.

## Criterios de salida

R1–R6 en `Conforme` u `Observado` con causa; pruebas R5 (a)-(e) en verde; `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
