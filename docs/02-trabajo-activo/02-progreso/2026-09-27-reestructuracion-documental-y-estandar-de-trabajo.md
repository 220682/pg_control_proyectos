# Progreso — Reestructuración documental y estándar de trabajo

> Referencia: [plan](../01-planes/2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md).

## Estado general y fase actual

En ejecución. Worker asignado tras el Gate 1 (2026-09-27). Fase actual: **Fase 4** (Fases 2 y 3 cerradas).

## Roles y estado

| Rol | Quién | Estado |
|---|---|---|
| Worker | Sesión asignada tras el Gate 1 (2026-09-27) | En ejecución |

## Avances terminados

- Fase 2: `git mv` del plan a `02-trabajo-activo/01-planes/`; referencia corregida en `docs/README.md` (§10.1, cambio mecánico de ruta).
- Fase 2: creados este progreso y su evidencia homónima.
- Fase 2: revisados los READMEs de la Fase 1 contra §2/§3 del plan. No hay menciones de `work-N` en los archivos creados en la Fase 1 (verificado con `grep -rn "work-N\|work-1\|work-2"` sobre las siete áreas numeradas: sin resultados). Corregida la etiqueta incorrecta en `docs/03-aprendizaje-continuo/README.md` (`git/ramas` → `entorno/infra` para "acceso Postgres sin IPv6" y "red bloqueada"); el índice completo se rehace en la Fase 5 según la clasificación final de §4.5.

- Fase 3: `git mv` del diagrama a `00-estandar-agentes/04-flujo-sdd-y-planes.md`, completado con los 18 pasos, tabla por rol y Mermaid aplicando D2 (`<entorno>-worker-N`), D6 (consulta directa del Worker) y D10 (lectura por rol). Creados `00-indice.md`, `01-principios-y-seguridad.md`, `02-roles-y-delegacion.md`, `03-sesiones-contexto-y-handoff.md` y `05-aprendizaje-continuo.md`, integrando el contenido universal de `docs/00-sistema/` (los tres originales de esa carpeta no se tocan todavía: se eliminan en la Fase 7 según §10.3-A, una vez confirmado que su contenido quedó cubierto). Creadas las 9 plantillas de `06-plantillas/`. Verificado con `grep -rniE "victor|pg_control_proyectos|py_control_proyectos_web" docs/00-estandar-agentes/`: dos apariciones encontradas y corregidas (README de la carpeta y de plantillas, creados en la Fase 1, mencionaban "Victor" y el nombre del repo) — ahora sin resultados.

## Trabajo actual

Fase 4: crear los 7 documentos de `01-contexto-repositorio/`.

## Pendientes

Fases 4 a 9 completas (ver Punch List del plan, §9).

## Commits, ramas y worktrees usados

Rama `main` de `pg_control_proyectos`, directo, sin worktree (§2.6 y §7 del plan). Commits registrados abajo a medida que se pushean.

## Hallazgos registrados en el momento

_(se agregan aquí, con fecha, a medida que ocurren — ver también §12–§14 del plan)_

## Bloqueos, riesgos y decisiones requeridas

Ninguno por ahora.

## Próximo paso verificable

Fase 4: crear `01-contexto-repositorio/00-indice.md` y los 6 documentos restantes de esa carpeta.

## Revisión de fuentes de verdad por fase

- **Fase 2:** revisado. El único cambio de fuente de verdad central fue la corrección de ruta en `docs/README.md` (mecánico, autorizado por §10.1). La corrección de etiqueta en `03-aprendizaje-continuo/README.md` no es fuente de verdad central. Fuentes de verdad revisadas: sin cambios normativos requeridos más allá de lo ya aplicado.
- **Fase 3:** el estándar de agentes (`00-estandar-agentes/`) nace como fuente normativa reusable, autorizado explícitamente por la excepción de §10.1 del plan (el objeto de este plan es construir esa estructura). No se tocó `AGENTS.md`, `README.md` ni `docs/README.md` en esta fase. Contenido integrado desde `docs/00-sistema/roles-y-flujo.md`, `gestion-de-sesiones-y-contexto.md` y `convenciones-de-trabajo.md` (universal → estándar; lo específico de este repo queda pendiente para `01-contexto-repositorio/` en la Fase 4) y desde dos mejoras continuas promovidas (`2026-09-23-verificar-antes-de-afirmar.md` → `01-principios-y-seguridad.md`; `2026-09-23-sendmessage-no-alcanza-sesiones-create-session.md` → `03-sesiones-contexto-y-handoff.md`) — los archivos originales de `Mejoras continuas/` no se tocan todavía, se mueven y clasifican formalmente en la Fase 5 según §4.5. **Propuesta normativa para el Auditor:** D10 (lectura por rol) reemplaza la instrucción vigente de `AGENTS.md`/`docs/README.md` de "leer todos los Flujos de trabajo para contexto general" — el cambio de contenido en `AGENTS.md` lo aplica el Orquestador tras el Gate 2, según §2.3 del plan; queda anotado también en §14 de este plan.

## Handoffs

_(secciones fechadas, si la tarea cambia de sesión)_
