# Brief de tanda C10 — Permisos y validación final

## Rol, modelo y tanda

CR-1, nivel 2 (n2), Sonnet, esfuerzo Medio. Ola 4. Se lanza como «Worker CR-1 · C10». Plan: `2026-10-15-cronograma-gantt-linea-base-histogramas.md` (no lo leas completo; busca por ID de ítem).

## Ítems de la tanda

- **CG-100**: Funciones de permiso nuevas en permisos.ts (crear/editar planeación, editar seguimiento, exportar) y pruebas contra el flujo 14.
- **CG-101**: Skill verificar-permisos-por-rol sobre los 13 roles.
- **CG-102**: Cada escritura validada en servidor (permiso, servicio, tipos, límites).
- **CG-103**: tsc, eslint, vitest y npm run build en verde.

Decisiones ya resueltas (no se reabren): D1 avance manual no alimenta PR/Dashboard/Curva S; D2 seguimiento editable con Plan Maestro aprobado; D3 cuatro tipos de vínculo FC/CC/FF/CF con desfase ±; D4 calendario lunes-sábado con no laborables; D5 sin cascada de pronóstico.

## Rama, worktree y puerto

Rama: local-worker-4. Worktree: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\<rama>`. Puerto: el que fije el Orquestador. Empieza con `git merge main` en tu rama y confirma `git status` limpio. Un solo worktree activo.

## Qué leer, y qué no

- src/lib/permisos/permisos.ts líneas 365-390 y permisos.test.ts
- docs/04-flujos-de-negocio/14-accesos-y-restricciones.md (filas de cronograma y nota 8)
- .claude/skills/verificar-permisos-por-rol/
- Spec del plan, tabla «Usuarios / roles afectados»
- No leas: el plan completo, la evidencia ni el progreso completos, ni los 21 flujos.

## Qué puede trabajar

- Puede: src/lib/permisos/permisos.ts y su test (el plan de Informes lo edita también: git merge main antes y resolver choque trivial)
- Puede: Rutas de api/cronograma/** (usar las funciones nuevas)
- NO puede: Flujo 14 y el artefacto (son de C11); registro-accesos.ts
- Siempre fuera de límites: flujos de negocio, AGENTS.md, el estándar, el Spec, `src/lib/rdts/**`, `db/098` a `db/102`.

## Dónde deja su entrega y su evidencia

- Código: su rama.
- Resumen de cierre: `resultados/C10.md` (plantilla `12-resumen-de-cierre-de-tanda.md`).
- Evidencia dentro de ese resumen; máximo una captura por ítem.

## Contrato técnico verificado

- Hoy: ver cronograma 13 roles; subir/reemplazar: administrador, jefe de proyectos, planner; plantilla: 13 roles.
- Migraciones: última en main 097; 098 a 102 son del plan de Informes; este plan usa 103 a 107. Verifica `ls db/` antes de escribir.
- Sin dependencias nuevas de interfaz (design.md §1 y §13).

## Skills que debe usar

- verificar-permisos-por-rol
- cerrar-tanda

## Comandos de verificación

- npx vitest run
- npx tsc --noEmit
- npx eslint .
- npm run build

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra lo que tiene y escribe el traspaso. Una sola captura por ítem. Las migraciones, las credenciales y la verificación en vivo siguen el protocolo del plan: el Worker escribe las migraciones, NO las aplica.

## Cómo registra hallazgos y preguntas

Los hallazgos van a su resumen, en los cinco grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos, preguntas). Una pregunta de negocio o un conflicto con un flujo se devuelve al Orquestador en el momento; no sigue con el conflicto sin resolver. Credenciales: nunca leerlas ni mostrarlas.

## Criterios de salida

- Tabla de permisos observada = tabla del flujo 14 propuesta.
- Todos los ítems de la tanda en Conforme u Observado con evidencia; ninguno a medias. Cierre con el Skill `cerrar-tanda`.
