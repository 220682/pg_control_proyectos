# Brief de tanda C7 — APU por partida (107)

## Rol, modelo y tanda

CR-2, nivel 3 (n3), Sonnet, esfuerzo Medio. Ola 1 (independiente de C1). Se lanza como «Worker CR-2 · C7». Plan: `2026-10-15-cronograma-gantt-linea-base-histogramas.md` (no lo leas completo; busca por ID de ítem).

## Ítems de la tanda

- **CG-70**: Migración 107 dp_partida_recursos (cargo con HH por unidad, equipo con HM por unidad). NO se aplica.
- **CG-71**: parser-apu.ts devuelve por partida el consumo de cada cargo y equipo; Σ HH por partida = hh_und_partida.
- **CG-72**: La importación del DP guarda esos datos sin cambiar lo demás (regresión).
- **CG-73**: Evaluar releer el APU guardado de un DP aprobado, sin cambiarlo, para completar HM; decisión escrita.
- **CG-74**: Servicios sin HM por partida: «sin dato», no cero.

Decisiones ya resueltas (no se reabren): D1 avance manual no alimenta PR/Dashboard/Curva S; D2 seguimiento editable con Plan Maestro aprobado; D3 cuatro tipos de vínculo FC/CC/FF/CF con desfase ±; D4 calendario lunes-sábado con no laborables; D5 sin cascada de pronóstico.

## Rama, worktree y puerto

Rama: local-worker-6 (nueva, autorizada por Victor el 2026-10-15; la crea el Orquestador desde main antes de lanzarte). Worktree: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\<rama>`. Puerto: el que fije el Orquestador. Empieza con `git merge main` en tu rama y confirma `git status` limpio. Un solo worktree activo.

## Qué leer, y qué no

- src/lib/dp/parser-apu.ts completo (272 líneas)
- db/004_dp.sql (dp_partidas, dp_recursos)
- db/097_semilla_recursos_4_servicios.sql (cabecera)
- docs/04-flujos-de-negocio/09-importar-dp.md (APU)
- Ruta de importación del DP en src/app/api/dp/ (por confirmar el archivo)
- No leas: el plan completo, la evidencia ni el progreso completos, ni los 21 flujos.

## Qué puede trabajar

- Puede: db/107_dp_partida_recursos.sql
- Puede: src/lib/dp/parser-apu.ts y su test
- Puede: Ruta de importación (solo guardar lo nuevo)
- Puede: db/README.md (tu línea)
- NO puede: Cronograma (src/lib/cronograma/** y api/cronograma/**), src/lib/rdts/**, db/098-106
- NO puede: dp_partidas.hh_und_partida (no cambia)
- Siempre fuera de límites: flujos de negocio, AGENTS.md, el estándar, el Spec, `src/lib/rdts/**`, `db/098` a `db/102`.

## Dónde deja su entrega y su evidencia

- Código: su rama.
- Resumen de cierre: `resultados/C7.md` (plantilla `12-resumen-de-cierre-de-tanda.md`).
- Evidencia dentro de ese resumen; máximo una captura por ítem.

## Contrato técnico verificado

- dp_partidas.hh_und_partida existe; no hay HM por partida; dp_recursos solo trae totales por cargo y equipo del servicio.
- Hecho del Orquestador: el parser calcula HH por partida sumando cuadrilla × cantidad (verificar).
- Migraciones: última en main 097; 098 a 102 son del plan de Informes; este plan usa 103 a 107. Verifica `ls db/` antes de escribir.
- Sin dependencias nuevas de interfaz (design.md §1 y §13).

## Skills que debe usar

- cerrar-tanda

## Comandos de verificación

- npx vitest run src/lib/dp
- npx tsc --noEmit
- npx eslint src/lib/dp

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra lo que tiene y escribe el traspaso. Una sola captura por ítem. Las migraciones, las credenciales y la verificación en vivo siguen el protocolo del plan: el Worker escribe las migraciones, NO las aplica.

## Cómo registra hallazgos y preguntas

Los hallazgos van a su resumen, en los cinco grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos, preguntas). Una pregunta de negocio o un conflicto con un flujo se devuelve al Orquestador en el momento; no sigue con el conflicto sin resolver. Credenciales: nunca leerlas ni mostrarlas.

## Criterios de salida

- Cifras cruzadas Σ HH = hh_und_partida en el DP de prueba.
- Todos los ítems de la tanda en Conforme u Observado con evidencia; ninguno a medias. Cierre con el Skill `cerrar-tanda`.
