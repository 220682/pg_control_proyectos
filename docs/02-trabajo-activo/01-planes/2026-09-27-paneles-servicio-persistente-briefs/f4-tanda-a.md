# F4-A · Panel derecho estandarizado: servicio en todo chip, deshabilitado por permiso

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F4 · **Depende de:** F3-C cerrada (chip compartido y marca informativo/acción).
**Punto de commit:** Al cerrar la tanda, en `local-worker-1`.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-30 | Dentro de SV1, cada chip del panel derecho cuya pantalla usa selector de OT (Crear RDTs, Subir RDTs, Crear RQ, Consolidado RDTs, Cronograma, Paquetes de Trabajo, Plan Maestro) abre con SV1 ya elegido en el selector | Tabla chip → valor del selector |
| PL-31 | Dentro de SV1, cada chip cuya pantalla filtra por N° OT (Status de RDTs, Archivo de RDTs, Requerimiento, Consolidado RQ) abre con el filtro = SV1 | Tabla chip → filtro |
| PL-32 | Dentro de SV1, cada chip con ruta de servicio (DP, PR, Dashboard, Curva S, Registro de costos) abre con SV1 | Tabla chip → URL |
| PL-33 | Recorrido completo de los 7 grupos del panel derecho y de "Accesos rápidos": ningún chip cuya pantalla existe queda sin el servicio (una fila por chip, sin excepciones) | Tabla completa de chips |
| PL-34 | El valor preseleccionado se puede cambiar y la pantalla responde (selector o filtro) | Captura antes y después |
| PL-41 | Cuenta B: en el panel derecho los chips que su rol no puede usar aparecen deshabilitados con título (según la decisión 3 aprobada; si se decide mantener el comportamiento actual, el ítem se reescribe en el Gate 1) | Tabla + captura |
| PL-42 | Cuentas A y B: Mi entorno conserva los mismos chips que en la línea base (A3); su estado habilitado o deshabilitado sigue la matriz base (cambia respecto de la línea base solo donde la matriz lo decide) y ahora envían el servicio | Comparación con la línea base de F0 |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- `ContenidoHerramientas` (`WorkspaceShell.tsx` ~289): `AccesosRapidos` (`PanelSecciones.tsx` ~26) con `CHIPS_ACCESO_RAPIDO` y `GruposAccordion` (~77) con los grupos de `NAV_PROYECTO` sin «Proyecto». Ambos derivan del registro (F1).
- Regla: dentro de un servicio, **todo** chip con pantalla existente abre esa pantalla con el servicio elegido (resultado esperado 6, sin excepciones): selector de OT (Crear RDTs, Subir RDTs, Crear RQ, Consolidado RDTs, Cronograma, Paquetes de Trabajo, Plan Maestro), filtro N° OT (Status de RDTs, Archivo de RDTs, Requerimiento, Consolidado RQ) o ruta de servicio (DP, PR, Dashboard, Curva S, Registro de costos). El valor preseleccionado se puede cambiar (PL-34).
- Decisión 3 (recomendación B vigente): el panel derecho pasa a «visible y deshabilitado» para lo no autorizado (mismo patrón que el chip compartido de F3-A; hoy no mira permisos y el clic rebota a Mi entorno). El `permiso` es el del registro (funciones vigentes hasta F5B).
- E3: «Status de RDTs» = `/rdts/status`; «Archivo de RDTs subidos» = `/rdts/listado` en todos los paneles.
- Mi entorno (`EntornoTrabajoGrupo.tsx`, `herramientasPorGrupo`): mismo conjunto de chips que la línea base LB-03 (A3), con estado según la matriz vigente y ahora enviando el servicio (PL-42).
- **PL-33:** tabla completa de chips (7 grupos + Accesos rápidos), una fila por chip. Prefiere una **prueba unitaria** que enumere cada acceso con `requiereServicio` y afirme el `?proyectoId=`/preselección, más confirmación en navegador de una muestra por mecanismo (no chip por chip con capturas).

## Qué NO hacer

- No cambies quién puede usar cada pantalla (F2B/F5B/F5C). No toques el asistente (F4B).
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
