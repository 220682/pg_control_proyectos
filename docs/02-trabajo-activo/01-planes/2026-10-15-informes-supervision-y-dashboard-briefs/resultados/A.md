# Resumen de cierre — Tanda A

## Tanda, rol y modelo

Tanda A, Ola 0, Worker 1, Sonnet, esfuerzo medio. Rama `local-worker-1`.

## Estado de los ítems

| ID | Estado | Evidencia | Causa |
|---|---|---|---|
| A1 | Conforme | `db/099_supervisor_operativo_a_cargo.sql` (aditiva, idempotente, reversa en comentario), línea 76 en `db/README.md`, `src/lib/proyectos/supervisor-operativo.ts`; `datos` usa `obtenerSupervisorACargo`; pruebas en `proyectos-supervisor-api.test.ts` | Migración revisada, no probada en base (no aplicada) |
| A2 | Conforme | Prueba de ruta: sin supervisor 400 con el mensaje; con los tres requisitos pasa 200; sin Plan Maestro 400 | |
| A3 | Conforme | Pruebas de ruta: cambiar, vaciar en planeación, vaciar en ejecución (400), rol equivocado (400), sin campo no toca | |
| A4 | Observado | `faltantesParaEjecucion` con prueba unitaria; `page.tsx` y `confirmar-transicion.tsx` muestran la lista | Sin captura: no se levantó la app |
| A5 | Conforme | `src/lib/dashboard/cargar-dashboard.ts` + prueba; la página lo usa | Diferencia menor: ahora el plan y los CNC se leen aunque el servicio no exista (el caso devuelve igual «no encontrado») |
| A6 | Conforme | `src/lib/curva-s/cargar-curva-s.ts`; snapshot de la respuesta tomado antes del cambio (`curva-s-route.test.ts`) y sin diferencias después; `curva-s.test.ts` verde | |
| A7 | Observado | `npm test` 118 archivos / 1189 pruebas verdes; `tsc --noEmit` limpio; `npm run lint` 9 errores y 22 avisos, idénticos sin mis cambios (preexistentes); `npm run build` (Turbopack) falla por el symlink de `node_modules` del worktree; `next build --webpack` verde | Lint preexistente; build solo funciona con `--webpack` en este worktree |
| A8 | Conforme | `puedeMedirSubcontratos` y `puedeVerInasistencias` + pruebas por los 13 roles | |

## Rama, commits y archivos tocados

`local-worker-1`: e65dcae (A1-A4) y c0dd874 (A5-A8), ambos con push y verificados con `git branch --contains`. Fuera de la lista del brief toqué `src/app/api/proyectos/route.ts` (una línea: la adjudicación guarda `supervisor_operativo_id` al crear el servicio). `db/095*` no existe en este worktree.

## Hallazgos

| ID | Grupo | Qué pasó | Destino propuesto |
|---|---|---|---|
| A-H1 | conflicto / pregunta | Servicios ya en `EJECUCION` sin miembro supervisor quedan con la columna nula; el brief dice que no retroceden. Un PATCH que no mande el campo no los afecta, pero cualquier edición desde el formulario (que manda `null`) sería rechazada con 400 hasta asignar a alguien | Pregunta al Orquestador |
| A-H2 | observación sobre la política | El brief no listaba `api/proyectos/route.ts`, pero sin tocarla los servicios nuevos nacen sin supervisor a cargo | Aceptar el cambio o indicarlo en el brief |
| A-H3 | mejora de trabajo | Turbopack no compila en worktrees con `node_modules` como symlink; usar `next build --webpack` | `docs/03-aprendizaje-continuo/` |

## Traspaso

Hecho: A1-A8. Falta: aplicar 099 (Orquestador) antes de desplegar, porque `datos`, adjudicación y transición dependen de la columna. Verificación: `npm test` verde, `npx tsc --noEmit` limpio, `npx next build --webpack` verde.

## Llamadas y contexto

Unas 35 llamadas.

## Skills revisados

`cerrar-tanda`: su secuencia se siguió en lo que corresponde al Worker (el commit de documentación lo hace el Orquestador).

## Fuentes de verdad revisadas

Ninguna actualizada. Pendiente para el Documentador: flujo 08 (transición a Ejecución exige supervisor a cargo) y flujo 14 nota ³.

## Corrección posterior (respuesta del Orquestador)

| ID | Estado | Evidencia | Causa |
|---|---|---|---|
| A3 (corregido) | Conforme | PATCH en EJECUCION con la columna ya nula y `null` da 200 sin tocar la columna; 400 solo si la columna tenía valor y se deja nula. Prueba de ruta nueva. `npm test` y `tsc` verdes. Commit nuevo en `local-worker-1`: 9ad0de7 (mensaje «A3: vaciar el supervisor solo es 400…») | Respuesta 2 del Orquestador; se aceptó también la línea en `api/proyectos/route.ts` |
