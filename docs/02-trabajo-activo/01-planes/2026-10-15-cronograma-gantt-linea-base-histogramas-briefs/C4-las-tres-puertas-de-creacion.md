# Brief de tanda C4 — Las tres puertas de creación

## Rol, modelo y tanda

CR-1, nivel 2 (n2), **Haiku** (Victor pidió Haiku para las tareas simples; brief cerrado que reutiliza parsers existentes; si no logra cerrar la tanda se suspende y el Orquestador pide a Victor aprobar Sonnet), esfuerzo Medio. Ola 2. Se lanza como «Worker CR-1 · C4». Plan: `2026-10-15-cronograma-gantt-linea-base-histogramas.md` (no lo leas completo; busca por ID de ítem).

## Ítems de la tanda

- **CG-40**: Desde el DP: una tarea por partida, niveles como actividades, enlace por WBS (PS-0000).
- **CG-41**: Desde archivo: los tres archivos de prueba abren en el editor y sus fechas quedan fijadas.
- **CG-42**: Predecesoras legibles quedan estructuradas; las ilegibles se informan; aviso si las fechas difieren.
- **CG-43**: A mano desde cero con numeración de EDT por sangría.
- **CG-44**: Aviso de lo que se perdería al reemplazar (incluye lo editado) y bloqueo con Plan Maestro aprobado. Decidido por Victor: crear desde el DP sobre un cronograma con actividades **reemplaza con aviso**, igual que la carga de archivo.

Decisiones ya resueltas (no se reabren): D1 avance manual no alimenta PR/Dashboard/Curva S; D2 seguimiento editable con Plan Maestro aprobado; D3 cuatro tipos de vínculo FC/CC/FF/CF con desfase ±; D4 calendario lunes-sábado con no laborables; D5 sin cascada de pronóstico.

## Rama, worktree y puerto

Rama: local-worker-4. Worktree: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\<rama>`. Puerto: el que fije el Orquestador. Empieza con `git merge main` en tu rama y confirma `git status` limpio. Un solo worktree activo.

## Qué leer, y qué no

- src/app/api/cronograma/route.ts POST (líneas 250-615)
- src/lib/cronograma/parser-excel.ts, parser-pdf.ts, niveles.ts, informe.ts
- src/components/ui/FormularioCronograma.tsx
- docs/04-flujos-de-negocio/15-cronograma.md (mapa de niveles, recarga bloqueada)
- Archivos de prueba: docs/06-material-de-apoyo/Informacion para pruebas/
- No leas: el plan completo, la evidencia ni el progreso completos, ni los 21 flujos.

## Qué puede trabajar

- Puede: Parsers (devolver predecesoras estructuradas con C1/predecesoras.ts)
- Puede: src/app/api/cronograma/desde-dp/route.ts (nuevo)
- Puede: POST de route.ts (guardar dependencias y origen)
- Puede: FormularioCronograma.tsx como puerta «archivo»
- NO puede: niveles.ts salvo ampliación mínima; src/lib/rdts/**; pantalla de Paquetes
- Siempre fuera de límites: flujos de negocio, AGENTS.md, el estándar, el Spec, `src/lib/rdts/**`, `db/098` a `db/102`.

## Dónde deja su entrega y su evidencia

- Código: su rama.
- Resumen de cierre: `resultados/C4.md` (plantilla `12-resumen-de-cierre-de-tanda.md`).
- Evidencia dentro de ese resumen; máximo una captura por ítem.

## Contrato técnico verificado

- Un cronograma por servicio (proyecto_cronograma.proyecto_id).
- Las pruebas existentes (parsers, cronograma-get.test.ts) siguen en verde.
- La carga llama recalcular_pr_fechas_base al terminar (route.ts:601): se conserva.
- Migraciones: última en main 097; 098 a 102 son del plan de Informes; este plan usa 103 a 107. Verifica `ls db/` antes de escribir.
- Sin dependencias nuevas de interfaz (design.md §1 y §13).

## Skills que debe usar

- cerrar-tanda

## Comandos de verificación

- npx vitest run src/lib/cronograma src/app/api/cronograma
- npx tsc --noEmit
- npx eslint src/lib/cronograma src/app/api/cronograma

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra lo que tiene y escribe el traspaso. Una sola captura por ítem. Las migraciones, las credenciales y la verificación en vivo siguen el protocolo del plan: el Worker escribe las migraciones, NO las aplica.

## Cómo registra hallazgos y preguntas

Los hallazgos van a su resumen, en los cinco grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos, preguntas). Una pregunta de negocio o un conflicto con un flujo se devuelve al Orquestador en el momento; no sigue con el conflicto sin resolver. Credenciales: nunca leerlas ni mostrarlas.

## Criterios de salida

- Los tres archivos de prueba abren; informe de predecesoras no legibles visible.
- Todos los ítems de la tanda en Conforme u Observado con evidencia; ninguno a medias. Cierre con el Skill `cerrar-tanda`.
