# 04 — Notificaciones
> Lee si: la tarea toca la bandeja `/notificaciones`, los chips de aviso, o a quién se notifica y a quién no (por ejemplo, al aprobar un RQ).


Bandeja `/notificaciones` y chips en Mi entorno.

Inbox de **Mi entorno**: solo **recibidas** (no enviadas). Así Geren/Admin no ven el eco “RQ aprobado” que ellos dispararon hacia Logística.

Al aprobar un RQ se notifica solo a `supervisor_logistica`. No se crea un aviso “atendida” al aprobador.

Tipos: DOCUMENTO_REQUERIDO, CHECKLIST_COMPLETO, MENSAJE.

Al emitir un informe de supervisión se avisa a los miembros del servicio, menos el autor, con una notificación de tipo MENSAJE (Victor, 2026-10-15; ver [flujo 22](22-informes-de-supervision.md)).
