# 23 — Gestión de interesados (antes «Estado del servicio»)
> Lee si: la tarea toca el apartado «Gestión de interesados» (minutas de la reunión semanal con el cliente y correos del cliente por tema), la lectura de los correos de Gmail y sus horas, el anti-duplicado entre los dos buzones, la clasificación de un correo a un servicio, a un portafolio o a un tema, las notas y sus movimientos, «Por revisar», o la configuración de correos en `/admin/estado-servicio`.

Origen: plan [Estado del servicio](../02-trabajo-activo/01-planes/2026-10-24-estado-del-servicio.md) (pedido de Victor el 2026-10-24; proveedor de correo y alcance confirmados por él). Quién puede cada acción: tablas 1 y 2 del [flujo 14](14-accesos-y-restricciones.md), nota ¹⁹; no se repite aquí.

## Qué es

Un apartado por servicio (y uno por portafolio) donde se ve **qué ha pasado con cada tema** que el cliente trata por correo, y donde se guardan las **minutas** de la reunión semanal. Sirve para llegar a esa reunión sabiendo qué está enviado, aprobado, observado o sin respuesta, sin releer los correos.

El sistema **lee dos correos** (los que reciben casi lo mismo), decide a qué servicio pertenece cada mensaje y lo anota en un **tema** del servicio. No responde correos ni los modifica en Gmail.

## Pantallas

| Pantalla | Ruta | Contenido |
|---|---|---|
| Gestión de interesados | `/proyectos/{id}/estado-servicio` | Pestañas **Temas**, **Por revisar** y **Minutas**; filtros de fecha, movimiento y texto. Chip «Gestión de interesados» (id `estado-servicio`, requiere servicio, grupo Planificación). |
| Gestión de interesados del portafolio | `/programas/{id}/portafolios/{portafolioId}/estado-servicio` | Lo mismo para los correos que no son de un servicio concreto; sin minutas. Enlace «Gestión de interesados del portafolio» en la página del portafolio. |
| Correos del cliente (configuración) | `/admin/estado-servicio` | Conectar o desconectar correos de Gmail, pausar uno, limitar lo que se lee, **horas de lectura**, «Sincronizar ahora», registro de las últimas lecturas y qué piezas faltan en el servidor. Se abre con el icono «Correos del cliente» (sobre de correos) junto a Usuarios en la parte baja del panel izquierdo, y con el enlace del mismo nombre en el encabezado de las pantallas de inicio; ambos solo los ven administrador y jefe de proyectos. |

Cualquier correo se abre completo (asunto, remitente, destinatarios, buzones donde llegó, texto y **documentos adjuntos descargables**) en un panel lateral desde la nota o desde «Por revisar».

## De dónde salen los correos

* **Dos buzones de Gmail / Google Workspace** (decisión de Victor, 2026-10-24). Se conectan con permiso de **solo lectura** de Google; la app no guarda contraseñas. El permiso permanente se guarda **cifrado** (AES-256-GCM, clave en el servidor) y nunca se muestra.
* **Lectura automática dos veces al día, 7:00 y 14:00** (hora de Lima por defecto). El botón «Guardar horas» de la configuración cambia las horas (de 1 a 6); un disparador externo llama al servidor cada hora y el servidor decide si toca, así que cambiar una hora no exige volver a desplegar. Si una hora programada no corrió, se recupera durante las 12 horas siguientes; pasado ese margen la cubre el turno siguiente. La lectura automática se puede pausar.
* **Sincronizar ahora** lee en el momento. Cada lectura deja su registro (nuevos, copias, ubicados, por revisar, avisos).
* Cada corrida trae hasta 40 correos nuevos por buzón; si hay más, el resto entra en la siguiente.

## Un correo que llega a los dos buzones se analiza una sola vez

Se reconoce primero por su identificador de mensaje (es el mismo en ambos buzones) y, si no coincide, por una huella del contenido. El segundo ejemplar se guarda como **copia**: no se analiza, no crea nota y la nota del original recuerda que llegó a los dos buzones.

## A qué servicio y a qué tema va un correo

Se prueba en este orden y se detiene en el primero que acierte:

1. **Hilo:** si responde a una conversación ya ubicada, hereda su servicio y su tema.
2. **Reglas:** el código del servicio (`PS-####`) o su nombre en el asunto o el texto, y el nombre de un tema ya existente.
3. **Asistente de IA** (solo si está configurado en el servidor): propone servicio, tema, movimiento y resumen. Es una respuesta validada: lo que diga el correo se trata como dato, nunca como instrucción. Si su confianza es baja, no se acepta.
4. **Por revisar:** si nada alcanza, el correo queda sin ubicar para que una persona lo mueva a mano.

* **Sin servicio identificable → portafolio** (Servicios Marcobre, el portafolio por defecto).
* **Tema que no existe → el sistema lo crea** (queda marcado como creado automáticamente). Un correo ubicado sin tema claro va a **Por revisar**, no a un tema inventado.
* Lo que una persona mueve a mano queda marcado **manual** y ni las reglas ni la IA lo vuelven a tocar.

## Temas y notas

* Un **tema** (ejemplo: «PETS») pertenece a un servicio o a un portafolio, está **Abierto** o **Cerrado** y guarda su historial de notas, de la más reciente a la más antigua.
* Cada correo ubicado agrega una **nota** con su fecha, un resumen y el correo de origen. También se pueden escribir notas a mano.
* **Movimiento** de cada nota: **Enviado**, **Aprobado**, **Observado**, **Solicitud** o **Información**. El movimiento de la nota más reciente es el «estado» que se ve en el encabezado del tema (ejemplo: PETS — Observado).
* **Sin respuesta:** un tema abierto cuyo último movimiento fue **Enviado** o **Solicitud** y que lleva **3 días o más** sin novedad se marca para prepararlo antes de la reunión.
* Quitar una nota que vino de un correo devuelve ese correo a **Por revisar**.

## Filtros

Fecha **desde / hasta**, movimiento y texto (tema, nota o asunto). Por defecto se ven los **últimos 30 días**, para no cargar todo el histórico. Los mismos filtros de fecha aplican a las minutas.

## Minutas

Solo en servicios. Cada minuta lleva fecha de la reunión, título y un archivo (hasta 15 MB). Se descargan desde la pantalla; no se editan, se eliminan y se vuelven a subir.

## Reglas de seguridad

* Todo se valida en el servidor: rol, y para un servicio, tenerlo a cargo; un portafolio solo exige el rol. Los adjuntos se descargan con un enlace firmado de dos minutos.
* Los adjuntos de más de 10 MB y las imágenes diminutas de firmas no se guardan; el correo indica que no se guardó.
* El contenido de los correos nunca se ejecuta ni se obedece.

## Datos (migración `db/119_estado_servicio.sql`)

`estado_buzones`, `estado_configuracion` (fila única con las horas), `estado_temas`, `estado_correos`, `estado_adjuntos`, `estado_notas`, `estado_minutas` y `estado_sincronizaciones`. Las tablas tienen RLS activada sin políticas: solo el servidor las lee y escribe. Los archivos van al bucket `documentos-proyecto`, bajo `estado-servicio/`.

## Fuera de alcance

Responder correos desde la app, otros proveedores distintos de Gmail, WhatsApp y convertir las minutas en acuerdos con seguimiento (mejora futura).

## Para que lea correos reales

La pantalla y el servidor están construidos; la lectura real necesita lo que solo Victor puede dar: cliente OAuth de Google, clave de cifrado, secreto del disparador horario (y, opcional, la clave de la IA), más aplicar la migración. La pantalla de configuración muestra cuáles faltan. Hasta entonces la lectura real con Gmail y con la IA **no está probada**; las piezas puras (huella, horas, reglas, lectura del mensaje, cifrado) sí tienen pruebas automáticas.
