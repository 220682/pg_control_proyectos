# Brief de tanda C3 — Gantt a mano en SVG

## Rol, modelo y tanda

CR-1, nivel 3 (n3), Sonnet, esfuerzo Medio. Ola 2. Se lanza como «Worker CR-1 · C3». Plan: `2026-10-15-cronograma-gantt-linea-base-histogramas.md` (no lo leas completo; busca por ID de ítem).

## Ítems de la tanda

- **CG-30**: Escalas día, semana (sábado a viernes) y mes.
- **CG-31**: Barras de tarea, resumen (negro con corchetes) e hitos (rombo).
- **CG-32**: Flechas de dependencia de los cuatro tipos.
- **CG-33**: Línea «hoy» punteada con fecha y leyenda siempre visible.
- **CG-34**: Arrastrar mueve/estira, actualiza la tabla y marca «fijada a mano».
- **CG-35**: Todo con teclado y escribiendo en la tabla.
- **CG-36**: Tres paneles ocultables, scroll vertical sincronizado, móvil solo lectura.

Decisiones ya resueltas (no se reabren): D1 avance manual no alimenta PR/Dashboard/Curva S; D2 seguimiento editable con Plan Maestro aprobado; D3 cuatro tipos de vínculo FC/CC/FF/CF con desfase ±; D4 calendario lunes-sábado con no laborables; D5 sin cascada de pronóstico.

## Rama, worktree y puerto

Rama: local-worker-4. Worktree: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\<rama>`. Puerto: el que fije el Orquestador. Empieza con `git merge main` en tu rama y confirma `git status` limpio. Un solo worktree activo.

## Qué leer, y qué no

- La maqueta aprobada de C0 (cronograma-editor-gantt.html)
- src/components/cronograma/TablaCronograma.tsx (de C2)
- src/components/plan-maestro/LienzoPlanMaestro.tsx (tres paneles)
- design.md §1, §13
- No leas: el plan completo, la evidencia ni el progreso completos, ni los 21 flujos.

## Qué puede trabajar

- Puede: src/components/cronograma/GanttCronograma.tsx y utilidades de escala (nuevos)
- Puede: EditorCronograma.tsx (montar el Gantt)
- NO puede: Dependencias nuevas en package.json (prohibido)
- NO puede: El motor (C1) salvo bugs, que se devuelven al Orquestador
- Siempre fuera de límites: flujos de negocio, AGENTS.md, el estándar, el Spec, `src/lib/rdts/**`, `db/098` a `db/102`.

## Dónde deja su entrega y su evidencia

- Código: su rama.
- Resumen de cierre: `resultados/C3.md` (plantilla `12-resumen-de-cierre-de-tanda.md`).
- Evidencia dentro de ese resumen; máximo una captura por ítem.

## Contrato técnico verificado

- El arrastre llama al mismo endpoint de C2; el servidor recalcula.
- Virtualización de filas desde 60 filas debe valer también para el Gantt.
- Migraciones: última en main 097; 098 a 102 son del plan de Informes; este plan usa 103 a 107. Verifica `ls db/` antes de escribir.
- Sin dependencias nuevas de interfaz (design.md §1 y §13).

## Skills que debe usar

- dataviz
- cerrar-tanda

## Comandos de verificación

- npx vitest run src/components/cronograma
- npx tsc --noEmit
- npx eslint src/components/cronograma
- Playwright: arrastre y teclado

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra lo que tiene y escribe el traspaso. Una sola captura por ítem. Las migraciones, las credenciales y la verificación en vivo siguen el protocolo del plan: el Worker escribe las migraciones, NO las aplica.

## Cómo registra hallazgos y preguntas

Los hallazgos van a su resumen, en los cinco grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos, preguntas). Una pregunta de negocio o un conflicto con un flujo se devuelve al Orquestador en el momento; no sigue con el conflicto sin resolver. Credenciales: nunca leerlas ni mostrarlas.

## Criterios de salida

- Gantt coincide con la maqueta aprobada; tabla y Gantt se actualizan juntos.
- Todos los ítems de la tanda en Conforme u Observado con evidencia; ninguno a medias. Cierre con el Skill `cerrar-tanda`.
