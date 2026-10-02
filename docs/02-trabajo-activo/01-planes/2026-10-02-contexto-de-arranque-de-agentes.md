# Plan — Contexto de arranque de los agentes: cerrar las fugas de lectura

## Identificación y estado

- Tema: reducir el contexto que un agente carga al arrancar y el que lee de más por obligación de la política.
- Fecha: 2026-10-02.
- Estado: `Implementando`.
- Gate Spec: `aprobado por Victor (2026-10-02)`.
- Gate 1: `aprobado por Victor (2026-10-02)`.
- Gate 2: `pendiente`.

**Pre-autorizaciones del Gate 1 (2026-10-02):** autorizado editar las fuentes de verdad listadas en § Archivos afectados; autorizado commit y push directo a `main` del repositorio de documentación al cerrar cada fase; confirmado que este plan **no toca la app real**. **No** autorizado: retirar los 10 Skills de redes sociales (quedan para otro momento).

> **Desviación del flujo que se declara:** Victor delegó el rol de Planner directamente, sin Spec previo. El diagnóstico medido de este plan hace las veces de Spec. Se pide el Gate Spec y el Gate 1 juntos en una sola consulta, porque la tabla de cambios de abajo es a la vez la especificación del cambio y el plan. Si Victor prefiere separarlos, el Gate Spec se pide primero y el plan se reordena.

## Referencia al Spec aprobado

No hay Spec aprobado. El § Diagnóstico de este archivo, con las mediciones reales, es el insumo del Spec. Al aprobar el Gate Spec se convierte en la referencia.

## Objetivo, alcance y no alcance

- **Resultado esperado:** que un agente que arranca con un brief bien escrito cargue lo mínimo, y que las lecturas que la política obliga sean proporcionales al trabajo. Meta concreta: la mediana del contexto de primera llamada de los subagentes **no baja de 38k** (es el piso del harness) pero **el crecimiento por sesión del Planner y del Auditor baja de ~195k a ~60k**, y el de un Worker de tanda simple, de ~133k a menos de 60k.
- **Alcance:** la política de lectura por rol (D10), la regla de arranque de cada agente, el disparador por documento (`lee_si:`), el tope de salida de herramientas, y la medición del arranque. Solo documentos de este repositorio y la configuración de Skills del usuario.
- **No alcance:** no se toca el prompt del sistema ni las definiciones de herramientas (eso es del harness y no lo controla este repositorio). No se reduce `AGENTS.md` por debajo de lo que dice su propia regla de las 200 líneas; se evalúa sacando reglas que pertenecen al estándar, no acortando el resto. No se reorganiza `docs/` en carpetas nuevas.
- **Validación esperada:** `python scripts/arranque.py 15` antes y después de un plan real, y el informe del Auditor sobre un plan que se ejecute con la política nueva.

## Diagnóstico (medido, no estimado)

Fuente: 28 sesiones del repositorio de documentación y de la app, del 2026-09-30 al 2026-10-01, leídas con `scripts/medir.py` y `scripts/arranque.py`.

### Qué trae un agente antes de hacer nada

| | Contexto de la 1ª llamada | Medición |
|---|---|---|
| Subagente (Worker, Planner, Auditor) | **40k** tokens (min 40k, mediana 40k, max 41k) | 8 sesiones |
| Sesión principal (Orquestador) | **52k** tokens | 4 sesiones |

Descomposición de esos 40k:

| Parte | Tokens | Se puede bajar desde este repositorio |
|---|---|---|
| Prompt del sistema + definiciones de herramientas | ~32k | No |
| `AGENTS.md` (18 KB) | 5.1k | Sí, parcialmente |
| Bloque de Skills | 3.0k | Sí |
| Brief de la tanda | el resto | Depende de cómo se escriba |

### Fuga 1 — Skills ya borrados que la herramienta sigue inyectando

`C:\Users\BRANDY\.claude\skills\.trash\` contenía 15 Skills eliminados (pdf, xlsx, docx, pptx, thesis, redes sociales). Claude Code los seguía publicando en el bloque de Skills de **cada** agente, incluidos los subagentes: **1.5k tokens por agente, sin uso posible**. Corregido el 2026-10-02 (ver § Registro de decisiones).

### Fuga 2 — D10 obliga a Planner y Auditor a leer los 21 flujos completos

Los 21 flujos de `docs/04-flujos-de-negocio/` suman **140.9 KB ≈ 40k tokens**. Con la regla D10 vigente, el Planner y el Auditor los leen enteros, **dos veces por plan, con el mismo contenido**. En el plan de permisos (2026-09-30) los flujos realmente afectados eran el 14 y el 16 (44 KB de 141 KB): se leyeron 141 KB para usar 44.

Evidencia directa: el Planner «plan de permisos» del 2026-10-01 consumió **52k tokens en 34 llamadas**, de los cuales 140k caracteres salieron por `Bash`: estaba leyendo los flujos por consola en lugar de abrirlos, y por eso su sesión creció 195k. Un Worker de la misma tanda, con dos flujos que tocar, creció 36k.

### Fuga 3 — Cada Worker lee el flujo del proceso entero para ejecutar 4 pasos

`docs/00-estandar-agentes/00-indice.md` fila «Implementación (Worker)» manda leer `04-flujo-sdd-y-planes.md` (16.6 KB) y `02-roles-y-delegacion.md` § Worker. En el plan de permisos fueron 12 subagentes: **~56k tokens repitiendo las mismas cuatro páginas de reglas de proceso**, que el brief ya podría traer resumidas.

### Fuga 4 — «Skills, antes de empezar» obliga a listar lo que ya viene inyectado

`docs/00-estandar-agentes/03-sesiones-contexto-y-handoff.md` manda a todo agente listar el contenido de `.claude/skills/` de los dos repositorios. La herramienta ya publica esa lista; el agente la vuelve a sacar: 2 llamadas y una lista duplicada por agente, ×14 agentes en un plan.

### Fuga 5 — Resultados de herramienta sin tope

Medido en las sesiones del 2026-10-01: un bloque `Read` de 54k caracteres (un archivo de progreso de 53.9 KB), un bloque `Artifact` de 36k, salidas de `Bash` de 19k y 9k, y `playwright_run_code_unsafe` sumando 64k caracteres en una tanda. El tope existe en `docs/01-contexto-repositorio/09-medicion-y-modelos.md` como nota «Aplicar en los briefs», **no como regla del estándar**, y por eso no se cumple.

### Fuga 6 — Contradicción entre dos fuentes normativas ya escritas

`AGENTS.md` § Frase de inicio de sesión (línea 98) manda leer «todos los archivos de `docs/04-flujos-de-negocio/`» en una sesión normal, mientras `04-flujo-sdd-y-planes.md` § Regla general de lectura mínima dice que «ningún rol lee todo el árbol de documentación de entrada». Las dos son normativa y se contradicen. Se reporta como observación sobre la política y se propone el cambio en la tabla.

## Cambios propuestos a reglas ya escritas (tabla del Gate 1)

La aprobación de esta tabla cubre a todos los Workers: ninguno edita una fuente de verdad sin estar en ella.

| # | Documento | Dice hoy | Pasaría a decir |
|---|---|---|---|
| 1 | `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md` (excepción D10, línea 60; regla de lectura mínima, línea 84; filas 6 y 12 de la tabla) | «el Planner y el Auditor leen **todos** los flujos de negocio del repositorio de documentación» | El Planner y el Auditor leen el **índice de flujos** y **solo los que el plan declara afectados**, igual que el Orquestador. Leen la lista completa únicamente en dos casos: el plan toca más de la mitad de los flujos, o el Auditor necesita comparar dos flujos enteros porque detectó un conflicto entre reglas. |
| 2 | `docs/00-estandar-agentes/00-indice.md` (fila «Implementación (Worker)») | `04-flujo-sdd-y-planes.md` (pasos 8–11) + `02-roles-y-delegacion.md` § Worker + los flujos que su parte toca | El **brief** de la tanda lleva el tramo que aplica (pasos 8–11 resumidos, ≈1.5 KB) y la regla D6. El Worker abre el documento completo solo si aparece un conflicto de negocio. El índice deja de ser la puerta de entrada del Worker. |
| 3 | `docs/00-estandar-agentes/03-sesiones-contexto-y-handoff.md` (línea 26) | «Todo agente, antes de empezar la tarea, **lista el contenido de `.claude/skills/`** del repositorio de documentación y del repositorio de código» | El brief **nombra** los Skills de la tanda (ya lo hace el paso 8). El agente **no** vuelve a listar las carpetas: la herramienta ya publica la lista disponible. Solo abre el `SKILL.md` del Skill que va a usar, y anota en el progreso «Skills revisados: ninguno aplica» cuando corresponda. |
| 4 | Cabecera de los 21 flujos de `docs/04-flujos-de-negocio/` + su `README.md` | El índice lista nombre y tema; el agente abre el flujo completo para decidir si le aplica | Cada flujo abre con **una línea `Lee si:`** (≤ 200 caracteres) que dice en qué situación el agente necesita ese flujo. El índice pasa a ser la **tabla de disparadores**: Planner, Auditor y Workers eligen por el disparador, no por el tema. |
| 5 | `docs/00-estandar-agentes/08-medicion-y-relevo.md` (nuevo apartado § briefs) + `docs/01-contexto-repositorio/09-medicion-y-modelos.md` | Tope de herramientas solo como nota: «Aplicar en los briefs. La evidencia guarda el resultado real, no el recortado» | Regla del estándar: ninguna orden sin tope de salida; ningún archivo mayor a 8 KB leído entero sin fragmento; un artefacto se abre por sección, no completo. La evidencia **sí** guarda el resultado real. |
| 6 | `docs/00-estandar-agentes/08-medicion-y-relevo.md` § Qué se mide + `docs/01-contexto-repositorio/09-medicion-y-modelos.md` § Ahorro de tokens | Se miden llamadas, herramientas, contexto máximo, caché leída y modelo | Se mide además el **contexto de la primera llamada** por sesión —la línea base que ningún brief puede bajar— y se revisa esa línea base cada vez que cambian `AGENTS.md` o el conjunto de Skills. La fila «Lectura de flujos de negocio» de `09-medicion-y-modelos.md` se actualiza con el cambio 1. |
| 7 | `AGENTS.md` § Frase de inicio de sesión (línea 98) | «...y **todos los archivos** de `docs/04-flujos-de-negocio/` para el contexto general» | «...y el **índice** de `docs/04-flujos-de-negocio/README.md`; se abre un flujo concreto solo cuando la tarea lo nombre». Resuelve la contradicción con la regla de lectura mínima del estándar. |

### Ahorro estimado (estimación, no medición — se confirma en el primer plan que use la política nueva)

| Ítem | Ahorro por plan | Base del cálculo |
|---|---|---|
| Cambio 1 (D10) | ~56k tokens | 2 agentes × (141 KB − 60 KB leídos) |
| Cambio 2 (brief en vez de leer el estándar) | ~50k tokens | 12 subagentes × ~4.7k del estándar repetido |
| Cambio 3 (no listar Skills) | ~28k tokens | 14 agentes × 2 llamadas + lista duplicada |
| Cambio 5 (topes de herramienta) | ~40k tokens | bloques de 54k + 36k + 19k + 9k observados |
| **Total** | **~175k tokens por plan** | |

Línea base: el arranque de un subagente es 40k y el piso del harness es ~32k, así que **el arranque no baja mucho**; lo que baja es el crecimiento. Ese es el punto, y conviene decirlo claro para no prometer lo que no se puede cumplir.

## Entorno, repositorios, ramas y worktrees

- Repositorio de documentación: `pg_control_proyectos`, rama `main`, sin worktree (por defecto se trabaja en `main`).
- Repositorio de código: **no se toca**. Este plan no implementa nada en la app.
- Configuración del usuario: `C:\Users\BRANDY\.claude\skills\` (movimiento de `.trash` fuera del directorio de Skills). Fuera de git, se reporta aparte.

## Skills aplicables

| Skill | Tanda | Para qué |
|---|---|---|
| `seguir-flujo-de-planes` | Antes del Gate 1 y antes del cierre | Verificar las puertas |
| `trasladar-hallazgos` | Tanda final (Documentador) | Llevar las filas del libro de hallazgos a su destino |
| `cerrar-planta` / `cerrar-tanda` | Final de cada tanda de implementación | Cierre con evidencia |
| Ninguno aplica | — | `verificar-permisos-por-rol` es de la app real y este plan no toca permisos |

## Fases y dependencias

- **F0 — Higiene del entorno** (ya ejecutada, 2026-10-02): mover los 15 Skills retirados fuera del directorio de Skills. No depende de ninguna puerta; la autorizó Victor en la consulta del 2026-10-02.
- **F1 — Cambios 1, 2, 3, 6** en el estándar y su índice. Es lo que quita la mayor parte del contexto. Depende del Gate 1.
- **F2 — Cambio 4**: `lee_si:` en los 21 flujos y tabla de disparadores en el índice. Depende del Gate 1. Es el único ítem que toca 22 archivos de contenido de negocio, y por eso va en tanda aparte.
- **F3 — Cambio 5**: topes de herramientas en el estándar. Depende del Gate 1.
- **F4 — Cambio 7**: `AGENTS.md`. Depende del Gate 1 y de que F1 esté escrita, porque las dos corrigen la misma regla.
- **F5 — Verificación**: medir un plan real con la política nueva y contrastar con la línea base de este plan. Depende de F1 a F4.

F1, F3 y F4 son el mismo tipo de edición (texto del estándar) y pueden ir en una tanda. F2 va aparte porque toca los flujos de negocio, que son fuente de verdad.

## Equipo del plan

| Rol | Modelo | Tanda | Rama | Estado |
|---|---|---|---|---|
| Orquestador | Sonnet | todas | `main` | activo |
| Planner | Sonnet | F0–F5 | `main` | en curso (este archivo) |
| Worker 1 | Sonnet | F1+F3+F4 | `main` | pendiente del Gate 1 |
| Worker 2 | Sonnet | F2 | `main` | pendiente del Gate 1 |
| Documentador | Sonnet | F5 | `main` | pendiente |
| Worker git | Haiku | a pedido | — | no aplica: todo va directo a `main` de documentación |
| Auditor | Sonnet | tras F5 | `main` | pendiente |

Un solo Worker por fase: los archivos de F1, F3 y F4 (`04-flujo-sdd-y-planes.md`, `00-indice.md`, `03-sesiones-contexto-y-handoff.md`, `08-medicion-y-relevo.md`, `AGENTS.md`) se solapan entre sí, así que dos Workers en paralelo se pisarían. La independencia real que justifica dos Workers es F2 contra el resto.

### Prompt del Auditor

Verificar, en este orden: (1) con `git log` que los cambios están en `main` del repositorio de documentación; (2) que la tabla «dice hoy / pasaría a decir» se aplicó **completa** en los siete puntos y no a medias en alguno; (3) que la excepción D10 del estándar y la fila «Lectura de flujos de negocio» de `09-medicion-y-modelos.md` dicen lo mismo (si no, el plan está a medias); (4) que los 21 flujos tienen su línea `Lee si:` y que ninguna miente sobre su contenido; (5) que `AGENTS.md` ya no contradice la regla de lectura mínima; (6) que `scripts/arranque.py` corre y su salida se cité textualmente. Informe en `02-trabajo-activo/04-auditoria/2026-10-02-contexto-de-arranque-de-agentes.md`.

## Archivos / componentes afectados

Estándar: `04-flujo-sdd-y-planes.md`, `00-indice.md`, `03-sesiones-contexto-y-handoff.md`, `08-medicion-y-relevo.md`.
Contexto del repositorio: `01-contexto-repositorio/09-medicion-y-modelos.md`.
Norma raíz: `AGENTS.md`.
Negocios: `docs/04-flujos-de-negocio/README.md` + los 21 flujos (solo cabecera).
Plantillas: `06-plantillas/13-brief-de tandas.md` (bloque de reglas del rol).
Herramientas: `scripts/arranque.py` (nuevo, ya creado), `scripts/README.md` (ya registrado).
Fuera de git: `C:\Users\BRANDY\.claude\skills_retirados_2026-10-02\`.

## Punch List embebida

### Estado de aprobación

Gate 1: pendiente.

### Validación en servidor / API

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| V1 | F0 | Los 15 Skills retirados ya no aparecen en el bloque de Skills de un agente nuevo | Arrancar una sesión nueva y contar los Skills: debe bajar de 29 a 14 | Sin verificar |
| V2 | F0 | `python scripts/arranque.py 15` corre en los dos repositorios | Salida del comando en la evidencia | Conforme |
| V3 | F1 | D10 dice índice + flujos afectados, con sus dos excepciones | El texto nuevo está en `04-flujo-sdd-y-planes.md` y `09-medicion-y-modelos.md` | Sin verificar |
| V4 | F1 | El brief del Worker trae el tramo del rol y el Worker no abre el estándar | Brief de una tanda real: el Worker no leyó `04-flujo-sdd-y-planes.md` | Sin verificar |
| V5 | F1 | La regla de listar Skills sale de `03-sesiones-contexto-y-handoff.md` | Texto nuevo + un Worker que anota «Skills revisados» sin listar | Sin verificar |
| V6 | F2 | Los 21 flujos tienen `Lee si:` y el índice es la tabla de disparadores | Un grep de `Lee si:` devuelve 21 coincidencias | Sin verificar |
| V7 | F2 | Cada `Lee si:` describe algo que el flujo realmente contiene | El Auditor abre 5 flujos al azar y contrasta el disparador con su contenido | Sin verificar |
| V8 | F3 | El tope de herramientas está como regla en el estándar | Texto en `08-medicion-y-relevo.md` | Sin verificar |
| V9 | F4 | `AGENTS.md` ya no manda leer todos los flujos | Línea 98 revisada | Sin verificar |
| V10 | F5 | La línea base del arranque quedó medida antes y después | Dos salidas de `arranque.py`: una de antes (este plan) y una del plan que use la política nueva | Sin verificar |

## Riesgos y bloqueos

- **R1 — Perder de vista una regla que el Worker necesitaba.** El cambio 2 mete reglas de proceso en el brief, y un brief mal escrito es una regla perdida. Mitigación: el bloque de reglas del rol va en la plantilla `13-brief-de-tandas.md`, no a mano; y el Auditor lo revisa (V4).
- **R2 — Que el disparador `Lee si:` mienta.** 21 disparadores son 21 promesas. Mitigación: el Auditor contrasta 5 al azar (V7). Si uno miente, se corrige el disparador, no la excepción.
- **R3 — El ahorro no se vea.** Los 32k del piso del harness no se mueven, y puede parecer que «no se logró». Mitigación: la meta del plan está escrita en crecimiento, no en arranque (§ Objetivo), y el V10 compara las dos medidas.
- **R4 — Sobrecargar al Planner con 21 disparadores.** Si cada uno es largo, el índice deja de ser corto. Mitigación: el límite de 200 caracteres por línea, y el V6 lo comprueba.
- **B1 — La contradicción de la fuga 6 es entre `AGENTS.md` y el estándar.** Mientras no se apruebe el cambio 7, sigue viva. No bloquea el resto.

## Registro de decisiones

| Fecha | Decisión | Quién |
|---|---|---|
| 2026-10-02 | El objetivo es reducir el contexto que carga un agente al arrancar y el que lee de más por la política | Victor |
| 2026-10-02 | **No usar Obsidian**: no reduce lo que el agente lee; se adopta en su lugar la capa de disparadores (`Lee si:`) en Markdown plano | Victor |
| 2026-10-02 | **Cambiar D10**: Planner y Auditor dejan de leer los 21 flujos completos | Victor |
| 2026-10-02 | Autorizados de inmediato: retirar los 15 Skills de `.trash` y promover `arranque.py` a `scripts/` | Victor |
| 2026-10-02 | Se declara la desviación del flujo: el Planner fue delegado sin Spec previo | Planner, para que Victor lo confirme o lo corrija |
| 2026-10-02 | **Gate Spec aprobado**: el diagnóstico medido pasa a ser el Spec de referencia | Victor |
| 2026-10-02 | **Gate 1 aprobado** con los siete cambios de la tabla. Pre-autorizado: editar esas fuentes de verdad, y commit + push a `main` de documentación por fase. Confirmado que no se toca la app real. **No** autorizado: retirar los 10 Skills de redes sociales | Victor |

## Enlaces a progreso y evidencia homónimos

- Progreso: `docs/02-trabajo-activo/02-progreso/2026-10-02-contexto-de-arranque-de-agentes.md`
- Evidencia: `docs/02-trabajo-activo/03-evidencia/2026-10-02-contexto-de-arranque-de-agentes.md`
- Auditoría: `docs/02-trabajo-activo/04-auditoria/2026-10-02-contexto-de-arranque-de-agentes.md`

## Libro de hallazgos

### Mejoras (de trabajo)

| ID | Fecha | Quién | Qué | Destino propuesto | Estado | Enlace |
|---|---|---|---|---|---|---|
| H1 | 2026-10-02 | Planner F0 | Los Skills dentro de `.trash` **siguen** inyectándose en el bloque de Skills de cada agente: borrarlos no basta, hay que sacarlos del directorio de Skills | `03-aprendizaje-continuo/` (workaround de configuración) | Registrada | |
| H2 | 2026-10-02 | Planner F0 | Para saber qué carga un agente al arrancar hay que leer la **primera** llamada de su `.jsonl`, no el máximo: `medir.py` suma `cache_creation` y no separa la línea base | `03-aprendizaje-continuo/` (ya cubierto por `scripts/arranque.py`) | Registrada | `scripts/arranque.py` |
| H3 | 2026-10-02 | Planner F0 | Los `tool_result` están en el turno del usuario y los `tool_use` en el del asistente: un desglose que solo mira turnos del asistente no ve ningún bloque | `03-aprendizaje-continuo/` | Registrada | `scripts/arranque.py` |

### Reglas de negocio acordadas en esta tarea

Ninguna. Este plan no toca reglas del sistema de control de proyectos.

### Observaciones sobre la política

| ID | Fecha | Quién | Qué | Estado |
|---|---|---|---|---|
| O1 | 2026-10-02 | Planner F0 | `AGENTS.md` línea 98 manda leer todos los flujos; la regla de lectura mínima del estándar dice que ningún rol los lee todos. Contradicción entre dos fuentes normativas | Registrada |
| O2 | 2026-10-02 | Planner F0 | El tope de salida de herramientas existe solo como nota en `09-medicion-y-modelos.md`, fuera del estándar, y por eso no se cumple | Registrada |
| O3 | 2026-10-02 | Planner F0 | Los resultados de `Read`, `Artifact` y `Bash` sin tope llegaron a 54k, 36k y 19k caracteres en un solo bloque, en sesiones que la política de metas declaraba sanas | Registrada |
| O4 | 2026-10-02 | Planner F0 | Los archivos de progreso miden 49–54 KB y el Auditor debe leer plan + progreso + evidencia + los flujos: el costo de leer el estado del plan crece con cada tanda | Registrada |
| O5 | 2026-10-02 | Planner F0 | La regla de listar Skills manda una acción que la herramienta ya hizo: trabajo mecánico sin valor y tokens de más en cada agente | Registrada |
| O6 | 2026-10-02 | Planner F0 | El verificador tiene un uso de método previsto y nuncapiloteado: `07-verificador-de-acciones.md` § «Decisiones de método (opcional, consultivo)» permite pedirle una opinión cheap y no bloqueante sobre texto —si una regla contradice un flujo, en cuál de los cuatro grupos cae un hallazgo, si la evidencia sostiene Conforme— y dice «se piloteará en un plan antes de volverse regla». Ese piloto no ocurrió. Además `.claude/settings.local.json` existe pero **no tiene ningún hook registrado**, así que el verificador no se dispara nunca | Registrada |

### Carpetas/archivos huérfanos

Ninguno detectado.

## Informe de Auditoría

Pendiente: `docs/02-trabajo-activo/04-auditoria/2026-10-02-contexto-de-arranque-de-agentes.md`

## Mensaje de cierre

Pendiente.

## Elementos postergados propuestos para planes futuros

- **Los 10 Skills de redes sociales que siguen en `~/.claude/skills/`** (publisher, caption-writer, x-writer, threads-writer, linkedin-writer, content-calendar, brand-onboarding, social-media-manager, social-creative-designer, social-performance-review) suman ~4.1k caracteres ≈ **1.2k tokens en cada agente** y no tienen relación con este proyecto. Se pueden mover al mismo directorio de retirados, pero son de otro proyecto de Victor: no se tocan sin su decisión.
- **Partir los archivos de progreso por tanda.** Hoy miden 49–54 KB y el Auditor los lee enteros (O4). Resolverlo con un índice de secciones y un tope de lectura en el prompt del Auditor.
- **`docs/06-material-de-apoyo/`** entra en la lectura de algún rol sin que esté justificado en la tabla de lectura por rol. Conviene revisarlo cuando se implemente el cambio 4.
- **Piloto de Jev para el chequeo de contradicciones (propuesto por Victor el 2026-10-02, O6).** El paso 6 del flujo obliga al Planner a «anticipar incongruencias con reglas de negocio ya documentadas, revisando los flujos afectados», y hoy lo hace con su propio contexto: por eso el Planner del plan de permisos creció 195k. El caso de uso que Jev ya describe en el estándar encaja exactamente ahí —una pregunta no bloqueante por flujo, «¿esta regla nueva contradice este texto?», sobre el texto que le pasa el script—. El Planner seguiría decidiendo; solo dejaría de cargar los 141 KB para hacerlo. Límites, todos verificados en `07-jev-verificador.md`: el script debe reunir el texto, porque Jev no ve el repositorio ni ejecuta comandos; su ventana es de 32.000 tokens, y el flujo mayor (el 14, 26.6 KB) entra de sobra; y las preguntas deben ser específicas o da falsas alarmas, porque con la genérica «¿es seguro?» un merge legítimo dio 0,39. El costo por llamada sube con los tokens de entrada, así que el total con 21 flujos hay que **medirlo**, no estimarlo: el dato de $0,00002 corresponde a una llamada de ~480 tokens de entrada, no a una de 10k. No se registra ningún hook sin autorización de Victor, porque un hook defectuoso bloquearía todas las sesiones, incluidas las de un plan en curso.
