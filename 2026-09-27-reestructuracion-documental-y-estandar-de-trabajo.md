# Plan de implementación — Reestructuración documental y estándar de trabajo

> **Estado:** Propuesto. No ejecutar hasta que Victor apruebe el plan completo.
>
> **Propósito:** reorganizar la documentación del repositorio para separar de forma explícita:
>
> 1. El estándar reusable de trabajo de agentes.
> 2. El contexto específico de `pg_control_proyectos`.
> 3. Los planes, su progreso y su evidencia.
> 4. El aprendizaje continuo que nace de los planes.
> 5. Los flujos de negocio, diseño y material de apoyo.
>
> **Regla central:** no se elimina ningún archivo sin autorización explícita de Victor. Todo movimiento o renombre se realiza con `git mv`, después de un inventario, una propuesta origen → destino y aprobación.

---

# 1. Resultado esperado

Al terminar, la estructura activa de documentación será:

```text
pg_control_proyectos/
├── AGENTS.md
├── README.md
├── .gitignore
├── .worktrees/
│   ├── work-1/
│   └── work-2/
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

La estructura no crea carpetas por cada plan, progreso ni evidencia. Cada plan, progreso o evidencia es un único archivo Markdown con el mismo nombre base.

---

# 2. Convenciones globales

## 2.1. Numeración de carpetas y archivos

Los prefijos numéricos tienen un propósito de orden y lectura, no representan prioridad absoluta ni fecha.

```text
00 = estándar y punto de partida.
01 = contexto particular del repositorio.
02 = trabajo operativo activo.
03 = aprendizaje que nace del trabajo.
04 = reglas y flujos de negocio.
05 = diseño y referencias visuales.
06 = material de apoyo no normativo.
```

Dentro de una carpeta, la numeración define el orden recomendado de lectura. Ejemplo:

```text
00-indice.md
01-principios-y-seguridad.md
02-roles-y-delegacion.md
```

Los documentos de trabajo real usan fecha ISO:

```text
YYYY-MM-DD-<slug-descriptivo>.md
```

Ejemplo:

```text
2026-09-27-reestructuracion-documental.md
```

## 2.2. Convención de README

Cada carpeta operativa debe tener un `README.md` corto. Un README responde únicamente:

1. Qué vive en la carpeta.
2. Qué no vive en la carpeta.
3. Qué documento se debe leer después.
4. Qué regla de nombre o ciclo de vida aplica.

El README no duplica el contenido completo de todos sus archivos hijos.

## 2.3. Convención de lectura progresiva

Un agente no lee toda la documentación por defecto.

```text
1. Lee AGENTS.md.
2. Lee README.md de la raíz si necesita visión general.
3. Lee docs/README.md para ubicarse dentro de docs/.
4. Lee el README de la carpeta aplicable.
5. Lee solo el MD indicado para el tipo de solicitud.
6. Lee únicamente los flujos de negocio y diseño afectados.
```

Esto evita saturar contexto, reduce tokens y evita que reglas irrelevantes oculten las importantes.

## 2.4. Convención de documentos únicos por plan

Un plan de trabajo real usa el mismo nombre base en tres ubicaciones:

```text
02-trabajo-activo/01-planes/YYYY-MM-DD-<tema>.md
02-trabajo-activo/02-progreso/YYYY-MM-DD-<tema>.md
02-trabajo-activo/03-evidencia/YYYY-MM-DD-<tema>.md
```

Significado:

```text
Plan      = intención aprobada: qué se hará y cómo se aceptará.
Progreso  = estado vivo: qué se ha hecho, qué falta y qué bloquea.
Evidencia = demostración: qué se verificó y con qué resultado.
```

No se crean carpetas por plan. No se duplican capturas, logs o resultados sin una referencia explícita.

## 2.5. Convención de planes futuros

`planes-futuros.md` es el último archivo fijo de `01-planes/`.

Solo se registra allí un pendiente cuando Victor decide explícitamente:

```text
“Esto no se hará dentro del plan actual; lo dejamos para después.”
```

Un elemento de `planes-futuros.md`:

- No es un plan aprobado.
- No tiene progreso.
- No tiene evidencia.
- No tiene Worker asignado.
- Debe pasar por Spec/SDD antes de convertirse en plan real.

Cuando Victor decida retomarlo:

```text
planes-futuros.md
→ Spec/SDD
→ plan aprobado
→ progreso y evidencia
```

El ítem se conserva como promovido con enlace al nuevo plan; no se borra sin trazabilidad.

## 2.6. Convención de `.worktrees/`

`.worktrees/` es una carpeta física dentro de la raíz del repositorio:

```text
pg_control_proyectos/.worktrees/work-1/
pg_control_proyectos/.worktrees/work-2/
```

Cada carpeta corresponde a un worktree Git y a una rama de trabajo persistente:

```text
.worktrees/work-1/ → rama work-1
.worktrees/work-2/ → rama work-2
```

Reglas:

- `.worktrees/` se excluye de Git mediante `.gitignore`.
- Solo se usa cuando haya Workers en paralelo.
- No se crea, borra, renombra o reasigna worktree sin autorización explícita de Victor.
- Los roles de coordinación trabajan en `main`, salvo autorización distinta.

## 2.7. Convención de fuentes de verdad

Las tres fuentes de verdad de operación son:

```text
AGENTS.md      → norma raíz para agentes.
README.md      → visión, arquitectura y cambios de alto nivel del sistema.
docs/README.md → navegación y operación documental dentro de docs/.
```

Los flujos de negocio son la fuente de verdad de las reglas funcionales de cada tema:

```text
docs/04-flujos-de-negocio/NN-*.md
```

Cuando un plan descubre una regla o cambio nuevo:

| Tipo de hallazgo | Destino aprobado |
| --- | --- |
| Regla funcional/de negocio | Flujo de negocio dueño de la regla |
| Cambio de arquitectura/visión | `README.md` raíz |
| Cambio de comportamiento de agentes | `AGENTS.md` o `00-estandar-agentes/` |
| Cambio específico de este repositorio | `01-contexto-repositorio/` |
| Diseño/UI | `05-diseno-y-referencias/design.md` |
| Procedimiento reusable | Propuesta en aprendizaje continuo; promoción posterior según política |
| Evidencia de una implementación | Archivo de evidencia del plan |
| Pendiente fuera de alcance | `planes-futuros.md`, solo con autorización explícita de Victor |

Ninguna actualización de fuente de verdad ocurre sin la autorización requerida por la política de seguridad.

### Revisión obligatoria de fuentes de verdad

Después de **cada sesión relevante, cada fase de plan, cada implementación y cada corrección aprobada**, el agente ejecuta esta revisión. No es opcional ni queda a criterio del agente:

1. Revisar si lo realizado creó, corrigió, aclaró o contradijo una regla documentada.
2. Clasificar el destino según la tabla de arriba.
3. Pedir autorización de Victor antes de modificar una fuente de verdad, cuando corresponda.
4. Registrar qué fuente se actualizó, qué sección, por qué y con qué evidencia.
5. Si nada aplica, registrar explícitamente: **"Fuentes de verdad revisadas: sin cambios requeridos."** — el silencio no cuenta como revisión hecha.

---

# 3. Estructura objetivo y contenido de cada carpeta

```text
docs/
├── README.md
├── 00-estandar-agentes/
├── 01-contexto-repositorio/
├── 02-trabajo-activo/
├── 03-aprendizaje-continuo/
├── 04-flujos-de-negocio/
├── 05-diseno-y-referencias/
└── 06-material-de-apoyo/
```

## 3.1. `docs/README.md`

### Propósito

Es el mapa de navegación de `docs/`. Indica qué carpeta usar según el tipo de información o solicitud.

### Debe contener

- Mapa breve de las siete áreas numeradas.
- Ruta de lectura progresiva.
- Diferencia entre conversación simple y trabajo mediante plan.
- Diferencia entre plan, progreso, evidencia y aprendizaje.
- Enlaces a los README de cada área.

### No debe contener

- Reglas detalladas de seguridad.
- Procedimientos completos de Git, Playwright o diseño.
- Reglas de negocio duplicadas.
- Estado de planes particulares.

---

## 3.2. `00-estandar-agentes/`

### Propósito

Contiene el estándar reusable de trabajo para agentes. Sus reglas deben poder aplicarse a otro repositorio sin depender de nombres, URLs, datos, cuentas o flujos específicos de este proyecto.

### Contenido esperado

```text
00-estandar-agentes/
├── README.md
├── 00-indice.md
├── 01-principios-y-seguridad.md
├── 02-roles-y-delegacion.md
├── 03-sesiones-contexto-y-handoff.md
├── 04-flujo-sdd-y-planes.md
├── 05-aprendizaje-continuo.md
└── 06-plantillas/
```

### `README.md`

- Indica que aquí vive el estándar reusable.
- Indica que las reglas específicas del repositorio van en `01-contexto-repositorio/`.
- Enlaza a `00-indice.md`.

### `00-indice.md`

- Define qué leer según el rol y tipo de solicitud:
  - chat normal;
  - análisis;
  - creación de Spec/SDD;
  - planificación;
  - Worker;
  - Auditoría;
  - cierre/handoff.
- No replica el contenido de las políticas; solo direcciona.
- Contiene la **tabla de lectura mínima por rol y paso**: qué archivo(s) debe abrir cada rol antes de cada paso del flujo SDD→Cierre, para que ningún agente lea documentación de más. Regla de fondo: índice barato primero (títulos/resúmenes de `04-flujos-de-negocio/` y de `03-aprendizaje-continuo/`), contenido completo solo de lo que el plan/tema activo indica que aplica.

### `01-principios-y-seguridad.md`

- Principio de no inventar hechos, reglas o herramientas.
- Protección de secretos.
- Acciones que requieren aprobación: borrar, renombrar, commit, push, merge, PR, ramas, worktrees, migraciones, despliegues, envío de comunicaciones y cambios externos.
- Regla de revisar contexto, alcance y diff.
- Regla de no declarar éxito sin evidencia.

### `02-roles-y-delegacion.md`

- Roles: Victor, Orquestador, Planner, Worker y Auditor.
- Responsabilidad, entradas, salidas y límites de cada rol.
- Cuándo dividir trabajo y cuándo usar un solo Worker.
- Regla de independencia: no paralelizar si se modifican los mismos archivos, migraciones, componentes base o recursos no aislados.
- Reglas de aprobación antes de delegar, crear infraestructura o cerrar.

### `03-sesiones-contexto-y-handoff.md`

- Un chat por tarea o etapa clara.
- Qué contexto mínimo inicia un chat.
- Cuándo usar compactación.
- Cómo cerrar un chat activo.
- Estructura obligatoria de handoff ante cambio de sesión, chat, LLM o entorno.
- Regla: una conversación histórica no se reutiliza como contexto activo de una tarea nueva.

### `04-flujo-sdd-y-planes.md`

- Diferencia entre chat normal y plan de implementación.
- Frases o condiciones de activación del Orquestador.
- Secuencia:

```text
Objetivo con Victor
→ Orquestador define entorno (local por defecto, o nube) y nomenclatura de ramas/worktrees
→ Spec/SDD (Orquestador + Victor)
→ GATE Spec — aprobación de Victor
→ Orquestador delega la tarea al Planner
→ Planner arma el plan y Punch List (un solo archivo; anticipa conflictos de negocio antes de implementar)
→ GATE 1 — aprobación de Victor (autoriza toda la implementación, sin pausas intermedias)
→ Workers implementan (rama <entorno>-worker-N; registran hallazgos en el plan/progreso en el momento)
→ pruebas/evidencia
→ Worker consolida y envía hallazgos (escribe directo lo operativo; deja anotado lo que toque una fuente de verdad central)
→ Auditor (confirma rama correcta con git log/git branch --contains; propone APLICAR AHORA / PROPONER A VICTOR / NO PROMOVER / PROPONER SKILL)
→ GATE 2 — aprobación de cierre de Victor
→ Merge <entorno>-worker-N → main + aplicación de cambios aprobados a fuentes de verdad centrales
→ mensaje de cierre del Orquestador, registrado en el propio archivo del plan
→ cierre autorizado (plan = 100% recién cuando todo está pusheado/mergeado)
```

- Regla: no hay implementación antes de aprobar SDD, plan y Punch List.
- Regla: el Orquestador nunca planifica ni implementa él mismo — siempre delega al Planner tras el Gate del Spec, salvo excepción escrita en el propio plan y autorizada por Victor.
- Regla de los dos repos: documentación de proceso (Spec, plan, progreso, evidencia, hallazgos, informe de auditoría, actualización de fuentes de verdad) se commitea y pushea siempre directo a `main` de este repo, sin rama ni merge. Código real de la app va siempre a la rama `<entorno>-worker-N`, nunca a `main`, hasta el merge autorizado en el Gate 2.

### `05-aprendizaje-continuo.md`

- Diferencia entre hallazgo, mejora de trabajo, regla de negocio, decisión pendiente, evidencia y procedimiento reusable.
- Remite explícitamente a la regla de **revisión obligatoria de fuentes de verdad** (§2.7): se ejecuta después de cada sesión relevante, fase de plan, implementación o corrección aprobada — no solo al cierre de un plan.
- Proceso de promoción:

```text
Hallazgo
→ registro de aprendizaje
→ clasificación
→ evidencia
→ revisión/auditoría
→ aprobación
→ actualización del destino correcto
```

- Regla: no todo aprendizaje se transforma en regla o procedimiento reusable.
- Regla: una experiencia aislada no se promueve sin evidencia y aprobación.
- Regla de escalación a Skill: cuando un procedimiento reusable **se repite** (no es la primera vez que aparece el mismo tipo de hallazgo), el Auditor puede proponer en su informe convertirlo en un Skill real de Claude Code (`.claude/skills/<nombre>/SKILL.md`), redactado de forma agnóstica (sin nombres, rutas ni datos de este repositorio en particular) para que sea copiable a otros repositorios. Requiere aprobación de Victor, igual que cualquier otra promoción.

### Índice de `03-aprendizaje-continuo/README.md`

No es solo una lista de archivos: cada mejora se lista con una **etiqueta corta** de categoría (ej. `playwright`, `migraciones-sql`, `git/ramas`, `sesiones/chat`, `worktrees/turbopack`, `lint`), para que cualquier rol escanee el índice barato y abra solo la mejora puntual que aplica a lo que está por hacer — nunca la carpeta completa por defecto.

---

## 3.3. `00-estandar-agentes/06-plantillas/`

### Propósito

Es la única ubicación de plantillas. No debe existir un archivo “plantillas.md” paralelo ni copias de plantillas en otras carpetas.

### Contenido esperado

```text
06-plantillas/
├── README.md
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

### `README.md`

- Índice de las plantillas.
- Qué documento real usa cada plantilla.
- Regla: copiar la plantilla aplicable y conservar sus secciones; proponer cambios al estándar si falta un apartado recurrente.

### `01-spec-sdd.md`

Plantilla para definir, junto con Victor, el problema antes de planificar.

Debe incluir:

- Estado.
- Problema y contexto.
- Resultado esperado.
- Alcance y no alcance.
- Usuarios/roles afectados.
- Reglas de negocio y documentos afectados.
- Datos, API, migraciones o dependencias afectadas.
- Diseño/UI aplicable.
- Riesgos y decisiones pendientes.
- Criterios de aceptación.
- Estrategia de prueba/evidencia.
- Aprobación de Victor.

### `02-plan.md`

Plantilla del único archivo Markdown de cada plan.

Debe incluir:

- Identificación y estado.
- Referencia al Spec/SDD aprobado.
- Objetivo, alcance y no alcance aprobados.
- Fases y dependencias.
- Asignación de roles, Workers, ramas y worktrees.
- Archivos/componentes potencialmente afectados.
- Punch List aprobada o referencia explícita a su sección.
- Riesgos y bloqueos.
- Registro de decisiones.
- Enlaces al archivo de progreso y evidencia homónimos.
- Sección de auditoría y cierre.
- Apartado de elementos postergados que serán propuestos para `planes-futuros.md` solo con decisión de Victor.

### `03-progreso.md`

Plantilla del archivo operativo vivo asociado a un plan.

Debe incluir:

- Referencia al plan homónimo.
- Estado general y fase actual.
- Tabla de roles/Workers y estado.
- Avances terminados.
- Trabajo actual.
- Pendientes.
- Commits, ramas y worktrees usados.
- Bloqueos, riesgos y decisiones requeridas.
- Próximo paso verificable.
- Última actualización, responsable y enlace a handoff si corresponde.

No contiene capturas o resultados extensos de pruebas: eso va en evidencia.

### `04-evidencia.md`

Plantilla del archivo de demostración verificable asociado a un plan.

Debe incluir:

- Referencia al plan homónimo.
- Entorno y fecha de prueba.
- Rol/usuario y datos autorizados de prueba, sin secretos.
- Tabla de Punch List ejecutada:
  - ítem;
  - esperado;
  - método;
  - observado;
  - estado;
  - evidencia/ruta/enlace;
  - responsable.
- Resultados de Playwright, pruebas técnicas, logs, consultas o cálculos.
- Regresiones verificadas.
- Limitaciones o casos no verificables.

No redefine alcance ni registra el avance narrativo: eso va en plan/progreso.

### `05-punch-list.md`

Plantilla del checklist que se incorpora o referencia desde un plan antes de implementar.

Debe incluir:

- Estado de aprobación de Victor.
- Ítems funcionales.
- Datos y cálculos.
- Permisos.
- UI/responsive/accesibilidad, si aplica.
- Estados vacío, carga y error, si aplica.
- Validación en servidor/API, si aplica.
- Regresión.
- Convención de estados: `Sin verificar`, `Conforme`, `Observado`, `No aplica`.
- Evidencia mínima requerida por ítem.

### `06-informe-auditoria.md`

Plantilla del informe del Auditor.

Debe incluir:

- Alcance auditado.
- Material revisado.
- Cumplimiento de SDD, plan, Punch List y evidencia.
- `APLICAR AHORA`.
- `PROPONER A VICTOR`.
- `NO PROMOVER`.
- `PROPONER SKILL` (procedimiento reusable que ya se repitió y amerita convertirse en un Skill de Claude Code agnóstico, copiable a otros repositorios).
- Pendientes técnicos y documentales.
- Recomendación: listo, bloqueado o requiere corrección.

### `07-handoff.md`

Plantilla de traspaso entre sesiones, chats, LLMs o personas.

Debe incluir:

- Objetivo y estado actual.
- Plan, progreso y evidencia relacionados.
- Rama, worktree y último commit.
- Trabajo terminado y no terminado.
- Pruebas ya ejecutadas.
- Bloqueos y riesgos.
- Archivos/documentos que debe leer el siguiente agente.
- Próximo paso concreto.

### `08-aprendizaje.md`

Plantilla de aprendizaje continuo.

Debe incluir:

- Origen: plan/sesión/evidencia.
- Observación o problema.
- Evidencia.
- Clasificación: mejora de trabajo, regla de negocio, decisión pendiente, contexto de repositorio o procedimiento reusable.
- Destino propuesto.
- Cambio propuesto.
- Estado: borrador, pendiente de aprobación, promovido, rechazado o reemplazado.
- Referencia a aprobación de Victor.

### `09-cierre.md`

Plantilla de cierre de plan.

Debe incluir:

- Alcance completado y no completado.
- Estado final de Punch List.
- Evidencia disponible.
- Auditoría y decisiones de Victor.
- Documentos promovidos.
- Aprendizajes registrados.
- Pendientes enviados a `planes-futuros.md`.
- Commit/push/merge realizados o pendientes.
- Autorización de cierre.

---

## 3.4. `01-contexto-repositorio/`

### Propósito

Contiene exclusivamente información aplicable a `pg_control_proyectos`. No contiene el estándar universal de agentes ni reglas de negocio duplicadas.

### Contenido esperado

```text
01-contexto-repositorio/
├── README.md
├── 00-indice.md
├── 01-proposito-y-alcance.md
├── 02-arquitectura-y-fuentes-de-verdad.md
├── 03-entorno-git-y-worktrees.md
├── 04-pruebas-y-evidencia.md
├── 05-diseno-y-ui.md
└── 06-mapa-documental.md
```

### `README.md`

- Indica que la carpeta contiene instrucciones específicas de este repositorio.
- Deriva a `00-indice.md`.

### `00-indice.md`

- Define qué documentos se leen según la tarea:
  - documentación;
  - Git/worktree;
  - pruebas;
  - UI;
  - flujos de negocio.
- No replica el contenido de cada documento.

### `01-proposito-y-alcance.md`

- Propósito del repositorio documental.
- Qué pertenece aquí y qué pertenece al repositorio de aplicación.
- Relación entre ambos repositorios.
- Límites de cambios y de validación disponibles.

### `02-arquitectura-y-fuentes-de-verdad.md`

- Tres fuentes de verdad: `AGENTS.md`, `README.md`, `docs/README.md`.
- Fuente dueña de cada regla de negocio: flujos numerados.
- Cómo se promueve un cambio desde un plan hacia una fuente de verdad.
- Regla de actualización de README raíz si cambia la visión/arquitectura.
- Regla de actualización de AGENTS si cambia el comportamiento requerido de agentes.

### `03-entorno-git-y-worktrees.md`

- Rama `main`.
- Pool real: `work-1`, `work-2`.
- Rutas reales de `.worktrees/`.
- Roles que pueden usar ramas de Worker.
- Política de commits aproximadamente cada 35% de Punch List acumulada, solo después de completar íntegramente el ítem en curso.
- Reglas de `git add` explícito, push, merge y autorización.

### `04-pruebas-y-evidencia.md`

- Uso del artefacto Punch List interactivo aprobado para el proyecto.
- Cuándo es obligatorio Playwright.
- Requisitos para capturas, pruebas con login y datos reales/autorizados.
- Cómo registrar evidencia en el MD homónimo del plan.
- Qué hacer si un caso no puede verificarse.

### `05-diseno-y-ui.md`

- Referencia obligatoria a `docs/05-diseno-y-referencias/design.md` cuando se modifica UI.
- Uso de mockups y nombres de pantallas.
- Reglas para no inventar componentes, comportamientos o diseño no documentado.

### `06-mapa-documental.md`

- Índice de los flujos de negocio existentes.
- Referencia a material de apoyo relevante.
- Mapa origen → destino de documentación migrada.
- Enlaces verificados a archivos clave.

---

## 3.5. `02-trabajo-activo/`

### Propósito

Contiene exclusivamente trabajo que está planificado, en ejecución o cerrado recientemente con su trazabilidad. No contiene reglas permanentes ni aprendizaje independiente.

### Contenido esperado

```text
02-trabajo-activo/
├── README.md
├── 01-planes/
│   ├── README.md
│   ├── YYYY-MM-DD-<tema>.md
│   └── planes-futuros.md
├── 02-progreso/
│   ├── README.md
│   └── YYYY-MM-DD-<tema>.md
└── 03-evidencia/
    ├── README.md
    └── YYYY-MM-DD-<tema>.md
```

### `README.md`

- Define plan, progreso y evidencia.
- Define relación uno-a-uno por nombre base.
- Aclara que no se crean carpetas por plan.

### `01-planes/README.md`

- Índice de planes activos, cerrados y en preparación.
- Convención de nombre por fecha.
- Regla: un plan es un único MD basado en `02-plan.md`.

### `01-planes/YYYY-MM-DD-<tema>.md`

- Es el plan completo de una implementación.
- Contiene SDD, plan, Punch List, roles, decisiones, auditoría y cierre según las plantillas aplicables.
- No se crea hasta que Victor decida que se realizará trabajo mediante plan, no solo conversación.

### `01-planes/planes-futuros.md`

- Último archivo fijo de la carpeta.
- Cola de pendientes que Victor decidió postergar explícitamente.
- Cada ítem registra origen, descripción, motivo, estado y si requiere Spec/SDD.
- No contiene plan aprobado, progreso, evidencia ni Worker.
- Un ítem se promueve a plan solo después de Spec/SDD y aprobación.

### `02-progreso/README.md`

- Explica que esta carpeta tiene un MD vivo por plan iniciado.
- Un archivo se crea al iniciar ejecución aprobada, no al registrar un futuro plan.

### `02-progreso/YYYY-MM-DD-<tema>.md`

- Estado operativo del plan homónimo.
- Se basa en `03-progreso.md`.
- Registra cambios reales durante la implementación.

### `03-evidencia/README.md`

- Explica que evidencia es prueba objetiva y no bitácora de avance.
- Un archivo se crea al iniciar ejecución aprobada, no para planes futuros.

### `03-evidencia/YYYY-MM-DD-<tema>.md`

- Demostración verificable del plan homónimo.
- Se basa en `04-evidencia.md`.
- Contiene estado final de Punch List, Playwright, pruebas y evidencias.

---

## 3.6. `03-aprendizaje-continuo/`

### Propósito

Contiene aprendizajes que nacen de la ejecución de planes y que requieren evaluación antes de alterar reglas, contexto, procedimientos o fuentes de verdad.

### Contenido esperado

```text
03-aprendizaje-continuo/
├── README.md
├── YYYY-MM-DD-<aprendizaje>.md
├── pendientes-de-promocion.md
└── historico.md
```

### `README.md`

- Define qué es aprendizaje continuo.
- Aclara que no contiene planes futuros ni tareas operativas completas.
- Indica que cada aprendizaje debe tener origen, evidencia y destino propuesto.

### `YYYY-MM-DD-<aprendizaje>.md`

- Un aprendizaje concreto basado en `08-aprendizaje.md`.
- Nace de una tarea, una sesión o evidencia real.
- No se crea para ideas hipotéticas sin origen.

### `pendientes-de-promocion.md`

- Lista consolidada de aprendizajes y decisiones pendientes de aprobación.
- No reemplaza los archivos individuales de aprendizaje; solo facilita revisión.

### `historico.md`

- Registro de aprendizajes promovidos, rechazados, reemplazados o cerrados.
- Incluye destino final y fecha de decisión.

---

## 3.7. `04-flujos-de-negocio/`

### Propósito

Contiene las reglas funcionales y operativas permanentes del sistema, una vez por tema dueño.

### Contenido esperado

```text
04-flujos-de-negocio/
├── README.md
├── 01-interfaz.md
├── 02-usuarios.md
├── ...
└── 20-plan-maestro.md
```

### `README.md`

- Índice de los flujos.
- Regla de lectura: leer solo los flujos afectados más los obligatorios definidos por el repositorio.
- Regla de actualización: una regla se escribe una vez en su flujo dueño; otros documentos enlazan, no copian.

### `NN-<tema>.md`

- Define funcionamiento de negocio, datos, reglas, estados, roles y restricciones de ese flujo.
- Se actualiza solo cuando una decisión de negocio fue validada y aprobada.
- No contiene bitácoras de sesión, estados de plan o procedimientos de agentes.

---

## 3.8. `05-diseno-y-referencias/`

### Propósito

Contiene el sistema visual y referencias de interfaz, separado de reglas de negocio y del estándar de agentes.

### Contenido esperado

```text
05-diseno-y-referencias/
├── README.md
├── design.md
└── mockups/
```

### `README.md`

- Indica cuándo `design.md` es lectura obligatoria.
- Aclara qué tipos de referencias pueden vivir en `mockups/`.

### `design.md`

- Sistema de diseño: layout, espaciado, tokens, componentes, tablas, responsive y accesibilidad.
- Fuente de verdad visual para cambios de interfaz.

### `mockups/`

- Contiene mockups HTML, capturas de referencia o archivos visuales.
- No contiene evidencia de pruebas de un plan; esa evidencia queda en `02-trabajo-activo/03-evidencia/`.

---

## 3.9. `06-material-de-apoyo/`

### Propósito

Centraliza material de referencia que se conserva pero no es fuente de verdad ni parte del flujo activo.

### Contenido inicial

```text
06-material-de-apoyo/
└── README.md
```

### `README.md`

Debe indicar que la carpeta comienza vacía y que aquí se guardará material de apoyo del repositorio que no sea:

- fuente de verdad;
- estándar de agentes;
- contexto de repositorio;
- plan, progreso o evidencia;
- aprendizaje continuo;
- flujo de negocio;
- sistema de diseño.

Debe indicar que el contenido y el README se actualizarán cada vez que se agregue, mueva, reclasifique o retire material de apoyo.

---

# 4. Migración de la estructura actual

## 4.1. Archivos actuales de `docs/00-sistema/`

| Archivo actual | Destino propuesto | Acción |
| --- | --- | --- |
| `roles-y-flujo.md` | `00-estandar-agentes/02-roles-y-delegacion.md` y `04-flujo-sdd-y-planes.md` | Revisar y dividir solo si el contenido mezcla roles y ciclo de planes |
| `gestion-de-sesiones-y-contexto.md` | `00-estandar-agentes/03-sesiones-contexto-y-handoff.md` | Eliminar primero la duplicación literal; luego migrar | 
| `convenciones-de-trabajo.md` | `01-contexto-repositorio/03-entorno-git-y-worktrees.md` | Mover reglas reales de este repositorio; dejar reglas universales en estándar |

## 4.2. Carpetas actuales

| Carpeta actual | Destino propuesto | Regla |
| --- | --- | --- |
| `docs/Flujos de trabajo/` | `docs/04-flujos-de-negocio/` | Mover con `git mv`, no cambiar contenido en la misma fase salvo enlaces necesarios |
| `docs/visual-companion/` | `docs/05-diseno-y-referencias/` | Mover con `git mv`; conservar `design.md` y mockups |
| `docs/Tareas de implementacion/` | Clasificar: planes reales a `02-trabajo-activo/01-planes/`; archivos de estado/evidencia según corresponda | No mover sin tabla de clasificación aprobada |
| `docs/Mejoras continuas/` | `docs/03-aprendizaje-continuo/` | Clasificar archivos: aprendizaje real, histórico o plan mal ubicado |
| Carpetas de apoyo en raíz | `docs/06-material-de-apoyo/` | Inventariar, clasificar y mover con aprobación; no borrar |

---

# 5. Fases de implementación

## Fase 0 — Diagnóstico y propuesta de migración

- [ ] Leer `AGENTS.md`, `README.md`, `docs/README.md` y los tres MD actuales de `docs/00-sistema/`.
- [ ] Ejecutar inventario de carpetas/archivos actuales.
- [ ] Identificar enlaces internos y referencias a rutas antiguas.
- [ ] Crear una tabla origen → destino para cada archivo/carpeta que se moverá.
- [ ] Clasificar los archivos actuales de Tareas/Mejoras.
- [ ] Presentar informe de impacto a Victor.

**No crear, mover, renombrar, borrar, commitear ni pushear antes de aprobación explícita.**

## Fase 1 — Crear estructura vacía y navegación

- [ ] Crear las siete carpetas numeradas dentro de `docs/`.
- [ ] Crear únicamente los README de cada carpeta y subcarpeta definida.
- [ ] Crear `docs/README.md` o reescribirlo para que enlace a la nueva estructura.
- [ ] Presentar estructura y READMEs a Victor.

## Fase 2 — Crear estándar y plantillas

- [ ] Crear los cinco MD de `00-estandar-agentes/`.
- [ ] Crear las nueve plantillas dentro de `06-plantillas/`.
- [ ] Verificar que no haya plantillas duplicadas fuera de esa carpeta.
- [ ] Presentar estándar y plantillas a Victor.

## Fase 3 — Crear contexto del repositorio

- [ ] Crear los seis documentos de `01-contexto-repositorio/`.
- [ ] Incluir la configuración confirmada: `main`, `work-1`, `work-2`, `.worktrees/`, commits al 35%, Punch List, Playwright y `design.md`.
- [ ] Presentar contexto específico a Victor.

## Fase 4 — Preparar trabajo activo y aprendizaje

- [ ] Crear READMEs de `02-trabajo-activo/` y sus subcarpetas.
- [ ] Crear `planes-futuros.md` usando la convención definida.
- [ ] Crear README, `pendientes-de-promocion.md` e `historico.md` de aprendizaje continuo.
- [ ] No crear planes, progreso, evidencia ni aprendizajes ficticios.
- [ ] Presentar archivos a Victor.

## Fase 5 — Migrar flujos, diseño y material de apoyo

- [ ] Ejecutar los `git mv` aprobados para flujos de negocio y diseño/referencias.
- [ ] Actualizar enlaces estrictamente necesarios tras cada movimiento.
- [ ] Inventariar material de apoyo; mover solo lo aprobado a `06-material-de-apoyo/`.
- [ ] Verificar que no haya rutas rotas.
- [ ] Presentar resultado de migración a Victor.

## Fase 6 — Clasificar trabajo histórico

- [ ] Clasificar archivos de las carpetas antiguas de tareas y mejoras.
- [ ] Proponer destino de cada archivo en una tabla.
- [ ] Esperar aprobación de Victor.
- [ ] Mover con `git mv` los archivos aprobados.
- [ ] Registrar cualquier archivo que deba permanecer como histórico.

## Fase 7 — Actualizar fuentes de verdad

- [ ] Actualizar `docs/README.md` como mapa de la estructura final.
- [ ] Actualizar README raíz si cambia la visión/arquitectura de alto nivel.
- [ ] Actualizar `AGENTS.md` para que derive a las rutas nuevas y diferencie chat normal de plan con Orquestador.
- [ ] Revisar que los tres no se contradigan.

## Fase 8 — Auditoría y cierre

- [ ] Revisar estructura real versus esta especificación.
- [ ] Verificar enlaces Markdown y rutas.
- [ ] Verificar que no se hayan eliminado archivos sin autorización.
- [ ] Verificar que cada sesión/fase/implementación/corrección relevante de este plan tenga registrada su revisión de fuentes de verdad (actualización hecha, o "sin cambios requeridos" explícito).
- [ ] Verificar que `planes-futuros.md` esté solo en `01-planes/`.
- [ ] Verificar que no existan archivos de progreso/evidencia para planes futuros no iniciados.
- [ ] Verificar que las plantillas existan solo en `00-estandar-agentes/06-plantillas/`.
- [ ] Verificar que los MD de estándares no contengan configuraciones específicas de repositorio.
- [ ] Presentar informe final, diff y propuesta de commit/push a Victor.
- [ ] Solicitar autorización explícita antes de commit/push.

---

# 6. Criterios de aceptación

- [ ] La estructura final tiene solo las siete áreas numeradas dentro de `docs/`.
- [ ] Cada sesión relevante, fase de plan, implementación o corrección aprobada de este plan registró su revisión de fuentes de verdad, con destino clasificado o "sin cambios requeridos".
- [ ] Cada carpeta operativa tiene un README breve y correcto.
- [ ] `00-estandar-agentes/` no contiene detalles de negocio ni rutas específicas del repositorio.
- [ ] `01-contexto-repositorio/` contiene configuración particular sin duplicar reglas universales.
- [ ] Todas las plantillas viven exclusivamente en `00-estandar-agentes/06-plantillas/`.
- [ ] Cada plan activo tiene, como máximo, un plan, un progreso y una evidencia con el mismo nombre base.
- [ ] Los planes futuros se registran solo en `01-planes/planes-futuros.md`.
- [ ] `03-aprendizaje-continuo/` no contiene planes futuros ni tareas operativas completas.
- [ ] Las reglas de negocio viven una sola vez en `04-flujos-de-negocio/`.
- [ ] `design.md` vive en `05-diseno-y-referencias/` y se referencia desde contexto/UI.
- [ ] `06-material-de-apoyo/` inicia solo con su README y se mantiene actualizado al cambiar su contenido.
- [ ] No quedan enlaces internos rotos por la migración.
- [ ] `AGENTS.md`, README raíz y `docs/README.md` están alineados.

---

# 7. Prompt de inicio para ejecutar este plan

```text
Vamos a implementar el plan de reestructuración documental.

Archivo de plan:
docs/02-trabajo-activo/01-planes/2026-09-27-reestructuracion-documental-y-estandar-de-trabajo.md

Empieza por Fase 0 — Diagnóstico y propuesta de migración.

Lee primero AGENTS.md, README.md, docs/README.md y los documentos actuales de docs/00-sistema/.

No crees, muevas, renombres, borres, commitees, pushees, hagas merge, abras PR, crees ramas ni worktrees antes de entregar:

1. Inventario de la estructura actual.
2. Tabla origen → destino propuesta.
3. Lista de enlaces/rutas que podrían romperse.
4. Lista de decisiones pendientes.

Espera mi aprobación explícita antes de continuar a la Fase 1.
```
