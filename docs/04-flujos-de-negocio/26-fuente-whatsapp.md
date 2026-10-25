# 26 — Fuente-WhatsApp
> Lee si: la tarea toca el apartado «Fuente-WhatsApp» (el grupo de WhatsApp del servicio, la bandeja «Por revisar», la sugerencia de pedido de campo / nota / archivo / sin importancia, los contactos por celular), el panel de **Notas** de Restricciones-Notas y su vigencia, el origen «WhatsApp» de una restricción con su emisor, o el script local que envía el grupo a la app.

Origen: plan [Fuente-WhatsApp](../02-trabajo-activo/01-planes/2026-10-25-fuente-whatsapp.md) (pedido de Victor el 2026-10-25; paso 2 de la reestructuración Fuentes / Gestión documentaria). Hermana de [Fuente-Gmail](23-estado-del-servicio.md) y de Fuente-Drive (pendiente). Quién puede cada acción: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md), nota 23; la lista de pantallas, en el [flujo 16](16-paneles.md). **Estado (2026-10-25): publicada; `db/122` aplicada; puente revinculado; grupo «Villa Fase 2» registrado y sus 337 mensajes ya en «Por revisar». Falta la copia de archivos a R2.**

## Qué es

Una pantalla por servicio (`/proyectos/{id}/fuente-whatsapp`, chip «Fuente-WhatsApp» en el grupo Planificación) que muestra lo que dice **el grupo de WhatsApp de ese servicio**. Cada mensaje llega ya **sugerido** y una persona lo **confirma con un clic**. Hoy hay **un solo grupo** («Villa Fase 2», servicio «Facilidades de Villa de Ejecución Fase 2»).

## De dónde salen los mensajes

Teléfono de Victor → **puente de WhatsApp** en su PC (`mcp_whatsapp`, vinculado como dispositivo con **su propio número**, **solo lectura**) → **script local** (`scripts/whatsapp/enviar_grupo.py` de la app, solo librería estándar de Python) → la app (`POST /api/fuente-whatsapp/ingresar`, protegida con el secreto `WHATSAPP_INGRESO_SECRETO`, sin sesión).

* **Privacidad:** el script toma **únicamente** el grupo configurado; la consulta filtra por el código del grupo y ningún otro chat del teléfono sale del PC. La app, además, **rechaza** cualquier lote cuyo grupo no esté registrado y activo en un servicio.
* **Registro del grupo:** administrador o jefe de proyectos escriben el código del grupo (termina en `@g.us`) en la pantalla; un grupo no puede estar en dos servicios. El grupo se puede pausar.
* **Idempotente:** cada mensaje se guarda una sola vez (por su id en WhatsApp). La misma información repetida por el mismo emisor en el mismo minuto entra ya **descartada**. Un fallo a medio envío se reintenta sin duplicar.
* **Envío automático:** una tarea de Windows en el PC de Victor ejecuta el script **cada 10 minutos** (solo con la sesión de Windows abierta y el puente corriendo); el secreto, el último mensaje enviado y el registro viven en una carpeta privada del PC, fuera de los repositorios.
* **Riesgos asumidos:** el puente usa una conexión **no oficial**; el teléfono debe abrir WhatsApp al menos cada ~14 días; el PC debe estar encendido para recibir.

## Qué se extrae

* **Imágenes y archivos:** siempre.
* **Texto:** solo si es relevante. El sistema **sugiere** con reglas simples (no IA): 
  * **Pedido de campo** si el texto pide, avisa que falta o impide algo («falta», «no hay», «necesitamos», «solicito», «urgente», «no llegó»…).
  * **Archivo** si trae imagen, documento o video (salvo que su texto pida algo: entonces pedido de campo).
  * **Nota** si informa un hecho (capacitación, charla, reunión, visita, «se realizó…»).
  * **Sin importancia** si es un saludo, «ok», «gracias», un texto muy corto o un audio.
  Cada sugerencia lleva su **confianza**; lo dudoso se sugiere como nota con poca confianza para que se revise. La sugerencia nunca decide sola: quien confirma puede cambiarla.

## La bandeja «Por revisar»

Cada mensaje muestra quién lo escribió (nombre y celular, con cargo y empresa si se conocen), cuándo, su texto o su archivo, y lo sugerido. Quien gestiona elige:

| Acción | Resultado |
|---|---|
| **Pedido de campo** (con prioridad Alta/Media/Baja) | Se crea una **restricción** del servicio con origen «WhatsApp», con el **celular y el nombre del emisor** y enlazada al mensaje. Avisa como cualquier restricción nueva ([flujo 22](22-informes-de-supervision.md)). |
| **Nota** | Se crea una **nota vigente** con el día del hecho (el del mensaje) en el panel de notas. |
| **Archivo** (con área o «Sin clasificar») | El mensaje queda como archivo con su área. **Su destino es Gestión documentaria** (flujo 25): áreas SSOMA, Oficina técnica, Calidad, Administración, Gerencia; sin área, «Sin clasificar». Mientras el almacén no esté listo queda «espera el almacén de archivos». |
| **Descartar** | Queda en «Revisados» como descartado. |

Un mensaje se confirma **una sola vez**: si dos personas lo hacen a la vez, gana una y la otra recibe un aviso; si crear el destino falla, el mensaje vuelve a «Por revisar».

## Quién es el emisor

Un mensaje trae el celular de quien lo escribió. Para saber quién es **no se duplica** lo que ya existe (Victor, 2026-10-25): se busca el celular, comparando los **últimos 9 dígitos** (WhatsApp lo manda con el código de país), en este orden:

1. **Usuarios del sistema** (perfiles): nombre y cargo.
2. **Personal de obra** (`recursos_personal`): nombre y cargo.
3. **Contacto externo de WhatsApp**: solo si no está en ninguna de las dos, se crea en la tabla propia de contactos (celular, nombre, cargo, empresa) con el nombre que muestra WhatsApp; quien gestiona completa nombre, cargo y empresa desde la bandeja.

**Emisor desconocido:** el historial que WhatsApp sincroniza al vincular el puente **no dice quién escribió** (el puente guarda entonces el código del propio grupo). Esos mensajes entran con emisor vacío y se muestran como «Emisor desconocido», sin celular ni «Editar contacto»; nunca se inventa un celular. Los mensajes **nuevos** sí traen al autor (si WhatsApp lo identifica con un código interno, el script lo cambia por su celular).

Los usuarios y el personal se editan donde ya viven (Usuarios, Personal), no en Fuente-WhatsApp: la bandeja solo muestra «Usuario del sistema» o «Personal de obra». Una restricción por WhatsApp lleva el nombre del usuario o del personal si el celular coincide; si no, el contacto externo; si no, el nombre que mostró WhatsApp.

## Restricciones-Notas: dos paneles

La pantalla Restricciones-Notas (`/proyectos/{id}/restricciones`) tiene dos paneles lado a lado:

* **Restricciones:** como siempre ([flujo 22](22-informes-de-supervision.md)); **se conservan crear, recepcionar y atender** (Victor, 2026-10-25: «vamos a dejarlo así»). Las que vienen de WhatsApp muestran «Desde WhatsApp — nombre (+celular)» y quién las registró y cuándo.
* **Notas:** hechos del servicio con su **día**, su origen (WhatsApp con emisor, o escrita a mano) y su vigencia. Las ven los 13 roles; escriben a mano y quitan validez administrador y jefe de proyectos. Una nota **pierde validez** cuando su información **ya está en un correo u otro apartado**: se marca «Ya está en…» con el motivo, queda tachada al final y **no se borra**. No se reactiva.

## Almacén de archivos

Los archivos de WhatsApp irán al mismo almacén de **Cloudflare R2** de la [Gestión documentaria](25-archivos-documentarios.md). R2 aún no está pagado ni configurado: hasta entonces el mensaje conserva el nombre, tipo, tamaño y huella del archivo y queda «pendiente de almacén»; **la copia del archivo en sí no está implementada**.

## Fuera de alcance por ahora

Clasificar con IA; copiar los archivos a R2; el árbol y el destino único de Gestión documentaria (paso 4); Fuente-Drive (paso 3).
