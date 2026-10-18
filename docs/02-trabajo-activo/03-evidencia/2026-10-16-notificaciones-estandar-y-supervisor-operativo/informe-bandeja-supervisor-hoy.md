# Cómo funciona hoy la bandeja del supervisor operativo (T1-05)

Observado en producción (`main`) el 2026-10-17 con `jeyger22` (Supervisor operativo, «Lopez Caceres Loayza») y, para la prueba de dos personas del mismo rol, «PRUEBA Logística 1» y «PRUEBA Logística 2». Mismo RQ de prueba que en `informe-ciclo-rq-hoy.md`.

## A. Qué le llega y qué no al supervisor operativo

| Evento | ¿Le llega aviso? | Texto exacto / observación | Cómo se supo |
|---|---|---|---|
| Aprobación de su RQ | Sí | `Requerimiento PS-0000-LL-SO-001 ha sido aprobado por Victor Perez Contreras` | Visto en su bandeja |
| Logística recepciona su RQ | Sí | `Requerimiento PS-0000-LL-SO-001 ha sido recepcionado por PRUEBA Logística 1` | Visto en su bandeja (cerrado después) |
| RQ pasa a En almacén | Sí | `Requerimiento PS-0000-LL-SO-001 está en almacén` | Visto en su bandeja (cerrado después) |
| RQ Atendido | Sí | `Requerimiento PS-0000-LL-SO-001 ha sido atendido por PRUEBA Logística 1` | Visto en su bandeja, **PENDIENTE** (queda así hasta que él lo abra o atienda) |
| Cierre de sus avisos propios | Los avisos que él mismo originó («pendiente de aprobación», 3 filas) los ve como **enviados** y ATENDIDO con respuesta «Enviado a Logística» | | Visto en su bandeja |
| Comentario sobre su RQ | **No** | El comentario de Logística 2 (`Comentario en RQ PS-0000-LL-SO-001: …`) fue a Administrador y Jefe de Proyectos; el solicitante no figura. Si un comentario lo escribe alguien que no es de Logística, va a Logística. El solicitante nunca es destino | Probado (POST real) y leído su bandeja: no apareció; confirmado en `comentarios/route.ts` |
| RDT validado o rechazado | **No hay aviso** (por código: ninguna ruta de validación o rechazo de RDT crea notificación; el alta de RDT avisa solo al rol supervisor de Administración y la acumulación a PR avisa al administrador y jefe de proyectos) | | **No probado**: validar o rechazar RDT altera datos ajenos |
| Servicio asignado | **No hay aviso de asignación** | Sí recibe avisos de documentos faltantes del checklist (`DOCUMENTO_REQUERIDO`, p. ej. `Proyecto: falta subir "Acta de conformidad" para poder cerrar.`, pendiente desde el 2026-10-07) y de informes emitidos (`Victor Perez Contreras emitio el informe PS-0000-ID-… (vN, fecha).`) | Parcial: lo segundo visto; la asignación en sí **no probada** (alteraría datos ajenos) |
| Mensajes sueltos de otra persona | Sí | `hola`, `hola que tal` (enviados por el administrador) | Visto |

Contador de la campana de `jeyger22`: es el conteo de avisos PENDIENTE recibidos. Antes de la prueba 7, tras la aprobación 8, al final 8 (7 viejos pendientes + el «atendido»).

Observación: los 7 avisos viejos pendientes de `jeyger22` siguen sin cerrar (informes emitidos, mensajes de prueba y un documento requerido); ninguno se cerró por el ciclo del RQ.

## B. Dos personas del mismo rol (hallazgo H8)

Prueba con Logística 1 y Logística 2 (rol supervisor de Logística). Capturas en esta carpeta.

| Momento | Logística 1 | Logística 2 | Captura |
|---|---|---|---|
| Antes de que nadie abra el aviso | 1 aviso PENDIENTE (`Requerimiento PS-0000-LL-SO-001 aprobado — …`), campana 1 | El **mismo** aviso PENDIENTE, campana 1 | `t1b-bandeja-logistica1-1-antes.png`, `t1b-bandeja-logistica2-1-antes.png` |
| Después de que Logística 1 lo abre | Aviso REVISADO, campana 0 | Aviso REVISADO (mismo identificador `09d8a3e3`), campana 0 | `t1b-bandeja-logistica1-2-abierto.png`, `t1b-bandeja-logistica2-2-tras-abrir-log1.png` |
| Después de que Logística 1 recepciona y llega a Atendido | Aviso ATENDIDO (respuesta «Recepcionado»), campana 0 | Aviso ATENDIDO, respuesta «Recepcionado», campana 0 | `t1b-bandeja-logistica1-3-atendido.png`, `t1b-bandeja-logistica2-3-tras-atender-log1.png` |

Conclusión: **sí se refleja** el cambio de una persona en la otra. El aviso de rol es una sola fila: cuando una persona de Logística lo abre, a la otra se le apaga la campana sin haber hecho nada; cuando una lo atiende, la otra lo ve atendido, y no queda registro visible de quién lo abrió. Nota: el aviso se cierra al **recepcionar** (paso 3b), no al llegar a «Atendido»: «En almacén» y «Atendido» no tienen aviso para Logística.

Efecto sobre el RQ del supervisor operativo: quien recepciona, deja su nombre en «recepcionado por»; la otra persona de Logística no recibe aviso de que su colega lo hizo.

## C. No probado y por qué

- Aviso de RDT validado o rechazado al supervisor operativo: validar/rechazar RDT modifica datos de producción ajenos; por código no existe.
- Aviso por servicio asignado: asignar altera datos de otros usuarios.
- Comentario escrito por el propio supervisor operativo: solo se probó el de Logística 2 (el flujo del solicitante hacia Logística se lee en el código).
- Dos personas del rol supervisor operativo: falta la cuenta del segundo supervisor operativo (Supabase limitó los correos); el hallazgo H8 se probó con Logística, que comparte el mismo mecanismo de aviso de rol.
