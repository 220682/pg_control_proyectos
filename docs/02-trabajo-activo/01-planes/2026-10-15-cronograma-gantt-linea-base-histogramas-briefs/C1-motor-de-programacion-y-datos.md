# Brief de tanda C1 — Motor de programación y datos (migración 103)

## Rol, modelo y tanda

CR-1, nivel 3 (n3), Sonnet, esfuerzo Medio. Ola 1 (en paralelo con C7). Se lanza como «Worker CR-1 · C1». Plan: `2026-10-15-cronograma-gantt-linea-base-histogramas.md` (no lo leas completo; busca por ID de ítem).

## Ítems de la tanda

- **CG-10**: Migración db/103_cronograma_programacion.sql: tablas cronograma_dependencias (actividad, predecesora, tipo FC/CC/FF/CF, desfase_dias entero con signo) y servicio_calendario (dias laborables de la semana, lista de no laborables); columnas fijada_a_mano y origen (archivo/dp/manual) en cronograma_actividades. Aditiva, RLS, reversa en comentario. NO se aplica.
- **CG-11**: calendario.ts: sumar/restar días laborables lunes-sábado con no laborables. Prueba: 12 días del 6 al 19/08 saltan los domingos.
- **CG-12**: predecesoras.ts: lee 5, 5FC+2, 5CC, 5FF-1, 5CF; rechaza lo ilegible con motivo.
- **CG-13**: programacion.ts: los cuatro vínculos con desfase ± calculan la fecha; actividad fijada no se mueve. Un test por tipo.
- **CG-14**: Ciclos rechazados con motivo (lista de actividades del ciclo).
- **CG-15**: Resumen: comienzo=min hijas, fin=max, duración; hito duración 0.
- **CG-16**: edt.ts: numeración automática del EDT por sangría (sube, baja, inserta).

Decisiones ya resueltas (no se reabren): D1 avance manual no alimenta PR/Dashboard/Curva S; D2 seguimiento editable con Plan Maestro aprobado; D3 cuatro tipos de vínculo FC/CC/FF/CF con desfase ±; D4 calendario lunes-sábado con no laborables; D5 sin cascada de pronóstico.

## Rama, worktree y puerto

Rama: local-worker-4. Worktree: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\<rama>`. Puerto: el que fije el Orquestador. Empieza con `git merge main` en tu rama y confirma `git status` limpio. Un solo worktree activo.

## Qué leer, y qué no

- db/036_cronograma.sql, db/072_paquetes_trabajo.sql (columna requiere_partidas), db/README.md (formato de entradas)
- src/lib/cronograma/tipos.ts y vinculos.ts
- Spec del plan, sección «Datos, API, migraciones» (buscar por ese título)
- No leas: el plan completo, la evidencia ni el progreso completos, ni los 21 flujos.

## Qué puede trabajar

- Puede: db/103_cronograma_programacion.sql (nuevo)
- Puede: src/lib/cronograma/calendario.ts, predecesoras.ts, programacion.ts, edt.ts y sus .test.ts (nuevos)
- Puede: src/lib/cronograma/tipos.ts (ampliar)
- Puede: db/README.md (solo tu línea)
- NO puede: src/lib/rdts/**, db/098 a 102, parsers existentes, api/cronograma/route.ts (es de C2)
- Siempre fuera de límites: flujos de negocio, AGENTS.md, el estándar, el Spec, `src/lib/rdts/**`, `db/098` a `db/102`.

## Dónde deja su entrega y su evidencia

- Código: su rama.
- Resumen de cierre: `resultados/C1.md` (plantilla `12-resumen-de-cierre-de-tanda.md`).
- Evidencia dentro de ese resumen; máximo una captura por ítem.

## Contrato técnico verificado

- cronograma_actividades: id uuid, proyecto_id, orden, edt, nombre, tipo ('TAREA','HITO','RESUMEN'), duracion_dias, fecha_inicio, fecha_fin, predecesoras/sucesoras texto, dp_enlazado, completo, motivos (db/036). Se conservan predecesoras y sucesoras como texto de origen.
- Última migración en main: 097; la 102 es del plan de Informes: tú usas 103. Vuelve a mirar ls db/ antes de escribir.
- Motor puro (sin base de datos), reutilizable en servidor y navegador.
- Migraciones: última en main 097; 098 a 102 son del plan de Informes; este plan usa 103 a 107. Verifica `ls db/` antes de escribir.
- Sin dependencias nuevas de interfaz (design.md §1 y §13).

## Skills que debe usar

- cerrar-tanda

## Comandos de verificación

- npx vitest run src/lib/cronograma
- npx tsc --noEmit
- npx eslint src/lib/cronograma

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra lo que tiene y escribe el traspaso. Una sola captura por ítem. Las migraciones, las credenciales y la verificación en vivo siguen el protocolo del plan: el Worker escribe las migraciones, NO las aplica.

## Cómo registra hallazgos y preguntas

Los hallazgos van a su resumen, en los cinco grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos, preguntas). Una pregunta de negocio o un conflicto con un flujo se devuelve al Orquestador en el momento; no sigue con el conflicto sin resolver. Credenciales: nunca leerlas ni mostrarlas.

## Criterios de salida

- Pruebas del motor en verde, migración escrita y revisada (no aplicada), resumen en resultados/C1.md.
- Todos los ítems de la tanda en Conforme u Observado con evidencia; ninguno a medias. Cierre con el Skill `cerrar-tanda`.
