# Brief de tanda C6 — Seguimiento modo RDT / manual (106)

## Rol, modelo y tanda

CR-1, nivel 3 (n3), Sonnet, esfuerzo Medio. Ola 3. Se lanza como «Worker CR-1 · C6». Plan: `2026-10-15-cronograma-gantt-linea-base-histogramas.md` (no lo leas completo; busca por ID de ítem).

## Ítems de la tanda

- **CG-60**: Migración 106: cronograma_seguimiento (modo, comienzo, fin, %) e historial. NO se aplica.
- **CG-61**: Modo RDT: comienzo = primer día con metrado validado; % ponderado por valor programado (método de src/lib/curva-s/curva-s.ts, salida en %); fin = último día con avance si 100 %, si no fin base u hoy si lo pasó.
- **CG-62**: Interruptor RDT/manual; manual no cambia con RDT nuevos y dice «Manual»; volver a RDT pide confirmación, recalcula y guarda historial.
- **CG-63**: Hito o actividad sin partidas: solo manual; interruptor deshabilitado con motivo.
- **CG-64**: Fila «Proyecto» en RDT = % físico de la Curva S del mismo corte (prueba cruzada).
- **CG-65**: PR, Dashboard y Curva S iguales antes y después de editar manual.
- **CG-66**: Se edita con Plan Maestro aprobado; validado en servidor.

Decisiones ya resueltas (no se reabren): D1 avance manual no alimenta PR/Dashboard/Curva S; D2 seguimiento editable con Plan Maestro aprobado; D3 cuatro tipos de vínculo FC/CC/FF/CF con desfase ±; D4 calendario lunes-sábado con no laborables; D5 sin cascada de pronóstico.

## Rama, worktree y puerto

Rama: local-worker-4. Worktree: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\<rama>`. Puerto: el que fije el Orquestador. Empieza con `git merge main` en tu rama y confirma `git status` limpio. Un solo worktree activo.

## Qué leer, y qué no

- src/lib/curva-s/curva-s.ts (método físico)
- src/app/api/cronograma/linea-base (de C5)
- Flujos 18 y 21 solo la parte de avance físico
- Spec del plan §D (buscar «Línea de seguimiento»)
- No leas: el plan completo, la evidencia ni el progreso completos, ni los 21 flujos.

## Qué puede trabajar

- Puede: db/106_*.sql
- Puede: src/lib/cronograma/seguimiento.ts + test
- Puede: src/app/api/cronograma/seguimiento/route.ts
- Puede: PanelSeguimiento.tsx
- NO puede: src/lib/rdts/**, src/lib/pr/**, src/lib/dashboard/**: solo LEER los validados; si hace falta compartir código, extraer a src/lib/curva-s/ sin cambiar su resultado y devolver la duda al Orquestador
- Siempre fuera de límites: flujos de negocio, AGENTS.md, el estándar, el Spec, `src/lib/rdts/**`, `db/098` a `db/102`.

## Dónde deja su entrega y su evidencia

- Código: su rama.
- Resumen de cierre: `resultados/C6.md` (plantilla `12-resumen-de-cierre-de-tanda.md`).
- Evidencia dentro de ese resumen; máximo una captura por ítem.

## Contrato técnico verificado

- D1: el avance manual NO alimenta PR, Dashboard ni Curva S. D2: seguimiento editable con Plan Maestro aprobado. D5: sin cascada.
- Cómo se leen los RDT validados por actividad: por confirmar en el código (primer paso).
- Migraciones: última en main 097; 098 a 102 son del plan de Informes; este plan usa 103 a 107. Verifica `ls db/` antes de escribir.
- Sin dependencias nuevas de interfaz (design.md §1 y §13).

## Skills que debe usar

- cerrar-tanda

## Comandos de verificación

- npx vitest run src/lib/cronograma src/lib/curva-s
- npx tsc --noEmit
- npx eslint src/lib/cronograma

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra lo que tiene y escribe el traspaso. Una sola captura por ítem. Las migraciones, las credenciales y la verificación en vivo siguen el protocolo del plan: el Worker escribe las migraciones, NO las aplica.

## Cómo registra hallazgos y preguntas

Los hallazgos van a su resumen, en los cinco grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos, preguntas). Una pregunta de negocio o un conflicto con un flujo se devuelve al Orquestador en el momento; no sigue con el conflicto sin resolver. Credenciales: nunca leerlas ni mostrarlas.

## Criterios de salida

- Prueba cruzada con la Curva S en verde.
- Todos los ítems de la tanda en Conforme u Observado con evidencia; ninguno a medias. Cierre con el Skill `cerrar-tanda`.
