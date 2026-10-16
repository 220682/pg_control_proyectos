# Brief de tanda C11 — Documentación y traslado de hallazgos

## Rol, modelo y tanda

Documentador, nivel 0 o 1 (n0/n1), Haiku, esfuerzo Medio. Ola 5. Se lanza como «Worker Documentador · C11». Plan: `2026-10-15-cronograma-gantt-linea-base-histogramas.md` (no lo leas completo; busca por ID de ítem).

## Ítems de la tanda

- **CG-110**: Flujos 09, 14, 15, 16, 18, 20 y design.md actualizados con lo aprobado en el Gate 1 (tabla de contradicciones del plan, fila por fila).
- **CG-111**: Artefacto «Matriz de permisos» actualizado con el flujo 14.
- **CG-112**: python scripts/verificar-referencias.py sin errores; planes-futuros.md marca el ítem como promovido.
- **CG-113**: Skill trasladar-hallazgos: reglas R1 a R5 a los flujos, mejoras a 03-aprendizaje-continuo, huérfanos reportados.

Decisiones ya resueltas (no se reabren): D1 avance manual no alimenta PR/Dashboard/Curva S; D2 seguimiento editable con Plan Maestro aprobado; D3 cuatro tipos de vínculo FC/CC/FF/CF con desfase ±; D4 calendario lunes-sábado con no laborables; D5 sin cascada de pronóstico.

## Rama, worktree y puerto

Rama: main del repo documental. Worktree: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\<rama>`. Puerto: el que fije el Orquestador. Empieza con `git merge main` en tu rama y confirma `git status` limpio. Un solo worktree activo.

## Qué leer, y qué no

- El plan: secciones «Cambios que contradicen lo escrito» y «Libro de hallazgos»
- Los flujos citados (solo las secciones afectadas)
- .claude/skills/trasladar-hallazgos/
- Resúmenes de resultados/
- No leas: el plan completo, la evidencia ni el progreso completos, ni los 21 flujos.

## Qué puede trabajar

- Puede: Los flujos 09, 14, 15, 16, 18, 20, design.md, planes-futuros.md y el artefacto Matriz de permisos
- NO puede: AGENTS.md, el estándar, el Spec; no editar un flujo sin respuesta de Victor registrada para esa fila
- NO puede: No borrar nada
- Siempre fuera de límites: flujos de negocio, AGENTS.md, el estándar, el Spec, `src/lib/rdts/**`, `db/098` a `db/102`.

## Dónde deja su entrega y su evidencia

- Código: su rama.
- Resumen de cierre: `resultados/C11.md` (plantilla `12-resumen-de-cierre-de-tanda.md`).
- Evidencia dentro de ese resumen; máximo una captura por ítem.

## Contrato técnico verificado

- Artefacto Matriz de permisos: https://claude.ai/artifact/4no1PCEfDb5pYmgmnrP5MT
- Migraciones: última en main 097; 098 a 102 son del plan de Informes; este plan usa 103 a 107. Verifica `ls db/` antes de escribir.
- Sin dependencias nuevas de interfaz (design.md §1 y §13).

## Skills que debe usar

- trasladar-hallazgos
- cerrar-tanda

## Comandos de verificación

- python scripts/verificar-referencias.py

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra lo que tiene y escribe el traspaso. Una sola captura por ítem. Las migraciones, las credenciales y la verificación en vivo siguen el protocolo del plan: el Worker escribe las migraciones, NO las aplica.

## Cómo registra hallazgos y preguntas

Los hallazgos van a su resumen, en los cinco grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos, preguntas). Una pregunta de negocio o un conflicto con un flujo se devuelve al Orquestador en el momento; no sigue con el conflicto sin resolver. Credenciales: nunca leerlas ni mostrarlas.

## Criterios de salida

- Todo el libro de hallazgos trasladado y listado.
- Todos los ítems de la tanda en Conforme u Observado con evidencia; ninguno a medias. Cierre con el Skill `cerrar-tanda`.
