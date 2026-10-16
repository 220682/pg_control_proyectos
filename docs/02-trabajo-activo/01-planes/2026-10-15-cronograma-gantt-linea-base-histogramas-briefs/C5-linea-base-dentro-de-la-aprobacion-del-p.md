# Brief de tanda C5 — Línea base dentro de la aprobación del Plan Maestro (104 y 105)

## Rol, modelo y tanda

CR-1, nivel 3 (n3), Sonnet, esfuerzo Medio (Victor aprobó nivel 3 con la prueba de atomicidad el 2026-10-15). Ola 3. Se lanza como «Worker CR-1 · C5». Plan: `2026-10-15-cronograma-gantt-linea-base-histogramas.md` (no lo leas completo; busca por ID de ítem).

## Ítems de la tanda

- **CG-55**: PRIMERO: confirmar en db/094 y plan-maestro-aprobado.ts cómo se crea y aprueba una versión nueva del Plan Maestro; escribir el resultado en el resumen. Si contradice el Spec, devolver al Orquestador.
- **CG-50**: Migraciones 104 (cronograma_lineas_base y cronograma_linea_base_actividades) y 105 (aprobar_plan_maestro_con_reposicionamiento con línea base). Aditivas, reversa en comentario. NO se aplican.
- **CG-51**: Aprobar crea la v1 con comienzo, fin y duración congelados, en la misma transacción.
- **CG-52**: Prueba de atomicidad: si falla la línea base o el reposicionamiento no queda aprobado nada.
- **CG-53**: Versión nueva aprobada crea la v2 y la v1 sigue; selector de línea base y variación de fin.
- **CG-54**: Antes de aprobar no hay línea base ni seguimiento.

Decisiones ya resueltas (no se reabren): D1 avance manual no alimenta PR/Dashboard/Curva S; D2 seguimiento editable con Plan Maestro aprobado; D3 cuatro tipos de vínculo FC/CC/FF/CF con desfase ±; D4 calendario lunes-sábado con no laborables; D5 sin cascada de pronóstico.

## Rama, worktree y puerto

Rama: local-worker-4. Worktree: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\<rama>`. Puerto: el que fije el Orquestador. Empieza con `git merge main` en tu rama y confirma `git status` limpio. Un solo worktree activo.

## Qué leer, y qué no

- db/094_aprobar_plan_maestro_reposicion_determinista.sql completo (271 líneas) y db/093
- src/lib/proyectos/plan-maestro-aprobado.ts
- src/lib/rdts/reposicionamiento-servidor.ts (solo leer la llamada)
- docs/04-flujos-de-negocio/20-plan-maestro.md §3 y §6
- No leas: el plan completo, la evidencia ni el progreso completos, ni los 21 flujos.

## Qué puede trabajar

- Puede: db/104_*.sql, db/105_*.sql (nuevos)
- Puede: src/lib/cronograma/linea-base.ts + test
- Puede: src/app/api/cronograma/linea-base/route.ts
- Puede: Selector y columna de variación en la tabla
- NO puede: db/094 (no se edita: create or replace en 105)
- NO puede: src/lib/rdts/**
- NO puede: La firma de la función (uuid, uuid, jsonb) debe conservarse
- Siempre fuera de límites: flujos de negocio, AGENTS.md, el estándar, el Spec, `src/lib/rdts/**`, `db/098` a `db/102`.

## Dónde deja su entrega y su evidencia

- Código: su rama.
- Resumen de cierre: `resultados/C5.md` (plantilla `12-resumen-de-cierre-de-tanda.md`).
- Evidencia dentro de ese resumen; máximo una captura por ítem.

## Contrato técnico verificado

- Función hoy: aprobar_plan_maestro_con_reposicionamiento(uuid, uuid, jsonb); orden interno: Plan Maestro, reposicionamiento, recalcular_pr_planificado (094, líneas 54-214).
- Tabla del Plan Maestro: proyecto_plan_maestro (campo estado 'APROBADO').
- El plan de Informes no redefine esta función.
- Migraciones: última en main 097; 098 a 102 son del plan de Informes; este plan usa 103 a 107. Verifica `ls db/` antes de escribir.
- Sin dependencias nuevas de interfaz (design.md §1 y §13).

## Skills que debe usar

- cerrar-tanda

## Comandos de verificación

- npx vitest run src/lib/cronograma
- npx tsc --noEmit
- Prueba SQL de atomicidad solo en base de prueba que indique Victor; si no hay, probar la lógica en TS y dejar la prueba SQL escrita

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra lo que tiene y escribe el traspaso. Una sola captura por ítem. Las migraciones, las credenciales y la verificación en vivo siguen el protocolo del plan: el Worker escribe las migraciones, NO las aplica.

## Cómo registra hallazgos y preguntas

Los hallazgos van a su resumen, en los cinco grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos, preguntas). Una pregunta de negocio o un conflicto con un flujo se devuelve al Orquestador en el momento; no sigue con el conflicto sin resolver. Credenciales: nunca leerlas ni mostrarlas.

## Criterios de salida

- Migraciones revisadas por el Orquestador antes de pasar a Victor. Nada aplicado.
- Todos los ítems de la tanda en Conforme u Observado con evidencia; ninguno a medias. Cierre con el Skill `cerrar-tanda`.
