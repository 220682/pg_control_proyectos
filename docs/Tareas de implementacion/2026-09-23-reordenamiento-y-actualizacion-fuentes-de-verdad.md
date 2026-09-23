# Reordenamiento y actualización de fuentes de verdad

> **Estado:** EJECUTADO — Fases 0 a 8 completadas y commiteadas el 2026-09-23 (commit `6c26fde`, pusheado a `origin/main`). Pendiente no bloqueante: confirmar si `design.md` recibió la regla visual del primer gráfico de líneas (Curva S) — ver decisión #12 de la tarea `2026-09-21-curva-s-fase-3-agente-d.md`.
>
> **Objetivo:** alinear la estructura física del repositorio con las fuentes de verdad (`AGENTS.md`, `README.md` raíz, `docs/README.md`), integrar la política de Orquestador/sesiones/worktrees, y establecer el ciclo de mejora continua donde cada aprendizaje se traslade a las fuentes de verdad correspondientes.
>
> **Resultado esperado:** un repositorio donde:
> - La estructura de carpetas coincida con lo que dice `docs/README.md`.
> - `README.md` (raíz) refleje la visión actual del sistema.
> - `AGENTS.md` integre el flujo de Orquestador con las frases de inicio/cierre de sesión.
> - `docs/00-sistema/` contenga las políticas operativas.
> - `docs/Tareas de implementacion/` y `docs/Mejoras continuas/` estén claramente separados.
> - Cada aprendizaje nuevo se traslade a las fuentes de verdad con autorización de Victor.

---

## Restricciones globales

- No borrar archivos sin aprobación explícita de Victor.
- No hacer commit, push, merge, PR, creación de rama o worktree sin autorización.
- No imprimir ni guardar secretos, tokens, contraseñas, cadenas de conexión ni archivos `.env`.
- Mantener una única fuente de verdad por concepto; no duplicar reglas entre archivos.
- Los cambios de documentación se hacen en `main` del repositorio documental, respetando `AGENTS.md`.
- Al usar `git add`, agregar archivos de forma explícita; no usar `git add .`.
- Registrar toda decisión nueva de Victor en el `## Registro de decisiones` de esta tarea.

---

## Distinción clave: Tareas de implementación vs Mejoras continuas

> Agregado el 2026-09-23 a pedido de Victor, para que el criterio sea explícito antes de clasificar o mover nada.

- **Tarea de implementación** = lo que hacen los Workers: trabajo operativo de construcción (código, pantallas, consultas, migraciones, etc.). Vive en `docs/Tareas de implementacion/`. Cada tarea registra **qué se implementó**, pero no es el lugar donde queda la regla permanente.
- **Mejora continua** = un aprendizaje, regla o buena práctica que nace de realizar una tarea y se traslada a una fuente de verdad (`Flujos de trabajo/NN-*.md`, `README.md`, `AGENTS.md`, `docs/00-sistema/*.md`). Vive en `docs/Mejoras continuas/`. Cada mejora debe indicar **de qué tarea nació** y **a qué fuente de verdad se trasladó**.

Ejemplos:
- "Se implementó el endpoint de importación de DP" → tarea de implementación.
- "Se descubrió que el parser debe validar WBS duplicado antes de extraer datos, y esa regla se agregó a `09-importar-dp.md`" → mejora continua.

**Nota — tensión detectada:** bajo este criterio estricto, los 9 lotes actuales de `docs/Mejoras continuas/` (PR Fase 1/2, Dashboard Fase 3, Curva S Fase 3, EVM Fase 0/1, etc.) documentan principalmente **trabajo de implementación** (código, migraciones, pantallas construidas), con una sección final `## Mejoras a flujos` reservada para los aprendizajes trasladables. Falta decidir con Victor si son documentos híbridos válidos tal como están, o si de aquí en adelante deben separarse en tarea de implementación (en `Tareas de implementacion/`) + mejora continua (en `Mejoras continuas/`, solo la regla trasladada). Ver Fase 3 abajo — no se mueve nada todavía.

---

## Registro de decisiones

> Registrar aquí, en el momento, toda respuesta de Victor, decisión del Orquestador, cambio de convención o hallazgo relevante. Al cerrar, trasladar cada decisión aprobada al documento permanente correspondiente.

| # | Fecha | Decisión / aprendizaje | Origen | Destino | Estado |
| --- | --- | --- | --- | --- | --- |
| 1 | 2026-09-23 | `README.md` (raíz) se actualiza solo cuando hay cambios que alteran contenido ya existente en ese archivo — no en cada sesión | Victor | `README.md` | Resuelto |
| 2 | 2026-09-23 | Actualizar `README.md` (raíz) con lo que ya está implementado; lo que está por implementarse se deja marcado explícitamente como pendiente, no como hecho | Victor | `README.md` | Resuelto |
| 3 | 2026-09-23 | `AGENTS.md` sí integra explícitamente el flujo de Orquestador | Victor | `AGENTS.md` | Resuelto |
| 4 | 2026-09-23 | Renombrar `docs/Flujos de trabajo/01-interfaz sera cambiado a configuracion.md` a `01-configuracion.md` (corrige el enlace roto en `AGENTS.md`); el contenido del flujo en sí queda marcado como pendiente de implementar/definir, no se reescribe ahora | Victor | `docs/Flujos de trabajo/01-configuracion.md`, `AGENTS.md` | Aprobado |
| 5 | 2026-09-23 | Agregar el flujo 21 (`21-curva-s.md`) a la lista de "Flujos principales" de `AGENTS.md` — es nuevo, faltaba | Victor | `AGENTS.md` | Aprobado |
| 6 | 2026-09-23 | Distinción explícita: Tarea de implementación (trabajo de Workers: código/UI/queries/migraciones, vive en `Tareas de implementacion/`) vs Mejora continua (aprendizaje/regla trasladado a una fuente de verdad, vive en `Mejoras continuas/`). Agregada como sección central del plan | Victor | `docs/README.md`, `AGENTS.md`, re-evaluación de `Mejoras continuas/` | Aplicado (ver filas siguientes) |
| 7 | 2026-09-23 | Victor elige opción B: separar. Movidos los 9 lotes completos de `Mejoras continuas/` a `Tareas de implementacion/`. De esos, 5 tenían contenido en `## Mejoras a flujos` (sub-lote-2, pr-fase-1, pr-fase-2, curva-s-fase-3, dashboard-fase-3) y se extrajo a un archivo nuevo homónimo en `Mejoras continuas/`. Los otros 4 tenían la sección vacía, no queda nada de ellos en `Mejoras continuas/` | Victor | `docs/Tareas de implementacion/*`, `docs/Mejoras continuas/*` | Aplicado y ejecutado |
| 8 | 2026-09-23 | `mejoras-futuras.md` renombrado a `tareas-futuras.md` y movido de `Mejoras continuas/` a `Tareas de implementacion/` — es backlog de tareas pospuestas (implementación), no de aprendizajes. Corregidas todas las referencias cruzadas (`docs/README.md`, `docs/Flujos de trabajo/14-accesos-y-restricciones.md`, y las 4 tareas movidas que lo mencionaban) | Victor | `docs/Tareas de implementacion/tareas-futuras.md` | Aplicado y ejecutado |
| 9 | 2026-09-23 | `docs/README.md` reescrito para reflejar la distinción: tabla de carpetas actualizada, nueva sección "Diferencia entre Tareas de implementación y Mejoras continuas", "Ciclo de vida de un archivo de Mejoras continuas" renombrado a "Ciclo de vida de una tarea de implementación (lote con Punch List)" con el paso nuevo de extracción, y las secciones de inicio/cierre de sesión y Punch List actualizadas para apuntar a `Tareas de implementacion/` | Victor | `docs/README.md` | Aplicado y ejecutado |
| 10 | 2026-09-23 | `AGENTS.md` actualizado: "Frase de cierre de sesión" ahora dice actualizar `Tareas de implementacion/` en ambos flujos y extraer a `Mejoras continuas/` solo si hay aprendizaje; nueva subsección "Tareas de implementación vs Mejoras continuas" dentro de "Flujo con Orquestador" con el criterio y cómo trasladar un aprendizaje | Victor | `AGENTS.md` | Aplicado y ejecutado |
| 11 | 2026-09-23 | Corrección de criterio (Victor): son 3 categorías, no 2 — Tarea de implementación (Workers), Mejora de trabajo/continua (método/herramientas, destino final en `Mejoras continuas/`), Regla de negocio (va directo e integrada al Flujo de trabajo correspondiente, nunca a un archivo aparte). Se borraron los 5 archivos mal creados en `Mejoras continuas/` (contenían reglas de negocio, no mejoras de trabajo) — esas reglas ya estaban aplicadas en sus flujos (confirmado), y se agregaron 2 que faltaban (`06-rdt.md`, `11-dashboard.md`). Se crearon 3 archivos reales de mejora de trabajo (acceso Postgres sin IPv6, falsos negativos Playwright, sobrecargas SQL huérfanas). Se agregaron los apartados obligatorios `## Mejoras (de trabajo)` y `## Reglas de negocio acordadas en esta tarea` al final de las 9 tareas, a la plantilla, y al rol de Auditor/Worker en `roles-y-flujo.md` | Victor | `docs/Mejoras continuas/*`, `docs/Flujos de trabajo/06-rdt.md`, `docs/Flujos de trabajo/11-dashboard.md`, `docs/Tareas de implementacion/*` (9 tareas + plantilla), `docs/00-sistema/roles-y-flujo.md`, `docs/README.md`, `AGENTS.md` | Aplicado y ejecutado |
| 12 | 2026-09-23 | `resumen-checklists.md` movido de `Mejoras continuas/` a `Tareas de implementacion/` (es índice de checklists de implementación, no una mejora de trabajo) — pedido explícito de Victor. Corregida la referencia en `docs/Flujos de trabajo/README.md` | Victor | `docs/Tareas de implementacion/resumen-checklists.md` | Aplicado y ejecutado |
| 13 | 2026-09-23 | Barrido de coherencia: corregidos 5 enlaces rotos que aún apuntaban a `Mejoras continuas/` para archivos ya movidos a `Tareas de implementacion/` (`10-generacion-pr.md`, `20-plan-maestro.md`, `21-curva-s.md` ×2, `Flujos de trabajo/README.md`) | Orquestador (barrido) | Varios flujos | Aplicado y ejecutado |
| 14 | 2026-09-23 | `resumen-checklists.md` movido de `Mejoras continuas/` a `Tareas de implementacion/` (índice de checklists de implementación, no mejora de trabajo) — pedido explícito de Victor. Corregidos: referencia en `Flujos de trabajo/README.md`, encabezado de columna "Documentado en..." (3 tablas), y 3 enlaces heredados en `docs/00-sistema/*.md` que aún apuntaban a la tarea 2026-09-22 en su ubicación vieja (`Mejoras continuas/`). También corregida descripción de `docs/Mejoras continuas` en "Estructura del repositorio" de `AGENTS.md` y una referencia vaga en `17-chat-agentico.md` | Victor | `docs/Tareas de implementacion/resumen-checklists.md`, `docs/00-sistema/*.md`, `AGENTS.md`, `docs/Flujos de trabajo/17-chat-agentico.md` | Aplicado y ejecutado |
| 15 | 2026-09-23 | Nuevo apartado obligatorio `## Carpetas/archivos huérfanos` agregado a la plantilla de tarea — con fin de limpieza, en ambos repositorios (`pg_control_proyectos` y `py_control_proyectos_web`); el agente no borra por su cuenta, reporta a Victor. Agregada la responsabilidad correspondiente a Worker y Auditor en `roles-y-flujo.md`, y mención en `docs/README.md` | Victor | `docs/Tareas de implementacion/plantilla-tarea.md`, `docs/00-sistema/roles-y-flujo.md`, `docs/README.md` | Aplicado y ejecutado — no retroactivo (Victor: "lo dejamos así") |
| 16 | 2026-09-23 | Simulación (no real) de conflicto: mejora de trabajo sin conflicto (MCP Browser vs Playwright) se aplica directo; regla de negocio que contradice una ya escrita (`CPI = HH×HM` vs `CPI = EV/AC` ya vigente en `18-control-avance.md`) se frena y se propone a Victor en vez de aplicarse — confirma que el mecanismo de conflicto funciona como se diseñó | Victor | N/A (simulación) | Confirmado — mecanismo validado |
| 17 | 2026-09-23 | Corrección de momento de registro: los tres apartados obligatorios (Mejoras de trabajo, Reglas de negocio, Huérfanos) **se escriben en el momento en que ocurre cada hallazgo**, no al cerrar la tarea — igual que el Registro de decisiones. Protocolo de conflicto en vivo: preguntar a Victor en el momento → validar respuesta → escribir la decisión → continuar; repetir el ciclo si no se resuelve. Al cerrar, se traslada cada entrada ya escrita a su destino. El Planner debe anticipar incongruencias con flujos ya documentados al armar el plan — el ciclo en vivo es para lo que de verdad no se pudo prever | Victor | `docs/Tareas de implementacion/plantilla-tarea.md`, `docs/00-sistema/roles-y-flujo.md`, `docs/README.md` | Aplicado y ejecutado |
| 18 | 2026-09-23 | Corrección de política de commits: no un commit por cada ítem de la Punch List — commitear cada ~35% de avance acumulado, y solo al terminar completo el ítem en curso (nunca a medias) | Victor | `docs/00-sistema/convenciones-de-trabajo.md`, `docs/00-sistema/roles-y-flujo.md` | Aplicado y ejecutado |
| 19 | 2026-09-23 | Fase 7 (prueba de coherencia) ejecutada: `docs/00-sistema/`, `docs/Tareas de implementacion/` y `docs/Mejoras continuas/` verificados correctos; simulación de tarea nueva con Orquestador exitosa; corregida una desalineación entre `AGENTS.md` y `docs/README.md` sobre el momento de registro (en vivo, no al cierre) y falta de mención a huérfanos en `AGENTS.md`; corregido enlace impreciso en `14-accesos-y-restricciones.md` | Orquestador (Auditor) | `AGENTS.md`, `docs/Flujos de trabajo/14-accesos-y-restricciones.md` | Aprobado |
| 20 | 2026-09-23 | Fase 8 ejecutada: commit `6c26fde` (31 archivos) pusheado a `origin/main`. Tarea queda **pendiente**, no `CERRADO 100%` — falta el ítem no bloqueante de `design.md` (Curva S) | Victor | `origin/main` | Aprobado y ejecutado |

---

# Fase 0 — Diagnóstico y congelamiento

## Objetivo

Validar el estado real del repositorio y confirmar qué está desactualizado.

## Pasos

- [x] Leer `AGENTS.md` completo.
- [x] Leer `README.md` (raíz) completo.
- [x] Leer `docs/README.md` completo.
- [x] Listar el contenido de `docs/`:
  - `docs/00-sistema/` existe: 3 archivos (roles-y-flujo.md, convenciones-de-trabajo.md, gestion-de-sesiones-y-contexto.md).
  - `docs/Tareas de implementacion/` existe: plantilla-tarea.md + 2 tareas (2026-09-22 orquestador, pendiente; esta misma del 2026-09-23).
  - `docs/Mejoras continuas/` existe: 11 archivos, los 9 lotes siguen bien el ciclo Punch List/CERRADO 100%, 2 son permanentes (mejoras-futuras.md, resumen-checklists.md). Nada que mover a Fase 3.
  - `docs/Flujos de trabajo/` existe: **21 flujos** (01 a 21), no 20 — ver hallazgo abajo.
- [x] Verificar rama actual y estado de Git: `main`, sincronizada con origin, único pendiente es el propio archivo de esta tarea.
- [x] Identificar cambios no relacionados; no agregarlos al commit de esta tarea. (Ninguno)
- [x] Crear o actualizar el `## Registro de decisiones` de la tarea activa.
- [x] Presentar informe de impacto a Victor antes de crear o modificar archivos.

## Entregable

Un informe breve con:

- Archivos que se crearán, moverán o modificarán.
- Posibles contradicciones entre `AGENTS.md`, `README.md` (raíz) y `docs/README.md`.
- Lista de los 20 flujos actuales.
- Preguntas pendientes de Victor.

**Punto de control:** no seguir a Fase 1 sin aprobación explícita de Victor.

---

# Fase 1 — Crear `docs/00-sistema/` con políticas operativas

## Objetivo

Crear la carpeta `docs/00-sistema/` con los tres archivos de política operativa.

## Pasos

- [x] Crear carpeta `docs/00-sistema/`. (Ya existía, creada en la tarea 2026-09-22)
- [x] Crear `docs/00-sistema/roles-y-flujo.md` con: Orquestador/Planner/Worker/Auditor, flujo completo, activación visible, límites. (Ya existe con todo el contenido requerido — verificado)
- [x] Crear `docs/00-sistema/convenciones-de-trabajo.md` con: entorno por defecto, pool de ramas (`work-1`/`work-2`, no work-4 — decisión ya tomada en la tarea anterior), worktrees, política de chats. (Ya existe — verificado)
- [x] Crear `docs/00-sistema/gestion-de-sesiones-y-contexto.md` con: dónde se trabaja, regla de contexto, nomenclatura de chats, inicio/cierre, `/compact`. (Ya existe — verificado)
- [x] Registrar en la tarea que estos archivos fueron creados. (Ya existían de la tarea anterior; esta tarea solo verifica, no recrea)
- [x] Presentar los tres archivos a Victor para aprobación.

**Punto de control:** no seguir sin aprobación de Victor.

---

# Fase 2 — Crear `docs/Tareas de implementacion/` y plantilla de tarea

## Objetivo

Crear la carpeta `docs/Tareas de implementacion/` con la plantilla mínima para tareas con Orquestador.

**Aclaración (2026-09-23):** aquí van los archivos que describen **tareas de implementación de Workers** (código, UI, queries, migraciones — ver "Distinción clave" al inicio de este documento). Cada tarea registra qué se implementó, pero **no** es el lugar donde queda la regla permanente — esa se traslada a `Mejoras continuas/` y de ahí a la fuente de verdad correspondiente.

## Pasos

- [x] Verificar si `docs/Tareas de implementacion/` ya existe. (Sí)
- [x] Si no existe, crearla. (No aplica, ya existe)
- [x] Crear `docs/Tareas de implementacion/plantilla-tarea.md` con la estructura requerida. (Ya existe, contenido verificado contra lo pedido — coincide)
- [x] Mover a esta carpeta cualquier archivo de tarea de implementación que esté en otra ubicación. (`docs/` raíz solo tiene `README.md`; nada suelto que mover)
- [x] Registrar en la tarea los archivos movidos. (Ninguno — nada que mover)
- [x] Presentar a Victor la lista de archivos movidos para aprobación. (Lista vacía)

**Punto de control:** no seguir sin aprobación de Victor.

---

# Fase 3 — Reordenar `docs/Mejoras continuas/`

## Objetivo

Dejar en `docs/Mejoras continuas/` solo lo que realmente es mejora continua (lotes de trabajo recurrente, con Punch List, cierres `CERRADO 100%`).

**Criterio de clasificación (2026-09-23):** ver "Distinción clave" al inicio de este documento.
- Es **tarea de implementación** (no pertenece aquí) si describe principalmente trabajo operativo de construcción: código, UI, queries, migraciones.
- Es **mejora continua** (sí pertenece aquí) si documenta un aprendizaje, regla o buena práctica que se traslada a una fuente de verdad.
- Aquí **NO** van tareas de implementación puras. Aquí van los aprendizajes, reglas y buenas prácticas que nacen de las tareas — cada mejora debe indicar de qué tarea nació y a qué fuente de verdad se trasladó.

## Pasos

- [x] Listar todos los archivos en `docs/Mejoras continuas/`. (11 archivos)
- [x] Re-evaluar los 9 lotes bajo el criterio estricto — **ejecutado** (Victor eligió la opción B: separar). Resultado:
  - Los 9 lotes completos se movieron a `Tareas de implementacion/` (son trabajo de Workers): `2026-09-20-sub-lote-2-alcance-proyecto.md`, `2026-09-20-evm-fase-0-catalogo-unico.md`, `2026-09-21-evm-fase-1-congelar-tarifa.md`, `2026-09-20-control-avance-plan-maestro.md`, `2026-09-21-fix-reemplazar-dp.md`, `2026-09-21-curva-s-fase-3-agente-d.md`, `2026-09-21-dashboard-fase-3-agente-c.md`, `2026-09-21-pr-fase-1-pipeline-rdt.md`, `2026-09-21-pr-fase-2-pipeline-linea-base.md`.
  - De esos 9, **5 tenían contenido real en `## Mejoras a flujos`** (sub-lote-2, pr-fase-1, pr-fase-2, curva-s-fase-3, dashboard-fase-3): se extrajo a un archivo nuevo homónimo en `Mejoras continuas/`, con origen/destino/estado de cada aprendizaje (varios ya aplicados, un par pendientes de verificar).
  - Los otros 4 tenían `## Mejoras a flujos` vacío (evm-fase-0, evm-fase-1, control-avance-plan-maestro, fix-reemplazar-dp): no queda nada de ellos en `Mejoras continuas/`.
  - `mejoras-futuras.md` se renombró a `tareas-futuras.md` y se movió también a `Tareas de implementacion/` (era backlog de tareas pospuestas, no de aprendizajes — pedido explícito de Victor). Se corrigieron todas las referencias cruzadas.
  - `resumen-checklists.md` queda en `Mejoras continuas/` (es un índice, no una tarea).
- [x] Verificar que no queden tareas de implementación en `Mejoras continuas/`. (Confirmado tras el traslado)
- [x] Registrar en la tarea los archivos movidos. (Ver arriba y Registro de decisiones)
- [x] Presentar a Victor la lista de archivos movidos para aprobación. (Ejecutado por indicación directa de Victor, ver Registro de decisiones)

**Punto de control:** no seguir sin aprobación de Victor.

---

# Fase 4 — Actualizar `docs/README.md`

## Objetivo

Asegurar que `docs/README.md` refleje la estructura real y el flujo de Orquestador.

## Pasos

- [x] Agregar o actualizar la sección "00-sistema/": ya existe en la tabla (fila `00-sistema/`), con referencia a los 3 archivos y la explicación "cómo se trabaja, no de qué trata el sistema" — texto literal ya presente.
- [x] Agregar o actualizar la sección "Inicio de tarea con Orquestador": ya existe completa (activación remite a `roles-y-flujo.md`, qué leer, crear archivo con plantilla, registrar entorno/chats/ramas/worktrees/decisiones).
- [x] Verificar que "Ciclo de vida de un archivo de Mejoras continuas" esté clara. (Sí, sin cambios)
- [x] Verificar que "Verificación en vivo — Punch List de Mejoras" esté actualizada. (Sí, enlace vigente al artifact)
- [x] **Nuevo (2026-09-23):** agregada sección "Diferencia entre Tareas de implementación y Mejoras continuas" con definición y ejemplo.
- [x] Reescrito "Ciclo de vida de una tarea de implementación (lote con Punch List)" (antes decía "de un archivo de Mejoras continuas") — ahora vive conceptualmente en `Tareas de implementacion/`, con el paso nuevo de extraer `## Mejoras a flujos` a `Mejoras continuas/`.
- [x] Actualizadas las tablas y secciones que mencionaban `Mejoras continuas/` como bitácora de trabajo activo: ahora apuntan a `Tareas de implementacion/` (Qué leer al iniciar sesión, Qué hace el agente al cerrar sesión, Verificación en vivo — Punch List).
- [x] Actualizada la sección "Tareas futuras" (antes "Mejoras futuras") con la nueva ubicación y nombre.
- [x] Presentar los cambios a Victor para aprobación.

**Punto de control:** no seguir sin aprobación de Victor.

---

# Fase 5 — Actualizar `README.md` (raíz)

## Objetivo

Actualizar la visión del sistema para que refleje la estructura real y los 20 flujos actuales.

## Pasos

- [x] Revisar "Estructura principal": agregadas las entradas `docs/00-sistema/` y `docs/Tareas de implementacion/`; `docs/Mejoras continuas/` ya estaba.
- [x] Revisar "Qué contiene": agregada la mención a políticas operativas de Orquestador/Planner/Worker/Auditor.
- [x] Agregar sección "Fuentes de verdad": creada, con los 4 documentos y regla de resolución de contradicciones (consultar a Victor).
- [x] Agregar sección "Ciclo de mejora continua": creada, con la regla de traslado solo con autorización explícita y el criterio de cuándo se actualiza cada fuente.
- [x] Revisar lista de los 20 flujos: **no existe tal lista en `README.md` raíz** (solo la "Regla de diseño central" de 8 pasos, que sigue siendo correcta) — no se agrega una lista nueva de los 21 flujos aquí para no duplicar la que ya vive en `AGENTS.md` y `docs/Flujos de trabajo/README.md` (regla de "única fuente de verdad por concepto").
- [x] Presentar los cambios a Victor para aprobación.

**Punto de control:** no seguir sin aprobación de Victor.

---

# Fase 6 — Actualizar `AGENTS.md`

## Objetivo

Integrar el flujo de Orquestador con las frases de inicio/cierre de sesión.

## Pasos

- [x] Revisar "Frase de inicio de sesión": diferenciada en dos frases de activación, la de Orquestador remite a la nueva sección "Flujo con Orquestador".
- [x] Revisar "Frase de cierre de sesión": ahora distingue actualizar `Mejoras continuas/` (flujo normal) o `Tareas de implementacion/` (flujo Orquestador); sigue sin crear memoria de sesión aparte.
- [x] Agregar sección "Flujo con Orquestador": creada, remite a `roles-y-flujo.md`, explica que el Orquestador es el punto único de contacto y que las tareas van en `Tareas de implementacion/`.
- [x] Además (aprobado en Fase 0): renombrado `01-interfaz sera cambiado a configuracion.md` → `01-configuracion.md` (título actualizado, marcado pendiente de definir), corregidas las referencias rotas en `AGENTS.md` y `docs/Flujos de trabajo/README.md`, y agregado el flujo 21 a la lista de "Flujos principales" de `AGENTS.md`.
- [x] **Nuevo (2026-09-23):** agregada subsección "Tareas de implementación vs Mejoras continuas" dentro de "Flujo con Orquestador": qué es cada una y cómo trasladar un aprendizaje.
- [x] Actualizada "Frase de cierre de sesión" para que ambos flujos (normal y Orquestador) actualicen `Tareas de implementacion/`, y extraigan a `Mejoras continuas/` solo si hay aprendizaje trasladable.
- [x] Presentar los cambios a Victor para aprobación.

**Punto de control:** no seguir sin aprobación de Victor.

---

# Fase 7 — Prueba de coherencia

## Objetivo

Verificar que las tres fuentes de verdad estén alineadas.

## Pasos

- [x] Verificar que `AGENTS.md`, `README.md` (raíz) y `docs/README.md` no se contradigan. (Encontrada y corregida una desalineación: `AGENTS.md` § "Tareas de implementación, Mejoras continuas y Reglas de negocio" todavía decía "termina en los apartados" (framing de cierre) y no mencionaba huérfanos ni el protocolo de conflicto en vivo — corregido para calzar con `docs/README.md`. También corregida "Frase de cierre de sesión" para incluir huérfanos)
- [x] Verificar que:
  - `docs/00-sistema/` existe con los 3 archivos. ✅
  - `docs/Tareas de implementacion/` existe con la plantilla. ✅
  - `docs/Mejoras continuas/` tiene solo mejoras continuas (3 archivos, todos mejoras de trabajo reales, sin reglas de negocio ni tareas). ✅
- [x] Simular una tarea nueva con Orquestador:
  - ¿Un agente nuevo sabría qué leer? Sí — `AGENTS.md` § Frase de inicio distingue el flujo Orquestador y remite a "Flujo con Orquestador", que remite a los 3 archivos de `00-sistema/`.
  - ¿Sabría dónde crear la tarea? Sí — `docs/Tareas de implementacion/` con `plantilla-tarea.md`.
  - ¿Sabría cómo trasladar aprendizajes a las fuentes de verdad? Sí — plantilla con los 3 apartados obligatorios, llenados en el momento, con protocolo de conflicto explícito.
  - Simulación de conflicto real ejecutada con Victor (mejora de trabajo sin conflicto vs. regla de negocio que contradice `18-control-avance.md`) — el mecanismo frenó correctamente el conflicto en vez de aplicarlo.
- [x] Registrar inconsistencias y corregirlas. (Ver filas 16-18 del Registro de decisiones + el enlace impreciso en `14-accesos-y-restricciones.md`, ya corregido)
- [x] Presentar resultados a Victor.

**Punto de control:** no seguir sin aprobación de Victor.

---

# Fase 8 — Cierre de esta implementación

## Pasos

- [x] Auditor revisa consistencia entre `AGENTS.md`, `README.md`, `docs/README.md`, `docs/00-sistema/`, `docs/Tareas de implementacion/`, `docs/Mejoras continuas/`.
- [x] Resolver contradicciones, enlaces rotos o duplicaciones. (10 enlaces rotos corregidos, ver Fase 7)
- [x] Presentar a Victor los cambios documentales que pasarán a ser permanentes.
- [x] Con aprobación de Victor, actualizar documentos aprobados.
- [x] Actualizar esta tarea con resultados y destino de cada decisión.
- [x] Solicitar autorización explícita antes de hacer commit/push.
- [x] Hacer commit y push solo con los archivos revisados y autorizados. (commit `6c26fde`, pusheado a `origin/main`)
- [ ] Renombrar esta tarea a `— CERRADO 100%.md` únicamente cuando no queden pendientes. (No aplica todavía: queda el pendiente no bloqueante de `design.md`)

## Cierre esperado

```text
✅ Fuentes de verdad alineadas.

- `docs/00-sistema/` creado con:
  - roles-y-flujo.md
  - convenciones-de-trabajo.md
  - gestion-de-sesiones-y-contexto.md
- `docs/Tareas de implementacion/` creado con plantilla.
- `docs/Mejoras continuas/` reordenado.
- `docs/README.md` actualizado.
- `README.md` (raíz) actualizado.
- `AGENTS.md` actualizado.
- Prueba de coherencia: aprobada.
- Pendientes futuros:

¿Autorizas el commit/push final y el cierre documental?
```

---

# Prompt para iniciar este plan

Copia este mensaje en Claude (app de escritorio o web), dentro del repositorio documental:

```text
Vamos a trabajar en un plan de reordenamiento y actualización de fuentes de verdad.

Ejecuta este único plan:
docs/Tareas de implementacion/2026-09-23-reordenamiento-y-actualizacion-fuentes-de-verdad.md

Empieza por Fase 0 — Diagnóstico y congelamiento.

No modifiques, crees, renombres, borres, commitees, pushees, hagas merge, abras PR, crees ramas, crees worktrees ni abras sesiones cloud antes de presentarme el informe de impacto y obtener mi aprobación explícita.

Lee AGENTS.md, README.md (raíz), docs/README.md y los documentos aplicables de docs/. Mantén actualizado el Registro de decisiones de esta tarea.

Al finalizar cada fase, presenta los cambios a Victor y espera aprobación explícita antes de continuar.
```
