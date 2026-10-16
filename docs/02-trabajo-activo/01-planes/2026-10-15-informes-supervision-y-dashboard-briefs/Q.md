# Brief — Tanda Q: pestaña «Inasistencias»

## Rol, modelo y tanda

Worker 3, Sonnet, esfuerzo medio. Tanda Q, Ola 3, carril W3 (después de F). Subagente «Worker 3 · Q». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **Q1**: `src/lib/informes/inasistencias.ts` (puro): filtro diario o semanal con el control de período de `periodo.ts` (B4), agrupación y orden — prueba: unitaria con bordes.
- **Q2**: `GET /api/inasistencias` (ver «Contrato técnico verificado») — prueba: de ruta (401, 403 de servicio ajeno, 400 de período fuera de límite, el administrador ve todos, los 13 roles entran).
- **Q3**: `GET /api/inasistencias/pdf` con `pdfkit` y `hoja.ts`, filtro aplicado en el encabezado y hoja con «Sin inasistencias» si no hay — prueba: PDF leído con `pdf-parse`.
- **Q4**: pestaña «Inasistencias» en la pantalla de Informes (la crea E2): Diario/Semanal, Desde/Hasta, «Todos mis servicios» o un servicio, tabla con scroll horizontal, estados vacío, carga y error, botón PDF — prueba: capturas escritorio y 390 px.
- **Q5**: prueba de que ningún bloque ni formato de informe incluye inasistencias, y de que la pestaña no cambia el listado de informes.
- **Q6**: verificación con las dos cuentas: los 13 roles ven la pestaña, y solo dentro de sus servicios — prueba: tabla observada (Skill `verificar-permisos-por-rol`).

Punto de corte: Q1–Q3 / Q4–Q6.

## Rama, worktree y puerto

Rama `local-worker-3`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-3`, **Esta tanda se entrega en dos mitades (decisión del Orquestador, 2026-10-16, para no dejar a W3 ocioso mientras W1 hace C y D; no cambia el contenido de ningún ítem):** la **primera mitad (Q1–Q3)** se hace ahora, antes de E, porque solo usa `periodo.ts` (tanda B), `puedeVerInasistencias` (tanda A) y archivos nuevos de W3; para ella verifica con `git log --oneline -5` que `local-worker-3` contiene el merge de `local-worker-1` hasta ee80c7a (tanda B) y que existe `src/lib/informes/periodo.ts` (si no, detente y avisa), y **no leas** la pantalla de E ni la maqueta. Su resumen va a `resultados/Q1-Q3.md`. La **segunda mitad (Q4–Q6)** se hace después de F, cuando existe la pantalla de Informes de E (verifica entonces que E y F están; si no, detente y avisa) y cierra `resultados/Q.md`. **W3 parte de `local-worker-3` con `local-worker-1` incorporada; el Worker git lo hace antes.** Puerto 3013 si levantas la app. Trabaja solo ahí.

## Qué leer, y qué no

1. `src/lib/informes/periodo.ts` (`validarPeriodo`, `rangoDeAtajo`, `MAX_MESES`, `sumarMeses`, `diasDelPeriodo`) y `tipos.ts` (**contrato congelado de B**; no lo cambies).
2. `src/lib/rdts/borrador.ts` (tipo `Inasistencia`, `InasistenciaFila`, `MOTIVOS_INASISTENCIA`: Falta, Descanso médico, Permiso, Vacaciones, Otro), `db/096_rdt_borradores_e_inasistencias.sql` (columna `rdt_partes.inasistencias jsonb`); verifica con `grep` los campos reales de cada fila (persona, DNI, motivo, nota) y el estado `RECHAZADO` en `src/lib/rdts/`. **Solo lectura:** `src/lib/rdts/**` y `api/rdts/**` están congelados por otro plan.
3. `src/lib/permisos/permisos.ts`: `puedeVerInasistencias` (los 13 roles; creada en la tanda A). Alcance: busca el helper existente `tieneAlcanceSobreProyecto` y cómo otras rutas listan los servicios del usuario (el administrador ve todos).
4. `src/lib/pdf/hoja.ts` (`crearPdf`, `celda`, `texto`, `cabeceraFormato`; **no se edita**) y `src/lib/rdts/exportador-pdf.ts` como patrón; `pdf-parse` ya está en `package.json`.
5. La pantalla de Informes que dejó E (`src/app/(workspace)/proyectos/[id]/informes/**`, `src/components/informes/**`). **Contrato por confirmar al incorporar D:** si el listado de informes de E usa pestañas, reutiliza ese patrón.
6. Diseño: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/05-diseno-y-referencias/design.md` y la maqueta `.../mockups/informes-supervision.html` (solo la vista `v-inasistencias`; no la copies).

**No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Crear: `src/lib/informes/inasistencias.ts`, `src/app/api/inasistencias/route.ts`, `src/app/api/inasistencias/pdf/route.ts`, el componente de la pestaña bajo `src/components/informes/`, y sus pruebas. Editar la pantalla de Informes de E solo para añadir la pestaña.

**No toca:** `src/lib/informes/tipos.ts`, `db/**` (sin migración nueva: lee `rdt_partes.inasistencias`), `db/095*` (sin seguimiento: no lo agregues a ningún commit), `src/lib/rdts/**`, `api/rdts/**`, `permisos.ts`, `registro-accesos.ts`, `next.config.ts`, `src/lib/pdf/hoja.ts`, `api/proyectos/[id]/informes/**` (W1), `package.json`, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica migraciones.**

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-3` (nunca a `main`) al cerrar Q1–Q3 y al cerrar Q4–Q6. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/Q.md`. **Lee y usa la plantilla** `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` (cinco grupos de hallazgos). No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- `GET /api/inasistencias?tipo=diario|semanal&desde=&hasta=&proyectoId=<id>|todos`: los 13 roles; solo servicios dentro del alcance (el administrador, todos); `proyectoId` fuera de alcance → 403; período con los límites del semanal (desde ≤ hasta, hasta ≤ hoy en fecha Lima, máximo 3 meses) → 400 si no. Lee `rdt_partes.inasistencias` de partes **no `RECHAZADO`**. Devuelve persona, DNI, motivo, nota, fecha, servicio y RDT de origen. Valida en servidor: sesión, rol y alcance; nunca confía en lo que manda el navegador.
- `GET /api/inasistencias/pdf?...`: mismo filtro y validaciones; PDF A4 con `pdfkit`; con cero filas, hoja con «Sin inasistencias».
- Las inasistencias son informativas: no suman HH ni cambian el costo. Ningún bloque ni formato de informe las incluye (Q5).
- **Decidido por el Orquestador (detalle derivado):** «Diario» es **una sola fecha** (por defecto hoy en fecha Lima; `desde` = `hasta`); «Semanal» es un rango con los límites del semanal. El DNI **sí está en la fila guardada** (`rdt_partes.inasistencias`: `personalId`, `dni`, `nombre`, `motivo`, `nota`; el servicio y la fecha salen de la fila del parte, plan §«Verificado en la app»): no se cruza con otra tabla. Verifica los nombres con `grep`; si el código real difiere de esto, devuélvelo como pregunta.
- Migraciones 098 a 102 pueden no estar aplicadas (P33); la 096 también puede estar sin aplicar: pruebas con datos simulados, «no probado en base». Sin cuentas de prueba (P36): capturas y sesión quedan «Observado» y los cierra la tanda L.

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). Q2 y Q6 tocan accesos por rol: **aplica `verificar-permisos-por-rol`** (`.claude/skills/verificar-permisos-por-rol/SKILL.md`), con pruebas de ruta por los 13 roles (tabla esperado contra observado); lo observado en vivo lo cierra L. Comandos: `npm test` (si solo cambia por fin de línea el `.snap` de curva-s, restaurarlo con `git checkout`); `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar nuevos, anota el conteo); `npx next build --webpack`. `.env.local`: copiar el principal al worktree (autorizado siempre).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**.

## Criterios de salida

Q1–Q6 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen con la tabla de permisos. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
