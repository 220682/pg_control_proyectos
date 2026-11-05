# 26 — Fuente-WhatsApp
> Lee si: la tarea toca el apartado «Fuente-WhatsApp» (el grupo de WhatsApp del servicio, la conversación por día con sus integrantes, el resumen diario, los contactos por celular), el panel de **Notas** de Restricciones-Notas y su vigencia, el origen «WhatsApp» de una restricción con su emisor, o el script local que envía el grupo a la app.

Origen: plan [Fuente-WhatsApp](../02-trabajo-activo/01-planes/2026-10-25-fuente-whatsapp.md) (pedido de Victor el 2026-10-25; paso 2 de la reestructuración Fuentes / Gestión documentaria). Hermana de [Fuente-Gmail](23-estado-del-servicio.md) y de Fuente-Drive (pendiente). Quién puede cada acción: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md), nota 23; la lista de pantallas, en el [flujo 16](16-paneles.md). **Estado (2026-11-05): rediseñada y publicada; ya no se clasifican mensajes (ver «La conversación del día»). Grupo «Villa Fase 2» con 643 mensajes del 22/10 al 05/11. Falta la copia de archivos a R2.**

## Qué es

Una pantalla por servicio (`/proyectos/{id}/fuente-whatsapp`, chip «Fuente-WhatsApp» en el grupo **Seguimiento** desde el 2026-11-05; antes en Planificación) que muestra lo que dice **el grupo de WhatsApp de ese servicio**: **solo extrae la conversación**, con quién escribió cada mensaje, y al costado un **resumen diario** de lo resaltante (Victor, 2026-11-05: «ya no será para elegir si un chat es para colocar en algún lugar, solo extrae la conversación con su nombre, identificación de quién lo hizo, y al costado un resumen diario de lo resaltante»). Hoy hay **un solo grupo** («Villa Fase 2», servicio «Facilidades de Villa de Ejecución Fase 2»).

## De dónde salen los mensajes

Teléfono de Victor → **puente de WhatsApp** en su PC (`mcp_whatsapp`, vinculado como dispositivo con **su propio número**, **solo lectura**) → **script local** (`scripts/whatsapp/enviar_grupo.py` de la app, solo librería estándar de Python) → la app (`POST /api/fuente-whatsapp/ingresar`, protegida con el secreto `WHATSAPP_INGRESO_SECRETO`, sin sesión).

* **Privacidad:** el script toma **únicamente** el grupo configurado; la consulta filtra por el código del grupo y ningún otro chat del teléfono sale del PC. La app, además, **rechaza** cualquier lote cuyo grupo no esté registrado y activo en un servicio.
* **Registro del grupo:** administrador o jefe de proyectos escriben el código del grupo (termina en `@g.us`) en la pantalla; un grupo no puede estar en dos servicios. El grupo se puede pausar.
* **Idempotente:** cada mensaje se guarda una sola vez (por su id en WhatsApp). La misma información repetida por el mismo emisor en el mismo minuto entra ya **descartada**. Un fallo a medio envío se reintenta sin duplicar.
* **Envío automático:** una tarea de Windows en el PC de Victor ejecuta el script **cada 10 minutos** (solo con la sesión de Windows abierta y el puente corriendo); el secreto, el último mensaje enviado y el registro viven en una carpeta privada del PC, fuera de los repositorios.
* **Riesgos asumidos:** el puente usa una conexión **no oficial**; el teléfono debe abrir WhatsApp al menos cada ~14 días; el PC debe estar encendido para recibir. **El puente debe estar corriendo:** el 2026-11-05 se halló apagado desde el 03/11 (no arranca solo al reiniciar el PC) y se volvió a encender; la pantalla muestra el «último envío del PC» para notarlo.

## La conversación del día

Todos los mensajes del grupo se guardan tal como llegan (texto, fotos, documentos, audios). La pantalla tiene tres partes:

* **Integrantes que escribieron:** todos los que escribieron alguna vez en el grupo, el que más escribe primero, con su **nombre, cargo y empresa** (o «Usuario del sistema», «Personal de obra», «Contacto de WhatsApp», «Sin identificar») y cuántos mensajes lleva. Al pasar el mouse se ve su celular y su último mensaje. Quien gestiona hace clic en un contacto externo para completar nombre, cargo y empresa (los usuarios y el personal se editan donde viven).
* **Conversación (izquierda):** los mensajes de **un día** (de Lima), en orden de hora; por defecto el último día con mensajes. Cada uno muestra **nombre** de quien lo escribió, su cargo y empresa, su celular (o «Número oculto por WhatsApp»), la **hora** y el texto (los muy largos se recortan con «Ver todo»); una foto, video, documento o audio se rotula con 📎, y los **archivos seguidos de una misma persona** (sin texto, a menos de 15 minutos uno de otro) van en **una sola tarjeta** («📎 5 fotos», con la hora de inicio y fin). Se cambia de día con «Día anterior», «Día siguiente» o la lista de días (cada uno con su cantidad de mensajes).
* **Resumen del día (derecha, fijo al bajar):** ver abajo.

La pantalla **se actualiza sola cada hora** (y con el botón «Actualizar»); si se está viendo el último día, sigue al día de hoy. Ya **no hay** bandeja «Por revisar» ni botones para convertir un mensaje en pedido de campo, nota o archivo (Victor, 2026-11-05). Las restricciones y notas que ya se crearon desde WhatsApp antes del cambio se conservan con su origen; las restricciones nuevas se crean en Restricciones-Notas.

## El resumen del día

Lo arma la app **con reglas, sin IA** (la app debe funcionar sola para cualquiera), a partir de las palabras de los mensajes del día:

* **Cabecera:** cuántos mensajes hubo, de qué hora a qué hora, y cuántas fotos o videos y documentos.
* **Quiénes escribieron:** cada persona con sus mensajes, fotos y documentos del día.
* **Lo resaltante, por tema**, en este orden (un mensaje va al primer tema que le calza; no se tienen en cuenta tildes ni mayúsculas):

| Tema | Palabras que lo reconocen (ejemplos) |
|---|---|
| **Problemas e incidentes** | problema, incidente, accidente, falla, malogrado, derrame, «botando», riesgo, «reportados», paralizado, stand by, demora, retraso, suspendido, «no llegó / no hay / no había / no se pudo», observado, rechazo, lluvia, clima, viento |
| **Pedidos y faltantes** | falta, necesitamos, se requiere, solicito, urgente, pendiente, vence, «su apoyo / su soporte», enviar, traer, comprar, cotizar, material, herramienta, EPP, RQ, pedido |
| **Seguridad (SSOMA)** | charla, ATS, PETS, IPERC, EPP, SSOMA, seguridad, permiso de trabajo, inspección, simulacro, inducción, alcohol, capacitación |
| **Avances y trabajos hechos** | avance, terminado, culminado, liberado, vaciado, instalación, ejecutado, realizado, entregado, montaje, soldadura, pintado, excavación, relleno, limpieza, colocación, encofrado, armado, perforación, demolición, fabricación; «se da inicio»; un metrado con unidad (12.5 ml, 3 m³, 80 %) |
| **Coordinaciones** | reunión, coordinar, visita, programa, cronograma, mañana, hoy, cliente, supervisor, turno, horario, movilidad, bus, camioneta, abastecimiento, traslado, fotocheck, garita, ingreso, salida, mantenimiento |

* Los saludos, «ok», «gracias» y textos de menos de 15 letras **no** entran al resumen. Cada tema muestra hasta **6 mensajes** (los más largos, que dicen más, en orden de hora) como «hora — nombre: texto», recortados a ~220 letras, y «y N más en la conversación» si hay más; un clic lleva al mensaje en la conversación.
* Si el día no tiene nada de eso, lo dice («solo saludos o fotos»).

## Quién es el emisor

Un mensaje trae el celular de quien lo escribió. Para saber quién es **no se duplica** lo que ya existe (Victor, 2026-10-25): se busca el celular, comparando los **últimos 9 dígitos** (WhatsApp lo manda con el código de país), en este orden:

1. **Usuarios del sistema** (perfiles): nombre y cargo.
2. **Personal de obra** (`recursos_personal`): nombre y cargo.
3. **Contacto externo de WhatsApp**: solo si no está en ninguna de las dos, se crea en la tabla propia de contactos (celular, nombre, cargo, empresa) con el nombre que muestra WhatsApp; quien gestiona completa nombre, cargo y empresa desde la lista de integrantes.

**Autor del historial (Victor, 2026-10-25: «buscar el celular y asignar el nombre automáticamente»):** el historial que WhatsApp sincroniza al vincular el puente no dice quién escribió en la tabla de mensajes (el puente guarda el código del propio grupo), pero el puente sí guarda el **autor de cada mensaje** en otra de sus tablas (`whatsmeow_message_secrets`). El script lo toma de ahí y, si WhatsApp lo identifica con un **código interno (LID)**, lo cambia por su **celular** con la tabla de equivalencias del puente (`whatsmeow_lid_map`). El **nombre que muestra WhatsApp** sale de los contactos del puente (`whatsmeow_contacts`). Con el celular, la app busca en el catálogo como se explicó arriba (usuario → personal → contacto) y el mensaje muestra **el nombre del catálogo**.

* **Reenvío:** `enviar_grupo.py --reenviar` manda el grupo desde el inicio; la app **completa el autor** de los mensajes ya guardados que no lo tenían, y el texto de los que no se convirtieron en restricción o nota. Un mensaje ya convertido conserva su texto.
* **Número oculto:** si WhatsApp no da el celular de alguien (solo su código interno), el mensaje lleva su nombre de WhatsApp y se rotula «Número oculto por WhatsApp»; el código interno **no** se compara con el catálogo (sus últimos dígitos podrían coincidir con un celular ajeno). Quien gestiona puede completar su nombre, cargo y empresa con «Editar contacto».
* **Emisor desconocido:** solo si el puente tampoco tiene el autor (mensaje sin registro); nunca se inventa un celular.

**Menciones `@…` dentro del texto:** WhatsApp las manda con el código interno de la persona, no con su nombre. El script las cambia por el celular (o por el nombre de WhatsApp si no hay celular) y la app muestra **`@Nombre`** buscando el celular en el catálogo (últimos 9 dígitos); un celular sin nombre se ve `@+51…` y un código sin celular, `@contacto`. El texto que pasa a una restricción o nota ya lleva los nombres.

Los usuarios y el personal se editan donde ya viven (Usuarios, Personal), no en Fuente-WhatsApp: la lista de integrantes solo muestra su cargo o «Usuario del sistema» / «Personal de obra». Una restricción por WhatsApp lleva el nombre del usuario o del personal si el celular coincide; si no, el contacto externo; si no, el nombre que mostró WhatsApp.

## Restricciones-Notas: dos paneles

La pantalla Restricciones-Notas (`/proyectos/{id}/restricciones`) tiene dos paneles lado a lado:

* **Restricciones:** como siempre ([flujo 22](22-informes-de-supervision.md)); **se conservan crear, recepcionar y atender** (Victor, 2026-10-25: «vamos a dejarlo así»). Las que vienen de WhatsApp muestran «Desde WhatsApp — nombre (+celular)» y quién las registró y cuándo.
* **Notas:** hechos del servicio con su **día**, su origen (WhatsApp con emisor, o escrita a mano) y su vigencia. Las ven los 13 roles; escriben a mano y quitan validez administrador y jefe de proyectos. Una nota **pierde validez** cuando su información **ya está en un correo u otro apartado**: se marca «Ya está en…» con el motivo, queda tachada al final y **no se borra**. No se reactiva.

## Almacén de archivos

Los archivos de WhatsApp irán al almacén de **Cloudflare R2** de la app (ya en uso desde el 2026-11-05 para el resto de archivos). Mientras tanto el mensaje conserva el nombre, tipo, tamaño y huella del archivo y queda «pendiente de almacén» (389 al 2026-11-05); **la copia del archivo en sí no está implementada**, por eso la conversación rotula la foto o el documento pero no lo abre.

## Fuera de alcance por ahora

Clasificar o resumir con IA; copiar los archivos a R2 y verlos en la conversación; Fuente-Drive (paso 3).
