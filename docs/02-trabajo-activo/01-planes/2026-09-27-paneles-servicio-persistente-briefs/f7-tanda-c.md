# F7-C · Documentación: resto de flujos (03, 05, 06, 08, 09, 11, 12, 15, 20, 21, README) y coherencia

Lee primero `00-reglas-de-contexto.md`. Repo de trabajo: `D:\VICTOR\CLAUDE CODE\pg_control_proyectos`, rama `main` (documentación; no uses el worktree de la app).
Fase F7 · **Depende de:** F7-A y F7-B cerradas y **respuestas de Victor** a C16 a C21, C23 a C26, C29 a C34, C36 y V6 (C35 ya resuelta el 2026-09-29).
**Punto de commit:** Commit en `main` de `pg_control_proyectos` con `git add` explícito, solo con autorización vigente de Victor.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-82 | Flujos 16, 01 y 14 (y 03, 05, 06, 11, 15, 21 si aplica) actualizados y coherentes con lo implementado, sin reglas pegadas al final | Diff de `pg_control_proyectos` |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

Sin la respuesta registrada de Victor a una contradicción, no edites ese flujo: devuélvela al Orquestador. Destinos (tabla «Trazabilidad por flujo» del plan; Grep por ese título):
- `03-entorno.md` (C16, C23, C26): tabla de chips por rol con las tablas 1 y 2; «Panel derecho». `05-rq.md` (C17, C26, C29): Status y Consolidado; «Borrar RQ» (administrador y JP); creación (13 roles) y estado (logística y administrador). `06-rdt.md` (C18, C24, C30): pantallas `/rdts/status` (Status) y `/rdts/listado` (Archivo), quién ve, sube, valida y borra.
- `08-programa-portafolio-proyecto.md` (C31, C32, C33): adjudicar y crear (administrador, JP, JOT), borrar y archivar (administrador y JP; JOT pierde), transición (los tres). `09-importar-dp.md` y `12-checklist.md` (V6): una línea con quién importa el DP y quién edita el checklist (enlace a la tabla 2).
- `11-dashboard.md` (C19, **C35 resuelta**): ubicación del chip por panel; el interruptor Parcial/Completo lo activan los roles con datos económicos de la matriz (`puedeVerEconomia`); que los demás lo vean fijo en Parcial es del plan futuro (`planes-futuros.md`). `15-cronograma.md` (C20, C25), `20-plan-maestro.md` (C25, C36), `21-curva-s.md` (C19, C25): quién ve y valida. `README.md` (C34): regla transversal «Borrado administrador» y sus citas en 05, 06 y 08.
- **PL-82:** al terminar, verifica la coherencia de los flujos 16, 01, 14, 03, 05, 06, 11, 15, 21 (y 08, 09, 12, 20, README) con lo implementado: sin reglas pegadas al final ni referencias a la versión anterior. Los flujos «Revisados» (02, 04, 07, 10, 13, 17, 18, 19) no se tocan salvo lo indicado.

## Qué NO hacer

- No edites el flujo 14 ni el artefacto. Un plan cerrado no se edita.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
