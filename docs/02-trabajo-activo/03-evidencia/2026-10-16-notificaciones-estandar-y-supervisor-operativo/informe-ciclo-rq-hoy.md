# Cómo funciona hoy el ciclo del RQ (T1-04)

Observado en producción (`py-control-proyectos-web.vercel.app`, rama `main`) el 2026-10-17 (hora Lima, 8:31 a 8:34 p. m.), con cuentas reales de prueba. RQ de prueba: `PS-0000-LL-SO-001` (id `9fff5fc7-7118-4ccc-aafe-5da8fe5ba826`), servicio `PS-0000`, una línea «PRUEBA T1B - ciclo RQ (no atender, dato de prueba)». Solicitante: `jeyger22` (Supervisor operativo). Aprobador: administrador. Logística: «PRUEBA Logística 1» y «PRUEBA Logística 2» (mismo rol, supervisor de Logística).

Cómo se leyó cada bandeja: `/api/notificaciones?direccion=todos` y `/api/notificaciones/count` (el número de la campana es solo el conteo de avisos en estado PENDIENTE recibidos por esa persona), más la pantalla `/notificaciones`. Los avisos «de rol» (para un rol, no para una persona) son **una sola fila compartida por todos los que tienen ese rol**.

Límite honrado: faltan las cuentas de jefe de proyectos, jefe de oficina técnica, segundo supervisor operativo y supervisor de administración. Por eso el aviso al «Jefe de Proyectos» y al «Jefe de Oficina Técnica» se comprobó solo por la lista de enviados del solicitante (no se vio su bandeja). El administrador tiene también el rol de jefe de oficina técnica, y por eso recibió dos copias del aviso de aprobación.

## Recorrido paso a paso

| Paso | Quién actúa | Qué se hizo | Avisos que se crean (texto exacto) | A quién llega | A quién NO llega | Avisos anteriores que se cierran | Campana después |
|---|---|---|---|---|---|---|---|
| 1. Crear | `jeyger22` (Supervisor operativo) | Crea el RQ (estado SOLICITADO, revisión de OT PENDIENTE) | `Requerimiento PS-0000-LL-SO-001 pendiente de aprobación — SERVICIO PRUEBA MARCOBRE 2026-10-07-19-33` (3 filas, una por rol destino) | Rol Jefe de Proyectos, rol Jefe de Oficina Técnica, rol Administrador. Administrador: 2 copias (por su rol de Jefe de Oficina Técnica y por el de Administrador) | Logística (ninguna de las dos), el propio solicitante (solo ve los 3 como «enviados» PENDIENTE) | Ninguno | Administrador 2, Logística 1 = 0, Logística 2 = 0, jeyger22 sin cambio (7) |
| 2. Aprobar | Administrador, desde el aviso: abre la tarjeta (el aviso pasa a REVISADO) y pulsa «Aprobado» | RQ pasa a APROBADO, revisión de OT REVISADO, «revisado por» = administrador | (a) a Logística: `Requerimiento PS-0000-LL-SO-001 aprobado — SERVICIO PRUEBA MARCOBRE 2026-10-07-19-33` (fila de rol); (b) al solicitante: `Requerimiento PS-0000-LL-SO-001 ha sido aprobado por Victor Perez Contreras` | (a) Logística 1 y Logística 2 (misma fila); (b) `jeyger22` | Jefe de Proyectos y Jefe de Oficina Técnica no reciben aviso de que ya se aprobó (solo se les cierra el anterior); el administrador (actor) no recibe aviso | Los 3 «pendiente de aprobación» (filas de Jefe de Oficina Técnica, Jefe de Proyectos y Administrador), todos con respuesta «Enviado a Logística». El cierre es por texto: a **toda** persona del proyecto cuyo aviso empiece por `Requerimiento <código>` | Administrador 0, Logística 1 = 1, Logística 2 = 1, jeyger22 = 8 |
| 3a. Logística abre el aviso | Logística 1 | Abre la tarjeta | Ninguno nuevo | — | — | Ninguno cerrado: el aviso de rol pasa de PENDIENTE a REVISADO **para las dos** personas de Logística | Logística 1 = 0 y Logística 2 = 0 (REVISADO ya no cuenta en la campana) |
| 3b. Recepcionar | Logística 1, botón «Recepcionado» de la tarjeta | RQ pasa a RECEPCIONADO; «recepcionado por» = Logística 1 | `Requerimiento PS-0000-LL-SO-001 ha sido recepcionado por PRUEBA Logística 1` | `jeyger22` | Logística 2 y el resto de Logística (no se les avisa de quién recepcionó); administrador y Jefe de Proyectos (no se enteran) | El aviso a Logística «aprobado — …» pasa a ATENDIDO con respuesta «Recepcionado». Se cierra para ambas personas | Logística 1 = 0, Logística 2 = 0, jeyger22 = 8 (deducido: se cierra «aprobado» y se crea «recepcionado»; no se miró su bandeja en este paso) |
| 4. En almacén | Logística 1, botón «En almacen» de la misma tarjeta (sigue ofrecida aunque su aviso ya estaba ATENDIDO) | RQ pasa a EN_ALMACEN | `Requerimiento PS-0000-LL-SO-001 está en almacén` (sin nombre de quien actúa) | `jeyger22` | Logística 2, administrador, Jefe de Proyectos | El «recepcionado por…» del solicitante pasa a ATENDIDO con respuesta «En almacén» | jeyger22 = 8 (deducido de la lista de enviados de Logística 1), Logística 0 |
| 5. Atendido | Logística 1, botón «Atendido» | RQ pasa a ATENDIDO | `Requerimiento PS-0000-LL-SO-001 ha sido atendido por PRUEBA Logística 1` | `jeyger22` | Logística 2, administrador, Jefe de Proyectos | El «está en almacén» pasa a ATENDIDO con respuesta «Atendido» | jeyger22 = 8 (7 viejos + el «atendido»; leído directamente al final; queda pendiente hasta que él lo abra o atienda, nada lo cierra solo), Logística 0 |

Pasos que no avisan a nadie: ninguno quedó totalmente mudo. Pero **abrir el aviso (3a) no avisa a nadie** y no deja constancia de quién lo vio. Logística nunca recibe aviso de «En almacén» ni de «Atendido» (el RQ avanza sin que la otra persona de Logística lo sepa), y administrador y jefes no reciben aviso de ninguna etapa después de aprobar.

## Hallazgos del ciclo (resumen)

1. El cierre de avisos es por **texto del mensaje** (`Requerimiento <código>%` en el servicio), no por vínculo con el RQ. Funciona hoy porque todos los mensajes empiezan igual, pero el aviso de Logística «Nuevo requerimiento …» (cuando crea alguien con derivación directa) **no** empieza por «Requerimiento» y no se cerraría. No se probó (solo se creó un RQ sin derivación directa).
2. Los avisos de rol son una sola fila compartida: lo que una persona de Logística hace sobre él (abrir, atender) lo ve cerrado la otra (ver `informe-bandeja-supervisor-hoy.md`).
3. El administrador recibió el mismo aviso dos veces (dos roles) y el sistema lo mostró como dos tarjetas idénticas, una REVISADO y otra PENDIENTE hasta que se aprobó.
4. Quien aprueba desde el aviso no pasa por una pantalla de motivo: un solo botón «Aprobado». «Rechazar» no existe en la tarjeta (no se buscó fuera de ella).
5. En la tarjeta, la barra de estados del aviso (Pendiente, Revisado, Recepcionado, En almacen, Atendido) y el estado del RQ avanzan juntos; los botones de la tarjeta siguen funcionando aunque el aviso ya esté ATENDIDO.
6. El aviso «Atendido» que llega al solicitante queda PENDIENTE para siempre si él no lo abre: hoy no hay cierre automático al finalizar el ciclo.

## Datos de prueba creados

- RQ `PS-0000-LL-SO-001` en `PS-0000`, estado final ATENDIDO.
- Un comentario «PRUEBA T1B…» de Logística 2 en ese RQ (ver informe de la bandeja del supervisor operativo), que dejó 2 avisos PENDIENTES (Administrador y Jefe de Proyectos).
- Nada se borró ni se tocó fuera de `PS-0000`.
