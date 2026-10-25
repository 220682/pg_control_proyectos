# 04 — Notificaciones
> Lee si: la tarea toca la bandeja `/notificaciones`, los chips y la campana de avisos, el catálogo de eventos, a quién se avisa (y a quién no) cuando pasa algo con un RQ, un RDT, un servicio o un documento del checklist, o cuándo se cierra un aviso.

Un aviso informa que **algo pasó** o que **algo está pendiente**; no es un chat. La fuente de verdad del catálogo en código es `src/lib/notificaciones/catalogo.ts` de la app real: este flujo lo describe y, si difieren, manda el código y la diferencia se anota aquí (ver «Diferencias temporales»). Un aviso nuevo se agrega primero al catálogo; la app tiene una prueba que falla si hay un aviso en el código que no está en el catálogo, o al revés.

## Qué es un aviso

Cada aviso tiene: un **evento** del catálogo (su clave, por ejemplo `rq.devuelto`), un **texto**, un **tipo** (`DOCUMENTO_REQUERIDO`, `CHECKLIST_COMPLETO` o `MENSAJE`), un **destinatario** (una persona o un rol), un **servicio** o ninguno («Entorno»), un **grupo**, una **referencia** (el RQ, el RDT o el documento al que se refiere, para poder cerrarlo cuando se cumple lo que pedía) y un **estado**.

Se ven en la bandeja `/notificaciones` y en la bandeja de **Mi entorno**; la campana cuenta los pendientes de verdad. Mi entorno muestra solo las **recibidas** (no las enviadas): así gerencia y administración no ven el eco «RQ aprobado» que ellos mismos dispararon hacia Logística. Las dos pantallas reciben el mismo cambio y siguen siendo dos.

## Estados y cierre

Tres estados: **Pendiente** → **Revisado** (se abrió) → **Atendido** (cerrado). Abrir un aviso Pendiente lo pasa a Revisado. Un aviso se cierra de tres maneras:

* **A mano:** el destinatario lo atiende («Atender», con respuesta) o, en un aviso de aprobación de RQ, aprueba o devuelve desde él.
* **Solo, al abrirlo** (avisos informativos, solo los avisos **por usuario**): `servicio.asignado`, `servicio.retirado`, `rq.aprobado_solicitante`, `rq.recepcionado_solicitante`, `rq.en_almacen_solicitante`, `rq.atendido_solicitante`, `rdt.validado`, `restriccion.recepcionada`, `restriccion.atendida` e `informe.emitido`. No piden ninguna acción, así que abrirlos los cierra y la campana baja. **No** se cierran al abrir `rq.comentario` (el solicitante puede responder) ni `rdt.rechazado` (hay que corregir el RDT).
* **Solo, cuando se cumple lo que pedían** (por la referencia del aviso): por ejemplo, el aviso «falta subir…» se cierra al subir el documento, y los avisos de un RQ se cierran al cambiar su estado. Los avisos viejos que no tienen referencia se cierran por su texto.

La campana cuenta los avisos **Pendiente** recibidos por la persona, una vez por tarjeta.

## Por usuario o por rol

* **Aviso por rol = cola compartida de trabajo.** Llega a todas las personas del rol; la primera que lo atiende lo cierra para todas (por ejemplo, Logística 1 abre el aviso de un RQ aprobado y la campana de Logística 2 baja).
* **Aviso por usuario = informativo y solo de esa persona** (servicio asignado, RDT validado o rechazado, estado de su RQ, RQ devuelto, comentario sobre su RQ, documento del checklist asignado). Nadie más lo ve, aunque tenga el mismo rol.
* **Una persona con dos roles ve una sola tarjeta** por aviso (por ejemplo, un administrador que además es jefe de oficina técnica ve «RQ pendiente de aprobación» una vez). Al abrirla o atenderla se cierran las filas de todos sus roles.

## Servicio, N° OT y «Entorno»

Un aviso muestra una pastilla con el **N° OT** del servicio al que pertenece, o **«Entorno»** cuando no pertenece a ningún servicio (por ejemplo, un mensaje enviado desde fuera de un servicio). «Entorno» ya no cae en el primer servicio de la lista (antes aparecía como `PS-0000`). «Enviar mensaje» parte en «Entorno (sin servicio)» y solo se liga a un servicio si la persona lo elige.

**Quién puede enviar a un servicio:** enviar un mensaje ligado a un servicio exige tener ese servicio a cargo (el administrador pasa). Los avisos **a uno mismo** y los de **«Entorno»** no exigen servicio. Detalle de permisos en el [flujo 14](14-accesos-y-restricciones.md).

## Grupos y filtros

Cada aviso tiene un grupo, el mismo conjunto de 8 que los entornos de trabajo: **Jefatura**, Planificación, Costos, Supervisión operativa, Logística, Oficina Técnica, Administración y SSOMA. **«Jefatura» reemplaza al antiguo «Proyecto»** (decisión de Victor, 2026-10-16): lo usan el jefe de proyectos y el administrador, igual que el área JF del [flujo 02](02-usuarios.md). El título «Entorno · Proyecto» de Mi entorno pasa a «Entorno · Jefatura». Los avisos viejos guardados con «Proyecto» se leen como «Jefatura» sin tocar los datos; el enlace viejo `proyecto` sigue llevando a Jefatura.

El grupo de un aviso por rol sale del rol del destinatario, salvo «RQ pendiente de aprobación», que nace siempre en **Jefatura** sea cual sea el rol (así el mismo aviso no cambia de grupo según quién lo mire); el de un aviso por usuario lo indica quien avisa (ver la columna «Grupo» del catálogo). **La tarjeta unificada** (la persona con dos roles) muestra el grupo de la fila del rol de la persona; si coinciden varias, Jefatura primero. **Filtros de la bandeja `/notificaciones`:** dirección (recibidos, enviados o todos), N° OT (con la opción **«Solo Entorno (sin servicio)»**), estado, grupo y **«Tipo de aviso»**, con seis categorías: Requerimientos, RDT, Servicio, Checklist, Mensajes y Otros (esta última incluye todo aviso sin evento o con un evento que el catálogo no conoce). La lista muestra cada aviso recortado en una línea y, **al abrirlo, el texto completo**.

## Catálogo de eventos

«Cierre» dice cuándo se cierra el aviso; «Grupo» es el grupo con el que nace. Los textos entre comillas son las plantillas reales.

### Requerimientos (RQ)

El ciclo completo, sus estados y reglas están en el [flujo 05](05-rq.md).

| Evento | Quién lo dispara | A quién llega | Texto | Grupo | Cierre |
|---|---|---|---|---|---|
| `rq.pendiente_aprobacion` | Crear un RQ que no va directo a Logística; reenviar un RQ Devuelto ya corregido | Por rol: administrador, jefe de proyectos y jefe de oficina técnica | «Requerimiento {código} pendiente de aprobación — {servicio}» | Siempre Jefatura | Solo, al aprobar, devolver o derivar el RQ. «Atender» este aviso **aprueba** el RQ si el rol puede (no si está Devuelto) |
| `rq.nuevo_logistica` | Crear un RQ directo a Logística (lo crea un jefe de proyectos o de oficina técnica y nace Aprobado) | Por rol: Logística | «Nuevo requerimiento {código} — {servicio}» | Logística | Al abrirlo una persona de Logística: el RQ pasa a Recepcionado y el aviso se cierra para todas |
| `rq.aprobado_logistica` | Aprobar el RQ (derivarlo a Logística) | Por rol: Logística | «Requerimiento {código} aprobado — {servicio}» | Logística | Igual que el anterior: al abrirlo, Recepcionado |
| `rq.aprobado_solicitante` | Aprobar el RQ | Por usuario: el solicitante, si no es quien aprueba | «Requerimiento {código} ha sido aprobado por {nombre}» | Jefatura | Informativo: solo, al abrirlo |
| `rq.recepcionado_solicitante` | Logística abre el aviso del RQ aprobado (o pulsa Recepcionado en el consolidado) | Por usuario: el solicitante, si no es quien actúa | «Requerimiento {código} ha sido recepcionado por {nombre}» | Jefatura | Informativo: solo, al abrirlo |
| `rq.en_almacen_solicitante` | El RQ pasa a En almacén (todos sus materiales ya están en almacén) | Por usuario: el solicitante, si no es quien actúa | «Requerimiento {código} está en almacén» | Jefatura | Informativo: solo, al abrirlo |
| `rq.atendido_solicitante` | El RQ pasa a Atendido (todos sus materiales ya están atendidos) | Por usuario: el solicitante, si no es quien actúa | «Requerimiento {código} ha sido atendido por {nombre}» | Jefatura | Informativo: solo, al abrirlo |
| `rq.devuelto` | Devolver un RQ Solicitado con motivo | Por usuario: el solicitante (no se avisa si quien devuelve es él) | «Requerimiento {código} devuelto por {nombre}: {motivo}» | Jefatura | Solo, al reenviar el RQ corregido. No es informativo: pide **Corregir y reenviar** |
| `rq.comentario` | Comentar un RQ | Por rol: si comenta gerencia, Logística; si comenta Logística, jefe de proyectos y administrador. Además, por usuario: el solicitante, salvo que sea quien comenta | «Comentario en RQ {código}: {texto}» (el aviso recorta el comentario a 120 caracteres) | Según el rol; Jefatura para el solicitante | Lo atiende el destinatario, o solo, al cambiar el estado del RQ |

Al cambiar el estado de un RQ se cierran los avisos pendientes de ese RQ y se avisa al solicitante del paso nuevo; el aviso anterior nunca queda abierto. No se crea un aviso «atendida» al aprobador.

### Restricciones

Reglas y estados en el [flujo 22](22-informes-de-supervision.md), «Restricciones». Un fallo al avisar nunca deshace ni frena la acción principal.

| Evento | Quién lo dispara | A quién llega | Texto | Grupo | Cierre |
|---|---|---|---|---|---|
| `restriccion.nueva` | Crear una restricción, desde la pantalla Restricciones o al registrar un RDT con restricciones en sus actividades | Por rol: administrador, jefe de proyectos y jefe de oficina técnica | «Restricción {código} ({prioridad}) — {servicio}: {descripción}» | Jefatura | **Abrir el aviso recepciona la restricción** (la pasa a Recepcionado); el aviso sigue pendiente. Se cierra para todos cuando cualquiera de los tres la atiende, aunque no la haya recepcionado |
| `restriccion.recepcionada` | Recepcionar la restricción al abrir su aviso o con «Recepcionar» (no avisa si quien la recepciona es quien la creó) | Por usuario: quien la creó | «Restricción {código} recepcionada por {nombre}» | Supervisión operativa | Informativo: solo, al abrirlo |
| `restriccion.atendida` | Atender la restricción (no avisa si quien la atiende es quien la creó) | Por usuario: quien la creó | «Restricción {código} atendida por {nombre}» | Supervisión operativa | Informativo: solo, al abrirlo |

### RDT

El detalle del RDT está en el [flujo 06](06-rdt.md).

| Evento | Quién lo dispara | A quién llega | Texto | Grupo | Cierre |
|---|---|---|---|---|---|
| `rdt.nuevo` | Subir un RDT como archivo (PDF o foto) | Por rol: supervisor de administración | «RDT nuevo · {N° OT} · {autor} · {fecha}» | Administración | A mano |
| `rdt.registrado` | Registrar un RDT estructurado en pantalla (nuevo o corregido) | Por rol: quienes pueden validarlo (administrador, jefe de proyectos y jefe de oficina técnica) | «RDT registrado para validar · {N° OT} · {autor} · {fecha}» | Según el rol | Solo, al validar o rechazar el RDT, o al reemplazarlo por una corrección |
| `rdt.validado` | Validar un RDT (no avisa si quien valida es el autor) | Por usuario: el autor del RDT | «Tu RDT del {fecha} (turno {turno}) del servicio {N° OT} fue validado.» | Supervisión operativa | Informativo: solo, al abrirlo |
| `rdt.rechazado` | Rechazar un RDT (no avisa si quien rechaza es el autor) | Por usuario: el autor, con el motivo | «Tu RDT del {fecha} (turno {turno}) del servicio {N° OT} fue rechazado: {motivo}» | Supervisión operativa | Solo, al validarse el RDT o al reemplazarlo el autor por una corrección. Un rechazo nuevo reemplaza al anterior que siguiera pendiente |
| `rdt.recursos_sin_tarifa` | Validar un RDT con recursos sin tarifa en el presupuesto | Por rol: administrador y jefe de proyectos | «RDT validado con recursos sin tarifa en el presupuesto: {detalle}. Declara la equivalencia en «Equivalencias de cargos del servicio» (página del DP).» (cambio del 2026-10-21; cualquier fallo al avisar queda en el log) | Jefatura | A mano |

### Servicio

| Evento | Quién lo dispara | A quién llega | Texto | Grupo | Cierre |
|---|---|---|---|---|---|
| `servicio.asignado` | Quedar a cargo de un servicio, por tres vías: al **crearlo** con supervisor operativo; al **cambiar el responsable** en los datos del servicio; al **asignarle la OT desde Usuarios** (solo si la persona tiene el rol supervisor operativo y es nueva en el servicio). Nunca avisa a quien hace el cambio | Por usuario: la persona que queda a cargo | «Se te asignó el servicio {N° OT} — {nombre}.» | Supervisión operativa | Informativo: solo, al abrirlo; o, por referencia, cuando la persona deja de estar a cargo |
| `servicio.retirado` | Dejar de estar a cargo: al cambiar o quitar el responsable en los datos del servicio, o al quitarle la OT desde Usuarios (solo supervisor operativo y solo si de verdad la tenía). Nunca avisa a quien hace el cambio | Por usuario: la persona a quien se retira | «Ya no tienes a cargo el servicio {N° OT} — {nombre}.» | Supervisión operativa | Informativo: solo, al abrirlo |
| `servicio.documento_requerido` | Crear el servicio: un aviso por cada documento del checklist inicial | Por rol: el rol responsable de ese documento | «Servicio {N° OT}: falta subir "{documento}".» | Según el rol | Solo, al subir el documento, marcarlo completado o quitarlo del checklist |
| `servicio.documento_cierre` (reservado) | **Ya no se genera.** Antes se creaba al confirmar la transición de cierre, un aviso por documento de cierre | — | «Proyecto: falta subir "{documento}" para poder cerrar.» | — | A mano (solo quedan avisos viejos) |

**Cambio de responsable de un servicio (Victor, 2026-10-18):** se avisa **al anterior** (`servicio.retirado`) y **al nuevo** (`servicio.asignado`); el aviso de asignación pendiente del anterior se cierra. **Asignar o quitar servicios desde Usuarios** avisa solo a los supervisores operativos; los demás roles reciben el cambio sin aviso. Si el responsable no cambia, no se avisa a nadie.

`servicio.documento_cierre` se deja de generar porque el [flujo 12](12-checklist.md) oculta los documentos de fase CIERRE y nadie podía atender el aviso (decisión de Victor, 2026-10-17). La entrada se conserva en el catálogo, marcada como reservada, para reconocer y clasificar los avisos viejos que sigan en la base.

### Checklist

| Evento | Quién lo dispara | A quién llega | Texto | Grupo | Cierre |
|---|---|---|---|---|---|
| `checklist.documento_pendiente` | Editar el checklist del servicio: agregar, personalizar o reasignar un documento | Por usuario: el responsable asignado al documento | «OT {N° OT}: falta {subir / completar} "{documento}".» | Según el rol del responsable | Solo, al subir el archivo, marcarlo completado o quitarlo del checklist. Reasignar el responsable cierra el aviso del anterior y avisa al nuevo |
| `checklist.completo` | Subir o completar el último documento del checklist, o importar el DP | Por rol: jefe de oficina técnica | «Servicio {N° OT}: checklist completo, listo para avanzar de estado.» | Oficina Técnica | A mano: el jefe de oficina técnica lo atiende al avanzar el estado. Se reconoce por su tipo `CHECKLIST_COMPLETO`, no por el texto |

Los avisos anteriores decían «Servicio: falta…» sin N° OT; hoy todos llevan el N° OT. Ver el [flujo 12](12-checklist.md).

### Mensajes y otros

| Evento | Quién lo dispara | A quién llega | Texto | Grupo | Cierre |
|---|---|---|---|---|---|
| `mensaje.manual` | Una persona envía un mensaje desde «Enviar mensaje»; con servicio o sin él («Entorno») | Lo elige quien envía: un rol o una persona | Texto libre | El que indica quien envía | A mano |
| `informe.emitido` (reservado) | Emitir un informe de supervisión ([flujo 22](22-informes-de-supervision.md)) | Por usuario: cada miembro del servicio menos el autor | «{autor} emitio el informe {código} (v{versión}, {periodo}).» | Supervisión operativa | Informativo: solo, al abrirlo |

**`informe.emitido` está reservado:** el catálogo lo contempla (categoría «Otros») para que el aviso del plan de Informes se alinee al mismo estándar, pero hoy el aviso lo crea `notificar-emision.ts` sin pasar el evento y el catálogo lo deduce del texto. Pasarlo al módulo central de avisos le corresponde al plan de Informes. Regla vigente (Victor, 2026-10-15): al emitir un informe se avisa a los miembros del servicio, menos el autor, con un aviso de tipo MENSAJE.

## Contrato de la API

* `GET /api/notificaciones`: devuelve cada aviso con `evento`, `categoria`, `referencia_id`, el grupo ya normalizado a «Jefatura», el N° OT y el nombre del servicio (o nulos si es «Entorno»). Parámetros: `direccion` (`recibidos`, `enviados` o `todos`), `categoria` (una de las seis; un valor inválido se ignora) y `soloEntorno=true`. Una persona con dos roles recibe una tarjeta por aviso, con todas sus filas en `ids`.
* `GET /api/notificaciones/count`: cuenta tarjetas Pendiente recibidas (campana).
* `POST /api/notificaciones`: `proyectoId` es opcional («Entorno»); con servicio exige tenerlo a cargo, salvo avisos a uno mismo.
* `POST /api/notificaciones/[id]/revisar`: marca Revisado; cierra solo los informativos por usuario; si la persona es de Logística y el aviso es de un RQ aprobado, **recepciona el RQ** una sola vez (ver [flujo 05](05-rq.md)); si el aviso es `restriccion.nueva` y la persona puede atender restricciones, **recepciona la restricción** (ver [flujo 22](22-informes-de-supervision.md)). Responde `{ ok, recepcionado, estado }`.
* `POST /api/notificaciones/[id]/atender`: cierra con respuesta; sobre un aviso de aprobación de RQ y con un rol que aprueba, aprueba el RQ; sobre un aviso `restriccion.nueva` y con un rol que atiende restricciones, atiende la restricción.

## Datos

La migración `108` (aditiva): `proyecto_id` admite vacío («Entorno») y se agregan las columnas `evento` y `referencia_id` (texto) con índices. El grupo «Jefatura» se resuelve al leer; no se actualizan los avisos viejos. Sin la migración, los avisos se crean igual (sin evento ni referencia) y un aviso de «Entorno» falla hasta aplicarla.

## Diferencias temporales entre este flujo y el código

Ninguna abierta. El rótulo del grupo del panel izquierdo ya dice «Jefatura» en el código (la clave interna `notificaciones-proyecto` no cambia).

## Fuera de alcance

Correo, push o WhatsApp (la app no los tiene), el chat agéntico ([flujo 17](17-chat-agentico.md)) y cualquier cambio de quién puede qué fuera de lo que cada flujo indica.
