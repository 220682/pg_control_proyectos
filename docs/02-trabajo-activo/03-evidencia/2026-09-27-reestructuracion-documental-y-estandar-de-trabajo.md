# Evidencia — Reestructuración documental y estándar de trabajo

> Referencia: [plan](../01-planes/2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md) y [progreso](../02-progreso/2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md).

## Entorno y fecha

`pg_control_proyectos`, rama `main`, directo. Sin worktree. Inicio: 2026-09-27.

## Rol/usuario y datos autorizados

Worker asignado por el Orquestador tras el Gate 1. Sin datos ni secretos reales involucrados: el cambio es puramente documental (reorganización de archivos Markdown).

## Punch List ejecutada

Tabla completa en el plan, §9. Se actualiza ítem por ítem con resultado, método y evidencia a medida que se cierra cada uno.

| ID | Esperado | Método | Observado | Estado | Evidencia | Responsable |
|---|---|---|---|---|---|---|
| PL-01 | Plan movido a `01-planes/`; progreso y evidencia homónimos creados | `git status`, `ls` | `git mv` del plan aplicado; este archivo y su homónimo de progreso creados | Conforme | Este commit | Worker |

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
