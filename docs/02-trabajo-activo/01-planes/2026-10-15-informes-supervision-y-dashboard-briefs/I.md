# Brief — Tanda I: Dashboard, gráficas

## Rol, modelo y tanda

Worker 2, Sonnet, esfuerzo medio. Tanda I, Ola 1, carril W2 (después de N, H y S). Subagente «Worker 2 · I». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **I1**: función pura `src/lib/dashboard/avance-por-nivel.ts` (partidas agrupadas por `servicio_encabezados`; programado con asignaciones del Plan Maestro al corte, real con RDT validados). Prueba unitaria.
- **I2**: gráfica de barras verticales con selector de nivel, clic para bajar un nivel y ruta para volver; «Pendiente» sin Plan Maestro aprobado.
- **I3**: función pura `recursos-contractual-acumulado.ts` desde `pr_recursos` (HH y HM; el exceso sobre lo contractual en rojo). Prueba: la suma es igual a la del PR. Confirma contra el DP la unidad de `cantidad_contractual` de los equipos (P5) y anótalo.
- **I4**: gráfica de recursos con pestañas HH, HM y Subcontratos. Subcontratos solo en Completo (deshabilitada con título en Parcial). **La pestaña usa el acumulado de la tanda N** (por avance físico o monto manual de cada subcontrato; `src/lib/pr/subcontratos*.ts`) y ya no queda «Pendiente». **HM incluye el stand-by** (cuenta contra lo contractual): lee `pr_recursos.cantidad_acumulada` que deja la tanda O/R; si el cierre de R no está incorporado en tu rama, la gráfica lee lo que dé el cargador y **lo dices en el resumen**.
- **I5**: leyenda que oculta o muestra series; globos accesibles con mouse, teclado y toque; todo valor también en etiqueta o matriz.
- **I6**: clic en cargo o equipo muestra en qué partidas se usó (`GET /api/proyectos/[id]/dashboard/recurso-partidas?tipo=&descripcion=`, solo horas, sin dinero).
- **I7**: capturas en escritorio y 390 px; estados vacío, carga y error.

Punto de corte: I1–I4 / I5–I7.

## Rama, worktree y puerto

Rama `local-worker-2`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-2`. **Parte con H (y S) cerradas**: verifica con `git log --oneline -5` que sus commits están; si no, avisa al Orquestador. Trabaja solo ahí. Puerto 3012 si levantas la app.

## Qué leer, y qué no

1. `src/lib/dashboard/cargar-dashboard.ts`: **recibe `clienteMediciones` como tercer parámetro (P27)**; `pr_subcontrato_medicion` no tiene política de lectura (db/095), así que la página debe pasarle el cliente admin **solo a los roles con economía** (`puedeVerEconomia`); sin él, todo sale como avance físico. Revisa cómo lo dejó S.
2. `src/lib/dashboard/**`, `src/components/dashboard/**`, `src/lib/niveles/agrupar-pantallas.ts`, `db/074`, `db/007`, `src/lib/pr/subcontratos.ts`, `src/lib/pr/evm.ts`.
3. En `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/`: flujo `04-flujos-de-negocio/11-dashboard.md`, `05-diseno-y-referencias/design.md` y la maqueta `05-diseno-y-referencias/mockups/dashboard-ip-hh-graficos.html`.

En Parcial no hay dinero en ningún byte (el modo lo decide el servidor, nunca un parámetro del navegador). **Verifica con `grep` los nombres reales** antes de usarlos. **No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Crear o editar: `src/lib/dashboard/**`, `src/components/dashboard/**`, `dashboard/page.tsx`, `api/proyectos/[id]/dashboard/recurso-partidas`, estilos del Dashboard y las pruebas.

**No toca:** `db/**` (ni `db/095*`, sin seguimiento: no lo agregues a ningún commit), `permisos.ts`, `src/lib/informes/**`, `src/lib/rdts/**`, `api/rdts/**`, `src/lib/pr/evm.ts` (solo se lee), `next.config.ts`, `package.json`, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica migraciones.**

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-2` (nunca a `main`) al cerrar I1–I4 y al cerrar I5–I7. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/I.md`. **Lee y usa la plantilla** `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` (cinco grupos de hallazgos) y una captura por ítem. No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- `pr_recursos` no tiene partida; HH y HM contractual y acumulada por cargo y equipo existen. Con las migraciones sin aplicar (P33), las capturas en vivo pueden quedar «Observado» para la tanda L.
- Sin dinero en Parcial: prueba que recorre la salida.

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). Comandos: `npm test`; `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar errores nuevos, anota el conteo); build con `npx next build --webpack` (con Turbopack falla en worktrees por el symlink de `node_modules`). `.env.local`: copiar el principal al worktree (autorizado siempre).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**; no lo decidas tú.

## Criterios de salida

I1–I7 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
