# Brief — Tanda N: Subcontratos con dos formas de medir

## Rol, modelo y tanda

Worker 2, Sonnet, esfuerzo medio. Tanda N, Ola 1, carril W2 (antes de I). Subagente «Worker 2 · N». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **N1**: `db/101_pr_subcontrato_medicion.sql` y una línea en `db/README.md`. Tabla `pr_subcontrato_medicion`: `proyecto_id`, `descripcion`, `modo` (`FISICO`/`MANUAL`, por defecto `FISICO`), `monto_manual numeric check (>= 0)`, `actualizado_por`, `actualizado_en`; `unique (proyecto_id, descripcion)`; un check que exige monto si el modo es `MANUAL`. RLS activado sin política (como `db/095`/`096`). Aditiva, reversa en comentario. **Solo crea la tabla**: no toques `recalcular_pr_desde_rdt` ni `curva_s_proyecto` (las reescribe W3 en las tandas O y R).
- **N2**: `src/lib/pr/subcontratos.ts` (función pura): acumulado, % y restante por modo (`FISICO` = contractual x avance físico del servicio, EV/BAC al corte; `MANUAL` = el monto escrito, el sistema calcula el %); aviso si el monto pasa del contractual (se acepta); rechazo de negativos; sin tope en 100 %. Prueba: contractual 200 e ingreso 40 -> 20 %.
- **N3**: `GET`/`PUT /api/proyectos/[id]/pr/subcontratos` con `puedeMedirSubcontratos` y alcance. `PUT` por subcontrato: `modo` y, si es `MANUAL`, `monto` >= 0 (negativo o no numérico -> 400); el subcontrato debe existir en `pr_recursos` tipo `subcontrato` de ese servicio; guarda quién y cuándo; el acumulado y el % los calcula el servidor, nunca se aceptan del navegador. Al guardar llama a `recalcularPr` (`src/lib/pr/acumulacion-rdt.ts`). Prueba de ruta: 403 sin economía, 400 monto negativo, subcontrato ajeno al servicio.
- **N4**: sección «Subcontratos» en el Reporte del proyecto (`proyectos/[id]/pr/page.tsx`, componentes en `src/components/pr/**`): desplegable «Por avance físico / Ingreso manual», campo de monto, % con barra, restante. **La nota de la pantalla dice que el monto ingresado es el costo real del subcontrato** (R20). Los roles sin economía no ven la sección. Prueba: capturas con las dos cuentas y a 390 px.
- **N5**: `src/lib/dashboard/cargar-dashboard.ts` (existe, de la Tanda A) incluye los subcontratos con su acumulado, para la gráfica de recursos de la tanda I. Prueba unitaria.
- **N6**: `subcontratos.ts` exporta los casos de prueba (contractual 200 con ingreso 40 -> 20 %; contractual 200 con avance físico 30 % -> 60) para que la prueba de equivalencia de la tanda R compruebe la cuenta SQL. El AC del subcontrato **no** se calcula aquí: lo hace la tanda R en una sola función.
- **N7**: prueba transversal: escribir un monto manual **no cambia el EV, el PV ni el BAC** y dispara el recálculo del PR (el cambio exacto del AC lo comprueba la tanda R).

Punto de corte: N1–N3 / N4–N7.

## Regla que manda sobre la maqueta

R20 (Victor, 2026-10-15): el subcontrato con ingreso manual **suma al costo real (AC)**: su monto es su costo real; el de avance físico aporta contractual x avance. La maqueta `mockups/pr-subcontratos-medicion.html` (líneas ~85 y ~94) está **desactualizada**: dice «cuenta como avance (valor ganado), no como costo real». Úsala solo para el aspecto; **el texto lo manda este brief** (hallazgo P23, lo corrige el Documentador). No es pregunta. Ya decidido por Victor: el subcontrato manual entra a la Curva S y no hay tope en 100 %.

## Rama, worktree y puerto

Rama `local-worker-2`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-2`. El Worker git le incorpora `local-worker-1` (Tanda A) **antes** de lanzarte; verifica con `git log --oneline -5` que ves `c0dd874` y `e65dcae`, y que existen `puedeMedirSubcontratos` en `src/lib/permisos/permisos.ts`, `cargarDatosDashboard` en `src/lib/dashboard/cargar-dashboard.ts` y `src/lib/proyectos/supervisor-operativo.ts`. Si falta algo, detente y avisa. Trabaja **solo** en ese worktree. Puerto 3012 si levantas la app.

## Qué leer, y qué no

1. `src/app/(workspace)/proyectos/[id]/pr/page.tsx`, `src/lib/pr/evm.ts`, `src/lib/pr/acumulacion-rdt.ts` (`recalcularPr`).
2. `db/007_pr.sql`, `db/060_pr_linea_base_dp.sql`, `db/096*` (forma de migración).
3. `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/05-diseno-y-referencias/mockups/pr-subcontratos-medicion.html` (solo aspecto).
4. Flujos en `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/04-flujos-de-negocio/`: `10-generacion-pr.md` y `14-accesos-y-restricciones.md`.

**No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Crear o editar: `db/101*`, una línea en `db/README.md`, `src/lib/pr/subcontratos*`, `src/app/api/proyectos/[id]/pr/subcontratos/**`, `proyectos/[id]/pr/page.tsx`, `src/components/pr/**`, `src/lib/dashboard/cargar-dashboard.ts` (solo N5) y sus pruebas.

**No toca:** `permisos.ts` (usa `puedeMedirSubcontratos` tal cual), `src/lib/pr/evm.ts` ni las funciones SQL del AC (de W3), `src/lib/pdf/hoja.ts`, `src/lib/rdts/**`, `api/rdts/**`, `registro-accesos.ts`, `next.config.ts`, `package.json`, `db/095*` (sin seguimiento: no lo agregues a ningún commit), `db/098*`, `db/100*`, `db/102*`, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica la migración**: solo escribe el archivo (la aplica el Orquestador).

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-2` (nunca a `main`) al cerrar N1–N3 y al cerrar N4–N7. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/N.md`, con la plantilla `docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` de ese repositorio (cinco grupos de hallazgos, una captura por ítem de pantalla). No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- Migración **101** (098 es de B, 099 de A, 100 de O). Re-verifica con `ls db/`.
- `pr_recursos` no tiene ligadura a partidas; avance físico = EV/BAC; el cálculo es a nivel servicio.
- Base de prueba: ninguna indicada: la migración queda «revisada, no probada en base».

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). Comandos: `npm test`; `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar errores nuevos, anota el conteo); build con `npx next build --webpack` (con Turbopack falla en worktrees por el symlink de `node_modules`).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**; no lo decidas tú.

## Criterios de salida

N1–N7 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
