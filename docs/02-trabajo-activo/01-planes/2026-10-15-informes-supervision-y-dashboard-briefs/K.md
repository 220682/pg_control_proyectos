# Brief — Tanda K: Dashboard, descarga PDF y Excel con Curva S

## Rol, modelo y tanda

Worker 2, Sonnet, esfuerzo medio. Tanda K, Ola 1, carril W2 (después de J). Subagente «Worker 2 · K». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **K1**: ruta `GET /api/proyectos/[id]/dashboard/descargar?formato=pdf|xlsx&corte=` (quien ve el Dashboard: `puedeVerDashboard` + alcance sobre el servicio). El corte sale del filtro; **el modo lo decide el servidor** (rol + `tipo_dashboard`), nunca un parámetro del navegador. Valida formato y corte; errores explícitos.
- **K2**: PDF A4 horizontal con `pdfkit`: lo que se ve en el Dashboard, **Curva S en hoja aparte** (Completo: económica y física; Parcial: solo física) y matriz. Las gráficas se dibujan como vectores en `src/lib/pdf/graficos.ts` (**archivo nuevo**). **Nadie edita `src/lib/pdf/hoja.ts`**: puedes importar sus helpers, no modificarlos (sus constantes son A4 vertical; para horizontal crea el documento y las medidas en `graficos.ts`).
- **K3**: Excel con `exceljs`: una hoja por bloque y las series de la Curva S.
- **K4**: botón «Descargar» (PDF/Excel) con estados de carga y error.
- **K5**: prueba: **en Parcial ni el PDF ni el Excel contienen dinero**. El PDF se lee con `pdf-parse` y el Excel con `exceljs` (ambos ya en `package.json`); la prueba busca montos, «USD», «S/», «$», BAC, PV, EV, AC, CPI y la hoja económica de la Curva S. Modelo: la prueba que recorre la salida de la tanda I (P40).
- **K6**: `export const maxDuration` explícito en la ruta y medición del tiempo de generación (PDF y Excel) con datos de prueba; anótalo en el resumen.
- **K7**: archivos abiertos y capturas.

Regla R2: la descarga incluye siempre el Dashboard y la Curva S, según el modo del rol. Punto de corte: K1–K3 / K4–K7.

## Rama, worktree y puerto

Rama `local-worker-2`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-2`. Contiene A, N, H e I (último commit `461a0f9`); verifica con `git log --oneline -5` (J debe estar cerrada; si no, avisa). El cierre de R **no** está incorporado: **no dependas de `proyecto_pr.costo_materiales_acum`** (la tanda S lo traerá). Trabaja solo ahí. Puerto 3012 si levantas la app.

## Qué leer, y qué no

1. `src/lib/pdf/hoja.ts` (solo lectura), `src/lib/pdf/parche-fuentes-pdfkit.ts` (fuentes de pdfkit en Vercel), `src/lib/dashboard/cargar-dashboard.ts` (tercer parámetro `clienteMediciones`, P27: solo para roles con economía), `src/lib/curva-s/cargar-curva-s.ts` y `src/app/api/curva-s/route.ts` como modelo de permisos y modo.
2. **Curva S (P37):** la Curva S del archivo usa `cargarCurvaS(supabase, proyectoId, modo, desde, hasta)`. El cierre de R hace que el servidor la llame con el **cliente de servicio**, tras validar sesión, rol y alcance. En esta rama la ruta aún pasa el cliente de sesión (verificado con grep: no hay cliente de servicio en `curva-s`). Busca con grep cómo se crea el cliente de servicio en el repo, valida en tu ruta sesión, rol y alcance **antes** de usarlo, y úsalo solo para la Curva S y en modo económico solo para roles con economía. Anota en el resumen cómo quedó, para que el Orquestador lo alinee con R.
3. En `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/`: `04-flujos-de-negocio/11-dashboard.md`, `04-flujos-de-negocio/21-curva-s.md` (criterio «SVG a mano») y `05-diseno-y-referencias/design.md`.

Decisión: PDF con `pdfkit`, sin navegador sin cabeza. **Verifica con `grep` los nombres reales.** **No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Crear o editar: `src/lib/pdf/graficos.ts` (nuevo), `src/lib/dashboard/**` (armado de datos de descarga), `api/proyectos/[id]/dashboard/descargar/route.ts` (nuevo), el botón en `src/components/dashboard/**` y las pruebas.

**No toca:** `src/lib/pdf/hoja.ts`, `db/**` (ni `db/095*`, sin seguimiento: no lo agregues a ningún commit), `permisos.ts`, `src/lib/informes/**`, `src/lib/rdts/**`, `api/rdts/**`, `src/lib/pr/evm.ts`, `next.config.ts`, `package.json`, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica migraciones.** La ruta nueva lleva fila en el flujo 14 y en la matriz: anótalo como hallazgo para el Documentador; no edites flujos.

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-2` (nunca a `main`) al cerrar K1–K3 y al cerrar K4–K7. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/K.md`. **Lee y usa la plantilla** `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` (cinco grupos de hallazgos). No hagas commit en el repositorio de documentación.
- **Capturas (P36):** ningún Worker puede leer las cuentas de prueba y las migraciones 098 a 101 no están aplicadas. Los ítems con captura (K7 y la apertura visual de los archivos) quedan **«Observado»** con esa causa, **sin intentar iniciar sesión**; genera los archivos con datos de prueba en la suite; se cierran en la tanda L.

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). Comandos: `npm test` (si cambia solo por fin de línea `src/app/api/curva-s/__snapshots__/curva-s-route.test.ts.snap`, restáuralo con `git checkout`); `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar errores nuevos, anota el conteo); build con `npx next build --webpack` (con Turbopack falla en worktrees). `.env.local`: copiar el principal al worktree (autorizado siempre).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**; no lo decidas tú.

## Criterios de salida

K1–K7 en `Conforme` u `Observado` con causa; pruebas (incluida K5), `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito con tiempos medidos. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
