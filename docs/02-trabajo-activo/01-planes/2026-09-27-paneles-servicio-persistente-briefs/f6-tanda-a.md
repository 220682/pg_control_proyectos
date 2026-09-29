# F6-A · Verificación de los 13 roles contra la matriz y informe antes/después

Lee primero `00-reglas-de-contexto.md`. Repo: `D:\VICTOR\CLAUDE CODE\py_control_proyectos_web` · rama `local-worker-1` (worktree `.worktrees/local-worker-1`).
Fase F6 · **Depende de:** F5D-B cerrada (F1 a F5D completas).
**Punto de commit:** Solo si hay correcciones.
Las líneas citadas son referencias en `1942b01` (HEAD inicial de `local-worker-1`); si se movieron, busca por nombre con Grep. Lo marcado «por verificar» lo comprueba el Worker.

## Ítems de la tanda (texto del plan; estado inicial `Sin verificar`)

| ID | Qué debe cumplirse | Evidencia mínima |
|---|---|---|
| PL-43 | Verificación de los 13 roles con "Ver como" desde la cuenta A: para cada rol, el estado de cada chip del panel izquierdo, del derecho y de Mi entorno coincide con la matriz base del flujo 14 (leída del archivo, no copiada) | Tabla 13 roles × chips generada contra la matriz |
| PL-96 | Verificación de los 13 roles contra las tablas 1 y 2 del flujo 14 leídas del archivo (una fila = una interfaz o acción y sus APIs): el resultado del servidor y el estado del chip o botón coinciden columna por columna; el plan no duplica las tablas | Tabla generada contra el flujo 14 |
| PL-97 | Informe "qué cambió por rol respecto de la línea base de F0" contra la **tabla 1 y la tabla 2 completas**: rol × interfaz y rol × acción, antes y después. Cambian solo las celdas que el flujo 14 decide; cualquier otro cambio es un hallazgo. Victor revisa esta tabla | Tabla en la evidencia |

## Contrato técnico verificado (2026-09-29, solo lectura sobre `1942b01`)

- Fuente única: tablas 1 y 2 de `D:\VICTOR\CLAUDE CODE\pg_control_proyectos\docs\04-flujos-de-negocio\14-accesos-y-restricciones.md`, **leídas del propio archivo** (no se duplican). Genera con un archivo de prueba temporal de vitest la comparación rol × interfaz y rol × acción entre las funciones `permisos.ts` y las tablas parseadas del markdown; usa la matriz derivada del registro de F5-A para chips.
- **PL-43:** para cada uno de los 13 roles (con «Ver como», `POST /api/ver-como`), estado de cada chip del panel izquierdo, derecho y Mi entorno = matriz. Un solo `browser_evaluate` puede recorrer roles y leer `aria-disabled`/clases; confirma con `browser_snapshot` en una muestra (no 13 × N capturas). Tabla 13 roles × chips.
- **PL-96:** resultado del servidor y estado del chip o botón coinciden columna por columna con las tablas 1 y 2 (una fila = una interfaz o acción y sus APIs); llamadas sin efecto (403 por rol = rechazo; 404/400 = pasó). R28: alcance por OT del usuario real.
- **PL-97:** informe «qué cambió por rol respecto de la línea base de F0» contra las tablas 1 y 2 completas: rol × interfaz y rol × acción, antes (F0-C) y después. Cambian solo las celdas que el flujo 14 decide; cualquier otra diferencia es un hallazgo. Victor revisa esta tabla.
- Si hay hallazgos que exigen cambiar permisos más allá del flujo 14, no los corrijas: devuélvelos al Orquestador.

## Qué NO hacer

- No escribas datos. No cambies la matriz ni el flujo 14.
- No leas el plan completo (Grep por ID). Sin migraciones ni cambios en `db/`. Sin push ni merge. No cambies quién puede hacer qué salvo lo que este brief indica.
- Ante contradicción con un flujo escrito, permiso no decidido, acción destructiva o duda de negocio: detente en ese punto y devuelve la pregunta (opciones y recomendación) al Orquestador.

## Cierre

Actualiza solo tus filas de la Punch List (Grep del ID + Edit de esa fila), evidencia y handoff según `00-reglas-de-contexto.md`. Mensaje final: ítems cerrados, pendientes y número de llamadas.
