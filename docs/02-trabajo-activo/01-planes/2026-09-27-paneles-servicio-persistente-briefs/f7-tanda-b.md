# F7-B · Documentación: flujo 14, artefacto «Matriz de permisos» y descargas

Lee primero `00-reglas-de-contexto.md`. Repo de trabajo: `D:\VICTOR\CLAUDE CODE\pg_control_proyectos`, rama `main` (documentación; no uses el worktree de la app).
Fase F7 · **Depende de:** F7-A cerrada; entrada de PL-155: lista de descargas de F0-A (PL-127). **Respuesta de Victor** sobre las 3 descargas propuestas (A12) y las 5 no listadas (A13), confirmadas o ajustadas en el artefacto.
**Punto de commit:** Commit en `main` de `pg_control_proyectos` con `git add` explícito, solo con autorización vigente de Victor.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-83 | La matriz derivada del registro coincide con la matriz base del flujo 14 (salvo lo que Victor haya aprobado); el Worker no reescribe la matriz base y deja anotado cómo repetir la comparación | Diff + comando o prueba usada |
| PL-100 | El flujo 14 aprobado (tablas 1 y 2) coincide con lo implementado; solo se toca si Victor decide algo nuevo (las tres descargas propuestas, A12), con consulta previa y sin dejar dos versiones conviviendo | Diff de `pg_control_proyectos` (vacío o con la decisión) |
| PL-149 | Política de trazabilidad: toda interfaz, acción, permiso o acceso nuevo o cambiado en esta tarea (por ejemplo las entradas del registro único, el modo "solo subir", el asistente, Ficha del servicio, Editar servicio, Editar checklist) figura en el artefacto «Matriz de permisos» y en el flujo 14 en la misma tarea; el Auditor lo comprueba | Diff del flujo 14 + captura del artefacto actualizado |
| PL-155 | Descargas encontradas por el Planner y no listadas en el artefacto (plantilla de cronograma, PDF de RDT estructurado, archivo de RDT subido, PDF individual de RQ, formato vacío PROM-GP-008; por verificar: adjuntos de RQ y documentos del checklist): el Worker confirma la lista, la entrega a Victor y, si Victor las decide, actualiza el artefacto y el flujo 14 en la misma tarea | Lista en la evidencia + respuesta de Victor |
| PL-156 | La sección «Descargas» del artefacto y la tabla 2 del flujo 14 quedan alineadas con lo decidido y con lo que el Worker implementó (registro de costos y consolidado RQ; las propuestas aprobadas o rechazadas), y el estado del artefacto deja de estar «En revisión» solo por decisión de Victor | Diff del flujo 14 + captura del artefacto |
| PL-173 | El flujo 14 ya no necesita las marcas "(por construir)" del grupo Recursos porque las 9 acciones existen; se verifica sin volver a escribir la matriz aprobada (solo se retira la marca si Victor lo pide, con consulta previa) | Nota en el progreso |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- El flujo 14 aprobado (tablas 1 y 2; `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\04-flujos-de-negocio\14-accesos-y-restricciones.md`, 19,7 KB) **no se reescribe**: solo se toca por una decisión nueva de Victor (descargas) o por entradas nuevas del registro, con consulta previa y sin dejar dos versiones conviviendo.
- **PL-100 / PL-83:** compara lo implementado y la matriz derivada del registro (F5-A, PL-56) con las tablas 1 y 2; deja anotado el comando o la prueba para repetir la comparación (verificado, no inventado).
- **PL-149:** toda interfaz, acción, permiso o acceso nuevo o cambiado en esta tarea (entradas del registro, «solo subir», Ficha del servicio, Editar servicio, Editar checklist, gestión de Recursos, el asistente como excepción) figura en el artefacto y en el flujo 14. **Por verificar por el Worker:** si su sesión tiene la herramienta `Artifact` (con `action: read` antes de publicar). Si no la tiene, entrega la lista exacta de filas al Orquestador, que publica.
- **PL-155/PL-156:** las 5 descargas de A13 (plantilla de cronograma, PDF de RDT estructurado, archivo de RDT subido, PDF individual de RQ, formato vacío PROM-GP-008) y las 3 propuestas de A12 (RDTs y listado RDTs, listado RQ, exportar DP): alinea la sección «Descargas» del artefacto y la tabla 2 con lo decidido y lo implementado. El estado del artefacto deja de estar «En revisión» **solo por decisión de Victor**.
- **PL-173:** las 9 acciones de Recursos «(por construir)» ya existen; solo se retira la marca si Victor lo pide (nota en el progreso).

## Qué NO hacer

- No reescribas la matriz aprobada. No publiques el artefacto sin `read` previo ni sin decisión de Victor.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
