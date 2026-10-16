# Brief — Tanda J: Dashboard, detalles e interacciones

## Rol, modelo y tanda

Worker 2, Sonnet, esfuerzo medio. Tanda J, Ola 1, carril W2 (después de I). Subagente «Worker 2 · J». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **J1**: detalle bajo la fila para cada tarjeta (% avance, BAC, PV, EV, AC, SPI, CPI, IP, HH, PPC) que abre y cierra al volver a tocar.
- **J2**: botón de cada detalle que lleva a la gráfica o matriz correspondiente; filas de partida tocables.
- **J3**: «Partida en revisión» (R7): franja fija «Revisando partida …» (avance, IP y CPI solo en Completo), fila de la matriz resaltada «En revisión», demás barras atenuadas; «Quitar» y Escape. La partida marcada rige en toda la pantalla hasta quitarla.
- **J4**: clic en la dona (Mano de obra, Equipos) lleva la gráfica de recursos a su pestaña; clic en «Desempeño por partida» marca la matriz.
- **J5**: en Parcial las tarjetas de dinero no existen y **ningún detalle muestra dinero**: prueba que recorre la salida (HTML y datos serializados), como la de P40 (`src/components/dashboard/graficas-parcial.test.ts`, modelo a seguir).
- **J6**: teclado (Tab, Enter, Espacio, Escape) y toque, con foco visible y `aria-expanded`/`aria-controls` en las tarjetas.
- **J7**: capturas de cada detalle y de la franja.

Punto de corte: J1–J3 / J4–J7.

## Rama, worktree y puerto

Rama `local-worker-2`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-2`. Contiene A, N, H e I (último commit `461a0f9`): verifica con `git log --oneline -5`; si falta algo, avisa al Orquestador. El cierre de R **no** está incorporado. Trabaja solo ahí. Puerto 3012 si levantas la app.

## Qué leer, y qué no

1. `src/components/dashboard/**` (sobre todo `TarjetaKpi.tsx`, `TarjetasProductividad.tsx`, `ResumenEjecutivo.tsx`, `MatrizPartidasDashboard.tsx`, `DonaCosto.tsx`, `GraficoAvanceNivel.tsx`, `GraficoRecursos.tsx`, `grafica-comun.tsx`), `src/lib/dashboard/**` y `dashboard/page.tsx`.
2. En `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/`: `04-flujos-de-negocio/11-dashboard.md`, `05-diseno-y-referencias/design.md` y la maqueta `05-diseno-y-referencias/mockups/dashboard-ip-hh-graficos.html`.

Reglas fijas: la etiqueta del supervisor va bajo el encabezado, no en la línea del servicio (P35: `CabeceraPagina` no admite hijos; no la muevas ni toques el componente compartido). En Parcial no hay dinero en ningún byte y el modo lo decide el servidor, nunca un parámetro del navegador; la tarjeta de avance dice «Avance físico ejecutado (RDT validados)», sin «EV / BAC» en Parcial. El avance real es solo de RDT `VALIDADO`. **Verifica con `grep` los nombres reales** antes de usarlos. **No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Crear o editar: `src/components/dashboard/**`, `src/lib/dashboard/**` (estado compartido de pantalla), `dashboard/page.tsx`, estilos del Dashboard y las pruebas.

**No toca:** `db/**` (ni `db/095*`, sin seguimiento: no lo agregues a ningún commit), `permisos.ts`, `src/lib/informes/**`, `src/lib/rdts/**`, `src/lib/pdf/**`, `api/**`, `src/lib/pr/evm.ts`, `next.config.ts`, `package.json`, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica migraciones.**

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-2` (nunca a `main`) al cerrar J1–J3 y al cerrar J4–J7. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/J.md`. **Lee y usa la plantilla** `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` (cinco grupos de hallazgos). No hagas commit en el repositorio de documentación.
- **Capturas (P36):** ningún Worker puede leer las cuentas de prueba y las migraciones 098 a 101 no están aplicadas. Los ítems con captura (J7 y la parte visual de J1–J6) quedan **«Observado»** con esa causa, **sin intentar iniciar sesión**; se cierran en la tanda L.

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). Comandos: `npm test` (si cambia solo por fin de línea `src/app/api/curva-s/__snapshots__/curva-s-route.test.ts.snap`, restáuralo con `git checkout`); `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar errores nuevos, anota el conteo); build con `npx next build --webpack` (con Turbopack falla en worktrees). `.env.local`: copiar el principal al worktree (autorizado siempre).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**; no lo decidas tú.

## Criterios de salida

J1–J7 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
