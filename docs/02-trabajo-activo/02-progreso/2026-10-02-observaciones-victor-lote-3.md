# Progreso — Observaciones de Victor, Lote 3 (Enmienda E1: el Plan Maestro es el umbral)

> Archivo escrito el 2026-10-04 tras las tandas R1, R2, R3, R4a, R4b, R5, R5b, R6a y R6b. Refleja el estado real antes del Gate 2.

## Referencia al plan

- Plan: [`docs/02-trabajo-activo/01-planes/2026-10-02-observaciones-victor-lote-3-plan.md`](../01-planes/2026-10-02-observaciones-victor-lote-3-plan.md)
- Spec: no hay Spec/SDD propio (OP2). El plan contiene las 13 observaciones y las reglas confirmadas; la Enmienda E1 y su Gate 1 Complementario se registers en el plan.
- Briefs y resultados: [`…/2026-10-02-observaciones-victor-lote-3-briefs/`](../01-planes/2026-10-02-observaciones-victor-lote-3-briefs/) (`resultados/` con `N`, `R1`, `R2-R3`, `R4a`, `R5`, `R6a`, `R6b`).
- Evidencia: [`docs/02-trabajo-activo/03-evidencia/2026-10-02-observaciones-victor-lote-3.md`](../03-evidencia/2026-10-02-observaciones-victor-lote-3.md)

## Estado general y fase actual

- **Estado: implementación terminada, informe del Auditor emitido, pendiente Gate 2.** Las nueve tandas de la Enmienda E1 están cerradas (más R4c en código). El informe del Auditor ([`04-auditoria/2026-10-02-observaciones-victor-lote-3.md`](../04-auditoria/2026-10-02-observaciones-victor-lote-3.md)) pide **corrección mayor**; sus Olas 0, 1, 2, 3 y 4 son el trabajo que sigue.
- **Tareas de la Enmienda E1, todas cerradas el 2026-10-04:**

| Tanda | Qué | Estado | Commit |
|---|---|---|---|
| R1 | Retirar la edición de actividades del cronograma con PM aprobado | Cerrada | `ceb269e` |
| R2 | Congelar paquetes con PM aprobado | Cerrada | `d916716` |
| R3 | RDT exige PM aprobado + servicio `EJECUCION` | Cerrada | `74734d7` |
| R4a | Reposicionamiento: código, módulo, pruebas y migración `093` | Cerrada | `11804b6`, `56c66e0`, `d7d96fd` |
| R4b | Aplicar la migración `093` | Cerrada | aplicada y verificada 08:41 |
| R5 | Escribir U1–U8 en los flujos | Cerrada | — |
| R5b | Precisiones de las tres respuestas de Victor | Cerrada | — |
| R6a | Guardia de U1 en la carga de RDT por archivo | Cerrada | `26288bf` |
| R6b | Congelar `MOVER` con PM aprobado (U10) | Cerrada | `9d033e3` |
| R4c | Reposicionamiento determinista: migración `094`, `sinLinea` que vuelve en la respuesta, aviso de dependencia de la `093` | **Cerrada en código; la `094` no está aplicada** | `ae476f1` · tsc 0 · 1115 tests · [`resultados/R4c.md`](../01-planes/2026-10-02-observaciones-victor-lote-3-briefs/resultados/R4c.md) |

- **Deuda que sigue abierta y no se ha resuelto en este plan:** F5 (RDT) quedó **parcial** en la tanda F; el PATCH del Plan Maestro nunca se verificó en vivo (OP9); el reposicionamiento **no se ha probado en vivo** porque ningún servicio de prueba sirve para una aprobación real; y la **`094` no se aplicó**, así que la base sigue con la `093`, que es la versión **no determinista** del reposicionamiento (riesgo `R4a-O3` del libro de hallazgos).

## Tabla de roles / Workers y estado

| Rol | Estado |
|---|---|
| Responsable humano | Aprobó el Gate 1 (2026-10-02), la Enmienda E1 (2026-10-03), el Gate 1 Complementario (2026-10-03) y respondió las tres preguntas de R4/R6 el 2026-10-04 |
| Orquestador | Continuó el plan, creó la política de niveles de modelos, lançó las tandas con `opencode run --model`, aplicó la migración `093`, hizo las precisiones R5b, y escribió el progreso y la evidencia |
| Worker flash (nivel 1) | R5, R6a, R6b y R4a: cuatro tarefas, todas cerradas |
| Planner | No particip\u00f3 (el plan lo hizo el Orquestador; OP2) |
| Documentador | Hecho por el Orquestador en esta tanda (progreso, evidencia, aprendizaje, índices) |
| Auditor | **Pendiente** |

## Skills revisados

`seguir-flujo-de-planes` (Orquestador, al abrir y antes del Gate 2), `cerrar-tandas` (Workers), `trasladar-hallazgos` (Documentador). `verificar-permisos-por-rol` **no aplica**: ninguna de las nueve tandas cambia la matriz de permisos (la que lo hacía, `puedeEditarActividadCronograma`, se retiró en R1).

## Avances terminados

- **La Enmienda E1 completa en código.** U1 (el RDT exige PM aprobado + servicio en Ejecución, en las tres vías de creación), U3 (congelamiento de DP, PR, cronogramas y paquetes, **incluido reordenar**), U4 (reposicionamiento de los RDT al aprobar un plan nuevo), U7 (rastro en el historial), U8 (todo o nada) y U10.
- **Migración `093` aplicada y verificada** con el protocolo: conexión directa, candado, una transacción, conteos de 8 tablas idénticos antes y después, CHECK de `rdt_partes_historial.accion` ampliado con `REPOSICIONAMIENTO`, función `aprobar_plan_maestro_con_reposicionamiento(uuid, uuid, jsonb)` creada. Script temporal y candado borrados.
- **El reposicionamiento no toca el metrado del RDT ni las cifras del PR; sí toca su asociación de paquete.** Verificado en código: no hay FK entre RDT y línea del plan, así que se re-vincula por la **clave de reporte** `paquete × partida`. **Lo que no cambia:** el `metrado_ejecutado`, los metrados derivados, las horas y el estado de validación, y **las cifras del PR consolidado** (el PR agrupa por partida, no por paquete). **Lo que sí cambia:** la asociación de paquete del RDT (`rdt_actividades.paquete_trabajo_id` y `rdt_actividad_partidas.paquete_trabajo_id`), que **se ve en su propio formulario y en la pantalla Status**. La frase anterior de este archivo («no toca los datos del RDT») era más fuerte que lo que el código garantiza; corregida el 2026-10-04 por el Auditor.
- **Documentación:** los seis flujos del alcance quedaron escritos (R5) y las cuatro precisiones de sus respuestas quedaron integradas (R5b). Verificador de referencias: 0 huérfanos, 0 enlaces rotos, exit 0.
- **Política de niveles de modelos** creada y verificada: `docs/00-estandar-agentes/10-niveles-de-modelos.md` + `scripts/niveles-modelos.py`, con la tabla medida de 21 modelos y cinco hechos comprobados sobre la configuración.

## Trabajo actual

Ninguno de implementación en documentación: las **Olas 1, 2 y 4** del Auditor (correcciones de redacción, las tres decisiones de negocio por escrito y el libro de hallazgos) están **cerradas** el 2026-10-04 ([`resultados/DOCS-L3.md`](../01-planes/2026-10-02-observaciones-victor-lote-3-briefs/resultados/DOCS-L3.md)). Lo que sigue, en orden: **Ola 0b** (aplicar la `094`) → **Ola 3** (U6 en código, corre en paralelo) → **Ola 5** (verificación en vivo) → **Gate 2 de Victor** → merge de `local-worker-4` a `main` en el repositorio de código y push de ambos.

## Pendientes

1. **Gate 2 de Victor** y, con su aprobación, merge de `local-worker-4` → `main` (código) y push de ambos repositorios.
2. **Verificación en vivo del reposicionamiento** (R4): ningún servicio de prueba tiene Plan Maestro en BORRADOR (OP9). Sin eso, U4 queda verificada por pruebas y por la migración, no en la app.
3. **Cinco reglas de negocio pendientes de decisión de Victor**: las cuatro que dejó abiertas el Worker de R4a —R4a-R1 (RDT cuya partida ya no está en el plan), R4a-R2 (partida en dos líneas con paquetes distintos), R4a-R3 (filas derivadas que cambian de paquete sin recalcular metrado) y R4a-R4 (porcentaje de avance calculado sobre el plan viejo)— y **R4c-R1** (actividad con varios vínculos que el plan nuevo reparte en paquetes distintos: no se reposiciona y se reporta como ambigua; el código ya lo hace con la `094`, la regla no está escrita).
4. **Aplicar la `094`** con el protocolo de migraciones: sin ella la base usa la `093`, que no es determinista.
5. **F5 parcial** (libertad de WBS para C/NC, equipos y materiales) y **OP9**: quedan para un plan futuro.
6. **`agent.roles` en los dos archivos de configuración** sigue nombrando `qwen3.8-plus`, que no existe. No lo edita un agente: lo retira Victor.
7. ~~Fila OP7 con una celda menos~~ — **resuelto el 2026-10-04**: la fila se completó y su estado se corrigió (decía «Resuelta» y no del todo; ahora es «Registrada», con el motivo).

## Commits, ramas y worktrees usados

- **Código (`py_control_proyectos_web`):** rama `local-worker-4`, worktree `.worktrees/local-worker-4`. Hoy: `ceb269e`, `d916716`, `74734d7`, `26288bf`, `9d033e3`, `11804b6`, `56c66e0`, `d7d96fd`, `ae476f1`. **Sin push y sin merge.** `main` = `origin/main` = `cd10882`.
- **Documentación (`pg_control_proyectos`):** todo el trabajo de hoy está **sin commitear**, en `main`. Esperando el Gate 2.

## Medición

`python scripts/niveles-modelos.py` sobre la base de opencode (227 sesiones del 2026-10-01 al 2026-10-04, 30,09 USD medidos). Las cinco tareas de hoy se lanzar con `opencode run --model`, y sus corridas también quedan en esa base. El costo de las cuatro tareas de Worker **no está desglosado por tanda** en este archivo: queda pendiente cruzarlo con los títulos de sesión (`R5-worker`, `R6a-worker`, `R6b-worker`, `R4a-worker`).

## Operaciones de git

- Ninguna escritura de código con push. Ningún merge. Ningún `git add -A` sobre archivos ajenos.
- Se movieron a `resultados/` cuatro archivos temporales del worktree (`R6a-resultado.md`, `R4a-resultado.md`, `R6b-resultado.md` no existió y se redactó, `_protocolo-migraciones.md`) y se borraron del repositorio de código.

## Hallazgos y preguntas de negocio

- El libro de hallazgos del plan tenía 17 mejoras, 9 reglas y 13 observaciones; el 2026-10-04 quedó con **24 mejoras, 13 reglas y 19 observaciones**: entraron las 12 filas que el Auditor encontró sin registrar y las 4 de R4c, y se aplicó su clasificación a las 39 que ya estaban. **Cinco reglas de negocio están pendientes de decisión de Victor**: R4a-R1, R4a-R2, R4a-R3, R4a-R4 y R4c-R1 (esta última, la actividad con varios vínculos repartidos en paquetes distintos: el código ya no la reposiciona y la reporta, pero la regla no está escrita en ningún flujo).
- Ningún huérfano.

## Bloqueos, riesgos y decisiones requeridas

- **Riesgo R6 (de siempre):** lo verificado en local no está verificado en la app desplegada.
- **Riesgo nuevo, declarado:** la aprobación del Plan Maestro ahora pasa por una función SQL. **Si la migración `093` no está aplicada en ese entorno (por ejemplo una base restaurada u otro ambiente), la acción de aprobación falla por completo y no hay fallback.** El 2026-10-04 (R4c, `ae476f1`) ese aviso quedó escrito en el repositorio de código: en la cabecera de `db/093` y en su fila de `db/README.md`. Ojo: la **`094`** —que hace el reposicionamiento determinista y devuelve `sinLinea`— **está en el repositorio pero no en la base**, así que la base usa la `093`.
- **Decisiones requeridas:** las cuatro reglas de R4a y el Gate 2.

## Próximo paso verificable

Informe del Auditor en `docs/02-trabajo-activo/04-auditoria/2026-10-02-observaciones-victor-lote-3.md`, y después el Gate 2.

## Última actualización y responsable

2026-10-04, Orquestador (nueva sesión: política de niveles, benchmark, R6a, R6b, R4a, R4b, R5b, R4/R5/R6b documentados, R6b result redacted).

## Handoffs

### Handoff del 2026-10-04 (Orquestador → Auditor)

- Lee el plan (Enmienda E1, U1–U10, libro de hallazgos, registro de decisiones), este progreso y la evidencia homónima.
- Los ocho commits de código están en `local-worker-4`, **sin mergear**: `ceb269e`, `d916716`, `74734d7`, `26288bf`, `9d033e3`, `11804b6`, `56c66e0`, `d7d96fd`.
- Lo que hay que mirar con más atención: (a) que el reposicionamiento no pueda tocar `metrado_ejecutado` ni las cifras del PR —es la aclaración de Victor y la razón por la que el PR no debe moverse—; (b) que la función `093` sea realmente atómica y que el `payload` que le manda la capa TS no pueda tocar más que la asociación de paquete; (c) que las cuatro reglas de R4a estén efectivamente **sin resolver** y no resueltas por el Worker por su cuenta; (d) el orden Documentador → Auditor: este archivo ya está escrito.
- No verificado en vivo: el reposicionamiento (OP9). No lo des por cierto.

## Cierre de la sesión del 2026-10-04 (tarde)

- **R4c** cerrada: la `094` hace determinista el reposicionamiento (`ae476f1`, tsc 0, 1115 tests). **La `094` no se pudo aplicar**: el archivo de credenciales quedó inalcanzable y el protocolo obliga a detenerse. La base conserva la `093`, no determinista. Es la salvedad número 1 del Gate 2.
- **U6** cerrada: el aviso de impacto antes de aprobar existe (`f19c801`, tsc 0, 1136 tests). Sin verificación en vivo.
- **DOCS-L3** cerrada: los 7 puntos de «APLICAR AHORA», las tres decisiones (U6 vigente, U7 ajustado a lo que guarda el `snapshot`, U9 solo para la creación) y el libro de hallazgos de 39 a **56 filas** con la clasificación del Auditor. Verificador 0/0, exit 0.
- **Dos Workers de nivel 3 murieron sin commitear** (R4c una vez, U6 una vez). En ambos casos el Orquestador validó y commiteó el trabajo que quedó en el worktree. Registrado como U6-M1 y U6-O1.
- **El nivel 3 resultó más caro en tiempo y en corridas perdidas que el nivel 1**, que cerró R5, R6a, R6b y R4a sin un solo corte.
- Pendiente para el siguiente paso: aplicar la `094`, verificar en vivo el reposicionamiento y el aviso U6, y resolver en el Gate 2 las reglas `R4a-R1` a `R4a-R4`, `R4c-R1` y `U6-R1`.
