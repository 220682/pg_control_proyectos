# Brief de tanda C12 — Verificación en vivo en PS-0000

## Rol, modelo y tanda

CR-1 o Worker nuevo, nivel 2 (n2), Sonnet, esfuerzo Medio. Ola 5. Se lanza como «Worker CR-1 o Worker nuevo · C12». Plan: `2026-10-15-cronograma-gantt-linea-base-histogramas.md` (no lo leas completo; busca por ID de ítem).

## Ítems de la tanda

- **CG-120**: Criterios 1 a 3 en vivo: crear, programar, tres puertas.
- **CG-121**: Criterios 4 a 6: línea base, seguimiento, manual no cambia PR/Dashboard/Curva S.
- **CG-122**: Criterios 7 y 8: histogramas, PDF y Excel.
- **CG-123**: Criterio 10: tres paneles, cuatro estados, teclado, móvil solo lectura.

Decisiones ya resueltas (no se reabren): D1 avance manual no alimenta PR/Dashboard/Curva S; D2 seguimiento editable con Plan Maestro aprobado; D3 cuatro tipos de vínculo FC/CC/FF/CF con desfase ±; D4 calendario lunes-sábado con no laborables; D5 sin cascada de pronóstico.

## Rama, worktree y puerto

Rama: local-worker-4 con todo incorporado. Worktree: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\<rama>`. Puerto: el que fije el Orquestador. Empieza con `git merge main` en tu rama y confirma `git status` limpio. Un solo worktree activo.

## Qué leer, y qué no

- Punch List del plan (ítems CG-120 a CG-123 y los de cada criterio)
- docs/01-contexto-repositorio/04-pruebas-y-evidencia.md
- No leas: el plan completo, la evidencia ni el progreso completos, ni los 21 flujos.

## Qué puede trabajar

- Puede: Solo resultados/C12.md y evidencia
- NO puede: Código; si algo falla se devuelve al Orquestador
- Siempre fuera de límites: flujos de negocio, AGENTS.md, el estándar, el Spec, `src/lib/rdts/**`, `db/098` a `db/102`.

## Dónde deja su entrega y su evidencia

- Código: su rama.
- Resumen de cierre: `resultados/C12.md` (plantilla `12-resumen-de-cierre-de-tanda.md`).
- Evidencia dentro de ese resumen; máximo una captura por ítem.

## Contrato técnico verificado

- Cuentas de prueba: las usa el Orquestador; nunca leer ni mostrar credenciales. Servicio PS-0000 del Portafolio Practica.
- Migraciones: última en main 097; 098 a 102 son del plan de Informes; este plan usa 103 a 107. Verifica `ls db/` antes de escribir.
- Sin dependencias nuevas de interfaz (design.md §1 y §13).

## Skills que debe usar

- cerrar-tanda
- verificar-permisos-por-rol

## Comandos de verificación

- Playwright, una captura por ítem

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra lo que tiene y escribe el traspaso. Una sola captura por ítem. Las migraciones, las credenciales y la verificación en vivo siguen el protocolo del plan: el Worker escribe las migraciones, NO las aplica.

## Cómo registra hallazgos y preguntas

Los hallazgos van a su resumen, en los cinco grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos, preguntas). Una pregunta de negocio o un conflicto con un flujo se devuelve al Orquestador en el momento; no sigue con el conflicto sin resolver. Credenciales: nunca leerlas ni mostrarlas.

## Criterios de salida

- Checklist al 100 % antes de pasar a Victor (protocolo aprobado).
- Todos los ítems de la tanda en Conforme u Observado con evidencia; ninguno a medias. Cierre con el Skill `cerrar-tanda`.
