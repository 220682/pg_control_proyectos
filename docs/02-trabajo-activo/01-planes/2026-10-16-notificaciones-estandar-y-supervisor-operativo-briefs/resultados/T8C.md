# Resumen de cierre — T8C (cierre documental tras la auditoría)

## Tanda, rol y modelo

Documentador · T8C · Sonnet 5.5 · esfuerzo medio. Aplica los puntos «APLICAR AHORA» 1 a 6 del informe del Auditor ([`04-auditoria/2026-10-16-notificaciones-estandar-y-supervisor-operativo.md`](../../../04-auditoria/2026-10-16-notificaciones-estandar-y-supervisor-operativo.md)) y la corrección V7 del flujo 05 pedida por el Orquestador. Fecha: 2026-10-18. Repositorio documental, rama `main`, sin push. La app se leyó en solo lectura (worktree `local-worker-7`).

## Estado de las tareas

| # | Tarea | Estado | Qué se hizo |
|---|---|---|---|
| 1 | Punch List al estado real | Hecha | 71 ítems: 65 Conforme, 5 Observado (T1-01, T7-09, T8-05, T8-06, T9-04) y 1 Sin verificar (T7-07), comprobado con un conteo automático. Los 44 ítems que pasaron a Conforme llevan al lado el enlace a su resumen de cierre y, cuando existe, la captura en vivo (`t7-*`, `t7b-*`). T7-09 y T9-04 llevan su causa |
| 2 | Encabezado, siguiente paso, esfuerzos, informe, progreso | Hecha | Línea «Estado» reescrita (`Auditado, a la espera del Gate 2`; no dice «cerrado»), Gate 2 sigue `pendiente`, tabla de equipo, «Siguiente paso» (pendientes de Victor y cierre), «Informe de Auditoría» enlazado, tabla de esfuerzos reales (todo Sonnet con esfuerzo medio, sin cambios de nivel, sin Max ni alto), registro de decisiones y enlaces. Progreso: T7 y T8 al día, filas nuevas T7fix, Auditoría y T8C, entradas de registro de T7fix, T7C, auditoría y T8C, y pendientes de Victor ampliados |
| 3 | Libro de hallazgos | Hecha | Mejoras M10 a M13 (T7B-H1, T7B-H7, roles temporales, T7C-H1) trasladadas al aprendizaje (puntos 9, 10 y 11). Reglas pendientes de decisión R18 (T7B-H5), R19 (T7B-H3), R20 (T3-H7) y R21 (T7B-H2). O4 (`puedeEditarPerfilExtendido`) como huérfano reportado a Victor. P-2 cerrada como `Descartada (cerrada: verificada en vivo)` con la evidencia de T7C. R14 precisado (Aprobar idempotente). Párrafo con los hallazgos que el Auditor clasificó como «no promover» |
| 4 | Flujo 13 | Hecha | Línea de remisión al aviso de asignación del responsable (flujo 04) y al cambio de responsable (flujo 08). El archivo no tenía cambios ajenos |
| 5 | Flujo 05, Aprobar repetido | Hecha | La línea del ciclo dice ahora que Recepcionado, En almacén y Atendido dan 409 si se saltan o repiten, y que Aprobar es idempotente (200, sin cambiar el estado ni avisar de nuevo) y solo da 409 sobre un Devuelto. Verificado en el código: ver abajo. No se cambió nada más del flujo |
| 6 | Evidencia suelta | Hecha | Se commitean `resultados/T7C.md` (modificado), `resultados/T7fix.md` (ya tenía seguimiento) y las capturas `t7c-09-p7`, `p8` y `p9` |
| 7 | `verificar-referencias.py` | Hecha | Ver «Verificación» |

## Verificación de la corrección del flujo 05 (solo lectura, worktree `local-worker-7`)

* `src/app/api/proyectos/[id]/requerimientos/[rqId]/estado/route.ts`: si el estado es DEVUELTO responde 409 (líneas 119 a 121); `derivar-logistica` responde siempre `200` con `{ ok: true, estado: 'APROBADO', ...resultado }` (línea 128); recepcionar, almacén y atender responden 409 si `cambiarEstadoRq` no cambia nada (líneas 131 a 136).
* `src/lib/requerimientos/derivar-logistica.ts`: si el RQ no está SOLICITADO devuelve `derivado: false` sin tocar nada (líneas 33 a 35), y el cambio es condicional «solo si sigue Solicitado» (líneas 37 a 50).
* Prueba que lo exige: `ciclo-rq-api.test.ts`, líneas 111 a 113 («aprobar dos veces no duplica»: 200 y un solo aviso `rq.aprobado_logistica`); y líneas 128 a 135 (repetir o saltar Recepcionado y Atender: 409).

## Commits

Ver `git log`: uno con la evidencia suelta del plan y otro con la documentación de T8C (plan, progreso, aprendizaje, flujos 05 y 13 y este resumen). Solo mis archivos; ningún archivo con cambios ajenos entró (los flujos 06, 09, 12, 14, 16, 18, 19, 20 y 22, `design.md`, mockups, `docs/02-trabajo-activo/README.md`, planes de otras tareas, `06-pruebas/`, material de apoyo y `login-ojo-contrasena.png` siguen sin commitear). Ningún archivo borrado.

## Lo que no pude hacer o queda para otros

* **Nada de lo que depende de Victor se tocó:** V1 (correo de T7-09), V2 (artefacto «Matriz de permisos»), V3 (limpieza de datos de prueba), decisiones R16 a R21 y P-1, P-3 a P-8, V6 a V10. El plan queda abierto y T7-07, T7-09, T8-05, T8-06 y T9-04 siguen sin cerrar.
* **Clasificación de R18 a R21:** el libro no tiene un apartado para defectos de interfaz; los registré en «Reglas de negocio» como `Pendiente de decisión` y los repetí en «Elementos postergados». Si Victor prefiere otro destino, se mueven.
* **Estado de P-2:** el libro no define un estado «Cerrada»; usé `Descartada` con la explicación entre paréntesis.
* **Índice de auditorías:** `04-auditoria/README.md` no lista el informe de este plan; el Auditor dejó dicho que lo agrega quien cierre el plan. No lo toqué.
* **Detalle fuera de alcance:** `03-evidencia/.../coherencia-flujos-codigo.md` (fila «Cada paso solo desde su estado de origen (409)») sigue sin la precisión de Aprobar idempotente; es evidencia de T8A y no se editó.
* **Nombre de una captura:** `t7c-09-p7-correo-anterior-rechazado.png` dice «rechazado», pero el resumen T7C indica que el correo anterior **sí entra** y que esa captura muestra el formulario aún cargando. Se commiteó tal cual (sin renombrar nada); conviene tenerlo en cuenta al leerla.
* **Reportado a Victor (huérfano O4):** `puedeEditarPerfilExtendido` (`src/lib/permisos/permisos.ts`, línea 555) ya no tiene uso en la app; solo su definición y su prueba. No se borró nada.

## Verificación

`python scripts/verificar-referencias.py`, ejecutado tras todas las ediciones: 46 archivos revisados, 0 huérfanos, 0 enlaces rotos y 2 menciones sin archivo (`convenciones-de-trabajo.md` en `01-contexto-repositorio/03-entorno-git-y-worktrees.md`, ajenas a este plan y ya reportadas por T8A y T8B). El conteo de la Punch List (71 ítems: 65 Conforme, 5 Observado, 1 Sin verificar) se comprobó con un script antes de guardar.

## Skills y fuentes de verdad revisadas

Skill `trasladar-hallazgos` y `cerrar-tanda` como guía; no se editó ninguna fuente de verdad por iniciativa propia: el único cambio de flujo con contradicción (05, Aprobar) lo ordenó expresamente el Orquestador a partir de V7.
