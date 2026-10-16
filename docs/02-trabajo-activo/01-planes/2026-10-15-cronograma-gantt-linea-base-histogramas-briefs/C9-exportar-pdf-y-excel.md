# Brief de tanda C9 — Exportar PDF y Excel

## Rol, modelo y tanda

CR-1, nivel 2 (n2), Sonnet, esfuerzo Medio. Ola 4. Se lanza como «Worker CR-1 · C9». Plan: `2026-10-15-cronograma-gantt-linea-base-histogramas.md` (no lo leas completo; busca por ID de ítem).

## Ítems de la tanda

- **CG-90**: PDF apaisado a la manera de MS Project (columnas, escala, barras base y seguimiento con %, resumen, hitos, flechas, hoy, leyenda, «Fecha: dd/mm/aa», paginación).
- **CG-91**: Opciones: solo base o base más seguimiento, rango de fechas, escala.
- **CG-92**: Excel de tres hojas: Cronograma, Gantt (celdas por semana), Histogramas.
- **CG-93**: La hoja «Cronograma» se vuelve a cargar sin errores.
- **CG-94**: PDF comparado a mano con CRON-PROMCOSER-AESA-001.pdf (una captura).

Decisiones ya resueltas (no se reabren): D1 avance manual no alimenta PR/Dashboard/Curva S; D2 seguimiento editable con Plan Maestro aprobado; D3 cuatro tipos de vínculo FC/CC/FF/CF con desfase ±; D4 calendario lunes-sábado con no laborables; D5 sin cascada de pronóstico.

## Rama, worktree y puerto

Rama: local-worker-4 (con CR-2 incorporado). Worktree: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web\.worktrees\<rama>`. Puerto: el que fije el Orquestador. Empieza con `git merge main` en tu rama y confirma `git status` limpio. Un solo worktree activo.

## Qué leer, y qué no

- src/lib/pdf/hoja.ts y parche-fuentes-pdfkit.ts (importar, NO editar)
- src/lib/rdts/exportador-pdf.ts (patrón de pdfkit, solo leer)
- src/app/api/cronograma/plantilla/route.ts (patrón exceljs)
- parser-excel.ts (columnas de carga)
- CRON-PROMCOSER-AESA-001.pdf
- No leas: el plan completo, la evidencia ni el progreso completos, ni los 21 flujos.

## Qué puede trabajar

- Puede: src/lib/cronograma/exportar-pdf.ts y exportar-excel.ts + tests
- Puede: src/app/api/cronograma/exportar/route.ts
- NO puede: hoja.ts, rdts/**, package.json (pdfkit y exceljs ya están)
- Siempre fuera de límites: flujos de negocio, AGENTS.md, el estándar, el Spec, `src/lib/rdts/**`, `db/098` a `db/102`.

## Dónde deja su entrega y su evidencia

- Código: su rama.
- Resumen de cierre: `resultados/C9.md` (plantilla `12-resumen-de-cierre-de-tanda.md`).
- Evidencia dentro de ese resumen; máximo una captura por ítem.

## Contrato técnico verificado

- Generación en servidor. Exportar: los 13 roles (propuesta del Spec, se concreta en C10).
- Migraciones: última en main 097; 098 a 102 son del plan de Informes; este plan usa 103 a 107. Verifica `ls db/` antes de escribir.
- Sin dependencias nuevas de interfaz (design.md §1 y §13).

## Skills que debe usar

- cerrar-tanda

## Comandos de verificación

- npx vitest run src/lib/cronograma
- npx tsc --noEmit
- npx eslint src/lib/cronograma src/app/api/cronograma

## Límites

80 llamadas como meta; a las ~60 deja de abrir frentes, cierra lo que tiene y escribe el traspaso. Una sola captura por ítem. Las migraciones, las credenciales y la verificación en vivo siguen el protocolo del plan: el Worker escribe las migraciones, NO las aplica.

## Cómo registra hallazgos y preguntas

Los hallazgos van a su resumen, en los cinco grupos (mejoras de trabajo, reglas de negocio, observaciones sobre la política, huérfanos, preguntas). Una pregunta de negocio o un conflicto con un flujo se devuelve al Orquestador en el momento; no sigue con el conflicto sin resolver. Credenciales: nunca leerlas ni mostrarlas.

## Criterios de salida

- PDF y Excel descargables desde la pantalla.
- Todos los ítems de la tanda en Conforme u Observado con evidencia; ninguno a medias. Cierre con el Skill `cerrar-tanda`.
