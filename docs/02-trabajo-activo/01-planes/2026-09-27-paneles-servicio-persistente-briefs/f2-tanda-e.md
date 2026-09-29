# F2-E · Verificación transversal del servicio persistente y correcciones

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F2 · **Depende de:** F2-A a F2-D cerradas.
**Punto de commit:** Al cerrar la fase F2 (fin de esta tanda).
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-17 | Recargar (F5) y usar Atrás/Adelante conservan el servicio; pegar la URL en una pestaña nueva lo restaura | Secuencia de URL y capturas |
| PL-18 | Ninguna pantalla de PL-02 a PL-13 muestra "Selecciona un servicio…" con servicio elegido (no hay parpadeo del mensaje durante la carga) | Tabla ruta → resultado + captura de la carga |
| PL-67 | Durante la carga inicial con `?proyectoId=` en la URL no se ve el mensaje "Selecciona un servicio" ni un salto de layout | Grabación o capturas seguidas |
| PL-69 | Servicio sin datos (sin DP, sin cronograma o sin Plan Maestro): los paneles y sus chips se comportan igual y las pantallas muestran su estado vacío habitual | Captura |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- Recorrido: rutas de PL-02 a PL-13 (Cronograma, Paquetes, Plan Maestro, Crear/Status/Archivo/Consolidado RDTs, Status RQ, Consolidado RQ, Notificaciones, Mi entorno, Recursos, DP/PR/Dashboard/Curva S/Registro de costos) con cuenta A y B, SV1.
- **PL-18:** «Selecciona un servicio…» es el texto de `ContenidoHerramientas` (`WorkspaceShell.tsx` ~289-310). Tabla ruta → resultado con un solo `browser_evaluate` (recorre rutas y lee `textContent()`, no `innerText()`).
- **PL-67:** durante la carga con `?proyectoId=` no debe verse ese mensaje ni saltar el layout: observa con `MutationObserver` en `browser_evaluate` (o dos capturas seguidas como máximo). El fallback de `Suspense` es «Cargando…» (`WorkspaceShell` ~493-510).
- **PL-17:** recargar (F5), Atrás/Adelante y pegar la URL en una pestaña nueva conservan el servicio. **PL-69:** servicio sin DP, sin cronograma o sin Plan Maestro (elige uno con datos vacíos): paneles y chips iguales, pantallas con su estado vacío.
- Si algo falla, corrígelo aquí (poco código esperado) y vuelve a verificar. Cierra F2 con la evidencia de PL-01 a PL-21 completa.

## Qué NO hacer

- No abras alcance nuevo. Si una corrección exige cambiar el diseño del helper, devuelve la duda al Orquestador.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
