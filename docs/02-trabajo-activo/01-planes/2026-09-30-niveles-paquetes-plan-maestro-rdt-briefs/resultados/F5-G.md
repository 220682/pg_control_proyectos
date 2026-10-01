# Resultados F5-G · Corrección: aprobar el borrador de versión nueva

**Skills revisados:** `cerrar-tanda` (aplicado). Los demás no aplican (solo documentación; el Orquestador verifica permisos aparte).

## Decisión aplicada (Victor, 2026-10-01)
Aprobar el borrador que reemplaza una versión aprobada: administrador, jefe de proyectos y planner (como la primera aprobación). Crear la versión nueva (POST con motivo): solo administrador y jefe de proyectos (sin cambio).

## Qué cambió por documento — Conforme
- **Flujo 14:** fila «Gestionar Plan Maestro» ahora incluye aprobar el borrador de reemplazo; fila «Crear una versión nueva» ya no incluye aprobar; nota 9 reescrita (crear = 2 roles, aprobar = 3 roles, código coincide: POST `puedeCrearVersionPlanMaestro`, PATCH `puedeGestionarPlanMaestro`); punto por decidir 6 resuelto, «brecha de código pendiente» eliminada; frase de corrección fechada en la actualización 2026-10-01.
- **Flujo 20:** § «4. Versión nueva» añade quién aprueba; tabla resumen de permisos con fila nueva «Aprobar el borrador de una versión nueva».
- **Flujos 19, 16, 10, 09 y otros:** revisados con Grep («versión nueva», «reemplaza», aprobar): sin texto que choque; sin cambios.
- **Artefacto «Matriz de permisos»:** republicado (versión 10, misma URL): etiquetas y hints de «Gestionar Plan Maestro» y «Crear una versión nueva» corregidos, nota en «Puntos por decidir». Documento `matriz/actual` actualizado con `if_version` 46 -> 47: la marca «Aprobada» estaba en `true` y se dejó en `false` (Victor la vuelve a poner). Roles de las filas ya eran correctos (versionpm = admin, jp; gestpm = admin, jp, plnr).
- **Tabla en bloque del plan (solo lectura):** líneas 261 (F3B-6) y 418 (pregunta 7) dicen crear versión nueva = administrador y jefe de proyectos; no chocan. La línea 370 (F5D-4) y F5-D2 mencionan la brecha de aprobar: es historial, no se editó. No choca.

## Handoff
- Pendiente de otro paso: revertir F5-E en el código (el flujo ya lo da por hecho).
- Victor debe volver a marcar «Aprobada» en la matriz.
- Fuentes de verdad revisadas: flujos 14 y 20 y artefacto actualizados; ningún otro pendiente.

## Mejoras de trabajo / reglas de negocio / huérfanos
- Regla de negocio: la de arriba, ya escrita directo en los flujos 14 y 20. Sin mejoras ni huérfanos nuevos.
- Observación: el documento `matriz/actual` llegó con «Aprobada» en true pese a F5-D2; probablemente Victor la puso. Se quitó por instrucción.

**Llamadas:** ~17.
