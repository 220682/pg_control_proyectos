# Plan — Reestructuración documental y estándar de trabajo

> **Estado:** **APROBADO — GATE 1 (Victor, 2026-09-27).** Plan v2, Punch List, tablas de §4, decisiones D1–D10 (§10.2, con D1 y D10 cambiadas por Victor) y autorización A. Excepción: la tarea `2026-09-23-cronograma-import-y-versatilidad-vinculo.md` **se elimina** (no se migra). Listo para asignar al Worker (§17).
>
> **Ejecución previa sin aprobación:** las Fases 0 y 1 fueron ejecutadas y pusheadas por un agente anterior el 2026-09-27 (commits `404ddb3` y `be53526`) cuando el plan todavía decía "Propuesto. No ejecutar hasta que Victor apruebe". Queda registrado en §11 (Registro de decisiones) y §12 (Mejoras de trabajo). La Fase 2 revisa lo creado en la Fase 1 contra este plan corregido.
>
> **Quién implementa:** un **Worker** asignado por el Orquestador tras el Gate 1 (§10). La sesión que corrigió este plan no lo implementa.
>
> **Propósito:** reorganizar la documentación del repositorio para separar de forma explícita:
>
> 1. El estándar reusable de trabajo de agentes.
> 2. El contexto específico de `pg_control_proyectos`.
> 3. Los planes, su progreso y su evidencia.
> 4. El aprendizaje continuo que nace de los planes.
> 5. Los flujos de negocio, diseño y material de apoyo.
>
> **Regla central:** no se elimina ningún archivo sin autorización explícita de Victor (§10.3). Todo movimiento o renombre se hace con `git mv`, según las tablas origen → destino de §4, que forman parte de lo que Victor aprueba en el Gate 1.

---

# 0. Fuente normativa y material de referencia

**El diagrama es la fuente normativa del flujo de trabajo (D1, Victor 2026-09-27).** Este plan y los artifacts se ajustan a él: si difieren, se corrige el plan o el artifact, no el diagrama. Si el diagrama no cubre un punto, aplica el plan. Las decisiones explícitas de Victor en el Gate 1 que cambian el diagrama (D2 nombre de rama en el Mermaid, D6 consulta del Worker, D10 lectura por rol) se aplican al diagrama en la Fase 3.

| Recurso | Ubicación | Rol | Estado frente a este plan |
|---|---|---|---|
| Diagrama commit/push/merge/gates | `diagrama-commit-push-merge-gates.md` (raíz) → destino `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md` (§4.3) | **Fuente normativa del flujo** (D1): tabla por rol + Mermaid | Base de §3.2 (`04-flujo-sdd-y-planes.md`) y de la tabla de lectura mínima. **Inconsistencia interna a corregir:** la tabla dice `<entorno>-worker-N` y el Mermaid dice `work-N`. |
| Artifact **Flujo SDD a Cierre** | https://claude.ai/artifact/8Wq3QsjFfiNs8YSs5T1gjd | Vista derivada interactiva del flujo | Base de la secuencia unificada de §3.2. **A corregir:** dice que la evidencia va "en el propio archivo del plan" (contradice §2.4) y mezcla la rama `<entorno>-worker-N` con el worktree `.worktrees/work-N/`. |
| Artifact **Recorrido del Plan** | https://claude.ai/artifact/YcT7akcjY5L2DXn1wPEeyx | Vista derivada: simulación fase por fase | Sus ítems adicionales se incorporaron a §5. **A corregir:** numeración de fases (ahora 0–9), conteo "7 de 11" (son 13 tareas), estado local que no refleja lo ya ejecutado. |
| Artifact **Punch List de Mejoras** | https://claude.ai/artifact/8yHL1cn8auxbYghuRoiNhd | Evidencia externa (checklist visual) | Enlazado hoy solo desde `docs/README.md:81`. Se conserva el enlace al reescribir `docs/README.md`. |
| Artifacts de evidencia de tareas cerradas: **Sub-lote 2 — Checklist F0-F7** (https://claude.ai/artifact/Xv6wSxUA2fbXaFX8ACe1rh), **Dashboards y Curva S — Fase 3** (https://claude.ai/artifact/CdUMm5cdoxGjYPUsMHM85q), **Matriz de Accesos y Restricciones** (https://claude.ai/artifact/Lq9LEPv8FE7QpSvke5f9Yz) | claude.ai | Evidencia externa | **Huérfanos:** ningún archivo del repo los enlaza. Se registran en §4.6 para enlazarlos (decisión 2 de §6.1). |

---

# 1. Resultado esperado

Al terminar, la estructura activa del repositorio será:

```text
pg_control_proyectos/
├── AGENTS.md
├── README.md
├── .gitignore          (conserva la exclusión de .worktrees/ por compatibilidad)
└── docs/
    ├── README.md
    ├── 00-estandar-agentes/
    ├── 01-contexto-repositorio/
    ├── 02-trabajo-activo/
    ├── 03-aprendizaje-continuo/
    ├── 04-flujos-de-negocio/
    ├── 05-diseno-y-referencias/
    └── 06-material-de-apoyo/
```

- No quedan carpetas ni archivos sueltos en la raíz (regla de Victor: "no quiero carpetas sueltas, todas deben estar en su lugar").
- `.worktrees/` **no forma parte de este repositorio**: los Workers implementan código en `py_control_proyectos_web` (diagrama, fila IMPLEMENTACIÓN). Los worktrees se documentan en `01-contexto-repositorio/03-entorno-git-y-worktrees.md` como recurso de ese repo.
- No se crean carpetas por plan. Cada plan, progreso o evidencia es un único archivo Markdown con el mismo nombre base.

---

# 2. Convenciones globales

## 2.1. Numeración de carpetas y archivos

Los prefijos numéricos definen orden de lectura, no prioridad ni fecha.

```text
00 = estándar y punto de partida.
01 = contexto particular del repositorio.
02 = trabajo operativo activo.
03 = aprendizaje que nace del trabajo.
04 = reglas y flujos de negocio.
05 = diseño y referencias visuales.
06 = material de apoyo no normativo.
```

Dentro de una carpeta, la numeración define el orden recomendado de lectura (`00-indice.md`, `01-...`, `02-...`).

Los documentos de trabajo real usan fecha ISO y slug sin espacios: `YYYY-MM-DD-<slug-descriptivo>.md`.

## 2.2. Convención de README

Cada carpeta operativa tiene un `README.md` corto que responde únicamente:

1. Qué vive en la carpeta.
2. Qué no vive en la carpeta.
3. Qué documento se debe leer después.
4. Qué regla de nombre o ciclo de vida aplica.

El README no duplica el contenido de sus archivos hijos.

## 2.3. Convención de lectura mínima

Regla tomada del diagrama ("Regla general de lectura mínima"), **ajustada por Victor en el Gate 1 (D10)**: **el Orquestador, el Planner y el Auditor leen todos los flujos de negocio; el Worker lee solo los que toca su parte.** Ningún rol lee todo `docs/` de entrada. Cada rol lee:

1. `AGENTS.md` y `docs/README.md` para ubicarse.
2. El estándar que corresponde a su rol (según `00-estandar-agentes/00-indice.md`).
3. El plan/progreso/evidencia del tema activo.
4. Flujos de negocio: **Orquestador, Planner y Auditor, todos**; **Worker, solo los que el plan indica afectados por su parte**. `design.md` solo si el plan toca UI.
5. El **índice** (no el contenido completo) de `03-aprendizaje-continuo/`, abriendo una mejora completa solo cuando su etiqueta coincide con lo que se está por hacer.

Victor no tiene lectura obligatoria: decide el objetivo y aprueba en los Gates con lo que el rol correspondiente le presenta.

> Esta regla **reemplaza** la instrucción vigente de AGENTS.md y `docs/README.md` de "leer todos los Flujos de trabajo para contexto general" (que hoy aplica a todos los roles). En la Fase 3 se ajusta también la columna de lectura y la "Regla general de lectura mínima" del diagrama. El cambio en AGENTS.md es normativo → lo propone el Auditor y lo aplica el Orquestador tras el Gate 2 (§5, cierre).

## 2.4. Convención de documentos por plan

Un plan de trabajo real usa el mismo nombre base en tres ubicaciones:

```text
02-trabajo-activo/01-planes/YYYY-MM-DD-<tema>.md
02-trabajo-activo/02-progreso/YYYY-MM-DD-<tema>.md
02-trabajo-activo/03-evidencia/YYYY-MM-DD-<tema>.md
```

| Archivo | Contiene | Quién lo escribe |
|---|---|---|
| **Plan** | Spec/SDD, plan, **Punch List embebida**, roles, registro de decisiones, Mejoras (de trabajo), Reglas de negocio acordadas, Carpetas/archivos huérfanos, **Informe de Auditoría** y **mensaje de cierre**. Las plantillas de `06-plantillas/` son el molde de cada sección que se copia adentro, no archivos separados. | Orquestador (Spec), Planner (plan + Punch List), Auditor (informe), Orquestador (cierre) |
| **Progreso** | Estado vivo: fase actual, avances, pendientes, commits/ramas, bloqueos, **hallazgos registrados en el momento** y **handoffs** (secciones fechadas al final). | Worker (y cualquier rol que retome la tarea) |
| **Evidencia** | Punch List ejecutada con resultado por ítem, Playwright/pruebas/consultas y **enlace al artifact de checklist visual** si existe. | Worker |

Reglas:

- Evidencia vive en **dos lugares que coexisten** (decisión 2 de §6.1): el artifact externo de claude.ai (checklist visual) y el archivo local de `03-evidencia/` (registro estructurado en texto, con enlace al artifact). No se duplican capturas o logs sin referencia explícita.
- `progreso` y `evidencia` se crean al iniciar la ejecución aprobada (tras el Gate 1), nunca para planes futuros.
- Las tareas históricas ya existentes se migran como **un único archivo** a `01-planes/`, sin descomponerlas (decisión 4 de §6.1 y §4.5).

## 2.5. Convención de planes futuros

`planes-futuros.md` es el último archivo fijo de `01-planes/`. Solo se registra allí un pendiente cuando Victor decide explícitamente: "Esto no se hará dentro del plan actual; lo dejamos para después."

Un elemento de `planes-futuros.md` no es un plan aprobado, no tiene progreso, evidencia ni Worker, y debe pasar por Spec/SDD antes de convertirse en plan real:

```text
planes-futuros.md → Spec/SDD → plan aprobado (Gate 1) → progreso y evidencia
```

El ítem se conserva como "promovido" con enlace al nuevo plan; no se borra sin trazabilidad.

## 2.6. Convención de ramas y worktrees

Fuentes: diagrama (tabla), artifact *Flujo SDD a Cierre* y `convenciones-de-trabajo.md` (corrección de Victor del 2026-09-23).

| Tipo de trabajo | Repositorio | Rama | Worktree |
|---|---|---|---|
| Documentación de proceso (Spec, plan, progreso, evidencia, hallazgos, informe de auditoría, fuentes de verdad, mensaje de cierre) | `pg_control_proyectos` | `main`, directo, sin rama ni merge | No se usa |
| Código de la app | `py_control_proyectos_web` | `<entorno>-worker-N` (ej. `local-worker-1`, `nube-worker-1`); nunca `main` hasta el merge tras el Gate 2 | `.worktrees/` de ese repo, subcarpeta con el mismo nombre de la rama (**confirmar en Gate 1**, §10.2) |

- `entorno` es `local` o `nube`; se verifica con la herramienta disponible, no se asume.
- La nomenclatura `work-1`/`work-2` queda **obsoleta** (tabla de pool de `convenciones-de-trabajo.md` y Mermaid del diagrama). Solo se conserva como dato histórico en las tareas que la usaron (ej. `2026-09-23-paquetes-de-trabajo.md`).
- No se crea, borra, renombra o reasigna rama ni worktree sin autorización de Victor.
- Los roles de coordinación (Orquestador, Planner, Auditor) trabajan en `main` de `pg_control_proyectos`.

## 2.7. Convención de autorizaciones (Gates)

Fuente: artifact *Flujo SDD a Cierre* y diagrama.

| Gate | Qué aprueba Victor | Efecto |
|---|---|---|
| **Gate Spec** | El Spec/SDD | Autoriza delegar al Planner |
| **Gate 1** | Plan + Punch List + tablas origen → destino + autorizaciones de §10.3 | **Autoriza toda la implementación de una vez: cero aprobaciones intermedias hasta el cierre.** Incluye commit + push del Worker dentro del alcance aprobado (cada ~35% de la Punch List, nunca a medias de un ítem). |
| **Gate 2** | Cierre, incluidas las propuestas del Auditor | Autoriza merge de código, cambios normativos a fuentes de verdad centrales y creación de Skills |

- Nunca se pide el Gate 2 sin Informe de Auditoría ya emitido.
- Si Victor dice **No** en un Gate, se vuelve al paso anterior (Spec, Planner o Worker), nunca se avanza.

## 2.8. Convención de fuentes de verdad

Fuentes de verdad de operación:

```text
AGENTS.md      → norma raíz para agentes.
README.md      → visión, arquitectura y cambios de alto nivel del sistema.
docs/README.md → navegación y operación documental dentro de docs/.
```

Los flujos de negocio (`docs/04-flujos-de-negocio/NN-*.md`) son la fuente de verdad de las reglas funcionales de cada tema.

| Tipo de hallazgo | Destino | Quién escribe y cuándo |
|---|---|---|
| Regla funcional/de negocio **validada por Victor en el momento** | Flujo de negocio dueño de la regla | Worker, al consolidar hallazgos (antes de entregar) |
| Mejora de trabajo / aprendizaje | `03-aprendizaje-continuo/` | Worker, al consolidar hallazgos |
| Evidencia de una implementación | Archivo de evidencia del plan | Worker |
| Cambio de arquitectura/visión | `README.md` raíz | Auditor propone → Victor aprueba en Gate 2 → Orquestador aplica |
| Cambio de comportamiento de agentes | `AGENTS.md` o `00-estandar-agentes/` | Auditor propone → Gate 2 → Orquestador aplica |
| Cambio de navegación de `docs/` | `docs/README.md` | Auditor propone → Gate 2 → Orquestador aplica |
| Cambio específico de este repositorio | `01-contexto-repositorio/` | Auditor propone → Gate 2 → Orquestador aplica |
| Diseño/UI | `05-diseno-y-referencias/design.md` | Auditor propone → Gate 2 → Orquestador aplica |
| Procedimiento reusable que ya se repitió | Skill agnóstico en `.claude/skills/<nombre>/SKILL.md` | Auditor propone (`PROPONER SKILL`) → Gate 2 → Orquestador crea |
| Pendiente fuera de alcance | `planes-futuros.md` | Solo con decisión explícita de Victor |

**El Worker nunca edita** `AGENTS.md`, README raíz, `docs/README.md` ni el estándar de agentes por hallazgos propios: los deja anotados en el progreso para que el Auditor los evalúe. (Excepción escrita y acotada para **este** plan en §10.1, porque su objeto es precisamente construir esa estructura.)

### Revisión obligatoria de fuentes de verdad

Después de **cada sesión relevante, cada fase de plan, cada implementación y cada corrección aprobada**, el rol que trabajó ejecuta esta revisión:

1. Revisar si lo realizado creó, corrigió, aclaró o contradijo una regla documentada.
2. Clasificar el destino según la tabla de arriba.
3. Escribir lo que le corresponde a su rol; anotar en el progreso lo que corresponde a otro rol.
4. Registrar qué fuente se actualizó (o se propone), qué sección, por qué y con qué evidencia.
5. Si nada aplica, registrar explícitamente: **"Fuentes de verdad revisadas: sin cambios requeridos."** El silencio no cuenta como revisión hecha.

---

# 3. Estructura objetivo y contenido de cada carpeta

## 3.1. `docs/README.md`

**Propósito:** mapa de navegación de `docs/`.

**Debe contener:** mapa de las siete áreas; ruta de lectura mínima (§2.3); diferencia entre conversación simple y trabajo mediante plan; diferencia entre plan, progreso, evidencia y aprendizaje; enlaces a los README de cada área; enlace al artifact **Punch List de Mejoras** (hoy en la línea 81).

**No debe contener:** reglas detalladas de seguridad; procedimientos completos de Git, Playwright o diseño; reglas de negocio duplicadas; estado de planes particulares; la sección "Migración en curso" (se elimina al terminar la Fase 6).

## 3.2. `00-estandar-agentes/`

**Propósito:** estándar reusable de trabajo para agentes. Sus reglas se aplican a otro repositorio sin depender de nombres, URLs, datos, cuentas ni flujos de este proyecto. **No nombra personas:** usa "Responsable humano" (en este repo es Victor, lo que se declara en `01-contexto-repositorio/`).

```text
00-estandar-agentes/
├── README.md                          (ya existe — Fase 1)
├── 00-indice.md
├── 01-principios-y-seguridad.md
├── 02-roles-y-delegacion.md
├── 03-sesiones-contexto-y-handoff.md
├── 04-flujo-sdd-y-planes.md           (nace del diagrama por git mv, §4.3)
├── 05-aprendizaje-continuo.md
└── 06-plantillas/
```

### `00-indice.md`

- Qué leer según rol y tipo de solicitud: chat normal; análisis; Spec/SDD; planificación; Worker; Auditoría; cierre/handoff.
- **Tabla de lectura mínima por rol y paso**, tomada de la columna "Qué debe leer antes" del diagrama, redactada sin rutas propias del repo (usa los nombres de área: "índice de aprendizaje continuo", "flujos de negocio afectados", "sistema de diseño").
- No replica el contenido de las políticas; solo direcciona.

### `01-principios-y-seguridad.md`

- No inventar hechos, reglas, rutas ni herramientas; **verificar antes de afirmar, o preguntar** (promovido de `2026-09-23-verificar-antes-de-afirmar.md`).
- Protección de secretos.
- Acciones que requieren autorización: borrar, renombrar, commit, push, merge, PR, ramas, worktrees, migraciones, despliegues, comunicaciones y cambios externos — indicando qué Gate las cubre (§2.7).
- Revisar contexto, alcance y diff antes de entregar.
- No declarar éxito sin evidencia.

### `02-roles-y-delegacion.md`

- Roles: Responsable humano, Orquestador, Planner, Worker y Auditor. Entradas, salidas y límites de cada uno.
- El Orquestador es el punto de contacto de coordinación con el Responsable humano. **Excepción documentada** (artifact *Flujo SDD*): ante un conflicto de regla de negocio no anticipado durante la implementación, el Worker consulta al Responsable humano en el momento y registra pregunta y respuesta en el progreso (**confirmar en Gate 1**, §10.2).
- El Orquestador nunca planifica ni implementa: delega al Planner tras el Gate Spec, salvo excepción escrita en el plan y autorizada.
- Cuándo dividir trabajo y cuándo usar un solo Worker. No paralelizar si se tocan los mismos archivos, migraciones, componentes base o recursos no aislados.
- Referencia cruzada visible a `03-aprendizaje-continuo/historico.md` (incidente "Orquestador salta el flujo de roles" y FAQ del flujo).

### `03-sesiones-contexto-y-handoff.md`

- Un chat por tarea o etapa clara; contexto mínimo de inicio; cuándo compactar; cómo cerrar un chat.
- Handoff obligatorio ante cambio de sesión, chat, LLM o entorno: se escribe como **sección fechada al final del progreso** del plan, con la plantilla `07-handoff.md`.
- Una conversación histórica no se reutiliza como contexto activo de una tarea nueva.
- Promovido de `2026-09-23-sendmessage-no-alcanza-sesiones-create-session.md` (limitación de comunicación entre sesiones), redactado de forma agnóstica.

### `04-flujo-sdd-y-planes.md`

- Diferencia entre chat normal y plan de implementación; condiciones de activación del Orquestador.
- **Secuencia unificada** (artifact *Flujo SDD a Cierre* + diagrama):

```text
 1. Objetivo — Responsable humano
 2. Entorno — Orquestador define local (por defecto) o nube, y la nomenclatura de ramas/worktrees; revisa recursos libres antes de pedir crear nuevos
 3. Spec/SDD — Orquestador + Responsable humano (plantilla 01-spec-sdd) → commit + push a main
 4. GATE SPEC — ¿aprueba el Spec?   No → vuelve a 3
 5. Delegación al Planner — Orquestador (el Spec aprobado es la entrada)
 6. Plan + Punch List — Planner, en el único archivo de plan; anticipa conflictos de negocio revisando los flujos afectados → commit + push a main
 7. GATE 1 — ¿aprueba plan + Punch List?   No → vuelve a 6.   Sí → autoriza toda la implementación, sin aprobaciones intermedias
 8. Implementación — Worker, en su rama <entorno>-worker-N (código) → commit + push a su rama cada ~35%, nunca a medias de un ítem, nunca a main
 9. ¿Conflicto de regla de negocio no anticipado? Sí → consulta en el momento y registra pregunta/respuesta en el progreso; vuelve a 8
10. Verificación y evidencia — Worker: Playwright cuando aplica (nunca solo por código), Punch List completada, archivo de evidencia + enlace al artifact
11. Consolidar hallazgos — Worker: escribe reglas de negocio validadas, aprendizajes y evidencia (commit + push a main de la documentación); deja anotado lo que toque fuentes de verdad centrales
12. Auditoría — Auditor: primero confirma con git log / git branch --contains que los commits están en la rama del Worker asignado; luego revisa SDD, plan, Punch List y evidencia. Informe: APLICAR AHORA / PROPONER A RESPONSABLE / NO PROMOVER / PROPONER SKILL
13. ¿Informe listo para cierre?   No → vuelve a 8
14. Orquestador consolida y presenta — informe + resultados + propuestas de cambio a fuentes de verdad centrales
15. GATE 2 — ¿aprueba el cierre?   No → vuelve a 8
16. Tres acciones independientes (cualquier orden, cada una solo si aplica):
    a. Merge <entorno>-worker-N → main del repositorio de código
    b. Cambios aprobados a fuentes de verdad centrales → commit + push a main
    c. Skill aprobado → .claude/skills/<nombre>/SKILL.md, redactado de forma agnóstica
17. Mensaje de cierre — Orquestador, dentro del propio archivo del plan: confirma qué ocurrió de 16a–16c y que todo quedó pusheado → commit + push a main
18. Cierre — el plan es 100% recién cuando todo está pusheado/mergeado; el archivo del plan nunca se borra ni se resume
```

- Incluye el diagrama Mermaid y la tabla por rol del archivo original (fuente normativa, D1), ya corregidos según las decisiones del Gate 1: rama `<entorno>-worker-N` en ambos (D2), consulta del Worker a Victor en su propio chat (D6), lectura de flujos por rol (D10) y los mismos 18 pasos y sin nombres propios de repositorio (se reemplazan por "repositorio de documentación" / "repositorio de código"; los nombres reales van en `01-contexto-repositorio/`).
- Referencia cruzada visible a la FAQ del flujo del Orquestador (en `historico.md`).

### `05-aprendizaje-continuo.md`

- Diferencia entre hallazgo, mejora de trabajo, regla de negocio, decisión pendiente, evidencia y procedimiento reusable.
- Remite a la revisión obligatoria de fuentes de verdad (§2.8).
- Proceso de promoción: hallazgo → registro → clasificación → evidencia → auditoría → aprobación → actualización del destino correcto.
- No todo aprendizaje se promueve; una experiencia aislada no se promueve sin evidencia y aprobación.
- Escalación a Skill: cuando un procedimiento reusable **se repite**, el Auditor puede proponer (`PROPONER SKILL`) convertirlo en un Skill agnóstico. Requiere aprobación en Gate 2.
- Formato del índice de `03-aprendizaje-continuo/README.md`: cada mejora con una **etiqueta corta de categoría** para lectura rápida.

## 3.3. `00-estandar-agentes/06-plantillas/`

**Única ubicación de plantillas vigentes.** No existe un "plantillas.md" paralelo ni copias en otras carpetas.

```text
06-plantillas/
├── README.md                (ya existe — Fase 1)
├── 01-spec-sdd.md
├── 02-plan.md
├── 03-progreso.md
├── 04-evidencia.md
├── 05-punch-list.md
├── 06-informe-auditoria.md
├── 07-handoff.md
├── 08-aprendizaje.md
└── 09-cierre.md
```

| Plantilla | Dónde se usa | Debe incluir |
|---|---|---|
| `01-spec-sdd.md` | Sección Spec del archivo de plan | Estado; problema y contexto; resultado esperado; alcance y no alcance; usuarios/roles afectados; reglas de negocio y documentos afectados; datos, API, migraciones o dependencias; diseño/UI aplicable; riesgos y decisiones pendientes; criterios de aceptación; estrategia de prueba/evidencia; aprobación (Gate Spec). |
| `02-plan.md` | Archivo de plan | Identificación y estado; referencia al Spec aprobado; objetivo, alcance y no alcance; entorno, repos, ramas y worktrees; fases y dependencias; asignación de roles; archivos/componentes afectados; Punch List embebida (formato `05-punch-list`); riesgos y bloqueos; registro de decisiones; enlaces a progreso y evidencia homónimos; **las tres secciones obligatorias heredadas de `plantilla-tarea.md`: `Mejoras (de trabajo)`, `Reglas de negocio acordadas en esta tarea`, `Carpetas/archivos huérfanos`** (se llenan en el momento del hallazgo, no al cierre); Informe de Auditoría (formato `06`); mensaje de cierre (formato `09`); elementos postergados propuestos para `planes-futuros.md`. |
| `03-progreso.md` | Archivo de progreso | Referencia al plan; estado general y fase actual; tabla de roles/Workers y estado; avances terminados; trabajo actual; pendientes; commits, ramas y worktrees usados; **hallazgos registrados en el momento** (incluidas preguntas de negocio y la respuesta de Victor); bloqueos, riesgos y decisiones requeridas; próximo paso verificable; última actualización y responsable; **sección de handoffs fechados**. No contiene resultados extensos de pruebas. |
| `04-evidencia.md` | Archivo de evidencia | Referencia al plan; entorno y fecha; rol/usuario y datos autorizados, sin secretos; tabla de Punch List ejecutada (ítem, esperado, método, observado, estado, evidencia/ruta/enlace, responsable); **enlace al artifact de checklist visual** si existe; resultados de Playwright, pruebas, logs, consultas o cálculos; regresiones verificadas; limitaciones o casos no verificables. |
| `05-punch-list.md` | Sección Punch List del plan | Estado de aprobación (Gate 1); ítems funcionales; datos y cálculos; permisos; UI/responsive/accesibilidad; estados vacío/carga/error; validación en servidor/API; regresión; estados `Sin verificar` / `Conforme` / `Observado` / `No aplica`; evidencia mínima por ítem. |
| `06-informe-auditoria.md` | Sección Informe de Auditoría del plan | Alcance auditado; material revisado; **verificación de rama** (commits en la rama del Worker asignado, con `git log`/`git branch --contains`); cumplimiento de SDD, plan, Punch List y evidencia; verificación de la revisión de fuentes de verdad por fase; `APLICAR AHORA`; `PROPONER A RESPONSABLE`; `NO PROMOVER`; `PROPONER SKILL`; pendientes técnicos y documentales; recomendación: listo, bloqueado o requiere corrección. |
| `07-handoff.md` | Sección de handoffs del progreso | Objetivo y estado; plan/progreso/evidencia relacionados; rama, worktree y último commit; terminado y no terminado; pruebas ejecutadas; bloqueos y riesgos; qué debe leer el siguiente agente; próximo paso concreto. |
| `08-aprendizaje.md` | Archivo individual en `03-aprendizaje-continuo/` | Origen (plan/sesión/evidencia); observación; evidencia; clasificación; etiqueta de categoría; destino propuesto; cambio propuesto; estado (borrador, pendiente, promovido, rechazado, reemplazado); referencia a la aprobación. |
| `09-cierre.md` | Sección de cierre del plan | Alcance completado y no completado; estado final de la Punch List; evidencia; auditoría y decisiones del Gate 2; documentos promovidos; aprendizajes registrados; pendientes enviados a `planes-futuros.md`; merge / fuentes de verdad / Skill realizados o no; confirmación de 100% pusheado; autorización de cierre. |

## 3.4. `01-contexto-repositorio/`

**Propósito:** solo información aplicable a `pg_control_proyectos`. No contiene el estándar universal ni reglas de negocio.

```text
01-contexto-repositorio/
├── README.md                              (ya existe — Fase 1)
├── 00-indice.md
├── 01-proposito-y-alcance.md
├── 02-arquitectura-y-fuentes-de-verdad.md
├── 03-entorno-git-y-worktrees.md
├── 04-pruebas-y-evidencia.md
├── 05-diseno-y-ui.md
└── 06-mapa-documental.md
```

| Documento | Contenido |
|---|---|
| `00-indice.md` | Qué documento leer según la tarea: documentación, Git/worktree, pruebas, UI, flujos de negocio. |
| `01-proposito-y-alcance.md` | Repositorio documental frente al repositorio de la app (`py_control_proyectos_web`); qué pertenece a cada uno; **el Responsable humano de este repo es Victor**; límites de cambios y de validación disponibles. |
| `02-arquitectura-y-fuentes-de-verdad.md` | Las tres fuentes de verdad; flujo dueño de cada regla; cómo se promueve un cambio (§2.8); cuándo se actualiza README raíz y AGENTS.md. |
| `03-entorno-git-y-worktrees.md` | **Regla de los dos repos** (§2.6): documentación de proceso a `main` de este repo; código en `<entorno>-worker-N` del repo de la app. Pool real verificado de ramas y worktrees del repo de la app (verificar con `git branch -a` / `git worktree list` en ese repo antes de escribirlo; no copiar la tabla obsoleta `work-1`/`work-2`). Commits cada ~35% de la Punch List, solo al terminar el ítem en curso. `git add` explícito. Promovido de `2026-09-23-turbopack-worktree-junction.md`. |
| `04-pruebas-y-evidencia.md` | Uso del artifact de Punch List interactivo; cuándo es obligatorio Playwright; capturas, login y datos reales/autorizados; cómo registrar evidencia en el MD homónimo; qué hacer si un caso no puede verificarse. Promovido de `verificacion-playwright-falsos-negativos`, `eslint-baseline-vs-cero` y `tests-contadores-congelados`. |
| `05-diseno-y-ui.md` | `docs/05-diseno-y-referencias/design.md` es lectura obligatoria cuando se modifica UI; uso de mockups y nombres de pantallas; no inventar componentes. |
| `06-mapa-documental.md` | Índice de los flujos existentes; material de apoyo relevante; **mapa origen → destino de la migración** (copia final de §4); enlaces verificados a archivos clave. |

## 3.5. `02-trabajo-activo/`

**Propósito:** trabajo planificado, en ejecución o cerrado, con su trazabilidad. No contiene reglas permanentes ni aprendizaje independiente.

```text
02-trabajo-activo/
├── README.md                     (ya existe — Fase 1)
├── 01-planes/
│   ├── README.md                 (ya existe — Fase 1)
│   ├── YYYY-MM-DD-<tema>.md      (planes nuevos y tareas históricas migradas)
│   └── planes-futuros.md         (git mv desde tareas-futuras.md)
├── 02-progreso/
│   ├── README.md                 (ya existe — Fase 1)
│   └── YYYY-MM-DD-<tema>.md
└── 03-evidencia/
    ├── README.md                 (ya existe — Fase 1)
    └── YYYY-MM-DD-<tema>.md
```

- `01-planes/README.md` incluye el índice de planes activos, cerrados (históricos) y en preparación.
- `planes-futuros.md`: cada ítem registra origen, descripción, motivo, estado y si requiere Spec/SDD.

## 3.6. `03-aprendizaje-continuo/`

**Propósito:** aprendizajes que nacen de la ejecución de planes y que requieren evaluación antes de alterar reglas, contexto, procedimientos o fuentes de verdad.

```text
03-aprendizaje-continuo/
├── README.md                     (ya existe — Fase 1; índice a corregir en Fase 5)
├── YYYY-MM-DD-<aprendizaje>.md   (las 11 mejoras migradas, §4.5)
├── pendientes-de-promocion.md
└── historico.md
```

- `pendientes-de-promocion.md`: lista consolidada de lo que espera aprobación; no reemplaza los archivos individuales.
- `historico.md`: aprendizajes promovidos, rechazados, reemplazados o cerrados, con destino final y fecha.
- Un archivo migrado y promovido **no se borra**: queda en la carpeta y su estado pasa a "promovido" en `historico.md` con enlace al destino.

## 3.7. `04-flujos-de-negocio/`

**Propósito:** reglas funcionales y operativas permanentes, una vez por tema dueño.

```text
04-flujos-de-negocio/
├── README.md                                         (ya existe — Fase 1)
├── 01-configuracion.md
├── 02-usuarios.md
├── ...
├── 19-paquetes-de-trabajo-y-jerarquia-de-control.md  (renombrado: el original tiene espacios)
├── 20-plan-maestro.md
└── 21-curva-s.md
```

- `README.md`: índice de los 21 flujos; regla de lectura por rol (§2.3: Orquestador, Planner y Auditor leen todos; el Worker solo los afectados por su parte); regla de actualización (una regla se escribe una vez en su flujo dueño; los demás enlazan).
- `NN-<tema>.md`: funcionamiento, datos, reglas, estados, roles y restricciones del flujo. Se actualiza solo con reglas validadas por Victor. No contiene bitácoras, estados de plan ni procedimientos de agentes.

## 3.8. `05-diseno-y-referencias/`

```text
05-diseno-y-referencias/
├── README.md       (ya existe — Fase 1)
├── design.md       (git mv desde docs/visual-companion/design.md)
└── mockups/
    ├── README.md   (ya existe — Fase 1)
    └── *.html      (los 6 mockups de docs/visual-companion/)
```

- `design.md` es la fuente de verdad visual y lectura obligatoria para cambios de UI.
- `mockups/` no contiene evidencia de pruebas de un plan (eso va en `03-evidencia/`).

## 3.9. `06-material-de-apoyo/`

**Propósito:** material de referencia que se conserva pero no es fuente de verdad ni parte del flujo activo.

**Contenido tras la Fase 6** (decisión 3 de §6.1):

```text
06-material-de-apoyo/
├── README.md                    (ya existe — Fase 1; se actualiza con cada carpeta que entra)
├── conocimiento/
├── Dashboard ejemplo/
├── Formatos/
├── Imagenes para fronted/
└── Informacion para pruebas/
```

- Las carpetas se mueven con su nombre actual (renombrarlas no está aprobado; si Victor lo quiere, va a `planes-futuros.md`).
- El README describe cada subcarpeta en una línea y se actualiza cada vez que se agrega, mueve, reclasifica o retira material.

---

# 4. Migración de la estructura actual (tablas origen → destino)

Estas tablas se aprueban en el Gate 1. El Worker las ejecuta **sin pedir aprobaciones intermedias**. Lo que no esté en ellas no se mueve: se anota en el progreso como hallazgo.

## 4.1. `docs/00-sistema/`

| Archivo | Destino del contenido | Qué pasa con el archivo original |
|---|---|---|
| `roles-y-flujo.md` | Reglas universales → `00-estandar-agentes/02-roles-y-delegacion.md` y `04-flujo-sdd-y-planes.md` | Se elimina tras integrar su contenido **solo si §10.3-A está autorizado**; si no, `git mv` a `06-material-de-apoyo/obsoleto/` |
| `gestion-de-sesiones-y-contexto.md` | `00-estandar-agentes/03-sesiones-contexto-y-handoff.md` (sin la duplicación literal que tiene hoy) | Igual que arriba |
| `convenciones-de-trabajo.md` | Reglas propias de este repo → `01-contexto-repositorio/03-entorno-git-y-worktrees.md`; reglas universales → estándar | Igual que arriba |

## 4.2. Carpetas de `docs/`

| Origen | Destino | Regla |
|---|---|---|
| `docs/Flujos de trabajo/NN-*.md` (21) | `docs/04-flujos-de-negocio/` | `git mv` sin cambiar contenido, salvo enlaces. Renombrar `19-paquetes de trabajo y jerarquia de control.md` → `19-paquetes-de-trabajo-y-jerarquia-de-control.md`. |
| `docs/Flujos de trabajo/README.md` | Contenido útil → `04-flujos-de-negocio/README.md` | Original: §10.3-A |
| `docs/visual-companion/design.md` | `docs/05-diseno-y-referencias/design.md` | `git mv` |
| `docs/visual-companion/*.html` (6: `crear-rdts`, `entorno-trabajo-herramientas`, `index`, `requerimiento-de-servicios-crear`, `requerimiento-de-servicios-listado`, `requerimiento-de-servicios-partidas`) | `docs/05-diseno-y-referencias/mockups/` | `git mv` |
| `docs/visual-companion/README.md` | Contenido útil → `05-diseno-y-referencias/README.md` | Original: §10.3-A |
| `docs/Tareas de implementacion/` | §4.5 | — |
| `docs/Mejoras continuas/` | §4.5 | — |

## 4.3. Archivos sueltos en la raíz

| Origen | Destino | Regla |
|---|---|---|
| `2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md` (este plan) | `docs/02-trabajo-activo/01-planes/` | `git mv` en la Fase 2, antes de cualquier otra cosa |
| `diagrama-commit-push-merge-gates.md` | `docs/00-estandar-agentes/04-flujo-sdd-y-planes.md` | `git mv` (conserva historial) y luego se completa y se hace agnóstico según §3.2 |

## 4.4. Carpetas de apoyo en la raíz

| Origen | Destino |
|---|---|
| `conocimiento/` | `docs/06-material-de-apoyo/conocimiento/` |
| `Dashboard ejemplo/` | `docs/06-material-de-apoyo/Dashboard ejemplo/` |
| `Formatos/` | `docs/06-material-de-apoyo/Formatos/` |
| `Imagenes para fronted/` | `docs/06-material-de-apoyo/Imagenes para fronted/` |
| `Informacion para pruebas/` | `docs/06-material-de-apoyo/Informacion para pruebas/` |

## 4.5. Trabajo histórico

### Tareas de implementación (13 fechadas + 3 auxiliares — verificado 2026-09-27)

| Archivo | Estado verificado | Destino |
|---|---|---|
| `2026-09-20-control-avance-plan-maestro.md` | Cerrada (decisión 4) | `01-planes/`, tal cual |
| `2026-09-20-evm-fase-0-catalogo-unico.md` | Cerrada (decisión 4) | `01-planes/`, tal cual |
| `2026-09-20-sub-lote-2-alcance-proyecto.md` | Cerrada (decisión 4) | `01-planes/`, tal cual |
| `2026-09-21-curva-s-fase-3-agente-d.md` | CERRADO (Punch List 20/20, PR #16 mergeado) | `01-planes/`, tal cual |
| `2026-09-21-dashboard-fase-3-agente-c.md` | Implementada y verificada (Punch List 25/25) | `01-planes/`, tal cual |
| `2026-09-21-evm-fase-1-congelar-tarifa.md` | Cerrada (decisión 4) | `01-planes/`, tal cual |
| `2026-09-21-fix-reemplazar-dp.md` | Cerrada (decisión 4) | `01-planes/`, tal cual |
| `2026-09-21-pr-fase-1-pipeline-rdt.md` | Completa, verificada y mergeada | `01-planes/`, tal cual |
| `2026-09-21-pr-fase-2-pipeline-linea-base.md` | Completa, verificada y mergeada | `01-planes/`, tal cual |
| `2026-09-22-plan-unico-orquestador-sesiones-worktrees-Claude-y-local.md` | Ejecutado; pendiente de cierre 100% (decisión 4) | `01-planes/`, tal cual |
| `2026-09-23-reordenamiento-y-actualizacion-fuentes-de-verdad.md` | Ejecutado (decisión 4) | `01-planes/`, tal cual |
| `2026-09-23-cronograma-import-y-versatilidad-vinculo.md` | Abierta ("Implementando") | **Se elimina con `git rm`** (decisión de Victor en el Gate 1, 2026-09-27). No se migra. La única referencia a ella, en `2026-09-23-orquestador-salta-flujo-de-roles-sin-auditoria.md` (línea 3), se reemplaza por texto sin enlace: "Origen: tarea `2026-09-23-cronograma-import-y-versatilidad-vinculo.md` (eliminada por decisión de Victor, 2026-09-27)". |
| `2026-09-23-paquetes-de-trabajo.md` | **Abierta** (Fase 1 terminada en `work-1`). **Tiene texto con codificación dañada** (ej. `â†’`, `Ã³`) | `01-planes/`, tal cual; sus archivos de progreso y evidencia se crean cuando se retome esa tarea (D9). **No se corrige la codificación en este plan**: se reporta a Victor (§14) |
| `plantilla-tarea.md` | Reemplazada por las 9 plantillas (decisión 1) | Tras verificar que `02-plan.md` cubre sus 13 secciones: §10.3-A |
| `tareas-futuras.md` | — | `git mv` → `01-planes/planes-futuros.md` (decisión 5) y se adapta al formato de §2.5 |
| `resumen-checklists.md` | — | Cada entrada cronológica se agrega como sección "Resumen de checklist (migrado)" al archivo de plan de su tema en `01-planes/`. Las entradas sin plan dueño se listan en §14. Original: §10.3-A (decisión 6: no se conserva como archivo agregado) |

- **"Tal cual"** significa sin editar el contenido. Sus rutas internas antiguas no se corrigen: se listan en la evidencia como enlaces históricos.

### Mejoras continuas (11 — clasificación de §6.1)

Las 11 se mueven con `git mv` a `docs/03-aprendizaje-continuo/` **conservando su nombre**. Después se aplica su clasificación:

| Archivo | Clasificación | Acción |
|---|---|---|
| `2026-09-21-acceso-postgres-sin-ipv6.md` | Histórico (excepción cerrada) | Entrada en `historico.md` |
| `2026-09-21-migraciones-sql-sobrecargas-huerfanas.md` | Se queda como aprendizaje, no promociona | Solo en el índice, etiqueta `migraciones-sql` |
| `2026-09-21-verificacion-playwright-falsos-negativos.md` | Promover | → `01-contexto-repositorio/04-pruebas-y-evidencia.md`; entrada "promovido" en `historico.md` |
| `2026-09-23-eslint-baseline-vs-cero.md` | Promover | → `04-pruebas-y-evidencia.md`; `historico.md` |
| `2026-09-23-orquestador-salta-flujo-de-roles-sin-auditoria.md` | Histórico (ya promovido a roles) | `historico.md` + referencia cruzada desde `02-roles-y-delegacion.md` |
| `2026-09-23-preguntas-frecuentes-flujo-orquestador.md` | Histórico con rastro visible | `historico.md` + referencias cruzadas desde `04-flujo-sdd-y-planes.md` y `02-roles-y-delegacion.md` |
| `2026-09-23-red-bloqueada-impide-autonomia-real.md` | Pendiente (acción de Victor) | `pendientes-de-promocion.md` |
| `2026-09-23-sendmessage-no-alcanza-sesiones-create-session.md` | Promover | → `00-estandar-agentes/03-sesiones-contexto-y-handoff.md`; `historico.md` |
| `2026-09-23-tests-contadores-congelados.md` | Promover | → `04-pruebas-y-evidencia.md`; `historico.md` |
| `2026-09-23-turbopack-worktree-junction.md` | Promover | → `01-contexto-repositorio/03-entorno-git-y-worktrees.md`; `historico.md` |
| `2026-09-23-verificar-antes-de-afirmar.md` | Promover (principio universal) | → `00-estandar-agentes/01-principios-y-seguridad.md`; `historico.md` |

- El índice de `03-aprendizaje-continuo/README.md` creado en la Fase 1 **tiene errores de etiqueta** (ej. "acceso a Postgres sin IPv6" y "red bloqueada" bajo `git/ramas`). Se rehace en la Fase 5 con una fila por archivo, su etiqueta correcta y su estado.

## 4.6. Evidencia externa huérfana

| Artifact | Tarea dueña (a verificar leyendo la tarea) | Acción |
|---|---|---|
| Sub-lote 2 — Checklist F0-F7 | `2026-09-20-sub-lote-2-alcance-proyecto.md` | Enlazarlo desde el índice de `01-planes/README.md` (la tarea histórica no se edita) |
| Dashboards y Curva S — Fase 3 | `2026-09-21-dashboard-fase-3-agente-c.md` y `2026-09-21-curva-s-fase-3-agente-d.md` | Igual |
| Matriz de Accesos y Restricciones | Flujo `14-accesos-y-restricciones.md` o tarea `sub-lote-2` | Igual; si no hay dueño claro, se lista en §14 |

## 4.7. Inventario de enlaces a rutas antiguas (base de la verificación)

Archivos que hoy referencian `Flujos de trabajo`, `Tareas de implementacion`, `Mejoras continuas`, `00-sistema`, `visual-companion`, `plantilla-tarea`, `tareas-futuras` o `resumen-checklists` (verificado 2026-09-27):

- **Fuentes centrales:** `AGENTS.md`, `README.md`, `docs/README.md`.
- **A migrar/integrar:** los 3 de `docs/00-sistema/`; `docs/Flujos de trabajo/README.md` y los flujos `10`, `14`, `17`, `20` y `21`; 10 de las 11 mejoras continuas; `docs/visual-companion/README.md`, `design.md` e `index.html`.
- **READMEs de la Fase 1:** `02-trabajo-activo/01-planes/README.md`, `04-flujos-de-negocio/README.md` y `05-diseno-y-referencias/mockups/README.md`.
- **Históricos (no se editan):** 12 tareas de `Tareas de implementacion/`, `plantilla-tarea.md` y `tareas-futuras.md`.

Rutas **ya inexistentes** citadas en fuentes centrales: `Sistema hibrido/`, `plantillas/`, `RDTs movimiento de tierra.../`, `memoria.md`, `control_de_proyectos.txt` y `.cursor/rules/*` (en `AGENTS.md` y `README.md`).

Comando de verificación (debe devolver solo archivos históricos de `01-planes/`, `03-aprendizaje-continuo/historico.md` o menciones textuales intencionales en `06-mapa-documental.md`):

```bash
grep -rlE "Flujos de trabajo|Flujos%20de%20trabajo|Tareas de implementacion|Tareas%20de%20implementacion|Mejoras continuas|Mejoras%20continuas|docs/00-sistema|visual-companion" --include=*.md --include=*.html .
```

---

# 5. Fases de implementación

**Reglas para el Worker durante todas las fases:**

- Gate 1 autoriza toda la implementación: **no hay "presentar a Victor" entre fases.** Cualquier caso no cubierto por §4 se anota en el progreso como hallazgo y **no se ejecuta**.
- Commit + push directo a `main` de `pg_control_proyectos` cada ~35% de la Punch List (§9), solo al terminar completo el ítem en curso, con `git add` explícito. **Cada `git mv` va en el mismo commit que la actualización de los enlaces que rompe** (así ninguna fuente queda rota entre commits).
- Al terminar cada fase: revisión de fuentes de verdad (§2.8) registrada en el progreso.

## Fase 0 — Diagnóstico ✅ (cerrada)

- [x] Inventario de la estructura actual.
- [x] Clasificación de tareas y mejoras (§6.1, completada en la corrección v2 con las 6 tareas que faltaban, §4.5).
- [x] Inventario de enlaces a rutas antiguas (§4.7, agregado en la corrección v2).
- [x] Tablas origen → destino completas (§4, completadas en la corrección v2).

## Fase 1 — Estructura vacía y navegación ✅ (ejecutada antes del Gate 1)

- [x] Siete carpetas numeradas y sus READMEs (commit `be53526`).
- [x] Sección "Migración en curso" en `docs/README.md`.
- [ ] Revisión de lo creado contra este plan corregido → se hace en la Fase 2.

## Fase 2 — Arranque del plan y ajuste de la Fase 1

- [ ] `git mv` de este plan a `docs/02-trabajo-activo/01-planes/` (§4.3) y actualizar su referencia en `docs/README.md`.
- [ ] Crear `02-progreso/2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md` y `03-evidencia/` homónimo con las secciones definidas en §3.3 (`03-progreso` y `04-evidencia`).
- [ ] Revisar los READMEs de la Fase 1 contra §2 y §3; corregir lo que contradiga el plan. Mínimo: el índice de `03-aprendizaje-continuo/README.md` (§4.5) y las menciones a `work-N`.
- [ ] Revisión de fuentes de verdad de la Fase 2.

## Fase 3 — Estándar y plantillas

- [ ] `git mv` del diagrama a `00-estandar-agentes/04-flujo-sdd-y-planes.md` y completarlo según §3.2: secuencia unificada de 18 pasos, Mermaid y tabla con `<entorno>-worker-N`, redacción agnóstica.
- [ ] Crear `00-indice.md` con la tabla de lectura mínima por rol y paso.
- [ ] Crear `01-principios-y-seguridad.md`, `02-roles-y-delegacion.md`, `03-sesiones-contexto-y-handoff.md` y `05-aprendizaje-continuo.md`, integrando el contenido universal de `docs/00-sistema/` (§4.1).
- [ ] Crear las 9 plantillas de §3.3. `02-plan.md` incluye las 3 secciones obligatorias; `06-informe-auditoria.md` incluye la verificación de rama y `PROPONER SKILL`.
- [ ] Verificar que ningún MD del estándar nombre a Victor, `pg_control_proyectos`, `py_control_proyectos_web` ni rutas propias del repo.
- [ ] Revisión de fuentes de verdad de la Fase 3.

## Fase 4 — Contexto del repositorio

- [ ] Crear los 7 documentos de `01-contexto-repositorio/` (§3.4), integrando las reglas propias del repo de `convenciones-de-trabajo.md`.
- [ ] En `03-entorno-git-y-worktrees.md`: regla de los dos repos, `<entorno>-worker-N`, worktrees en el repo de la app, commits cada ~35%. El pool real se verifica en el repo de la app; si no hay acceso, se escribe "por verificar" y se anota como hallazgo.
- [ ] Revisión de fuentes de verdad de la Fase 4.

## Fase 5 — Trabajo activo y aprendizaje

- [ ] `git mv` de `tareas-futuras.md` → `01-planes/planes-futuros.md` y adaptarlo al formato de §2.5.
- [ ] `git mv` de las 11 mejoras a `03-aprendizaje-continuo/` y actualizar sus enlaces internos.
- [ ] Aplicar la clasificación de §4.5: integrar las 6 promovidas en su destino y crear `historico.md` y `pendientes-de-promocion.md`.
- [ ] Rehacer el índice etiquetado de `03-aprendizaje-continuo/README.md`.
- [ ] No crear planes, progreso, evidencia ni aprendizajes ficticios.
- [ ] Revisión de fuentes de verdad de la Fase 5.

## Fase 6 — Migrar flujos, diseño y material de apoyo

- [ ] `git mv` de los 21 flujos (con el renombre del 19) y actualización de sus enlaces, en el mismo commit.
- [ ] `git mv` de `design.md` y los 6 mockups; integrar `visual-companion/README.md` en `05-diseno-y-referencias/README.md`.
- [ ] `git mv` de las 5 carpetas de apoyo (§4.4) y actualización de `06-material-de-apoyo/README.md`.
- [ ] Actualización **mecánica** de rutas en `AGENTS.md`, `README.md` y `docs/README.md` en el mismo commit que cada movimiento (excepción de §10.1).
- [ ] Revisión de fuentes de verdad de la Fase 6.

## Fase 7 — Trabajo histórico

- [ ] `git mv` de las 12 tareas a `01-planes/` tal cual y `git rm` de `2026-09-23-cronograma-import-y-versatilidad-vinculo.md` (§4.5).
- [ ] Descomponer `resumen-checklists.md` según §4.5.
- [ ] Índice de `01-planes/README.md`: activos, cerrados, en preparación y enlaces a los artifacts de evidencia huérfanos (§4.6).
- [ ] Aplicar §10.3 a los originales integrados: eliminar si está autorizado; si no, `git mv` a `06-material-de-apoyo/obsoleto/`.
- [ ] Revisión de fuentes de verdad de la Fase 7.

## Fase 8 — Navegación final y vistas derivadas

- [ ] Reescribir `docs/README.md` según §3.1 y quitar la sección "Migración en curso".
- [ ] Quitar de `AGENTS.md` y `README.md` las referencias a rutas inexistentes (§4.7). Solo es mecánico: los cambios de contenido van al Auditor.
- [ ] Alinear el artifact **Flujo SDD a Cierre** con §2.4, §2.6 y §3.2 (evidencia en su archivo propio, `<entorno>-worker-N`, los 18 pasos). Si no hay acceso al artifact, dejar el texto corregido en la evidencia y anotarlo como pendiente.
- [ ] Alinear el artifact **Recorrido del Plan** con las fases 0–9 de este plan y las 12 tareas migradas (más la eliminada).
- [ ] Ejecutar el comando de verificación de §4.7 y registrar el resultado en la evidencia.
- [ ] Revisión de fuentes de verdad de la Fase 8.

## Fase 9 — Consolidación y entrega del Worker

- [ ] Completar la evidencia: Punch List ejecutada con resultado por ítem.
- [ ] Consolidar hallazgos del progreso en §12, §13 y §14 de este plan.
- [ ] Anotar las propuestas normativas para el Auditor. Mínimo:
  - `AGENTS.md`: lectura mínima (§2.3), frases de inicio/cierre de sesión con rutas nuevas, excepción de consulta del Worker (§3.2) y plantillas nuevas en lugar de `plantilla-tarea.md`.
  - `docs/00-sistema` → estándar ya no existe como ruta.
- [ ] Último commit + push y entrega al Orquestador.

## Cierre del flujo (fuera del alcance del Worker)

1. **Auditor:** verificación de rama; SDD, plan, Punch List, evidencia y revisiones de fuentes de verdad por fase; criterios de §6. Informe en §15.
2. **Orquestador:** consolida y presenta a Victor.
3. **Gate 2.**
4. **Orquestador:** aplica los cambios normativos aprobados a `AGENTS.md`, `README.md` y `docs/README.md` y crea el Skill si se aprobó. No hay merge de código en este plan.
5. **Orquestador:** mensaje de cierre en §16 → commit + push a `main`.

---

# 6. Criterios de aceptación

- [ ] La raíz contiene solo `AGENTS.md`, `README.md`, `.gitignore` y `docs/`.
- [ ] `docs/` contiene solo `README.md` y las siete áreas numeradas.
- [ ] Cada fase registró su revisión de fuentes de verdad (actualización o "sin cambios requeridos").
- [ ] Cada carpeta operativa tiene un README breve y correcto, sin contradicciones con este plan.
- [ ] `00-estandar-agentes/` no nombra personas, repositorios, rutas ni datos de este proyecto.
- [ ] `01-contexto-repositorio/` contiene la configuración particular sin duplicar reglas universales.
- [ ] Las plantillas **vigentes** viven solo en `00-estandar-agentes/06-plantillas/`, y `02-plan.md` incluye las 3 secciones obligatorias.
- [ ] Ninguna fuente usa `work-1`/`work-2` como convención vigente.
- [ ] El diagrama (tabla y Mermaid) y el texto de `04-flujo-sdd-y-planes.md` describen los mismos 18 pasos con la misma nomenclatura de ramas.
- [ ] Cada plan activo nuevo tiene como máximo un plan, un progreso y una evidencia con el mismo nombre base; las tareas históricas son un único archivo.
- [ ] `planes-futuros.md` existe solo en `01-planes/`, y no hay progreso ni evidencia para planes futuros.
- [ ] `03-aprendizaje-continuo/` contiene las 11 mejoras, `historico.md` y `pendientes-de-promocion.md`, y su índice tiene una etiqueta correcta por archivo.
- [ ] Las reglas de negocio viven una sola vez en `04-flujos-de-negocio/`, sin nombres con espacios.
- [ ] `design.md` vive en `05-diseno-y-referencias/` y se referencia desde `01-contexto-repositorio/05-diseno-y-ui.md`.
- [ ] `06-material-de-apoyo/` contiene las 5 carpetas de §4.4 y su README las describe.
- [ ] El comando de §4.7 no devuelve rutas antiguas en documentos vigentes.
- [ ] Ningún archivo se eliminó sin autorización (§10.3).
- [ ] Los artifacts de evidencia huérfanos (§4.6) quedan enlazados.
- [ ] Los artifacts *Flujo SDD a Cierre* y *Recorrido del Plan* coinciden con este plan, o su corrección quedó registrada como pendiente con el texto listo.

---

# 6.1. Anexo — Decisiones de Victor ya resueltas (Fase 0)

1. **Plantillas:** las 9 plantillas separadas (§3.3) reemplazan a `plantilla-tarea.md`.
2. **Evidencia:** dos lugares coexisten — el artifact externo de claude.ai (checklist visual) y el archivo local en `02-trabajo-activo/03-evidencia/<tema>.md` (registro estructurado con enlace al artifact).
3. **Carpetas de apoyo de la raíz:** se mueven todas a `docs/06-material-de-apoyo/` ("no quiero carpetas sueltas, todas deben estar en su lugar").
4. **Tareas cerradas:** se mueven tal cual a `01-planes/` como un solo archivo histórico, sin re-descomponerlas. El formato de 3 archivos aplica a planes nuevos (para las abiertas, ver §4.5 y §10.2).
5. **`tareas-futuras.md` → `planes-futuros.md`**: mapeo directo.
6. **`resumen-checklists.md`**: no se conserva como archivo agregado; se descompone según §4.5.

---

# 7. Entorno de ejecución de este plan

| Campo | Valor |
|---|---|
| Repositorio | `pg_control_proyectos` (documentación; no hay código de app en este plan) |
| Rama | `main`, directo (§2.6 y AGENTS.md § Git y entrega). Sin worktree. |
| Requisito previo | Esta versión corregida (v2) debe estar en `main` antes de asignar al Worker (§10.4). |
| Commits | Cada ~35% de la Punch List, solo con ítems completos; `git mv` y sus enlaces en el mismo commit. |
| Herramientas de verificación | `git status`, `git log`, `git mv`, `grep` (comando de §4.7). No hay lint, tests ni build verificados en este repo (AGENTS.md). |

---

# 8. Roles de este plan

| Rol | Quién | Estado |
|---|---|---|
| Orquestador | Sesión de coordinación de Victor | Asigna al Worker tras el Gate 1 |
| Planner | Sesión que corrigió este plan (v2, 2026-09-27) | Entregado para el Gate 1 |
| Worker | Por asignar (chat propio) | Pendiente del Gate 1 |
| Auditor | Por asignar (chat propio, distinto del Worker) | Pendiente de la entrega del Worker |

---

# 9. Punch List

Estados: `Sin verificar` / `Conforme` / `Observado` / `No aplica`. La evidencia de cada ítem va en el archivo de evidencia homónimo.

| ID | Fase | Ítem | Evidencia mínima | Estado |
|---|---|---|---|---|
| PL-01 | 2 | Plan movido a `01-planes/`; progreso y evidencia homónimos creados | `git log --follow` del plan; los 3 archivos existen | Sin verificar |
| PL-02 | 2 | READMEs de la Fase 1 sin contradicciones con el plan | Diff de los READMEs corregidos | Sin verificar |
| PL-03 | 3 | Diagrama movido a `04-flujo-sdd-y-planes.md` con los 18 pasos y nomenclatura única | `git log --follow`; `grep -n "work-N"` sin resultados | Sin verificar |
| PL-04 | 3 | `00-indice.md` con la tabla de lectura mínima por rol y paso | Archivo | Sin verificar |
| PL-05 | 3 | 4 MD restantes del estándar, agnósticos | `grep -nE "Victor\|pg_control\|py_control"` sin resultados en el estándar | Sin verificar |
| PL-06 | 3 | 9 plantillas; `02-plan` con las 3 secciones obligatorias; `06` con verificación de rama y `PROPONER SKILL` | Archivos | Sin verificar |
| PL-07 | 4 | 7 documentos de contexto; regla de los dos repos; pool real verificado o "por verificar" | Archivos + comando usado | Sin verificar |
| PL-08 | 5 | `planes-futuros.md` por `git mv` y en el formato de §2.5 | `git log --follow` | Sin verificar |
| PL-09 | 5 | 11 mejoras movidas; 6 promovidas integradas; `historico.md` y `pendientes-de-promocion.md` | Tabla de §4.5 con el resultado por archivo | Sin verificar |
| PL-10 | 5 | Índice etiquetado de aprendizaje corregido | Diff | Sin verificar |
| PL-11 | 6 | 21 flujos movidos, el 19 renombrado, enlaces actualizados en el mismo commit | `git show --stat` del commit | Sin verificar |
| PL-12 | 6 | `design.md` y 6 mockups movidos; README de diseño integrado | `git show --stat` | Sin verificar |
| PL-13 | 6 | 5 carpetas de apoyo movidas; README actualizado | `ls` de la raíz y de `06-material-de-apoyo/` | Sin verificar |
| PL-14 | 7 | 12 tareas movidas tal cual; tarea de cronograma eliminada y su referencia en la mejora reemplazada por texto | `git show --stat` (12 renombres sin cambios + 1 borrado) | Sin verificar |
| PL-15 | 7 | `resumen-checklists.md` descompuesto; entradas sin dueño listadas | Lista por entrada → destino | Sin verificar |
| PL-16 | 7 | Índice de `01-planes/` con los artifacts huérfanos enlazados | Archivo | Sin verificar |
| PL-17 | 7 | Originales integrados tratados según §10.3 | Lista de archivos: eliminado / movido a `obsoleto/` | Sin verificar |
| PL-18 | 8 | `docs/README.md` reescrito según §3.1 | Archivo | Sin verificar |
| PL-19 | 8 | Rutas inexistentes quitadas de `AGENTS.md` y `README.md` (solo mecánico) | Diff | Sin verificar |
| PL-20 | 8 | Artifacts *Flujo SDD* y *Recorrido* alineados o pendiente registrado | URL/versión o texto listo | Sin verificar |
| PL-21 | 8 | Comando de §4.7 sin rutas antiguas en documentos vigentes | Salida del comando | Sin verificar |
| PL-22 | 2–9 | Revisión de fuentes de verdad registrada en cada fase | Entradas en el progreso | Sin verificar |
| PL-23 | 9 | Hallazgos consolidados en §12–§14 y propuestas normativas anotadas para el Auditor | Secciones llenas | Sin verificar |
| PL-24 | 2–9 | Ningún archivo eliminado sin autorización | `git log --diff-filter=D` contra §10.3 | Sin verificar |

Puntos de commit sugeridos (~35%): tras PL-06, tras PL-13 y tras PL-24.

---

# 10. Gate 1 — qué aprueba Victor

## 10.1. Excepción escrita para este plan

El objeto de este plan es construir el estándar y la navegación. Por eso, **con el Gate 1**, el Worker queda autorizado a:

- crear los archivos de `00-estandar-agentes/` y `01-contexto-repositorio/` definidos en §3;
- reescribir `docs/README.md` según §3.1;
- actualizar **solo rutas y enlaces** en `AGENTS.md` y `README.md`.

**Cualquier cambio de contenido normativo** en `AGENTS.md`, `README.md` o `docs/README.md` que no esté descrito en §3 lo propone el Auditor y lo aplica el Orquestador tras el Gate 2.

## 10.2. Decisiones resueltas con el diagrama y los artifacts (confirmar)

| # | Decisión | Fuente | ¿Confirma Victor? |
|---|---|---|---|
| D1 | **El diagrama es la fuente normativa del flujo**; el plan y los artifacts se ajustan a él (si no cubre un punto, aplica el plan) | Victor, Gate 1 (cambió la propuesta original: "manda el plan") | [x] |
| D2 | Rama de Worker: `<entorno>-worker-N`; `work-N` queda obsoleto | Tabla del diagrama, *Flujo SDD*, corrección del 2026-09-23 | [x] |
| D3 | Los worktrees viven en el repo de la app, en una subcarpeta con el nombre de la rama | Diagrama (Worker implementa en `py_control_proyectos_web`) | [x] |
| D4 | El plan embebe Spec, Punch List, auditoría y cierre; progreso y evidencia van aparte | Diagrama (el Auditor lee plan + progreso + evidencia), decisión 2, READMEs de la Fase 1 | [x] |
| D5 | El Gate 1 autoriza toda la implementación, incluidos los commits del Worker; sin aprobaciones intermedias | *Flujo SDD* | [x] |
| D6 | El Worker consulta a Victor **en el propio chat del Worker** ante un conflicto de negocio no anticipado, y registra pregunta y respuesta en el progreso | *Flujo SDD* (contradice el "punto único de contacto" de AGENTS.md → propuesta de ajuste al Auditor) | [x] |
| D7 | Después del Gate 2: merge, fuentes de verdad y Skill son independientes; el mensaje de cierre va al final | Diagrama + *Flujo SDD* | [x] |
| D8 | El handoff se escribe como sección fechada al final del progreso | Propuesta del Planner (no había destino) | [x] |
| D9 | La tarea abierta `paquetes-de-trabajo` se mueve tal cual; progreso y evidencia se crean al retomarla. `cronograma-import` **se elimina** (Victor, Gate 1) | Propuesta del Planner (decisión 4 no lo cubría) | [x] |
| D10 | **Orquestador, Planner y Auditor leen todos los flujos de negocio; el Worker solo los que toca su parte** | Victor, Gate 1 (cambió la propuesta original: lectura mínima para todos) | [x] |

## 10.3. Autorizaciones de eliminación solicitadas

Sin autorización, cada original se mueve con `git mv` a `docs/06-material-de-apoyo/obsoleto/`: no se pierde nada, pero queda un duplicado.

- [x] **A — Eliminar (`git rm`) los originales cuyo contenido ya se integró en otro archivo:** los 3 de `docs/00-sistema/`, `docs/Flujos de trabajo/README.md`, `docs/visual-companion/README.md`, `plantilla-tarea.md` y `resumen-checklists.md`.

## 10.4. Checklist del Gate 1

- [x] Victor aprueba el plan corregido (v2), la Punch List (§9) y las tablas de §4 (2026-09-27), con la excepción de la tarea de cronograma, que se elimina.
- [x] Victor confirma D3, D8 y D9 (D9 ajustada: cronograma se elimina).
- [x] Victor confirma D1, D2, D4, D5, D6, D7 y D10, presentadas una por una (D1 y D10 con cambios).
- [x] Victor autoriza A (§10.3).
- [x] La v2 está en `main` (commit `421c6bc`).
- [ ] El Orquestador asigna el Worker con el prompt de §17.

---

# 11. Registro de decisiones

| Fecha | Decisión / suceso | Quién |
|---|---|---|
| 2026-09-27 | Plan v1 creado (commit `c4102ff`) | Agente anterior |
| 2026-09-27 | Fases 0 y 1 ejecutadas y pusheadas (`404ddb3`, `be53526`) **sin Gate 1**, con el plan en estado "Propuesto" | Agente anterior |
| 2026-09-27 | Revisión del plan: contradicciones entre el plan, el diagrama y los artifacts (ramas, evidencia, secciones obligatorias, 6 tareas sin clasificar, enlaces sin inventariar, estándar no agnóstico, worktrees en el repo equivocado) | Sesión de revisión |
| 2026-09-27 | Victor ordena corregir el plan de punta a punta según los artifacts y el diagrama, y que lo implemente un Worker, no la sesión que corrige | Victor |
| 2026-09-27 | Plan v2: decisiones D1–D10 (§10.2) pendientes de confirmar en el Gate 1 | Planner (sesión de corrección) |
| 2026-09-27 | **Gate 1 parcial**: plan v2, Punch List, tablas de §4, D3, D8, D9 y autorización A. Excepción: `2026-09-23-cronograma-import-y-versatilidad-vinculo.md` se elimina en lugar de migrarse. D1, D2, D4–D7 y D10 quedan pendientes de su confirmación | Victor |
| 2026-09-27 | Corrección: el Planner había registrado D1–D10 como confirmadas cuando Victor solo vio D3, D8 y D9. Se corrigió el registro | Planner (sesión de corrección) |
| 2026-09-27 | **Gate 1 completo.** Victor responde las 7 pendientes: D2, D4, D5 y D7 como se propusieron; **D1: manda el diagrama** (no el plan); **D6: el Worker consulta en su propio chat**; **D10: Orquestador, Planner y Auditor leen todos los flujos, el Worker solo los suyos** | Victor |
| 2026-09-27 | Worker asignado ejecuta Fases 2–3. Hallazgo de entorno (verificado con `git branch --show-current` y `git log` de `origin/main`, no asumido): el harness de esta sesión exige commitear en una rama designada (`claude/reestructuracion-documental-pg-control-jvj5mf`) y prohíbe pushear a otra sin permiso; `origin/main` tiene historia propia de otras sesiones concurrentes, no relacionada con este plan. Se pushea a la rama designada en vez de a `main` directo (contradice §2.6/§7 del plan, que asumían push directo a `main`). Detalle completo en el progreso. Queda para el Auditor/Orquestador decidir cómo se lleva el resultado a `main` real | Worker |

---

# 12. Mejoras (de trabajo)

- **Un plan "Propuesto" no se ejecuta.** El agente anterior ejecutó las Fases 0 y 1 sin Gate 1. Aprendizaje: antes de ejecutar cualquier fase, el agente verifica en el encabezado que el estado diga "Aprobado (Gate 1)". Si no lo dice, se detiene. Candidato a `03-aprendizaje-continuo/` (etiqueta `roles/orquestador`); lo registra el Worker en la Fase 5.
- **Las vistas derivadas divergen si no hay una fuente normativa declarada.** El diagrama y los artifacts se editaron en paralelo al plan y terminaron contradiciéndose. Aprendizaje: todo artifact o diagrama declara de qué documento deriva, y ese documento manda.

# 13. Reglas de negocio acordadas en esta tarea

- Ninguna. Este plan no toca reglas de negocio del sistema, solo organización documental y método de trabajo.

# 14. Carpetas/archivos huérfanos

Se reportan a Victor. No se borra nada por cuenta propia.

- Artifacts de evidencia sin enlace desde el repo: Sub-lote 2 Checklist, Dashboards y Curva S Fase 3, Matriz de Accesos (§4.6).
- `2026-09-23-paquetes-de-trabajo.md` tiene texto con codificación dañada (UTF-8 doblemente codificado). Se reporta; no se corrige en este plan.
- `.vscode/extensions.json` en la raíz: carpeta no contemplada en ninguna tabla de §4 ni en el criterio de aceptación de §6 ("la raíz contiene solo AGENTS.md, README.md, .gitignore y docs/"). No se mueve ni se borra por no estar autorizada explícitamente; se reporta a Victor para que decida si se conserva, se ignora vía `.gitignore` o se mueve a `06-material-de-apoyo/`.
- Rutas citadas en `AGENTS.md`/`README.md` que ya no existen: `Sistema hibrido/`, `plantillas/`, `RDTs movimiento de tierra.../`, `memoria.md`, `control_de_proyectos.txt`, `.cursor/rules/*`.
- `.worktrees/` figura en `convenciones-de-trabajo.md` como pool creado el 2026-09-23, pero no existe en este repo.
- Entradas de `resumen-checklists.md` sin plan dueño: las completa el Worker en la Fase 7.

---

# 15. Informe de Auditoría

_Pendiente. Lo escribe el Auditor con la plantilla `06-informe-auditoria.md` tras la entrega del Worker._

# 16. Mensaje de cierre

_Pendiente. Lo escribe el Orquestador tras el Gate 2 con la plantilla `09-cierre.md`._

---

# 17. Prompt de asignación al Worker (lo usa el Orquestador tras el Gate 1)

```text
Eres el Worker del plan de reestructuración documental de pg_control_proyectos.

Plan (fuente normativa):
2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md
(en la raíz; tu primera tarea, Fase 2, es moverlo a docs/02-trabajo-activo/01-planes/)

Antes de empezar:
1. Lee AGENTS.md y el plan completo. Verifica en el encabezado y en §10.4 que el Gate 1 esté aprobado. Si no lo está, detente y avisa.
2. Lee §10.2 y §10.3 para saber qué confirmó Victor y qué autorizó eliminar.
3. Trabaja en main de pg_control_proyectos. No crees ramas ni worktrees.

Ejecuta las Fases 2 a 9 en orden, siguiendo solo las tablas de §4:
- Sin aprobaciones intermedias: el Gate 1 ya autorizó todo lo que describe el plan.
- Lo que no esté en §4 no lo muevas: anótalo como hallazgo en el progreso.
- Cada git mv va en el mismo commit que la actualización de los enlaces que rompe.
- Commit + push a main cada ~35% de la Punch List (§9), solo con ítems completos y git add explícito.
- En AGENTS.md y README.md solo cambias rutas (§10.1). Todo cambio normativo lo anotas para el Auditor.
- No elimines nada que §10.3 no autorice.
- Al final de cada fase, registra en el progreso la revisión de fuentes de verdad (§2.8).
- Si surge un conflicto no previsto, consulta a Victor y registra pregunta y respuesta en el progreso.

Entrega (Fase 9): Punch List con evidencia, hallazgos consolidados en §12–§14 y propuestas normativas para el Auditor. No te autoauditas ni cierras el plan.
```
