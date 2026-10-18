# Progreso — Notificaciones: estándar de avisos y apoyo al supervisor operativo

Plan: `docs/02-trabajo-activo/01-planes/2026-10-16-notificaciones-estandar-y-supervisor-operativo.md`. Evidencia: `docs/02-trabajo-activo/03-evidencia/2026-10-16-notificaciones-estandar-y-supervisor-operativo/`. Briefs y resúmenes de cierre: carpeta `...-briefs/` del plan.

Rama de código: `local-worker-7` (worktree `.worktrees/local-worker-7` en `py_control_proyectos_web`), creada desde `main` en `69ebf94` el 2026-10-17.

## Estado por tanda

| Tanda | Estado | Notas |
|---|---|---|
| T1A (cuentas, respaldo, cierre de avisos, datos) | Parcial | Cuentas: 2 de 6 (límite de correos de Supabase; pendiente repetir). Respaldo, cierre de los 18 avisos (SQL aplicado por Victor, comprobado en T1B) y datos de `PS-0000`: hechos |
| T1B (informes «cómo funciona hoy») | Hecha | Ciclo del RQ completo verificado en producción con el RQ de prueba `PS-0000-LL-SO-001` (queda en Atendido); informes en la carpeta de evidencia. Avisos de Victor: 18 en Atendido (comprobado) |
| T1C (maqueta de la bandeja) | Hecha y aprobada por Victor el 2026-10-18 («APPRUEBO», con mis recomendaciones: pastilla para OT y Entorno, «Solo Entorno», Devolver con borde rosa, texto completo al abrir, corregir solo ítems existentes) | `mockups/notificaciones-bandeja.html` (seis vistas); el Orquestador la abrió a 1440 px (vista Bandeja correcta, sin errores en consola); falta que Victor la apruebe antes de la parte visual de T3 y T5 |
| T2 (catálogo, módulo central, migración 108) | Hecha | Commits `cc44f47` y `814efb4`; 1754 pruebas en verde; migración 108 escrita, **sin aplicar** |
| T9 (perfil propio: contraseña, celular, correo) | Hecha | Commit `c067583`; 1787 pruebas en verde; capturas y pruebas en vivo en T7 |
| T4 (ciclo del RQ) | Hecha | Commits `69ce6aa` y `817e9d8`; 1829 pruebas en verde; lint con los 9 errores previos; verificada por el Orquestador |
| T6 | Hecha | Commits `bcba4da`, `853bf57`, `e3c4dfa`; 1883 pruebas en verde; lint con los 9 errores previos; verificada por el Orquestador. Sin la migración 108 los cierres automáticos de documentos y RDT no funcionan (solo registran error) |
| T3 | Hecha | Commits `041e9e4`, `b6017c2`, `9529853`; 1933 pruebas en verde; lint con los 9 errores previos; verificada por el Orquestador. Capturas y verificación en vivo en T7 |
| T5 | Hecha | Commits `83bd0f9`, `21a0e59`, `1d036ec`, `85626fd`; 2001 pruebas en verde; lint con los 9 errores previos; verificada por el Orquestador. Migración 109 escrita y **sin aplicar** (revisada por el Orquestador: aditiva e idempotente) |
| T7, T8 | Pendientes | |

## Registro

- 2026-10-17: Gate 1 aprobado por Victor. Worker git creó la rama y el worktree (verificado por el Orquestador con `git worktree list`).
- 2026-10-17: T1A. El `+` en el correo funciona. Cuentas creadas: `+logistica1` y `+logistica2`. Faltan `+jefeproy`, `+ofitec`, `+supop2` y `+admin2` (límite de correos por hora de Supabase).
- 2026-10-17: T2 verificada por el Orquestador (`git log`, `npm test`, `npm run lint`): lint con 9 errores previos en archivos que el plan no toca.
- 2026-10-17: Victor avisa que aplicó el SQL de cierre de avisos (T1-03).
- 2026-10-17: T4 y la maqueta T1C cortadas por el límite de uso de la sesión; reanudadas y terminadas. T4 verificada (`git log`, `npm test`, `npm run lint`).
- Hallazgos de T4 para el libro: pasos del RQ solo desde su estado de origen (409 si se repite o salta; integrar en flujo 05 y confirmar con Victor); T3/T7 deben llamar a `revisar` también con aviso Revisado y refrescar el estado con `recepcionado`; posible aviso doble al solicitante con rol de cola (decide Victor); pregunta abierta: si al corregir un RQ Devuelto se agregan y quitan ítems.
- 2026-10-17: T6 verificada (`git log`, `npm test`, `npm run lint`). Hallazgos de T6: vía 2 avisa si el responsable cambia a otra persona aunque ya fuera miembro; vía 3 avisa a cualquier rol, no solo a supervisores operativos (decide Victor); `cerrarAvisos` no cae a texto sin la migración 108 (el brief decía que sí); al corregir un RDT se cierran los avisos del anterior; flujos para el Documentador: 04, 06, 12, 13.
- 2026-10-18: Victor aplicó la migración 108 en Supabase; comprobada con su captura (`proyecto_id`, `evento` y `referencia_id` existen y admiten vacío). Quedan por aplicar la 109 (la escribe T5). Los 8 snapshots de Playwright con claves se borraron con su autorización; las claves siguen vigentes y se cambian al final de las pruebas.
- 2026-10-18: Decisiones de Victor sobre T6. (1) Si cambia el responsable de un servicio, se avisa al anterior (`servicio.retirado`) y al nuevo (`servicio.asignado`). (2) Al asignar o quitar servicios desde Usuarios, solo se avisa a quien corresponde: lo interpreto como supervisores operativos (Victor puede corregirlo). Ajuste «T6b» lanzado al Worker 7; los flujos 04, 06, 12, 13 y 14 se actualizan en T8. Falta su aprobación de la maqueta (T3 y T5 detenidas).
- 2026-10-18: T6b hecha y verificada por el Orquestador (commit `04739ec`, 1889 pruebas, lint con los 9 errores previos). Cambio de responsable avisa al anterior y al nuevo; en Usuarios solo a supervisores operativos. Los avisos `servicio.asignado` anteriores a T6b no se cierran solos (no tienen referencia).
- 2026-10-18: Victor aprobó la maqueta («APPRUEBO») tras mis cinco recomendaciones; lanzada T3. Brief de T3 escrito.
- 2026-10-18: T3 verificada (`git log`, `npm test`, `npm run lint`). Hallazgos de T3: (H2) el grupo del panel izquierdo (`registro-accesos.ts`) sigue llamándose «Proyecto»: decide Victor con los flujos 14 y 16; (H4) lista de avisos informativos a confirmar: `servicio.asignado`, `servicio.retirado`, `rq.*_solicitante` (aprobado, recepcionado, en almacén, atendido), `rdt.validado`, `informe.emitido`; `rq.comentario` y `rdt.rechazado` no son informativos; (H5) el alias `marcar-visto` no cierra informativos y ninguna pantalla lo usa; la tarjeta única por persona agrupa filas iguales creadas con menos de 30 s de diferencia. T5 lanzada.
- 2026-10-18: T5 verificada (`git log`, `npm test`, `npm run lint`) y migración 109 leída completa. Hallazgos de T5: (H1) en el consolidado de RQ no existe Aprobar hoy; Devolver está en el aviso y en el Status; Logística ve los Devueltos sin acciones; decide Victor si se agregan Aprobar/Devolver al consolidado; (H3) el estado Devuelto y sus permisos no están en ningún flujo (T8: flujos 05, 14, 16, `design.md` y Matriz de permisos); (H4) «Corregir y reenviar» son dos llamadas, reintentar es seguro; atender un aviso viejo de aprobación no cierra el aviso de devolución de un Devuelto.

## Pendientes de Victor

1. ~~Aplicar la migración 108~~ (hecha el 2026-10-18); falta la 109 (escrita por T5, lista para aplicar) antes de la verificación en vivo.
2. ~~Aprobar la maqueta de la bandeja~~ (aprobada el 2026-10-18).
3. Abrir el enlace de confirmación del cambio de correo (T7-09).
