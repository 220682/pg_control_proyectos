# Evidencia — Reestructuración documental y estándar de trabajo

> Referencia: [plan](../01-planes/2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md) y [progreso](../02-progreso/2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md).

## Entorno y fecha

`pg_control_proyectos`. Sin worktree. Inicio: 2026-09-27. **Nota:** el plan (§2.6, §7) asumía commit/push directo a `main`; el harness de esta sesión exigió trabajar en una rama designada (`claude/reestructuracion-documental-pg-control-jvj5mf`) — ver el hallazgo verificado en el progreso y en `01-contexto-repositorio/03-entorno-git-y-worktrees.md`.

## Rol/usuario y datos autorizados

Worker asignado por el Orquestador tras el Gate 1. Sin datos ni secretos reales involucrados: el cambio es puramente documental (reorganización de archivos Markdown).

## Punch List ejecutada

Tabla completa en el plan, §9. Se actualiza ítem por ítem con resultado, método y evidencia a medida que se cierra cada uno.

| ID | Esperado | Método | Observado | Estado | Evidencia | Responsable |
|---|---|---|---|---|---|---|
| PL-01 | Plan movido a `01-planes/`; progreso y evidencia homónimos creados | `git status`, `ls` | `git mv` del plan aplicado; este archivo y su homónimo de progreso creados | Conforme | Commit `5fe891b` | Worker |
| PL-02 | READMEs de la Fase 1 sin contradicciones con el plan | `grep -rn "work-N"`, revisión manual | Sin menciones de `work-N`; corregida etiqueta `git/ramas` → `entorno/infra` en `03-aprendizaje-continuo/README.md` | Conforme | Commit `5fe891b` | Worker |
| PL-03 | Diagrama movido con los 18 pasos y nomenclatura única | `git mv`, `grep -n "work-N"` | Movido a `00-estandar-agentes/04-flujo-sdd-y-planes.md`; secuencia de 18 pasos, tabla y Mermaid con `<entorno>-worker-N`; sin `work-N` | Conforme | Commit `5fe891b` | Worker |
| PL-04 | `00-indice.md` con tabla de lectura mínima | Lectura del archivo | Tabla por rol y por tipo de solicitud presente | Conforme | Commit `5fe891b` | Worker |
| PL-05 | 4 MD restantes del estándar, agnósticos | `grep -rniE "victor\|pg_control_proyectos\|py_control_proyectos_web" docs/00-estandar-agentes/` | Dos apariciones encontradas (README de la carpeta y de plantillas, de la Fase 1) y corregidas; segunda pasada sin resultados | Conforme | Commit `5fe891b` | Worker |
| PL-06 | 9 plantillas; `02-plan` con 3 secciones; `06` con verificación de rama y `PROPONER SKILL` | `grep` sobre cada plantilla | Las 9 plantillas creadas; `02-plan.md` con `## Mejoras (de trabajo)`, `## Reglas de negocio acordadas en esta tarea`, `## Carpetas/archivos huérfanos`; `06-informe-auditoria.md` con `## Verificación de rama` y `PROPONER SKILL` | Conforme | Commit `5fe891b` | Worker |
| PL-07 | 7 documentos de contexto; regla de los dos repos; pool real o "por verificar" | Lectura de los 7 archivos | Los 7 creados; pool de `py_control_proyectos_web` marcado explícitamente "por verificar" (sin acceso a ese repo desde esta sesión) | Conforme | Commit `b412276` | Worker |
| PL-08 | `planes-futuros.md` por `git mv` en formato §2.5 | `git log --follow`, lectura | Movido y adaptado (estado + "requiere Spec/SDD" por ítem) | Conforme | Commit `b412276` | Worker |
| PL-09 | 11 mejoras movidas; 6 promovidas integradas; `historico.md`/`pendientes-de-promocion.md` | `ls`, lectura de `historico.md` | 11 archivos movidos; 6 integradas (Fases 3–4); `historico.md` (9 entradas) y `pendientes-de-promocion.md` (1 entrada) creados | Conforme | Commit `b412276` | Worker |
| PL-10 | Índice etiquetado de aprendizaje corregido | Lectura de `03-aprendizaje-continuo/README.md` | Tabla reconstruida, una fila por archivo con etiqueta y estado final | Conforme | Commit `b412276` | Worker |
| PL-11 | 21 flujos movidos, el 19 renombrado, enlaces en el mismo commit | `git show --stat` | 21 renombres + enlaces corregidos (10, 14, 17, 20, 21) en el commit `d8c1833` | Conforme | Commit `d8c1833` | Worker |
| PL-12 | `design.md` y 6 mockups movidos; README integrado | `git show --stat`, `ls` | Movidos; contenido de `visual-companion/README.md` integrado en los 2 README nuevos; original eliminado | Conforme | Commit `d8c1833` | Worker |
| PL-13 | 5 carpetas de apoyo movidas; README actualizado | `ls` raíz y `06-material-de-apoyo/` | Raíz sin las 5 carpetas; las 5 presentes en destino; README actualizado (ya no dice "comienza vacía") | Conforme | Commit `d8c1833` | Worker |
| PL-14 | 12 tareas movidas tal cual; tarea de cronograma eliminada, referencia reemplazada | `git show --stat` | 12 renombres sin cambio de contenido + 1 `git rm`; referencia en `orquestador-salta-flujo...md` sin enlace | Conforme | Commit `73455c0` | Worker |
| PL-15 | `resumen-checklists.md` descompuesto; entradas sin dueño listadas | Lectura de los 9 planes + §14 del plan | 9 filas anexadas a sus 9 planes; metodología/totales sin dueño único en §14 | Conforme | Commit `73455c0` | Worker |
| PL-16 | Índice de `01-planes/` con artifacts huérfanos enlazados | Lectura de `01-planes/README.md` | Sub-lote 2 y Dashboard/Curva S enlazados; Matriz de Accesos reportada en §14 (sin dueño único) | Conforme | Commit `73455c0` | Worker |
| PL-17 | Originales integrados tratados según §10.3 | `git log --diff-filter=D` | 9 archivos eliminados, todos autorizados (§10.3-A o excepción de Gate 1) | Conforme | `git log --diff-filter=D --name-only ab4bd63..HEAD` | Worker |
| PL-18 | `docs/README.md` reescrito según §3.1 | Lectura del archivo | Mapa de 7 áreas, lectura mínima, diferencia plan/progreso/evidencia/aprendizaje; sin "Migración en curso" | Conforme | Commit `73455c0` | Worker |
| PL-19 | Rutas inexistentes quitadas de `AGENTS.md`/`README.md` | `grep` antes/después | Rutas actualizadas o quitadas; sin cambio de contenido normativo | Conforme | Commit `73455c0` | Worker |
| PL-20 | Artifacts alineados o pendiente registrado | `Artifact` read/publish | Ambos republicados; limitación de estructura de nodos anotada (Flujo SDD) | Conforme (con limitación anotada) | Versión 5 y versión 3 de los artifacts, respectivamente | Worker |
| PL-21 | Comando de §4.7 sin rutas antiguas en documentos vigentes | Comando exacto de §4.7 | 23 resultados, todos históricos/intencionales o un título de sección | Conforme | Ver tabla de clasificación abajo | Worker |
| PL-22 | Revisión de fuentes de verdad por fase | Lectura del progreso | Una entrada por fase, 2 a 9 | Conforme | Progreso homónimo | Worker |
| PL-23 | Hallazgos consolidados en §12–§14 y propuestas para el Auditor | Lectura del plan | §12 (3 mejoras), §13 (ninguna), §14 (7 huérfanos/hallazgos), §14.1 (7 propuestas normativas) | Conforme | Plan, §12–§14.1 | Worker |
| PL-24 | Ningún archivo eliminado sin autorización | `git log --diff-filter=D --name-only ab4bd63..HEAD` | 9 archivos eliminados, los 9 autorizados | Conforme | Ver PL-17 | Worker |
| PL-25 | Chat del Worker renombrado según §2.9; convención completa en su destino | `set_session_title`; lectura de `03-entorno-git-y-worktrees.md` y `03-sesiones-contexto-y-handoff.md` | Chat renombrado a `nube_3.worker_reestructuracion-documental`; patrón, jerarquía 1–4 y `hist_` ya estaban completos desde la Fase 3/4; agregado en esta actualización: "crear chat nuevo es autónomo del Orquestador" (F16) | Conforme | Título de sesión actual; `03-sesiones-contexto-y-handoff.md` § Nombres de chats | Worker |
| PL-26 | Las 31 reglas de §4.8 están en su destino | Tabla de §4.8 con columna "verificado en" (ver tabla completa más abajo en esta evidencia) | Las 31 filas ya tenían destino en la migración original (Fases 3–5); 6 huecos puntuales completados en esta actualización (F3, F5, F13, F16, F29, F31) | Conforme | Tabla "§4.8 — 31 reglas verificadas" abajo | Worker |
| PL-27 | 21 flujos revisados contra §3.7; contenido retirado preservado; sin reglas inventadas | Lectura completa de los 11 flujos con indicios + grep de verificación sobre los 21 | 2 de 21 modificados (`11-dashboard.md`, `21-curva-s.md`: se retiraron referencias a agente/plan/Punch List, sin tocar ninguna regla funcional); 19 sin cambios | Conforme | Tabla "Fase 7B — antes/después por flujo" abajo | Worker |

## Resultados de pruebas técnicas

No aplica: este repositorio no tiene lint, build ni tests verificados (AGENTS.md). La verificación es por inspección de `git status`, `git log --follow`, `git show --stat` y el comando `grep` de §4.7 del plan.

## Regresiones verificadas

Se verifica en cada fase que los enlaces internos rotos por un `git mv` queden corregidos en el mismo commit (regla del plan, §5).

## Comando de verificación de §4.7 (Fase 8)

Comando ejecutado tal cual lo define el plan:

```bash
grep -rlE "Flujos de trabajo|Flujos%20de%20trabajo|Tareas de implementacion|Tareas%20de%20implementacion|Mejoras continuas|Mejoras%20continuas|docs/00-sistema|visual-companion" --include=*.md --include=*.html .
```

Resultado (23 archivos), clasificado:

- **12 archivos históricos de `docs/02-trabajo-activo/01-planes/`** (las tareas migradas tal cual) — permitido explícitamente por el propio comando de verificación del plan.
- **`docs/02-trabajo-activo/01-planes/README.md` y `planes-futuros.md`** — mencionan la ruta antigua solo como nota de procedencia de la migración ("migradas desde `docs/Tareas de implementacion/`"), no como enlace roto.
- **`docs/02-trabajo-activo/01-planes/2026-09-27-...md` y su progreso homónimo** — es este mismo plan y su registro de ejecución; mencionan las rutas antiguas al narrar la migración.
- **4 archivos de `docs/03-aprendizaje-continuo/`** (`orquestador-salta-flujo-de-roles-sin-auditoria.md`, `preguntas-frecuentes-flujo-orquestador.md`, `red-bloqueada-impide-autonomia-real.md`, `verificar-antes-de-afirmar.md`) — narrativa histórica que describe políticas y rutas tal como existían en el momento del hallazgo (2026-09-23), antes de esta reestructuración. No son enlaces funcionales rotos, son relato de hechos pasados — mismo criterio que aplica a las tareas históricas de `01-planes/`.
- **`docs/04-flujos-de-negocio/README.md`, `docs/05-diseno-y-referencias/README.md` y `mockups/README.md`** — mencionan "migrado/migradas desde `docs/Flujos de trabajo/`" / "`docs/visual-companion/`" como nota de procedencia intencional, igual que el criterio del comando permite para `06-mapa-documental.md`.
- **`AGENTS.md`** — un único resultado: el título de sección `### Tareas de implementación, Mejoras continuas y Reglas de negocio` (línea 229). Es un encabezado conceptual, no una ruta ni un enlace; no se renombró porque cambiar títulos de sección es contenido, no ruta (fuera del alcance de §10.1 para el Worker). Se anota como propuesta menor para el Auditor: alinear el título a la terminología nueva (`docs/02-trabajo-activo/`, `docs/03-aprendizaje-continuo/`) si lo considera necesario.

**Ningún resultado es un enlace roto real.** Todos son referencias históricas intencionales o el título de una sección.

## Artifacts alineados (Fase 8)

- **Flujo SDD a Cierre** (https://claude.ai/artifact/8Wq3QsjFfiNs8YSs5T1gjd): corregido — evidencia ahora apunta a `02-trabajo-activo/03-evidencia/` (antes decía "en el propio archivo del plan", contradecía §2.4); worktree corregido a `.worktrees/<entorno>-worker-N/` (antes mezclaba con `work-N`); referencia al diagrama actualizada a `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md`; agregadas menciones a D10 (lectura de flujos por rol) y a la consulta directa del Worker (D6). **Pendiente:** la simulación interactiva tiene 14 nodos, no un mapeo 1:1 con los 18 pasos numerados del documento normativo — alinear el conteo exacto de nodos queda para quien retome este artifact, es un rediseño de estructura, no una corrección de dato.
- **Recorrido del Plan** (https://claude.ai/artifact/YcT7akcjY5L2DXn1wPEeyx): reescrito — pasa de 9 fases (0–8) a 10 (0–9), con el contenido real de cada fase ejecutada (no la propuesta original); corregido el conteo "7 de 11" de tareas históricas (son 13 fechadas + 3 auxiliares); quitadas las menciones a `work-1`/`work-2`.

## §4.8 — 31 reglas verificadas (PL-26)

Cruce completo de las 7 fuentes (`AGENTS.md`, `README.md`, `docs/README.md`, los 3 de `docs/00-sistema/` y `plantilla-tarea.md`) contra su destino final, agregado en la actualización del plan del 2026-09-27. "Cambia (D1)" son las 4 filas que el propio §4.8 ya marca así — no son pérdidas, son decisiones ya tomadas en el Gate 1.

| # | Verificado en | Estado |
|---|---|---|
| F1 | `docs/README.md` § Ruta de lectura mínima / mapa de áreas | Conforme |
| F2 | `docs/README.md` | Conforme |
| F3 | `01-contexto-repositorio/04-pruebas-y-evidencia.md` § Ciclo de vida de un lote con Punch List | Conforme (completado en esta actualización) |
| F4 | `00-estandar-agentes/04-flujo-sdd-y-planes.md` § Diferencia entre chat normal y plan | Conforme |
| F5 | `00-estandar-agentes/04-flujo-sdd-y-planes.md` § Respuesta de activación del Orquestador | Conforme (completado en esta actualización) |
| F6 | `00-estandar-agentes/04-flujo-sdd-y-planes.md` (18 pasos, Gate Spec incluido) | Cambia (D1) — aplicado; propuesta pendiente para `AGENTS.md` en §14.1.8 |
| F7 | `00-estandar-agentes/02-roles-y-delegacion.md` § Los dos únicos puntos de parada | Conforme |
| F8 | `00-estandar-agentes/02-roles-y-delegacion.md` § Orquestador | Conforme |
| F9 | `01-contexto-repositorio/03-entorno-git-y-worktrees.md` § Regla de los dos repos | Conforme |
| F10 | `00-estandar-agentes/02-roles-y-delegacion.md` § Planner (10 entregables) + plantilla `02-plan.md` | Conforme |
| F11 | `00-estandar-agentes/02-roles-y-delegacion.md` § Worker + `01-contexto-repositorio/04-pruebas-y-evidencia.md` | Conforme |
| F12 | `00-estandar-agentes/02-roles-y-delegacion.md` § Auditor + plantilla `06-informe-auditoria.md` | Conforme |
| F13 | `01-contexto-repositorio/03-entorno-git-y-worktrees.md` § Dónde se trabaja | Conforme (completado en esta actualización) |
| F14 | `00-estandar-agentes/04-flujo-sdd-y-planes.md` (paso 2, "local por defecto") | Cambia (D1) — aplicado; propuesta pendiente para `AGENTS.md` en §14.1.8 |
| F15 | `00-estandar-agentes/03-sesiones-contexto-y-handoff.md` § Regla de contexto | Conforme |
| F16 | `01-contexto-repositorio/03-entorno-git-y-worktrees.md` § Chats (patrón) + `00-estandar-agentes/03-sesiones-contexto-y-handoff.md` (autonomía, no reutilizar `hist_`) | Conforme (completado en esta actualización) |
| F17 | `00-estandar-agentes/03-sesiones-contexto-y-handoff.md` § Inicio de cada chat | Conforme |
| F18 | `00-estandar-agentes/03-sesiones-contexto-y-handoff.md` § Compactar contexto | Conforme |
| F19 | `01-contexto-repositorio/03-entorno-git-y-worktrees.md` (ramas) | Conforme (`work-N` obsoleto, D2) |
| F20 | `01-contexto-repositorio/03-entorno-git-y-worktrees.md` (worktrees) | Conforme (ubicación cambia, D3) |
| F21 | `01-contexto-repositorio/03-entorno-git-y-worktrees.md` § Commits durante la implementación | Conforme |
| F22 | `00-estandar-agentes/05-aprendizaje-continuo.md` (genérico) + `01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md` (ejemplos) | Conforme (ejemplos agregados en esta actualización) |
| F23 | Plantilla `02-plan.md` | Conforme |
| F24 | `01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md` § Integrar una regla de negocio nueva en un flujo | Conforme (completado en esta actualización) |
| F25 | `00-estandar-agentes/05-aprendizaje-continuo.md` | Cambia (D1) — aplicado; propuesta pendiente para `README.md` en §14.1.9 |
| F26 | Plan, §2.5 | Conforme |
| F27 | Plan, §2.6 + `01-contexto-repositorio/03-entorno-git-y-worktrees.md` | Conforme |
| F28 | `01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md` | Conforme |
| F29 | `01-contexto-repositorio/02-arquitectura-y-fuentes-de-verdad.md` § Ante una contradicción entre fuentes | Conforme (completado en esta actualización, incluida la excepción D1) |
| F30 | `00-estandar-agentes/01-principios-y-seguridad.md` (lo universal); resto en `AGENTS.md` | Conforme |
| F31 | Plantilla `02-plan.md` (Estado con 6 valores, tabla Rol/Chat/Rama/Worktree/Estado, prompts) | Conforme (completado en esta actualización) |

**Ninguna de las 31 reglas se perdió.** 4 cambiaron por decisiones ya tomadas en el Gate 1 (D1); esos 4 cambios generan 3 propuestas normativas nuevas para `AGENTS.md`/`README.md` (§14.1, puntos 8–9), ya anotadas, no aplicadas por el Worker.

## Fase 7B — antes/después por flujo

Revisados los 21 flujos de `04-flujos-de-negocio/` contra §3.7, con foco en los 11 con indicios detectados en el cruce (`14-accesos-y-restricciones`, `10-generacion-pr`, `16-paneles`, `09-importar-dp`, `20-plan-maestro`, `18-control-avance`, `15-cronograma`, `12-checklist`, `21-curva-s`, `11-dashboard`, `04-notificaciones`) más el README, y una segunda pasada de `grep` sobre los 21 completos buscando "Punch List", "CERRADO 100%", "Worker/Auditor/Orquestador" literales y etiquetas "Agente A–D".

| Flujo | Resultado |
|---|---|
| `01` a `08`, `12`, `13`, `15`, `17`–`20` | Sin cambios — sin indicios reales tras la revisión (las coincidencias del cruce eran nombres de rol como "Planner" o términos técnicos como "sesión de servidor", no bitácora ni procedimiento de agentes) |
| `09-importar-dp.md` | Sin cambios — "el agente" se refiere al motor de análisis de la app (software), no a un rol de este estándar; sin indicios reales |
| `14-accesos-y-restricciones.md` | Sin cambios — el contenido "pendiente"/"a futuro" es una regla de negocio no implementada todavía (accesos que faltan), no un estado de plan ni bitácora de sesión |
| `16-paneles.md` | Sin cambios de contenido — tiene HTML de copia/pega sin limpiar y una sección "Estado de implementación" (Existente/Pendiente) que describe avance de la *funcionalidad*, no de un plan del flujo de Orquestador; se registra como hallazgo de formato en §14 del plan, no se reescribe sin autorización explícita |
| `11-dashboard.md` | **Modificado.** Se retiró el párrafo "Construido en dos fases" (fechas, número de PR, etiqueta "Agente C" y cita de archivo de plan — bitácora de implementación) y las dos menciones de "Agente D"/"(Fase 3)" que quedaban sueltas tras el retiro, reescribiendo esas dos frases para que queden autocontenidas sin perder su regla funcional (el toggle es funcional; la Curva S vive en pantalla propia). Ninguna regla de negocio cambió. Contenido retirado preservado abajo |
| `21-curva-s.md` | **Modificado.** Se retiró la etiqueta "Agente C" de una referencia cruzada al flujo 11 (queda "(flujo 11)") y el párrafo final que apuntaba al plan de implementación para "el detalle de implementación, la Punch List verificada y el cuadre" — es procedimiento de agentes/estado de plan, no una regla del flujo. El resto del archivo (incluida la sección "Por qué existe pantalla propia", que es razonamiento de negocio legítimo, no bitácora) se conserva igual. Contenido retirado preservado abajo |
| `README.md` | Sin cambios — las menciones a Orquestador/Planner/Auditor/Worker y Punch List son la propia regla de lectura por rol (D10) y la referencia al índice de planes, contenido legítimo de un README de navegación, no de un flujo |

**No se inventó ni se reescribió ninguna regla de negocio.** No surgió ningún conflicto de regla ambigua o contradictoria que requiriera consultar a Victor (D6) durante esta revisión.

### Contenido retirado de flujos (preservado íntegro)

**De `11-dashboard.md`:**

> Construido en dos fases:
>
> - **PR #6** (2026-08-17, spec `2026-08-16-dashboard-parcial-design.md`): Dashboard Parcial, sobre un diseño aprobado en Excel.
> - **Dashboard Fase 3** (Agente C, plan `2026-09-21-dashboard-fase-3-agente-c.md`): interfaz rehecha dentro del shell de la app, y construcción del Dashboard Completo (antes solo mostraba un aviso).

**De `21-curva-s.md`:**

> Ver [2026-09-21-curva-s-fase-3-agente-d.md](../02-trabajo-activo/01-planes/2026-09-21-curva-s-fase-3-agente-d.md) para el detalle de implementación, la Punch List verificada y el cuadre documentado contra el PR.

Ambos fragmentos son bitácora de implementación (quién lo construyó, con qué plan, en qué fecha) — la información completa sigue disponible en los propios archivos de plan (`2026-09-21-dashboard-fase-3-agente-c.md`, `2026-09-21-curva-s-fase-3-agente-d.md`) en `02-trabajo-activo/01-planes/`, que no se tocaron.

## Limitaciones o casos no verificables

Los artifacts de claude.ai citados en el plan (*Flujo SDD a Cierre*, *Recorrido del Plan*) sí eran accesibles desde esta sesión y se corrigieron (Fase 8). Sigue sin poder verificarse desde esta sesión el contenido exacto de la *Punch List de Mejoras* (artifact de checklist visual, fuera del alcance de lectura de este Worker) y de las 3 evidencias externas huérfanas de §4.6 — se deja registrado el texto/estado esperado donde aplica, sin poder confirmar el estado real del artifact.
