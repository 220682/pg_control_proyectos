# Brief — Tanda C: Informes, datos de los bloques del sistema

## Rol, modelo y tanda

Worker 1, Sonnet, esfuerzo medio. Tanda C, Ola 2, carril W1. Subagente «Worker 1 · C». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **C1**: `src/lib/informes/armar-datos-diario.ts`: encabezado, actividades del RDT (metrado del día, acumulado, %) e indicadores al corte (avance, programado, IP, HH) desde el cargador de A (`cargarDatosDashboard`, `src/lib/dashboard/cargar-dashboard.ts`); lo no validado sale «reportado, pendiente de validación». Prueba unitaria con RDT `VALIDADO` y `REGISTRADO`.
- **C2**: personal desglosado (nombre, cargo, partida, HH normales, HH extra, total) y equipos (equipo, partida, HM operativas, HM stand-by, estado). Lee `rdt_tareo.horas_extra`, `rdt_equipos_parte.horas_standby` y `estado_equipo` (tanda O, `db/100`); los RDT viejos salen con extra 0, stand-by 0 y estado «—». Prueba unitaria con un parte nuevo y uno viejo.
- **C3**: avance por nivel (mapa DP), Curva S física (`cargarCurvaS`, `src/lib/curva-s/cargar-curva-s.ts`), PPC y causas, avance de una partida, Plan Maestro próximos 7 días.
- **C4**: `armar-datos-semanal.ts`: por actividad contractual, acumulado anterior, metrado por día (o por semana si el período pasa de 10 días), total del período, acumulado a la fecha y %; personal y equipos igual; programado contra real; indicadores del período; diarios emitidos; días sin diario (solo con datos del RDT). Prueba: acumulado anterior + período = acumulado a la fecha, y cuadra con la suma de los diarios.
- **C5**: formato COSTOS: EV, AC, CV, CPI, SPI; personal y equipos valorizados (HH o HM x tarifa congelada); costo por partida con la fila «Materiales y subcontratos (sin partida)» para que cuadre; HH de MOI sin valorizar. **Materiales y subcontratos se leen de `proyecto_pr.costo_materiales_acum` y `costo_subcontratos_acum` (tanda R, `db/102`) y entran por `src/lib/pr/evm.ts`: no hagas cuenta propia** (R20/R22: solo a nivel servicio). Las HH extra (recargo 1,25) y las HM stand-by ya vienen dentro del costo real. La función rechaza al rol sin economía. Prueba: AC del formato = AC del PR al mismo corte.
- **C6**: `congelar.ts`: foto fija (`FotoFija`) con los valores del momento y su rotulación. Prueba: cambiar el RDT después no cambia el resultado.
- **C7**: prueba transversal: recorrer la salida de **todos los formatos distintos de `COSTOS`** (TECNICO, EJECUTIVO, FOTOGRAFICO, PERSONALIZADO y el semanal) y fallar si aparece algún campo en dinero (tarifas, costos, AC, EV, PV, BAC en moneda; IP, SPI y CPI no son dinero).

Punto de corte: C1–C3 / C4–C7.

## Rama, worktree y puerto

Rama `local-worker-1`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-1`. **Parte de `local-worker-1` después de que el Worker git incorpore el cierre de la tanda R (`local-worker-3`)**: antes de empezar verifica con `git log --oneline -5` y `ls db/` que están `db/100*` y `db/102*` y que `src/lib/rdts/horas-extra.ts` existe; si no están, **detente y avisa al Orquestador**. Trabaja solo en ese worktree. Puerto 3011 si levantas la app.

## Qué leer, y qué no

1. `src/lib/informes/tipos.ts` (**contrato congelado de la tanda B**: `Bloque`, `TipoBloqueDatos`, `FotoFija`; no lo cambies), `periodo.ts`, `formatos.ts`.
2. `src/lib/pr/evm.ts`, `db/026`, `db/053`, `db/100`, `db/102`, `src/lib/curva-s/`, `src/lib/dashboard/cargar-dashboard.ts`, `src/lib/rdts/parte.ts` (campos `horasExtra`, `horasStandby`, `estado`; columnas SQL `horas_extra`, `horas_standby`, `estado_equipo`).
3. Flujos en `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/04-flujos-de-negocio/`: `06-rdt.md`, `10-generacion-pr.md`, `11-dashboard.md` (confirma el nombre real con `ls`).

**Verifica con `grep` los nombres reales** de columnas, funciones y campos antes de usarlos; no los infieras del brief. **No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Crear: `src/lib/informes/armar-datos-diario.ts`, `armar-datos-semanal.ts`, `armar-datos-costos.ts`, `congelar.ts` y sus pruebas. Si hace falta un cargador compartido nuevo, créalo bajo `src/lib/informes/`.

**No toca:** `src/lib/informes/tipos.ts`, `db/**` (ninguna migración nueva), `db/095*` (sin seguimiento: no lo agregues a ningún commit), `src/lib/rdts/**` y `api/rdts/**` (congelados por otro plan), `src/lib/pr/evm.ts` (solo se lee), `dashboard/page.tsx`, `next.config.ts`, `package.json`, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica migraciones.**

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-1` (nunca a `main`) al cerrar C1–C3 y al cerrar C4–C7. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/C.md`. **Lee y usa la plantilla** `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` (cinco grupos de hallazgos). No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- Las migraciones 098 a 102 están escritas y **puede que no estén aplicadas** (P33): no hay base para probar; las pruebas son unitarias con datos de ejemplo. Anota «no probado en base».
- Dinero solo en COSTOS (R5): el AC, EV y tarifas no salen en ningún otro formato. COSTOS lo ven y crean los 5 roles con economía.
- El AC total incluye materiales y subcontratos (R20); el costo por partida (`pr_partidas.costo_real_acum`) **no**: de ahí la fila sin partida.

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). Comandos: `npm test`; `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar errores nuevos, anota el conteo); build con `npx next build --webpack` (con Turbopack falla en worktrees por el symlink de `node_modules`). `.env.local`: copiar el principal al worktree (autorizado siempre).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**; no lo decidas tú.

## Criterios de salida

C1–C7 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
