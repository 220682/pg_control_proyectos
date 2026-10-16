# Brief — Tanda O: RDT, HH extra, HM stand-by y estado del equipo (datos y cálculo)

## Rol, modelo y tanda

Worker 3, Sonnet, esfuerzo medio. Tanda O, Ola 1, carril W3. Subagente «Worker 3 · O». Plan: `docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard.md` (no lo leas completo).

## Ítems de la tanda (Punch List)

- **O1**: `db/100_rdt_extra_standby_estado.sql` y una línea en `db/README.md`. `rdt_tareo.horas_extra numeric not null default 0 check (horas_extra >= 0)`; `rdt_equipos_parte.horas_standby numeric not null default 0 check (>= 0)` y `estado_equipo text` con check de `OPERATIVO`, `STAND_BY`, `AVERIADO`, `EN_MANTENIMIENTO`. Lo existente queda en 0 / vacío; no se reescribe ningún RDT. Aditiva, reversa en comentario.
- **O2**: `create or replace guardar_rdt_parte` (misma firma) partiendo del **cuerpo vigente en `main`** (última definición: `db/054_catalogo_cnc.sql`, no el archivo antiguo): lee `horasExtra` por persona y `horasStandby` y `estado` por equipo; rechaza extra > total de la persona, negativos y estados fuera de la lista.
- **O3**: `create or replace recalcular_pr_desde_rdt` (cuerpo vigente: `db/053_pr_motor_rdt.sql`, no redefinida después): costo HH = `tarifa x horas x (1 + 0,25 x extra_persona / total_persona)` (recargo repartido entre las actividades de la persona **en proporción a sus horas**); HM = `horas + horas_standby` en `hm_reales_acum`, costo, `pr_recursos.cantidad_acumulada` y `costo_acumulado` por cargo y equipo, balde legacy y aviso de tarifa. **HH reales e IP no cambian** (la extra ya está en el total); MOI sin valorizar. Solo HH y HM: materiales y subcontratos los agrega la tanda R (102) sobre esta función.
- **O4**: la serie diaria de la Curva S (`curva_s_proyecto`, cuerpo vigente: `db/070_curva_s_serie.sql`; `ac_diario_hh` y `ac_diario_hm`) con la misma cuenta. Prueba: el AC final de la Curva S = el AC del PR al mismo corte (sin materiales ni subcontratos todavía).
- **O5**: `src/lib/rdts/horas-extra.ts` (nuevo): `FACTOR_HH_EXTRA = 1.25`, normales = total − extra, HM total, `ESTADOS_EQUIPO`, validaciones. Prueba unitaria y una prueba que lee `db/100*` y comprueba que el factor del SQL es el mismo.
- **O6**: `src/lib/rdts/{tipos,plantilla,parte,borrador}.ts`: campos nuevos opcionales; un borrador viejo (sin las claves) se abre con 0 y vacío. `api/rdts/partes` (POST) y `api/rdts/partes/[id]` (PATCH) validan en servidor `horasExtra` (>= 0 y <= total de la persona), `horasStandby` (>= 0) y `estado` (uno de los 4 o vacío). Prueba de ruta: extra mayor que el total -> 400; estado inválido -> 400.
- **O7**: prueba de impacto: con RDT validados antiguos, AC, HH y HM del PR salen **idénticos** antes y después; con un parte nuevo solo sube el AC por el recargo y las HM por el stand-by; el historial de correcciones conserva las columnas nuevas.
- **O8**: comparación con datos reales del servicio de prueba PS-0011 (Portafolio Practica), **solo lectura** y **solo si Victor indicó una base**; si no hay base indicada, escribe «no probado en base» y sigue.

Punto de corte: O1–O4 / O5–O8.

## Rama, worktree y puerto

Rama `local-worker-3`, worktree `D:/VICTOR/CLAUDE CODE/py_control_proyectos_web/.worktrees/local-worker-3`. O **parte de `main` al día, no de la Tanda A**: empieza con `git merge main` y verifica con `git log --oneline -3` y `ls db/`. Trabaja **solo** en ese worktree. Puerto 3013 si levantas la app.

## Qué leer, y qué no

1. `db/053_pr_motor_rdt.sql`, `db/054_catalogo_cnc.sql` (confirma cuál es la definición vigente de `guardar_rdt_parte` con `grep -ln "function public.guardar_rdt_parte" db/*.sql`), `db/070_curva_s_serie.sql`, `db/096*` (forma de migración).
2. `src/lib/rdts/{parte,plantilla,tipos,borrador,consolidado,real-por-clave}.ts` y `src/app/api/rdts/partes/**`; pruebas existentes como `reposicionamiento-sql*.test.ts` (patrón de prueba de texto del SQL).
3. Flujos en `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/04-flujos-de-negocio/`: `06-rdt.md` y `10-generacion-pr.md`.

**No leas** el plan completo ni otros flujos.

## Qué puede trabajar

Crear o editar: `db/100*`, una línea en `db/README.md`, `src/lib/rdts/**`, `src/app/api/rdts/**`, `src/lib/pr/evm.ts` solo si hace falta para O3/O4 y su prueba, y las pruebas de todo lo anterior.

**No toca:** `FormularioCrearRdt.tsx` ni el PDF del RDT (tanda P), `db/102*` (tanda R), `permisos.ts`, `src/lib/pdf/hoja.ts`, `registro-accesos.ts`, `next.config.ts`, `package.json`, `db/095*` (sin seguimiento: no lo agregues a ningún commit), `db/098*`, `db/099*`, `db/101*`, flujos, `AGENTS.md`, el archivo del plan, ni otros worktrees. **No aplica la migración**: solo escribe el archivo (la aplica el Orquestador). Otro plan («Revisión completa de la app») tiene **congelados los archivos del RDT** mientras duren O, R y P: no edites fuera de la lista de arriba.

## Dónde deja su entrega y su evidencia

- Código: commit y push a `local-worker-3` (nunca a `main`) al cerrar O1–O4 y al cerrar O5–O8. `git add <ruta>` por nombre, nunca `git add -A`. Mensaje en español con `Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>`.
- Resumen de cierre: `D:/VICTOR/CLAUDE CODE/pg_control_proyectos/docs/02-trabajo-activo/01-planes/2026-10-15-informes-supervision-y-dashboard-briefs/resultados/O.md`, con la plantilla `docs/00-estandar-agentes/06-plantillas/12-resumen-de-cierre-de-tanda.md` de ese repositorio (cinco grupos de hallazgos). No hagas commit en el repositorio de documentación.

## Contrato técnico verificado

- Migración **100** (098 es de B, 099 de A, 101 de N; 102 la escribirá R después de ti). Re-verifica con `ls db/`.
- Las tres funciones se reescriben desde su **cuerpo vigente en `main`**, copiado completo y con solo los cambios de la tanda.
- Factor de HH extra 1,25 en una constante TS y en el SQL; stand-by suma a costo y a consumo de HM con la tarifa del equipo.
- Base de prueba: ninguna indicada salvo que Victor la dé: la migración queda «revisada, no probada en base».

## Skills y verificación

`cerrar-tanda` al terminar (`D:/VICTOR/CLAUDE CODE/pg_control_proyectos/.claude/skills/cerrar-tanda/SKILL.md`; el commit de documentación lo hace el Orquestador). Comandos: `npm test`; `npx tsc --noEmit`; `npm run lint` (9 errores y 22 avisos **preexistentes**: no agregar errores nuevos, anota el conteo); build con `npx next build --webpack` (con Turbopack falla en worktrees por el symlink de `node_modules`).

## Límites y preguntas

80 llamadas como meta; a las ~60 cierra el ítem en curso, commit, push y traspaso. Si hallas un conflicto con una regla de negocio o algo que el brief no decide, **detente y devuélvelo como pregunta al Orquestador**; no lo decidas tú.

## Criterios de salida

O1–O8 en `Conforme` u `Observado` con causa; pruebas, `tsc`, lint (sin errores nuevos) y build webpack en verde; commits comprobados con `git branch --contains`; árbol limpio salvo `db/095*`; resumen escrito. Respuesta final en <= 25 líneas: estado por ítem, commits, resultado de los comandos, preguntas abiertas.
