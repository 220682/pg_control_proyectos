# Brief de tanda C2 — API de edición y editor de tabla

## Rol, modelo y tanda

CR-1, nivel 3 (n3), Sonnet, esfuerzo Medio. Ola 2. Se lanza como «Worker CR-1 · C2». Plan: `2026-10-15-cronograma-gantt-linea-base-histogramas.md` (no lo leas completo; busca por ID de ítem).

## Ítems de la tanda

- **CG-20**: API bajo /api/cronograma/actividades, /dependencias y /calendario: validación en servidor (permiso, alcance al servicio, ciclo, tipo, calendario) y rechazo de planeación con Plan Maestro aprobado (usa planMaestroAprobado).
- **CG-21**: Editor de tabla: árbol de 14 px plegable y las columnas del Spec; Playwright.
- **CG-22**: Cambiar duración o predecesora mueve las siguientes; crear 15 actividades en 3 niveles.
- **CG-23**: Borrador con guardado parcial, que sobrevive a recargar.
- **CG-24**: Personalizar campos (componente existente) y virtualización desde 60 filas.
- **CG-25**: Editor de días no laborables que recalcula.
- **CG-26**: Hito: el tipo Hito del editor es la fuente (decidido por Victor, 2026-10-15). La pantalla de Paquetes lo muestra atenuado, solo lectura, con la etiqueta «◆ Hito»; ya no se marca desde Paquetes. Primero ubica el archivo de Paquetes y `src/app/api/cronograma/hitos/route.ts`, anota en tu resumen cómo funciona hoy la marca y cómo tratas los hitos ya marcados; si exige cambiar datos existentes, devuélvelo al Orquestador antes de seguir.

Decisiones ya resueltas (no se reabren): D1 avance manual no alimenta PR/Dashboard/Curva S; D2 seguimiento editable con Plan Maestro aprobado; D3 cuatro tipos de vínculo FC/CC/FF/CF con desfase ±; D4 calendario lunes-sábado con no laborables; D5 sin cascada de pronóstico.

## Rama, worktree y puerto

Rama: local-worker-4. Worktree: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\<rama>`. Puerto: el que fije el Orquestador. Empieza con `git merge main` en tu rama y confirma `git status` limpio. Un solo worktree activo.

## Qué leer, y qué no

- src/app/api/cronograma/route.ts (GET líneas 46-166, patrón de permisos y admin client), src/lib/proyectos/plan-maestro-aprobado.ts
- src/components/ui/FormularioCronograma.tsx y PersonalizarCampos.tsx
- src/components/plan-maestro/LienzoPlanMaestro.tsx (patrón de borrador y tres paneles)
- src/lib/permisos/permisos.ts líneas 365-390
- docs/04-flujos-de-negocio/15-cronograma.md y 20-plan-maestro.md §6
- design.md §3
- No leas: el plan completo, la evidencia ni el progreso completos, ni los 21 flujos.

## Qué puede trabajar

- Puede: src/app/api/cronograma/actividades|dependencias|calendario/route.ts (nuevos)
- Puede: src/components/cronograma/EditorCronograma.tsx y TablaCronograma.tsx (nuevos)
- Puede: src/app/(workspace)/cronograma/page.tsx (pasa a montar el editor)
- Puede: src/lib/cronograma/* (solo importar el motor de C1)
- Puede (solo CG-26): src/app/api/cronograma/hitos/route.ts y el componente de Paquetes que muestra el hito, únicamente para volverlo de solo lectura y atenuado
- NO puede: src/lib/rdts/**, permisos.ts (las funciones nuevas son de C10: usa puedeSubirCronograma por ahora)
- NO puede: registro-accesos.ts (el chip ya existe)
- NO puede: Flujos y design.md
- Siempre fuera de límites: flujos de negocio, AGENTS.md, el estándar, el Spec, `src/lib/rdts/**`, `db/098` a `db/102`.

## Dónde deja su entrega y su evidencia

- Código: su rama.
- Resumen de cierre: `resultados/C2.md` (plantilla `12-resumen-de-cierre-de-tanda.md`).
- Evidencia dentro de ese resumen; máximo una captura por ítem.

## Contrato técnico verificado

- La página hoy es solo CabeceraPagina + FormularioCronograma, con puedeVerCronograma/puedeSubirCronograma.
- Tablas por servicio con proyecto_id; clientes con service role en servidor (patrón de route.ts).
- Servidor recalcula con el motor de C1; no confía en fechas del navegador.
- Migraciones: última en main 097; 098 a 102 son del plan de Informes; este plan usa 103 a 107. Verifica `ls db/` antes de escribir.
- Sin dependencias nuevas de interfaz (design.md §1 y §13).

## Skills que debe usar

- cerrar-tanda

## Comandos de verificación

- npx vitest run src/app/api/cronograma src/lib/cronograma
- npx tsc --noEmit
- npx eslint src/components/cronograma src/app/api/cronograma
- Playwright en el puerto de la rama: crear 15 actividades

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra lo que tiene y escribe el traspaso. Una sola captura por ítem. Las migraciones, las credenciales y la verificación en vivo siguen el protocolo del plan: el Worker escribe las migraciones, NO las aplica.

## Cómo registra hallazgos y preguntas

Los hallazgos van a su resumen, en los cinco grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos, preguntas). Una pregunta de negocio o un conflicto con un flujo se devuelve al Orquestador en el momento; no sigue con el conflicto sin resolver. Credenciales: nunca leerlas ni mostrarlas.

## Criterios de salida

- API y tabla funcionando contra una base con 103 aplicada (la aplica Victor); si no está aplicada, probar con pruebas de ruta y dejarlo escrito.
- Todos los ítems de la tanda en Conforme u Observado con evidencia; ninguno a medias. Cierre con el Skill `cerrar-tanda`.
