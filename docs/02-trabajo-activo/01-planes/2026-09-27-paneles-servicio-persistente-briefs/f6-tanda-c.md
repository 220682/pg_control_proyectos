# F6-C · Regresión de Recursos, tablas con scroll horizontal y asistente

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F6 · **Depende de:** F6-B cerrada.
**Punto de commit:** Solo si hay correcciones.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-65 | Las tablas largas conservan scroll horizontal y columnas fijas (Consolidado RDTs, Status de RDTs, Consolidado RQ, PR) | Captura de cada una |
| PL-117 | Regresión con el asistente ya como icono: pantallas con tablas y formularios largos no ganan scroll horizontal de página ni pierden filas visibles respecto de la línea base; portafolio y Mi entorno se ven como antes salvo la barra | Comparación con F0 |
| PL-170 | Regresión de lectura: Cargos y Equipos conservan filtro, orden y "Personalizar campos" que ya tenían, para los 13 roles, después de agregar los controles de alta, edición y baja | Comparación con la línea base de F0 |
| PL-171 | Regresión: Personal conserva su flujo de creación (validación de DNI único, cargo tomado del catálogo activo) después de agregar edición y baja | Comparación con la línea base de F0 |
| PL-172 | Por los dos lados con las dos cuentas: la cuenta A (o "Ver como" administrador y jefe de proyectos) crea, edita y desactiva en los cuatro recursos sin error; la cuenta B (o cualquier otro rol) no ve ningún control de mutación y sus llamadas directas (`POST`, `PATCH`, `PATCH` de desactivar) responden 403, sin cambiar ningún dato | Tabla 13 roles × las 12 acciones de Recursos |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- **PL-170/171:** compara con la línea base F0: Cargos y Equipos conservan filtro, orden y «Personalizar campos» (`src/lib/recursos/filtros.ts`) para los 13 roles; Personal conserva la validación de DNI único y el cargo tomado del catálogo activo (`api/recursos/personal/route.ts`).
- **PL-172:** por los dos lados con las dos cuentas: A (o «Ver como» administrador y JP) crea, edita y desactiva en los cuatro recursos; B (o cualquier otro rol) no ve ningún control de mutación y sus llamadas directas (`POST`, `PATCH`, `PATCH` de desactivar) responden 403 sin cambiar datos. **Datos reales:** aplica la misma regla de F5D (sin escribir hasta que el Orquestador confirme la autorización de Victor); el lado «A crea/edita» queda `Observado` con esa causa si no la hay. Tabla 13 roles × las 12 acciones de Recursos.
- **PL-65:** tablas largas con scroll horizontal y columnas fijas (Consolidado RDTs, Status de RDTs, Consolidado RQ, PR): una captura de cada una.
- **PL-117:** con el asistente como icono, las pantallas con tablas y formularios largos no ganan scroll horizontal de página ni pierden filas visibles frente a la línea base (LB-02, LB-04); portafolio y Mi entorno se ven como antes salvo la barra.

## Qué NO hacer

- No escribas datos reales sin la autorización indicada.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
