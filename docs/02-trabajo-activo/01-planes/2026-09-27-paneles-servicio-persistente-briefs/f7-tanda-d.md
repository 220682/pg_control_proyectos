# F7-D · Cierre documental: trazabilidad, traslado de mejoras, reglas y huérfanos, credenciales

Lee primero `00-reglas-de-contexto.md`. Repo de trabajo: `D:\VICTOR\CLAUDE CODE\pg_control_proyectos`, rama `main` (documentación; no uses el worktree de la app).
Fase F7 · **Depende de:** F7-A, F7-B y F7-C cerradas.
**Punto de commit:** Commit en `main` de `pg_control_proyectos` con `git add` explícito, solo con autorización vigente de Victor.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-81 | Cada contradicción de la lista se consultó a Victor antes de editar el flujo afectado y su respuesta quedó en el progreso | Progreso con pregunta y respuesta |
| PL-85 | Apartados "Mejoras (de trabajo)", "Reglas de negocio acordadas" y "Carpetas/archivos huérfanos" trasladados a sus destinos; huérfanos reportados a Victor sin borrar nada | Diff + mensaje |
| PL-86 | Ninguna credencial de las cuentas de prueba aparece en ningún archivo de ninguno de los dos repositorios | Búsqueda en el diff |
| PL-150 | Trazabilidad por flujo: cada fila de la tabla "Trazabilidad por flujo" del plan tiene su consulta a Victor, el flujo actualizado y el enlace a la sección donde quedó aplicado; ningún flujo o documento afectado queda sin actualizar ni con referencia a la versión anterior | Tabla completada en el progreso |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- **PL-150:** completa en el progreso la tabla «Trazabilidad por flujo» del plan: por cada fila, la consulta a Victor, el flujo actualizado y el enlace a la sección; ningún flujo afectado sin actualizar ni con referencia a la versión anterior. **PL-81:** cada contradicción se consultó antes de editar y su respuesta está en el progreso.
- **PL-85:** traslada los apartados del plan a su destino: «Mejoras (de trabajo)» → archivo nuevo en `docs/03-aprendizaje-continuo/` (con la lección de las tandas y la medición de `medicion.md`); «Reglas de negocio acordadas» → directo al flujo correspondiente (ya hecho en F7-A a C: solo verifica); «Carpetas/archivos huérfanos» → **reportados a Victor sin borrar nada** (`hist_nucleo/.env.local`, `hist_local-worker`, los dos `git stash`). Actualiza `docs/README.md` y `docs/02-trabajo-activo/01-planes/README.md`.
- **PL-86:** ninguna credencial de las cuentas de prueba en ningún archivo de ninguno de los dos repositorios. Comprobación **sin imprimir valores**: un script que lea en memoria los valores de la memoria del agente (`cuentas-prueba.md`, carpeta `memory` del proyecto en `%USERPROFILE%\.claude\projects`) y busque en `git diff`/árbol de ambos repos, mostrando solo el conteo de coincidencias. No hagas `grep`/`sed` sobre ese archivo (incidente del 2026-09-27).
- No se declara el plan cerrado: el Informe de Auditoría y el Gate 2 son de otros roles.

## Qué NO hacer

- No borres carpetas ni ramas. No cierres el plan ni escribas el Informe de Auditoría.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
