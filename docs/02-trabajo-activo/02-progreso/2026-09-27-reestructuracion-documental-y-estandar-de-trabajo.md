# Progreso — Reestructuración documental y estándar de trabajo

> Referencia: [plan](../01-planes/2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md).

## Estado general y fase actual

En ejecución. Worker asignado tras el Gate 1 (2026-09-27). Fase actual: **Fase 7** (Fases 2 a 6 cerradas).

## Roles y estado

| Rol | Quién | Estado |
|---|---|---|
| Worker | Sesión asignada tras el Gate 1 (2026-09-27) | En ejecución |

## Avances terminados

- Fase 2: `git mv` del plan a `02-trabajo-activo/01-planes/`; referencia corregida en `docs/README.md` (§10.1, cambio mecánico de ruta).
- Fase 2: creados este progreso y su evidencia homónima.
- Fase 2: revisados los READMEs de la Fase 1 contra §2/§3 del plan. No hay menciones de `work-N` en los archivos creados en la Fase 1 (verificado con `grep -rn "work-N\|work-1\|work-2"` sobre las siete áreas numeradas: sin resultados). Corregida la etiqueta incorrecta en `docs/03-aprendizaje-continuo/README.md` (`git/ramas` → `entorno/infra` para "acceso Postgres sin IPv6" y "red bloqueada"); el índice completo se rehace en la Fase 5 según la clasificación final de §4.5.

- Fase 3: `git mv` del diagrama a `00-estandar-agentes/04-flujo-sdd-y-planes.md`, completado con los 18 pasos, tabla por rol y Mermaid aplicando D2 (`<entorno>-worker-N`), D6 (consulta directa del Worker) y D10 (lectura por rol). Creados `00-indice.md`, `01-principios-y-seguridad.md`, `02-roles-y-delegacion.md`, `03-sesiones-contexto-y-handoff.md` y `05-aprendizaje-continuo.md`, integrando el contenido universal de `docs/00-sistema/` (los tres originales de esa carpeta no se tocan todavía: se eliminan en la Fase 7 según §10.3-A, una vez confirmado que su contenido quedó cubierto). Creadas las 9 plantillas de `06-plantillas/`. Verificado con `grep -rniE "victor|pg_control_proyectos|py_control_proyectos_web" docs/00-estandar-agentes/`: dos apariciones encontradas y corregidas (README de la carpeta y de plantillas, creados en la Fase 1, mencionaban "Victor" y el nombre del repo) — ahora sin resultados.

- Fase 4: creados los 7 documentos de `01-contexto-repositorio/` integrando `convenciones-de-trabajo.md` (regla de los dos repos, pool de ramas, commits ~35%, chats) y tres mejoras continuas promovidas (`verificacion-playwright-falsos-negativos.md`, `eslint-baseline-vs-cero.md`, `tests-contadores-congelados.md` → `04-pruebas-y-evidencia.md`; `turbopack-worktree-junction.md` → `03-entorno-git-y-worktrees.md`, corregido tras un primer error de ubicación). El pool real de ramas/worktrees de `py_control_proyectos_web` queda **"por verificar"**: no hay acceso a ese repositorio desde esta sesión, anotado explícitamente en `03-entorno-git-y-worktrees.md` en vez de copiar la tabla obsoleta `work-1`/`work-2`.

- Fase 5: `git mv` de `tareas-futuras.md` → `01-planes/planes-futuros.md`, adaptado al formato de §2.5 (estado y "requiere Spec/SDD" por ítem). `git mv` de las 11 mejoras a `03-aprendizaje-continuo/`. Clasificación aplicada según §4.5: 6 promovidas ya integradas (Fases 3 y 4), creados `historico.md` (9 entradas) y `pendientes-de-promocion.md` (1 entrada: red bloqueada). Índice de `03-aprendizaje-continuo/README.md` rehecho, una fila por archivo con etiqueta y estado final. Enlaces corregidos en el mismo commit: `AGENTS.md` (verificar-antes-de-afirmar), dos enlaces internos en `preguntas-frecuentes-flujo-orquestador.md`, uno en `acceso-postgres-sin-ipv6.md`, y los dos enlaces de "Fase 1/Fase 2" en `planes-futuros.md` (apuntan a `Tareas de implementacion/` hasta que la Fase 7 los migre; nota dejada en el propio archivo).

- Fase 6: `git mv` de los 21 flujos a `04-flujos-de-negocio/` (renombrado el 19 sin espacios); `git mv` de `design.md` y los 6 mockups a `05-diseno-y-referencias/`; `git mv` de las 5 carpetas de apoyo a `06-material-de-apoyo/`. Integrado el contenido útil de `docs/Flujos de trabajo/README.md` (índice de los 21 flujos, regla "Borrado administrador") y de `docs/visual-companion/README.md` (nomenclatura oficial, índice de mockups, campos del formulario RQ) en los README nuevos; ambos originales eliminados con `git rm` (§10.3-A, contenido ya integrado). Corregidos en el mismo commit: la regla de lectura de `04-flujos-de-negocio/README.md` (ahora refleja D10, antes decía "nunca los 21 completos" sin la excepción por rol — contradecía el Gate 1); dos menciones a `tareas-futuras.md`/`visual-companion` en `14-accesos-y-restricciones.md`, `10-generacion-pr.md`, `design.md` y `mockups/index.html`. `docs/06-material-de-apoyo/README.md` actualizado con las 5 carpetas ya presentes (ya no "comienza vacía").

## Trabajo actual

Fase 7: mover las 12 tareas históricas a `01-planes/`, eliminar la tarea de cronograma, descomponer `resumen-checklists.md`.

## Pendientes

Fases 7 a 9 completas (ver Punch List del plan, §9).

## Commits, ramas y worktrees usados

Rama `main` de `pg_control_proyectos`, directo, sin worktree (§2.6 y §7 del plan). Commits registrados abajo a medida que se pushean.

## Hallazgos registrados en el momento

_(se agregan aquí, con fecha, a medida que ocurren — ver también §12–§14 del plan)_

## Bloqueos, riesgos y decisiones requeridas

- **Hallazgo de entorno (no es conflicto de regla de negocio, verificado con herramientas — `git branch --show-current`, `git log` de `origin/main`):** esta sesión de Worker corre en un contenedor cuyo harness exige commitear en la rama designada `claude/reestructuracion-documental-pg-control-jvj5mf` y prohíbe explícitamente pushear a otra rama sin permiso. `origin/main` tiene historia propia, no relacionada, de otras sesiones concurrentes en la nube (ej. commits "cierre de sesion — ambos agentes en ejecucion en la nube"). El primer intento de `git push -u origin main` fue rechazado (`non-fast-forward`) porque intentaba subir la rama de esta sesión a un `main` remoto con historia divergente. Se corrigió pusheando a `origin/claude/reestructuracion-documental-pg-control-jvj5mf` (rama nueva creada en GitHub, sin PR abierto). **No se resuelve por cuenta propia:** el plan (§2.6, §7) exige trabajar "directo en main, sin rama"; esta ejecución quedó en la rama designada por el entorno. Se anota para el Auditor y el Orquestador — llevar esto a `main` real requiere una decisión fuera del alcance del Worker (abrir PR / merge, o que el Orquestador reconcilie ambas ramas). Ver también §14 del plan.

## Próximo paso verificable

Fase 7: `git mv` de las 12 tareas históricas restantes a `01-planes/` y `git rm` de la tarea de cronograma (§4.5).

## Revisión de fuentes de verdad por fase

- **Fase 2:** revisado. El único cambio de fuente de verdad central fue la corrección de ruta en `docs/README.md` (mecánico, autorizado por §10.1). La corrección de etiqueta en `03-aprendizaje-continuo/README.md` no es fuente de verdad central. Fuentes de verdad revisadas: sin cambios normativos requeridos más allá de lo ya aplicado.
- **Fase 3:** el estándar de agentes (`00-estandar-agentes/`) nace como fuente normativa reusable, autorizado explícitamente por la excepción de §10.1 del plan (el objeto de este plan es construir esa estructura). No se tocó `AGENTS.md`, `README.md` ni `docs/README.md` en esta fase. Contenido integrado desde `docs/00-sistema/roles-y-flujo.md`, `gestion-de-sesiones-y-contexto.md` y `convenciones-de-trabajo.md` (universal → estándar; lo específico de este repo queda pendiente para `01-contexto-repositorio/` en la Fase 4) y desde dos mejoras continuas promovidas (`2026-09-23-verificar-antes-de-afirmar.md` → `01-principios-y-seguridad.md`; `2026-09-23-sendmessage-no-alcanza-sesiones-create-session.md` → `03-sesiones-contexto-y-handoff.md`) — los archivos originales de `Mejoras continuas/` no se tocan todavía, se mueven y clasifican formalmente en la Fase 5 según §4.5. **Propuesta normativa para el Auditor:** D10 (lectura por rol) reemplaza la instrucción vigente de `AGENTS.md`/`docs/README.md` de "leer todos los Flujos de trabajo para contexto general" — el cambio de contenido en `AGENTS.md` lo aplica el Orquestador tras el Gate 2, según §2.3 del plan; queda anotado también en §14 de este plan.
- **Fase 4:** `01-contexto-repositorio/` nace con lo específico de este repositorio, autorizado por §10.1. Integra `convenciones-de-trabajo.md` (aún no se elimina el original: eso ocurre en la Fase 7 según §10.3-A) y cuatro mejoras continuas promovidas. No se tocó ninguna fuente de verdad central. Fuentes de verdad revisadas: sin cambios normativos requeridos más allá de lo ya anotado para el Auditor en la Fase 3.
- **Fase 5:** las reglas de negocio no se tocaron (ninguna de las 11 mejoras era una regla de negocio). Los flujos de negocio (`docs/Flujos de trabajo/`, todavía no migrados) no se modificaron. Fuentes de verdad revisadas: sin cambios normativos requeridos.
- **Fase 6:** los 21 flujos de negocio son ahora la fuente de verdad en su ubicación definitiva (`04-flujos-de-negocio/`); no se cambió ninguna regla funcional, solo ubicación, nombre de archivo (el 19) y los enlaces que la migración rompía. El único contenido normativo tocado fue la regla de lectura de `04-flujos-de-negocio/README.md`, alineada a D10 (ya aprobada en el Gate 1, no es una decisión nueva del Worker). `design.md` queda como fuente de verdad visual en su ubicación definitiva. Fuentes de verdad revisadas: sin cambios normativos nuevos más allá de aplicar D10 (ya aprobado).

## Handoffs

_(secciones fechadas, si la tarea cambia de sesión)_
