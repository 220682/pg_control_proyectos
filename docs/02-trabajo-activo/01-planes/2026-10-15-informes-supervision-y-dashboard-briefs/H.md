# Brief — Tanda H: Dashboard, responsable, % avance, IP y HH

## Rol, modelo y tanda

Worker 2, Sonnet, esfuerzo medio. Tanda H, Ola 1, carril W2 (después de N). Subagente «Worker 2 · H». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **H1**: etiqueta «Supervisor operativo a cargo» (color de Supervisión operativa) con `obtenerSupervisorACargo` (tanda A); sin asignar: «Sin supervisor a cargo». Un solo supervisor por servicio (R1).
- **H2**: tarjeta % avance físico más grande, con barra: ejecutado, marca en lo programado al corte, restante. Sin Plan Maestro no hay marca. En Completo y en Parcial.
- **H3**: tarjetas IP (valor, HH ganadas y reales) y HH contractuales (barra de consumo, acumuladas con %, restantes) junto a la dona en Completo; en Parcial, tarjeta propia en la misma fila. Sin cuadros dentro de SPI y CPI.
- **H4**: matriz con columnas HH contractuales, HH acumuladas e IP por partida (también en Parcial).
- **H5**: contorno punteado amarillo en tarjetas, paneles, detalle y matriz (R8). **No** hagas aquí la partida «en revisión» ni el detalle que abren las tarjetas (R7): son de la tanda J.
- **H6**: pruebas: IP y HH iguales a los del PR al mismo corte; en Parcial **no hay dinero en ninguna salida** (HTML, props de componentes y respuestas de las rutas `api/**/dashboard/**`); la fila de tarjetas no crece.

Punto de corte: H1–H3 / H4–H6.

## Rama, worktree y puerto

Rama `local-worker-2`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-2`. Parte de lo que dejó N: verifica con `git log --oneline -5` que ves los commits de la tanda N y de la A, y con grep que existen `obtenerSupervisorACargo` (en `src/lib/proyectos/supervisor-operativo.ts`) y `cargarDatosDashboard` (`src/lib/dashboard/cargar-dashboard.ts`). Si falta algo, detente y avisa. Trabaja **solo** en ese worktree. Puerto 3012 si levantas la app.

## Qué leer, y qué no

1. `src/app/(workspace)/proyectos/[id]/dashboard/page.tsx`, `src/components/dashboard/**`, `src/lib/dashboard/{dashboard,cargar-dashboard}.ts`, `src/lib/pr/evm.ts` (solo leer: IP y HH ya están ahí).
2. Maqueta `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/05-diseno-y-referencias/mockups/dashboard-ip-hh-graficos.html`: **mira solo las secciones que necesitas** (tarjetas, matriz, contorno); y `docs/05-diseno-y-referencias/design.md` (solo la parte de Dashboard y contorno punteado) del mismo repositorio.
3. Flujo `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/04-flujos-de-negocio/11-dashboard.md` (verifica el nombre con `ls`).

**No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Crear o editar: `dashboard/page.tsx`, `src/components/dashboard/**`, `src/lib/dashboard/**`, `api/**/dashboard/**`, estilos del Dashboard y sus pruebas.

**No toca:** `permisos.ts`, `src/lib/pr/evm.ts` ni SQL (de W3), `src/lib/pdf/hoja.ts`, `src/lib/rdts/**`, `registro-accesos.ts`, `next.config.ts`, `package.json`, `db/095*` (sin seguimiento: no lo agregues a ningún commit), cualquier `db/*`, `costo-recursos.ts` y `pr/page.tsx` (de la tanda S), flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. Parcial sin dinero: no muestres costo, AC, CPI ni montos; no hay lógica de permisos nueva.

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-2` (nunca a `main`) al cerrar H1–H3 y al cerrar H4–H6. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/H.md`, con la plantilla `docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` de ese repositorio (cinco grupos de hallazgos, una captura por ítem de pantalla: escritorio y 390 px, en Completo y en Parcial). No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- Sin migración en esta tanda. IP y HH salen de `evm.ts` y del PR; no los recalcules por otro camino.
- BAC: `evm.ts` usa Σ `pr_partidas.bac` y `dashboard.ts` (`calcularBac`) suma `costo_contractual` de recursos y pueden diferir (P21). No lo corrijas: anótalo si lo ves.
- El modo del Dashboard lo decide el servidor (rol + `tipo_dashboard`), nunca un parámetro del navegador.
- Avance real solo con RDT `VALIDADO`.

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). Esta tanda no cambia permisos por rol, así que no uses `verificar-permisos-por-rol`; la prueba H6 de Parcial sin dinero es la que recorre la salida. Comandos: `npm test`; `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar errores nuevos, anota el conteo); build con `npx next build --webpack` (con Turbopack falla en worktrees por el symlink de `node_modules`).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**; no lo decidas tú.

## Criterios de salida

H1–H6 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
