# Brief — Tanda P: RDT, formulario, borrador, PDF y consolidado

## Rol, modelo y tanda

Worker 3, Sonnet, esfuerzo medio. Tanda P, Ola 1-2, carril W3 (después de R). Subagente «Worker 3 · P». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **P1**: `FormularioCrearRdt.tsx`: por persona, campo «HH extra» (las HH normales = total − extra se calculan y se muestran); por equipo, «HM stand-by» y desplegable «Estado» (Operativo, Stand-by, Averiado, En mantenimiento); validación visible (extra no mayor que el total de la persona, sin negativos); sin cambiar lo demás. Prueba: captura escritorio y 390 px.
- **P2**: el borrador guarda y restaura los campos nuevos y abre bien borradores viejos. Prueba unitaria y captura.
- **P3**: PDF del RDT (`exportador-parte-pdf.ts`, `partes/[id]/pdf`, `partes/pdf-borrador`): columnas HH normales/extra y HM operativas/stand-by/estado **dentro del mismo formato impreso PROM-GP-002** (R21), sin dinero. Prueba: PDF abierto y leído.
- **P4**: Consolidado (`consolidado.ts`, `api/rdts/consolidado`): HH normales y extra, HM operativas y stand-by, sin dinero; los totales de HH y HM incluyen todo. Prueba: `consolidado.test.ts`.
- **P5**: detalle, corrección de un RDT rechazado y listados conservan y muestran los campos nuevos. Prueba de ruta y captura.
- **P6**: ZIP, listado PDF y exportaciones existentes siguen funcionando. Prueba: `npm test` completo.
- **P7**: recorrido Playwright: crear un RDT con extra y stand-by, validarlo y ver el AC en el PR; permisos: lo hacen los mismos roles que crean RDT. Capturas. Si las migraciones 100 y 102 **no están aplicadas** (P33), P7 queda «Observado» con causa y pasa a la tanda L; no apliques nada.

Punto de corte: P1–P3 / P4–P7.

## Rama, worktree y puerto

Rama `local-worker-3`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-3`, tras cerrar R (verifica con `git log --oneline -5` y `ls db/`). Trabaja solo ahí. Puerto 3013 si levantas la app.

## Qué leer, y qué no

1. Lo que dejó O (`resultados/O.md`, solo «Hallazgos»): `src/lib/rdts/horas-extra.ts` (`FACTOR_HH_EXTRA`, `horasNormales`, `hmTotal`, `ESTADOS_EQUIPO`, `ETIQUETAS_ESTADO_EQUIPO`, `errorHorasExtra`, `errorHorasStandby`) y `src/lib/rdts/parte.ts`. **Nombres reales de los campos del formulario: `horasExtra` (persona), `horasStandby` y `estado` (equipo)**; en SQL `horas_extra`, `horas_standby`, `estado_equipo`. Verifica con `grep` antes de usarlos.
2. `FormularioCrearRdt.tsx`, `src/lib/rdts/{exportador-parte-pdf,consolidado,borrador,plantilla,tipos}.ts`, `api/rdts/partes/**`, `api/rdts/consolidado`, y `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/05-diseno-y-referencias/design.md`.
3. Flujo `06-rdt.md` en `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/04-flujos-de-negocio/`.

**Aviso P32:** `borrador.ts` y `tipos.ts` no se tocaron en O porque el borrador pasa por `aplicarDatosPlantilla`; confirma que restaura los campos nuevos antes de editarlos. El PATCH de `partes/[id]` solo valida o rechaza el parte (no recibe tareo): la validación vive en el POST, la RPC y el formulario. **No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Editar: `FormularioCrearRdt.tsx`, `src/lib/rdts/{exportador-parte-pdf,consolidado,borrador,plantilla,tipos,parte}.ts` solo en lo necesario, las rutas de PDF y consolidado, las pruebas de `src/lib/rdts/**` y los listados que muestran el parte.

**Coordinación:** el plan «Revisión completa de la app» tiene **congelados los archivos del RDT** salvo para esta tanda; no edites fuera de lo listado. **No toca:** `db/**` (ni `db/095*`, sin seguimiento: no lo agregues a ningún commit), `permisos.ts`, `src/lib/pdf/hoja.ts`, `next.config.ts`, `package.json`, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica migraciones.**

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-3` (nunca a `main`) al cerrar P1–P3 y al cerrar P4–P7. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/P.md`. **Lee y usa la plantilla** `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` (cinco grupos de hallazgos) y una captura por ítem cuando aplique. No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- Sin dinero en el formulario, el PDF ni el consolidado. HH reales e IP no cambian: la extra ya está en el total. Las HM del consolidado suman operativas + stand-by.
- RDT existentes: extra 0, stand-by 0, estado vacío («—»).
- Base de prueba: ninguna salvo que Victor la indique.

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). Comandos: `npm test`; `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar errores nuevos, anota el conteo); build con `npx next build --webpack` (con Turbopack falla en worktrees por el symlink de `node_modules`). `.env.local`: copiar el principal al worktree (autorizado siempre).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**; no lo decidas tú.

## Criterios de salida

P1–P7 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
