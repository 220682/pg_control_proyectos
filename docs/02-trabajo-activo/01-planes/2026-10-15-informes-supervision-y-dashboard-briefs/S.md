# Brief — Tanda S: AC con materiales y subcontratos en las pantallas

## Rol, modelo y tanda

Worker 2, Sonnet, esfuerzo medio. Tanda S, Ola 1-2, carril W2 (después de H, con el cierre de R incorporado). Subagente «Worker 2 · S». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **S1**: `src/lib/dashboard/cargar-dashboard.ts`, `dashboard/page.tsx` y `pr/page.tsx` leen `costo_materiales_acum` y `costo_subcontratos_acum` de `proyecto_pr` y los pasan a `evm.ts` (R4, ya hecho por W3). Prueba unitaria: el AC del Dashboard es igual al del PR.
- **S2**: `src/lib/dashboard/costo-recursos.ts` (bloque «Costo real de recursos»): `TipoRecursoCosto` suma `material` y `subcontrato`, con filas de `pr_recursos.costo_acumulado`; la fila «Sin resolver» sigue en 0 cuando todo cuadra (hoy el bloque supone Σ mano de obra + equipos = AC, lo que deja de ser cierto con R20; hallazgo P18). Prueba unitaria.
- **S3**: Reporte del proyecto (`pr/page.tsx`): el KPI AC muestra el desglose personal, equipos, materiales y subcontratos; la tabla por partida suma la fila «Materiales y subcontratos (sin partida)» para que cuadre con el AC total. Prueba: captura con las dos cuentas, escritorio y 390 px.
- **S4**: prueba (c) de R5 con el cargador real y un servicio de prueba: AC del PR = último punto de la Curva S = AC del Dashboard. La igualdad con el AC del formato Costos (C5) se comprueba en L7, no aquí. Prueba unitaria y captura.

Punto de corte: S1–S2 / S3–S4.

## Rama, worktree y puerto

Rama `local-worker-2`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-2`. El Worker git le incorpora el cierre de R de `local-worker-3` **antes** de lanzarte. Verifica con `git log --oneline -8`, `ls db/` (debe existir `102*`) y con grep que `costoMaterialesAcum` y `costoSubcontratosAcum` están en `src/lib/pr/evm.ts`. Los nombres reales de lo que dejó R los verificas tú con grep antes de usarlos. Si falta algo, detente y avisa. Trabaja **solo** en ese worktree. Puerto 3012 si levantas la app.

## Qué leer, y qué no

1. `src/lib/dashboard/{cargar-dashboard,costo-recursos,dashboard}.ts` y su prueba, `dashboard/page.tsx`, `src/app/(workspace)/proyectos/[id]/pr/page.tsx`, `src/lib/pr/evm.ts` (solo leer), `db/102*` (para ver las columnas y la función).
2. Flujos en `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/04-flujos-de-negocio/`: `10-generacion-pr.md` y `11-*` (Dashboard).

**No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Crear o editar: `src/lib/dashboard/cargar-dashboard.ts`, `src/lib/dashboard/costo-recursos.ts`, `proyectos/[id]/pr/page.tsx`, `dashboard/page.tsx`, `src/components/pr/**`, `src/components/dashboard/**` (solo lo que S3 y S2 exigen) y sus pruebas.

**No toca:** **ningún SQL** (`db/*`) ni `src/lib/pr/evm.ts` (R4 es de W3: si falta algo en `evm.ts`, devuélvelo como pregunta), `permisos.ts`, `src/lib/pdf/hoja.ts`, `src/lib/rdts/**`, `registro-accesos.ts`, `next.config.ts`, `package.json`, `db/095*` (sin seguimiento: no lo agregues a ningún commit), flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. En Parcial el Dashboard no muestra dinero: no lo reintroduzcas con el desglose del AC.

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-2` (nunca a `main`) al cerrar S1–S2 y al cerrar S3–S4. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/S.md`, con la plantilla `docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` de ese repositorio (cinco grupos de hallazgos, una captura por ítem de pantalla). No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- La cuenta nueva se lee de `proyecto_pr.costo_materiales_acum` y `costo_subcontratos_acum` y de `pr_recursos.costo_acumulado` por fila; **no se recalcula en TypeScript** (una sola cuenta, en SQL).
- `pr_partidas.costo_real_acum` no cambia, por eso la tabla por partida necesita la fila «Materiales y subcontratos (sin partida)».
- BAC: `evm.ts` usa Σ `pr_partidas.bac` y `calcularBac` de `dashboard.ts` suma recursos (P21). Si ves una diferencia, anótala; no la corrijas.
- Base de prueba: ninguna salvo que Victor la dé; las pruebas S1, S2 y S4 son unitarias con datos armados.

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). No toca permisos por rol. Comandos: `npm test`; `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar errores nuevos, anota el conteo); build con `npx next build --webpack` (con Turbopack falla en worktrees por el symlink de `node_modules`).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**; no lo decidas tú.

## Criterios de salida

S1–S4 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.


## Avisos de la tanda N (Orquestador)

- `cargarDatosDashboard` tiene un tercer parámetro opcional `clienteMediciones`: la tabla `pr_subcontrato_medicion` no tiene política de lectura. En `dashboard/page.tsx` pásale `crearClienteAdmin()` **solo** si el rol tiene economía (verifica el nombre real con grep); sin él los subcontratos salen como avance físico.
- El pie de `pr/page.tsx` (~línea 422) dice que los subcontratos «no suman al AC»: corrígelo en S3 para que diga que materiales y subcontratos suman al costo real.
