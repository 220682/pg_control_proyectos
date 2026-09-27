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

## Limitaciones o casos no verificables

No hay acceso automatizado a los artifacts de claude.ai citados en el plan (*Flujo SDD a Cierre*, *Recorrido del Plan*, *Punch List de Mejoras*, evidencias huérfanas de §4.6): se deja registrado el texto de corrección donde aplique, sin poder confirmar que se aplicó en el artifact real (Fase 8, PL-20).
