# Brief de tanda C8 — Histogramas de HH y HM

## Rol, modelo y tanda

CR-2, nivel 2 (n2), Sonnet, esfuerzo Medio. Ola 2 (tras incorporar C1 y C7). Se lanza como «Worker CR-2 · C8». Plan: `2026-10-15-cronograma-gantt-linea-base-histogramas.md` (no lo leas completo; busca por ID de ítem).

## Ítems de la tanda

- **CG-80**: Histograma programado: metrado programado por día del Plan Maestro × tasa de la partida.
- **CG-81**: Estimado sin Plan Maestro: metrado vinculado repartido parejo sobre días laborables; rótulo de la fuente.
- **CG-82**: Con Plan Maestro al 100 %, Σ HH semanales = HH contractual y Σ HM = HM contractual.
- **CG-83**: Pestaña Histogramas en SVG: semana sábado a viernes, acumulado, pico, filtro cargo/equipo con barras apiladas (design.md §13).
- **CG-84**: Línea «Real» de HH cuando exista tareo validado; HM real apagado y rotulado.

Decisiones ya resueltas (no se reabren): D1 avance manual no alimenta PR/Dashboard/Curva S; D2 seguimiento editable con Plan Maestro aprobado; D3 cuatro tipos de vínculo FC/CC/FF/CF con desfase ±; D4 calendario lunes-sábado con no laborables; D5 sin cascada de pronóstico.

## Rama, worktree y puerto

Rama: local-worker-6 (autorizada por Victor el 2026-10-15). Worktree: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\<rama>`. Puerto: el que fije el Orquestador. Empieza con `git merge main` en tu rama y confirma `git status` limpio. Un solo worktree activo.

## Qué leer, y qué no

- src/lib/plan-maestro/lienzo.ts y lineas.ts (metrado programado por día)
- src/lib/cronograma/calendario.ts (de C1)
- db de C7 (dp_partida_recursos)
- design.md §13
- Maqueta de C0 (pestaña Histogramas)
- No leas: el plan completo, la evidencia ni el progreso completos, ni los 21 flujos.

## Qué puede trabajar

- Puede: src/lib/cronograma/histograma.ts + test
- Puede: src/app/api/cronograma/histogramas/route.ts
- Puede: src/components/cronograma/Histogramas.tsx
- NO puede: src/lib/rdts/**
- NO puede: El tareo real: solo LEER lo validado; HM real depende del plan de Informes
- Siempre fuera de límites: flujos de negocio, AGENTS.md, el estándar, el Spec, `src/lib/rdts/**`, `db/098` a `db/102`.

## Dónde deja su entrega y su evidencia

- Código: su rama.
- Resumen de cierre: `resultados/C8.md` (plantilla `12-resumen-de-cierre-de-tanda.md`).
- Evidencia dentro de ese resumen; máximo una captura por ítem.

## Contrato técnico verificado

- Semana sábado-viernes como el Plan Maestro.
- Sin librería de gráficos.
- Por confirmar: tabla del metrado programado por día del Plan Maestro (leer lienzo.ts y la migración que la crea).
- Migraciones: última en main 097; 098 a 102 son del plan de Informes; este plan usa 103 a 107. Verifica `ls db/` antes de escribir.
- Sin dependencias nuevas de interfaz (design.md §1 y §13).

## Skills que debe usar

- dataviz
- cerrar-tanda

## Comandos de verificación

- npx vitest run src/lib/cronograma
- npx tsc --noEmit
- npx eslint src/components/cronograma src/lib/cronograma

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra lo que tiene y escribe el traspaso. Una sola captura por ítem. Las migraciones, las credenciales y la verificación en vivo siguen el protocolo del plan: el Worker escribe las migraciones, NO las aplica.

## Cómo registra hallazgos y preguntas

Los hallazgos van a su resumen, en los cinco grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos, preguntas). Una pregunta de negocio o un conflicto con un flujo se devuelve al Orquestador en el momento; no sigue con el conflicto sin resolver. Credenciales: nunca leerlas ni mostrarlas.

## Criterios de salida

- Cifras cruzadas CG-82 en verde con el servicio de prueba.
- Todos los ítems de la tanda en Conforme u Observado con evidencia; ninguno a medias. Cierre con el Skill `cerrar-tanda`.
